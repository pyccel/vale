# coding: utf-8

from vale import ValeCodegen
from vale import ValeParser
from vale import construct_model

from sympy import S
from sympy.core.sympify import sympify
import numpy as np


# ...
def run(filename):
    # ...
    from caid.cad_geometry import square
    geometry = square()

    from clapp.spl.mapping import Mapping
    mapping = Mapping(geometry=geometry)
    # ...

    # ... creates discretization parameters
    from clapp.disco.parameters.bspline import BSpline

    bspline_params = BSpline([16,16], [3,3], \
                             bc_min=[0,0], \
                             bc_max=[0,0])
    # ...

    # ... create a context from discretization
    from clapp.fema.context        import Context

    context = Context(dirname="input", \
                      discretization_params=bspline_params)
    # ...

    # ...
    pde = construct_model(filename, backend="clapp", \
                          context=context, mapping=mapping)
    # ...

    # ... accessing the pde declarations
    V           = pde["V"]
    phi         = pde["phi"]
    form_a      = pde["a"]
    form_b      = pde["b"]
    f           = pde["f"]
    # ...

    # ...
    assembler_a = form_a.assembler
    matrix      = form_a.matrix
    assembler_b = form_b.assembler
    rhs         = form_b.vector
    # ...

    # ... set expression for the function f
    expr = "((kx * pi) * (kx * pi) * (kx * pi) * (kx * pi) + (ky * pi) * (ky * pi) * (ky * pi) * (ky * pi)) " + \
           " * sin(kx * pi * x) * sin(ky * pi * y)"
    f.set(expr, constants={"kx": 2., "ky": 2.})
    # ...

    # ...
    assembler_a.assemble()
    assembler_b.assemble()
    # ...

    # ...
    from clapp.plaf.parameters.linear_solver import LAPACK_LU
    from clapp.plaf.parameters.linear_solver import DRIVER
    from clapp.plaf.linear_solver  import Linear_solver

    params = DRIVER(solver=LAPACK_LU())
    linsol = Linear_solver(matrix=matrix, dirname="input", parameters=params)
    # ...

    # ...
    y = linsol.solve(rhs)
    # ...

    # ... exports the field
    phi.set(y)
    # ...

    # ... plot field using matplotlib
    import matplotlib.pyplot as plt

    phi.plot(n_pts=100)
    plt.colorbar()
    plt.show()
    # ...

    # ... define the analytical solution for phi
    from clapp.vale.expressions.function import Function

    expr = "sin(kx * pi * x) * sin(ky * pi * y)"
    phi_analytic = Function("phi_analytic", expr, \
                            args=["x", "y"], \
                            constants={"kx": 2., "ky": 2.})
    # ...

    # ... compute L2 error
    x = phi.compute_l2_error(mapping=mapping, function=phi_analytic)[0,0]
    print(("    L2-error norm : " + str(x)))
    # ...

    # ...
    cmd = "rm -rf input"
    os.system(cmd)
    # ...

    # ...
    plt.clf()
    # ...

    print(("> run using ", filename, " passed."))
    # ...
# ...

import clapp.common.utils      as clapp_utils

# ... initializing Clapp
clapp_utils.initialize()
# ...

import os

cmd = "rm -rf input"
os.system(cmd)

run(filename="inputs/2d/biharmonic.vl")

cmd = "rm -rf input"
os.system(cmd)

# ... Finalizing Clapp
clapp_utils.finalize()
# ...
