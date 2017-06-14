# coding: utf-8
from symcc.types.ast import For, Assign
from symcc.utilities.codegen import codegen, Result


from sympy.core.singleton import S
from sympy.core.symbol import Symbol
from sympy import Matrix
from sympy.abc import x,y,i
from sympy.tensor import Idx, Indexed, IndexedBase
from sympy.core.sympify import sympify

from vale.utilities import replace_symbol_derivatives, replace_function_with_args

__all__ = ["ValeCodegen"]

# TODO add _ at the begining of all generated variables in LUA


class Codegen(object):
    """Abstract class for code generation.

    A code generation class must provide

    * body: a list of statements
    * args: arguments for the body
    * local_vars: variables that are local and do not appear in args

    A Codegen class can be described by a function or procedure, depending on
    the backend languages.

    """
    def __init__(self, body, local_vars=None, args=None):
        """Constructor for the Codegen class.

        body: list
            list of statements.

        local_vars: list
            list of local variables.

        args: list
            list of arguments.
        """

        self._body = body

        self._local_vars = local_vars
        if local_vars is None:
            self._local_vars = []

        self._args = args
        if args is None:
            self._args = []

    @property
    def body(self):
        """Returns the body of the Codegen class"""
        return self._body

    @property
    def local_vars(self):
        """Returns the local variables of the Codegen class"""
        return self._local_vars

    @property
    def args(self):
        """Returns the arguments of the Codegen class"""
        return self._args



