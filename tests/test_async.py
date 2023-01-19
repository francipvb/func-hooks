# pylint: disable=missing-module-docstring,missing-function-docstring
import typing
from unittest import mock

import pytest
import func_hooks

pytestmark = [
    pytest.mark.filterwarnings("ignore:Error while calling"),
]


@pytest.mark.anyio()
async def test_run_func():
    func = mock.AsyncMock()
    hooks = func_hooks.Hooks(func)
    await hooks(1, 2, x=4)
    func.assert_called_with(1, 2, x=4)
    func.assert_awaited()


@pytest.mark.anyio()
async def test_call_before():
    func = mock.AsyncMock()
    before = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_before(before)
    await hooks(1, 2)
    before.assert_called_with(func_hooks.Invocation(args=(1, 2), kwargs={}, func=func))


@pytest.mark.anyio()
async def test_call_before_awaited():
    func = mock.AsyncMock()
    before = mock.AsyncMock()

    hooks = func_hooks.Hooks(func)
    hooks.on_before(before)
    await hooks(1, 2)
    before.assert_called_with(func_hooks.Invocation(args=(1, 2), kwargs={}, func=func))
    before.assert_awaited()


@pytest.mark.anyio()
async def test_call_before_once():
    func = mock.AsyncMock()
    before = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_before_once(before)
    await hooks(1, 2)
    await hooks(3, 2)
    before.assert_called_once_with(func_hooks.Invocation(func, (1, 2), {}))


@pytest.mark.anyio()
async def test_call_before_once_awaited():
    func = mock.AsyncMock()
    before = mock.AsyncMock()

    hooks = func_hooks.Hooks(func)
    hooks.on_before_once(before)
    await hooks(1, 2)
    await hooks(3, 2)
    before.assert_called_once_with(func_hooks.Invocation(func, (1, 2), {}))
    before.assert_awaited()


@pytest.mark.anyio()
async def test_call_after():
    func = mock.AsyncMock()
    after = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_after(after)
    result = await hooks(1, 2)
    after.assert_called_with(func_hooks.InvocationResult(func, (1, 2), {}, result))


@pytest.mark.anyio()
async def test_call_after_awaited():
    func = mock.AsyncMock()
    after = mock.AsyncMock()

    hooks = func_hooks.Hooks(func)
    hooks.on_after(after)
    result = await hooks(1, 2)
    after.assert_called_with(func_hooks.InvocationResult(func, (1, 2), {}, result))
    after.assert_awaited()


@pytest.mark.anyio()
async def test_call_after_once():
    func = mock.AsyncMock()
    after = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_after_once(after)
    result = await hooks(1, 2)
    await hooks(3, 2)
    after.assert_called_once_with(func_hooks.InvocationResult(func, (1, 2), {}, result))


@pytest.mark.anyio()
async def test_call_after_once_awaited():
    func = mock.AsyncMock()
    after = mock.AsyncMock()

    hooks = func_hooks.Hooks(func)
    hooks.on_after_once(after)
    result = await hooks(1, 2)
    await hooks(3, 2)
    after.assert_called_once_with(func_hooks.InvocationResult(func, (1, 2), {}, result))
    after.assert_awaited()


@pytest.mark.anyio()
async def test_call_error():
    func = mock.AsyncMock()
    error = Exception()
    func.side_effect = error
    on_error = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_error(on_error)
    with pytest.raises(Exception):
        await hooks(1, 2)
    on_error.assert_called_with(func_hooks.InvocationError(func, (1, 2), {}, error))


@pytest.mark.anyio()
async def test_call_error_async():
    func = mock.AsyncMock()
    error = Exception()
    func.side_effect = error
    on_error = mock.AsyncMock()

    hooks = func_hooks.Hooks(func)
    hooks.on_error(on_error)
    with pytest.raises(Exception):
        await hooks(1, 2)
    on_error.assert_called_with(func_hooks.InvocationError(func, (1, 2), {}, error))
    on_error.assert_awaited()


@pytest.mark.anyio()
async def test_call_error_once():
    func = mock.AsyncMock()
    error = Exception()
    func.side_effect = error
    on_error = mock.Mock()

    hooks = func_hooks.Hooks(func)
    hooks.on_error_once(on_error)
    with pytest.raises(Exception):
        await hooks(1, 2)
    with pytest.raises(Exception):
        await hooks(1, 2)
    on_error.assert_called_once_with(
        func_hooks.InvocationError(func, (1, 2), {}, error)
    )


@pytest.mark.anyio()
async def test_run_result_hook():
    func = mock.AsyncMock()
    hooks = func_hooks.Hooks(func)
    results = mock.Mock()
    hooks.on_results(results)

    await hooks(1, 2)
    results.assert_called()


@pytest.mark.anyio()
async def test_collect_before_errors():
    func = mock.AsyncMock()
    error = Exception()

    hooks = func_hooks.Hooks(func)
    error_mock = mock.Mock(side_effect=error)
    hooks.on_before(error_mock)

    def _results(results: typing.Dict[str, typing.Any]):
        assert error in results["before_errors"]

    hooks.on_results(_results)

    await hooks(1, 2)
    func.assert_called()


@pytest.mark.anyio()
async def test_collect_after_errors():
    func = mock.AsyncMock()
    error = Exception()

    hooks = func_hooks.Hooks(func)
    hooks.on_after(mock.Mock(side_effect=error))

    def _results(results: typing.Dict[str, typing.Any]):
        assert error in results["after_errors"]

    hooks.on_results(_results)

    await hooks(1, 2)
    func.assert_called()


@pytest.mark.anyio()
async def test_collect_error_errors():
    func = mock.AsyncMock()
    error = Exception()
    func.side_effect = error

    hooks = func_hooks.Hooks(func)
    hooks.on_error(mock.Mock(side_effect=error))

    def _results(results: typing.Dict[str, typing.Any]):
        assert error in results["error_hook_errors"]

    hooks.on_results(_results)

    with pytest.raises(Exception):
        await hooks(1, 2)

    func.assert_called()
