"""The decorator module."""
from functools import wraps
import typing

import typing_extensions


from .sync import Hooks

_P = typing_extensions.ParamSpec("_P")
_R_co = typing.TypeVar("_R_co", covariant=True)


def hooks(func: typing.Callable[_P, _R_co]) -> Hooks[_P, _R_co]:
    """Decorate a function to have hoks.

    Args:
        func (typing.Callable[_P, _R_co]): The function to decorate

    Raises:
        ValueError: If the provided function is not callable

    Returns:
        Hooks[_P, _R_co]: A callable object with some decorators to provide hooks
    """
    if not callable(func):
        raise ValueError("Provided function is not callable.")

    return wraps(func)(Hooks(func))
    # return
