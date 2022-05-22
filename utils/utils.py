import random


from pygame import Color
from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound


def load_sprite(name, with_alpha=True):
    path = f"assetes/sprites/{name}"
    loaded_sprite = load(path)

    if with_alpha:
        return loaded_sprite.convert_alpha()
    return loaded_sprite.convert()

def load_sound(name):
    return Sound(f"assetes/sounds/{name}")
