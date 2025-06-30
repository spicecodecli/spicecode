import React from 'react';
import { styles } from '../utils/styles';

interface MethodTypeCardProps {
  value: {
    public: number;
    private: number;
  };
}

export const MethodTypeCard: React.FC<MethodTypeCardProps> = ({ value }) => {
  return (
    <div 
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
          <span style={styles.methodTypeValue}>{value.public}</span>
        </div>
        <div style={styles.methodTypeItem}>
          <div style={styles.methodTypeLabel}>
            <span style={{ ...styles.methodTypeDot, background: '#3b82f6' }}></span>
            <span style={styles.methodTypeText}>Private</span>
          </div>
          <span style={styles.methodTypeValue}>{value.private}</span>
        </div>
      </div>
    </div>
  );
};