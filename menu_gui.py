import pygame
from pygame.math import Vector2
import pygame_menu

from Master import Master
from utils.utils import load_sound, load_sprite, blit_picture_by_harvest


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
        self.poppy_sprites = tuple(load_sprite(f"poppy/Poppy_Stage_{n}.png") for n in range(1, 5 + 1))
        self.violet_sprites = tuple(load_sprite(f"sunflower/Sunflower_Stage_{n}.png") for n in range(1, 5 + 1))
        self.rose_sprites = tuple(load_sprite(f"summer_spangle/Summer_Spangle_Stage_{n}.png") for n in range(1, 5 + 1))
        self.pine_sprites = tuple(load_sprite(f"pine/Pine_Stage_{n}.png") for n in range(1, 5 + 1))
        self.oak_sprites = tuple(load_sprite(f"oak/Oak_Stage_{n}.png") for n in range(1, 5 + 1))
        self.palm_sprites = tuple(load_sprite(f"palm/Palm_Stage_{n}.png") for n in range(1, 3 + 1))
        self.orange_sprites = tuple(load_sprite(f"orange/Orange_Stage_{n}.png") for n in range(1, 6 + 1))

        # List for garden plants
        self.master = master
        self.plants_list = [[] for _ in range(5)]

        self.theme = pygame_menu.themes.THEME_DARK.copy()
        self.theme.background_color = (0, 0, 0, 180)

        # Warehouse
        self.warehouse_theme = pygame_menu.themes.THEME_GREEN.copy()
        self.warehouse_menu = pygame_menu.Menu(
            title="WAREHOUSE",
            enabled=False,
            width=600,
            height=600,
            theme=self.warehouse_theme
        )

        # Statistics
        self.statistics_theme = pygame_menu.themes.THEME_BLUE.copy()
        self.statistics_menu = pygame_menu.Menu(
            title="STATISTICS",
            enabled=False,
            width=600,
            height=450,
            theme=self.theme,
            onclose=self._back_to_menu
        )

        # Main Menu
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
            "STEP",
            self._do_step
        )
        self.menu.add.button(
            "GARDEN",
            self._main_garden
        )
        self.menu.add.button(
            "WAREHOUSE",
            self._warehouse_menu
        )
        self.menu.add.button(
            "STATISTICS",
            self._statistics_menu
        )
        self.menu.add.button(
            "EXIT",
            pygame_menu.events.EXIT
        )

        # Garden menu
        self.garden_menu_theme = pygame_menu.themes.THEME_DARK.copy()
        # self.garden_menu_theme.background_color = (0, 0, 0, 180)
        self.garden_menu = pygame_menu.Menu(
            title="Garden",
            width=200,
            height=800,
            position=(1000, 0, False),
            theme=self.garden_menu_theme
        )
        
        do_step_button = self.garden_menu.add.button(
            "DO STEP",
            self._do_step,
        )
        do_step_button.translate(0, -270)
        
        plant_button = self.garden_menu.add.button(
            "PLANT",
            self._plant
        )
        plant_button.translate(0, -260)
        
        delete_button = self.garden_menu.add.button(
            "GARDENBED",
            self._choose_garden
        )
        delete_button.translate(0, -250)

        menu_button = self.garden_menu.add.button(
            "MENU",
            self._call_main_menu
        )
        menu_button.translate(0, -240)
        
        # New plant menu
        self.__new_plant_name: str = "Poppy"
        self.__new_plant_position: int = 0
        self.planting_menu = pygame_menu.Menu(
            title="",
            enabled=False,
            width=600,
            height=400
        )

        # Garden selector menu
        self.__gardenbed_number: int = None
        self.garden_selector_menu = pygame_menu.Menu(
            title="",
            enabled=False,
            width=600,
            height=600
        )

        # Cut plant
        self.__cut_plant_number: int = 0

        # Detail gardenbed statistics menu
        self.statistics_menu = pygame_menu.Menu(
            title="",
            enabled=False,
            width=600,
            height=600,
            onclose=self._main_garden
        )

        self._do_step()

