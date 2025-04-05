import pygame
import math
import random

class Enemy_one:
    def __init__(self, x, y):
        # Posição inicial do inimigo
        self.x = random.randint(0, x)
        self.y = random.randint(0, y)
        self.life = 10
        self.speed = 1.0  # Aumentado para compensar o tamanho maior
        
        self.invulnerable = False
        self.invulnerable_time = 1
        self.last_hit_time = 0
        
        # Animação com escala
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"sprites/zombie/andando/frame{i}.png").convert_alpha(),
                (50, 50)
            )
            for i in range(10)
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1  # Diminua para animação mais lenta

        # Máscara do inimigo baseada no primeiro frame
        self.mask = pygame.mask.from_surface(self.frames[0])

    def move(self, player, mask):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        
        
        self.moving_left = False
        if dx < 0:
            self.moving_left = True
        elif dx> 0:
            self.moving_left = False
            
        

        if distance > 0:
            dx /= distance
            dy /= distance

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Posições futuras para checar colisão
        future_pos_x = (int(new_x) - 32, int(self.y) - 32)
        future_pos_y = (int(self.x) - 32, int(new_y) - 32)

        if mask.overlap(self.mask, future_pos_x) is None:
            self.x = new_x
        if mask.overlap(self.mask, future_pos_y) is None:
            self.y = new_y

    def draw(self, game_window, offset_x, offset_y):
        self.frame_timer += self.frame_speed
        if self.frame_timer >= 1:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = 0

        frame_image = self.frames[self.current_frame]

        if self.moving_left:
            frame_image = pygame.transform.flip(frame_image, True, False)

        draw_rect = frame_image.get_rect(center=(int(self.x - offset_x), int(self.y - offset_y)))
        game_window.blit(frame_image, draw_rect.topleft)

    def update_invulnerability(self, current_time):
        if self.invulnerable:
            if current_time - self.last_hit_time >= self.invulnerable_time:
                self.invulnerable = False

    def make_invulnerable(self, current_time):
        self.invulnerable = True
        self.last_hit_time = current_time
