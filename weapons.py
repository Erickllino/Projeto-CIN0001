import pygame
import math



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



class Book:
    def __init__(self):
        # Atributos essenciais da arma
        self.damage = 1

        self.x = 0
        self.y = 0

        self.cooldown = 4 # Tempo total de cooldown para checagem de hit
        self.draw_duration = self.cooldown//2
        self.activation_time = -self.cooldown

        # Atributos específicos da arma
        self.color = (255, 0, 100)
        self.radius = 100
        self.drop = 2 # O o intervalo de tempo entre os drops de livro
        self.size = 10
        
    
    def check_hit(self, target_x, target_y, player_x, player_y, elapsed_time):
        distance = math.sqrt((self.x - target_x) ** 2 + (self.y - target_y) ** 2)

        if distance <= self.radius:
            return -self.damage
        else:
            return 0
      
    def draw(self, game_window, off_x, off_y, play, elapsed_time):
        # Se estiver dentro do período em que a arma deve ser desenhada, desenha

        X = self.x
        Y = self.y

        if self.can_drop(elapsed_time):
            print("Cooldown")
            X = play.x - off_x
            Y = play.y - off_y

            self.x = X
            self.y = Y
        else:
            self.x = X
            self.y = Y

        if elapsed_time - self.activation_time < self.draw_duration:
            pygame.draw.circle(game_window, self.color, (self.x, self.y), self.radius, width=5)
        
    def can_activate(self, elapsed_time):
        return elapsed_time - self.activation_time >= self.cooldown

    def activate(self, elapsed_time):
        self.activation_time = elapsed_time
        
    def can_drop(self, elapsed_time):
        return elapsed_time - self.activation_time >= self.drop