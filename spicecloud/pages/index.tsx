import { useState, useEffect } from 'react';

interface MetricData {
  id: string;
  hash: string;
  timestamp: number;
  file_name: string;
  file_path: string;
  metrics: any;
  age: number;
  readable_timestamp: string;
}

export default function Home() {
  const [data, setData] = useState<MetricData[]>([]);
  const [selectedFile, setSelectedFile] = useState<MetricData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/data');
      const result = await response.json();
      
      if (result.success) {
        setData(result.data);
        if (result.data.length > 0 && !selectedFile) {
          setSelectedFile(result.data[0]);
        }
      } else {
        setError('Failed to load data');
      }
    } catch (err) {
      setError('Error fetching data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const formatMetricValue = (key: string, value: any): string => {
    if (typeof value === 'object' && value !== null) {
      return JSON.stringify(value, null, 2);
    }
    if (key.includes('ratio') && typeof value === 'number') {
      return `${(value * 100).toFixed(2)}%`;
    }
    return String(value);
  };

  const getMetricColor = (key: string): string => {
    if (key.includes('count') || key.includes('line')) return 'text-blue-600';
    if (key.includes('ratio')) return 'text-green-600';
    if (key.includes('dependencies')) return 'text-orange-600';
    if (key.includes('indentation')) return 'text-purple-600';
    return 'text-gray-600';
  };

  const formatAge = (age: number): string => {
    const hours = Math.floor(age / (1000 * 60 * 60));
    const minutes = Math.floor((age % (1000 * 60 * 60)) / (1000 * 60));
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ago`;
    }
    return `${minutes}m ago`;
  };

  if (loading && data.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading metrics data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center text-red-600">
          <p className="text-xl mb-4">⚠️ {error}</p>
          <button 
            onClick={fetchData}
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-6xl mb-4">📊</div>
          <h1 className="text-2xl font-bold text-gray-800 mb-2">No Analysis Data Yet</h1>
          <p className="text-gray-600 mb-4">
            Run your CLI analyzer and submit data to see metrics here.
          </p>
          <div className="bg-gray-800 text-green-400 p-4 rounded-lg text-left font-mono text-sm max-w-md">
            <p># Example usage:</p>
            <p>python -m cli.main analyze file.py --json</p>
          </div>
          <button 
            onClick={fetchData}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Refresh
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Code Quality Metrics Dashboard</h1>
          <div className="flex items-center gap-4">
            <p className="text-gray-600">{data.length} files analyzed</p>
            <button 
              onClick={fetchData}
              className={`px-3 py-1 rounded text-sm ${loading ? 'bg-gray-300' : 'bg-blue-600 hover:bg-blue-700'} text-white`}
              disabled={loading}
            >
              {loading ? 'Refreshing...' : 'Refresh'}
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* File List */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-4">Analyzed Files</h2>
              <div className="space-y-2 max-h-96 overflow-y-auto">
                {data.map((item) => (
                  <div
                    key={item.id}
                    onClick={() => setSelectedFile(item)}
                    className={`p-3 rounded-lg cursor-pointer transition-colors ${
                      selectedFile?.id === item.id 
                        ? 'bg-blue-100 border-2 border-blue-300' 
                        : 'bg-gray-50 hover:bg-gray-100 border-2 border-transparent'
                    }`}
                  >
                    <div className="font-medium text-sm text-gray-900 truncate" title={item.file_name}>
                      {item.file_name}
                    </div>
                    <div className="text-xs text-gray-500 truncate" title={item.file_path}>
                      {item.file_path}
                    </div>
                    <div className="text-xs text-gray-400 mt-1">
                      {formatAge(item.age)}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Metrics Details */}
          <div className="lg:col-span-2">
            {selectedFile ? (
              <div className="bg-white rounded-lg shadow-md p-6">
                <div className="mb-6">
                  <h2 className="text-xl font-semibold text-gray-900 mb-2">{selectedFile.file_name}</h2>
                  <p className="text-sm text-gray-600 mb-2" title={selectedFile.file_path}>
                    📁 {selectedFile.file_path}
                  </p>
                  <p className="text-sm text-gray-500">
                    🕒 Analyzed {selectedFile.readable_timestamp}
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(selectedFile.metrics).map(([key, value]) => {
                    if (key === 'method_type_count' && typeof value === 'object' && value !== null) {
                      return (
                        <div key={key} className="bg-gray-50 rounded-lg p-4">
                          <h3 className="font-medium text-gray-900 mb-2">Method Types</h3>
                          <div className="space-y-1">
                            <div className="flex justify-between">
                              <span className="text-sm text-gray-600">Public:</span>
                              <span className="text-sm font-medium text-green-600">{(value as any).public}</span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-sm text-gray-600">Private:</span>
                              <span className="text-sm font-medium text-blue-600">{(value as any).private}</span>
                            </div>
                          </div>
                        </div>
                      );
                    }

                    return (
                      <div key={key} className="bg-gray-50 rounded-lg p-4">
                        <h3 className="font-medium text-gray-900 mb-1 capitalize">
                          {key.replace(/_/g, ' ')}
                        </h3>
                        <p className={`text-lg font-semibold ${getMetricColor(key)}`}>
                          {formatMetricValue(key, value)}
                        </p>
                      </div>
                    );
                  })}

                  {/* File Info */}
                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-medium text-gray-900 mb-1">File Size</h3>
                    <p className="text-lg font-semibold text-gray-600">
                      {selectedFile.metrics.file_size ? `${(selectedFile.metrics.file_size / 1024).toFixed(2)} KB` : 'N/A'}
                    </p>
                  </div>

                  <div className="bg-gray-50 rounded-lg p-4">
                    <h3 className="font-medium text-gray-900 mb-1">File Extension</h3>
                    <p className="text-lg font-semibold text-gray-600">
                      {selectedFile.metrics.file_extension || 'N/A'}
                    </p>
                  </div>
                </div>
              </div>
            ) : (
              <div className="bg-white rounded-lg shadow-md p-6 text-center">
                <p className="text-gray-500">Select a file to view its metrics</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}