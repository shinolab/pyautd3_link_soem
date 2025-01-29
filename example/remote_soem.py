import numpy as np
from pyautd3 import AUTD3, Controller, Focus, FocusOption, Hz, Sine, SineOption

from pyautd3_link_soem import RemoteSOEM

if __name__ == "__main__":
    with Controller.open(
        [AUTD3(pos=[0.0, 0.0, 0.0], rot=[1.0, 0.0, 0.0, 0.0])],
        RemoteSOEM("127.0.0.1:8080"),
    ) as autd:
        autd.send(
            (
                Sine(freq=150.0 * Hz, option=SineOption()),
                Focus(pos=autd.center + np.array([0.0, 0.0, 150.0]), option=FocusOption()),
            ),
        )

        _ = input("Press Enter to exit")

        autd.close()
