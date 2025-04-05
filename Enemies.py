import pygame
import math
import random

class Enemy_one:
    def __init__(self, x, y):
        self.x = random.randint(0, x)
        self.y = random.randint(0, y)
        self.life = 10
        self.speed = 1.0

        self.invulnerable = False
        self.invulnerable_time = 1
        self.last_hit_time = 0

        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"sprites/zombie/andando/frame{i}.png").convert_alpha(),
                (64, 64)
            )
            for i in range(10)
        ]
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1

        # Máscara gerada a partir do centro do frame (assumindo alinhamento 64x64)
        self.mask = pygame.mask.from_surface(self.frames[0])
        self.rect = self.frames[0].get_rect(center=(self.x, self.y))

    def move(self, player, mask):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)

        if distance > 0:
            dx /= distance
            dy /= distance

        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        future_rect_x = self.mask.get_rect(center=(int(new_x), int(self.y)))
        future_rect_y = self.mask.get_rect(center=(int(self.x), int(new_y)))

        if mask.overlap(self.mask, (future_rect_x.x, future_rect_x.y)) is None:
            self.x = new_x
        if mask.overlap(self.mask, (future_rect_y.x, future_rect_y.y)) is None:
            self.y = new_y

        self.rect.center = (int(self.x), int(self.y))

    def draw(self, game_window, offset_x, offset_y):
        self.frame_timer += self.frame_speed
        if self.frame_timer >= 1:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.frame_timer = 0

        frame_image = self.frames[self.current_frame]
        draw_pos = frame_image.get_rect(center=(int(self.x - offset_x), int(self.y - offset_y)))
        game_window.blit(frame_image, draw_pos.topleft)

    def update_invulnerability(self, current_time):
        if self.invulnerable:
            if current_time - self.last_hit_time >= self.invulnerable_time:
                self.invulnerable = False

    def make_invulnerable(self, current_time):
        self.invulnerable = True
        self.last_hit_time = current_time
