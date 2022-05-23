from doctest import master
import pygame
from pygame.math import Vector2
import pygame_menu

from Master import Master
from utils.utils import load_sound, load_sprite


class GardenApp:
    def __init__(self, master):
        self._init_pygame()
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)

        # self.warehouse_background = load_sprite("warehouse_background.jpg")
        self.garden_background = load_sprite("tiles.png")
        self.garden_background = pygame.transform.scale(self.garden_background, (1000, 800))
        self.main_menu_background = load_sprite("main_menu_background.jpg")
        self.main_menu_background = pygame.transform.scale(self.main_menu_background, (1200, 800))

        # Plants sprites
        self.tomato_sprites = tuple(load_sprite(f"tomato/tomato_{n}.png") for n in range(1, 5 + 1))
        self.potato_sprites = tuple(load_sprite(f"potato/potato_{n}.png") for n in range(1, 2 + 1))
        self.carrot_sprites = tuple(load_sprite(f"melon/melon_{n}.png") for n in range(1, 3 + 1))
        self.pineapple_sprites = tuple(load_sprite(f"grape/grape_{n}.png") for n in range(1, 6 + 1))
        self.apple_sprites = tuple(load_sprite(f"apple/apple_{n}.png") for n in range(1, 5 + 1))

        # Garden back
        self.master = master
        self.plants_list = [[] for _ in range(5)]

        # Warehouse
        self.warehouse_theme = pygame_menu.themes.THEME_GREEN.copy()
        self.warehouse_menu = pygame_menu.Menu(
            title="Warehouse",
            width=1200,
            height=800,
            theme=self.warehouse_theme
        )
        for plant, count in self.master.warehouse.items():
            self.warehouse_menu.add.button(
                f"{plant}: {count}"
            )
        self.warehouse_menu.add.button(
            "Back",
            pygame_menu.events.BACK
        )

        # Statistics
        self.statistics_theme = pygame_menu.themes.THEME_BLUE.copy()
        self.statistics_menu = pygame_menu.Menu(
            title="Statistics",
            width=1200,
            height=800,
            theme=self.statistics_theme
        )
        for plant, value in self.master.avg_statistics().items():
            self.statistics_menu.add.button(
                f"{plant}: {value}"
            )
        self.statistics_menu.add.button(
            "Back",
            pygame_menu.events.BACK
        )

        # Sort
        self.sort_theme = pygame_menu.themes.THEME_BLUE.copy()
        self.sort_menu = pygame_menu.Menu(
            title="Sort",
            width=1200,
            height=800,
            theme=self.sort_theme
        )
        self.sort_items = [
            ("Name", "NAME"),
            ("Harvest", "HARVEST"), 
            ("Live", "LIVE"), 
            ("Immunity", "IMMUNITY"),
            ("Ills", "ILLS")
        ]
        self.sort_menu.add.selector(
            title="Sort by: ",
            items=self.sort_items
        )

        # Menu
        self.theme = pygame_menu.themes.THEME_DARK.copy()
        self.theme.background_color = (0, 0, 0, 180)
        self.menu = pygame_menu.Menu(
            title="",
            enabled=False,
            width=600,
            height=450,
            theme=self.theme
        )
        self.menu.add.label(
            "GARDEN MODEL"
        ).translate(0, -25)
        self.menu.add.button(
            "Step",
            self._do_step
        )
        self.menu.add.button(
            "Garden",
            self._main_garden
        )
        self.menu.add.button(
            "Warehouse",
            self.warehouse_menu
        )
        self.menu.add.button(
            "Statistics",
            self.statistics_menu
        )
        self.menu.add.button(
            "Sort",
            self.sort_menu
        )
        self.menu.add.button(
            "Exit",
            pygame_menu.events.EXIT
        )

        # Gardenbed menu
        # self.gardenbed_menu = pygame_menu.Menu(

        # )

        # Garden menu
        self.garden_menu_theme = pygame_menu.themes.THEME_GREEN.copy()
        # self.garden_menu_theme.background_color = (0, 0, 0, 180)
        self.garden_menu = pygame_menu.Menu(
            title="Garden",
            width=200,
            height=800,
            position=(1000, 0, False),
            theme=self.garden_menu_theme
        )
        menu_button = self.garden_menu.add.button(
            "MENU",
            self._call_main_menu,
            align=pygame_menu.locals.ALIGN_RIGHT
        )
        menu_button.translate(0, 345)
        do_step_button = self.garden_menu.add.button(
            "DO STEP",
            self._do_step,
            # align=pygame_menu.locals.ALIGN_LEFT
        )
        do_step_button.translate(0, -345)

########
    def _call_main_menu(self):
        self.garden_menu.disable()
        self.menu.enable()

    def _do_step(self):
        self.master.step()
        self.plants_list = [[] for _ in range(5)]

    def _main_garden(self):
        self.menu.disable()
        self.garden_menu.enable()

    def _sort_plants(self):
        pass
