from random import random, choice
from utils.OS_color_them_detecter import detect_dark_mode

try:
    from colorama import Fore
except ImportError as err:
    print(err)
    Fore = None


class Warehouse:
    _seeds = {
        "Poppy": 5, "Rose": 5, "Violet": 5,
        "Pineapple": 2, "Apple": 2, "Orange": 2,
        "Cactus": 1, "Oak": 1, "Pine": 1,
        "Carrot": 5, "Potato": 5, "Tomato": 5
    }

    @property
    def seeds(self):
        return self._seeds

    def step(self):
        """Add random seeds (0-3) with a 50% probability."""
        for _ in range(3):
            self._seeds[choice(list(self._seeds.keys()))] += 1 if random() > 0.5 else 0

    def add_seed(self, seed_name: str, count: int = 1):
        try:
            self._seeds[seed_name] += count
        except KeyError as err:
            print(err)
            raise "This seed is unavailable."

    def show_seeds(self):
        """Print all the seeds you own."""
        plants_type_list = [
            Fore.RED + "Flowers:" + detect_dark_mode(),
            Fore.YELLOW + "Fruits:" + detect_dark_mode(),
            Fore.GREEN + "Trees:" + detect_dark_mode(),
            Fore.LIGHTGREEN_EX + "Vegetables:" + detect_dark_mode()
        ]
        plant_type = 0
        element = 3
        for plants, values in self._seeds.items():
            if element == 3:
                element = 0
                print(plants_type_list[plant_type])
                plant_type += 1
            print(plants, values)
            element += 1

    def plant_seed(self, seed: str):
        """Plant seed to gardenbed and delete from warehouse.
        If seeds less than 1 making a mistake."""
        if seed in self._seeds.keys() and self._seeds[seed] >= 1:
            self._seeds[seed] -= 1
            return seed
        else:
            raise "This seed is unavailable."
