from plants.Flower import *


class Rose(Flower):
    def __init__(self,
                 inp_harvest_progress: int = 0,
                 inp_harvest_max: int = 10,
                 inp_live: int = 0,
                 inp_live_max: int = 60,
                 inp_immunity: float | int = 0.5,
                 inp_ills: list = []
                 ):
        self._harvest_progress = inp_harvest_progress
        self._harvest_max = inp_harvest_max
        self._live = inp_live
        self._live_max = inp_live_max
        self._immunity = inp_immunity
        self._ills: list = inp_ills
        self._name = "Rose"
