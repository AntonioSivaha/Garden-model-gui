from random import random, choice


class Plant:
    _name: str
    _harvest_progress: int | float = 0
    _harvest_max: int
    _live: int | float = 0
    _live_max: int
    _immunity: int | float = 0  # immunity max: 1, min: 0
    _ills: list
    _ills_list: list
    _live_status: bool = True

    @property
    def name(self) -> str:
        return self._name

    @property
    def harvest_progress(self) -> int | float:
        return self._harvest_progress

    @property
    def harvest_max(self) -> int:
        return self._harvest_max

    @property
    def live(self) -> int | float:
        return self._live

    @property
    def live_max(self) -> int:
        return self._live_max

    @property
    def immunity(self) -> int | float:
        return self._immunity

    @property
    def ills(self) -> list:
        return self._ills

    @property
    def ills_list(self) -> list:
        return self._ills_list

    @property
    def live_status(self) -> bool:
        return self._live_status

    def age(self):
        """Plant is getting old."""
        self._harvest_progress = 1 + self._harvest_progress if \
            self._harvest_progress + 1 <= self._harvest_max else self._harvest_max
        self._live += 1
        if self._live >= self._live_max:
            self._live_status = False

    def sick(self):
        """If plant immunity is very low (0.6<) or plant print(is not lucky,
        it can get chance to get sick. Pineapple never gets sick."""
        if random() + self._immunity < 1.6 and self._name:
            self._ills.append(choice(self._ills_list))

    def stop_sick(self):
        """Remove sick if immunity + random >= 1."""
        return self._ills.pop() if self._ills and random() + self._immunity >= 0.65 else None

    def change_boosts(self, moisture: int | float, sun: float | int, weeding: bool):
        """Changing immunity, harvest progress, life max
        under the influence of the environment."""
        if moisture < 0.2:
            self._immunity += moisture + 0.5 + weeding * 0.3 + sun - 0.7 - len(self.ills) * 0.2
            self._live_max -= 2 + len(self.ills)
        if 0.2 <= moisture < 0.4:
            self._immunity += moisture + 0.3 + weeding * 0.5 + sun - 0.7 - len(self.ills) * 0.2
            self._live_max -= 1 + len(self.ills)
        if 0.4 <= moisture < 0.6:
            self._immunity += moisture + weeding * 0.5 + sun - 0.8 - len(self.ills) * 0.2
            self._live_max -= len(self.ills)
        if 0.6 <= moisture < 0.8:
            self._immunity += moisture + weeding * 0.5 + sun - 0.8 - len(self.ills) * 0.2
            self._live_max += 1 - len(self.ills)
        if 0.8 <= moisture <= 1:
            self._immunity += moisture + weeding * 0.3 + sun - 0.8 - len(self.ills) * 0.2
            self._live_max += 2 - len(self.ills)
            self._harvest_progress += 1 if self._harvest_progress + 1 < self._harvest_max else 0
        self._immunity = 1 if self._immunity > 1 else self._immunity
        self._immunity = 0 if self._immunity < 0 else self._immunity
