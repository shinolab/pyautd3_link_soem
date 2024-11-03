import os

import numpy as np
from pyautd3 import AUTD3, Controller, Focus, Hz, Sine

from pyautd3_link_soem import SOEM, Status


def err_handler(slave: int, status: Status) -> None:
    print(f"slave[{slave}]: {status}")
    if status == Status.Lost():
        # You can also wait for the link to recover, without exitting the process
        os._exit(-1)


if __name__ == "__main__":
    from pyautd3 import tracing_init

    os.environ["RUST_LOG"] = "autd3=INFO"

    tracing_init()

    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(
        SOEM.builder().with_err_handler(err_handler),  # type: ignore[arg-type]
    ) as autd:
        autd.send((Sine(150.0 * Hz), Focus(autd.center + np.array([0.0, 0.0, 150.0]))))

        _ = input("Press Enter to exit")

        autd.close()
