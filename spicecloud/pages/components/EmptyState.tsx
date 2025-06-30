import React from 'react';
import { styles } from '../utils/styles';

export const EmptyState: React.FC = () => {
  return (
    <div style={styles.emptyState}>
      <div style={styles.emptyStateContent}>
        <div style={styles.emptyStateIcon}>👆</div>
        <p style={styles.emptyStateText}>Select a file from the sidebar to view its metrics</p>
      </div>
    </div>
  );
};