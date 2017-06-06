# coding: utf-8

import os
from sympy import Symbol, sympify

from symcc.dsl.vale.utilities import grad, d_var, inner, outer, cross, dot
from symcc.dsl.vale.syntax import (Vale, \
                                   Expression, Term, Operand, \
                                   FactorSigned, FactorUnary, FactorBinary, \
                                   LinearForm, BilinearForm, \
                                   Domain, Space, Field, Function, Real)

from textx.metamodel import metamodel_from_str

__all__ = ["ValeParser", "ast_to_dict"]

# ...
def _get_by_name(ast, name):
    """
    Returns an object from the AST by giving its name.
    """
    for token in ast.declarations:
        if token.name == name:
            return token
    return None
# ...

# ...
def ast_to_dict(ast):
    """
    Returns an object from the AST by giving its name.
    """
    tokens = {}
    for token in ast.declarations:
        tokens[token.name] = token
    return tokens
# ...

class Parser(object):
    """ Class for a Parser using TextX.

    A parser can be created from a grammar (str) or a filename. It is preferable
    to specify the list classes to have more control over the abstract grammar;
    for example, to use a namespace, and to do some specific anotation.

    >>> parser = Parser(filename="gammar.tx")

    Once the parser is created, you can parse a given set of instructions by
    calling

    >>> parser.parse(["Field(V) :: u"])

    or by providing a file to parse

    >>> parser.parse_from_file("tests/inputs/1d/poisson.vl")
    """
    def __init__(self, grammar=None, filename=None, \
                 classes=None):
        """Parser constructor.

        grammar : str
            abstract grammar describing the DSL.

        filename: str
            name of the file containing the abstract grammar.

        classes : list
            a list of Python classes to be used to describe the grammar. Take a
            look at TextX documentation for more details.
        """

        _grammar = grammar

        # ... read the grammar from a file
        if not (filename is None):
            dir_path = os.path.dirname(os.path.realpath(__file__))
            filename = os.path.join(dir_path, filename)

            f = open(filename)
            _grammar = f.read()
            _grammar.replace("\n", "")
            f.close()
        # ...

        # ...
        self.grammar = _grammar
        # ...

        # ...
        if classes is None:
            self.model = metamodel_from_str(_grammar)
        else:
            self.model = metamodel_from_str(_grammar, classes=classes)
        # ...

    def parse(self, instructions):
        """Parse a set of instructions with respect to the grammar.

        instructions: list
            list of instructions to parse.
        """
        # ... parse the DSL code
        return self.model.model_from_str(instructions)
        # ...

    def parse_from_file(self, filename):
        """Parse a set of instructions with respect to the grammar.

        filename: str
            a file containing the instructions to parse.
        """
        # ... read a DSL code
        f = open(filename)
        instructions = f.read()
        instructions.replace("\n", "")
        f.close()
        # ...

        # ... parse the DSL code
        return self.parse(instructions)
        # ...

# User friendly parser

class ValeParser(Parser):
    def __init__(self, filename=None):
        classes = [Vale, \
                   Expression, Term, Operand, \
                   FactorSigned, FactorUnary, FactorBinary, \
                   LinearForm, BilinearForm, \
                   Domain, Space, Field, Function, Real \
                   ]

        if filename is None:
            filename = "grammar.tx"

        super(ValeParser, self).__init__(filename = filename, \
                                         classes=classes)

    def parse_from_file(self, filename):
        ast = super(ValeParser, self).parse_from_file(filename)

        # ... annotating the AST
        for token in ast.declarations:
            if isinstance(token, LinearForm):
                user_fields    = []
                user_functions = []
                user_constants = []

                space  = _get_by_name(ast, token.args.space)
                domain = _get_by_name(ast, space.domain)

                expr = token.to_sympy()
                free_symbols = expr.free_symbols
                for symbol in free_symbols:
                    var = _get_by_name(ast, str(symbol))
                    if isinstance(var, Field):
                        user_fields.append(var.name)
                    elif isinstance(var, Function):
                        user_functions.append(var.name)
                    elif isinstance(var, Real):
                        user_constants.append(var.name)

                token.set("dim", domain.dim)
                token.set("user_fields", user_fields)
                token.set("user_functions", user_functions)
                token.set("user_constants", user_constants)

            elif isinstance(token, BilinearForm):
                user_fields    = []
                user_functions = []
                user_constants = []

                space_test  = _get_by_name(ast, token.args_test.space)
                space_trial = _get_by_name(ast, token.args_trial.space)
                domain      = _get_by_name(ast, space_test.domain)

                expr = token.to_sympy()
                free_symbols = expr.free_symbols
                for symbol in free_symbols:
                    var = _get_by_name(ast, str(symbol))
                    if isinstance(var, Field):
                        user_fields.append(var.name)
                    elif isinstance(var, Function):
                        user_functions.append(var.name)
                    elif isinstance(var, Real):
                        user_constants.append(var.name)

                token.set("dim", domain.dim)
                token.set("user_fields", user_fields)
                token.set("user_functions", user_functions)
                token.set("user_constants", user_constants)
        # ...

        return ast
