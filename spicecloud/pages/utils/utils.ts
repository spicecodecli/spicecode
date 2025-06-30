export const getFileIconSrc = (ext: string): string => {
  switch (ext) {
    case '.py':  return '/python-logo.png';
    case '.js':  return '/javascript-logo.png';
    case '.rb':  return '/ruby-logo.png';
    case '.go':  return '/go-logo.png';
    default:     return '/file-icon.png';
  }
};

export const formatMetricValue = (key: string, value: any): string => {
  if (typeof value === 'object' && value !== null) {
    return JSON.stringify(value, null, 2);
  }
  if (key.includes('ratio') && typeof value === 'number') {
    return `${(value * 100).toFixed(1)}%`;
  }
  return String(value);
};

export const getMetricIcon = (key: string): string => {
  if (key.includes('line_count')) return '📄';
  if (key.includes('function_count')) return '⚡';
  if (key.includes('comment')) return '💬';
  if (key.includes('dependencies')) return '📦';
  if (key.includes('indentation')) return '📐';
  if (key.includes('method')) return '🔧';
  if (key.includes('ratio')) return '📊';
  return '📋';
};

export const getMetricColor = (key: string): string => {
  if (key.includes('count') || key.includes('line')) 
    return 'linear-gradient(135deg, #e3d6b0, #c9b67a)';
  if (key.includes('ratio')) 
    return 'linear-gradient(135deg, #d97304, #a35402)';
  if (key.includes('dependencies')) 
    return 'linear-gradient(135deg, #a67c23, #6b4c1b)';
  if (key.includes('indentation')) 
    return 'linear-gradient(135deg, #d7b377, #f0e3c8)';
  if (key.includes('method')) 
    return 'linear-gradient(135deg, #a35402, #d97304)';
  return 'linear-gradient(135deg, #6b4c1b, #4a2c0b)';
};

export const formatAge = (age: number): string => {
  const hours = Math.floor(age / (1000 * 60 * 60));
  const minutes = Math.floor((age % (1000 * 60 * 60)) / (1000 * 60));
  
  if (hours > 0) {
    return `${hours}h ${minutes}m ago`;
  }
  return `${minutes}m ago`;
};

export const formatLabel = (key: string): string => {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, l => l.toUpperCase());
};