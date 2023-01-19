# pylint: disable=missing-module-docstring,missing-function-docstring
import typing
from unittest import mock

import pytest
import func_hooks


def test_run_func():
    func = mock.Mock()
    hooks = func_hooks.Hooks(func)
    hooks(1, 2, x=4)
    func.assert_called_with(1, 2, x=4)


def test_call_before():
    func = mock.Mock()
    before = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_before(before)
    hooks(1, 2)
    before.assert_called_with(func_hooks.Invocation(args=(1, 2), kwargs={}, func=func))


def test_call_before_once():
    func = mock.Mock()
    before = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_before_once(before)
    hooks(1, 2)
    hooks(3, 2)
    before.assert_called_once_with(func_hooks.Invocation(func, (1, 2), {}))


def test_call_after():
    func = mock.Mock()
    after = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_after(after)
    result = hooks(1, 2)
    after.assert_called_with(func_hooks.InvocationResult(func, (1, 2), {}, result))


def test_call_after_once():
    func = mock.Mock()
    after = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_after_once(after)
    result = hooks(1, 2)
    hooks(3, 2)
    after.assert_called_once_with(func_hooks.InvocationResult(func, (1, 2), {}, result))


def test_call_error():
    func = mock.Mock()
    error = Exception()
    func.side_effect = error
    on_error = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_error(on_error)
    with pytest.raises(Exception):
        hooks(1, 2)
    on_error.assert_called_with(func_hooks.InvocationError(func, (1, 2), {}, error))


def test_call_error_once():
    func = mock.Mock()
    error = Exception()
    func.side_effect = error
    on_error = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_error_once(on_error)
    with pytest.raises(Exception):
        hooks(1, 2)
    with pytest.raises(Exception):
        hooks(1, 2)
    on_error.assert_called_once_with(
        func_hooks.InvocationError(func, (1, 2), {}, error)
    )


def test_run_result_hook():
    func = mock.Mock()
    hooks = func_hooks.Hooks(func)
    results = mock.Mock()
    hooks.on_results(results)

    hooks(1, 2)
    results.assert_called()


def test_collect_before_errors():
    func = mock.Mock()
    error = Exception()

    hooks = func_hooks.Hooks(func)
    error_mock = mock.MagicMock(side_effect=error)
    hooks.on_before(error_mock)

    def _results(results: typing.Dict[str, typing.Any]):
        assert error in results["before_errors"]

    hooks.on_results(_results)

    hooks(1, 2)
    func.assert_called()


def test_collect_after_errors():
    func = mock.Mock()
    error = Exception()

    hooks = func_hooks.Hooks(func)
    hooks.on_after(mock.MagicMock(side_effect=error))

    def _results(results: typing.Dict[str, typing.Any]):
        assert error in results["after_errors"]

    hooks.on_results(_results)

    hooks(1, 2)
    func.assert_called()


def test_collect_error_errors():
    func = mock.Mock()
    error = Exception()
    func.side_effect = error

    hooks = func_hooks.Hooks(func)
    hooks.on_error(mock.Mock(side_effect=error))

    def _results(results: typing.Dict[str, typing.Any]):
        assert error in results["error_hook_errors"]

    hooks.on_results(_results)

    with pytest.raises(Exception):
        hooks(1, 2)

    func.assert_called()
