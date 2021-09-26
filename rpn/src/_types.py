#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module for type hints.

See: https://docs.python.org/3/library/typing.html
"""

from typing import Any, AnyStr, Callable, List, Tuple, TypeVar, Union

# Scalars
Num = Union[int, float]

# Vectors
AnyList = List[Any]
IntList = List[int]
FloatList = List[float]
NumList = List[Num]
StrList = List[str]

# Tuples
TupIntHomo = Tuple[int, ...]
TupStrHomo = Tuple[str, ...]

# Matrices/Grids
AnyMatrix = List[StrList]
AnyGrid = List[StrList]
StrMatrix = List[StrList]
StrGrid = List[StrList]
NumMatrix = List[NumList]
NumGrid = List[NumList]

# Callables
FuncReturnNum = Callable[..., Num]
