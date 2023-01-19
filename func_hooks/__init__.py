"""Function hooks decorator.

The decorator adds functionality to run code before, after and on function error.

This adds extension points to the decorated function or method.
"""

from .decorator import hooks
from .sync import Hooks
from .typing import Invocation, InvocationError, InvocationResult

__all__ = [
    "Hooks",
    "hooks",
    # Type definitions:
    "Invocation",
    "InvocationError",
    "InvocationResult",
]
