import React from 'react';
import { styles } from '../utils/styles';

interface IndentationCardProps {
  indentationType?: string;
  indentationSize?: number;
}

export const IndentationCard: React.FC<IndentationCardProps> = ({ 
  indentationType, 
  indentationSize 
}) => {
  return (
    <div style={{ ...styles.metricCard, ...styles.indentationCard }} className="metric-card">
      <div style={styles.metricHeader}>
        <span style={styles.metricIcon} className="metric-icon">📐</span>
        <h3 style={styles.metricTitle}>Indentation</h3>
      </div>
      <div style={styles.indentationList}>
        <div style={styles.indentationItem}>
          <span style={styles.indentationLabel}>Type:</span>
          <span style={styles.indentationValue}>
            {indentationType || 'N/A'}
          </span>
        </div>
        <div style={styles.indentationItem}>
          <span style={styles.indentationLabel}>Size:</span>
          <span style={styles.indentationValue}>
            {indentationSize || 'N/A'}
          </span>
        </div>
      </div>
    </div>
  );
};