import pygame
from pygame.math import Vector2
import pygame_menu

from Master import Master
from utils.utils import load_sound, load_sprite


class PlantObject:
    def __init__(self, position, sprite):
        self.position = Vector2(position)
        self.sprite = sprite

    def draw(self, surface):
        surface.blit(self.sprite, self.position)


class GardenApp:
    def __init__(self, master):
        self._init_pygame()
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)

        self.warehouse_background = load_sprite("warehouse_background.jpg")

        self.master = master
        self.plants_list = [[] for _ in range(5)]

        # Warehouse
        self.warehouse_theme = pygame_menu.themes.THEME_GREEN.copy()
        self.warehouse_menu = pygame_menu.Menu(
            title="Warehouse",
            width=800,
            height=600,
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
            width=800,
            height=600,
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

        # Menu
        self.theme = pygame_menu.themes.THEME_DARK.copy()
        # self.theme.background_color = (0, 0, 0, 180)
        self.menu = pygame_menu.Menu(
            title="Menu",
            width=800,
            height=600,
            theme=self.theme
        )
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
            self._sort_plants
        )
        self.menu.add.button(
            "Exit",
            pygame_menu.events.EXIT
        )

########
    def _do_step(self):
        self.master.step()

    def _main_garden(self):
        self.menu.disable()

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

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            # do step
            elif event.type == pygame.KEYDOWN and \
                event.key == pygame.K_SPACE and not self.menu.is_enabled():
                self._do_step()
            # call menu
            elif event.type == pygame.KEYDOWN and \
                event.key == pygame.K_ESCAPE and not self.menu.is_enabled():
                self.menu.enable()

    def _process_game_logic(self):
        pass

    def _draw(self):
        self.screen.fill((105, 219, 17))

        if self.menu.is_enabled():
            self.menu.mainloop(self.screen)

        pygame.display.flip()
        self.clock.tick(60)


def menu_gui(inp_master=None):
    master = inp_master
    if not master:
        master = Master()
    garden = GardenApp(master)
    garden.main_loop()


if __name__ == "__main__":
    menu_gui()
