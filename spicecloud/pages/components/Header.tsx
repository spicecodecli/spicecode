import React from 'react';
import { styles } from '../utils/styles';

interface HeaderProps {
  dataLength: number;
  loading: boolean;
  onRefresh: () => void;
}

export const Header: React.FC<HeaderProps> = ({ dataLength, loading, onRefresh }) => {
  return (
    <div style={styles.header}>
      <div style={styles.headerContent}>
        <div>
          <h1 style={styles.title}>
            <img 
              src="/spicecloud-logo.png" 
              alt="SpiceCloud Logo" 
              style={{ width: '3rem', height: '3rem', verticalAlign: 'middle', marginRight: '0.5rem' }}
            />
            SpiceCloud | Powered by SpiceCodeCLI
          </h1>
          <p style={styles.subtitle}>{dataLength} files analyzed</p>
        </div>
        <button 
          onClick={onRefresh}
          disabled={loading}
          style={{
            ...styles.refreshButton,
            background: loading ? '#bfa865' : '#d97304'
          }}
        >
          {loading ? '🔄 Updating...' : '🔄 Refresh'}
        </button>
      </div>
    </div>
  );
};