# coding: utf-8

from vale.parser  import ValeParser, get_by_name
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
    # ...

    # ...
    kernel = ValeCodegen(token)
    print (kernel.doprint("LUA"))
    # ...

# ...

#def test_dsl():
#
#    # ... creates an instance of Vale parser
#    vale = ValeParser()
#    # ...
#
#    # ... parse the Vale code
##    ast = vale.parse_from_file("inputs/1d/example_1.vl")
##    ast = vale.parse_from_file("inputs/2d/example_1.vl")
#    ast = vale.parse_from_file("inputs/3d/example_1.vl")
#
##    ast = vale.parse_from_file("inputs/1d/example_2.vl")
##    ast = vale.parse_from_file("inputs/2d/example_2.vl")
##    ast = vale.parse_from_file("inputs/3d/example_2.vl")
#    # ...
#
##    import sys; sys.exit(0)
#
#    # ...
#    def get_by_name(ast, name):
#        """
#        Returns an object from the AST by giving its name.
#        """
#        for token in ast.declarations:
#            if token.name == name:
#                return token
#        return None
#    # ...
#
#    # ...
#    b = get_by_name(ast, "b")
#    a = get_by_name(ast, "a")
#    # ...
#
#    # ... TODO get dim from domain
##    for f in [b, a]:
#    for f in [b]:
##    for f in [a]:
#        print("============ " + str(f) + " ============")
#        kernel = ValeCodegen(f)
#
##        print (kernel.doprint("F95"))
#        print (kernel.doprint("LUA"))
#    # ...


######################################
if __name__ == "__main__":
    test_linear_form_11()
