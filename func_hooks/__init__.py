import typing
import typing_extensions

_P = typing_extensions.ParamSpec("_P")
_R = typing.TypeVar("_R")


class Hooks(typing.Generic[_P, _R]):
    def __init__(self, func: typing.Callable[_P, _R]) -> None:
        super().__init__()
        self.func = func

    def __call__(self, *args: _P.args, **kwds: _P.kwargs) -> _R:
        return self.func(*args, **kwds)

    def _run_pre_hooks(self):
        pass

    def _run_post(self, result: _R, *args: _P.args, **kwargs: _P.kwargs):
        pass

    def before(self):
        pass

    def after(self):
        pass
