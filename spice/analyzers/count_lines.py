# this will count lines straight from the raw code
def count_lines(code):
    """Count the number of lines in the code.
    
    Args:
        code (str): The source code to analyze
        
    Returns:
        int: Number of lines in the code
    """
    # Use splitlines to split the code into lines, which handles all line ending types
    # (Unix \n, Windows \r\n, and old Mac \r)
    return len(code.splitlines())
    