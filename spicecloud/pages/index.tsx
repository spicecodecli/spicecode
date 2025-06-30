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

const getFileIconSrc = (ext: string): string => {
  switch (ext) {
    case '.py':  return '/python-logo.png';
    case '.js':  return '/javascript-logo.png';
    case '.rb':  return '/ruby-logo.png';
    case '.go':  return '/go-logo.png';
    default:     return '/file-icon.png';
  }
};

export default function Home() {
  const [data, setData] = useState<MetricData[]>([]);
  const [selectedFile, setSelectedFile] = useState<MetricData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

const fetchData = async () => {
  try {
    setLoading(true);

    // ‼ ajuste a rota se o seu endpoint for diferente
    const res  = await fetch('/api/files');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);

    const json = await res.json();           

    const files = json.map((f: any) => ({
      ...f,
      age: Date.now() - f.timestamp,
      readable_timestamp: new Date(f.timestamp).toLocaleString('pt-BR'),
      // se comment_ratio vier como string (“16.23%”) e você preferir número:
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
  if (key.includes('count') || key.includes('line')) 
    return 'linear-gradient(135deg, #e3d6b0, #c9b67a)'; // lighter sand
  if (key.includes('ratio')) 
    return 'linear-gradient(135deg, #d97304, #a35402)'; // spice orange
  if (key.includes('dependencies')) 
    return 'linear-gradient(135deg, #a67c23, #6b4c1b)'; // brown earth
  if (key.includes('indentation')) 
    return 'linear-gradient(135deg, #d7b377, #f0e3c8)'; // light sand
  if (key.includes('method')) 
    return 'linear-gradient(135deg, #a35402, #d97304)'; // spice orange
  return 'linear-gradient(135deg, #6b4c1b, #4a2c0b)'; // darker earth tones
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

  const styles = {
  container: {
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #f0e3c8, #e3d6b0, #d7b377)', // lighter sand gradient
    fontFamily: 'system-ui, -apple-system, sans-serif',
    color: '#000000' // black text globally
  },
  header: {
    background: 'rgba(215, 179, 119, 0.9)', // light sand with opacity for clarity
    backdropFilter: 'blur(10px)',
    borderBottom: '1px solid rgba(160, 130, 60, 0.8)', // darker sand border
    position: 'sticky' as const,
    top: 0,
    zIndex: 40,
    padding: '1rem 1.5rem',
    color: '#000000',
  },
  headerContent: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    maxWidth: '1200px',
    margin: '0 auto'
  },
  title: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    color: '#000000',
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem'
  },
  subtitle: {
    color: 'rgba(0, 0, 0, 0.7)',
    marginTop: '0.25rem'
  },
  refreshButton: {
    padding: '0.5rem 1rem',
    borderRadius: '0.5rem',
    fontWeight: '500',
    transition: 'all 0.2s',
    border: 'none',
    cursor: 'pointer',
    background: loading ? '#bfa865' : '#d97304', // lighter brown / orange
    color: '#000000',
  },
  mainContent: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '2rem 1.5rem',
    display: 'grid',
    gridTemplateColumns: 'minmax(300px, 1fr) 2fr',
    gap: '2rem'
  },
  sidebar: {
    background: 'rgba(215, 179, 119, 0.25)',
    backdropFilter: 'blur(10px)',
    borderRadius: '1rem',
    padding: '1.5rem',
    border: '1px solid rgba(160, 130, 60, 0.5)',
    height: 'fit-content',
    position: 'sticky' as const,
    top: '6rem',
    color: '#000000'
  },
  sidebarTitle: {
    fontSize: '1.25rem',
    fontWeight: '600',
    color: '#000000',
    marginBottom: '1.5rem',
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem'
  },
  fileList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.75rem',
    maxHeight: '60vh',
    overflowY: 'auto' as const
  },
  fileItem: {
    padding: '1rem',
    borderRadius: '0.75rem',
    cursor: 'pointer',
    transition: 'all 0.2s',
    border: '1px solid rgba(160, 130, 60, 0.3)',
    background: 'rgba(215, 179, 119, 0.1)',
    color: '#000000',
  },
  fileItemSelected: {
    background: 'linear-gradient(45deg, #d97304, #a35402)',
    color: '#000000',
    transform: 'scale(1.02)',
    boxShadow: '0 10px 25px rgba(217, 115, 4, 0.5)'
  },
  fileItemDefault: {
    background: 'rgba(215, 179, 119, 0.1)',
    color: '#000000'
  },
  fileInfo: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '0.75rem'
  },
  fileIcon: {
    fontSize: '1.25rem'
  },
  fileName: {
    fontWeight: '500',
    fontSize: '0.875rem',
    marginBottom: '0.25rem'
  },
  filePath: {
    fontSize: '0.75rem',
    opacity: 0.7,
    marginBottom: '0.5rem'
  },
  fileAge: {
    fontSize: '0.75rem',
    opacity: 0.7,
    display: 'flex',
    alignItems: 'center',
    gap: '0.25rem'
  },
  metricsArea: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '1.5rem'
  },
  fileHeader: {
    background: 'linear-gradient(135deg, rgba(215, 179, 119, 0.3), rgba(160, 130, 60, 0.2))',
    backdropFilter: 'blur(10px)',
    borderRadius: '1rem',
    padding: '1.5rem',
    border: '1px solid rgba(160, 130, 60, 0.5)',
    color: '#000000'
  },
  fileHeaderContent: {
    display: 'flex',
    alignItems: 'flex-start',
    gap: '1rem'
  },
  fileHeaderIcon: {
    fontSize: '2.5rem'
  },
  fileHeaderTitle: {
    fontSize: '1.5rem',
    fontWeight: 'bold',
    color: '#000000',
    marginBottom: '0.5rem'
  },
  fileHeaderPath: {
    color: 'rgba(0, 0, 0, 0.7)',
    fontSize: '0.875rem',
    marginBottom: '0.5rem'
  },
  fileHeaderMeta: {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
    fontSize: '0.875rem',
    color: 'rgba(0, 0, 0, 0.5)'
  },
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '1.5rem'
  },
  metricCard: {
    borderRadius: '1rem',
    padding: '1.5rem',
    border: '1px solid rgba(160, 130, 60, 0.5)',
    backdropFilter: 'blur(10px)',
    background: 'rgba(217, 115, 4, 0.15)',
    transition: 'all 0.2s',
    cursor: 'default',
    color: '#000000'
  },
  metricHeader: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.75rem',
    marginBottom: '1rem',
    color: '#000000'
  },
  metricIcon: {
    fontSize: '1.5rem',
    transition: 'transform 0.2s'
  },
  metricTitle: {
    fontWeight: '600',
    color: '#000000',
    fontSize: '1.125rem'
  },
  metricValue: {
    fontSize: '2rem',
    fontWeight: 'bold',
    color: '#000000',
    marginBottom: '0.5rem'
  },
  progressBar: {
    width: '100%',
    height: '0.5rem',
    background: 'rgba(160, 130, 60, 0.3)',
    borderRadius: '0.25rem',
    marginTop: '0.75rem',
    overflow: 'hidden'
  },
  progressFill: {
    height: '100%',
    background: 'linear-gradient(90deg, #d97304, #a35402)',
    borderRadius: '0.25rem',
    transition: 'width 1s ease'
  },
  methodTypeCard: {
    background: 'linear-gradient(135deg, rgba(217, 115, 4, 0.2), rgba(161, 84, 2, 0.2))',
    border: '1px solid rgba(217, 115, 4, 0.2)',
    color: '#000000'
  },
  methodTypeList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.75rem'
  },
  methodTypeItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '0.75rem',
    background: 'rgba(160, 130, 60, 0.1)',
    borderRadius: '0.5rem',
    color: '#000000'
  },
  methodTypeLabel: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem'
  },
  methodTypeDot: {
    width: '0.75rem',
    height: '0.75rem',
    borderRadius: '50%'
  },
  methodTypeText: {
    color: '#000000'
  },
  methodTypeValue: {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    color: '#000000'
  },
  indentationCard: {
    background: 'linear-gradient(135deg, rgba(217, 115, 4, 0.2), rgba(161, 84, 2, 0.2))',
    border: '1px solid rgba(217, 115, 4, 0.2)',
    color: '#000000'
  },
  indentationList: {
    display: 'flex',
    flexDirection: 'column' as const,
    gap: '0.75rem'
  },
  indentationItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    color: '#000000'
  },
  indentationLabel: {
    color: '#000000'
  },
  indentationValue: {
    fontSize: '1.125rem',
    fontWeight: '600',
    color: '#000000'
  },
  loading: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '100vh',
    background: 'linear-gradient(135deg, #f0e3c8, #e3d6b0, #d7b377)',
    color: '#000000'
  },
  loadingSpinner: {
    width: '4rem',
    height: '4rem',
    border: '4px solid rgba(217, 115, 4, 0.3)',
    borderTop: '4px solid #d97304',
    borderRadius: '50%',
    animation: 'spin 1s linear infinite'
  },
  emptyState: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    height: '24rem',
    color: '#000000'
  },
  emptyStateContent: {
    textAlign: 'center' as const
  },
  emptyStateIcon: {
    fontSize: '3.75rem',
    marginBottom: '1rem',
    opacity: 0.5
  },
  emptyStateText: {
    color: 'rgba(0, 0, 0, 0.7)',
    fontSize: '1.25rem'
  },
  fileIconImg: { width: '1.5rem', height: '1.5rem', objectFit: 'contain' as const },
  fileHeaderImg: { width: '3rem', height: '3rem', objectFit: 'contain' as const }
};



  if (loading && data.length === 0) {
    return (
      <div style={styles.loading}>
        <div style={{ textAlign: 'center' }}>
          <div style={styles.loadingSpinner}></div>
          <p style={{ marginTop: '1.5rem', fontSize: '1.125rem' }}>Loading your code metrics...</p>
        </div>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
          
          .metric-card:hover .metric-icon {
            transform: scale(1.1);
          }
        `}
      </style>
      
      {/* Header */}
<div style={styles.header}>
  <div style={styles.headerContent}>
    <div>
      <h1 style={styles.title}>
        <img 
          src="/spicecode-logo.png" 
          alt="SpiceCode Logo" 
          style={{ width: '3rem', height: '3rem', verticalAlign: 'middle', marginRight: '0.5rem' }}
        />
        SpiceCloud | Powered by SpiceCodeCLI
      </h1>
      <p style={styles.subtitle}>{data.length} files analyzed</p>
    </div>
    <button 
      onClick={fetchData}
      disabled={loading}
      style={{
        ...styles.refreshButton,
        ...(loading ? {} : { ':hover': { background: '#6d28d9' } })
      }}
    >
      {loading ? '🔄 Updating...' : '🔄 Refresh'}
    </button>
  </div>
</div>
      

      <div style={styles.mainContent}>
  {/* Sidebar */}
  <div style={styles.sidebar}>
    <h2 style={styles.sidebarTitle}>
      <span>📁</span>
      Analyzed Files
    </h2>
    <div style={styles.fileList}>
      {data.map((item) => (
        <div
          key={item.id}
          onClick={() => setSelectedFile(item)}
          style={{
            ...styles.fileItem,
            ...(selectedFile?.id === item.id
              ? styles.fileItemSelected
              : styles.fileItemDefault)
          }}
          className="file-item"
          onMouseEnter={(e) => {
            if (selectedFile?.id !== item.id) {
              e.currentTarget.style.background = 'rgba(255, 255, 255, 0.1)';
            }
          }}
          onMouseLeave={(e) => {
            if (selectedFile?.id !== item.id) {
              e.currentTarget.style.background = 'rgba(255, 255, 255, 0.05)';
            }
          }}
        >
          <div style={styles.fileInfo}>
            <div style={styles.fileIcon}>
              <img
                src={getFileIconSrc(item.metrics.file_extension)}
                alt={item.metrics.file_extension}
                style={styles.fileIconImg}
              />
            </div>

            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={styles.fileName} title={item.file_name}>
                {item.file_name}
              </div>
              <div style={styles.filePath} title={item.file_path}>
                {item.file_path.replace(item.file_name, '')}
              </div>
              <div style={styles.fileAge}>
                <span>🕒</span>
                {formatAge(item.age)}
              </div>
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>

        {/* Metrics Display */}
        <div style={styles.metricsArea}>
          {selectedFile ? (
            <>
              {/* File Header */}
              <div style={styles.fileHeader}>
                <div style={styles.fileHeaderContent}>
                  <div style={styles.fileHeaderIcon}>
  <img
    src={getFileIconSrc(selectedFile.metrics.file_extension)}
    alt={selectedFile.metrics.file_extension}
    style={styles.fileHeaderImg}
  />
</div>

                  <div style={{ flex: 1 }}>
                    <h2 style={styles.fileHeaderTitle}>{selectedFile.file_name}</h2>
                    <p style={styles.fileHeaderPath} title={selectedFile.file_path}>
                      📁 {selectedFile.file_path}
                    </p>
                    <div style={styles.fileHeaderMeta}>
                      <span>🕒 {selectedFile.readable_timestamp}</span>
                      <span>💾 {selectedFile.metrics.file_size ? `${(selectedFile.metrics.file_size / 1024).toFixed(1)} KB` : 'N/A'}</span>
                      <span>📂 {selectedFile.metrics.file_extension || 'N/A'}</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Metrics Grid */}
              <div style={styles.metricsGrid}>
                {Object.entries(selectedFile.metrics).map(([key, value]) => {
                  // Skip file info metrics
                  if (['file_name', 'file_path', 'file_size', 'file_extension'].includes(key)) {
                    return null;
                  }

                  if (key === 'method_type_count' && typeof value === 'object' && value !== null) {
                    return (
                      <div 
                        key={key} 
                        style={{ ...styles.metricCard, ...styles.methodTypeCard }}
                        className="metric-card"
                      >
                        <div style={styles.metricHeader}>
                          <span style={styles.metricIcon} className="metric-icon">🔧</span>
                          <h3 style={styles.metricTitle}>Method Types</h3>
                        </div>
                        <div style={styles.methodTypeList}>
                          <div style={styles.methodTypeItem}>
                            <div style={styles.methodTypeLabel}>
                              <span style={{ ...styles.methodTypeDot, background: '#10b981' }}></span>
                              <span style={styles.methodTypeText}>Public</span>
                            </div>
                            <span style={styles.methodTypeValue}>{(value as any).public}</span>
                          </div>
                          <div style={styles.methodTypeItem}>
                            <div style={styles.methodTypeLabel}>
                              <span style={{ ...styles.methodTypeDot, background: '#3b82f6' }}></span>
                              <span style={styles.methodTypeText}>Private</span>
                            </div>
                            <span style={styles.methodTypeValue}>{(value as any).private}</span>
                          </div>
                        </div>
                      </div>
                    );
                  }

                  if (key === 'indentation_type' || key === 'indentation_size') {
                    return null;
                  }

                  return (
                    <div 
                      key={key} 
                      style={{ 
                        ...styles.metricCard, 
                        background: getMetricColor(key).replace('135deg', '135deg') + '20'
                      }}
                      className="metric-card"
                      onMouseEnter={(e) => {
                        e.currentTarget.style.transform = 'scale(1.05)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.transform = 'scale(1)';
                      }}
                    >
                      <div style={styles.metricHeader}>
                        <span style={styles.metricIcon} className="metric-icon">
                          {getMetricIcon(key)}
                        </span>
                        <h3 style={styles.metricTitle}>
                          {formatLabel(key)}
                        </h3>
                      </div>
                      <div style={styles.metricValue}>
                        {formatMetricValue(key, value)}
                      </div>
                      {key.includes('ratio') && (
                        <div style={styles.progressBar}>
                          <div 
                            style={{
                              ...styles.progressFill,
                              width: `${Math.min((value as number) * 100, 100)}%`
                            }}
                          ></div>
                        </div>
                      )}
                    </div>
                  );
                })}

                {/* Indentation Card */}
                {(selectedFile.metrics.indentation_type || selectedFile.metrics.indentation_size) && (
                  <div style={{ ...styles.metricCard, ...styles.indentationCard }} className="metric-card">
                    <div style={styles.metricHeader}>
                      <span style={styles.metricIcon} className="metric-icon">📐</span>
                      <h3 style={styles.metricTitle}>Indentation</h3>
                    </div>
                    <div style={styles.indentationList}>
                      <div style={styles.indentationItem}>
                        <span style={styles.indentationLabel}>Type:</span>
                        <span style={styles.indentationValue}>
                          {selectedFile.metrics.indentation_type || 'N/A'}
                        </span>
                      </div>
                      <div style={styles.indentationItem}>
                        <span style={styles.indentationLabel}>Size:</span>
                        <span style={styles.indentationValue}>
                          {selectedFile.metrics.indentation_size || 'N/A'}
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </>
          ) : (
            <div style={styles.emptyState}>
              <div style={styles.emptyStateContent}>
                <div style={styles.emptyStateIcon}>👆</div>
                <p style={styles.emptyStateText}>Select a file from the sidebar to view its metrics</p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}