import os

import numpy as np
from pyautd3 import AUTD3, Controller, Focus, FocusOption, Hz, Sine, SineOption

from pyautd3_link_soem import SOEM, SOEMOption, Status, tracing_init


def err_handler(slave: int, status: Status) -> None:
    print(f"slave[{slave}]: {status}")
    if status == Status.Lost():
        # You can also wait for the link to recover, without exitting the process
        os._exit(-1)


if __name__ == "__main__":
    os.environ["RUST_LOG"] = "autd3=INFO"

    tracing_init()

    with Controller.open([AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])], SOEM(err_handler, SOEMOption())) as autd:
        autd.send(
            (
                Sine(freq=150.0 * Hz, option=SineOption()),
                Focus(pos=autd.center + np.array([0.0, 0.0, 150.0]), option=FocusOption()),
            ),
        )

        _ = input("Press Enter to exit")

        autd.close()
