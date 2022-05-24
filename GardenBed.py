from utils.OS_color_them_detecter import *
from plants.flowers.Poppy import *
from plants.flowers.Rose import *
from plants.flowers.Violet import *
from plants.fruits.Apple import *
from plants.fruits.Pineapple import *
from plants.fruits.Orange import *
from plants.trees.Pine import *
from plants.trees.Oak import *
from plants.trees.Cactus import *
from plants.vegetables.Potato import *
from plants.vegetables.Carrot import *
from plants.vegetables.Tomato import *
import time


class GardenBed:
    def __init__(self):
        self._weeding = False
        self._moisture = 1
        self._garden = []

    @property
    def garden(self) -> list:
        return self._garden

    @property
    def weeding(self) -> bool:
        return self._weeding

    def weed_plants(self):
        self._weeding = True
        for garden_plant in self._garden:
            if garden_plant in ["Ambrosia", "Dandelion", "Cornflower"]:
                self._garden.remove(garden_plant)

    @property
    def moisture(self) -> float | int:
        return self._moisture

    def water_the_plants(self):
        self._moisture = 1

    def add_plant(self, plant: str) -> None:
        """Add plant to gardenbed, if plants in gardenbed less than 5."""
        if len(self._garden) <= 5:
            match plant:
                case "Poppy":
                    self._garden.append(Poppy())
                case "Rose":
                    self._garden.append(Rose())
                case "Violet":
                    self._garden.append(Violet())
                case "Pineapple":
                    self._garden.append(Pineapple())
                case "Apple":
                    self._garden.append(Apple())
                case "Orange":
                    self._garden.append(Orange())
                case "Cactus":
                    self._garden.append(Cactus())
                case "Oak":
                    self._garden.append(Oak())
                case "Pine":
                    self._garden.append(Pine())
                case "Carrot":
                    self._garden.append(Carrot())
                case "Potato":
                    self._garden.append(Potato())
                case "Tomato":
                    self._garden.append(Tomato())
        else:
            print("You can't add more then 5 plants to garden.")
            time.sleep(5)
            return
            # raise "You can't add more then 5 plants to garden."

    def del_plant(self, position) -> None:
        """Delete and return requested item from garednbed."""
        try:
            return self._garden.pop(position)
        except IndexError as err:
            print(err, "\nThis plant position is unavailable.")
            time.sleep(5)
            return
            # raise "This plant position is unavailable."

    def step(self, rain: bool, sun: float | int):
        """Each turn the plant and gardenbed changes under
        the influence of the environment."""
        if rain:
            self._moisture = self._moisture + 0.15 if self._moisture + 0.15 < 1 else 1
        else:
            self._moisture = self._moisture - 0.05 if self._moisture - 0.05 > 0 else 0
        for garden_plant in self._garden:
            if garden_plant not in ["Ambrosia", "Dandelion", "Cornflower"]:
                if not garden_plant._live_status:
                    self._garden.remove(garden_plant)
                    continue
                garden_plant.age()
                garden_plant.change_boosts(self.moisture, sun, self.weeding)
                garden_plant.stop_sick()
                garden_plant.sick()
            if garden_plant in ["Ambrosia", "Dandelion", "Cornflower"] and random() < 0.3:
                self._garden.remove(garden_plant)
        if len(self._garden) < 5 and random() < 0.1:
            self._garden.append(choice(["Ambrosia", "Dandelion", "Cornflower"]))
        if random() < 0.2:
            self._weeding = False

    def show_plants_names(self):
        for point in range(5):
            if point > len(self._garden) - 1:
                print("empty", end=", ")
            else:
                if self._garden[point] not in ["Ambrosia", "Dandelion", "Cornflower"]:
                    if self._garden[point].ills:
                        print(Fore.MAGENTA + self._garden[point].name + detect_dark_mode(), end=", ")
                    else:
                        print(self._garden[point].name, end=", ")
                else:
                    print(Fore.YELLOW + self._garden[point] + detect_dark_mode(), end=", ")
        print()

    def show_all_stats(self):
        """Show all plants in gardenbed. If the plant is illing,
        it become with magenta name. If harvest or live >= 50%
        printing yellow, if >= 80% printing red, in standard green."""
        print(detect_dark_mode())
        for point in range(5):
            print(f"\n{point+1}. ", end='')
            if point > len(self._garden) - 1:
                print()
                continue
            if self._garden[point] in ["Ambrosia", "Dandelion", "Cornflower"]:
                print(f"Name: {Fore.YELLOW + self._garden[point] + detect_dark_mode()}")
                continue

            # Name
            print(f"Name: {self._garden[point].name}")

            # Harvest
            color = Fore.GREEN
            if self._garden[point].harvest_progress >= self._garden[point].harvest_max * 0.5:
                color = Fore.YELLOW
            if self._garden[point].harvest_progress >= self._garden[point].harvest_max * 0.8:
                color = Fore.RED
            print(f"Harvest: {color + str(self._garden[point].harvest_progress) + detect_dark_mode()}/"
                  f"{self._garden[point].harvest_max}")

            # Live
            color = Fore.GREEN
            if self._garden[point].live >= self._garden[point].live_max * 0.5:
                color = Fore.YELLOW
            if self._garden[point].harvest_progress >= self._garden[point].live_max * 0.8:
                color = Fore.RED
            print(f"Live: {color + str(self._garden[point].live) + detect_dark_mode()}/"
                  f"{self._garden[point].live_max}")

            # Immunity
            print(f"Immunity: {self._garden[point].immunity}")
            
            # Ills
            print("Ills:", Fore.MAGENTA + ", ".join(self._garden[point].ills) + detect_dark_mode() if self._garden[point].ills else None)
