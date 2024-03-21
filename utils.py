# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 13:59:01 2021

@author: Kam
"""

import random
from pygame.image import load   # import load method
from pygame.math import Vector2
from pygame.mixer import Sound
from pygame import Color


def load_sprite(name, with_alpha=True):
    path = f"{name}.png"
    loaded_sprite = load(path)   # load the image
    
    if with_alpha:     # convert the image to a format better fits the screen
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

def load_sound(name):
    path = f"{name}.wav"
    return Sound(path)  # load sound effect
    
def wrap_position(position, surface):
    x, y = position
    w, h = surface.get_size()
    return Vector2(x % w, y % h)

def get_random_position(surface):
    return Vector2(
        random.randrange(surface.get_width()),   # get random set of coordinates on a given surface to place asteriods
        random.randrange(surface.get_height()),
        )

def get_random_velocity(min_speed, max_speed): 
    speed = random.randint(min_speed, max_speed)  # generate random value between min_speed and max_speed for asteroids
    angle = random.randrange(0, 360)        # generate random angle between 0 and 360 degree for asteroids
    return Vector2(speed, 0).rotate(angle)

def print_text(surface, text, font, color=Color("tomato")):
    text_surface = font.render(text, False, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    surface.blit(text_surface, rect)