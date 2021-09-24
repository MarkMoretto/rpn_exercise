#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    "Rpn",
    ]

import re
import math
import heapq
import inspect
from collections import deque

from ._types import FloatList, FuncReturnNum, List, Num, TupIntHomo, TupStrHomo
from ._exceptions import ValueCountError

# From ./rpn/
# from src._types import FloatList, FuncReturnNum, List, Num, TupIntHomo
# from src._exceptions import ValueCountError


class Expression:
    """Expression class. Handles single mathematical expression.
    
    Parameters
    ----------
    alias_or_name : str
        Math operator or alias of expression to create.
    cb_function : FuncReturnNum
        Callback function, or main expression to create.
    """
    def __init__(self, alias_or_name: str, cb_function: FuncReturnNum):
        self.alias = alias_or_name
        self.function = cb_function
        self.__set_attrs()

    def __set_lengths(self) -> None:
        """Set length attributes for a given expression instance.
        """
        self.len_alias = len(self.alias)
        self.len_func = len(self.func_string)
        self.len_sig = len(self.signature)        

    def __set_attrs(self) -> None:
        """Process and set attributes for a given expression instance.
        """
        self.signature = str(inspect.signature(self.function))
        self.func_string = self.process_function(self.function)
        self.__set_lengths()

    @staticmethod
    def process_function(fn: FuncReturnNum) -> str:
        """Static method to process function expression.

        Parameters
        ----------
        fn : FuncReturnNum
            Function with numeric return value.
        
        Returns
        -------
        str
            String value of the processed function.
        """
        aa = inspect.getsource(fn).strip()
        _res = re.search(r".+:\s+?(.+)(?=\))", aa, flags = re.I)
        if _res:
            return _res.group(1)
    
    @property
    def lengths(self) -> TupIntHomo:
        """Lengths propery for given Expression instance.

        Parameters
        ----------
        None

        Returns
        -------
        TupIntHomo
            Tuple of homogeneous integer type.
        """
        return self.len_alias, self.len_sig, self.len_func

    @property
    def values(self) -> TupStrHomo:
        """Return key attribute values for given Expression instance.
    
        Parameters
        ----------
        None

        Returns
        -------
        TupStrHomo
            Tuple of homogeneous string type.
        """
        return self.alias, self.signature, self.func_string        

# e = Expression("+", lambda a, b: math.fsum([a, b]))
# e = Expression("/", lambda a, b: b / a if a != 0 else math.inf)
# aa = inspect.getsource(e.function).strip()
# re.search(r".+:\s+?(.+)(?=\))", aa, flags = re.I).group(1)

# inspect.getsource(e.function).strip().split(":")[1].strip()