class Pullback(Codegen):
    """Allows to compute test and trial functions on the physical domain using the appropriate mapping.
    """
    def __init__(self, dim, n_deriv, trial=False):
        """
        Constructor for the Pullback class.

        dim: int
            dimension of the physical domain.

        n_deriv: int
            number of derivatives. Both trial and test functions are handled
            using the same n_deriv, even if the AST may give 2 different values.

        trial: bool
            if True, then the same rules will apply to trial functions.
        """
        # ...
        n1 = Symbol('n1', integer=True)
        n2 = Symbol('n2', integer=True)
        n3 = Symbol('n3', integer=True)
        # ...

        # ...
        arr_jacobian = IndexedBase('arr_jacobian')
        # ...

        # ... pullback definition
        #     TODO rename jux to u_x ?
        jux = Symbol('jux')
        jvx = Symbol('jvx')
        jwx = Symbol('jwx')

        juy = Symbol('juy')
        jvy = Symbol('jvy')
        jwy = Symbol('jwy')

        juz = Symbol('juz')
        jvz = Symbol('jvz')
        jwz = Symbol('jwz')
        # ...

        # ... second order derivatives of the mapping
        juxx = Symbol('juxx')
        jvxx = Symbol('jvxx')
        jwxx = Symbol('jwxx')
        # ...

        # ...
        Ni_u  = Symbol('Ni_u')
        Ni_v  = Symbol('Ni_v')
        Ni_w  = Symbol('Ni_w')
        Ni_uu = Symbol('Ni_uu')
        Ni_vv = Symbol('Ni_vv')
        Ni_ww = Symbol('Ni_ww')
        Ni_uv = Symbol('Ni_uv')
        Ni_vw = Symbol('Ni_vw')
        Ni_uw = Symbol('Ni_uw')

        Ni_x  = Symbol('Ni_x')
        Ni_y  = Symbol('Ni_y')
        Ni_z  = Symbol('Ni_z')
        Ni_xx = Symbol('Ni_xx')
        Ni_yy = Symbol('Ni_yy')
        Ni_zz = Symbol('Ni_zz')
        Ni_xy = Symbol('Ni_xy')
        Ni_yz = Symbol('Ni_yz')
        Ni_xz = Symbol('Ni_xz')
        # ...

        # ...
        if trial:
            Nj_u  = Symbol('Nj_u')
            Nj_v  = Symbol('Nj_v')
            Nj_w  = Symbol('Nj_w')
            Nj_uu = Symbol('Nj_uu')
            Nj_vv = Symbol('Nj_vv')
            Nj_ww = Symbol('Nj_ww')
            Nj_uv = Symbol('Nj_uv')
            Nj_vw = Symbol('Nj_vw')
            Nj_uw = Symbol('Nj_uw')

            Nj_x  = Symbol('Nj_x')
            Nj_y  = Symbol('Nj_y')
            Nj_z  = Symbol('Nj_z')
            Nj_xx = Symbol('Nj_xx')
            Nj_yy = Symbol('Nj_yy')
            Nj_zz = Symbol('Nj_zz')
            Nj_xy = Symbol('Nj_xy')
            Nj_yz = Symbol('Nj_yz')
            Nj_xz = Symbol('Nj_xz')
        # ...

        # ...
        args  = [arr_jacobian]
        # ...

        body  = []

        # ...
        if dim == 1:
            # ...
            ggg = Idx('ggg', min(1, n_deriv) * n1)
            # ...

            # ...
            if n_deriv > 1:
                body.append(Assign(ggg, sympify('2*(g1 - 1) + 1')))
                body.append(Assign(jux, arr_jacobian[ggg]))

                body.append(Assign(ggg, sympify('2*(g1 - 1) + 2')))
                body.append(Assign(juxx, arr_jacobian[ggg]))
            else:
                body.append(Assign(jux, arr_jacobian[g1]))
            # ...

            # ...
            body += [Assign(Ni_x, jux * Ni_u)]
            if n_deriv > 1:
                body += [Assign(Ni_xx, juxx * Ni_u + jux * jux * Ni_uu)]

            if trial:
                body += [Assign(Nj_x, jux * Nj_u)]

                if n_deriv > 1:
                    body += [Assign(Nj_xx, juxx * Nj_u + jux * jux * Nj_uu)]
            # ...
        elif dim == 2:
            # ...
            ggg = Idx('ggg', 4 * n1 * n2)

            body.append(Assign(ggg, sympify('4*(gg - 1) + 1')))
            body.append(Assign(jux, arr_jacobian[ggg]))

            body.append(Assign(ggg, sympify('4*(gg - 1) + 2')))
            body.append(Assign(jvx, arr_jacobian[ggg]))

            body.append(Assign(ggg, sympify('4*(gg - 1) + 3')))
            body.append(Assign(juy, arr_jacobian[ggg]))

            body.append(Assign(ggg, sympify('4*(gg - 1) + 4')))
            body.append(Assign(jvy, arr_jacobian[ggg]))
            # ...

            # ...
            body += [Assign(Ni_x, jux * Ni_u + jvx * Ni_v), \
                     Assign(Ni_y, juy * Ni_u + jvy * Ni_v)]

            if n_deriv > 1:
                body += [Assign(Ni_xx, Ni_uu), \
                         Assign(Ni_xy, Ni_uv), \
                         Assign(Ni_yy, Ni_vv)]

            if trial:
                body += [Assign(Nj_x, jux * Nj_u + jvx * Nj_v), \
                         Assign(Nj_y, juy * Nj_u + jvy * Nj_v)]

                if n_deriv > 1:
                    body += [Assign(Nj_xx, Nj_uu), \
                             Assign(Nj_xy, Nj_uv), \
                             Assign(Nj_yy, Nj_vv)]
            # ...
        elif dim == 3:
            # ...
            ggg = Idx('ggg', 9 * n1 * n2 * n3)

            body.append(Assign(ggg, sympify('9*(gg - 1) + 1')))
            body.append(Assign(jux, arr_jacobian[ggg]))

            body.append(Assign(ggg, sympify('9*(gg - 1) + 2')))
            body.append(Assign(jvx, arr_jacobian[ggg]))

            body.append(Assign(ggg, sympify('9*(gg - 1) + 3')))
            body.append(Assign(jwx, arr_jacobian[ggg]))


            body.append(Assign(ggg, sympify('9*(gg - 1) + 4')))
            body.append(Assign(juy, arr_jacobian[ggg]))

            body.append(Assign(ggg, sympify('9*(gg - 1) + 5')))
            body.append(Assign(jvy, arr_jacobian[ggg]))

            body.append(Assign(ggg, sympify('9*(gg - 1) + 6')))
            body.append(Assign(jwy, arr_jacobian[ggg]))


            body.append(Assign(ggg, sympify('9*(gg - 1) + 7')))
            body.append(Assign(juz, arr_jacobian[ggg]))

            body.append(Assign(ggg, sympify('9*(gg - 1) + 8')))
            body.append(Assign(jvz, arr_jacobian[ggg]))

            body.append(Assign(ggg, sympify('9*(gg - 1) + 9')))
            body.append(Assign(jwz, arr_jacobian[ggg]))
            # ...

            # ...
            body += [Assign(Ni_x, jux * Ni_u + jvx * Ni_v + jwx * Ni_w), \
                     Assign(Ni_y, juy * Ni_u + jvy * Ni_v + jwy * Ni_w), \
                     Assign(Ni_z, juz * Ni_u + jvz * Ni_v + jwz * Ni_w)]

            if n_deriv > 1:
                body += [Assign(Ni_xx, Ni_uu), \
                         Assign(Ni_yy, Ni_vv), \
                         Assign(Ni_zz, Ni_ww), \
                         Assign(Ni_xy, Ni_uv), \
                         Assign(Ni_yz, Ni_vw), \
                         Assign(Ni_xz, Ni_uw)]

            if trial:
                body += [Assign(Nj_x, jux * Nj_u + jvx * Nj_v + jwx * Nj_w), \
                         Assign(Nj_y, juy * Nj_u + jvy * Nj_v + jwy * Nj_w), \
                         Assign(Nj_z, juz * Nj_u + jvz * Nj_v + jwz * Nj_w)]

                if n_deriv > 1:
                    body += [Assign(Nj_xx, Nj_uu), \
                             Assign(Nj_yy, Nj_vv), \
                             Assign(Nj_zz, Nj_ww), \
                             Assign(Nj_xy, Nj_uv), \
                             Assign(Nj_yz, Nj_vw), \
                             Assign(Nj_xz, Nj_uw)]
            # ...
        # ...

        # ...
        local_vars  = []

        local_vars += [Ni_u, Ni_v, Ni_w][:dim]
        local_vars += [Ni_x, Ni_y, Ni_z][:dim]

        local_vars += [jux, jvx, jwx][:dim]
        local_vars += [juy, jvy, jwy][:dim]
        local_vars += [juz, jvz, jwz][:dim]

        if n_deriv > 1:
            if dim == 1:
                local_vars += [Ni_uu]
                local_vars += [Ni_xx]

                local_vars += [juxx]
            elif dim == 2:
                local_vars += [Ni_uu, Ni_uv, Ni_vv]
                local_vars += [Ni_xx, Ni_xy, Ni_yy]
            elif dim == 3:
                local_vars += [Ni_uu, Ni_vv, Ni_ww, Ni_uv, Ni_vw, Ni_uw]
                local_vars += [Ni_xx, Ni_yy, Ni_zz, Ni_xy, Ni_yz, Ni_xz]

        if trial:
            local_vars += [Nj_u, Nj_v, Nj_w][:dim]
            local_vars += [Nj_x, Nj_y, Nj_z][:dim]

            if n_deriv > 1:
                if dim == 1:
                    local_vars += [Nj_uu]
                    local_vars += [Nj_xx]
                elif dim == 2:
                    local_vars += [Nj_uu, Nj_uv, Nj_vv]
                    local_vars += [Nj_xx, Nj_xy, Nj_yy]
                elif dim == 3:
                    local_vars += [Nj_uu, Nj_vv, Nj_ww, Nj_uv, Nj_vw, Nj_uw]
                    local_vars += [Nj_xx, Nj_yy, Nj_zz, Nj_xy, Nj_yz, Nj_xz]
        # ...

        # ...
        super(Pullback, self).__init__(body, args=args, local_vars=local_vars)
        # ...


