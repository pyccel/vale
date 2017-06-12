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
    from caid.cad_geometry import line
    geometry = line()

    from clapp.spl.mapping import Mapping
    mapping = Mapping(geometry=geometry)
    # ...

    # ... creates discretization parameters
    from clapp.disco.parameters.bspline import BSpline

    bspline_params = BSpline([8], [2], \
                             bc_min=[0], \
                             bc_max=[0])
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
    psi         = pde["psi"]
    form_a      = pde["a"]
    form_b      = pde["b"]
    f           = pde["f"]
    g           = pde["g"]
    # ...

    # ...
    assembler_a = form_a.assembler
    matrix      = form_a.matrix
    assembler_b = form_b.assembler
    rhs         = form_b.vector
    # ...

    # ... set expression for the function f
    f.set("2")
    # ...

    # ... set expression for the function g
    g.set("0")
    # ...

    # ...
    assembler_b.assemble()
    assembler_a.assemble()
    # ...
#    rhs.export("rhs.txt")
#    matrix.export("matrix.mm")

    # ...
    from clapp.plaf.parameters.linear_solver import LAPACK_LU
    from clapp.plaf.parameters.linear_solver import PACK_GMRES
    from clapp.plaf.parameters.linear_solver import DRIVER
    from clapp.plaf.linear_solver  import Linear_solver

#    params = DRIVER(solver=LAPACK_LU())
    params = DRIVER(solver=PACK_GMRES())
    linsol = Linear_solver(matrix=matrix, dirname="input", parameters=params)
    # ...

    # ...
    z = rhs.get()
    print "z0 : ", z[0,:]
    print "z1 : ", z[1,:]
    n,m = z.shape
    y = linsol.solve(z.ravel())
    # ...

    # ... exports the field
    print "y0 : ", y[:m]
    print "y1 : ", y[m:]
    phi.set(y[:m])
    psi.set(y[m:])
    # ...

#    import sys; sys.exit(0)

    # ... plot field using matplotlib
    import matplotlib.pyplot as plt

    phi.plot(n_pts=100)
    plt.show()

    psi.plot(n_pts=100)
    plt.show()
    # ...

    # ... define the analytical solution for phi
    from clapp.vale.expressions.function import Function

    phi_analytic = Function("phi_analytic", "x*(1 - x)", args=["x"])
    psi_analytic = Function("psi_analytic", "2*x*(1 - x)", args=["x"])
    # ...

    # ... compute L2 error
    x = phi.compute_l2_error(mapping=mapping, function=phi_analytic)[0,0]
    print ("    L2-error norm (phi): " + str(x))

    x = psi.compute_l2_error(mapping=mapping, function=psi_analytic)[0,0]
    print ("    L2-error norm (psi): " + str(x))
    # ...

    # ...
    cmd = "rm -rf input"
    os.system(cmd)
    # ...

    # ...
    plt.clf()
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

run(filename="inputs/1d/poisson_block.vl")

cmd = "rm -rf input"
os.system(cmd)

# ... Finalizing Clapp
clapp_utils.finalize()
# ...
