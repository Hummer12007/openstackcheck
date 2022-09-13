import sys
import inspect
import traceback as tb
from functools import wraps
from contextlib import _GeneratorContextManager

from openstackcheck.util.error_ctx import log_error, ErrorType

class _SuppressGCM(_GeneratorContextManager):
    def __enter__(self):
        return super().__enter__()
    """Helper for exception-catching @contextmanager decorator."""
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

def context(func):
    """@contextmanager decorator replacement which ignores exceptions in cleanup.
    """
    @wraps(func)
    def _osc_context_helper(*args, **kwargs):
        return _SuppressGCM(func, args, kwargs)
    return _osc_context_helper

def resource(func):
    """token decorator for stack frame marking.
    """
    @wraps(func)
    def _osc_resource_helper(*args, **kwargs):
        return func(*args, **kwargs)
    return _osc_resource_helper

def test(func):
    """token decorator for stack frame marking.
    """
    @wraps(func)
    def _osc_test_helper(*args, **kwargs):
        return func(*args, **kwargs)
    return _osc_test_helper