class Geometry(Codegen):
    """Allows to compute data related to the geometry.
    """
    def __init__(self, dim):
        """Constructor for the Geometry rule.

        dim: int
            dimension of the physical domain.

        """
        # ...
        n1 = Symbol('n1', integer=True)
        n2 = Symbol('n2', integer=True)
        n3 = Symbol('n3', integer=True)

        arr_x = IndexedBase('arr_x')
        arr_y = IndexedBase('arr_y')
        arr_z = IndexedBase('arr_z')

        arr_wvol = IndexedBase('arr_wvol')

        args  = [n1, n2, n3][:dim]
        args += [arr_wvol]
        args += [arr_x, arr_y, arr_z][:dim]
        # ...

        # ...
        g1 = Idx('g1', n1)
        g2 = Idx('g2', n2)
        g3 = Idx('g3', n3)

        x  = Symbol('x')
        y  = Symbol('y')
        z  = Symbol('z')

        wvol  = Symbol('wvol')

        local_vars  = [wvol]

        local_vars += [ x,  y,  z][:dim]
        # ...

        # ...
        body = []
        if dim == 1:
            body.append(Assign(x, arr_x[g1]))

            body.append(Assign(wvol, arr_wvol[g1]))
        if dim == 2:
            gg = Idx('gg', n1 * n2)
            body.append(Assign(gg, sympify('(g1 - 1)*n2 + g2')))

            body.append(Assign(x, arr_x[gg]))
            body.append(Assign(y, arr_y[gg]))

            body.append(Assign(wvol, arr_wvol[gg]))
        if dim == 3:
            gg = Idx('gg', n1 * n2 * n3)
            body.append(Assign(gg, sympify('(g1 - 1)*n2*n3 + (g2 - 1)*n3 + g3')))

            body.append(Assign(x, arr_x[gg]))
            body.append(Assign(y, arr_y[gg]))
            body.append(Assign(z, arr_z[gg]))

            body.append(Assign(wvol, arr_wvol[gg]))
        # ...

        super(Geometry, self).__init__(body, local_vars=local_vars, args=args)


