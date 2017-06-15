# coding: utf-8

import os
from vale.codegen import ValeCodegen
from vale.parser  import (ValeParser, ast_to_dict)
from vale.syntax  import (LinearForm, BilinearForm, \
                          Domain, Space, Field, Function, Real)
from vale.utilities import replace_symbol_derivatives, replace_function_with_args


DEBUG = False
#DEBUG = True

__all__ = ["construct_model"]

# ...
_available_backends = []
# ...

# ...
try:
    from clapp.disco.space               import Space     as ClappSpace
    from clapp.disco.field               import Field     as ClappField
    from clapp.plaf.matrix               import Matrix    as ClappMatrix
    from clapp.fema.assembler            import Assembler as ClappAssembler
    from clapp.plaf.vector               import Vector    as ClappVector
    from clapp.vale.expressions.function import Function  as ClappFunction

    _available_backends.append("clapp")
except:
    pass
# ...

# ...
def construct_glt_expression(form):
    """Constructs the glt expression to be used for glt_symbol from a bilinear
    form.

    form: BilinearForm
        a bilinear form from the AST.
    """
    _expr = form.to_sympy()
    for f in form.args_test.functions:
        _expr = replace_symbol_derivatives(_expr, f, "Ni")

    for f in form.args_trial.functions:
        _expr = replace_symbol_derivatives(_expr, f, "Nj")

    dim   = form.attributs["dim"]

    # update calls to functions
    user_functions = form.attributs["user_functions"]
    for f_name in user_functions:
        args = ["x", "y", "z"][:dim]
        _expr = replace_function_with_args(_expr, f_name, args)

    # list of fields
    user_fields = form.attributs["user_fields"]
    for f_name in user_fields:
        _expr = _expr.subs(Symbol(f_name), Symbol(f_name+"_0"))

    return _expr
# ...

# ...
class ClappFormulation(object):
    """
    A generic class for Bilinear and Linear forms, which can be considered as a
    container.
    """
    def __init__(self, \
                 matrix=None, \
                 vector=None, \
                 assembler=None, \
                 functions=None, \
                 expr=None, \
                 glt_expr=None):
        """
        Creates a Bilinear or Linear Formulation

        matrix: clapp.plaf.matrix.Matrix
          a plaf matrix if a bilinear form

        vector: clapp.plaf.vector.Vector
          a plaf vector if a linear form

        assembler: clapp.fema.assembler.Assembler
          fema assembler object

        functions: dict
            a dictionary containing the functions used in the formulation

        expr: sympy.Expression
            expression of the linear/bilinear form

        glt_expr: sympy.Expression
            pretty expression of the bilinear form for glt computation

        """

        self._matrix    = matrix
        self._vector    = vector
        self._assembler = assembler
        self._functions = functions
        self._expr      = expr
        self._glt_expr  = glt_expr

    @property
    def matrix(self):
        """
        Returns the matrix if bilinear form
        """
        return self._matrix

    @property
    def vector(self):
        """
        Returns the vector if linear form
        """
        return self._vector

    @property
    def assembler(self):
        """
        Returns the assembler object
        """
        return self._assembler

    @property
    def functions(self):
        """
        Returns the functions dictionary
        """
        return self._functions

    @property
    def expr(self):
        """
        Returns the expression of the linear/bilinear form
        """
        return self._expr

    @property
    def glt_expr(self):
        """
        Returns the glt expression of the bilinear form, same as expr but we
        apply some pretty printing.
        """
        return self._glt_expr
# ...

# ...
class ClappAST(object):
    """
    A Class representing the Annotated Abstract Syntax Tree for CLAPP/Django.
    """
    def __new__(cls, ast, **settings):
        """
        Converts the AST to CLAPP Python objects

        context: clapp.fema.context.Context
            a fema context object

        ddm_params: clapp.plaf.parameters.ddm.Ddm
            a plaf ddm parameter object

        mapping: clapp.spl.mapping.Mapping
            a spl mapping object

        verbose: bool
            talk more
        """
        context   = settings["context"]
        mapping   = settings["mapping"]
        directory = settings["directory"]

        try:
            verbose = settings["verbose"]
        except:
            verbose = False

        try:
            ddm_params = settings["ddm_params"]
        except:
            ddm_params = context.ddm_params

        try:
            language = settings["language"]
        except:
            language = "LUA"

        p_dim = mapping.p_dim

        tokens     = ast_to_dict(ast)

        _dict = {}
        for token in ast.declarations:
            if isinstance(token, Domain):
                print ("> No translation for Domain node. TODO")
            elif isinstance(token, Space):
                if token.kind == "union":
                    print ("> Found a union space. Will not be treated.")
                else:
                    X = ClappSpace(context=context,type_space=token.kind)
                    _dict[token.name] = X
            elif isinstance(token, Field):
                X = ClappField(_dict[token.space], name=token.name)
                _dict[token.name] = X
            elif isinstance(token, Function):
                # TODO how to set args
                # TODO use expression of function
                args = ["x", "y", "z"][:p_dim]
                X = ClappFunction(name=token.name, \
                                  expr="x-x", \
                                  args=args)
                _dict[token.name] = X
            elif isinstance(token, LinearForm):
                # ... TODO use constants