########

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    @staticmethod
    def _init_pygame():
        pygame.init()
        pygame.display.set_caption("Garden")
        # pygame.display.set_icon(load_sprite(
        #     "spring_tree_plant_garden_nature_wood_forest_icon_133298.png", False))

    def _handle_input(self):
        if self.menu.is_enabled():
            self.menu.update(pygame.event.get())

        if self.garden_menu.is_enabled():
            self.garden_menu.update(pygame.event.get())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            # do step
            elif event.type == pygame.KEYDOWN and \
                event.key == pygame.K_SPACE and not self.menu.is_enabled():
                print("Step")
                self._do_step()
            # call menu
            elif event.type == pygame.KEYDOWN and \
                event.key == pygame.K_ESCAPE and not self.menu.is_enabled():
                print("ESC")
                self.garden_menu.disable()
                self.menu.enable()

    def _process_game_logic(self):
        x_pos = {
            0: 50,
            1: 275,
            2: 500,
            3: 725,
            4: 900
        }
        y_pos = {
            0: 100,
            1: 250,
            2: 400,
            3: 550,
            4: 700
        }

        for gbed_num in range(len(self.master.gardenbed)):
            for plant_num in range(len(self.master.gardenbed[gbed_num].garden)):
                if self.master.gardenbed[gbed_num].garden[plant_num]:
                    plant = self.master.gardenbed[gbed_num].garden[plant_num]
                    # Weeds
                    if plant in ["Ambrosia", "Dandelion", "Cornflower"]:
                        match plant:
                            case "Ambrosia":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]), load_sprite("Ambrosia_bush.png")))
                            case "Dandelion":
                                dandelion_sprite = load_sprite("Dandelions.png")
                                dandelion_sprite = pygame.transform.scale(dandelion_sprite, (64, 64))
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]), dandelion_sprite))
                            case "Cornflower":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]), load_sprite("Daylily.png")
                                ))
                    # Plants
                    else:
                        match plant._name:
                            case "Poppy":
                                pass
                            case "Rose":
                                pass
                            case "Violet":
                                pass
                            case "Pineapple":
                                if plant._harvest_progress >= plant._harvest_max:
                                    pineapple_pct = 5
                                elif plant._harvest_progress * 5 // 6 >= plant._harvest_max:
                                    pineapple_pct = 4
                                elif plant._harvest_progress * 4 // 6 >= plant._harvest_max:
                                    pineapple_pct = 3
                                elif plant._harvest_progress * 3 // 6 >= plant._harvest_max:
                                    pineapple_pct = 2
                                elif plant._harvest_progress * 2 // 6 >= plant._harvest_max:
                                    pineapple_pct = 1
                                elif plant._harvest_progress * 1 // 6 >= 0:
                                    pineapple_pct = 0
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.tomato_sprites[pineapple_pct]
                                ))
                            case "Apple":
                                if plant._harvest_progress >= plant._harvest_max:
                                    apple_pct = 4
                                elif plant._harvest_progress * 4 // 5 >= plant._harvest_max:
                                    apple_pct = 3
                                elif plant._harvest_progress * 3 // 5 >= plant._harvest_max:
                                    apple_pct = 2
                                elif plant._harvest_progress * 2 // 5 >= plant._harvest_max:
                                    apple_pct = 1
                                elif plant._harvest_progress * 1 // 5 >= 0:
                                    apple_pct = 0
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.apple_sprites[apple_pct]
                                ))
                            case "Orange":
                                pass
                            case "Cactus":
                                pass
                            case "Oak":
                                pass
                            case "Pine":
                                pass
                            case "Carrot":
                                if plant._harvest_progress >= plant._harvest_max:
                                    carrot_pct = 2
                                elif plant._harvest_progress * 2 // 3 >= plant._harvest_max:
                                    carrot_pct = 1
                                elif plant._harvest_progress * 1 // 3 >= 0:
                                    carrot_pct = 0
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.carrot_sprites[tomato_pct]
                                ))
                            case "Potato":
                                if plant._harvest_progress >= plant._harvest_max:
                                    potato_pct = 1
                                elif plant._harvest_progress * 1 // 2 >= plant._harvest_max:
                                    tomato_pct = 0
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.potato_sprites[potato_pct]
                                ))
                            case "Tomato":
                                if plant._harvest_progress >= plant._harvest_max:
                                    tomato_pct = 4
                                elif plant._harvest_progress * 4 // 5 >= plant._harvest_max:
                                    tomato_pct = 3
                                elif plant._harvest_progress * 3 // 5 >= plant._harvest_max:
                                    tomato_pct = 2
                                elif plant._harvest_progress * 2 // 5 >= plant._harvest_max:
                                    tomato_pct = 1
                                elif plant._harvest_progress * 1 // 5 >= 0:
                                    tomato_pct = 0
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.tomato_sprites[tomato_pct]
                                ))

    def _draw(self):
        self.screen.fill((0, 75, 25))

        if self.menu.is_enabled():
            self.screen.blit(self.main_menu_background, (0, 0))
            self.menu.draw(self.screen)

        if self.garden_menu.is_enabled():
            self.garden_menu.draw(self.screen)
            self.screen.blit(self.garden_background, (0, 0))
            
            for gardenbed in self.plants_list:
                for plant in gardenbed:
                    if plant:
                        plant.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(5)


class PlantObject:
    def __init__(self, position, sprite):
        self.position = Vector2(position)
        self.sprite = sprite

    def draw(self, surface):
        surface.blit(self.sprite, self.position)


def menu_gui(inp_master=None):
    master = inp_master
    if not master:
        master = Master()
    garden = GardenApp(master)
    garden.main_loop()


if __name__ == "__main__":
    menu_gui()
