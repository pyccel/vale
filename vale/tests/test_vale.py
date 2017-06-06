# coding: utf-8

from symcc.dsl.vale import ValeCodegen
from symcc.dsl.vale import ValeParser
from symcc.dsl.vale import construct_model

from sympy import S
from sympy.core.sympify import sympify
import numpy as np


def test_vale():
    dim = 2

    expr = sympify("Ni_x*Nj_x")
    kernel = ValeCodegen(expr, dim, name="kernel", trial=True)
    print (kernel.doprint("F95"))


def test_dsl():

    # ... creates an instance of Vale parser
    vale = ValeParser()
    # ...

    # ... parse the Vale code
#    ast = vale.parse_from_file("inputs/1d/example_1.vl")
#    ast = vale.parse_from_file("inputs/2d/example_1.vl")
    ast = vale.parse_from_file("inputs/3d/example_1.vl")

#    ast = vale.parse_from_file("inputs/1d/example_2.vl")
#    ast = vale.parse_from_file("inputs/2d/example_2.vl")
#    ast = vale.parse_from_file("inputs/3d/example_2.vl")
    # ...

#    import sys; sys.exit(0)

    # ...
    def get_by_name(ast, name):
        """
        Returns an object from the AST by giving its name.
        """
        for token in ast.declarations:
            if token.name == name:
                return token
        return None
    # ...

    # ...
    b = get_by_name(ast, "b")
    a = get_by_name(ast, "a")
    # ...

    # ... TODO get dim from domain
#    for f in [b, a]:
    for f in [b]:
#    for f in [a]:
        print("============ " + str(f) + " ============")
        kernel = ValeCodegen(f)

#        print (kernel.doprint("F95"))
        print (kernel.doprint("LUA"))
    # ...

def test_model_1d():

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
        f.set("2")
        # ...

        try:
            q = pde["q"]
            q.set(np.ones(q.n_size))
        except:
            pass

        # ...
        assembler_a.assemble()
        assembler_b.assemble()
        # ...

        # ...
        matrix.export("matrix_1d.mm")
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

#        # ... plot field using matplotlib
#        import matplotlib.pyplot as plt
#
#        phi.plot(n_pts=100)
#        plt.show()
#        # ...

        # ... define the analytical solution for phi
        from clapp.vale.expressions.function import Function

        phi_analytic = Function("phi_analytic", "x*(1 - x)", args=["x"])
        # ...

        # ... compute L2 error
        x = phi.compute_l2_error(mapping=mapping, function=phi_analytic)[0,0]
        print ("    L2-error norm : " + str(x))
        # ...

        # ...
        cmd = "rm -rf input"
        os.system(cmd)
        # ...

#        # ...
#        plt.clf()
#        # ...

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

#    run(filename="inputs/1d/example_1.vl")
#    run(filename="inputs/1d/example_2.vl")
    run(filename="inputs/1d/example_3.vl")

    cmd = "rm -rf input"
    os.system(cmd)

    # ... Finalizing Clapp
    clapp_utils.finalize()
    # ...

def test_model_2d():

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

        bspline_params = BSpline([8,8], [2,2], \
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
        phi           = pde["phi"]
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
        f.set("2*x*(1-x) + 2*y*(1-y)")
        # ...

        try:
            q = pde["q"]
            q.set(np.ones(q.n_size))
        except:
            pass

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

        phi_analytic = Function("phi_analytic", "x*(1-x)*y*(1-y)", args=["x", "y"])
        # ...

        # ... compute L2 error
        x = phi.compute_l2_error(mapping=mapping, function=phi_analytic)[0,0]
        print ("    L2-error norm : " + str(x))
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

    run(filename="inputs/2d/example_1.vl")
#    run(filename="inputs/2d/example_2.vl")

    cmd = "rm -rf input"
    os.system(cmd)

    # ... Finalizing Clapp
    clapp_utils.finalize()
    # ...

def test_model_3d():

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

        bspline_params = BSpline([8,8,8], [2,2,2], \
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
        phi           = pde["phi"]
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
        f.set("2*x*(1-x)*y*(1-y) + 2*y*(1-y)*z*(1-z) + 2*z*(1-z)*x*(1-x)")
        # ...

        try:
            q = pde["q"]
            q.set(np.ones(q.n_size))
        except:
            pass

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

        phi_analytic = Function("phi_analytic", "x*(1-x)*y*(1-y)*z*(1-z)", args=["x", "y", "z"])
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

    run(filename="inputs/3d/example_1.vl")
#    run(filename="inputs/3d/example_2.vl")

    cmd = "rm -rf input"
    os.system(cmd)

    # ... Finalizing Clapp
    clapp_utils.finalize()
    # ...

######################################
if __name__ == "__main__":
#    test_vale()
#    test_dsl()
    test_model_1d()
#    test_model_2d()
#    test_model_3d()
