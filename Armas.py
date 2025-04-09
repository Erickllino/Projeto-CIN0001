import pygame
import math

# Inicializa o pygame
pygame.init()

# Configuração da tela
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mover Quadrado, Fixar Círculo e Atirar Triângulo")

# Cores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)

# Configuração do quadrado
square_size = 40
square_x = WIDTH // 2 - square_size // 2
square_y = HEIGHT // 2 - square_size // 2
square_speed = 5

# Configuração do ponto verde
circle_radius = square_size // 2 + 20
angle_green = 0
rotation_speed = 0.05

class Book:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255,0,0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)

class Bottle:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.speed = 7
        self.color = (0, 0, 0)

    def update(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

    def draw(self, screen):
        p1 = (self.x + 10 * math.cos(self.angle), self.y + 10 * math.sin(self.angle))
        p2 = (self.x + 5 * math.cos(self.angle + 2.5), self.y + 5 * math.sin(self.angle + 2.5))
        p3 = (self.x + 5 * math.cos(self.angle - 2.5), self.y + 5 * math.sin(self.angle - 2.5))
        pygame.draw.polygon(screen, self.color, [p1, p2, p3])

# Listas para armazenar círculos e 
books = []
bottles = []

# Loop principal do jogo
running = True
while running:
    pygame.time.delay(30)

    # Captura eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                books.append(Book(square_x + square_size // 2, square_y + square_size // 2))
            if event.key == pygame.K_k:
                angle = math.atan2(point_green_y - (square_y + square_size // 2),
                                   point_green_x - (square_x + square_size // 2))
                bottles.append(Bottle(square_x + square_size // 2, square_y + square_size // 2, angle))

    # Captura teclas pressionadas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        square_x -= square_speed
    if keys[pygame.K_RIGHT]:
        square_x += square_speed
    if keys[pygame.K_UP]:
        square_y -= square_speed
    if keys[pygame.K_DOWN]:
        square_y += square_speed
    if keys[pygame.K_a]:
        angle_green -= rotation_speed
    if keys[pygame.K_s]:
        angle_green += rotation_speed

    # Atualiza a posição do ponto verde
    point_green_x = square_x + square_size // 2 + circle_radius * math.cos(angle_green)
    point_green_y = square_y + square_size // 2 + circle_radius * math.sin(angle_green)

    # Atualiza a posição dos tiros
    for triangle in bottles:
        triangle.update()

    # Remove tiros que saíram da tela
    bottles = [t for t in bottles if 0 < t.x < WIDTH and 0 < t.y < HEIGHT]

    # Atualiza a tela
    screen.fill(WHITE)

    # Desenha a circunferência do círculo cinza
    pygame.draw.circle(screen, GRAY, (square_x + square_size // 2, square_y + square_size // 2), circle_radius, 3)
    
    # Desenha o ponto verde
    pygame.draw.circle(screen, GREEN, (int(point_green_x), int(point_green_y)), 5)
    
    # Desenha os círculos fixos
    for book in books:
        book.draw(screen)
    
    # Desenha os tiros
    for bottle in bottles:
        bottle.draw(screen)
    
    # Desenha o quadrado
    pygame.draw.rect(screen, BLUE, (square_x, square_y, square_size, square_size))
    imagem = pygame.image.load("./sprites/garrafa.png")
    imagem = pygame.transform.scale(imagem, (20, 40))
   
    
    screen.blit(imagem, (250, 250))
    
    pygame.display.update()

pygame.quit()
