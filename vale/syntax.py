# coding: utf-8

from sympy import Symbol, sympify

from vale.utilities import grad, d_var, inner, outer, cross, dot


__all__ = ["Vale", \
           "Expression", "Term", "Operand", \
           "FactorSigned", "FactorUnary", "FactorBinary", \
           "LinearForm", "BilinearForm", \
           "BodyForm", "SimpleBodyForm", "ExpressionBodyForm", \
           "TermForm", "CallForm", \
           "Domain", "Space", "Field", "Function", "Real", \
           "replace_symbol_derivatives"
           ]


# Global variable namespace
namespace = {}
stack     = {}
settings  = {}

operators = {}
operators["1"] = ["dx", "dy", "dz"]
operators["2"] = ["dxx", "dyy", "dzz", "dxy", "dyz", "dxz"]

# TODO use this function in codegen and everywhere it is needed, to avoid code
#      duplication
def replace_symbol_derivatives(expr, f, B):
    """Replaces derivatives of the symbol f by those of B in a sympy expression.

    expr: sympy.Expression
        sympy expression, for linear or bilinear form.

    f: str
        name of the symbol to replace

    B: str
        name of the new symbol
    """
    expr = expr.subs({Symbol(f): Symbol(B)})
    expr = expr.subs({Symbol(f + "_0"): Symbol(B + "_0")})

    for d in ["x", "y", "z"]:
        expr = expr.subs({Symbol(f + "_" + d): Symbol(B + "_" + d)})
    for d in ["xx", "yy", "zz", "xy", "yz", "xz"]:
        expr = expr.subs({Symbol(f + "_" + d): Symbol(B + "_" + d)})
    return expr


class Vale(object):
    """Class for Vale syntax."""
    def __init__(self, **kwargs):
        """
        Constructor for Vale.

        In Vale, we only have declarations for the moment.
        """
        self.declarations = kwargs.pop('declarations')

class Domain(object):
    """Class representing a Domain."""
    def __init__(self, **kwargs):
        """
        A Domain has the following attributs

        * name
        * dim
        * kind

        .. note::
            The grammar rule to define a Domain is

            Domain:
            "Domain" LPAREN "dim" EQ dim=INT COMMA "kind" EQ kind=STRING RPAREN DEF name=ID
            ;
        """
        self.name = kwargs.pop('name')
        self.dim  = kwargs.pop('dim')
        self.kind = kwargs.pop('kind')

        namespace[self.name] = self

class Space(object):
    """Class representing a Finite Element Space."""
    def __init__(self, **kwargs):
        """
        A Space has the following attributs

        * name
        * domain
        * kind

        .. note::
            The grammar rule to define a Space is

            Space:
            "Space" LPAREN "domain" EQ domain=ID COMMA "kind" EQ kind=STRING RPAREN  DEF name=ID
            ;
        """
        self.name   = kwargs.pop('name')
        self.domain = kwargs.pop('domain')
        self.kind   = kwargs.pop('kind')

        namespace[self.name] = self

class Field(object):
    """Class representing a Field."""
    def __init__(self, **kwargs):
        """
        A Field has the following attributs

        * name
        * space

        .. note::
            The grammar rule to define a Field is

            Field:
            "Field" LPAREN "space" EQ space=ID RPAREN  DEF name=ID
            ;
        """
        self.name  = kwargs.pop('name')
        self.space = kwargs.pop('space')

        namespace[self.name] = self

    @property
    def expr(self):
        return Symbol(self.name)

class Real(object):
    """Class representing a Real number."""
    def __init__(self, **kwargs):
        """
        A Real number is defined by

        * name

        .. note::
            The grammar rule to define a Real is

            Real:
            "Real" DEF name=ID
            ;
        """
        self.name  = kwargs.pop('name')

        namespace[self.name] = self

    @property
    def expr(self):
        return Symbol(self.name)


class Function(object):
    """Class representing a Function."""
    def __init__(self, **kwargs):
        """
        A Function has the following attributs

        * name
        * parameters

        .. note::
            The grammar rule to define a Function is

            Function:
            "Function" LPAREN parameters*=ID[','] RPAREN  DEF name=ID
            ;
        """
        self.name       = kwargs.pop('name')
        self.parameters = kwargs.pop('parameters', {})

        namespace[self.name] = self

    @property
    def expr(self):
        return Symbol(self.name)