class OperatorsMixin:
    """Operators mixin.
    
    Class handles some of the mundane tasks related to 
    simple math expressions.
    """

    CAPTURE_FUNC_REGEX: str = r"(?:.+:)\s*(.+),"

    # Operations with two parameters.
    OPERATIONS = [
        Expression("+", lambda a, b: math.fsum([a, b])),
        Expression("-", lambda a, b: b - a),
        Expression("*", lambda a, b: b * a),
        Expression("/", lambda a, b: b / a if a != 0 else math.inf),
        Expression("^", lambda a, b: math.pow(b, a)),     
    ]

    OPERATIONS_EXT = [
        Expression("log", lambda n, base: math.log(n, base)),
        Expression("sin", lambda n: math.sin(n)),
        Expression("cos", lambda n: math.cos(n)),
        Expression("tanh", lambda n: math.tan(n)),
        Expression("acos", lambda n: math.acos(n)),
        Expression("e", lambda n: math.exp(n)),
    ]

    NUMBERS = set(map(str, range(10)))

    def __init__(self) -> None:
        self.description_cols = "Alias", "Args", "Function"
        self.__update_ops()

    def __update_ops(self):
        self.OPERATIONS += self.OPERATIONS_EXT

    @property
    def operators(self):
        return set([o.alias for o in self.OPERATIONS])

    def del_nth(self, n):
        """Use `deque` library to remove item
        from OPERATIONS list by the item's index.
        """
        d = deque(self.OPERATIONS)
        d.rotate(-n)
        d.popleft()
        d.rotate(n)

    def operation_index(self, lookup_value: str) -> int:
        """Return index related to lookup_value, which should be 
        an operator "sign" or alias.
        """
        _tmp  = (i for i, o in enumerate(self.OPERATIONS) if o.alias == lookup_value)
        return next(_tmp, -1)

    def add_expression(self, e: Expression) -> None:
        """Add new function to OPERATIONS.
        """
        if not e.alias in self.operators:
            self.OPERATIONS.append(e)

    def remove_expression(self, operator_alias: str) -> None:
        """Delete item from OPERATIONS collection by key.
        """
        _idx = self.operation_index(operator_alias)
        if _idx > -1:
            self.del_nth(_idx)


    def __update_length_data(self):
        """Set a length map for description output.
        """
        self.max_len_list = [0] * 3

        for e in self.OPERATIONS:
            for i, length in enumerate(e.lengths):
                if length > self.max_len_list[i]:
                    self.max_len_list[i] = length

        # Consider if column heading is wider than the max
        # width for a given column.
        for i, c in enumerate(self.description_cols):
            if len(c) > self.max_len_list[i]:
                self.max_len_list[i] = len(c)
        

    def __pad_lengths(self, p):
        """Calculate padding amount for description columns.
        """
        p = p if p > 1 else p / 100
        self.max_len_list = [int(n * p) for n in self.max_len_list]

    def descriptions(self, padding = 1.5):
        """Print out basic table of operators, signatures, and expressions.
        
        Parameters
        ----------
        padding : float
            Amount to pad columns by.  If 
        """
        self.__update_length_data()
        self.__pad_lengths(padding)
        _msg = []
        _submsg = "".join([f"{c:<{l}}" for c, l in zip(self.description_cols, self.max_len_list)])
        _msg.append(_submsg)

        for expr in self.OPERATIONS:
            _submsg = "".join([f"{e:<{L}}" for e, L in zip(expr.values, self.max_len_list)])
            _msg.append(_submsg)

        print("\n".join(_msg))



class Rpn(OperatorsMixin):
    """Main Reverse Polish Notation (RPN) class.
    """
    def __init__(self) -> None:
        super().__init__()
        self.stacker = []
        self.current_char = None

    @staticmethod
    def is_int(obj: Num) -> bool:
        """Return True if value is int data type;
        False otherwise.
        """
        return float(obj).is_integer()

    @property
    def remove_last(self) -> None:
        """Remove last item added to stack.  Like .pop()
        without all the "return value" hype.
        """
        if len(self.stacker) > 0:
            self.stacker = self.stacker[:-1]
    
    @property
    def reset(self) -> None:
        """Reset stack. AGNB.
        """
        self.stacker = []

    @property
    def status(self) -> FloatList:
        """Return current stack, empty or otherwise.
        """
        return self.stacker
    
    @property
    def result(self) -> Num:
        """Return result of RPN calculation(s).

        Returns
        -------
        Num : (float, int)
            Numeric value
        """
        # Default result
        _result = 0

        # Check if stack contains final value.
        if len(self.stacker) > 0:
            # Set result to final value if True.
            _result = self.stacker[-1]

            if self.is_int(_result):
                _result = int(_result)

        return _result


    def execute_next(self, new_char: str) -> None:
        """Update stack with new numeric value or valid expression execution.
        
        Parameters
        ----------
        new_entry : str
            The next user input character.

        Returns
        -------
        None
        """
        
        # Character found in valid operator set.
        if new_char in self.OPERATIONS:
            if len(self.stacker) > 1:
                # Expressions with two parameters.
                self.stacker.append(self.OPERATIONS[new_char](self.stacker.pop(), self.stacker.pop()))

            elif len(self.stacker) == 1:
                # Expressions with one parameter.
                if new_char in self.OPERATIONS_EXT:
                    self.stacker.append(self.OPERATIONS[new_char](self.stacker.pop()))
    
            else:
                raise ValueCountError("Not enough values to perform operation.")

        elif new_char in self.NUMBERS:
            try:
                self.stacker.append(float(new_char))
            except ValueError:
                print(f"Error trying to convert {new_char}")
