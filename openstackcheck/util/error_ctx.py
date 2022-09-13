import sys
import traceback

from enum import Enum
from dataclasses import dataclass

from openstackcheck.resources import ctx

class ErrorType(Enum):
    SETUP = 'Setup'
    TEST = 'Test'
    CLEANUP = 'Cleanup'

@dataclass
class ErrorInfo:
    error_type: ErrorType
    exception: Exception
    resource: str
    traceback: str

error_stack = []

# not 100% correct, but works for our usecase
def get_caller(frame):
    caller_method = frame.f_code.co_name
    caller_class = frame.f_locals.get('__class__', None)
    if not caller_class:
        arglist = list(frame.f_code.co_varnames)
        if not arglist:
            return None, caller_method
        caller_self = frame.f_locals.get(arglist[0])
        if not caller_self:
            return None, caller_method
        caller_class = type(caller_self)
    return caller_class, caller_method

_get_self = lambda frame: frame.f_locals[frame.f_code.co_varnames[0]]

def get_error_info(error_type=None):
    _, exc_val, tb = sys.exc_info()
    frames = list(traceback.walk_tb(tb))
    target = -1
    inferred_error = None
    description = None
    for i, frame in enumerate(frames):
        caller_class, caller_method = get_caller(frame[0])
        if caller_class == ctx._SuppressGCM and caller_method == '__enter__':
            target = i + 2
            inferred_error = ErrorType.SETUP
            description = getattr(_get_self(frame[0]), 'description', None)
        elif caller_class == ctx._SuppressGCM and caller_method == '__exit__':
            target = i + 1
            inferred_error = ErrorType.CLEANUP
            description = getattr(_get_self(frame[0]), 'description', None)
        elif caller_method == '_osc_resource_helper':
            inferred_error = ErrorType.SETUP
            description = frame[0].f_locals.get('description', None)
        elif caller_method == '_osc_test_helper':
            target = i + 1
            inferred_error = ErrorType.TEST
            description = frame[0].f_locals.get('description', None)
    error_type = error_type or inferred_error or ErrorType.SETUP
    if target >= len(frames):
        target = -1

    frame = frames[target]

    caller = frame[0].f_code.co_name
    if description:
        caller = f'{caller} ({description})'

    return ErrorInfo(error_type, exc_val, caller, traceback.format_exc())

def log_error(error_type=None):
    error_stack.append(get_error_info(error_type))
