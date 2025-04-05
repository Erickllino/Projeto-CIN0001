import pygame
import math



class Basic_attack:
    def __init__(self):
        self.color = (0, 0, 100)
        self.radius = 60
        self.damage = 10

        self.x = 0
        self.y = 0
        
        # Tempo de cooldown e duração do desenho
        self.cooldown = 2            # Tempo total de cooldown
        self.draw_duration = self.cooldown//2   # Tempo em que a arma ficará desenhada após a ativação
        
        self.activation_time = -self.cooldown  # Inicializa com um valor que não bloqueie logo no começo

    def check_hit(self, target_x, target_y, player_x, player_y, elapsed_time):
        distance = math.sqrt((player_x - target_x) ** 2 + (player_y - target_y) ** 2)
        if distance <= self.radius:
            return -self.damage
        else:
            return 0

    def draw(self, game_window, play, elapsed_time):
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



class Book:
    def __init__(self):
        self.color = (255, 0, 100)
        self.radius = 100
        self.damage = 1

        self.x = 0
        self.y = 0

        self.drop = 2

        self.cooldown = 4
        self.draw_duration = self.cooldown//2
        self.activation_time = -self.cooldown

        self.size = 10
        
    
    def check_hit(self, target_x, target_y, player_x, player_y, elapsed_time):
        distance = math.sqrt((self.x - target_x) ** 2 + (self.y - target_y) ** 2)

        if distance <= self.radius:
            return -self.damage
        else:
            return 0
      
    def draw(self, game_window, play, elapsed_time):
        # Se estiver dentro do período em que a arma deve ser desenhada, desenha
        if self.can_activate(elapsed_time):
            print("Cooldown")
            self.x = play.draw_x
            self.y = play.draw_y

        if elapsed_time - self.activation_time < self.draw_duration:
            pygame.draw.circle(game_window, self.color, (self.x, self.y), self.radius, width=5)
        




    def can_activate(self, elapsed_time):
        return elapsed_time - self.activation_time >= self.cooldown

    def activate(self, elapsed_time):
        self.activation_time = elapsed_time
        