########
    def _statistics_menu(self):
        self.menu.disable()
        self.garden_menu.disable()
        self.statistics_menu = pygame_menu.Menu(
            title="STATISTICS",
            enabled=False,
            width=600,
            height=450,
            theme=self.theme,
            onclose=self._back_to_menu
        )

        for plant, value in self.master.avg_statistics().items():
            self.statistics_menu.add.button(
                f"{plant}: {value}"
            )

        self.statistics_menu.add.button(
            "Back",
            self._back_to_menu
        )

        self.statistics_menu.enable()

    def _warehouse_menu(self):
        self.menu.disable()
        self.garden_menu.disable()
        # self.warehouse_theme = pygame_menu.themes.THEME_GREEN.copy()
        self.warehouse_menu = pygame_menu.Menu(
            title="Warehouse",
            enabled=False,
            width=600,
            height=600,
            theme=self.theme,
            onclose=self._back_to_menu
        )

        for plant, count in self.master.warehouse.items():
            self.warehouse_menu.add.button(
                f"{plant}: {count}"
            )
        self.warehouse_menu.add.button(
            "Back",
            self._back_to_menu
        )

        self.warehouse_menu.enable()

    def _plant(self):
        """Garden menu option for create new plant."""
        self.garden_menu.disable()
        self.planting_menu = pygame_menu.Menu(
            title="",
            enabled=False,
            width=600,
            height=400,
            onclose=self._main_garden
        )
        self.planting_menu.add.selector(
            title="PLANT",
            items=[
                ("POPPY", "Poppy"),
                ("ROSE", "Rose"),
                ("VIOLET", "Violet"),
                ("APPLE", "Apple"),
                ("ORANGE", "Orange"),
                ("PINEAPPLE", "Pineapple"),
                ("CACTUS", "Cactus"),
                ("OAK", "Oak"),
                ("PINE", "Pine"),
                ("CARROT", "Carrot"),
                ("POTATO", "Potato"),
                ("TOMATO", "Tomato")
            ],
            default=0,
            onchange=self._plant_name,
            onreturn=self._plant_name
        )

        self.planting_menu.add.selector(
            title="GARDENT",
            items=[
                ("1", 0),
                ("2", 1),
                ("3", 2),
                ("4", 3),
                ("5", 4)
            ],
            default=0,
            onchange=self._plant_position,
            onreturn=self._plant_position
        )

        self.planting_menu.add.button(
            "PLANT",
            self._add_new_plant
        )

        self.planting_menu.add.button(
            "CANCEL",
            self._main_garden
        )

        self.planting_menu.enable()

    def _plant_name(self, value, plant_name):
        """Plant name getter."""
        self.__new_plant_name = plant_name
        print(self.__new_plant_name)

    def _plant_position(self, value, plant_position):
        """Plant position getter."""
        self.__new_plant_position = plant_position
        print(self.__new_plant_position)

    def _add_new_plant(self):
        """Add selected plant to selected gardenbed in master."""
        if self.__new_plant_name and self.__new_plant_position >= 0:
            self.master.grow_plant(self.__new_plant_name, self.__new_plant_position)
            self._main_garden()

    def _choose_garden(self):
        """Window with garden selector."""
        self.garden_menu.disable()
        self.garden_selector_menu = pygame_menu.Menu(
            title="",
            enabled=False,
            width=600,
            height=600,
            onclose=self._main_garden
        )
        
        self.garden_selector_menu.add.selector(
            title="GARDEN NUMBER",
            items=[
                ("NONE", None),
                ("1", 0),
                ("2", 1),
                ("3", 2),
                ("4", 3),
                ("5", 4)
            ],
            default=0,
            onchange=self._selected_garden,
            onreturn=self._selected_garden
        ).translate(0, -100)

        self.garden_selector_menu.add.selector(
            title="PLANT NUMBER",
            items=[
                ("NO", None),
                ("1", 0),
                ("2", 1),
                ("3", 2),
                ("4", 3),
                ("5", 4)
            ],
            default=0,
            onchange=self._cut_plant_number,
            onreturn=self._cut_plant_number
        ).translate(0, -50)
        self.garden_selector_menu.add.button(
            "CUT PLANT",
            self._cut_plant
        ).translate(0, -40)

        self.garden_selector_menu.add.button(
            "DETAIL STATISTICS",
            self._show_detail_statistics_menu
        )

        self.garden_selector_menu.add.button(
            "WEED",
            self._weed_plants
        )

        self.garden_selector_menu.add.button(
            "WATER THE PLANTS",
            self._water_the_plants
        )

        self.garden_selector_menu.add.button(
            "CANCEL",
            self._main_garden
        ).translate(0, 50)

        self.garden_selector_menu.enable()

    def _selected_garden(self, value, selected_garden):
        """Selected garden number getter."""
        self.__gardenbed_number = selected_garden
        print(self.__gardenbed_number)

    def _cut_plant_number(self, value, selected_plant):
        """Selected plant number getter."""
        self.__cut_plant_number = selected_plant
        print(self.__cut_plant_number)

    def _cut_plant(self):
        """Delete plant by number."""
        if self.__cut_plant_number >= 0 and self.__gardenbed_number >= 0:
            self.master.delete_plant(
                self.__gardenbed_number, self.__cut_plant_number
            )

    def _show_detail_statistics_menu(self):
        """Run window with detail statistics about the plants 
        in choosen gardenbed."""
        self.garden_menu.disable()
        self.statistics_menu = pygame_menu.Menu(
            title="",
            enabled=False,
            width=600,
            height=600,
            onclose=self._main_garden
        )
        self.statistics_menu.add.label(
            "DETAIL STATISTICS:"
        )
        if self.__gardenbed_number is None:
            self._main_garden()
            return
        gbed = self.master.gardenbed[self.__gardenbed_number].garden
        for n, gb in enumerate(gbed):
            if gb not in ["Ambrosia", "Dandelion", "Cornflower"]:
                self.statistics_menu.add.label(
                    f"{n + 1}.Name: {gb.name}\n"
                    f"  Harvest progress: {round((gb.harvest_max / gb.harvest_progress), 2)}\n"
                    f"  Live: {round((gb.live_max / gb.live), 2)}\n"
                    f"  Immunity: {round(gb.immunity, 2)}\n"
                    f"  Ills list: {gb.ills if gb.ills else None}\n",
                    align=pygame_menu.locals.ALIGN_LEFT,
                    margin=(0, -1)
                )
        
        self.statistics_menu.add.button(
            "CLOSE",
            self._main_garden
        )

        self.statistics_menu.enable()

    def _weed_plants(self):
        if self.__gardenbed_number:
            self.master.weed(self.__gardenbed_number)

    def _water_the_plants(self):
        if self.__gardenbed_number:
            self.master.water(self.__gardenbed_number)

    def _call_main_menu(self):
        self.garden_menu.disable()
        self.menu.enable()

    def _do_step(self):
        """Do step and update garden."""
        self.master.step()
        self.plants_list = [[] for _ in range(5)]

    def _main_garden(self):
        """Return to garden."""
        if self.menu.is_enabled():
            self.menu.disable()
        if self.planting_menu.is_enabled():
            self.planting_menu.disable()
        if self.garden_selector_menu.is_enabled():
            self.garden_selector_menu.disable()
        self.garden_menu.enable()

    def _back_to_menu(self):
        """Return to main menu."""
        if self.warehouse_menu.is_enabled():
            self.warehouse_menu.disable()
        if self.statistics_menu.is_enabled():
            self.statistics_menu.disable()
        self.menu.enable()
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

        if self.garden_selector_menu.is_enabled():
            self.garden_selector_menu.update(pygame.event.get())

        if self.planting_menu.is_enabled():
            self.planting_menu.update(pygame.event.get())

        if self.statistics_menu.is_enabled():
            self.statistics_menu.update(pygame.event.get())

        if self.warehouse_menu.is_enabled():
            self.warehouse_menu.update(pygame.event.get())

        if self.statistics_menu.is_enabled():
            self.statistics_menu.update(pygame.event.get())

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
                self._main_garden()

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
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.poppy_sprites[blit_picture_by_harvest(plant, len(self.poppy_sprites))]
                                ))
                            case "Rose":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.rose_sprites[blit_picture_by_harvest(plant, len(self.rose_sprites))]
                                ))
                            case "Violet":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.violet_sprites[blit_picture_by_harvest(plant, len(self.violet_sprites))]
                                ))
                            case "Pineapple":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.pineapple_sprites[blit_picture_by_harvest(plant, len(self.pineapple_sprites))]
                                ))
                            case "Apple":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.apple_sprites[blit_picture_by_harvest(plant, len(self.apple_sprites))]
                                ))
                            case "Orange":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.orange_sprites[blit_picture_by_harvest(plant, len(self.orange_sprites))]
                                ))
                            case "Cactus":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.palm_sprites[blit_picture_by_harvest(plant, len(self.palm_sprites))]
                                ))
                            case "Oak":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.oak_sprites[blit_picture_by_harvest(plant, len(self.oak_sprites))]
                                ))
                            case "Pine":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.pine_sprites[blit_picture_by_harvest(plant, len(self.pine_sprites))]
                                ))
                            case "Carrot":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.carrot_sprites[blit_picture_by_harvest(plant, len(self.carrot_sprites))]
                                ))
                            case "Potato":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.potato_sprites[blit_picture_by_harvest(plant, len(self.potato_sprites))]
                                ))
                            case "Tomato":
                                self.plants_list[gbed_num].append(PlantObject(
                                    (x_pos[plant_num], y_pos[gbed_num]),
                                    self.tomato_sprites[blit_picture_by_harvest(plant, len(self.tomato_sprites))]
                                ))

    def _draw(self):
        self.screen.fill((0, 75, 25))

        if self.menu.is_enabled():
            self.screen.blit(self.main_menu_background, (0, 0))
            self.menu.draw(self.screen)

        if self.planting_menu.is_enabled():
            self.planting_menu.draw(self.screen)

        if self.garden_selector_menu.is_enabled():
            self.garden_selector_menu.draw(self.screen)

        if self.statistics_menu.is_enabled():
            self.statistics_menu.draw(self.screen)

        if self.warehouse_menu.is_enabled():
            self.screen.blit(self.main_menu_background, (0, 0))
            self.warehouse_menu.draw(self.screen)

        if self.statistics_menu.is_enabled():
            self.screen.blit(self.main_menu_background, (0, 0))
            self.statistics_menu.draw(self.screen)

        if self.garden_menu.is_enabled():
            self.garden_menu.draw(self.screen)
            self.screen.blit(self.garden_background, (0, 0))
            
            for gardenbed in self.plants_list:
                for plant in gardenbed:
                    if plant:
                        plant.draw(self.screen)

        pygame.display.flip()
        self.clock.tick(20)


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
