import pytest
from parser.ast import (
    Program, Identifier, Literal, Assignment, BinaryOperation, 
    FunctionDefinition, FunctionCall
)

# Test Identifier Node
def test_identifier_node():
    ident = Identifier("my_var")
    assert ident.name == "my_var"
    assert str(ident) == "<Identifier:my_var>"

# Test Literal Node
@pytest.mark.parametrize(
    "value, expected_str",
    [
        (123, "<Literal:123>"),
        ("hello", "<Literal:hello>"),
        (True, "<Literal:True>"),
        (None, "<Literal:None>"),
    ]
)
def test_literal_node(value, expected_str):
    literal = Literal(value)
    assert literal.value == value
    assert str(literal) == expected_str

# Test Assignment Node
def test_assignment_node():
    var = Identifier("x")
    val = Literal(10)
    assign = Assignment(var, val)
    assert assign.variable == var
    assert assign.value == val
    assert str(assign) == "<Assignment:<Identifier:x> = <Literal:10>>"

# Test BinaryOperation Node
def test_binary_operation_node():
    left = Identifier("a")
    right = Literal(5)
    op = BinaryOperation(left, "+", right)
    assert op.left == left
    assert op.operator == "+"
    assert op.right == right
    assert str(op) == "<BinaryOp:<Identifier:a> + <Literal:5>>"

# Test FunctionDefinition Node
def test_function_definition_node():
    name = Identifier("my_func")
    params = [Identifier("p1"), Identifier("p2")]
    body = [
        Assignment(Identifier("local_var"), Literal(1)),
        BinaryOperation(Identifier("p1"), "+", Identifier("p2"))
    ]
    func_def = FunctionDefinition(name, params, body)
    assert func_def.name == name
    assert func_def.parameters == params
    assert func_def.body == body
    expected_str = (
        "<FunctionDef:<Identifier:my_func>(<Identifier:p1>, <Identifier:p2>)>\n"
        "    <Assignment:<Identifier:local_var> = <Literal:1>>\n"
        "    <BinaryOp:<Identifier:p1> + <Identifier:p2>>"
    )
    assert str(func_def) == expected_str

def test_function_definition_no_params_no_body():
    name = Identifier("empty_func")
    func_def = FunctionDefinition(name, None, None)
    assert func_def.name == name
    assert func_def.parameters == []
    assert func_def.body == []
    assert str(func_def) == "<FunctionDef:<Identifier:empty_func>()>\n"

# Test FunctionCall Node
def test_function_call_node():
    func = Identifier("call_me")
    args = [Literal(10), Identifier("arg2")]
    func_call = FunctionCall(func, args)
    assert func_call.function == func
    assert func_call.arguments == args
    assert str(func_call) == "<FunctionCall:<Identifier:call_me>(<Literal:10>, <Identifier:arg2>)>"

def test_function_call_no_args():
    func = Identifier("no_args_call")
    func_call = FunctionCall(func, None)
    assert func_call.function == func
    assert func_call.arguments == []
    assert str(func_call) == "<FunctionCall:<Identifier:no_args_call>()>"

# Test Program Node
def test_program_node():
    statements = [
        Assignment(Identifier("a"), Literal(1)),
        FunctionCall(Identifier("print"), [Identifier("a")])
    ]
    program = Program(statements)
    assert program.statements == statements
    expected_str = (
        "<Program>\n"
        "  <Assignment:<Identifier:a> = <Literal:1>>\n"
        "  <FunctionCall:<Identifier:print>(<Identifier:a>)>"
    )
    assert str(program) == expected_str

def test_program_empty():
    program = Program([])
    assert program.statements == []
    assert str(program) == "<Program>\n"


