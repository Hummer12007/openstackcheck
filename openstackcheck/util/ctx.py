import sys
import traceback
from enum import Enum
from dataclasses import dataclass

_resource_context = []
error_stack = []

class ContextType(Enum):
    SETUP = 'Setup'
    TEST = 'Test'
    CLEANUP = 'Cleanup'
    UNKNOWN = 'Unknown'

class HandledException(Exception):
    def __init__(self, inner):
        self.inner = inner

@dataclass
class Context:
    type: ContextType
    resource: str
    description: str
    def __enter__(self):
        _resource_context.append(self)
    def __exit__(self, typ, value, tb):
        popped = _resource_context.pop()
        assert self == popped
    def to_error(self):
        _, exc_val, __ = sys.exc_info()
        if isinstance(exc_val.__context__, HandledException):
            exc_val.__suppress_context__ = True
        return ErrorInfo(self, exc_val, traceback.format_exc())

@dataclass
class ErrorInfo:
    context: Context
    exception: Exception
    traceback: str

def get_error_info(context_type=ContextType.UNKNOWN):
    _, exc_val, tb = sys.exc_info()
    frames = list(traceback.walk_tb(tb))
    frame = frames[-1]

    context = Context(context_type, frame[0].f_code.co_name, None)

    return ErrorInfo(context, exc_val, traceback.format_exc())

def log_error(context_type=None):
    if _resource_context:
        ctx = _resource_context[-1]
        error_stack.append(ctx.to_error())
        print(f'{ctx.type.value} error occured for {ctx.resource} ({ctx.description})')
    else:
        ctx_type = context_type or ContextType.UNKNOWN
        error_info = get_error_info(context_type)
        error_stack.append(error_info)
        print(f'{ctx_type.value} error occured for {error_info.context.resource}')
    print(traceback.format_exc())
