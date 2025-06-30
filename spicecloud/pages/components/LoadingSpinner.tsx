import React from 'react';
import { styles } from '../utils/styles';

export const LoadingSpinner: React.FC = () => {
  return (
    <div style={styles.loading}>
      <div style={{ textAlign: 'center' }}>
        <div style={styles.loadingSpinner}></div>
        <p style={{ marginTop: '1.5rem', fontSize: '1.125rem' }}>Loading your code metrics...</p>
      </div>
    </div>
  );
};