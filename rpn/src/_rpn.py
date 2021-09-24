#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    "Expression",
    "Rpn",
    ]

import re
import heapq
import inspect
from collections import deque

import math
import statistics

from ._types import FloatList, FuncReturnNum, IntList, List, Num, TupIntHomo, TupStrHomo
from ._exceptions import ValueCountError


class Expression:
    """Expression class. Handles single mathematical expression.
    
    Parameters
    ----------
    alias_or_name : str
        Math operator or alias of expression to create.
    cb_function : FuncReturnNum
        Callback function, or main expression to create.
    """
    def __init__(self, alias_or_name: str, cb_function: FuncReturnNum = None):
        if len(alias_or_name) > 0:
            self.alias = alias_or_name
        else:
            raise ValueError("Alias or name needs to be at least one character long.")

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
        self.description_cols = "Oper", "Args", "Function"
        self.OPERATIONS.extend(self.OPERATIONS_EXT)

    def __update_ops(self):
        self.OPERATIONS.extend(self.OPERATIONS_EXT)

    @property
    def operators(self):
        return set([o.alias for o in self.OPERATIONS])

    def del_nth(self, n):
        """Use `deque` library to remove item
        from OPERATIONS list by the item's index.
        """
        ops = self.OPERATIONS
        d = deque(ops)
        d.rotate(-n)
        d.popleft()
        d.rotate(n)
        self.OPERATIONS = list(d)

    def operation_index(self, lookup_value: str) -> int:
        """Return index related to lookup_value, which should be 
        an operator "sign" or alias.
        """
        _tmp  = (i for i, o in enumerate(self.OPERATIONS) if o.alias == lookup_value)
        return next(_tmp, -1)

    def add_expression(self, sig: str, fn: str) -> None:
        """Add new function to OPERATIONS.
        """
        e = Expression(sig, fn)
        if not e.alias in self.operators:
            self.OPERATIONS.append(e)
            self.set_length_data()

    def remove_expression(self, operator_alias: str) -> None:
        """Delete item from OPERATIONS collection by key.
        """
        _idx = self.operation_index(operator_alias)
        if _idx > -1:
            self.del_nth(_idx)

    def get_function(self, alias: str):
        _idx = self.operation_index(alias)
        if _idx > -1:
            return 

    def set_length_data(self, _padding = 1.5):
        """Calculate padding amount for description columns.

        Parameters
        ----------
        _padding : float
            Amount of padding for each column.  Can be whole number or decimal.
            Values at or over 100 will be reduced to decimal.

        Returns
        -------
        IntList
            List of integer values representing text padding for each column.
        """
        _max_len_list = [0] * 3

        for e in self.OPERATIONS:
            for i, length in enumerate(e.lengths):
                if length > _max_len_list[i]:
                    _max_len_list[i] = length

        # Consider if column heading is wider than the max
        # width for a given column.
        for i, c in enumerate(self.description_cols):
            if len(c) > _max_len_list[i]:
                _max_len_list[i] = len(c)
            
        # Add padding to columns.
        p = self.__norm_padding(_padding)
        return [int(n * p) for n in _max_len_list]
        
    
    def __norm_padding(self, p) -> float:
        """Standardize padding to value between 0 and 100"""
        return p if p < 100 else p / 100

    def descriptions(self, padding = 1.5):
        """Print out basic table of operators, signatures, and expressions.
        
        Parameters
        ----------
        padding : float
            Amount to pad columns by.  If 
        """
        max_len_list = self.set_length_data(padding)

        _msg = []
        _submsg = "".join([f"{c:<{l}}" for c, l in zip(self.description_cols, max_len_list)])
        _msg.append(_submsg)
        _msg.append("-" * sum(max_len_list))

        for expr in self.OPERATIONS:
            _submsg = "".join([f"{e:<{L}}" for e, L in zip(expr.values, max_len_list)])
            _msg.append(_submsg)

        # Little room for easier reading on prompt.
        _msg.insert(0, "")
        _msg.append("")

        print("\n".join(_msg))



class Rpn(OperatorsMixin):
    """Main Reverse Polish Notation (RPN) class.
    """
    def __init__(self) -> None:
        super().__init__()
        self.stacker = []
        self.current_char = None

    @staticmethod
    def is_int(obj: str) -> bool:
        """Return True if value is int data type;
        False otherwise.
        """
        if isinstance(obj, str):
            return float(obj).is_integer()
        raise ValueError("Integer or float numberic string value expected.")

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

            if self.is_int(f"{_result}"):
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
        _idx = self.operation_index(new_char)

        # Character found in valid operator set.
        if new_char in self.operators:
            if len(self.stacker) > 1:
                # Expressions with two parameters.
                self.stacker.append(self.OPERATIONS[_idx].function(self.stacker.pop(), self.stacker.pop()))

            # If there is only one value in the stack.
            elif len(self.stacker) == 1:
                # See if new_char in single-arg operations collection and run.
                if new_char in self.OPERATIONS_EXT:
                    self.stacker.append(self.OPERATIONS[_idx].function(self.stacker.pop()))
                else:
                    # If the selected next operator requires 
                    raise ValueCountError("Operation requires at least one numeric value.")

            else:
                # If new_char is an operator, but there are not enough values
                # to execute the expression, then raise an error.
                raise ValueCountError("Not enough values to perform operation.")

        elif new_char in self.NUMBERS:
            self.stacker.append(float(new_char))
        
        else:
            # If a non-numeric or non-valid operator are passed, raise error.
            raise ValueError("Values must be valid number or operator.")


if __name__ == "__main__":
    import doctest
    doctest.testmod()
