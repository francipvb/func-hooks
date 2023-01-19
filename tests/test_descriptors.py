# pylint: disable=redefined-outer-name,too-few-public-methods
# pylint: disable=missing-module-docstring,missing-function-docstring
import typing
from unittest import mock

import pytest

import func_hooks


@pytest.fixture()
def call_mock():
    return mock.Mock()


@pytest.fixture()
def proxy_class(call_mock: mock.Mock):
    class _CallTest:
        test_method = func_hooks.hooks(call_mock)

    return _CallTest


def test_call_func(proxy_class: typing.Any, call_mock: mock.Mock):

    obj = proxy_class()
    obj.test_method()
    call_mock.assert_called_with(obj)
