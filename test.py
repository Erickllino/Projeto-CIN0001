import pygame
import random
import math
from weapons import Basic_attack
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Comic Sans MS', 30)

class Player:
    def __init__(self, x, y, radius=10, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.draw_x = 0
        self.draw_y = 0
        self.xp = 0
        self.health = 100
        self.radius = radius
        self.color = color
        self.speed = 4

    def move(self, keys, map_size, mask):
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        new_x = max(self.radius, min(map_size[0] - self.radius, self.x + dx))
        new_y = max(self.radius, min(map_size[1] - self.radius, self.y + dy))

        if not mask.overlap_area(pygame.mask.Mask((self.radius * 2, self.radius * 2), fill=True), (new_x - self.radius, new_y - self.radius)):
            self.x = new_x
            self.y = new_y

    def draw(self, game_window, center, map_size, window_size, offset_x, offset_y):
        if self.x > window_size[0] // 2 and self.x < map_size[0] - window_size[0] // 2:
            draw_x = center[0]
        else:
            draw_x = self.x - offset_x

        if self.y > window_size[1] // 2 and self.y < map_size[1] - window_size[1] // 2:
            draw_y = center[1]
        else:
            draw_y = self.y - offset_y

        self.draw_x = draw_x
        self.draw_y = draw_y
        # draw self
        pygame.draw.circle(game_window, self.color, (int(draw_x), int(draw_y)), self.radius)

"""class Basic_attack:
    def __init__(self):
        self.color = (0, 0, 100)
        self.radius = 60
        self.basic_weapon = True
        self.damage = 1
        self.time = 0

    def check_hit(self, target_x, target_y, player_x, player_y, elapsed_time):
        distance = math.sqrt((player_x - target_x) ** 2 + (player_y - target_y) ** 2)

        if distance <= self.radius and elapsed_time % 2 == 0:
            return -self.damage
        else:
            return 0

    def draw(self, game_window, x, y, elapsed_time):
        if elapsed_time % 2 == 0 and elapsed_time != 0:
            pygame.draw.circle(game_window, self.color, (x, y), self.radius)
        self.time = elapsed_time

    def increase_range(self, increase):
        self.radius += increase
        print(self.radius)"""

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

class Vampire_Cinvivals:
    def __init__(self, w=600, h=600):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Vampire_Cinvivals")
        self.clock = pygame.time.Clock()
        self.Map = pygame.image.load("sprites/map.jpg").convert()  # Resolução da Imagem 2550x3300
        self.mask = pygame.mask.from_threshold(self.Map, (0, 0, 0), (1, 1, 1))  # Cria a máscara de colisão
        self.last_spawn = 0
        self.active_weapons = [Basic_attack]
        self.basic_attack_instance = Basic_attack()  # Instância de Basic_attack para aumentar o raio

    def play_step(self, player, enemies, elapsed_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                # Cria um projétil na posição do jogador em direção ao mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()
                self.projectiles.append(Projectile(player.x, player.y, mouse_x, mouse_y))

        keys = pygame.key.get_pressed()
        player.move(keys, self.Map.get_size(), self.mask)

        self.display.fill((0, 0, 0))
        map_size = self.Map.get_size()
        window_size = self.display.get_size()
        offset_x = max(0, min(map_size[0] - window_size[0], player.x - window_size[0] / 2))
        offset_y = max(0, min(map_size[1] - window_size[1], player.y - window_size[1] / 2))
        self.display.blit(self.Map, (-offset_x, -offset_y))

        player.draw(self.display, (window_size[0] // 2, window_size[1] // 2), map_size, window_size, offset_x, offset_y)

        # Weapons
        for weapon in self.active_weapons:
            weapon_instance = weapon()
            weapon_instance.draw(self.display, player.draw_x, player.draw_y, elapsed_time)
            for enemy in enemies:
                enemy.life += weapon_instance.check_hit(enemy.x, enemy.y, player.x, player.y, elapsed_time)

        # Check Weapon Hit
        for enemy in enemies:
            enemy.life += self.basic_attack_instance.check_hit(enemy.x, enemy.y, player.x, player.y, elapsed_time)

        # Increase Basic_attack range if player XP >= 10
        if player.xp >= 10:
            player.xp = 0
            self.basic_attack_instance.increase_range(10)

        # Spawn Enemies
        if len(enemies) <= 3000:
            spawn_rate = int(1.06173 * (elapsed_time ** 0.6231684))  # Colocar uma fórmula para o aumento de inimigos
        else:
            spawn_rate = 30
        if elapsed_time != self.last_spawn:
            for i in range(spawn_rate):
                while True:
                    spawn_x = random.randint(0, self.Map.get_width())
                    spawn_y = random.randint(0, self.Map.get_height())
                    # Calcular a área visível da tela
                    visible_x_min = player.x - self.display.get_width() // 2
                    visible_x_max = player.x + self.display.get_width() // 2
                    visible_y_min = player.y - self.display.get_height() // 2
                    visible_y_max = player.y + self.display.get_height() // 2
                    # Verificar se a posição de spawn está fora da área visível
                    if not (visible_x_min <= spawn_x <= visible_x_max and visible_y_min <= spawn_y <= visible_y_max):
                        break
                enemies.append(Enemy_one(spawn_x, spawn_y))
                print(f'Number of Enemies: {len(enemies)}, Health {player.health}, XP: {player.xp}, Basic_attack radius: {self.basic_attack_instance.radius}')
                self.last_spawn = elapsed_time
                spawn_rate += 1

        # Move Enemies
        for enemy_one in enemies:
            enemy_one.move(player, self.mask)
            enemy_one.draw(self.display, offset_x, offset_y)

        # Check if enemies hit player
        for enemy_one in enemies:
            distance = math.sqrt((player.x - enemy_one.x) ** 2 + (player.y - enemy_one.y) ** 2)
            if distance < 10:
                player.health -= 1

        # Remove dead Enemies
        for enemy_one in enemies[:]:
            if enemy_one.life <= 0:
                enemies.remove(enemy_one)
                player.xp += 1

        # Mostrar FPS na tela
        fps = int(self.clock.get_fps())
        fps_text = my_font.render(f"FPS: {fps}", True, (0, 0, 255))
        self.display.blit(fps_text, (10, 10))

        # Mostrar o tempo total de jogo
        time_text = my_font.render(f'Time: {elapsed_time}s', True, (255, 255, 0))
        self.display.blit(time_text, (250, 10))

        pygame.display.flip()
        self.clock.tick(120)
        return False

game = Vampire_Cinvivals()
player = Player(x=1250, y=3150)
enemies = []
game_over = False
start_time = pygame.time.get_ticks()  # Tempo inicial do jogo

while not game_over:
    # Calcula o tempo total de jogo em segundos
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    game_over = game.play_step(player, enemies, elapsed_time)

pygame.quit()