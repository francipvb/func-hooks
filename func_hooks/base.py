"""Base types for hook decorator."""
import abc
import typing

import typing_extensions

from .typing import ErrorFunc, PostFunc, PreFunc

_R = typing.TypeVar("_R")

_F = typing.TypeVar("_F", bound=typing.Callable[..., typing.Any])


class BaseHooks(typing.Generic[_F, _R], abc.ABC):
    """Base hooks decorators functionality.

    Args:
        func: The decorating function.
    """

    def __init__(self) -> None:
        super().__init__()

        self._pre_hooks: typing.Set[PreFunc[_F]] = set()
        self._post_hooks: typing.Set[PostFunc[_F, _R]] = set()
        self._error_hooks: typing.Set[ErrorFunc[_F]] = set()
        self._once_pre_hooks: typing.Set[PreFunc[_F]] = set()
        self._once_post_hooks: typing.Set[PostFunc[_F, _R]] = set()
        self._once_error_hooks: typing.Set[ErrorFunc[_F]] = set()

    def on_before(self, func: PreFunc[_F]) -> PreFunc[_F]:
        """A decorator to add a `before` callback.

        You can use this as a decorator, for example:

            @hooks.on_before
            def _before_func(*args, **kwargs):
                println('Ran before the real function...)

        Parameters:
            func: The function to attach as the callback

        Returns:
            func: The passed function, to be able to use this as a decorator
        """
        self._pre_hooks.add(func)
        return func

    def on_before_once(self, func: PreFunc[_F]) -> PreFunc[_F]:
        """Add a `before` callback to be called once.

        Args:
            func: The callback function

        Returns:
            typing.Callable[_P, None]: The passed callable
        """
        self._once_pre_hooks.add(func)
        return func

    def on_after(self, func: PostFunc[_F, _R]) -> PostFunc[_F, _R]:
        """Add a callback to be called after the function execution.

        Parameters:
            func: The function to call

        Returns:
            The function itself
        """
        self._post_hooks.add(func)
        return func

    def on_after_once(self, func: PostFunc[_F, _R]) -> PostFunc[_F, _R]:
        """Add an `after` callback to be called once.

        Args:
            func: The callback to be called

        Returns:
            The passed func
        """
        self._once_post_hooks.add(func)
        return func

    def on_error(self, func: ErrorFunc[_F]) -> ErrorFunc[_F]:
        """Add a callback for a function error

        Args:
            func: The error callback

        Returns:
            The provided function
        """
        self._error_hooks.add(func)
        return func

    def on_error_once(self, func: ErrorFunc[_F]) -> ErrorFunc[_F]:
        """Add an error callback to be called once.

        Args:
            func: The error callback

        Returns:
            The function itself
        """
        self._once_error_hooks.add(func)
        return func

    @typing_extensions.final
    def get_before_hooks(self, clean_once: bool = False):
        """Retrieve a list of `after` hooks.

        Args:
            clean_once (bool, optional): Wether to clean up the list of once hooks.
                Defaults to False.

        Returns:
            A set of the hook functions
        """
        hooks = {*self._pre_hooks, *self._once_pre_hooks}
        if clean_once:
            self._once_pre_hooks.clear()
        return hooks

    @typing_extensions.final
    def get_after_hooks(self, clean_once: bool = False):
        """Retrieve a set of `after` hooks.

        Args:
            clean_once (bool, optional): Wether to clean up the after once hooks.
                Defaults to False.

        Returns:
            A set of all hooks
        """
        hooks = {*self._post_hooks, *self._once_post_hooks}

        if clean_once:
            self._once_post_hooks.clear()
        return hooks

    @typing_extensions.final
    def get_error_hooks(self, clean_once: bool = False):
        """Retrieve a set of error hooks.

        Args:
            clean_once (bool, optional): Wether to clean up the once error callbacks.
                Defaults to False.

        Returns:
            A set of all hooks.
        """
        hooks = {*self._error_hooks, *self._once_error_hooks}

        if clean_once:
            self._once_error_hooks.clear()
        return hooks
