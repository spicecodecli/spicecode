# this will count external dependencies (imports/requires from external libraries)
# EXTERNAL DEPENDENCY is an import/require statement that references an external library
from utils.get_lexer import get_lexer_for_file
from lexers.token import TokenType
import os
import re
import sys

# Python standard library modules to exclude from dependency count
PYTHON_STD_LIBS = set([
    'abc', 'argparse', 'ast', 'asyncio', 'base64', 'collections', 'concurrent', 'contextlib',
    'copy', 'csv', 'ctypes', 'datetime', 'decimal', 'enum', 'functools', 'glob', 'gzip',
    'hashlib', 'http', 'importlib', 'inspect', 'io', 'itertools', 'json', 'logging', 'math',
    'multiprocessing', 'operator', 'os', 'pathlib', 'pickle', 'queue', 're', 'random',
    'shutil', 'signal', 'socket', 'sqlite3', 'statistics', 'string', 'subprocess', 'sys',
    'tempfile', 'threading', 'time', 'typing', 'unittest', 'urllib', 'uuid', 'warnings',
    'weakref', 'xml', 'zipfile', 'zlib'
])

# Node.js standard modules to exclude
NODE_STD_LIBS = set([
    'assert', 'async_hooks', 'buffer', 'child_process', 'cluster', 'console', 'constants',
    'crypto', 'dgram', 'dns', 'domain', 'events', 'fs', 'http', 'https', 'module', 'net',
    'os', 'path', 'perf_hooks', 'process', 'punycode', 'querystring', 'readline', 'repl',
    'stream', 'string_decoder', 'timers', 'tls', 'tty', 'url', 'util', 'v8', 'vm', 'zlib'
])

# Go standard packages to exclude
GO_STD_LIBS = set([
    'archive', 'bufio', 'builtin', 'bytes', 'compress', 'container', 'context', 'crypto',
    'database', 'debug', 'encoding', 'errors', 'expvar', 'flag', 'fmt', 'go', 'hash',
    'html', 'image', 'index', 'io', 'log', 'math', 'mime', 'net', 'os', 'path', 'plugin',
    'reflect', 'regexp', 'runtime', 'sort', 'strconv', 'strings', 'sync', 'syscall',
    'testing', 'text', 'time', 'unicode', 'unsafe'
])

# Ruby standard libraries to exclude
RUBY_STD_LIBS = set([
    'abbrev', 'base64', 'benchmark', 'bigdecimal', 'cgi', 'csv', 'date', 'delegate',
    'digest', 'drb', 'e2mmap', 'erb', 'etc', 'fcntl', 'fiddle', 'fileutils', 'find',
    'forwardable', 'io', 'ipaddr', 'irb', 'json', 'logger', 'matrix', 'monitor', 'mutex_m',
    'net', 'observer', 'open-uri', 'open3', 'optparse', 'ostruct', 'pathname', 'pp',
    'prettyprint', 'prime', 'profile', 'profiler', 'pstore', 'pty', 'racc', 'rake',
    'rdoc', 'readline', 'resolv', 'rexml', 'rinda', 'ripper', 'rss', 'rubygems', 'scanf',
    'sdbm', 'set', 'shellwords', 'singleton', 'socket', 'stringio', 'strscan', 'sync',
    'syslog', 'tempfile', 'thread', 'thwait', 'time', 'timeout', 'tmpdir', 'tracer',
    'tsort', 'uri', 'weakref', 'webrick', 'yaml', 'zlib'
])

def count_external_dependencies(file_path):
    """Count external dependencies in a file.
    
    Args:
        file_path (str): Path to the file to analyze
        
    Returns:
        int: Number of external dependencies found
    """
    # Get file extension to determine language
    _, ext = os.path.splitext(file_path)
    
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    # Count dependencies based on the language
    if ext == '.py':
        return count_python_dependencies(code)
    elif ext == '.js':
        return count_javascript_dependencies(code)
    elif ext == '.rb':
        return count_ruby_dependencies(code)
    elif ext == '.go':
        return count_go_dependencies(code)
    else:
        # Default to 0 for unsupported languages
        return 0
        
