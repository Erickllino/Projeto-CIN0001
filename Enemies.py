import pygame
import math
import random

class Enemy_one:
    def __init__(self, x, y):
        # Posição inicial do inimigo
        self.x = random.randint(0, x)
        self.y = random.randint(0, y)
        self.life = 10
        self.speed = 0.5
        
        self.invulnerable = False
        self.invulnerable_time = 1
        self.last_hit_time = 0

    def move(self, player, mask):
        # Faz o algoritmo de movimentação do inimigo
        # Aqui ele se move em direção ao jogador diretamente
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 0:
            dx /= distance
            dy /= distance

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Check collision with map, a hitbox é um quadrado de 10x10 (5*2, 5*2)
        if not mask.overlap_area(pygame.mask.Mask((5 * 2, 5 * 2), fill=True), (new_x - 5, self.y - 5)):
            self.x = new_x
        if not mask.overlap_area(pygame.mask.Mask((5 * 2, 5 * 2), fill=True), (self.x - 5, new_y - 5)):
            self.y = new_y

    def draw(self, game_window, offset_x, offset_y):

        # Desenho do inimigo, se for trocar por uma imagem, use game_window.blit(imagem, (int(self.x - offset_x), int(self.y - offset_y)))
        pygame.draw.circle(game_window, (255, 0, 0), (int(self.x - offset_x), int(self.y - offset_y)), 5)

    # Replace the get_invunerable method with this:
    def update_invulnerability(self, current_time):
        if self.invulnerable:
            # Check if invulnerability period has ended
            if current_time - self.last_hit_time >= self.invulnerable_time:
                self.invulnerable = False
                
    def make_invulnerable(self, current_time):
        self.invulnerable = True
        self.last_hit_time = current_time