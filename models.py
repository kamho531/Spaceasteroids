# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 15:43:07 2021

@author: Kam
"""

from pygame.math import Vector2
from pygame.transform import rotozoom  # module reponsible for scaling and rotating images

from utils import load_sprite, wrap_position, get_random_velocity, load_sound

UP = Vector2(0, -1)  # negative value actually points upwards


class GameObject:
    def __init__(self, position, sprite, velocity):   # create GameObject class needs 3 arguements
        self.position = Vector2(position)    # centre of the object
        self.sprite = sprite                # the image used to draw the object
        self.velocity = Vector2(velocity)   # update the position of the object each frame
        self.radius = sprite.get_width() / 2    # calculate the raduis as hald the width of the sprite image
        
    def draw(self, surface):   # define draw(), which will draw the object's sprite on the surface passed as an argument
        blit_position = self.position - Vector2(self.radius)  # calculates the correct position for blitting the image
        surface.blit(self.sprite, blit_position)  # uses the newly calculated blit position to put your object’s sprite in a correct place on the given surface
        
    def move(self, surface):   # defines move(). It will update the position of the game object.
        self.position = wrap_position(self.position + self.velocity, surface)   # adds the velocity to the position and gets an updated position vector as a result
        
    def collides_with(self, other_obj):  # defines the collides_with() method, that will be used to detect collisions
        distance = self.position.distance_to(other_obj.position) # calculates the distance between two objects by using Vector2.distance_to()
        return distance < self.radius + (other_obj.radius / 5) # checks if that distance is smaller than the sum of the objects’ radiuses. If so, the objects collide 
    
    
class Spacefighter(GameObject):
    MANEUVERABILITY = 4  # determines how fast your spaceship can rotate
    ACCELERATION = 1.50  # adding the current velocity to the current position of the spaceship
    DECELERATION = 1.50
    BULLET_SPEED = 6
    
    def __init__(self, position, create_bullet_callback):
        self.create_bullet_callback = create_bullet_callback
        self.laser_sound = load_sound("assets/laser")
        # make a copy of the original UP vector
        self.direction = Vector2(UP)
        super().__init__(position, load_sprite("assets/spacefighter8"), Vector2(0)) # calls the GameObject constructor with a specific image and a zero velocity
        
    def rotate(self, clockwise=True):
        if clockwise:
            sign = 1
        else:
            sign = -1
        angle = self.MANEUVERABILITY * sign  # change the direction by rotating it either clockwise or counterclockwise
        self.direction.rotate_ip(angle) # method of the Vector2 class rotates it in place by a given angle in degrees

    def accelerate(self):
        self.velocity = self.direction * self.ACCELERATION
        
    def decelerate(self):
        self.velocity = -self.direction * self.DECELERATION

    def draw(self, surface):
        angle = self.direction.angle_to(UP)  # method of the Vector2 class to calculate the angle by which one vector needs to be rotated in order to point in the same direction as the other vector
        rotated_surface = rotozoom(self.sprite, angle, 1.0) # rotates the sprite, takes the original image, the angle by which it should be rotated, and the scale applied to the sprite. Since we don’t want to change the size, so keep the scale as 1.0
        rotated_surface_size = Vector2(rotated_surface.get_size()) #  recalculate the blit position
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position) # uses the newly calculated blit position to put the image on the screen

    def shoot(self):
        bullet_velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity) 
        self.create_bullet_callback(bullet)
        self.laser_sound.play()

        
class Asteroid(GameObject):
    def __init__(self, position, create_asteroid_callback, size=3):
        self.create_asteroid_callback = create_asteroid_callback  # an asteroid to be able to create new asteroids
        self.size = size
        self.bomb_sound = load_sound("assets/Bomb2")
        size_to_scale = {3: 1.0, 2: 0.5, 1: 0.25}    # set the scale of asteroid to split 
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("assets/asteroid"), 0, scale)  # load the image of asteroid
        super().__init__(position, sprite, get_random_velocity(1, 3))
        
    def split(self):
        self.bomb_sound.play()
        if self.size > 1: # create two new asteroids at the same position as the current one           
            for _ in range(2):
                asteroid = Asteroid(self.position, self.create_asteroid_callback, self.size - 1)
                self.create_asteroid_callback(asteroid)

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("assets/bullet1"), velocity) 
        
    def move(self, surface):
        self.position = self.position + self.velocity  # disabling the wrapping only for bullets
        
        