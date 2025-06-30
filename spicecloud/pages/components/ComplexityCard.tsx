import React from 'react';
import { styles } from '../utils/styles';

interface Props {
  averageComplexity?: string;
  distribution?: Record<string, number>;
  totalFunctions?: number;
}

export const ComplexityCard: React.FC<Props> = ({
  averageComplexity = 'N/A',
  distribution,
  totalFunctions,
}) => {
  return (
    <div style={styles.metricCard} className="metric-card">
      <div style={styles.metricHeader}>
        <h3 style={styles.metricTitle}>Complexity</h3>
        <span style={styles.metricValue}>{averageComplexity}</span>
      </div>

      <div style={styles.metricDetails}>
        {totalFunctions !== undefined && (
          <p style={styles.detailLine}>
            Functions analysed: {totalFunctions}
          </p>
        )}
        {distribution &&
          Object.entries(distribution).map(([bigO, qty]) => (
            <p key={bigO} style={styles.detailLine}>
              {bigO}: {qty}
            </p>
          ))}
      </div>
    </div>
  );
};
