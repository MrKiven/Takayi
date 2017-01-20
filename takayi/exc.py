# -*- coding: utf-8 -*-


class TypeHintsBaseError(Exception):
    pass


class ParseTypeError(TypeHintsBaseError):
    pass


class InvalidHintsError(TypeHintsBaseError):
    pass
