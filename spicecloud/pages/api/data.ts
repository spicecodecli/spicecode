import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs';
import path from 'path';

const DATA_FILE = path.join(process.cwd(), 'data', 'metrics.json');

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

function cleanOldData(data: MetricData[]): MetricData[] {
  const sevenDaysAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
  return data.filter(item => item.timestamp > sevenDaysAgo);
}

function saveData(data: MetricData[]): void {
  fs.writeFileSync(DATA_FILE, JSON.stringify(data, null, 2));
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'GET') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Load and clean data
    let data = loadData();
    const originalLength = data.length;
    data = cleanOldData(data);
    
    // Save cleaned data if we removed any old entries
    if (data.length !== originalLength) {
      saveData(data);
      console.log(`Cleaned ${originalLength - data.length} old entries`);
    }

    // Sort by timestamp (newest first)
    data.sort((a, b) => b.timestamp - a.timestamp);

    res.status(200).json({
      success: true,
      data: data.map(item => ({
        ...item,
        age: Date.now() - item.timestamp,
        readable_timestamp: new Date(item.timestamp).toLocaleString()
      }))
    });

  } catch (error) {
    console.error('Error loading data:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}