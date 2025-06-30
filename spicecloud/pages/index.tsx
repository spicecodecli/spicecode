
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
        // Only auto-select if no file is currently selected
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
    const interval = setInterval(fetchData, 10000); // Refresh every 10 seconds
    return () => clearInterval(interval);
  }, []);

  const formatMetricValue = (key: string, value: any): string => {
    if (typeof value === 'object' && value !== null) {
      return JSON.stringify(value, null, 2);
    }
    if (key.includes('ratio') && typeof value === 'number') {
      return `${(value * 100).toFixed(1)}%`;
    }
    return String(value);
  };

  const getMetricIcon = (key: string): string => {
    if (key.includes('line_count')) return '📄';
    if (key.includes('function_count')) return '⚡';
    if (key.includes('comment')) return '💬';
    if (key.includes('dependencies')) return '📦';
    if (key.includes('indentation')) return '📐';
    if (key.includes('method')) return '🔧';
    if (key.includes('ratio')) return '📊';
    return '📋';
  };

  const getMetricColor = (key: string): string => {
    if (key.includes('count') || key.includes('line')) return 'from-blue-500 to-blue-600';
    if (key.includes('ratio')) return 'from-green-500 to-green-600';
    if (key.includes('dependencies')) return 'from-orange-500 to-orange-600';
    if (key.includes('indentation')) return 'from-purple-500 to-purple-600';
    if (key.includes('method')) return 'from-pink-500 to-pink-600';
    return 'from-gray-500 to-gray-600';
  };

  const formatAge = (age: number): string => {
    const hours = Math.floor(age / (1000 * 60 * 60));
    const minutes = Math.floor((age % (1000 * 60 * 60)) / (1000 * 60));
    
    if (hours > 0) {
      return `${hours}h ${minutes}m ago`;
    }
    return `${minutes}m ago`;
  };

  const formatLabel = (key: string): string => {
    return key
      .replace(/_/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  if (loading && data.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center">
        <div className="text-center">
          <div className="relative">
            <div className="animate-spin rounded-full h-16 w-16 border-4 border-purple-500 border-t-transparent mx-auto"></div>
            <div className="absolute inset-0 rounded-full h-16 w-16 border-4 border-blue-500 border-b-transparent mx-auto animate-spin" style={{animationDirection: 'reverse', animationDuration: '1.5s'}}></div>
          </div>
          <p className="text-white/80 mt-6 text-lg">Loading your code metrics...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-red-900 to-slate-900 flex items-center justify-center">
        <div className="text-center bg-red-950/50 backdrop-blur-sm rounded-2xl p-8 border border-red-500/20">
          <div className="text-6xl mb-4">⚠️</div>
          <p className="text-red-200 text-xl mb-4">{error}</p>
          <button 
            onClick={fetchData}
            className="px-6 py-3 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition-all duration-200 hover:scale-105"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }

  if (data.length === 0) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex items-center justify-center p-4">
        <div className="text-center max-w-md">
          <div className="text-8xl mb-6 animate-bounce">📊</div>
          <h1 className="text-3xl font-bold text-white mb-4">Ready for Analysis!</h1>
          <p className="text-white/70 mb-6 text-lg leading-relaxed">
            Start analyzing your code files to see beautiful metrics here.
          </p>
          <div className="bg-gray-900/80 backdrop-blur text-green-400 p-6 rounded-xl font-mono text-sm border border-green-500/20">
            <div className="text-green-300 mb-2"># Run your analyzer:</div>
            <div className="text-white">python -m cli.main analyze file.py</div>
          </div>
          <button 
            onClick={fetchData}
            className="mt-6 px-6 py-3 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-medium transition-all duration-200 hover:scale-105"
          >
            🔄 Check for Updates
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet"></link> */}
      {/* Header */}
      <div className="bg-black/20 backdrop-blur-sm border-b border-white/10 sticky top-0 z-40">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                <span className="text-3xl">📊</span>
                Code Quality Dashboard
              </h1>
              <p className="text-white/60 mt-1">{data.length} files analyzed</p>
            </div>
            <button 
              onClick={fetchData}
              disabled={loading}
              className={`px-4 py-2 rounded-lg font-medium transition-all duration-200 ${
                loading 
                  ? 'bg-gray-700 text-gray-400 cursor-not-allowed' 
                  : 'bg-purple-600 hover:bg-purple-700 text-white hover:scale-105'
              }`}
            >
              {loading ? '🔄 Updating...' : '🔄 Refresh'}
            </button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-6 py-8">
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-8">
          {/* File Selector Sidebar */}
          <div className="xl:col-span-1">
            <div className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 border border-white/20 sticky top-24">
              <h2 className="text-xl font-semibold text-white mb-6 flex items-center gap-2">
                <span>📁</span>
                Analyzed Files
              </h2>
              <div className="space-y-3 max-h-[60vh] overflow-y-auto custom-scrollbar">
                {data.map((item) => (
                  <div
                    key={item.id}
                    onClick={() => setSelectedFile(item)}
                    className={`group p-4 rounded-xl cursor-pointer transition-all duration-200 hover:scale-[1.02] ${
                      selectedFile?.id === item.id 
                        ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg shadow-purple-500/25 scale-[1.02]' 
                        : 'bg-white/5 hover:bg-white/10 text-white/80 hover:text-white border border-white/10'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      <div className="text-xl">
                        {item.metrics.file_extension === '.py' ? '🐍' : 
                         item.metrics.file_extension === '.js' ? '🟨' :
                         item.metrics.file_extension === '.ts' ? '🔷' :
                         item.metrics.file_extension === '.jsx' ? '⚛️' :
                         item.metrics.file_extension === '.tsx' ? '⚛️' : '📄'}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-medium truncate text-sm" title={item.file_name}>
                          {item.file_name}
                        </div>
                        <div 
                          className={`text-xs truncate mt-1 ${
                            selectedFile?.id === item.id ? 'text-white/80' : 'text-white/50'
                          }`} 
                          title={item.file_path}
                        >
                          {item.file_path.replace(item.file_name, '')}
                        </div>
                        <div className={`text-xs mt-2 flex items-center gap-2 ${
                          selectedFile?.id === item.id ? 'text-white/70' : 'text-white/40'
                        }`}>
                          <span>🕒</span>
                          {formatAge(item.age)}
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Metrics Display */}
          <div className="xl:col-span-3">
            {selectedFile ? (
              <div className="space-y-6">
                {/* File Header */}
                <div className="bg-gradient-to-r from-white/10 to-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/20">
                  <div className="flex items-start gap-4">
                    <div className="text-4xl">
                      {selectedFile.metrics.file_extension === '.py' ? '🐍' : 
                       selectedFile.metrics.file_extension === '.js' ? '🟨' :
                       selectedFile.metrics.file_extension === '.ts' ? '🔷' :
                       selectedFile.metrics.file_extension === '.jsx' ? '⚛️' :
                       selectedFile.metrics.file_extension === '.tsx' ? '⚛️' : '📄'}
                    </div>
                    <div className="flex-1">
                      <h2 className="text-2xl font-bold text-white mb-2">{selectedFile.file_name}</h2>
                      <p className="text-white/60 text-sm mb-2" title={selectedFile.file_path}>
                        📁 {selectedFile.file_path}
                      </p>
                      <div className="flex items-center gap-4 text-sm text-white/50">
                        <span>🕒 {selectedFile.readable_timestamp}</span>
                        <span>💾 {selectedFile.metrics.file_size ? `${(selectedFile.metrics.file_size / 1024).toFixed(1)} KB` : 'N/A'}</span>
                        <span>📂 {selectedFile.metrics.file_extension || 'N/A'}</span>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Metrics Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {Object.entries(selectedFile.metrics).map(([key, value]) => {
                    // Skip file info metrics as they're shown in header
                    if (['file_name', 'file_path', 'file_size', 'file_extension'].includes(key)) {
                      return null;
                    }

                    if (key === 'method_type_count' && typeof value === 'object' && value !== null) {
                      return (
                        <div key={key} className="bg-gradient-to-br from-pink-500/20 to-purple-500/20 backdrop-blur-sm rounded-2xl p-6 border border-pink-500/20 hover:scale-105 transition-all duration-200">
                          <div className="flex items-center gap-3 mb-4">
                            <span className="text-2xl">🔧</span>
                            <h3 className="font-semibold text-white text-lg">Method Types</h3>
                          </div>
                          <div className="space-y-3">
                            <div className="flex items-center justify-between p-3 bg-white/10 rounded-lg">
                              <div className="flex items-center gap-2">
                                <span className="w-3 h-3 bg-green-500 rounded-full"></span>
                                <span className="text-white/80">Public</span>
                              </div>
                              <span className="text-xl font-bold text-white">{(value as any).public}</span>
                            </div>
                            <div className="flex items-center justify-between p-3 bg-white/10 rounded-lg">
                              <div className="flex items-center gap-2">
                                <span className="w-3 h-3 bg-blue-500 rounded-full"></span>
                                <span className="text-white/80">Private</span>
                              </div>
                              <span className="text-xl font-bold text-white">{(value as any).private}</span>
                            </div>
                          </div>
                        </div>
                      );
                    }

                    // Special handling for indentation
                    if (key === 'indentation_type' || key === 'indentation_size') {
                      return null; // We'll handle these together
                    }

                    return (
                      <div 
                        key={key} 
                        className={`bg-gradient-to-br ${getMetricColor(key)}/20 backdrop-blur-sm rounded-2xl p-6 border border-white/20 hover:scale-105 transition-all duration-200 group`}
                      >
                        <div className="flex items-center gap-3 mb-4">
                          <span className="text-2xl group-hover:scale-110 transition-transform duration-200">
                            {getMetricIcon(key)}
                          </span>
                          <h3 className="font-semibold text-white text-lg">
                            {formatLabel(key)}
                          </h3>
                        </div>
                        <div className="text-3xl font-bold text-white mb-2">
                          {formatMetricValue(key, value)}
                        </div>
                        {key.includes('ratio') && (
                          <div className="w-full bg-white/20 rounded-full h-2 mt-3">
                            <div 
                              className="bg-gradient-to-r from-green-400 to-green-600 h-2 rounded-full transition-all duration-1000"
                              style={{width: `${Math.min((value as number) * 100, 100)}%`}}
                            ></div>
                          </div>
                        )}
                      </div>
                    );
                  })}

                  {/* Special indentation card */}
                  {(selectedFile.metrics.indentation_type || selectedFile.metrics.indentation_size) && (
                    <div className="bg-gradient-to-br from-purple-500/20 to-indigo-500/20 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/20 hover:scale-105 transition-all duration-200">
                      <div className="flex items-center gap-3 mb-4">
                        <span className="text-2xl">📐</span>
                        <h3 className="font-semibold text-white text-lg">Indentation</h3>
                      </div>
                      <div className="space-y-3">
                        <div className="flex justify-between items-center">
                          <span className="text-white/80">Type:</span>
                          <span className="text-lg font-semibold text-white">
                            {selectedFile.metrics.indentation_type || 'N/A'}
                          </span>
                        </div>
                        <div className="flex justify-between items-center">
                          <span className="text-white/80">Size:</span>
                          <span className="text-lg font-semibold text-white">
                            {selectedFile.metrics.indentation_size || 'N/A'}
                          </span>
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            ) : (
              <div className="flex items-center justify-center h-96">
                <div className="text-center">
                  <div className="text-6xl mb-4 opacity-50">👆</div>
                  <p className="text-white/60 text-xl">Select a file from the sidebar to view its metrics</p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(255, 255, 255, 0.1);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(147, 51, 234, 0.8);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(147, 51, 234, 1);
        }
      `}</style>
    </div>
  );
}