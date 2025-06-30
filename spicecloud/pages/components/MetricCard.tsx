import React from 'react';
import { formatMetricValue, getMetricIcon, getMetricColor, formatLabel } from '../utils/utils';
import { styles } from '../utils/styles';

interface MetricCardProps {
  metricKey: string;
  value: any;
}

export const MetricCard: React.FC<MetricCardProps> = ({ metricKey, value }) => {
  return (
    <div 
      style={{ 
        ...styles.metricCard, 
        background: getMetricColor(metricKey).replace('135deg', '135deg') + '20'
      }}
      className="metric-card"
      onMouseEnter={(e) => {
        e.currentTarget.style.transform = 'scale(1.05)';
      }}
      onMouseLeave={(e) => {
        e.currentTarget.style.transform = 'scale(1)';
      }}
    >
      <div style={styles.metricHeader}>
        <span style={styles.metricIcon} className="metric-icon">
          {getMetricIcon(metricKey)}
        </span>
        <h3 style={styles.metricTitle}>
          {formatLabel(metricKey)}
        </h3>
      </div>
      <div style={styles.metricValue}>
        {formatMetricValue(metricKey, value)}
      </div>
      {metricKey.includes('ratio') && (
        <div style={styles.progressBar}>
          <div 
            style={{
              ...styles.progressFill,
              width: `${Math.min((value as number) * 100, 100)}%`
            }}
          ></div>
        </div>
      )}
    </div>
  );
};