from functools import wraps
from contextlib import _GeneratorContextManager

from openstackcheck.util.error_ctx import log_error, ErrorType

class _SuppressGCM(_GeneratorContextManager):
    """Helper for exception-catching @contextmanager decorator."""
    def __init__(self, description, func, args, kwargs):
        super().__init__(func, args, kwargs)
        self.description = description
    def __enter__(self):
        return super().__enter__()
    def __exit__(self, typ, value, traceback):
        try:
            next(self.gen)
        except StopIteration:
            return False
        except:
            print('An error occured during cleanup')
            log_error(ErrorType.CLEANUP)
        else:
            raise RuntimeError("generator didn't stop")

def context(description=None):
    def context_decorator(func):
        """@contextmanager decorator replacement which ignores exceptions in cleanup.
        """
        @wraps(func)
        def _osc_context_helper(*args, **kwargs):
            nonlocal description # explicitely capture into the closure
            return _SuppressGCM(description, func, args, kwargs)
        return _osc_context_helper
    return context_decorator

def resource(description=None):
    """token decorator for stack frame marking.
    """
    def resource_decorator(func):
        @wraps(func)
        def _osc_resource_helper(*args, **kwargs):
            nonlocal description # explicitely capture into the closure
            return func(*args, **kwargs)
        return _osc_resource_helper
    return resource_decorator

def test(description=None):
    """token decorator for stack frame marking.
    """
    def test_decorator(func):
        @wraps(func)
        def _osc_test_helper(*args, **kwargs):
            nonlocal description # explicitely capture into the closure
            return func(*args, **kwargs)
        return _osc_test_helper
    return test_decorator
