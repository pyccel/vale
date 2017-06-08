# coding: utf-8

from vale.parser import ValeParser, get_by_name

# ... creates an instance of Vale parser
vale = ValeParser()
# ...

# ...
def test_domain():
    # ... parse the Vale code
    ast = vale.parse("Domain(dim=1,kind='structured') :: Omega")

    token = get_by_name(ast, "Omega")
    # ...

    # ...
    assert(token.name == "Omega")
    assert(token.dim  == 1)
    assert(token.kind == "structured")
    # ...
# ...

# ...
def test_space():
    # ... parse the Vale code
    ast = vale.parse("Space(domain=Omega,kind='h1') :: V")

    token = get_by_name(ast, "V")
    # ...

    # ...
    assert(token.name   == "V")
    assert(token.domain == "Omega")
    assert(token.kind   == "h1")
    # ...
# ...

# ...
def test_field():
    # ... parse the Vale code
    ast = vale.parse("Field(space=V) :: phi")

    token = get_by_name(ast, "phi")
    # ...

    # ...
    assert(token.name  == "phi")
    assert(token.space == "V")
    # ...
# ...

# ...
def test_function():
    # ... parse the Vale code
    ast = vale.parse("Function(x,y) :: f")

    token = get_by_name(ast, "f")
    # ...

    # ...
    assert(token.name       == "f")
    assert(token.parameters == ["x", "y"])
    # ...
# ...

# ...
def test_linear_form():
    # ... parse the Vale code
    ast = vale.parse("b(v::V) := < f * v >_Omega")

    token = get_by_name(ast, "b")
    # ...

    # ...
    assert(token.name           == "b")
    assert(token.domain         == "Omega")
    assert(token.args.space     == "V")
    assert(token.args.functions == ["v"])

    # TODO add assert on expression.
    #      need to annotate the ast
#    print token.expression.expr
#    assert(token.expression     == "Omega")
    # ...
# ...

# ...
def test_bilinear_form():
    # ... parse the Vale code
    ast = vale.parse("a(v::V, u::V) := < dx(v) * dx(u) >_Omega")

    token = get_by_name(ast, "a")
    # ...

    # ...
    assert(token.name                 == "a")
    assert(token.domain               == "Omega")
    assert(token.args_test.space      == "V")
    assert(token.args_test.functions  == ["v"])
    assert(token.args_trial.space     == "V")
    assert(token.args_trial.functions == ["u"])

    # TODO add assert on expression.
    #      need to annotate the ast
#    print token.expression.expr
#    assert(token.expression     == "Omega")
    # ...
# ...

######################################
if __name__ == "__main__":
    test_domain()
    test_space()
    test_field()
    test_function()
    test_linear_form()
    test_bilinear_form()
