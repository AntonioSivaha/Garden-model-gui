from plants.Fruit import *


class Pineapple(Fruit):
    def __init__(self,
                 inp_harvest_progress: int = 0,
                 inp_harvest_max: int = 30,
                 inp_live: int = 0,
                 inp_live_max: int = 110,
                 inp_immunity: float | int = 1,
                 inp_ills: list = []
                 ):
        self._harvest_progress = inp_harvest_progress
        self._harvest_max = inp_harvest_max
        self._live = inp_live
        self._live_max = inp_live_max
        self._immunity = inp_immunity
        self._ills: list = inp_ills
        self._ills_list = []
        self._name = "Ananas"
