import pygame
import math

class Basic_attack:
    def __init__(self):
        self.color = (0, 0, 100)
        self.radius = 60
        self.damage = 10
        self.time = 0
        self.cooldown = 2

    def increase_range(self, increase):
        self.radius *= increase
        print(self.radius)
    
    def check_hit(self, target_x, target_y, player_x, player_y, elapsed_time):
        distance = math.sqrt((player_x - target_x) ** 2 + (player_y - target_y) ** 2)

        if distance <= self.radius and elapsed_time % 2 == 0:
            return -self.damage
        else:
            return 0

    def draw(self, game_window, x, y, elapsed_time):
        if elapsed_time % self.cooldown == 0 and elapsed_time != 0:
            pygame.draw.circle(game_window, self.color, (x, y), self.radius, width=5)
        self.time = elapsed_time

class Book:
    def __init__(self):
        self.color = (255, 0, 100)
        self.radius = 60
        self.size = 10
        self.damage = 1
        self.time = 0
        self.cooldown = 2

    def check_hit(self, target_x, target_y, player_x, player_y, elapsed_time):
        distance = math.sqrt((player_x - target_x) ** 2 + (player_y - target_y) ** 2)

        if distance <= self.radius and elapsed_time % 2 == 0:
            return -self.damage
        else:
            return 0

    def lauch_projectile(self, x, y, elapsed_time):
        if elapsed_time % self.cooldown == 0 and elapsed_time != 0:
            return x, y
        else:
            return 0, 0
        

    def draw(self, game_window, x, y, elapsed_time):
        if elapsed_time % self.cooldown == 0 and elapsed_time != 0:

            pygame.draw.rect(game_window, self.color, pygame.Rect(x, y, self.size, self.size))
            #pygame.draw.rect(game_window, self.color, (x, y), self.size)
        self.time = elapsed_time