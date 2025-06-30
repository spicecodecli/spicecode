import React from 'react';
import { useData } from './utils/useData';
import { Header } from './components/Header';
import { FileList } from './components/FileList';
import { FileHeader } from './components/FileHeader';
import { MetricsGrid } from './components/MetricsGrid';
import { LoadingSpinner } from './components/LoadingSpinner';
import { EmptyState } from './components/EmptyState';
import { styles } from './utils/styles';

export default function Home() {
  const { data, selectedFile, setSelectedFile, loading, error, fetchData } = useData();

  if (loading && data.length === 0) {
    return <LoadingSpinner />;
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
      
      <Header 
        dataLength={data.length}
        loading={loading}
        onRefresh={fetchData}
      />

      <div style={styles.mainContent}>
        <FileList 
          data={data}
          selectedFile={selectedFile}
          onFileSelect={setSelectedFile}
        />

        <div style={styles.metricsArea}>
          {selectedFile ? (
            <>
              <FileHeader selectedFile={selectedFile} />
              <MetricsGrid selectedFile={selectedFile} />
            </>
          ) : (
            <EmptyState />
          )}
        </div>
      </div>
    </div>
  );
}