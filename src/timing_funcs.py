import decimal
import inspect
import math
import timeit
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from types import FrameType

type _Stmt = str | Callable[[], object]


def get_caller_globals(frame: FrameType | None) -> dict[str, Any] | None:
    if frame is None:
        return None

    caller_frame = frame.f_back

    if caller_frame is None:
        return None

    return caller_frame.f_globals


def beautify_time(time: float) -> str:
    ten_power = math.log10(time)

    def four_digits(num: float) -> str:
        number = decimal.Decimal.from_float(num)

        with decimal.localcontext() as ctx:
            ctx.prec = 4
            number = +number

        return str(number)

    if ten_power > 3:
        return f"{round(time)}s"

    if ten_power > -0.25:
        return f"{four_digits(time)}s"

    if ten_power > -3.25:
        return f"{four_digits(time * 1e3)}ms"

    if ten_power > -6.25:
        return f"{four_digits(time * 1e6)}\u03bcs"

    if ten_power > -9.25:
        return f"{four_digits(time * 1e9)}ns"

    return f"{four_digits(time * 1e12)}ps"


def run_test(test_name: str, statement: _Stmt, setup: _Stmt = "pass") -> None:
    globs = get_caller_globals(inspect.currentframe())

    timer = timeit.Timer(statement, setup, globals=globs)
    loop_count, time_taken = timer.autorange()

    print(  # noqa: T201
        f"One loop time for {test_name}: "
        f"{beautify_time(time_taken / loop_count)} ({loop_count=})"
    )