class Form(object):
    """Abstract Class for Linear/Bilinear forms."""
    def __init__(self, **kwargs):
        self._attributs = {}

    @property
    def attributs(self):
        return self._attributs

    def set(self, attribut, value):
        """Sets value to the attribut"""
        if attribut in self._available_attributs:
            self._attributs[attribut] = value
        else:
            raise ValueError("Unknown attribut : %s" % attribut)


class LinearForm(Form):
    """Class representing a Linear Form."""
    _available_attributs = ["dim", \
                            "space", \
                            "user_fields", \
                            "user_functions", \
                            "user_constants"]

    def __init__(self, **kwargs):
        """
        A Domain has the following attributs

        * name
        * args
        * body
        * -- domain
        * -- expression

        .. note::
            The grammar rule to define a LinearForm is

            LinearForm:
            name=ID
            LPAREN
            args=ArgForm
            RPAREN
            DEF
            LTRIANGLE
            expression=Expression
            RTRIANGLE SUBSCRIPT domain=ID
            ;
        """
        self.name       = kwargs.pop('name')
        self.args       = kwargs.pop('args')
        self.body       = kwargs.pop('body')
        self.blocks     = None

        namespace[self.name] = self

        super(LinearForm, self).__init__(**kwargs)

        if isinstance(self.body, SimpleBodyForm):
            self.domain     = self.body.domain
            self.expression = self.body.expression
        elif isinstance(self.body, ExpressionBodyForm):
            self.blocks     = {}

            # ... 
            stack["parent"] = self.name
            self.body.expr
            stack.pop("parent")
            # ... 

            # ... TODO check domain
            for key, form in self.blocks.items():
                self.domain = form.domain
                break
            # ... 
        else:
            raise Exception('Could not parse the linear form body at position {}'
                            .format(self._tx_position))

        self.set("dim", namespace[self.domain].dim)
        self.set("user_fields",    [])
        self.set("user_functions", [])
        self.set("user_constants", [])

        self.set("space", self.args.space)

    def to_sympy(self):
        if type(self.blocks) == dict:
            expr = {}
            for key, form in self.blocks.items():
                expr[key] = form.to_sympy()
                if len(form.args.functions) == 1:
                    old = form.args.functions[0]
                    new = self.args.functions[key]

                    expr[key] = replace_symbol_derivatives(expr[key], old, new)
                else:
                    raise ValueError("Expecting one argument but given: %s" % form.args.functions)

        else:
            for f in self.args.functions:
                stack[f] = f

            settings["n_deriv"] = 0
            settings["n_deriv_fields"] = 0

            expr = self.expression.expr

            for f in self.args.functions:
                stack.pop(f)

            self.n_deriv        = settings["n_deriv"]
            self.n_deriv_fields = settings["n_deriv_fields"]

            settings.pop("n_deriv")
            settings.pop("n_deriv_fields")

#        print(">> Linear.n_deriv        : " + str(self.n_deriv))
#        print(">> Linear.n_deriv_fields : " + str(self.n_deriv_fields))

        return expr