#                constants = []
#                for name in token.constants:
#                    constants.append(_dict[name])

                # ...
                fields = []
                for name in token.attributs["user_fields"]:
                    fields.append(_dict[name])
                # ...

                # ...
                functions = {}
                for name in token.attributs["user_functions"]:
                    functions[name] = _dict[name]
                # ...

                # ... TODO block space
                space       = _dict[token.attributs["space"]]
                # ...

                # ... sets n_deriv dict
                n_deriv={"trial":token.n_deriv, \
                         "test":token.n_deriv, \
                         "fields":token.n_deriv_fields}
                # ...

                # ...
                kernel_name = "kernel_" + str(token.name)
                filename    = os.path.join(directory, "kernels.lua")
                # ...

                # ... generates Lua kernel
                #     TODO move parts of this code
                code = ValeCodegen(token).doprint(language)

                # ...
                includes = "setmetatable(_ENV, { __index=math }) " + " \n"
                for name in token.attributs["user_functions"]:
                    txt = "function_" + name
                    includes += txt + " = require '" + txt + "'" + " \n"
                    includes += "setmetatable(_ENV, { __index=" + txt + " })" + " \n"
                # ...

                header = code.split(")")[0] + ")\n"
                body   = code[len(header):]

                new_code = header + includes + body

                # ARA
                if not DEBUG:
                    f = open(filename, "a")
                    f.write(new_code)
                    f.close()
                # ...

                # ... creates the matrix object
                vector = ClappVector(n_blocks=token.n_rows)
                # ...

                # ... create an assembler  from a context
                assembler = ClappAssembler(spaces=[space, space], \
                                           fields=fields, \
                                           vectors=[vector], \
                                           mapping=mapping, \
                                           ddm_parameters=ddm_params, \
                                           n_deriv=n_deriv, \
                                           verbose=verbose)
                # ...

                # ...
                assembler.set_kernel(filename=filename, rhs_name=kernel_name)
                # ...

                # ...
                d = ClappFormulation(vector=vector, \
                                     assembler=assembler, \
                                     expr=token.to_sympy())
                _dict[token.name] = d
                # ...
            elif isinstance(token, BilinearForm):
                # ... TODO use constants
#                constants = []
#                for name in token.constants:
#                    constants.append(_dict[name])

                # ...
                fields = []
                for name in token.attributs["user_fields"]:
                    fields.append(_dict[name])
                # ...

                # ...
                functions = {}
                for name in token.attributs["user_functions"]:
                    functions[name] = _dict[name]
                # ...

                # ... TODO block spaces
                space_test  = _dict[token.attributs["space_test"]]
                space_trial = _dict[token.attributs["space_trial"]]
                # ...

                # ... sets n_deriv dict
                n_deriv={"trial":token.n_deriv, \
                         "test":token.n_deriv, \
                         "fields":token.n_deriv_fields}
                # ...

                # ...
                kernel_name = "kernel_" + str(token.name)
                filename    = os.path.join(directory, "kernels.lua")
                # ...

                # ... generates Lua kernel
                #     TODO move parts of this code
                code = ValeCodegen(token).doprint(language)

                # ...
                includes = "setmetatable(_ENV, { __index=math }) " + " \n"
                for name in token.attributs["user_functions"]:
                    txt = "function_" + name
                    includes += txt + " = require '" + txt + "'" + " \n"
                    includes += "setmetatable(_ENV, { __index=" + txt + " })" + " \n"
                # ...

                header = code.split(")")[0] + ")\n"
                body   = code[len(header):]

                new_code = header + includes + body

                # ARA
                if not DEBUG:
                    f = open(filename, "a")
                    f.write(new_code)
                    f.close()
                # ...

                # ... creates the matrix object
                matrix = ClappMatrix(n_block_rows=token.n_rows, \
                                     n_block_cols=token.n_cols)
                # ...

                # ... create an assembler  from a context
                assembler = ClappAssembler(spaces=[space_test, space_trial], \
                                           fields=fields, \
                                           matrices=[matrix], \
                                           mapping=mapping, \
                                           ddm_parameters=ddm_params, \
                                           n_deriv=n_deriv, \
                                           verbose=verbose)
                # ...

                # ...
                if (filename is not None) and (kernel_name is not None):
                    assembler.set_kernel(filename=filename, \
                                         matrix_name=kernel_name)
                # ...

                # ...
                d = ClappFormulation(matrix=matrix, \
                                     assembler=assembler, \
                                     functions=functions, \
                                     expr=token.to_sympy(), \
                                     glt_expr=construct_glt_expression(token))
                _dict[token.name] = d
                # ...
            elif isinstance(token, Real):
                print ("> No translation for Real node. TODO")


#            if type(token) is Number:
#                # TODO gets value from the pde file
#                from sympy.printing.codeprinter      import Assignment
#                from sympy import Symbol
#
#                _dict[token.name] = Assignment(Symbol(token.name), 0.0)
        return _dict
# ...


# user friendly backend
def construct_model(ast_or_filename, backend="clapp", **settings):
    """Generates a Model for a given backend and a programming Language.

    A backend describes a library. For the moment, only clapp is used as
    backend, but we can easily add fenics for example.

    ast_or_filename: list or str
        either a filename that contains Vale instructions or an AST.

    backend: str
        Target library to deal with and assemble our weak formulations.

    directory: str
        working directory to save temporary files. When using Clapp as a
        backend, a directory .clapp will be created in the working directory.
    """
    if not isinstance(ast_or_filename, (list, str)):
        raise ValueError("Either ast or filename must be provided.")

    if backend in _available_backends:
        if isinstance(ast_or_filename, str):
            filename = ast_or_filename

            # ... creates an instance of Vale parser
            vale = ValeParser()
            # ...

            # ... parse the Vale code
            ast = vale.parse_from_file(filename)
            # ...
        else:
            ast = ast_or_filename

        # ...
        folder = "." + str(backend)
        # ARA
        if not DEBUG:
            if not os.path.exists(folder):
                os.makedirs(folder)

            for the_file in os.listdir(folder):
                file_path = os.path.join(folder, the_file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(e)

        settings["directory"] = folder
        # ...

        if backend.lower() == "clapp":
            return ClappAST(ast, **settings)
    else:
        raise ValueError("Only %s backends are available." % _available_backends)
