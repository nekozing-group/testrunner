from RestrictedPython import safe_builtins
from RestrictedPython import Eval, Guards, PrintCollector

allowed = {}

valid_inplace_types = (list, set)
inplace_slots = {
    "+=": "__iadd__",
    "-=": "__isub__",
    "*=": "__imul__",
    "/=": (1 / 2 == 0) and "__idiv__" or "__itruediv__",
    "//=": "__ifloordiv__",
    "%=": "__imod__",
    "**=": "__ipow__",
    "<<=": "__ilshift__",
    ">>=": "__irshift__",
    "&=": "__iand__",
    "^=": "__ixor__",
    "|=": "__ior__",
}

def __iadd__(x, y):
    x += y
    return x


def __isub__(x, y):
    x -= y
    return x


def __imul__(x, y):
    x *= y
    return x


def __idiv__(x, y):
    x /= y
    return x


def __ifloordiv__(x, y):
    x //= y
    return x


def __imod__(x, y):
    x %= y
    return x


def __ipow__(x, y):
    x **= y
    return x


def __ilshift__(x, y):
    x <<= y
    return x


def __irshift__(x, y):
    x >>= y
    return x


def __iand__(x, y):
    x &= y
    return x


def __ixor__(x, y):
    x ^= y
    return x


def __ior__(x, y):
    x |= y
    return x

inplace_ops = {
    "+=": __iadd__,
    "-=": __isub__,
    "*=": __imul__,
    "/=": __idiv__,
    "//=": __ifloordiv__,
    "%=": __imod__,
    "**=": __ipow__,
    "<<=": __ilshift__,
    ">>=": __irshift__,
    "&=": __iand__,
    "^=": __ixor__,
    "|=": __ior__,
}

def protected_inplacevar(op, var, expr):
    """Do an inplace operation

    If the var has an inplace slot, then disallow the operation
    unless the var an instance of ``valid_inplace_types``.
    """
    if hasattr(var, inplace_slots[op]) and not isinstance(var, valid_inplace_types):
        try:
            cls = var.__class__
        except AttributeError:
            cls = type(var)
        raise TypeError(
            "Augmented assignment to %s objects is not allowed"
            " in untrusted code" % cls.__name__
        )
    return inplace_ops[op](var, expr)


import uuid

class PrintCollectorSingletonFactory:
    def create_singleton(self):
        instance = PrintCollector()
        
        # rewrite constructor
        def get_instance(self, _getattr_=None):
            instance._getattr_ = _getattr_
            return instance

        return type(f'PrintCollectorSingleton-{str(uuid.uuid4())}', (), {
            'instance': instance,
            'get_instance': get_instance
        })
        

ALLOWED_IMPORTS = frozenset([
    "array",
    "bisect",
    "calendar",
    "collections",
    "datetime",
    "heapq",
    "re",
    "string",
    "time",
    "typing",
    "zoneinfo"
])

def guarded_import(name, *args):
    if name in ALLOWED_IMPORTS:
        return __import__(name, *args)
    else:
       raise ImportError(f"{name} is not an allowed import.")

factory = PrintCollectorSingletonFactory()
singleton = factory.create_singleton()

allowed = {}
allowed['_getitem_'] = Eval.default_guarded_getitem
allowed['_getattr_'] = Eval.default_guarded_getattr
allowed['__metaclass__'] = type
allowed['__name__'] = 'name'
allowed['_getiter_'] = Eval.default_guarded_getiter
allowed['_iter_unpack_sequence_'] = Guards.guarded_iter_unpack_sequence
allowed['_print_'] = singleton.get_instance
allowed['_inplacevar_'] = protected_inplacevar
allowed['__builtins__'] = safe_builtins | {
    '__import__': guarded_import
}
