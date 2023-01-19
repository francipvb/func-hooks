"""Type definitions."""
import dataclasses
import typing
import typing_extensions

_P = typing_extensions.ParamSpec("_P")
_F = typing.TypeVar("_F", bound=typing.Callable[..., typing.Any])
_R_co = typing.TypeVar("_R_co", covariant=True)
_R_contra = typing.TypeVar("_R_contra", contravariant=True)


@dataclasses.dataclass()
class Invocation(typing.Generic[_F]):
    """Information of an invocation."""

    func: _F
    args: typing.Tuple[typing.Any, ...]
    kwargs: typing.Dict[str, typing.Any]

    def copy(self):
        """Return a new invocation."""
        return dataclasses.replace(self)


@dataclasses.dataclass()
class InvocationResult(Invocation[_F], typing.Generic[_F, _R_co]):
    """Invocation data with the result."""

    result: _R_co


@dataclasses.dataclass()
class InvocationError(Invocation[_F]):
    """Error invocation result."""

    exception: BaseException


class PreFunc(typing.Protocol[_F]):  # pylint: disable=too-few-public-methods
    """Protocol for pre-hooks."""

    def __call__(self, invocation: Invocation[_F]) -> typing.Any:  # pragma: nocover
        ...


class PostFunc(
    typing.Protocol[_F, _R_contra]
):  # pylint: disable=too-few-public-methods
    """Protocol for post hooks."""

    def __call__(
        self, result: InvocationResult[_F, _R_contra]
    ) -> typing.Any:  # pragma: nocover
        ...


class ErrorFunc(typing.Protocol[_F]):  # pylint: disable=too-few-public-methods
    """Protocol for error hooks."""

    def __call__(self, result: InvocationError[_F]) -> typing.Any:  # pragma: nocover
        ...
