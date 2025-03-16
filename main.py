import pygame
import random
import math

from weapons import Basic_attack
from weapons import Book

from Enemies import Enemy_one

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
my_font = pygame.font.SysFont('Comic Sans MS', 20)


class Player:
    def __init__(self, x, y, radius=10, color=(255, 0, 0)):
        # Posição do jogador
        self.x = x
        self.y = y
        # Posição do jogador na tela
        self.draw_x = 0
        self.draw_y = 0
        # Características do jogador
        self.xp = 0
        self.health = 100
        self.speed = 4
        
        # Desenho do jogador
        self.radius = radius
        self.color = color
        

    def hitbox(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self, keys, map_size, mask):
        dx, dy = 0, 0
        # Movimentação do jogador
        if keys[pygame.K_LEFT]:
            dx = -self.speed
        if keys[pygame.K_RIGHT]:
            dx = self.speed
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed
        if keys[pygame.K_TAB]:
            pygame.quit()

        new_x = max(self.radius, min(map_size[0] - self.radius, self.x + dx))
        new_y = max(self.radius, min(map_size[1] - self.radius, self.y + dy))

        # Check collision with map
        if not mask.overlap_area(pygame.mask.Mask((self.radius * 2, self.radius * 2), fill=True), (new_x - self.radius, self.y - self.radius)):
            self.x = new_x
        if not mask.overlap_area(pygame.mask.Mask((self.radius * 2, self.radius * 2), fill=True), (self.x - self.radius, new_y - self.radius)):
            self.y = new_y

        
    def draw(self, game_window, center, map_size, window_size, offset_x, offset_y):
        # Mantém o jogador no centro da tela
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
        
        # Desenha o jogador, quando for colocar uma imagem, substituir o pygame.draw.circle por game_window.blit
        pygame.draw.circle(game_window, self.color, (int(draw_x), int(draw_y)), self.radius)



class Vampire_Cinvivals:
    def __init__(self, w=600, h=600):
        # Tamanho da tela
        self.w = w
        self.h = h
        # Inicializa a tela
        self.display = pygame.display.set_mode((w, h))
        # Nome do jogo
        pygame.display.set_caption("Vampire_Cinvivals")
        # Inicializa o relógio, para contgem do tempo e FPS
        self.clock = pygame.time.Clock()

        # Carrega o mapa
        self.Map = pygame.image.load("sprites/map.jpg").convert()  # Resolução da Imagem 2550x3300

        # Cria a máscara de colisão, se quiser usar uma mascara diferente, basta trocar o arquivo
        self.mask = pygame.mask.from_threshold(self.Map, (0, 0, 0), (1, 1, 1))  # Cria a máscara de colisão
        
        # Inicializa o spawn de inimigos
        self.last_spawn = 0

        # Inicializa as armas, pode ser adicionado mais armas
        self.active_weapons = [Basic_attack(), Book()]

    def map_collision(self):
        NotImplemented

    def play_step(self, player, enemies, elapsed_time):
        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return True

        keys = pygame.key.get_pressed()
        player.move(keys, self.Map.get_size(), self.mask)

        self.display.fill((0, 0, 0))
        map_size = self.Map.get_size()
        window_size = self.display.get_size()
        # Calcula o offset para manter o jogador no centro da tela
        offset_x = max(0, min(map_size[0] - window_size[0], player.x - window_size[0] / 2))
        offset_y = max(0, min(map_size[1] - window_size[1], player.y - window_size[1] / 2))
        self.display.blit(self.Map, (-offset_x, -offset_y))

        player.draw(self.display, (window_size[0] // 2, window_size[1] // 2), map_size, window_size, offset_x, offset_y)

        # Weapons
        for weapon in self.active_weapons:
            weapon_instance = weapon
            weapon_instance.draw(self.display, player.draw_x, player.draw_y, elapsed_time)
            for enemy in enemies:
                enemy.life += weapon_instance.check_hit(enemy.x, enemy.y, player.x, player.y, elapsed_time)

        # Upgrade Basic_attack
        if player.xp >= 10 and player.xp != 0:
            player.xp = 0
            self.active_weapons[0].radius *= 1.10
      
        # Spawn Enemies
        if len(enemies) <= 3000:
            spawn_rate = int(1.06173*(elapsed_time**0.6231684)) # Colocar uma fórmula para o aumento de inimigos
        else:
            spawn_rate = 30

        
        if elapsed_time != self.last_spawn:
            for i in range(spawn_rate):
                bool_spawn = True
                while bool_spawn:

                    spawn_x = random.randint(0, self.Map.get_width())
                    spawn_y = random.randint(0, self.Map.get_height())
                    # Calcular a área visível da tela
                    visible_x_min = player.draw_x - self.display.get_width() // 2
                    visible_x_max = player.draw_x + self.display.get_width() // 2
                    visible_y_min = player.draw_y - self.display.get_height() // 2
                    visible_y_max = player.draw_y + self.display.get_height() // 2
                    # Verificar se a posição de spawn está fora da área visível
                    if not (visible_x_min <= spawn_x <= visible_x_max and visible_y_min <= spawn_y <= visible_y_max):
                        print(f'Player at: {player.x, player.y}, Enemy at: {spawn_x, spawn_y}')
                        bool_spawn = False
                
                enemies.append(Enemy_one(spawn_x, spawn_y))
                #enemies.append(Enemy_one(random.randint(1000, 2550), random.randint(1500, 3300)))
                print(f'Number of Enemies: {len(enemies)},Health {player.health}, XP: {player.xp}, Basic_attack radius: {self.active_weapons[0].radius}')
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

        # Mostrar a vida do jogador
        health_text = my_font.render(f'Health: {player.health}', True, (255, 0, 0))
        self.display.blit(health_text, (10, 570))

        # Mostrar a pontuação do jogador
        xp_text = my_font.render(f'XP: {player.xp}', True, (0, 255, 0))
        self.display.blit(xp_text, (250, 570))

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