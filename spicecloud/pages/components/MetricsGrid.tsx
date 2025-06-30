import React from 'react';
import { MetricData } from '../utils/types';
import { MetricCard } from './MetricCard';
import { MethodTypeCard } from './MethodTypeCard';
import { IndentationCard } from './IndentationCard';
import { ComplexityCard } from './ComplexityCard';
import { DuplicateCodeCard } from './DuplicateCodeCard';
import { styles } from '../utils/styles';

interface MetricsGridProps {
  selectedFile: MetricData;
}

// keys handled by special cards ↓
const SKIP_KEYS = [
  'file_name',
  'file_path',
  'file_size',
  'file_extension',
  'indentation_type',
  'indentation_size',
  'method_type_count',
  'duplicate_blocks',
  'duplicate_lines',
  'duplicate_percentage',
  'average_complexity',
  'complexity_distribution',
  'total_analyzed_functions',
];

export const MetricsGrid: React.FC<MetricsGridProps> = ({ selectedFile }) => {
  const m = selectedFile.metrics;

  return (
    <div style={styles.metricsGrid}>
      {/* generic & existing cards */}
      {Object.entries(m).map(([key, value]) => {
        if (SKIP_KEYS.includes(key)) return null;

        if (key === 'method_type_count') {
          return (
            <MethodTypeCard
              key={key}
              value={value as { public: number; private: number }}
            />
          );
        }

        return <MetricCard key={key} metricKey={key} value={value} />;
      })}

      {/* indentation */}
      {(m.indentation_type || m.indentation_size) && (
        <IndentationCard
          indentationType={m.indentation_type}
          indentationSize={m.indentation_size}
        />
      )}

      {/* duplicate‑code */}
      {(m.duplicate_percentage !== undefined ||
        m.duplicate_blocks !== undefined ||
        m.duplicate_lines !== undefined) && (
        <DuplicateCodeCard
          percentage={m.duplicate_percentage}
          blocks={m.duplicate_blocks}
          lines={m.duplicate_lines}
        />
      )}

      {/* complexity */}
      {m.average_complexity && (
        <ComplexityCard
          averageComplexity={m.average_complexity}
          distribution={m.complexity_distribution}
          totalFunctions={m.total_analyzed_functions}
        />
      )}
    </div>
  );
};
