# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 11:23:40 2021

@author: Kam
"""
import pygame
from utils import load_sprite, get_random_position, print_text
from models import Spacefighter, Asteroid

class Spaceasteroids:
    MIN_ASTEROID_DISTANCE = 150  # create a constant representing an area that has to remain empty to avoid overlaping of 
                                 # asteriods and spacefighter
    
    def __init__(self):
        self.init_pygame()    
        self.screen = pygame.display.set_mode((1600, 900)) # create a window (width,height) to draw and display
        self.bg = load_sprite("space1", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 60)
        self.text = ""
        self.bullets = []
        self.health = 150
        self.visible = True
        self.spacefighter = Spacefighter((800, 450), self.bullets.append)
        self.asteroids = []  
        for _ in range(20):   # set how many asteroid display on screen 
            while True:
                position = get_random_position(self.screen)
                if (position.distance_to(self.spacefighter.position) > self.MIN_ASTEROID_DISTANCE):  # check if position of asteroid is larger than minimal asteroid distance
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append))  # add the callback to each newly created asteroid in the constructor  
                
   

    def main_loop(self): 
        while True:
            self.handle_input()
            self.process_game_logic()
            self.draw()
        

    def init_pygame(self):
        pygame.init()     #initialize pygame
        pygame.display.set_caption("Spacefighter vs Asteroids")  # give the window a caption

   
    def handle_input(self):
        for event in pygame.event.get():    # when requested, the program to end by clicking Close or Escape key
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
            elif (self.spacefighter and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                self.spacefighter.shoot()
        
        is_key_pressed = pygame.key.get_pressed()
        
        if self.spacefighter:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spacefighter.rotate(clockwise=True)           
            elif is_key_pressed[pygame.K_LEFT]:
                self.spacefighter.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spacefighter.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.spacefighter.decelerate()

    
    def process_game_logic(self):
        for game_object in self.get_game_objects():
            game_object.move(self.screen)
        
       
        if self.spacefighter:            
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spacefighter):  # when asteroids hit spacefighter,
                    self.health -= 1                          # health level reduces
                    if self.health == 0:                      # when health level reaches zero, game over
                        self.spacefighter = None
                        self.text = "Game Over. You Lost!"
                        break
                   

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):   # whenever a collision is detected between a bullet and an asteroid, both will be removed
                    #self.asteroids.bomb_sound.play()    
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()       # when asteroids are large and medium size, they split
                    break
            
        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):  # remove bullets as soon as they leave the screen
                self.bullets.remove(bullet)

        if not self.asteroids and self.spacefighter:
            self.text = "Congrat. You won!"
    
    def draw(self):
        self.screen.blit(self.bg, (0,0))   # set the screen to be background
        for game_object in self.get_game_objects():
            game_object.draw(self.screen) 
        if self.visible:
            pygame.draw.rect(self.screen, (255,0,0), (50, 50, 150, 10))    # draw health bar
            pygame.draw.rect(self.screen, (0,255,0), (50, 50, self.health, 10))  # display current health status 
            if self.health == 0:   # when health = 0, health bar disappears
                self.visible = False
        if self.text:
            print_text(self.screen, self.text, self.font)  
        pygame.display.update()
        self.clock.tick(60) # set the speed of objects move

    def get_game_objects(self):   # a helper method to returns game objects 
        game_objects = [*self.asteroids, *self.bullets]
        if self.spacefighter:
            game_objects.append(self.spacefighter)
        return game_objects