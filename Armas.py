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
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Configuração do quadrado
square_size = 40
square_x = WIDTH // 2 - square_size // 2
square_y = HEIGHT // 2 - square_size // 2
square_speed = 5

# Configuração do ponto verde
circle_radius = square_size // 2 + 20
angle_green = 0
point_green_x = square_x + square_size // 2 + circle_radius * math.cos(angle_green)
point_green_y = square_y + square_size // 2 + circle_radius * math.sin(angle_green)
rotation_speed = 0.05

# Listas para armazenar círculos e tiros
circles = []
triangles = []
triangle_speed = 7

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
                circles.append((square_x + square_size // 2, square_y + square_size // 2))
            if event.key == pygame.K_k:
                angle = math.atan2(point_green_y - (square_y + square_size // 2),
                                   point_green_x - (square_x + square_size // 2))
                triangles.append([square_x + square_size // 2, square_y + square_size // 2, angle])

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
    for triangle in triangles:
        triangle[0] += triangle_speed * math.cos(triangle[2])
        triangle[1] += triangle_speed * math.sin(triangle[2])

    # Remove tiros que saíram da tela
    triangles = [t for t in triangles if 0 < t[0] < WIDTH and 0 < t[1] < HEIGHT]

    # Atualiza a tela
    screen.fill(WHITE)

    # Desenha apenas a circunferência do círculo cinza
    pygame.draw.circle(screen, GRAY, (square_x + square_size // 2, square_y + square_size // 2), circle_radius, 3)
    
    # Desenha o ponto verde
    pygame.draw.circle(screen, GREEN, (int(point_green_x), int(point_green_y)), 5)
    
    # Desenha os círculos fixos
    for circle in circles:
        pygame.draw.circle(screen, RED, circle, 10)
    
    # Desenha os tiros
    for triangle in triangles:
        x, y, angle = triangle
        p1 = (x + 10 * math.cos(angle), y + 10 * math.sin(angle))
        p2 = (x + 5 * math.cos(angle + 2.5), y + 5 * math.sin(angle + 2.5))
        p3 = (x + 5 * math.cos(angle - 2.5), y + 5 * math.sin(angle - 2.5))
        pygame.draw.polygon(screen, BLACK, [p1, p2, p3])
    
    # Desenha o quadrado
    pygame.draw.rect(screen, BLUE, (square_x, square_y, square_size, square_size))
    
    pygame.display.update()

pygame.quit()
