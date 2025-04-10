import pygame
import math
import random

class Enemy:
    def __init__(self, x, y, sprite_path, frame_counts, scale, life=10, speed=1.0, damage=1, death_frame_speed=0.1):
        self.x = random.randint(0, x)
        self.y = random.randint(0, y)
        self.life = life
        self.speed = speed
        self.damage = damage

        self.invulnerable = False
        self.invulnerable_time = 1
        self.last_hit_time = 0

        # Carrega animações
        self.frames = self.load_frames(f"{sprite_path}/andando", frame_counts['andando'], scale)
        self.death_frames = self.load_frames(f"{sprite_path}/morrendo", frame_counts['morrendo'], scale)
        self.atack_frames = self.load_frames(f"{sprite_path}/atacando", frame_counts['atacando'], scale)

        self.current_frame = 0
        self.frame_timer = 0
        self.frame_speed = 0.1

        self.is_dying = False
        self.death_frame_index = 0
        self.death_frame_timer = 0
        self.death_frame_speed = death_frame_speed  
        self.marked_for_removal = False 

        self.atack = False
        self.atack_frame_index = 0
        self.atack_frame_timer = 0
        self.atack_frame_speed = 0.1
        self.atack_sound = pygame.mixer.Sound("sprites/sons_effects/zombie_atack.wav")

        self.mask = pygame.mask.from_surface(self.frames[0])
        self.moving_left = False

    def load_frames(self, path, count, scale):
        return [
            pygame.transform.scale(pygame.image.load(f"{path}/frame{i}.png").convert_alpha(), scale)
            for i in range(count)
        ]

    def move(self, player, mask):
        if self.is_dying or self.atack:
            return
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        self.moving_left = dx < 0

        if distance < 20:
            self.atack = True
            return

        if distance > 0:
            dx /= distance
            dy /= distance
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        future_pos_x = (int(new_x) - 32, int(self.y) - 32)
        future_pos_y = (int(self.x) - 32, int(new_y) - 32)

        if mask.overlap(self.mask, future_pos_x) is None:
            self.x = new_x
        if mask.overlap(self.mask, future_pos_y) is None:
            self.y = new_y

    def draw(self, game_window, offset_x, offset_y):
        if self.is_dying:
            frame_image = self.death_frames[min(self.death_frame_index, len(self.death_frames) - 1)]
        elif self.atack:
            frame_image = self.atack_frames[min(self.atack_frame_index, len(self.atack_frames) - 1)]
        else:
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
        if self.invulnerable and current_time - self.last_hit_time >= self.invulnerable_time:
            self.invulnerable = False

    def make_invulnerable(self, current_time):
        self.invulnerable = True
        self.last_hit_time = current_time


    def update_death(self, current_time):
        if self.is_dying:
            self.death_frame_timer += self.death_frame_speed
            if self.death_frame_timer >= 1:
                self.death_frame_index += 1
                self.death_frame_timer = 0
                if self.death_frame_index >= len(self.death_frames):
                    self.marked_for_removal = True

    def update_atack(self, current_time, player):
        if self.atack:
            self.atack_frame_timer += self.atack_frame_speed
            if self.atack_frame_timer >= 1:
                self.atack_frame_index += 1
                self.atack_frame_timer = 0
                if self.atack_frame_index >= len(self.atack_frames):
                    self.atack = False
                    self.atack_frame_index = 0
                    self.atack_sound.play()
                    distance = math.hypot(player.x - self.x, player.y - self.y)
                    if distance < 20 and not player.invulnerable:
                        player.health -= self.damage
                        player.player_gets_damaged_sound.play()
                        player.player_gets_damaged_sound.set_volume(0.5)  # Reduz o som
                        player.make_invulnerable(current_time)
                        
class ZombieOne(Enemy):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            sprite_path="sprites/zombie/zombie1",
            frame_counts={"andando": 10, "morrendo": 6, "atacando": 5},
            scale= (64,64),
            life=10,
            speed=1.0,
            damage=10
        )

class ZombieTwo(Enemy):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            sprite_path="sprites/zombie/zombie2",
            frame_counts={"andando": 10, "morrendo": 5, "atacando": 4},
            scale= (98,98),
            life=20,
            speed=2,
            damage=4
        )

class ZombieBoss(Enemy):
    def __init__(self, x, y):
        super().__init__(
            x, y,
            sprite_path="sprites/zombie/zombieboss",
            frame_counts={"andando": 10, "morrendo": 6, "atacando": 5},
            scale=(130, 130),  
            life=100,        
            speed=0.8,        
            damage=20,        
            death_frame_speed=0.2  
        )
        self.radius = 50  
        self.frame_speed = 0.1
        self.atack_frame_speed = 0.3
        self.radius = 60
        self.attack_cooldown = 1.3 

    def move(self, player, mask):
        if self.is_dying or self.atack:
            return

        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        self.moving_left = dx < 0

        if distance < 75:
            self.atack = True
            return

        if distance > 0:
            dx /= distance
            dy /= distance

        # Movimento base
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        frame_width = self.frames[0].get_width()
        frame_height = self.frames[0].get_height()
        offset_x = frame_width // 2
        offset_y = frame_height // 2

        future_pos_x = (int(new_x) - offset_x, int(self.y) - offset_y)
        future_pos_y = (int(self.x) - offset_x, int(new_y) - offset_y)

        moved_x = False
        moved_y = False

        if mask.overlap(self.mask, future_pos_x) is None:
            self.x = new_x
            moved_x = True

        if mask.overlap(self.mask, future_pos_y) is None:
            self.y = new_y
            moved_y = True

        # caso fique preso, tenta ajustar com ângulo aleatório
        if not moved_x and not moved_y:
            angle_offset = random.uniform(-math.pi / 4, math.pi / 4)  
            angle = math.atan2(dy, dx) + angle_offset
            dodge_dx = math.cos(angle)
            dodge_dy = math.sin(angle)

            alt_x = self.x + dodge_dx * self.speed
            alt_y = self.y + dodge_dy * self.speed

            future_alt_x = (int(alt_x) - offset_x, int(self.y) - offset_y)
            future_alt_y = (int(self.x) - offset_x, int(alt_y) - offset_y)

            if mask.overlap(self.mask, future_alt_x) is None:
                self.x = alt_x
            if mask.overlap(self.mask, future_alt_y) is None:
                self.y = alt_y
