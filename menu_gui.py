import pygame
import pygame_menu

from Master import Master
from utils.utils import load_sound, load_sprite


class PlantObject:
    pass


class GardenApp:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((1200, 800))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)

        self.warehouse_background = load_sprite("warehouse_background.jpg")

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
            self._warehouse
        )
        self.menu.add.button(
            "Exit",
            pygame_menu.events.EXIT
        )

########
    def _main_garden(self):
        self.menu.disable()

    def _warehouse(self):
        self.menu.disable()

    def _do_step(self):
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
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pass
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


def main():
    garden = GardenApp()
    garden.main_loop()


if __name__ == "__main__":
    main()
