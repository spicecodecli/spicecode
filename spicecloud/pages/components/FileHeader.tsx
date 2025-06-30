import React from 'react';
import { MetricData } from '../utils/types';
import { getFileIconSrc } from '../utils/utils';
import { styles } from '../utils/styles';

interface FileHeaderProps {
  selectedFile: MetricData;
}

export const FileHeader: React.FC<FileHeaderProps> = ({ selectedFile }) => {
  return (
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
  );
};