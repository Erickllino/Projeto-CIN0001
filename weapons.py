import pygame
import math
from time import sleep as sp

class Basic_attack:
    def __init__(self):
        # Atributos essenciais da arma
        self.damage = 10

        self.x = 0
        self.y = 0
        
        # Tempo de cooldown e duração do desenho
        self.cooldown = 2            # Tempo total de cooldown
        self.draw_duration = self.cooldown//2   # Tempo em que a arma ficará desenhada após a ativação
        
        self.activation_time = -self.cooldown  # Inicializa com um valor que não bloqueie logo no começo
        
        self.color = (0, 0, 100)
        self.radius = 60

    def check_hit(self, target_x, target_y, player_x, player_y, elapsed_time):
        distance = math.sqrt((player_x - target_x) ** 2 + (player_y - target_y) ** 2)
        if distance <= self.radius:
            return -self.damage
        else:
            return 0

    def draw(self, game_window, off_x, off_y, play, elapsed_time):
        # Se estiver dentro do período em que a arma deve ser desenhada, desenha
        self.x = play.draw_x
        self.y = play.draw_y
        #self.draw_duration = self.cooldown/2
        
        if elapsed_time - self.activation_time < self.draw_duration:
            pygame.draw.circle(game_window, self.color, (self.x, self.y), self.radius, width=5)

    def can_activate(self, elapsed_time):
        return elapsed_time - self.activation_time >= self.cooldown

    def activate(self, elapsed_time):
        self.activation_time = elapsed_time



# class Book:
#     def __init__(self):
#         # Atributos essenciais da arma
#         self.damage = 1

#         self.x = 0
#         self.y = 0

#         self.cooldown = 4 # Tempo total de cooldown para checagem de hit
#         self.draw_duration = self.cooldown//2
#         self.activation_time = -self.cooldown

#         # Atributos específicos da arma
#         self.color = (255, 0, 100)
#         self.radius = 100
#         self.drop = 2 # O o intervalo de tempo entre os drops de livro
#         self.size = 10
        
    
#     def check_hit(self, target_x, target_y, player_x, player_y, elapsed_time):
#         distance = math.sqrt((self.x - target_x) ** 2 + (self.y - target_y) ** 2)

#         if distance <= self.radius:
#             return -self.damage
#         else:
#             return 0
      
#     def draw(self, game_window, off_x, off_y, play, elapsed_time):
#         # Se estiver dentro do período em que a arma deve ser desenhada, desenha

#         X = self.x
#         Y = self.y

#         if self.can_drop(elapsed_time):
#             print("Cooldown")
#             X = play.x - off_x
#             Y = play.y - off_y

#             self.x = X
#             self.y = Y
#         else:
#             self.x = X
#             self.y = Y

#         if elapsed_time - self.activation_time < self.draw_duration:
#             pygame.draw.circle(game_window, self.color, (self.x, self.y), self.radius, width=5)
        
#     def can_activate(self, elapsed_time):
#         return elapsed_time - self.activation_time >= self.cooldown

#     def activate(self, elapsed_time):
#         self.activation_time = elapsed_time
        
#     def can_drop(self, elapsed_time):
#         return elapsed_time - self.activation_time >= self.drop

class Bottle:
    def __init__(self, x, y, temp):
        self.x = x
        self.y = y
        self.temp = temp
        self.imagem = pygame.image.load("./sprites/garrafa/garrafa.png")
        self.imagem = pygame.transform.scale(self.imagem, (20, 40))
        self.damage = 5
   
    def draw(self, screen, diff_tempo, offset_x, offset_y):
        dimensao_explocao = (40, 40)
        ponto = (self.x - offset_x, self.y - offset_y)
        ponto_centro = (self.x - offset_x + 20, self.y - offset_y + 20)
        if diff_tempo < 0.16:
            self.imagem = pygame.image.load("./sprites/garrafa/garrafa.png")
            self.imagem = pygame.transform.scale(self.imagem, (20, 40))
        elif diff_tempo < 0.17:
            self.imagem = pygame.image.load("./sprites/garrafa/explosao1.png")
            self.imagem = pygame.transform.scale(self.imagem, dimensao_explocao)
        elif diff_tempo < 0.32:
            self.imagem = pygame.image.load("./sprites/garrafa/explosao2.png")
            self.imagem = pygame.transform.scale(self.imagem, dimensao_explocao)
        elif diff_tempo < 0.48:
            self.imagem = pygame.image.load("./sprites/garrafa/explosao3.png")
            self.imagem = pygame.transform.scale(self.imagem, dimensao_explocao)
        elif diff_tempo < 0.64:
            self.imagem = pygame.image.load("./sprites/garrafa/explosao4.png")
            self.imagem = pygame.transform.scale(self.imagem, dimensao_explocao)
        elif diff_tempo < 0.80:
            self.imagem = pygame.image.load("./sprites/garrafa/explosao5.png")
            self.imagem = pygame.transform.scale(self.imagem, dimensao_explocao)
            pygame.draw.circle(screen, (100,100,100), ponto_centro, 60, width=5)
        else:            
            self.imagem = pygame.image.load("./sprites/garrafa/explosao6.png")
            self.imagem = pygame.transform.scale(self.imagem, dimensao_explocao)
            pygame.draw.circle(screen, (100,100,100), ponto_centro, 60, width=5)
        
        screen.blit(self.imagem, ponto)
    
    
    def check_hit(self, opp_x, opp_y, offset_x, offset_y):
        distance = math.sqrt((self.x - opp_x) ** 2 + (self.y - opp_y) ** 2)
        
        if distance <= 60:
            

            return -self.damage
        return 0

    def estado(self, tempo, screen, offset_x, offset_y):
        if tempo - self.temp < 1:
            self.draw(screen, tempo - self.temp, offset_x, offset_y)
            return False
        return True


    # def check_hit(self):
    #     pass

    # def update(self):
    #     self.x += self.speed * math.cos(self.angle)
    #     self.y += self.speed * math.sin(self.angle)

    # def draw(self, screen):
    #     p1 = (self.x + 10 * math.cos(self.angle), self.y + 10 * math.sin(self.angle))
    #     p2 = (self.x + 5 * math.cos(self.angle + 2.5), self.y + 5 * math.sin(self.angle + 2.5))
    #     p3 = (self.x + 5 * math.cos(self.angle - 2.5), self.y + 5 * math.sin(self.angle - 2.5))
    #     pygame.draw.polygon(screen, self.color, [p1, p2, p3])



# class Book:
#     def __init__(self, x, y):
#         self.x = x
#         self.y = y
#         self.color = (255,0,0)

#     def draw(self, screen):
#         pygame.draw.circle(screen, self.color, (self.x, self.y), 10)