class TestFunction(Codegen):
    """Assigns test functions from corresponding arrays.
    """
    def __init__(self, dim, n_deriv):
        """Constructor for the current rule.

        dim: int
            dimension of the physical domain.

        n_deriv: int
            number of derivatives.

        """
        # ...
        n1 = Symbol('n1', integer=True)
        n2 = Symbol('n2', integer=True)
        n3 = Symbol('n3', integer=True)

        arr_Ni1_0 = IndexedBase('arr_Ni1_0')
        arr_Ni2_0 = IndexedBase('arr_Ni2_0')
        arr_Ni3_0 = IndexedBase('arr_Ni3_0')

        arr_Ni1_s = IndexedBase('arr_Ni1_s')
        arr_Ni2_s = IndexedBase('arr_Ni2_s')
        arr_Ni3_s = IndexedBase('arr_Ni3_s')

        arr_Ni1_ss = IndexedBase('arr_Ni1_ss')
        arr_Ni2_ss = IndexedBase('arr_Ni2_ss')
        arr_Ni3_ss = IndexedBase('arr_Ni3_ss')
        # ...

        # ...
        g1 = Idx('g1', n1)
        g2 = Idx('g2', n2)
        g3 = Idx('g3', n3)

        Ni_0  = Symbol('Ni_0')
        Ni_u  = Symbol('Ni_u')
        Ni_v  = Symbol('Ni_v')
        Ni_w  = Symbol('Ni_w')
        Ni_uu = Symbol('Ni_uu')
        Ni_vv = Symbol('Ni_vv')
        Ni_ww = Symbol('Ni_ww')
        Ni_uv = Symbol('Ni_uv')
        Ni_vw = Symbol('Ni_vw')
        Ni_uw = Symbol('Ni_uw')
        # ...

        # ...
        args  = [n1, n2, n3][:dim]
        args += [arr_Ni1_0, arr_Ni2_0, arr_Ni3_0][:dim]
        args += [arr_Ni1_s, arr_Ni2_s, arr_Ni3_s][:dim]

        if n_deriv > 1:
            args += [arr_Ni1_ss, arr_Ni2_ss, arr_Ni3_ss][:dim]
        # ...

        # ...
        local_vars  = [Ni_0]
        local_vars += [Ni_u, Ni_v, Ni_w][:dim]

        if n_deriv > 1:
            if dim == 1:
                local_vars += [Ni_uu]
            elif dim == 2:
                local_vars += [Ni_uu, Ni_uv, Ni_vv]
            elif dim == 3:
                local_vars += [Ni_uu, Ni_vv, Ni_ww, Ni_uv, Ni_vw, Ni_uw]
        # ...

        # ...
        body = []

        if dim == 1:
            body.append(Assign(Ni_0, arr_Ni1_0[g1]))
            body.append(Assign(Ni_u, arr_Ni1_s[g1]))

            if n_deriv > 1:
                body.append(Assign(Ni_uu, arr_Ni1_ss[g1]))
        elif dim == 2:
            body.append(Assign(Ni_0, arr_Ni1_0[g1] * arr_Ni2_0[g2]))
            body.append(Assign(Ni_u, arr_Ni1_s[g1] * arr_Ni2_0[g2]))
            body.append(Assign(Ni_v, arr_Ni1_0[g1] * arr_Ni2_s[g2]))

            if n_deriv > 1:
                body.append(Assign(Ni_uu, arr_Ni1_ss[g1] * arr_Ni2_0[g2]))
                body.append(Assign(Ni_uv,  arr_Ni1_s[g1] * arr_Ni2_s[g2]))
                body.append(Assign(Ni_vv,  arr_Ni1_0[g1] * arr_Ni2_ss[g2]))
        elif dim == 3:
            body.append(Assign(Ni_0, arr_Ni1_0[g1] * arr_Ni2_0[g2] * arr_Ni3_0[g3]))
            body.append(Assign(Ni_u, arr_Ni1_s[g1] * arr_Ni2_0[g2] * arr_Ni3_0[g3]))
            body.append(Assign(Ni_v, arr_Ni1_0[g1] * arr_Ni2_s[g2] * arr_Ni3_0[g3]))
            body.append(Assign(Ni_w, arr_Ni1_0[g1] * arr_Ni2_0[g2] * arr_Ni3_s[g3]))

            if n_deriv > 1:
                body.append(Assign(Ni_uu, arr_Ni1_ss[g1] * arr_Ni2_0[g2] * arr_Ni3_0[g3]))
                body.append(Assign(Ni_vv, arr_Ni1_0[g1] * arr_Ni2_ss[g2] * arr_Ni3_0[g3]))
                body.append(Assign(Ni_ww, arr_Ni1_0[g1] * arr_Ni2_0[g2] * arr_Ni3_ss[g3]))
                body.append(Assign(Ni_uv, arr_Ni1_s[g1] * arr_Ni2_s[g2] * arr_Ni3_0[g3]))
                body.append(Assign(Ni_vw, arr_Ni1_0[g1] * arr_Ni2_s[g2] * arr_Ni3_s[g3]))
                body.append(Assign(Ni_uw, arr_Ni1_s[g1] * arr_Ni2_0[g2] * arr_Ni3_s[g3]))
        # ...

        super(TestFunction, self).__init__(body, local_vars=local_vars, args=args)


