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

def blit_picture_by_harvest(plant, blits: int):
    if blits == 2:
        if plant._harvest_progress >= plant._harvest_max:
            pct = 1
        else:
            pct = 0
    else:
        for el in range(1, blits):
            if plant._harvest_progress >= plant._harvest_max:
                pct = blits - 1
            elif plant._harvest_progress >= plant._harvest_max * el // blits:
                pct = el - 1
            elif plant._harvest_max * 2 // blits > plant._harvest_progress >= 0:
                pct = 0

    return pct
