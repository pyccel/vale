# coding: utf-8

import os
from symcc.dsl.vale.codegen import ValeCodegen
from symcc.dsl.vale.parser  import ValeParser
from symcc.dsl.vale.parser  import ast_to_dict
from symcc.dsl.vale.syntax  import (LinearForm, BilinearForm, \
                                    Domain, Space, Field, Function, Real)


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
class ClappFormulation(object):
    """
    A generic class for Bilinear and Linear forms, which can be considered as a
    container.
    """
    def __init__(self, \
                 matrix=None, \
                 vector=None, \
                 assembler=None, \
                 functions=None):
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

        """

        self._matrix     = matrix
        self._vector     = vector
        self._assembler  = assembler
        self._functions  = functions

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
        """
        context   = settings["context"]
        mapping   = settings["mapping"]
        directory = settings["directory"]

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
                f = open(filename, "a")
                f.write(new_code)
                f.close()
                # ...

                # ... creates the matrix object
                #     TODO use n_components from space
                vector = ClappVector(n_blocks=1)
                # ...

                # ... create an assembler  from a context
                #     TODO how to pass verbose?
                assembler = ClappAssembler(spaces=[space, space], \
                                           fields=fields, \
                                           vectors=[vector], \
                                           mapping=mapping, \
                                           ddm_parameters=ddm_params, \
                                           n_deriv=n_deriv, \
                                           verbose=False)
                # ...

                # ...
                assembler.set_kernel(filename=filename, rhs_name=kernel_name)
                # ...

                # ...
                d = ClappFormulation(vector=vector, assembler=assembler)
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
                f = open(filename, "a")
                f.write(new_code)
                f.close()
                # ...

                # ... creates the matrix object
                #     TODO set n_block_rows/cols
                matrix = ClappMatrix(n_block_rows=1, \
                                     n_block_cols=1)
                # ...

                # ... create an assembler  from a context
                #     TODO how to set verbose?
                assembler = ClappAssembler(spaces=[space_test, space_trial], \
                                           fields=fields, \
                                           matrices=[matrix], \
                                           mapping=mapping, \
                                           ddm_parameters=ddm_params, \
                                           n_deriv=n_deriv, \
                                           verbose=True)
                # ...

                # ...
                if (filename is not None) and (kernel_name is not None):
                    assembler.set_kernel(filename=filename, \
                                         matrix_name=kernel_name)
                # ...

                # ...
                d = ClappFormulation(matrix=matrix, \
                                     assembler=assembler, \
                                     functions=functions)
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