class BilinearForm(Form):
    """Class representing a Bilinear Form."""
    _available_attributs = ["dim", \
                            "space_test", \
                            "space_trial", \
                            "user_fields", \
                            "user_functions", \
                            "user_constants"]

    def __init__(self, **kwargs):
        """
        A Domain has the following attributs

        * name
        * args
        * domain
        * expression

        .. note::
            The grammar rule to define a LinearForm is

            BilinearForm:
            name=ID
            LPAREN
            args_test=ArgForm
            COMMA
            args_trial=ArgForm
            RPAREN
            DEF
            LTRIANGLE
            expression=Expression
            RTRIANGLE SUBSCRIPT domain=ID
            ;
        """
        self.name       = kwargs.pop('name')
        self.args_test  = kwargs.pop('args_test')
        self.args_trial = kwargs.pop('args_trial')
        self.body       = kwargs.pop('body')
        self.blocks     = None

        namespace[self.name] = self

        super(BilinearForm, self).__init__(**kwargs)

        if isinstance(self.body, SimpleBodyForm):
            self.domain     = self.body.domain
            self.expression = self.body.expression
        elif isinstance(self.body, ExpressionBodyForm):
            self.blocks     = {}

            # ... 
            stack["parent"] = self.name
            self.body.expr
            stack.pop("parent")
            # ... 

            # ... TODO check domain
            for key, form in self.blocks.items():
                self.domain = form.domain
                break
            # ... 
        else:
            raise Exception('Could not parse the bilinear form body at position {}'
                            .format(self._tx_position))

        self.set("dim", namespace[self.domain].dim)
        self.set("user_fields",    [])
        self.set("user_functions", [])
        self.set("user_constants", [])

        self.set("space_test",  self.args_test.space)
        self.set("space_trial", self.args_trial.space)


    def to_sympy(self):
        if type(self.blocks) == dict:
            expr = {}
            for key, form in self.blocks.items():
                expr[key] = form.to_sympy()
                if (len(form.args_test.functions) == 1) and \
                   (len(form.args_trial.functions) == 1):

                    # ...
                    old = form.args_test.functions[0]
                    new = self.args_test.functions[key[0]]

                    expr[key] = replace_symbol_derivatives(expr[key], old, new)
                    # ...

                    # ...
                    old = form.args_trial.functions[0]
                    new = self.args_trial.functions[key[1]]

                    expr[key] = replace_symbol_derivatives(expr[key], old, new)
                    # ...
                else:
                    raise ValueError("Expecting one argument but given: %s" % form.args.functions)
        else:
            args = self.args_test.functions + self.args_trial.functions
            for f in args:
                stack[f] = f

            settings["n_deriv"] = 0
            settings["n_deriv_fields"] = 0

            expr = self.expression.expr

            for f in args:
                stack.pop(f)

            self.n_deriv        = settings["n_deriv"]
            self.n_deriv_fields = settings["n_deriv_fields"]

            settings.pop("n_deriv")
            settings.pop("n_deriv_fields")

#        print(">> Bilinear.n_deriv        : " + str(self.n_deriv))
#        print(">> Bilinear.n_deriv_fields : " + str(self.n_deriv_fields))

        return expr


class BodyForm(object):
    """Class representing the body of a linear/bilinear form."""
    def __init__(self, **kwargs):

        super(BodyForm, self).__init__()


class SimpleBodyForm(BodyForm):
    """Class representing the body of a simple linear/bilinear form."""
    def __init__(self, **kwargs):

        self.domain     = kwargs.pop('domain')
        self.expression = kwargs.pop('expression')

        super(SimpleBodyForm, self).__init__()


class ExpressionElement(object):
    """Class representing an element of an expression."""
    def __init__(self, **kwargs):

        # textX will pass in parent attribute used for parent-child
        # relationships. We can use it if we want to.
        self.parent = kwargs.get('parent', None)

        # We have 'op' attribute in all grammar rules
        self.op = kwargs['op']

        super(ExpressionElement, self).__init__()


class FactorSigned(ExpressionElement):
    """Class representing a signed factor."""
    def __init__(self, **kwargs):
        self.sign = kwargs.pop('sign', '+')
        super(FactorSigned, self).__init__(**kwargs)

    @property
    def expr(self):
#        print "> FactorSigned "
        expr = self.op.expr
        return -expr if self.sign == '-' else expr

class FactorUnary(ExpressionElement):
    """Class representing a unary factor."""
    def __init__(self, **kwargs):
        # name of the unary operator
        self.name = kwargs['name']

        super(FactorUnary, self).__init__(**kwargs)

    @property
    def expr(self):
#        print "> FactorUnary "
        expr = self.op.expr
        # TODO gets dim from Domain
        dim = 2

        try:
            if isinstance(namespace[str(expr)], Field):
                if self.name in operators["1"]:
                    settings["n_deriv_fields"] = max(settings["n_deriv_fields"], 1)
                elif self.name in operators["2"]:
                    settings["n_deriv_fields"] = max(settings["n_deriv_fields"], 2)
        except:
            if self.name in operators["1"]:
                settings["n_deriv"] = max(settings["n_deriv"], 1)
            elif self.name in operators["2"]:
                settings["n_deriv"] = max(settings["n_deriv"], 2)

        if self.name == "dx":
            return d_var(expr, 'x')
        elif self.name == "dy":
            return d_var(expr, 'y')
        elif self.name == "dz":
            return d_var(expr, 'z')
        elif self.name == "dxx":
            return d_var(expr, 'xx')
        elif self.name == "dyy":
            return d_var(expr, 'yy')
        elif self.name == "dzz":
            return d_var(expr, 'zz')
        elif self.name == "dxy":
            return d_var(expr, 'xy')
        elif self.name == "dyz":
            return d_var(expr, 'yz')
        elif self.name == "dxz":
            return d_var(expr, 'xz')
        elif self.name == "grad":
            return grad(expr, dim=dim)
        else:
            raise Exception('Unknown variable "{}" at position {}'
                            .format(op, self._tx_position))