def count_python_dependencies(code):
    """Count external dependencies in Python code."""
    # Regular expressions for import patterns
    import_pattern = r'^\s*import\s+([a-zA-Z0-9_.,\s]+)'
    from_pattern = r'^\s*from\s+([a-zA-Z0-9_.]+)\s+import'
    
    dependencies = set()
    
    # Find all import statements
    for line in code.split('\n'):
        # Check for 'import X' pattern
        import_match = re.match(import_pattern, line)
        if import_match:
            modules = [m.strip() for m in import_match.group(1).split(',')]
            for module in modules:
                # Get the top-level package
                top_level = module.split('.')[0]
                dependencies.add(top_level)
                
        # Check for 'from X import Y' pattern
        from_match = re.match(from_pattern, line)
        if from_match:
            # Get the top-level package
            module = from_match.group(1)
            top_level = module.split('.')[0]
            dependencies.add(top_level)
    
    # Filter out standard library modules
    external_deps = {dep for dep in dependencies if dep not in PYTHON_STD_LIBS}
    
    return len(external_deps)

def count_javascript_dependencies(code):
    """Count external dependencies in JavaScript code."""
    # Regular expressions for require and import patterns
    require_pattern = r'(?:const|let|var)\s+.+\s*=\s*require\([\'"]([^\'".]+)[\'"]'
    import_pattern = r'import\s+(?:.+\s+from\s+)?[\'"]([^\'".]+)[\'"]'
    
    dependencies = set()
    
    # Find all require statements
    for match in re.finditer(require_pattern, code):
        module_name = match.group(1)
        dependencies.add(module_name)
    
    # Find all import statements
    for match in re.finditer(import_pattern, code):
        module_name = match.group(1)
        dependencies.add(module_name)
    
    # Filter out Node.js standard libraries and relative imports
    external_deps = {
        dep for dep in dependencies 
        if dep not in NODE_STD_LIBS and not dep.startswith('./') and not dep.startswith('../')
    }
    
    return len(external_deps)

def count_ruby_dependencies(code):
    """Count external dependencies in Ruby code."""
    # Regular expressions for require and gem patterns
    require_pattern = r'require\s+[\'"]([^\'"]+)[\'"]'
    gem_pattern = r'gem\s+[\'"]([^\'"]+)[\'"]'
    
    dependencies = set()
    
    # Find all require statements
    for match in re.finditer(require_pattern, code):
        module_name = match.group(1)
        dependencies.add(module_name)
    
    # Find all gem statements
    for match in re.finditer(gem_pattern, code):
        module_name = match.group(1)
        dependencies.add(module_name)
    
    # Filter out Ruby standard libraries
    external_deps = {
        dep for dep in dependencies 
        if dep not in RUBY_STD_LIBS and not dep.startswith('./') and not dep.startswith('../')
    }
    
    return len(external_deps)

def count_go_dependencies(code):
    """Count external dependencies in Go code."""
    # Regular expression for import statements
    single_import_pattern = r'import\s+[\'"]([^\'"]+)[\'"]'
    multi_import_pattern = r'import\s+\(\s*((?:[\'"][^\'"]+[\'"][\s\n]*)+)\)'
    
    dependencies = set()
    
    # Find all single import statements
    for match in re.finditer(single_import_pattern, code):
        module_path = match.group(1)
        if module_path:
            # Get the top-level package
            dependencies.add(module_path)
    
    # Find all multi-line import statements
    for match in re.finditer(multi_import_pattern, code, re.DOTALL):
        imports_block = match.group(1)
        for line in imports_block.strip().split('\n'):
            line = line.strip()
            if line and (line.startswith('"') or line.startswith("'")):
                # Extract package path from quoted string
                module_path = re.findall(r'[\'"]([^\'"]+)[\'"]', line)
                if module_path:
                    dependencies.add(module_path[0])
    
    # Filter out standard library imports (packages without a domain or github.com/)
    external_deps = set()
    for dep in dependencies:
        # Skip standard library packages (no dots in path)
        if '.' in dep and not any(dep.startswith(std + '/') for std in GO_STD_LIBS):
            external_deps.add(dep)
    
    return len(external_deps) 