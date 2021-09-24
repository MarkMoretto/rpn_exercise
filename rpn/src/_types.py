#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for type hints.

See: https://docs.python.org/3/library/typing.html
"""

from typing import Callable, List, Tuple, TypeVar, Union

# Scalars
Num = Union[int, float]

# Vectors
IntList = List[int]
FloatList = List[float]
NumList = List[Num]
StrList = List[str]

# Tuples
TupIntHomo = Tuple[int, ...]

# Callables
FuncReturnNum = Callable[..., Num]
