import React from 'react';
import { MetricData } from '../utils/types';
import { getFileIconSrc, formatAge } from '../utils/utils';
import { styles } from '../utils/styles';

interface FileListProps {
  data: MetricData[];
  selectedFile: MetricData | null;
  onFileSelect: (file: MetricData) => void;
}

export const FileList: React.FC<FileListProps> = ({ data, selectedFile, onFileSelect }) => {
  return (
    <div style={styles.sidebar}>
      <h2 style={styles.sidebarTitle}>
        <span>📁</span>
        Analyzed Files
      </h2>
      <div style={styles.fileList}>
        {data.map((item) => (
          <div
            key={item.id}
            onClick={() => onFileSelect(item)}
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
  );
};