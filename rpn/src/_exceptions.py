#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__all__ = [
    "ValueCountError",
    "MissingArgumentError",
]


class RPNException(Exception):
    ...

class ValueCountError(RPNException):
    ...

class MissingArgumentError(RPNException):
    ...
