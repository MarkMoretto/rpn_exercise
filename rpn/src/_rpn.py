#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    "Rpn",
    ]

import re
import math
import inspect

from _types import FloatList, Num
from _exceptions import ValueCountError


class OperatorsMixin:
    """Operators mixin.
    
    Class handles some of the mundane tasks related to 
    simple math expressions.
    """

    CAPTURE_FUNC_REGEX: str = r"(?:.+:)\s*(.+),"

    # Operations with two parameters.
    OPERATIONS = {
        "+": lambda a, b: math.fsum([a, b]),
        "-": lambda a, b: b - a,
        "*": lambda a, b: b * a,
        "/": lambda a, b: b / a if a != 0 else math.inf, # Zero-division
        "^": lambda a, b: math.pow(b, a),
        "log": lambda n, base: math.log(n, base),
    }

    # Infrequent operations with single parameter.
    OPERATIONS_EXT = {
        "sin": lambda n: math.sin(n),
        "cos": lambda n: math.cos(n),
        "tanh": lambda n: math.tan(n),            
        "acos": lambda n: math.acos(n),
        "e": lambda n: math.exp(n),
    }

    def __init__(self) -> None:
        # Update OPERATIONS dict with extended operations.
        self.OPERATIONS.update(**self.OPERATIONS_EXT)        
        self.NUMBERS = None
        self.OPERATORS = None
        self.__update_ops()

    def __update_ops(self) -> None:
        """Update OPERATORS data set with the numeric values 0 - 9.
        """
        self.NUMBERS = set(map(str, range(0, 10)))
        self.OPERATORS = set(self.OPERATIONS.keys())
        self.OPERATORS.update(self.NUMBERS)

    def add_func(self, function_name, function_object) -> None:
        """Add new function to OPERATIONS."""
        if not function_name in self.OPERATIONS:
            self.OPERATIONS[function_name] = function_object
            self.__update_ops()

    def remove_func(self, function_name) -> None:
        """Delete item from OPERATIONS collection by key."""
        try:
            del self.OPERATIONS[function_name]
            self.__update_ops()
        except ValueError:
            pass

    def descriptions(self):
        self.__update_ops()
        print("Alias\tArgs\t\tFunction")
        for k, fn in self.OPERATIONS.items():
            _sig = inspect.signature(fn)
            _fn = inspect.getsource(fn).strip().split(":")[2].strip()
            print(f"{k}\t{_sig}\t\t{_fn}")




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
