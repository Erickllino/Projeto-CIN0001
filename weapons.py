import pygame
import math

class Basic_attack:
    def __init__(self):
        self.color = (0, 0, 100)
        self.radius = 60
        self.damage = 10
        
        # Tempo de cooldown e duração do desenho
        self.cooldown = 2            # Tempo total de cooldown
        self.draw_duration = self.cooldown/2    # Tempo em que a arma ficará desenhada após a ativação
        
        self.activation_time = -self.cooldown  # Inicializa com um valor que não bloqueie logo no começo

    def check_hit(self, target_x, target_y, player_x, player_y, elapsed_time):
        distance = math.sqrt((player_x - target_x) ** 2 + (player_y - target_y) ** 2)
        if distance <= self.radius:
            return -self.damage
        else:
            return 0

    def draw(self, game_window, x, y, elapsed_time):
        # Se estiver dentro do período em que a arma deve ser desenhada, desenha
        self.draw_duration = self.cooldown/2
        if elapsed_time - self.activation_time < self.draw_duration:
            pygame.draw.circle(game_window, self.color, (x, y), self.radius, width=5)

    def on_cooldown(self, elapsed_time):
        # Se ainda estiver no cooldown, retorna True
        print('O cooldown é:', self.cooldown)
        if elapsed_time - self.activation_time <= self.cooldown:
            return True
        else:
            # Atualiza o tempo de ativação e retorna False (não está em cooldown)
            self.activation_time = elapsed_time
            return False



class Book:
    def __init__(self):
        self.color = (255, 0, 100)
        self.radius = 60
        self.damage = 1

        self.cooldown = 2
        self.draw_duration = self.cooldown//2
        self.activation_time = -self.cooldown

        self.size = 10
        
        

    def check_hit(self, target_x, target_y, player_x, player_y, elapsed_time):
        distance = math.sqrt((player_x - target_x) ** 2 + (player_y - target_y) ** 2)

        if distance <= self.radius:
            return -self.damage
        else:
            return 0
      
    def draw(self, game_window, x, y, elapsed_time):
        # Se estiver dentro do período em que a arma deve ser desenhada, desenha
        if elapsed_time - self.activation_time <= self.draw_duration:
            pygame.draw.rect(game_window, self.color, pygame.Rect(x, y, self.size, self.size))
            #pygame.draw.rect(game_window, self.color, (x, y), self.size)


    def on_cooldown(self, elapsed_time):
        # Se ainda estiver no cooldown, retorna True
        if elapsed_time - self.activation_time < self.cooldown:
            return True
        else:
            # Atualiza o tempo de ativação e retorna False (não está em cooldown)
            self.activation_time = elapsed_time
            return False
        
    def lauch_projectile(self, x, y, elapsed_time):
        if elapsed_time % self.cooldown == 0 and elapsed_time != 0:
            return x, y
        else:
            return 0, 0
