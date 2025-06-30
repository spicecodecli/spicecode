import React from 'react';
import { MetricData } from '../utils/types';
import { MetricCard } from './MetricCard';
import { MethodTypeCard } from './MethodTypeCard';
import { IndentationCard } from './IndentationCard';
import { styles } from '../utils/styles';

interface MetricsGridProps {
  selectedFile: MetricData;
}

export const MetricsGrid: React.FC<MetricsGridProps> = ({ selectedFile }) => {
  return (
    <div style={styles.metricsGrid}>
      {Object.entries(selectedFile.metrics).map(([key, value]) => {
        // Skip file info metrics
        if (['file_name', 'file_path', 'file_size', 'file_extension'].includes(key)) {
          return null;
        }

        // Handle method type count specially
        if (key === 'method_type_count' && typeof value === 'object' && value !== null) {
          return (
            <MethodTypeCard 
              key={key}
              value={value as { public: number; private: number }}
            />
          );
        }

        // Skip indentation keys as they'll be handled in their own card
        if (key === 'indentation_type' || key === 'indentation_size') {
          return null;
        }

        return (
          <MetricCard 
            key={key}
            metricKey={key}
            value={value}
          />
        );
      })}

      {/* Indentation Card */}
      {(selectedFile.metrics.indentation_type || selectedFile.metrics.indentation_size) && (
        <IndentationCard 
          indentationType={selectedFile.metrics.indentation_type}
          indentationSize={selectedFile.metrics.indentation_size}
        />
      )}
    </div>
  );
};