# coding: utf-8

from sympy import Symbol, sympify, Matrix
from sympy.core.singleton import S
from sympy.core.function import Function

__all__ = ["grad", "d_var", "dot", \
           "cross", "outer", "inner", \
           "replace_symbol_derivatives"]


# ...
def grad(expr, dim):
    """
    Returns the sympy expression for the gradient applied to expr.

    expr: sympy.expression
        a sympy expression

    dim: int
        dimension of the manifold
    """
    args = ['x', 'y', 'z']

    g = []
    for x in args[:dim]:
        u_x = d_var(expr, x)
        g.append(u_x)

    return Matrix(g)
# ...

# ...
def d_var(expr, var):
    """
    Returns the sympy expression for the derivative with respect to var applied to expr.

    expr: sympy.expression
        a sympy expression

    var: str
        variable over which we compute the derivative
    """
    return Symbol(expr.name + "_" + var)
# ...

# ...
def dot(a, b):
    """
    dot product of two vectors.

    a: sympy.expression
        a vector as sympy expression

    b: sympy.expression
        a vector as sympy expression
    """
    # TODO must check that a and b are vectors or matrix with shape[1] = 1
    v1 = a[:,0]
    v2 = b[:,0]
    return v1.dot(v2)
# ...

# ...
def cross(a, b):
    """
    cross product of two vectors.

    a: sympy.expression
        a matrix as sympy expression

    b: sympy.expression
        a matrix as sympy expression
    """
    # TODO must check that a and b are vectors or matrix with shape[1] = 1
    v1 = a[:,0]
    v2 = b[:,0]
    return v1.cross(v2)
# ...

# ...
def outer(a, b):
    """
    outer product of two vectors.

    a: sympy.expression
        a matrix as sympy expression

    b: sympy.expression
        a matrix as sympy expression
    """
    # TODO must check that a and b are vectors or matrix with shape[1] = 1
    v1 = a[:,0]
    v2 = b[:,0]

    n = a.shape[0]
    m = b.shape[0]

    expr = Matrix(n,m, lambda i,j: 0)
    for i in range(0, n):
        for j in range(0, m):
            expr[i,j] = a[i] * b[j]
    return expr
# ...

# ...
def inner(a, b):
    """
    inner product of two matrices.

    a: sympy.expression
        a matrix as sympy expression

    b: sympy.expression
        a matrix as sympy expression
    """
    # TODO check dimensions
    n = a.shape[0]
    m = a.shape[1]

    expr = S.Zero
    for i in range(0, n):
        for j in range(0, m):
            expr += a[i,j] * b[i,j]

    return expr
# ...

# TODO use this function in codegen and everywhere it is needed, to avoid code
#      duplication
# ...
def replace_symbol_derivatives(expr, f, B):
    """Replaces derivatives of the symbol f by those of B in a sympy expression.

    expr: sympy.Expression
        sympy expression, for linear or bilinear form.

    f: str
        name of the symbol to replace

    B: str
        name of the new symbol
    """
    if type(expr) == dict:
        for key, form in expr.items():
            expr[key] = replace_symbol_derivatives(form, f, B)
    else:
        expr = expr.subs({Symbol(f): Symbol(B)})
        expr = expr.subs({Symbol(f + "_0"): Symbol(B + "_0")})

        for d in ["x", "y", "z"]:
            expr = expr.subs({Symbol(f + "_" + d): Symbol(B + "_" + d)})
        for d in ["xx", "yy", "zz", "xy", "yz", "xz"]:
            expr = expr.subs({Symbol(f + "_" + d): Symbol(B + "_" + d)})

    return expr
# ...

# TODO use this function in codegen and everywhere it is needed, to avoid code
#      duplication
# ...
def replace_function_with_args(expr, f_name, args):
    """Replaces derivatives of the symbol f by those of B in a sympy expression.

    expr: sympy.Expression
        sympy expression, for linear or bilinear form.

    f: str
        name of the symbol to replace

    args: list of str
        arguments to give to the function. example: ["x", "y"]
    """
    if type(expr) == dict:
        for key, form in expr.items():
            expr[key] = replace_function_with_args(form, f_name, args)
    else:
        dim = len(args)
        if dim == 1:
            f = Function(f_name)(Symbol(args[0]))
        elif dim == 2:
            f = Function(f_name)(Symbol(args[0]), Symbol(args[1]))
        elif dim == 3:
            f = Function(f_name)(Symbol(args[0]), Symbol(args[1]), Symbol(args[2]))

        expr = expr.subs(Symbol(f_name), f)

    return expr
# ...
