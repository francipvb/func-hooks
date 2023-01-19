# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
from unittest import mock

import pytest

import func_hooks


def test_decorator():
    assert isinstance(func_hooks.hooks(mock.Mock()), func_hooks.Hooks)


def test_decorator_not_callable():
    with pytest.raises(ValueError):
        func_hooks.hooks(mock.NonCallableMock(object))
