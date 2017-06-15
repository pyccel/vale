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
def test_number_1():
    # ... parse the Vale code
    ast = vale.parse("Real :: alpha")

    token = get_by_name(ast, "alpha")
    # ...

    # ...
    assert(token.name       == "alpha")
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
    stmts  = "b1(v::V) := < f * v >_Omega" + "\n"
    stmts += "b2(v::V) := < g * v >_Omega" + "\n"
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
    print expr
    # ...
# ...

# ...
def test_linear_form_12():
    # ... parse the Vale code
    stmts  = "Domain(dim=1,kind='structured') :: Omega" + "\n"
    stmts += "Space(domain=Omega,kind='h1')   :: V"     + "\n"
    stmts += "Real                            :: s" + "\n"
    stmts += "b(v::V) := < s * v >_Omega"           + "\n"

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
    print expr
    # ...
# ...

# ...
def test_linear_form_21():
    # ... parse the Vale code
    stmts  = "Domain(dim=1,kind='structured') :: Omega" + "\n"
    stmts += "Space(domain=Omega,kind='h1')   :: V"     + "\n"
    stmts += "Function(x)                     :: f"     + "\n"
    stmts += "Function(x)                     :: g"     + "\n"
    stmts += "b1(u::V) := < f * u >_Omega"              + "\n"
    stmts += "b2(w::V) := < g * dx(w) >_Omega"          + "\n"
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
    expr = token.to_sympy()
    print expr
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
    # ...
# ...

# ...
def test_bilinear_form_2():
    # ... parse the Vale code
    stmts  = "a1(v::V, u::V) := < dx(v) * dx(u) >_Omega" + "\n"
    stmts += "a2(v::V, u::V) := < v * u >_Omega"         + "\n"
    stmts += "a3(v::V, u::V) := < dx(v) * u >_Omega"     + "\n"
    stmts += "a((v1,v2)::V,(u1,u2)::V) := a1(v1,u1) + a2(v2,u2) + a3(v1,u2)"

    ast = vale.parse(stmts)

    token = get_by_name(ast, "a")
    # ...

    # ...
    assert(token.name == "a")
    assert(token.blocks[0,0] == get_by_name(ast, "a1"))
    assert(token.blocks[1,1] == get_by_name(ast, "a2"))
    assert(token.blocks[0,1] == get_by_name(ast, "a3"))
    # ...
# ...

# ...
def test_bilinear_form_11():
    # ... parse the Vale code
    stmts  = "Domain(dim=1,kind='structured') :: Omega" + "\n"
    stmts += "Space(domain=Omega,kind='h1')   :: V"     + "\n"
    stmts += "a(v::V, u::V) := < dx(v) * dx(u) >_Omega"

    ast = vale.parse(stmts)

    token = get_by_name(ast, "a")
    # ...

    # ...
    assert(token.name                 == "a")
    assert(token.domain               == "Omega")
    assert(token.args_test.space      == "V")
    assert(token.args_test.functions  == ["v"])
    assert(token.args_trial.space     == "V")
    assert(token.args_trial.functions == ["u"])
    # ...

    # ... sends the expression to sympy to check its validity
    expr = token.to_sympy()
    print expr
    # ...
# ...

# ...
def test_bilinear_form_21():
    # ... parse the Vale code
    stmts  = "Domain(dim=1,kind='structured') :: Omega" + "\n"
    stmts += "Space(domain=Omega,kind='h1')   :: V"     + "\n"
    stmts += "a1(v::V, u::V) := < dx(v) * dx(u) >_Omega" + "\n"
    stmts += "a2(v::V, u::V) := < v * u >_Omega"         + "\n"
    stmts += "a3(v::V, u::V) := < dx(v) * u >_Omega"     + "\n"
    stmts += "a((v1,v2)::V,(u1,u2)::V) := a1(v1,u1) + a2(v2,u2) + a3(v1,u2)"

    ast = vale.parse(stmts)

    token = get_by_name(ast, "a")
    # ...

    # ...
    assert(token.name == "a")
    assert(token.blocks[0,0] == get_by_name(ast, "a1"))
    assert(token.blocks[1,1] == get_by_name(ast, "a2"))
    assert(token.blocks[0,1] == get_by_name(ast, "a3"))
    # ...

    # ... sends the expression to sympy to check its validity
    expr = token.to_sympy()
    print expr
    # ...
# ...

######################################
if __name__ == "__main__":
#    # ... domain testing
#    test_domain_1()
#    # ...
#
#    # ... space testing
#    test_space_1()
#    # ...
#
#    # ... field testing
#    test_field_1()
#    # ...
#
#    # ... function testing
#    test_function_1()
#    # ...
#
#    # ... number testing
#    test_number_1()
#    # ...
#
#    # ... linear form testing
#    test_linear_form_1()
#    test_linear_form_2()
#    test_linear_form_11()
    test_linear_form_12()
#    test_linear_form_21()
#    # ...
#
#    # ... linear form testing
#    test_bilinear_form_1()
#    test_bilinear_form_2()
#    test_bilinear_form_11()
#    test_bilinear_form_21()
#    # ...
