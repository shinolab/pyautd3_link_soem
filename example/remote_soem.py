import numpy as np
from pyautd3 import AUTD3, Controller, Focus, Hz, Sine

from pyautd3_link_soem import RemoteSOEM

if __name__ == "__main__":
    with Controller.builder([AUTD3([0.0, 0.0, 0.0])]).open(
        RemoteSOEM.builder("127.0.0.1:8080"),
    ) as autd:
        autd.send((Sine(150.0 * Hz), Focus(autd.center + np.array([0.0, 0.0, 150.0]))))

        _ = input("Press Enter to exit")

        autd.close()
