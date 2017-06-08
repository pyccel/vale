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

######################################
if __name__ == "__main__":
    test_domain()
    test_space()
    test_field()
    test_function()
