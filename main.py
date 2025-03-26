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
        self.level = 1
        self.xp = 0
        self.max_health = 100
        self.health = 100
        self.speed = 4

        self.life_steal = 0
        
        self.invulnerable = False
        self.invulnerable_time = 1
        self.last_hit_time = 0

        # Desenho do jogador
        self.radius = radius
        self.color = color
        
        # Possiveis upgrades ao upar de nivel
        self.upgrades = {'Health':['Aumenta a vida do jogador em 10%', 'player.max_health *= 1.1 ; player.health *= 1.1'],
                         'Restore Health':['Restaura a vida do jogador', 'player.health = player.max_health'], 
                         'Speed':['Aumenta a velocidade em 10%', 'player.speed *= 1.1'],
                         'Life Steal':[self.get_life_steal_description(), 'player.life_steal += 0.1'],
                         'Cracha radius':['Aumenta o raio do ataque básico em 10%', 'self.active_weapons[\'Cracha\'].radius *= 1.1'],
                         'Cracha damage':['Aumenta o dano do ataque básico em 10', 'self.active_weapons[\'Cracha\'].damage += 10'],
                         'Cracha cooldown':['Diminui o cooldown do ataque básico', 'self.active_weapons[\'Cracha\'].cooldown *= 0.5']}

    def get_life_steal_description(self):
        return f'Aumenta em 10% o roubo de vida: {self.life_steal * 100 + 10}% dano causado cura o personagem'

        
    def update_invulnerability(self, current_time):
        if self.invulnerable:
            # Check if invulnerability period has ended
            if current_time - self.last_hit_time >= self.invulnerable_time:
                self.invulnerable = False
    
    def make_invulnerable(self, current_time):
        self.invulnerable = True
        self.last_hit_time = current_time
    
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
        self.mask = pygame.mask.from_threshold(self.Map, (0, 0, 0), (2, 2, 2))  # Cria a máscara de colisão
        
        # Inicializa o spawn de inimigos
        self.last_spawn = 0

        # Inicializa as armas, pode ser adicionado mais armas
        self.active_weapons = {'Cracha':Basic_attack(),'Book': Book()}

        


    def main_menu(self,game):
        menu_ativo = True
        while menu_ativo:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Quando o jogador pressionar ENTER, inicia o jogo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        menu_ativo = False

            # Preenche a tela com uma cor de fundo
            # da pra colocar um imagem aqui
            game.display.fill((0, 0, 0))
            

            menu_font = pygame.font.SysFont('Comic Sans MS', 50)
            # Renderiza o título e a mensagem de iniciar
            title_text = menu_font.render("Vampire Cinvivals", True, (255, 255, 255))
            prompt_text = my_font.render("Pressione Enter para iniciar", True, (255, 255, 255))
            
            # Centraliza os textos na tela
            title_pos = (game.w // 2 - title_text.get_width() // 2, game.h // 2 - 100)
            prompt_pos = (game.w // 2 - prompt_text.get_width() // 2, game.h // 2)
            game.display.blit(title_text, title_pos)
            game.display.blit(prompt_text, prompt_pos)
            
            pygame.display.flip()
            clock.tick(60)

    def game_over(self):
        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Quando o jogador pressionar ENTER, tenta denovo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        
                        game_over = False
                        return True, False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        
                        game_over = True
                        return False, True

            # Preenche a tela com uma cor de fundo
            # da pra colocar um imagem aqui
            self.display.fill((0, 0, 0))
            
           
            
            title_text = my_font.render("Você Morreu", False, (255, 255, 255))
            prompt_text = my_font.render("Aperte esc para sair", True, (255, 255, 255))
            
            # Centraliza os textos na tela
            title_pos = (self.w // 2 - title_text.get_width() // 2, self.h // 2 - 100)
            prompt_pos = (self.w // 2 - prompt_text.get_width() // 2, self.h // 2)
            self.display.blit(title_text, title_pos)
            self.display.blit(prompt_text, prompt_pos)
            
            pygame.display.flip()
            clock.tick(60)

    def level_up(self, player):
        leveling_up = True
        player.upgrades = player.upgrades
        selected_keys = random.sample(list(player.upgrades.keys()), 3)
        selected_upgrades = { key: player.upgrades[key] for key in selected_keys }

        while leveling_up:
            
            # tamanho do retângulo
            up_size = self.w//4

            # Renderiza cada linha e posiciona no retângulo
            def blit_text(display, text_lines, rect, font, color=(255,255,255)):
                line_height = font.get_linesize()
                total_text_height = len(text_lines) * line_height
                y_offset = rect.centery - total_text_height // 2
                for line in text_lines:
                    rendered_line = font.render(line, True, color)
                    line_rect = rendered_line.get_rect(centerx=rect.centerx, y=y_offset)
                    display.blit(rendered_line, line_rect)
                    y_offset += line_height

            def wrap_text(text, font, max_width):
                words = text.split(' ')
                lines = []
                current_line = ''
                for word in words:
                    test_line = current_line + word + ' '
                    if font.size(test_line)[0] <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word + ' '
                lines.append(current_line)
                return lines



            # Configura a fonte do Texto do upgrade
            font = pygame.font.SysFont('Arial', 30)
            max_text_width = up_size - 10  # margem

            lines1 = wrap_text(selected_upgrades[selected_keys[0]][0], font, max_text_width)
            lines2 = wrap_text(selected_upgrades[selected_keys[1]][0], font, max_text_width)
            lines3 = wrap_text(selected_upgrades[selected_keys[2]][0], font, max_text_width)

            # Criação dos retângulos (exemplo)
            rect1 = pygame.Rect((self.w - up_size) // 4 - up_size // 2, (self.h - up_size) // 2, up_size, up_size)
            rect2 = pygame.Rect((self.w - up_size) // 2, (self.h - up_size) // 2, up_size, up_size)
            rect3 = pygame.Rect((3 * self.w - up_size) // 4, (self.h - up_size) // 2, up_size, up_size)

            # Desenha os retângulos
            pygame.draw.rect(self.display, (255, 0, 0), rect1)
            pygame.draw.rect(self.display, (0, 255, 0), rect2)
            pygame.draw.rect(self.display, (0, 0, 255), rect3)

            # Blita o texto com quebra de linha
            blit_text(self.display, lines1, rect1, font)
            blit_text(self.display, lines2, rect2, font)
            blit_text(self.display, lines3, rect3, font)

            upgrade1 = my_font.render("Aperte 1", True, (0, 0, 0))
            self.display.blit(upgrade1, ((self.w-up_size)//4-up_size//2, (self.h-up_size)//2-30))
            upgrade2 = my_font.render("Aperte 2", True, (0, 0, 0))
            self.display.blit(upgrade2, ((self.w-up_size)//2, (self.h-up_size)//2-30))
            upgrade3 = my_font.render("Aperte 3", True, (0, 0, 0))
            self.display.blit(upgrade3, ((3*self.w-up_size)//4, (self.h-up_size)//2-30))

            pygame.display.flip()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Quando o jogador pressionar ENTER, tenta denovo
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        exec(selected_upgrades[selected_keys[0]][1])
                        leveling_up = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_2:
                        exec(selected_upgrades[selected_keys[1]][1])
                        leveling_up = False
                        
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_3:
                        exec(selected_upgrades[selected_keys[2]][1])
                        leveling_up = False
                        
                    

            
        

    def play_step(self, player, enemies, elapsed_time):
        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
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


        # Update invulnerability
        player.update_invulnerability(elapsed_time)
        for enemy in enemies:
            enemy.update_invulnerability(elapsed_time)

        # Weapons
        for weapon in self.active_weapons:
            weapon_instance = self.active_weapons[weapon]
            # Se a arma não estiver em cooldown, atualiza a ativação (e aplica o efeito)


            if not weapon_instance.on_cooldown(elapsed_time):
                for enemy in enemies:
                    if not enemy.invulnerable:
                        enemy.life += weapon_instance.check_hit(enemy.x, enemy.y, player.x, player.y, elapsed_time)
                        if player.health < player.max_health:
                            player.health -= (player.life_steal)*weapon_instance.check_hit(player.x, player.y, enemy.x, enemy.y, elapsed_time)
                        
                        enemy.make_invulnerable(elapsed_time)

            # Chama o método draw sempre, que internamente verificará se deve desenhar ou não
            
            weapon_instance.draw(self.display, player.draw_x, player.draw_y, elapsed_time)

        # Upgrade Basic_attack
        if player.xp >= 1*(1.1**(player.level-1)) and player.xp != 0:
           self.level_up(player)
           player.xp = 0
           player.level += 1
      
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
                print(f'Number of Enemies: {len(enemies)},Health {player.health}, XP: {player.xp}, Basic_attack radius: {self.active_weapons['Cracha'].radius}')
                self.last_spawn = elapsed_time
                spawn_rate += 1

        # Move Enemies
        for enemy_one in enemies:
            enemy_one.move(player, self.mask)
            enemy_one.draw(self.display, offset_x, offset_y)

            
        # Check if enemies hit player
        for enemy_one in enemies:
            distance = math.sqrt((player.x - enemy_one.x) ** 2 + (player.y - enemy_one.y) ** 2)
            if distance < 10 and not player.invulnerable:
                player.health -= 1
                player.make_invulnerable(elapsed_time)

        if player.health <= 0:
            return True

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
        self.display.blit(time_text, (self.w//2, 10))

        # Mostrar a vida do jogador
        health_text = my_font.render(f'Health: {player.health}', True, (255, 0, 0))
        self.display.blit(health_text, (10, self.h - 30))

        # Mostrar a pontuação do jogador
        xp_text = my_font.render(f'XP: {player.xp}', True, (0, 255, 0))
        self.display.blit(xp_text, (self.w//2, self.h - 30))

        pygame.display.flip()
        self.clock.tick(120)
        return False
    
player = Player(x=1250, y=3150)
game = Vampire_Cinvivals(1200, 800)

enemies = []
game_over = False
try_again = True 
start_time = pygame.time.get_ticks()  # Tempo inicial do jogo

game.main_menu(game)
while try_again:
    while not game_over:
        # Calcula o tempo total de jogo em segundos
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        game_over = game.play_step(player, enemies, elapsed_time)

    try_again, game_over = game.game_over()
pygame.quit()