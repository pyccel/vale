# coding: utf-8

from vale.parser  import ValeParser, get_by_name, annotate_form
from vale.codegen import ValeCodegen

# ... creates an instance of Vale parser
vale = ValeParser()
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
    token = annotate_form(token, ast)
    # ...

    # ...
    kernel = ValeCodegen(token)
    print (kernel.doprint("LUA"))
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
    token = annotate_form(token, ast)
    # ...

    # ...
    kernel = ValeCodegen(token)
    print (kernel.doprint("LUA"))
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
    token = annotate_form(token, ast)
    # ...

    # ...
    kernel = ValeCodegen(token)
    print (kernel.doprint("LUA"))
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
    token = annotate_form(token, ast)
    # ...

    # ...
    kernel = ValeCodegen(token)
    print (kernel.doprint("LUA"))
    # ...
# ...

######################################
if __name__ == "__main__":
#    # ... code generation for linear forms
#    test_linear_form_11()
    test_linear_form_21()
#    # ...

#    # ... code generation for bilinear forms
#    test_bilinear_form_11()
    test_bilinear_form_21()
#    # ...
