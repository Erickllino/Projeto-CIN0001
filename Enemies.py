import pygame
import math
import random

class Enemy_one:
    def __init__(self, x, y):
        self.x = random.randint(0, x)
        self.y = random.randint(0, y)
        self.life = 10
        self.speed = 0.5

    def move(self, player, mask):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx /= distance
            dy /= distance

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        if not mask.overlap_area(pygame.mask.Mask((5 * 2, 5 * 2), fill=True), (new_x - 5, new_y - 5)):
            self.x = new_x
            self.y = new_y

    def draw(self, game_window, offset_x, offset_y):
        pygame.draw.circle(game_window, (255, 0, 0), (int(self.x - offset_x), int(self.y - offset_y)), 5)