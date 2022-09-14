from functools import wraps
from contextlib import _GeneratorContextManager

from openstackcheck.util.ctx import Context, ContextType, log_error, HandledException

class _SuppressGCM(_GeneratorContextManager):
    """Helper for exception-catching @contextmanager decorator."""
    def __init__(self, description, func, args, kwargs):
        super().__init__(func, args, kwargs)
        self.original_func = func
        self.description = description
    def __enter__(self):
        with Context(ContextType.SETUP, f'{self.original_func.__module__}.{self.original_func.__name__}', self.description):
            try:
                return super().__enter__()
            except HandledException:
                raise
            except Exception as e:
                log_error()
                raise HandledException(e) from e
    def __exit__(self, typ, value, traceback):
        with Context(ContextType.CLEANUP, f'{self.original_func.__module__}.{self.original_func.__name__}', self.description):
            try:
                next(self.gen)
            except StopIteration:
                return False
            except HandledException:
                return True
            except:
                log_error()
                return True
            else:
                raise RuntimeError("generator didn't stop")
        if typ:
            return True

def context(description=None):
    def context_decorator(func):
        """@contextmanager decorator replacement which ignores exceptions in cleanup.
        """
        @wraps(func)
        def _osc_context_helper(*args, **kwargs):
            return _SuppressGCM(description, func, args, kwargs)
        return _osc_context_helper
    return context_decorator

def resource(description=None):
    """token decorator for stack frame marking.
    """
    def resource_decorator(func):
        @wraps(func)
        def _osc_resource_helper(*args, **kwargs):
            with Context(ContextType.SETUP, f'{func.__module__}.{func.__name__}', description):
                try:
                    return func(*args, **kwargs)
                except HandledException:
                    raise
                except Exception as e:
                    log_error()
                    raise HandledException(e) from e
        return _osc_resource_helper
    return resource_decorator

def test(description=None):
    """token decorator for stack frame marking.
    """
    def test_decorator(func):
        @wraps(func)
        def _osc_test_helper(*args, **kwargs):
            with Context(ContextType.TEST, f'{func.__module__}.{func.__name__}', description):
                try:
                    return func(*args, **kwargs)
                except HandledException:
                    raise
                except Exception as e:
                    log_error()
                    raise HandledException(e) from e
        return _osc_test_helper
    return test_decorator
