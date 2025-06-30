import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

const DATA_DIR = path.join(process.cwd(), 'data');
const DATA_FILE = path.join(DATA_DIR, 'metrics.json');

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

interface MetricData {
  id: string;
  hash: string;
  timestamp: number;
  file_name: string;
  file_path: string;
  metrics: any;
}

function loadData(): MetricData[] {
  if (!fs.existsSync(DATA_FILE)) {
    return [];
  }
  try {
    const data = fs.readFileSync(DATA_FILE, 'utf8');
    return JSON.parse(data);
  } catch {
    return [];
  }
}

function saveData(data: MetricData[]): void {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

function cleanOldData(data: MetricData[]): MetricData[] {
  const sevenDaysAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
  return data.filter(item => item.timestamp > sevenDaysAgo);
}

function generateHash(filePath: string, fileSize: number, metrics: any): string {
  const hashData = JSON.stringify({ filePath, fileSize, metrics });
  return crypto.createHash('md5').update(hashData).digest('hex');
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { file_path, file_name, file_size, ...metrics } = req.body;

    if (!file_path || !file_name) {
      return res.status(400).json({ error: 'file_path and file_name are required' });
    }

    // Generate hash for deduplication
    const hash = generateHash(file_path, file_size || 0, metrics);
    
    // Load existing data and clean old entries
    let data = loadData();
    data = cleanOldData(data);

    // Check if this exact analysis already exists
    const existingIndex = data.findIndex(item => 
      item.file_path === file_path && item.hash === hash
    );

    const newEntry: MetricData = {
      id: crypto.randomUUID(),
      hash,
      timestamp: Date.now(),
      file_name,
      file_path,
      metrics
    };

    if (existingIndex !== -1) {
      // Update existing entry with new timestamp
      data[existingIndex] = newEntry;
      console.log(`Updated existing analysis for: ${file_path}`);
    } else {
      // Remove any old analysis for this file and add new one
      data = data.filter(item => item.file_path !== file_path);
      data.push(newEntry);
      console.log(`Added new analysis for: ${file_path}`);
    }

    saveData(data);

    res.status(200).json({ 
      success: true, 
      message: 'Data submitted successfully',
      id: newEntry.id,
      isDuplicate: existingIndex !== -1
    });

  } catch (error) {
    console.error('Error processing submission:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}