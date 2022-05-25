import time
from GardenBed import *
from Warehouse import Warehouse
from utils.OS_color_them_detecter import detect_dark_mode
import json
import statistics

try:
    from colorama import Fore
except ImportError as err:
    print(err)
    colorama = None


class Master:
    def __init__(self, warehouse: Warehouse = Warehouse(), gardenbed: list = None):
        if gardenbed is None:
            gardenbed = [GardenBed() for _ in range(5)]
        self.__gbed = gardenbed
        self.__whouse: Warehouse = warehouse
        self.__sun: float = 1
        self.__rain: bool = False

    @property
    def sun(self) -> float:
        return self.__sun

    @property
    def rain(self) -> bool:
        return self.__rain

    @property
    def warehouse(self) -> Warehouse:
        return self.__whouse.seeds

    @property
    def gardenbed(self) -> list:
        return self.__gbed

    def weed(self, position: int):
        """Weed you're gardenbed."""
        self.__gbed[position].weed_plants()

    def water(self, position):
        """Watering you're gradenbed."""
        self.__gbed[position].water_the_plants()

    @staticmethod
    def convert_garden_to_dict(garden: list):
        """Write garden info into dict to save in json."""
        return [
            [
                [{"Name": plant.name,
                  "Harvest progress": plant.harvest_progress,
                  "Harvest max": plant.harvest_max,
                  "Live": plant.live,
                  "Live max": plant.live_max,
                  "Immunity": plant.immunity,
                  "Ills": plant.ills,
                  }, gardenbed.moisture, gardenbed.weeding] if plant not in ["Ambrosia", "Dandelion", "Cornflower"] and
                                                               plant else plant for plant in gardenbed.garden]
            for gardenbed in garden]

    def restore_info(self):
        """Restore garden info from json and write into objects."""
        garden_save: list
        warehouse_save: dict
        try:
            with open("autosave_garden.json", "r") as autosave_file:
                garden_save = json.load(autosave_file)
        except OSError as err:
            print(err)
            time.sleep(5)
            return
        if not garden_save:
            return
        garden: list = []
        for gardenbed in garden_save:
            restore_gbed = GardenBed()
            for plant in gardenbed:
                if plant not in ["Ambrosia", "Dandelion", "Cornflower"] and plant:
                    for point in range(len(plant)):
                        match point:
                            case 2:
                                restore_gbed._weeding = plant[point]
                            case 1:
                                restore_gbed._moisture = plant[point]
                            case 0:
                                match plant[point]["Name"]:
                                    case "Poppy":
                                        restore_gbed._garden.append(Poppy(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Rose":
                                        restore_gbed._garden.append(Rose(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Violet":
                                        restore_gbed._garden.append(Violet(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Pineapple":
                                        restore_gbed._garden.append(Pineapple(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Apple":
                                        restore_gbed._garden.append(Apple(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Orange":
                                        restore_gbed._garden.append(Orange(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Cactus":
                                        restore_gbed._garden.append(Cactus(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Oak":
                                        restore_gbed._garden.append(Oak(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Pine":
                                        restore_gbed._garden.append(Pine(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Carrot":
                                        restore_gbed._garden.append(Carrot(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Potato":
                                        restore_gbed._garden.append(Potato(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                                    case "Tomato":
                                        restore_gbed._garden.append(Tomato(
                                            plant[point]["Harvest progress"],
                                            plant[point]["Harvest max"],
                                            plant[point]["Live"],
                                            plant[point]["Live max"],
                                            plant[point]["Immunity"],
                                            plant[point]["Ills"]
                                        ))
                else:
                    restore_gbed._garden.append(plant)
            garden.append(restore_gbed)
        self.__gbed = garden

        try:
            with open("autosave_warehouse.json", "r") as autosave_file:
                warehouse_save = json.load(autosave_file)
        except OSError as err:
            print(err)
            time.sleep(5)
            return
        if not warehouse_save:
            return
        self.__whouse._seeds = warehouse_save

    def grow_plant(self, inp_plant_name: str = None, inp_gardenbed_place: int = None):
        """Grow plant in gardenbed and delete one seed from warehouse."""
        self.restore_info()
        plant_name: str = inp_plant_name.strip()
        gardenbed_number: int = inp_gardenbed_place
        if not plant_name:
            try:
                plant_name: str = str(input(detect_dark_mode() +
                                            "Enter the name of the plant you want to grow: ")).strip()
            except TypeError as err:
                print(err)
        if len(self.__gbed[gardenbed_number].garden) <= 5:
            try:
                self.__whouse.plant_seed(plant_name)
            except KeyError as err:
                print(err)
                return
            else:
                self.__gbed[gardenbed_number].add_plant(plant_name)
        else:
            print("Max length 5.")
            return
        with open("autosave_garden.json", "w") as autosave:
            json.dump(self.convert_garden_to_dict(self.__gbed), autosave)
        with open("autosave_warehouse.json", "w") as autosave:
            json.dump(self.__whouse.seeds, autosave)

    def delete_plant(self, inp_gardenbed_number: int = None, inp_position: int = None):
        """Delete chosen plant."""
        self.restore_info()
        gardenbed_number = inp_gardenbed_number
        position = inp_position
        if inp_gardenbed_number is None:
            try:
                gardenbed_number: int = int(input("Enter garden number: ")) - 1
                position: int = int(input("Enter position: ")) - 1
            except TypeError as err:
                print(err)
        if inp_position is None:
            try:
                position: int = int(input("Enter position: ")) - 1
            except TypeError as err:
                print(err)
        try:
            self.__gbed[gardenbed_number].del_plant(position)
        except IndexError as err:
            print(err)
            time.sleep(5)
            return
        with open("autosave_garden.json", "w") as autosave:
            json.dump(self.convert_garden_to_dict(self.__gbed), autosave)

    def show_plants_short(self):
        """Print plants names, if plant is ill print magenta name."""
        self.restore_info()
        for key, plant in enumerate(self.__gbed):
            print(key + 1, end=".")
            plant.show_plants_names()

    def show_gardenbed_info(self, position: int = 0):
        """Print detail information about gardenbed."""
        self.restore_info()
        try:
            self.__gbed[position].show_all_stats()
        except IndexError as err:
            print("This gardenbed is unavailable.\n", err)

    def show_warehouse_info(self):
        """Print seeds names and count."""
        self.__whouse.show_seeds()

    @staticmethod
    def print_information(plants: list):
        """Print detail information about every transferred
        plant like show_garden_info."""
        for pl in plants:
            # Name
            print(f"Name: {pl.name}")
            # Harvest
            color = Fore.GREEN
            if pl.harvest_progress >= pl.harvest_max * 0.5:
                color = Fore.YELLOW
            if pl.harvest_progress >= pl.harvest_max * 0.8:
                color = Fore.RED
            print(f"Harvest: {color + str(pl.harvest_progress) + detect_dark_mode()}/"
                  f"{pl.harvest_max}")
            # Live
            color = Fore.GREEN
            if pl.live >= pl.live_max * 0.5:
                color = Fore.YELLOW
            if pl.harvest_progress >= pl.live_max * 0.8:
                color = Fore.RED
            print(f"Live: {color + str(pl.live) + detect_dark_mode()}/"
                  f"{pl.live_max}")
            # Immunity
            print(f"Immunity: {pl.immunity}")
            # Ills
            print("Ills:", Fore.MAGENTA + ", ".join(pl.ills) + detect_dark_mode() if pl.ills else None, end="\n\n")

    def sort_elements(self, sort_name: str) -> list:
        """Sort and show or return plants by name, harvest,
        live, immunity, ills."""
        self.restore_info()
        sorted_plants = []
        for gardenbed in self.__gbed:
            sorted_plants += [plant for plant in gardenbed.garden if
                              plant not in ["Ambrosia", "Dandelion", "Cornflower"]]
        match sort_name:
            case "Name":
                sorted_plants.sort(key=lambda plant: plant.name)
            case "Harvest":
                sorted_plants.sort(key=lambda plant: plant.harvest_progress / plant.harvest_max)
            case "Live":
                sorted_plants.sort(key=lambda plant: plant.live / plant.live_max)
            case "Immunity":
                sorted_plants.sort(key=lambda plant: plant.immunity)
            case "Ills":
                sorted_plants.sort(key=lambda plant: plant.ills)
                sorted_plants = filter(lambda plant: plant.ills, sorted_plants)
        self.print_information(sorted_plants)
        return sorted_plants

    def avg_statistics(self) -> tuple:
        """Show or return tuple with avg statistics
        by different plant parameters."""
        self.restore_info()
        plant_data = {
            "Harvest": [],
            "Live": [],
            "Immunity": [],
            "Ills count": []
        }
        for gardenbed in self.__gbed:
            plant_data["Harvest"] += [plant.harvest_progress / plant.harvest_max for plant in
                                      gardenbed.garden if plant not in ["Ambrosia", "Dandelion", "Cornflower"]]
            plant_data["Live"] += [plant.live / plant.live_max for plant in
                                   gardenbed.garden if plant not in ["Ambrosia", "Dandelion", "Cornflower"]]
            plant_data["Immunity"] += [plant.immunity for plant in
                                       gardenbed.garden if plant not in ["Ambrosia", "Dandelion", "Cornflower"]]
            plant_data["Ills count"] += [len(plant.ills) for plant in
                                         gardenbed.garden if plant not in ["Ambrosia", "Dandelion", "Cornflower"]]
        for param in plant_data.keys():
            if plant_data[param]:
                plant_data[param] = statistics.mean(plant_data[param])

        for param, value in plant_data.items():
            if not value:
                continue
            print(f"{param}: {round(value * .85, 2)}")
        return plant_data

    def step(self, count: int = 1):
        """Call step in warehouse and gardenbed. Also call
        rain and change sun intensity."""
        self.restore_info()
        for _ in range(count):
            self.__sun = random()
            self.__rain = choice([True, False])
            self.__whouse.step()
            for gardenbed in self.__gbed:
                gardenbed.step(self.__rain, self.__sun)
        with open("autosave_garden.json", "w") as autosave:
            json.dump(self.convert_garden_to_dict(self.__gbed), autosave)
        with open("autosave_warehouse.json", "w") as autosave:
            json.dump(self.__whouse.seeds, autosave)
