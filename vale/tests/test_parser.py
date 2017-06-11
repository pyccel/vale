# coding: utf-8

from vale.parser import ValeParser, get_by_name

# ... creates an instance of Vale parser
vale = ValeParser()
# ...

# ...
def test_domain_1():
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
def test_space_1():
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
def test_field_1():
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
def test_function_1():
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
def test_linear_form_1():
    # ... parse the Vale code
    ast = vale.parse("b(v::V) := < f * v >_Omega")

    token = get_by_name(ast, "b")
    # ...

    # ...
    assert(token.name           == "b")
    assert(token.domain         == "Omega")
    assert(token.args.space     == "V")
    assert(token.args.functions == ["v"])
    # ...
# ...

# ...
def test_linear_form_2():
    # ... parse the Vale code
    stmts  = "b1(v1::V) := < f * v1 >_Omega" + "\n"
    stmts += "b2(v2::V) := < g * v2 >_Omega" + "\n"
    stmts += "b((v1,v2)::V) := b1(v1) + b2(v2)"

    ast = vale.parse(stmts)

    token = get_by_name(ast, "b")
    # ...

    # ...
    assert(token.name == "b")
    assert(token.blocks[0] == get_by_name(ast, "b1"))
    assert(token.blocks[1] == get_by_name(ast, "b2"))
    # ...
# ...

# ...
def test_linear_form_11():
    # ... parse the Vale code
    stmts  = "Domain(dim=1,kind='structured') :: Omega" + "\n"
    stmts += "Space(domain=Omega,kind='h1')   :: V"     + "\n"
    stmts += "Function(x)                     :: f"     + "\n"
    stmts += "b(v::V) := < f * v >_Omega"               + "\n"

    ast = vale.parse(stmts)

    token = get_by_name(ast, "b")
    # ...

    # ...
    assert(token.name           == "b")
    assert(token.domain         == "Omega")
    assert(token.args.space     == "V")
    assert(token.args.functions == ["v"])
    # ...

    # ... sends the expression to sympy to check its validity
    expr = token.to_sympy()
    # ...
# ...

# ...
def test_linear_form_21():
    # ... parse the Vale code
    stmts  = "Domain(dim=1,kind='structured') :: Omega" + "\n"
    stmts += "Space(domain=Omega,kind='h1')   :: V"     + "\n"
    stmts += "Function(x)                     :: f"     + "\n"
    stmts += "Function(x)                     :: g"     + "\n"
    stmts += "b1(v1::V) := < f * v1 >_Omega"            + "\n"
    stmts += "b2(v2::V) := < g * v2 >_Omega"            + "\n"
    stmts += "b((v1,v2)::V) := b1(v1) + b2(v2)"

    ast = vale.parse(stmts)

    token = get_by_name(ast, "b")
    # ...

    # ...
    assert(token.name == "b")
    assert(token.blocks[0] == get_by_name(ast, "b1"))
    assert(token.blocks[1] == get_by_name(ast, "b2"))
    # ...

    # ... sends the expression to sympy to check its validity
#    expr = token.to_sympy()
    # ...
# ...

# ...
def test_bilinear_form_1():
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
#    test_domain_1()

#    test_space_1()

#    test_field_1()

#    test_function_1()

#    test_linear_form_1()
#    test_linear_form_2()
#    test_linear_form_11()
    test_linear_form_21()

#    test_bilinear_form_1()
