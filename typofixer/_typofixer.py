import builtins
import difflib
import inspect
import pkgutil
import sys

_base_import = builtins.__import__
_module_names = [m.name for m in pkgutil.iter_modules()]


def enable():
    builtins.__import__ = _import


def _import(name, globals=None, locals=None, fromlist=(), level=0):
    matches = difflib.get_close_matches(name, _module_names, n=1, cutoff=0)
    if not matches:
        return
    module = _base_import(matches[0], globals, locals, fromlist, level)
    wrapper = Wrapper(module)
    sys.modules[name] = wrapper
    return wrapper


class Wrapper:

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, item):
        member_names = [k for k, v in inspect.getmembers(self.obj)]
        matches = difflib.get_close_matches(item, member_names, n=1, cutoff=0)
        if not matches:
            raise AttributeError()
        return Wrapper(getattr(self.obj, matches[0]))

    def __call__(self, *args, **kwargs):
        result = self.obj.__call__(*args, **kwargs)
        return Wrapper(result) if result is not None else None

    def __str__(self):
        return str(self.obj)

    def __iter__(self):
        return Wrapper(iter(self.obj))

    def __next__(self):
        return Wrapper(next(self.obj))

    def __getitem__(self, item):
        return Wrapper(self.obj[item])

    def __eq__(self, other):
        return self.obj == (other.obj if isinstance(other, Wrapper) else other)


def wrap(obj):
    return Wrapper(obj)
