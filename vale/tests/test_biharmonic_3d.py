# coding: utf-8

from symcc.dsl.vale import ValeCodegen
from symcc.dsl.vale import ValeParser
from symcc.dsl.vale import construct_model

from sympy import S
from sympy.core.sympify import sympify
import numpy as np


# ...
def run(filename):
    # ...
    from caid.cad_geometry import cube
    geometry = cube()

    from clapp.spl.mapping import Mapping
    mapping = Mapping(geometry=geometry)
    # ...

    # ... creates discretization parameters
    from clapp.disco.parameters.bspline import BSpline

    bspline_params = BSpline([8,8,8], [3,3,3], \
                             bc_min=[0,0,0], \
                             bc_max=[0,0,0])
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
    expr  = "( (kx * pi) * (kx * pi) * (kx * pi) * (kx * pi) " \
            "+ (ky * pi) * (ky * pi) * (ky * pi) * (ky * pi) " \
            "+ (kz * pi) * (kz * pi) * (kz * pi) * (kz * pi))"
    expr += " * sin(kx * pi * x) * sin(ky * pi * y) * sin(kz * pi * z)"
    f.set(expr, constants={"kx": 1., "ky": 1., "kz": 1.})
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

    # ... exports phi to vtk file. Can be used in Visit and Paraview
    filename_out = "uh_3d_"+filename.split('/')[-1].split('.')[0] + ".vtk"
    phi.to_vtk(filename_out, mapping=mapping, n_pts=20)
    # ...

    # ... define the analytical solution for phi
    from clapp.vale.expressions.function import Function

    expr = "sin(kx * pi * x) * sin(ky * pi * y) * sin(kz * pi * z)"
    phi_analytic = Function("phi_analytic", expr, \
                            args=["x", "y", "z"], \
                            constants={"kx": 1., "ky": 1., "kz": 1.})
    # ...

    # ... compute L2 error
    x = phi.compute_l2_error(mapping=mapping, function=phi_analytic)[0,0]
    print ("    L2-error norm : " + str(x))
    # ...

    # ...
    cmd = "rm -rf input"
    os.system(cmd)
    # ...

    print ("> run using ", filename, " passed.")
    # ...
# ...

import clapp.common.utils      as clapp_utils

# ... initializing Clapp
clapp_utils.initialize()
# ...

import os

cmd = "rm -rf input"
os.system(cmd)

run(filename="inputs/3d/biharmonic.vl")

cmd = "rm -rf input"
os.system(cmd)

# ... Finalizing Clapp
clapp_utils.finalize()
# ...
