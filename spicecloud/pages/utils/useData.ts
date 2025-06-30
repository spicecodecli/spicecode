import { useState, useEffect } from 'react';
import { MetricData } from './types';

export const useData = () => {
  const [data, setData] = useState<MetricData[]>([]);
  const [selectedFile, setSelectedFile] = useState<MetricData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);

      // Adjust the route if your endpoint is different
      const res = await fetch('/api/files');
      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const json = await res.json();

      const files = json.map((f: any) => ({
        ...f,
        age: Date.now() - f.timestamp,
        readable_timestamp: new Date(f.timestamp).toLocaleString('pt-BR'),
        // If comment_ratio comes as string ("16.23%") and you prefer number:
        metrics: {
          ...f.metrics,
          comment_ratio: typeof f.metrics.comment_ratio === 'string'
            ? parseFloat(f.metrics.comment_ratio) / 100
            : f.metrics.comment_ratio
        }
      }));

      setData(files);
      if (files.length && !selectedFile) setSelectedFile(files[0]);
    } catch (err) {
      setError('Erro ao buscar dados');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 10000);
    return () => clearInterval(interval);
  }, []);

  return {
    data,
    selectedFile,
    setSelectedFile,
    loading,
    error,
    fetchData
  };
};