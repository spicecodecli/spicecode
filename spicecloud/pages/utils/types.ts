export interface MetricData {
  id: string;
  hash: string;
  timestamp: number;
  file_name: string;
  file_path: string;
  metrics: {
    file_extension: string;
    line_count: number;
    comment_line_count: number;
    inline_comment_count: number;
    indentation_type: string;
    indentation_size: number;
    function_count: number;
    external_dependencies_count: number;
    method_type_count: { private: number; public: number };
    comment_ratio: string;
    average_function_size?: number;

    /* duplicate code */
    duplicate_blocks?: number;
    duplicate_lines?: number;
    duplicate_percentage?: number;

    /* complexity */
    average_complexity?: string;
    complexity_distribution?: Record<string, number>;
    total_analyzed_functions?: number;
  };
  age: number;
  readable_timestamp: string;
}
