from typing import Any, Union


class Result:
    def __init__(self, ok: bool, value: Any):
        self.ok = ok
        self.value = value

    def __repr__(self) -> str:
        return f'Result(ok={self.ok}, value={self.value})'


class Ok(Result):
    def __init__(self, value: Any = None):
        super().__init__(ok=True, value=value)

    def __repr__(self) -> str:
        return f'Ok({self.value})'


class Err(Result):
    def __init__(self, error: Union[Exception, str]):
        super().__init__(ok=False, value=error)

    def __repr__(self) -> str:
        return f'Err({self.value})'
