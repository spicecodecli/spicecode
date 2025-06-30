# spice/analyzers/duplicate_code_detection.py
import hashlib
import re
from collections import defaultdict

def detect_duplicate_code(file_path, min_lines=3):
    """Detect duplicate code blocks in a file.
    
    Args:
        file_path (str): Path to the file to analyze
        min_lines (int): Minimum number of lines to consider as a block
        
    Returns:
        dict: Contains duplicate_blocks_count, total_duplicate_lines, and duplicate_percentage
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    lines = code.split('\n')
    
    # Normalize lines by removing comments and extra whitespace
    normalized_lines = []
    for line in lines:
        normalized = _normalize_line(line)
        normalized_lines.append(normalized)
    
    # Generate all possible blocks of min_lines or more
    block_hashes = defaultdict(list)
    total_lines = len(normalized_lines)
    
    # Check blocks of different sizes
    for block_size in range(min_lines, min(total_lines + 1, 20)):  # Limit to reasonable block sizes
        for i in range(total_lines - block_size + 1):
            block = normalized_lines[i:i + block_size]
            # Skip blocks that are mostly empty
            if sum(1 for line in block if line.strip()) < block_size // 2:
                continue
                
            block_text = '\n'.join(block)
            block_hash = hashlib.md5(block_text.encode()).hexdigest()
            block_hashes[block_hash].append({
                'start_line': i + 1,
                'end_line': i + block_size,
                'size': block_size,
                'content': block_text
            })
    
    # Find duplicates (blocks that appear more than once)
    duplicates = {}
    total_duplicate_lines = 0
    processed_lines = set()
    
    for block_hash, occurrences in block_hashes.items():
        if len(occurrences) > 1:
            # Choose the largest block size for this hash
            largest_block = max(occurrences, key=lambda x: x['size'])
            duplicates[block_hash] = {
                'occurrences': len(occurrences),
                'locations': occurrences,
                'size': largest_block['size']
            }
            
            # Count unique duplicate lines (avoid double counting overlapping blocks)
            for occurrence in occurrences:
                for line_num in range(occurrence['start_line'], occurrence['end_line'] + 1):
                    if line_num not in processed_lines:
                        processed_lines.add(line_num)
                        total_duplicate_lines += 1
    
    duplicate_percentage = (total_duplicate_lines / max(total_lines, 1)) * 100
    
    return {
        'duplicate_blocks_count': len(duplicates),
        'total_duplicate_lines': total_duplicate_lines,
        'duplicate_percentage': round(duplicate_percentage, 2),
        'details': duplicates
    }

def _normalize_line(line):
    """Normalize a line of code for comparison by removing comments and standardizing whitespace."""
    # Remove comments (simplified approach)
    line = re.sub(r'//.*$', '', line)  # JS/Go style comments
    line = re.sub(r'#.*$', '', line)   # Python/Ruby style comments
    
    # Remove string literals (simplified)
    line = re.sub(r'"[^"]*"', '""', line)
    line = re.sub(r"'[^']*'", "''", line)
    
    # Normalize whitespace
    line = re.sub(r'\s+', ' ', line.strip())
    
    return line

def get_duplicate_code_summary(file_path):
    """Get a summary of duplicate code detection for integration with main analyzer.
    
    Args:
        file_path (str): Path to the file to analyze
        
    Returns:
        dict: Summary of duplicate code analysis
    """
    result = detect_duplicate_code(file_path)
    return {
        'duplicate_blocks': result['duplicate_blocks_count'],
        'duplicate_lines': result['total_duplicate_lines'],
        'duplicate_percentage': result['duplicate_percentage']
    }