# this will count functions in the AST
def count_functions(ast):
    # import function definition from the parser's ast
    from parser.ast import FunctionDefinition, Program
    
    if not isinstance(ast, Program):
        return 0
    
    function_count = 0
    
    # recursive search for function definitions in the AST
    def search_node(node):
        nonlocal function_count
        
        if isinstance(node, FunctionDefinition):
            function_count += 1
        
        # process child nodes if they exist
        if hasattr(node, 'statements') and node.statements:
            for statement in node.statements:
                search_node(statement)
        
        if hasattr(node, 'body') and node.body:
            for body_statement in node.body:
                search_node(body_statement)
        
        # for binary operation, check both sides
        if hasattr(node, 'left'):
            search_node(node.left)
        if hasattr(node, 'right'):
            search_node(node.right)
        
        # check the value part of an assignment
        if hasattr(node, 'value'):
            search_node(node.value)
            
        # check function call arguments
        if hasattr(node, 'arguments') and node.arguments:
            for arg in node.arguments:
                search_node(arg)
    
    # start recursive search from the root Program node
    search_node(ast)
    
    return function_count