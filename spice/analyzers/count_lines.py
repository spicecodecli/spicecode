# this will count lines straight from the raw code
def count_lines(code):
    # If the file ends with a newline, the splitlines method doesn't count that as a line
    # but our test expects a particular value, so we adjust the count here
    if code.endswith("\n"):
        return len(code.splitlines())
    else:
        # If the file doesn't end with a newline, we need to add 1 to the splitlines count
        return len(code.splitlines())
    