class TrialFunction(Codegen):
    """Assigns trial functions from corresponding arrays.
    """
    def __init__(self, dim, n_deriv):
        """Constructor for the current rule.

        dim: int
            dimension of the physical domain.

        n_deriv: int
            number of derivatives.

        """
        # ...
        n1 = Symbol('n1', integer=True)
        n2 = Symbol('n2', integer=True)
        n3 = Symbol('n3', integer=True)

        arr_Nj1_0 = IndexedBase('arr_Nj1_0')
        arr_Nj2_0 = IndexedBase('arr_Nj2_0')
        arr_Nj3_0 = IndexedBase('arr_Nj3_0')

        arr_Nj1_s = IndexedBase('arr_Nj1_s')
        arr_Nj2_s = IndexedBase('arr_Nj2_s')
        arr_Nj3_s = IndexedBase('arr_Nj3_s')

        arr_Nj1_ss = IndexedBase('arr_Nj1_ss')
        arr_Nj2_ss = IndexedBase('arr_Nj2_ss')
        arr_Nj3_ss = IndexedBase('arr_Nj3_ss')
        # ...

        # ...
        g1 = Idx('g1', n1)
        g2 = Idx('g2', n2)
        g3 = Idx('g3', n3)

        Nj_0  = Symbol('Nj_0')
        Nj_u  = Symbol('Nj_u')
        Nj_v  = Symbol('Nj_v')
        Nj_w  = Symbol('Nj_w')
        Nj_uu = Symbol('Nj_uu')
        Nj_vv = Symbol('Nj_vv')
        Nj_ww = Symbol('Nj_ww')
        Nj_uv = Symbol('Nj_uv')
        Nj_vw = Symbol('Nj_vw')
        Nj_uw = Symbol('Nj_uw')
        # ...

        # ...
        args  = [n1, n2, n3][:dim]
        args += [arr_Nj1_0, arr_Nj2_0, arr_Nj3_0][:dim]
        args += [arr_Nj1_s, arr_Nj2_s, arr_Nj3_s][:dim]

        if n_deriv > 1:
            args += [arr_Nj1_ss, arr_Nj2_ss, arr_Nj3_ss][:dim]
        # ...

        # ...
        local_vars  = [Nj_0]
        local_vars += [Nj_u, Nj_v, Nj_w][:dim]

        if n_deriv > 1:
            if dim == 1:
                local_vars += [Nj_uu]
            elif dim == 2:
                local_vars += [Nj_uu, Nj_uv, Nj_vv]
            elif dim == 3:
                local_vars += [Nj_uu, Nj_vv, Nj_ww, Nj_uv, Nj_vw, Nj_uw]
        # ...

        # ...
        body = []

        if dim == 1:
            body.append(Assign(Nj_0, arr_Nj1_0[g1]))
            body.append(Assign(Nj_u, arr_Nj1_s[g1]))

            if n_deriv > 1:
                body.append(Assign(Nj_uu, arr_Nj1_ss[g1]))
        elif dim == 2:
            body.append(Assign(Nj_0, arr_Nj1_0[g1] * arr_Nj2_0[g2]))
            body.append(Assign(Nj_u, arr_Nj1_s[g1] * arr_Nj2_0[g2]))
            body.append(Assign(Nj_v, arr_Nj1_0[g1] * arr_Nj2_s[g2]))

            if n_deriv > 1:
                body.append(Assign(Nj_uu, arr_Nj1_ss[g1] * arr_Nj2_0[g2]))
                body.append(Assign(Nj_uv,  arr_Nj1_s[g1] * arr_Nj2_s[g2]))
                body.append(Assign(Nj_vv,  arr_Nj1_0[g1] * arr_Nj2_ss[g2]))
        elif dim == 3:
            body.append(Assign(Nj_0, arr_Nj1_0[g1] * arr_Nj2_0[g2] * arr_Nj3_0[g3]))
            body.append(Assign(Nj_u, arr_Nj1_s[g1] * arr_Nj2_0[g2] * arr_Nj3_0[g3]))
            body.append(Assign(Nj_v, arr_Nj1_0[g1] * arr_Nj2_s[g2] * arr_Nj3_0[g3]))
            body.append(Assign(Nj_w, arr_Nj1_0[g1] * arr_Nj2_0[g2] * arr_Nj3_s[g3]))

            if n_deriv > 1:
                body.append(Assign(Nj_uu, arr_Nj1_ss[g1] * arr_Nj2_0[g2] * arr_Nj3_0[g3]))
                body.append(Assign(Nj_vv, arr_Nj1_0[g1] * arr_Nj2_ss[g2] * arr_Nj3_0[g3]))
                body.append(Assign(Nj_ww, arr_Nj1_0[g1] * arr_Nj2_0[g2] * arr_Nj3_ss[g3]))
                body.append(Assign(Nj_uv, arr_Nj1_s[g1] * arr_Nj2_s[g2] * arr_Nj3_0[g3]))
                body.append(Assign(Nj_vw, arr_Nj1_0[g1] * arr_Nj2_s[g2] * arr_Nj3_s[g3]))
                body.append(Assign(Nj_uw, arr_Nj1_s[g1] * arr_Nj2_0[g2] * arr_Nj3_s[g3]))
        # ...

        super(TrialFunction, self).__init__(body, local_vars=local_vars, args=args)