class FactorBinary(ExpressionElement):
    def __init__(self, **kwargs):
        # name of the unary operator
        self.name = kwargs['name']

        super(FactorBinary, self).__init__(**kwargs)

    @property
    def expr(self):
#        print "> FactorBinary "
#        print self.op

        expr_l = self.op[0].expr
        expr_r = self.op[1].expr

        if self.name == "dot":
            return dot(expr_l, expr_r)
        elif self.name == "inner":
            return inner(expr_l, expr_r)
        elif self.name == "outer":
            return outer(expr_l, expr_r)
        elif self.name == "cross":
            return cross(expr_l, expr_r)
        else:
            raise Exception('Unknown variable "{}" at position {}'
                            .format(op, self._tx_position))


class Term(ExpressionElement):
    @property
    def expr(self):
#        print "> Term "
        ret = self.op[0].expr
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == '*':
                ret *= sympify(operand.expr)
            else:
                ret /= sympify(operand.expr)
        return ret


class Expression(ExpressionElement):
    @property
    def expr(self):
#        print "> Expression "
        ret = self.op[0].expr
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == '+':
                ret += sympify(operand.expr)
            else:
                ret -= sympify(operand.expr)
        return ret


class Operand(ExpressionElement):
    @property
    def expr(self):
#        print "> Operand "
        op = self.op[0]
        if type(op) in {int, float}:
            return op
        elif isinstance(op, ExpressionElement):
            return op.expr
        elif op in namespace:
            if type(namespace[op]) in [Field, Function, Real]:
                return namespace[op].expr
            else:
                return namespace[op]
        elif op in stack:
#            print ">>> found local variables: " + op
            return Symbol(op)
        else:
            raise Exception('Unknown variable "{}" at position {}'
                            .format(op, self._tx_position))


class ExpressionBodyForm(ExpressionElement):
    @property
    def expr(self):
#        print "> ExpressionBodyForm "
        ret = self.op[0].expr
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation in ['+', '-']:
                ret += operation + ' ' + operand.expr
            else:
                raise Exception('Unknown operation "{}" at position {}'
                                .format(operation, self._tx_position))
        return ret


class TermForm(ExpressionElement):
    @property
    def expr(self):
#        print "> TermForm "
        ret = self.op[0].expr
        for operation, operand in zip(self.op[1::2], self.op[2::2]):
            if operation == '*':
                ret += '*' + ' ' + operand.expr
            else:
                raise Exception('Unknown operation "{}" at position {}'
                                .format(operation, self._tx_position))
        return ret


class CallForm(ExpressionBodyForm):
    """Class representing the call to a linear/bilinear form."""
    def __init__(self, **kwargs):

        self.name = kwargs.pop('name')
        self.args = kwargs.pop('args')

#        super(ExpressionBodyForm, self).__init__()

    @property
    def expr(self):
#        print "> CallForm"
        if self.name in namespace:
            b  = namespace[stack["parent"]]

            if isinstance(b, LinearForm):
                if len(self.args) != 1:
                    raise Exception('Expecting exactly one argument at position {}.'
                                    .format(self._tx_position))

                i_row = b.args.functions.index(self.args[0])
                bi = namespace[self.name]
                b.blocks[i_row] = bi
            elif isinstance(b, BilinearForm):
                if len(self.args) != 2:
                    raise Exception('Expecting exactly two argument at position {}.'
                                    .format(self._tx_position))

                i_row = b.args_test.functions.index(self.args[0])
                i_col = b.args_trial.functions.index(self.args[1])
                bi = namespace[self.name]
                b.blocks[i_row, i_col] = bi
            else:
                raise ValueError("Expecting a Linear or Bilinear form.")

        return self.name

