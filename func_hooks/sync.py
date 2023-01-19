"""Synchronous hooks implementation."""
import asyncio
import typing

import typing_extensions

import anyio

from .base import BaseHooks
from .typing import Invocation, InvocationError, InvocationResult

_P = typing_extensions.ParamSpec("_P")
_R = typing.TypeVar("_R")
_FR = typing.TypeVar("_FR")


class Hooks(BaseHooks[typing.Callable[_P, _FR], typing.Any], typing.Generic[_P, _FR]):
    """A decorator for synchronous hooks."""

    def __init__(self, func: typing.Callable[_P, _FR]) -> None:
        super().__init__()

        self._func = func
        self._result_hooks: typing.Set[
            typing.Callable[[typing.Dict[str, typing.Any]], typing.Any]
        ] = set()

    @property
    def is_async(self):
        """Return wether the hooks are for an async function."""
        return asyncio.iscoroutinefunction(self._func)

    def __call__(self, *args: _P.args, **kwargs: _P.kwargs) -> _FR:
        if not self.is_async:
            return self._run_sync(*args, **kwargs)  # type: ignore

        return anyio.to_thread.run_sync(  # type: ignore
            lambda args, kwargs: self._run_sync(*args, **kwargs), args, kwargs
        )

    def _run_sync(self, *args: _P.args, **kwargs: _P.kwargs) -> typing.Any:
        results: typing.Dict[str, typing.Any] = {
            "before_errors": [],
            "after_errors": [],
            "error_hook_errors": [],
            "success": False,
            "result": None,
        }
        results["before_errors"] = self._run_pre_hooks(
            Invocation(
                func=self._func,
                args=args,
                kwargs=kwargs,
            )
        )
        try:
            if self.is_async:
                results["result"] = anyio.from_thread.run(
                    lambda args, kwargs: self._func(*args, **kwargs),  # type: ignore
                    args,
                    kwargs,
                )
            else:
                results["result"] = self._func(*args, **kwargs)
        except Exception as exc:
            results["error_hook_errors"] = self._run_error_hooks(
                InvocationError(
                    func=self._func,
                    args=args,
                    kwargs=kwargs,
                    exception=exc,
                )
            )
            raise
        else:
            results["after_errors"] = self._run_post_hooks(
                InvocationResult(
                    func=self._func,
                    args=args,
                    kwargs=kwargs,
                    result=results["result"],  # type: ignore
                )
            )
        self._run_results_hook(results)
        return results["result"]  # type: ignore

    def _run_results_hook(self, results: typing.Dict[str, typing.Any]) -> None:
        for item in self._result_hooks.copy():
            item(results)

    def _run_pre_hooks(self, invocation: Invocation[typing.Any]):
        errors: typing.List[BaseException] = []

        for item in self.get_before_hooks(clean_once=True):
            try:
                if not asyncio.iscoroutinefunction(item):
                    item(invocation.copy())  # type: ignore
                else:
                    anyio.from_thread.run(item, invocation.copy())
            except BaseException as exc:  # pylint: disable=broad-except
                errors.append(exc)
        return errors

    def _run_post_hooks(
        self, invocation_result: InvocationResult[typing.Any, typing.Any]
    ):
        errors: typing.List[BaseException] = []

        for item in self.get_after_hooks(clean_once=True):
            try:
                if not asyncio.iscoroutinefunction(item):
                    item(invocation_result.copy())  # type: ignore
                else:
                    anyio.from_thread.run(item, invocation_result.copy())
            except BaseException as exc:  # pylint: disable=broad-except
                errors.append(exc)
        return errors

    def _run_error_hooks(self, result: InvocationError[typing.Any]):
        errors: typing.List[BaseException] = []

        for item in self.get_error_hooks(clean_once=True):
            try:
                if not asyncio.iscoroutinefunction(item):
                    item(result.copy())  # type: ignore
                else:
                    anyio.from_thread.run(item, result.copy())
            except BaseException as exc:  # pylint: disable=broad-except
                errors.append(exc)

        return errors

    def on_results(
        self, func: typing.Callable[[typing.Dict[str, typing.Any]], None]
    ) -> typing.Callable[[typing.Dict[str, typing.Any]], None]:
        """A function to call on results.

        Args:
            func: The function that receives all results

        Returns:
            typing.Callable[[typing.Dict[str, typing.Any]], None]: The function itself
        """
        self._result_hooks.add(func)
        return func