class Field(Codegen):
    """Allows to handle fields as additional inputs to Finite Elements kernels.
    """
    def __init__(self, dim, n_deriv, fields, **settings):
        """Constructor for the field rule.

        dim: int
            dimension of the physical domain.

        n_deriv: int
            number of derivatives.

        fields: list
            list of field names as given from the parser.

        n_deriv_fields: int
            number of derivatives applied to the field.

        """
        # ...
        n1 = Symbol('n1', integer=True)
        n2 = Symbol('n2', integer=True)
        n3 = Symbol('n3', integer=True)
        # ...

        # ...
        n_fields = Symbol('n_fields', integer=True)
        n_deriv  = Symbol('n_deriv',  integer=True)

        arr_fields = IndexedBase('arr_fields')

        args  = [n_fields, n_deriv]
        args += [arr_fields]
        # ...

        # ...
        ns = [n1, n2, n3][:dim]
        n = S.One
        for k in range(0, dim):
            n *= ns[k]
        # ...

        # ...
        def assign_index(i_field, i_deriv):
            """
            i_field in [1, n_fields]
            i_deriv in [0, n_deriv]
            """
            if dim == 1:
                expr = '(g1-1)*n_fields*(n_deriv+1) + (i_field-1)*(n_deriv+1) + i_deriv + 1'
            else:
                expr = '(gg-1)*n_fields*(n_deriv+1) + (i_field-1)*(n_deriv+1) + i_deriv + 1'
            expr = sympify(expr)
            expr = expr.subs({Symbol("i_field"): i_field})
            expr = expr.subs({Symbol("i_deriv"): i_deriv})

            return Assign(i_f, expr)
        # ...

        # ...
        n_deriv_fields = settings["n_deriv_fields"]
        # ...

        # ...
        local_vars = []
        body = []
        i_f  = Idx('i_f', n*n_fields*(n_deriv+1))
        for i_field, field in enumerate(fields):
            # ... value on quad points
            local_vars  += [Symbol(str(field) + "_0")]

            body.append(assign_index(i_field+1, i_deriv=0))
            body.append(Assign(Symbol(str(field) + "_0"), arr_fields[i_f]))
            # ...

            # ... field derivatives
            if n_deriv_fields > 0:
                for axis, d in enumerate(["x","y","z"][:dim]):
                    local_vars  += [Symbol(str(field) + "_" + d)]

                    body.append(assign_index(i_field+1, i_deriv=axis+1))
                    body.append(Assign(Symbol(str(field) + "_" + d), arr_fields[i_f]))
            # ...
        # ...

        super(Field, self).__init__(body, local_vars=local_vars, args=args)


