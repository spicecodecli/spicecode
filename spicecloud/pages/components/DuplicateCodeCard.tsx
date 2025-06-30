import React from 'react';
import { styles } from '../utils/styles';

interface Props {
  percentage?: number;
  blocks?: number;
  lines?: number;
}

export const DuplicateCodeCard: React.FC<Props> = ({
  percentage = 0,
  blocks,
  lines,
}) => {
  return (
    <div style={styles.metricCard} className="metric-card">
      <div style={styles.metricHeader}>
        <h3 style={styles.metricTitle}>Duplicate Code</h3>
        <span style={styles.metricValue}>{percentage.toFixed(2)}%</span>
      </div>

      <div style={styles.metricDetails}>
        {blocks !== undefined && (
          <p style={styles.detailLine}>Duplicate blocks: {blocks}</p>
        )}
        {lines !== undefined && (
          <p style={styles.detailLine}>Duplicate lines: {lines}</p>
        )}
      </div>
    </div>
  );
};
