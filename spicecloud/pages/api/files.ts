// pages/api/files.ts
import { promises as fs } from 'fs';
import path from 'path';

export default async function handler(req: any, res: { status: (arg0: number) => { (): any; new(): any; json: { (arg0: { error: string; }): void; new(): any; }; }; }) {
  try {
    const filePath = path.join(process.cwd(), 'data', 'metrics.json');
    const fileContent = await fs.readFile(filePath, 'utf-8');
    const jsonData = JSON.parse(fileContent);
    res.status(200).json(jsonData);
  } catch (err) {
    console.error('Erro ao ler metrics.json', err);
    res.status(500).json({ error: 'Failed to load metrics.json' });
  }
}