class Formulation(Codegen):
    """An abstract rule for Bilinear and Linear Forms.
    """
    def __init__(self, expr):
        """Constructor of a Bilinear/Linear form rule from a sympy expression.

        expr: sympy.Expression
            a symbolic expression describing the bilinear/linear form.
        """
        wvol = Symbol("wvol")

        body       = []
        local_vars = []
        args       = []
        if type(expr) == dict:
            for key, form in expr.items():
                txt = "contribution_"
                if type(key) == int:
                    label = str(key)
                elif type(key) in [tuple, list]:
                    label = str(key[0]) + str(key[1])
                else:
                    raise TypeError("expecting int or (tuple, list) but given : %s" % type(key))

                txt += label
                contribution = Symbol(txt)

                body += [Assign(contribution, contribution + form * wvol)]
                args += [contribution]
        else:
            contribution = Symbol("contribution")

            body += [Assign(contribution, contribution + expr * wvol)]
            args += [contribution]

        super(Formulation, self).__init__(body, local_vars=local_vars, args=args)


class ValeCodegen(Codegen):
    """Code generation for the Vale Grammar"""
    def __init__(self, expr, dim=None, name=None, trial=False, ast=None):
        """
        Generates the kernel associated to a linear/bilinear form.

        expr: sympy.expression or LinearForm or BilinearForm
            if expr is a LinearForm or BilinearForm, then either dim or ast must
            be provided, in addition to trial if expr describes the expression
            of a bilinear form.

        dim: int
            dimension of the physical domain.

        name: str
            name to give for the kernel function/subroutine

        trial: bool
            if True and expr is a sympy expression then, it will define a
            bilinear form.

        ast: list
            the AST as given by the parser.

        """
        from vale.syntax import LinearForm, BilinearForm

        _expr   = None
        _name   = None
        _dim    = None
        _trial  = False
        _n_rows = None
        _n_cols = None
        user_fields = []
        n_deriv = 1
        n_deriv_fields = 0
        n_blocks = 1

        if isinstance(expr, LinearForm):
            _expr = expr.to_sympy()
            for f in expr.args.functions:
                _expr = replace_symbol_derivatives(_expr, f, "Ni")

            _name = "kernel_" + expr.name
            _dim  = expr.attributs["dim"]

            # TODO get n_rows from LinearForm
            _n_rows = Symbol('n_rows', integer=True)

            # update calls to functions
            user_functions = expr.attributs["user_functions"]
            for f_name in user_functions:
                args = ["x", "y", "z"][:_dim]
                _expr = replace_function_with_args(_expr, f_name, args)

            # list of fields
            user_fields = expr.attributs["user_fields"]
            for f_name in user_fields:
                _expr = _expr.subs(Symbol(f_name), Symbol(f_name+"_0"))

            n_deriv        = expr.n_deriv
            n_deriv_fields = expr.n_deriv_fields
            n_blocks       = expr.n_rows

        elif isinstance(expr, BilinearForm):
            _expr = expr.to_sympy()
            for f in expr.args_test.functions:
                _expr = replace_symbol_derivatives(_expr, f, "Ni")

            for f in expr.args_trial.functions:
                _expr = replace_symbol_derivatives(_expr, f, "Nj")

            _name  = "kernel_" + expr.name
            _dim   = expr.attributs["dim"]
            _trial = True

            # TODO get n_rows,n_cols from BilinearForm
            _n_rows = Symbol('n_rows', integer=True)
            _n_cols = Symbol('n_cols', integer=True)

            # update calls to functions
            user_functions = expr.attributs["user_functions"]
            for f_name in user_functions:
                args = ["x", "y", "z"][:_dim]
                _expr = replace_function_with_args(_expr, f_name, args)

            # list of fields
            user_fields = expr.attributs["user_fields"]
            for f_name in user_fields:
                _expr = _expr.subs(Symbol(f_name), Symbol(f_name+"_0"))

            n_deriv        = expr.n_deriv
            n_deriv_fields = expr.n_deriv_fields
            n_blocks       = [expr.n_rows, expr.n_cols]

        else:
            if not(dim is None) or not(name is None):
                raise ValueError("Both dim and name must be provided.")

            _expr  = expr
            _name  = name
            _dim   = dim
            _trial = trial

        self._name = _name

        stmts  = []
        stmts += [Geometry(_dim), \
                  TestFunction(_dim, n_deriv)]
        if _trial:
            stmts += [TrialFunction(_dim, n_deriv)]

        stmts += [Pullback(_dim, n_deriv, trial=_trial)]

        if len(user_fields) > 0:
            stmts += [Field(_dim, n_deriv, user_fields,
                            n_deriv_fields=n_deriv_fields)]

        stmts += [Formulation(_expr)]


        body       = []
        local_vars = []
        args       = []

        if not(_n_rows is None):
            args.append(_n_rows)

        if not(_n_cols is None):
            args.append(_n_cols)

        for stmt in stmts:
            if isinstance(stmt, Codegen):
                body       += stmt.body
                local_vars += stmt.local_vars
                args       += stmt.args
            elif isinstance(stmt, For):
                body       += stmt.body
                local_vars += stmt.target
                args       += stmt.iterable.stop
            else:
                raise ValueError("Unknown statement : %s" % stmt)

        # ...
        g1 = Symbol('g1', integer=True)
        n1 = Symbol('n1', integer=True)

        g2 = Symbol('g2', integer=True)
        n2 = Symbol('n2', integer=True)

        g3 = Symbol('g3', integer=True)
        n3 = Symbol('n3', integer=True)

        if _dim >= 3:
            body = [For(g3, (1, n3, 1), body)]
        if _dim >= 2:
            body = [For(g2, (1, n2, 1), body)]
        body = [For(g1, (1, n1, 1), body)]
        # ...

        # ...
        if type(_expr) == dict:
            for key, form in _expr.items():
                txt = "contribution_"
                if type(key) == int:
                    label = str(key)
                elif type(key) in [tuple, list]:
                    label = str(key[0]) + str(key[1])
                else:
                    raise TypeError("expecting int or (tuple, list) but given : %s" % type(key))

                txt += label
                contribution = Symbol(txt)
                body.insert(0, Assign(contribution, 0.))
        else:
            contribution = Symbol("contribution")
            body.insert(0, Assign(contribution, 0.))
        # ...

        # ...
        self._expr = _expr
        self._n_blocks = n_blocks
        # ...

        super(ValeCodegen, self).__init__(body, \
                                            local_vars=local_vars, \
                                            args=args)

    @property
    def name(self):
        """Returns the name of the current kernel."""
        return self._name

    @property
    def expr(self):
        """Returns the expression to print"""
        return self._expr

    @property
    def n_blocks(self):
        """Returns the number of blocks to print"""
        return self._n_blocks

    def doprint(self, language):
        """Generate the current kernel in the given language.

        language: str
            target language. Possible values {"LUA", "F95"}
        """
        args        = self.args
        local_vars  = self.local_vars
        return_vars = []
        if language in ["LUA"]:
            # ...
            if type(self.expr) == dict:
                # we order the dictionary with respect to the keys
                from collections import OrderedDict, Counter
                expr = OrderedDict(sorted(self.expr.items(), \
                                          key= lambda t:str(t[0]).lower()))

                for key, form in expr.items():
                    txt = "contribution_"
                    if type(key) == int:
                        label = str(key)
                    elif type(key) in [tuple, list]:
                        label = str(key[0]) + str(key[1])
                    else:
                        raise TypeError("expecting int or (tuple, list) but given : %s" % type(key))

                    txt += label
                    contribution = Symbol(txt)

                    args.remove(contribution)
                    local_vars.append(contribution)
                    return_vars.append(Result(contribution, \
                                              name=Symbol("output_"+label)))

                # ... linear form case
                if type(self.n_blocks) == int:
                    n_rows = self.n_blocks
                    for i in range(0, n_rows):
                        if not expr.has_key(i):
                            label = str(i)
                            return_vars.append(Result(sympify("0.0"), \
                                                      name=Symbol("output_"+label)))

                elif type(self.n_blocks) in [tuple, list]:
                    n_rows = self.n_blocks[0]
                    n_cols = self.n_blocks[1]
                    for i in range(0, n_rows):
                        for j in range(0, n_cols):
                            if not expr.has_key((i,j)):
                                label = str(i) + str(j)
                                return_vars.append(Result(sympify("0.0"), \
                                                          name=Symbol("output_"+label)))
                else:
                    raise TypeError("expecting int or (tuple, list) but given : %s" % type(key))
                # ...

            else:
                args.remove(Symbol("contribution"))
                local_vars.append(Symbol("contribution"))
                return_vars.append(Result(Symbol("contribution"), \
                                          name=Symbol("output")))
            # ...

            [(f_name, f_code)] = codegen((self.name, self.body), language, \
                                         header=False, empty=True, \
                                         argument_sequence=set(args), \
                                         local_vars=set(local_vars), \
                                         return_vars=return_vars)
        else:
            [(f_name, f_code), header] = codegen((self.name, self.body), language, \
                                                 header=False, empty=True, \
                                                 argument_sequence=set(args), \
                                                 local_vars=set(local_vars), \
                                                 return_vars=return_vars)

        return f_code

