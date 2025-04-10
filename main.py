import pygame
import random
import math
import time
from weapons import Basic_attack, Bottle

from Enemies import ZombieOne, ZombieTwo, ZombieThree, ZombieFour, ZombieFive, ZombieBoss

from PlayerCharacter import Player

from gerenciador_fases import GerenciadorFases
from fases import Fase, dados_fase1, dados_fase2, dados_fase3, dados_fase4

pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
my_font = pygame.font.Font('font/Mantinia Regular/Mantinia Regular.otf', 20)


class Vampire_Cinvivals:

    def __init__(self, w=1000, h=1000):
        
        Vampire_Cinvivals._instancia = self  # Registra a instância
        self.offset_x = 0  # Novo atributo
        self.offset_y = 0  # Novo atributo

        self.bottles = [] # As Garrafas no chão
        self.temp_garrafa = time.time() # Controla o tempo entre a criação das garrafas

        # Metricas da garrafa dourada
        self.temp_gold = time.time() # Tempo para controlar a aparição da garrada dourada
        self.garrafa_dourada = '' # A garrada dourada será declado quando for aparecer
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

        self.Map = pygame.image.load("sprites/map.png").convert()  # Resolução da Imagem  3902x5055
        self.walls = pygame.image.load("sprites/walls.png").convert()  # Resolução da Imagem  3902x5055
        # Cria a máscara de colisão, se quiser usar uma mascara diferente, basta trocar o arquivo

        self.mask = pygame.mask.from_threshold(self.walls, (0, 0, 0), (2, 2, 2))  # Cria a máscara de colisão        

        # Inicializa o som de level up
        self.level_up_sound = pygame.mixer.Sound("sprites/sons_effects/level_up.mp3")

        # Inicializa o som de morte
        self.game_over_sound = pygame.mixer.Sound("sprites/sons_effects/game_over.mp3")
        
        # Inicializa o som de vitória
        self.victory_sound = pygame.mixer.Sound("sprites/sons_effects/victory.mp3")

        self.menu_music = pygame.mixer.Sound("sprites/sons_effects/menu_music.mp3")
        # Inicializa o spawn de inimigos
        self.last_spawn = 0

        self.boss = None
        self.boss_can_spawn = False  # Controle para o spawn do boss
        self.boss_spawn_time = None  # 1 minutos para o primeiro spawn
        self.boss_respawn_delay = 120   # 2 minutos para reaparecer após a morte
        self.last_boss_death_time = None

        self.victory = False  # Controle para a vitória do jogador

        # Inicializa as armas, pode ser adicionado mais armas

        self.active_weapons = {'Cracha':Basic_attack(),}

        self.all_weapons = ['Cracha', "Garrafa", "Garrafa_dourada"]

        # fases

        self.gerenciador_fases = GerenciadorFases()

        self.gerenciador_fases.adicionar_fase(Fase(dados_fase1))

        self.gerenciador_fases.adicionar_fase(Fase(dados_fase2))

        self.gerenciador_fases.adicionar_fase(Fase(dados_fase3))

        self.gerenciador_fases.adicionar_fase(Fase(dados_fase4))

        self.gerenciador_fases.iniciar_proxima_fase()

    def main_menu(self,game):

        menu_ativo = True
        self.menu_music.play(-1)  # Toca a música em loop
        self.menu_music.set_volume(10000)  # Ajusta o volume da música do menu
        while menu_ativo:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    pygame.quit()

                    quit()

                # Quando o jogador pressionar ENTER, inicia o jogo

                if event.type == pygame.KEYDOWN:

                    if event.key:

                        menu_ativo = False
                        self.menu_music.stop()  # Para a música do menu quando o jogo começa
                        

            # Preenche a tela com uma cor de fundo
            # da pra colocar um imagem aqui
            game.display.fill((0, 0, 0))

            menu_font = pygame.font.Font('font/Mantinia Regular/Mantinia Regular.otf', 100)

            # Renderiza o título e a mensagem de iniciar
            title_text = menu_font.render("Vampire Cinvivals", True, (255, 255, 255))

            prompt_text = my_font.render("Pressione Qualquer Tecla", True, (255, 255, 255))

            # Centraliza os textos na tela
            title_pos = (game.w // 2 - title_text.get_width() // 2, game.h // 2 - 100)

            prompt_pos = (game.w // 2 - prompt_text.get_width() // 2, game.h // 2 + 100)

            game.display.blit(title_text, title_pos)
            game.display.blit(prompt_text, prompt_pos)

        
            pygame.display.flip()

            clock.tick(60)

    def game_over(self):

        game_over = True
        self.game_over_sound.play()
        
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

        pygame.mixer.stop()

        # Seleciona 3 upgrades aleatórios
        selected_keys = random.sample(list(player.upgrades.keys()), 3)

        # Cria um dicionário com os upgrades selecionados e suas respectivas funções
        selected_upgrades = { key: player.upgrades[key] for key in selected_keys }

        # Inicializa o som de level up
        self.level_up_sound.play()
        self.level_up_sound.set_volume(1)  # Ajusta o volume do som de level up
        leveling_up = True

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
            Level_up_font = pygame.font.SysFont('Arial', 50)
            max_text_width = up_size - 10  # margem
            
            tittle = Level_up_font.render('Level UP!', True, (255,255,0), (200,200,200))
            self.display.blit(tittle, ((self.w) // 2 - tittle.get_width()//2, (self.h  - up_size)//2 - tittle.get_height()-30))

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



            upgrade1 = my_font.render("Aperte 1", True, (0, 0, 0), (255, 255, 255))

            self.display.blit(upgrade1, ((self.w-up_size)//4-up_size//2, (self.h-up_size)//2-30))

            upgrade2 = my_font.render("Aperte 2", True, (0, 0, 0), (255, 255, 255))

            self.display.blit(upgrade2, ((self.w-up_size)//2, (self.h-up_size)//2-30))

            upgrade3 = my_font.render("Aperte 3", True, (0, 0, 0), (255, 255, 255))

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

    def victory_screen(self, game):
        won = True
        pygame.mixer.stop()

        self.victory_sound.play()
        self.victory_sound.set_volume(1)
        
        while won:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # Quando o jogador pressionar qualquer tecla
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return
                        


            # Preenche a tela com uma cor de fundo

            # da pra colocar um imagem aqui
            game.display.fill((0, 0, 0))
            final_font = pygame.font.Font('font/Mantinia Regular/Mantinia Regular.otf', 100)
            title_text = final_font.render("Você Venceu!", False, (255, 255, 255))

            prompt_text = my_font.render("Aperte Enter", True, (255, 255, 255))

            # Centraliza os textos na tela

            title_pos = (self.w // 2 - title_text.get_width() // 2, self.h // 2 - 100)

            prompt_pos = (self.w // 2 - prompt_text.get_width() // 2, self.h // 2 + 100)

            game.display.blit(title_text, title_pos)

            game.display.blit(prompt_text, prompt_pos)

            pygame.display.flip()

            clock.tick(60)


    def play_step(self, player, enemies, elapsed_time):

        # Eventos do jogo

        for event in pygame.event.get():

            if event.type == pygame.QUIT:

                pygame.quit()

                quit()

                return True

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_TAB:
                
                del enemies[:]


                

        keys = pygame.key.get_pressed()

        player.move(keys, self.Map.get_size(), self.mask)

        # Atualizar fases
        self.gerenciador_fases.atualizar((player.x, player.y), elapsed_time)

        # Verificar transição de fases
        if self.gerenciador_fases.fase_atual.esta_concluida:
            
            if not self.gerenciador_fases.iniciar_proxima_fase() and self.boss_spawn_time == None:
                
                self.boss_can_spawn = True  # Permite o spawn do boss após todas as fases serem concluídas
                self.boss_spawn_time = elapsed_time  # Registra o tempo do primeiro spawn do boss
                print("Boss Spawned at:", self.boss_spawn_time)

            elif self.last_boss_death_time is not None:
                self.victory = True # Retorna True para indicar que o jogo deve terminar após a morte do boss
            
            
        self.display.fill((0, 0, 0))

        map_size = self.Map.get_size()

        window_size = self.display.get_size()

        # Calcula o offset para manter o jogador no centro da tela

        offset_x = max(0, min(map_size[0] - window_size[0], player.x - window_size[0] / 2))

        offset_y = max(0, min(map_size[1] - window_size[1], player.y - window_size[1] / 2))
        # Calcular e armazenar offset
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.display.blit(self.Map, (-offset_x, -offset_y))


        # Renderizar elementos das fases
        self.gerenciador_fases.desenhar(self.display, offset_x, offset_y)

        player.draw(self.display, (window_size[0] // 2, window_size[1] // 2), map_size, window_size, offset_x, offset_y)

        #print(f'Player at: {player.x, player.y}')

        # Update invulnerability

        player.update_invulnerability(elapsed_time)

        for enemy in enemies:

            enemy.update_invulnerability(elapsed_time)
        

        # Desenha as armas a serem colocadas no chão
        for weapon_instance in self.all_weapons:

            if weapon_instance not in self.active_weapons.keys():

                if weapon_instance == 'Garrafa':
                    screen_x = 1800 - offset_x
                    screen_y = 3330 - offset_y
                    imagem = pygame.image.load("./sprites/garrafa/garrafa.png")
                    imagem = pygame.transform.scale(imagem, (20, 40))
                    self.display.blit(imagem, (int(screen_x), int(screen_y)))
                    if player.hitbox().colliderect(pygame.Rect(1800 - 10, 3330 - 10, 20, 20)):
                        self.active_weapons['Garrafa'] = ""
 
            if weapon_instance == 'Garrafa_dourada' and time.time() - self.temp_gold >= 20:
                screen_x = 1925 - offset_x
                screen_y = 4550 - offset_y
                imagem = pygame.image.load("./sprites/garrafa/garrafa_dourada.png")
                imagem = pygame.transform.scale(imagem, (50, 60))
                self.display.blit(imagem, (int(screen_x), int(screen_y)))
                    
                if player.hitbox().colliderect(pygame.Rect(1925 - 10, 4550 - 10, 20, 20)):
                    self.active_weapons['Garrafa_dourada'] = True
                    self.temp_gold = time.time()
                    time.sleep(1)

        # Weapons
        for weapon in self.active_weapons:

            weapon_instance = self.active_weapons[weapon]
        
            # Ações das armas de acordo com o seu tipo
            if weapon == "Garrafa":
                remover = []
                if time.time() - self.temp_garrafa >= 0.5:
                    self.bottles.append(Bottle(player.x, player.y, time.time()))
                    self.temp_garrafa = time.time() 
                for i in range(len(self.bottles)):
                    bottle = self.bottles[i]                
                    isAtivo = bottle.estado(time.time(), self.display, offset_x, offset_y)
                    if isAtivo:
                        for enemy in enemies:
                          
                          enemy.life += bottle.check_hit(enemy.x, enemy.y, offset_x, offset_y)

                        remover.append(i)
                for x in remover:
                    try:                            
                        del self.bottles[x]
                    except IndexError:
                        pass  
            elif weapon == "Garrafa_dourada":
                if weapon_instance:
                    for enemy in enemies:
                        enemy.life -= enemy.life
                    self.active_weapons[weapon] = False

            else:

                weapon_instance.draw(self.display,offset_x,offset_y, player, elapsed_time)

                # Se a arma não estiver em cooldown, atualiza a ativação (e aplica o efeito)

                if weapon_instance.can_activate(elapsed_time):

                    weapon_instance.activate(elapsed_time)

                    for enemy in enemies:

                        if not enemy.invulnerable:

                            enemy.life += weapon_instance.check_hit(enemy.x, enemy.y, player.x, player.y, elapsed_time)

                            if player.health < player.max_health:

                                
                                player.health -= (player.life_steal)*weapon_instance.check_hit(player.x, player.y, enemy.x, enemy.y, elapsed_time)

                            
                            enemy.make_invulnerable(elapsed_time)

                        
        # Upgrade Basic_attack

        if player.xp >= 10*(1.1**(player.level-1)) and player.xp != 0:
           self.level_up(player)
           player.xp = 0
           player.level += 1

        # Spawn Enemies
        
        if len(enemies) <= 500:
            spawn_rate = int(0.318519 * (elapsed_time ** 0.6231684))  # metade da fórmula original
        elif len(enemies) > 500:
            spawn_rate = 0
            for enemy in enemies:
                distance = math.hypot(player.x - enemy.x, player.y - enemy.y)
                if distance > 1000:
                    if enemy != self.boss:
                        enemies.remove(enemy)       
        else:
            spawn_rate = 5

        if elapsed_time != self.last_spawn:

            for i in range(spawn_rate):

                bool_spawn = True

                



                distancia_minima = math.sqrt(self.display.get_width()**2 + self.display.get_height()**2) / 2 - 100

                # Escolhe um ângulo aleatório (em radianos)
                angulo = random.uniform(0, 2 * math.pi)

                # Calcula a posição de spawn fora do campo de visão
                spawn_x = player.x + math.cos(angulo) * distancia_minima
                spawn_y = player.y + math.sin(angulo) * distancia_minima
                # Verificar se a posição de spawn está fora da área visível

                spawn_x = int(max(0, min(spawn_x, self.walls.get_width() - 1)))
                spawn_y = int(max(0, min(spawn_y, self.walls.get_height() - 1)))

                

        
                enemies.append(ZombieTwo(spawn_x, spawn_y))
                enemies.append(ZombieOne(spawn_x, spawn_y))
                enemies.append(ZombieThree(spawn_x, spawn_y))
                enemies.append(ZombieFour(spawn_x, spawn_y))
                enemies.append(ZombieFive(spawn_x, spawn_y))

               # Verifica se o boss já está em campo ou morrendo
                boss_exists = any(isinstance(e, ZombieBoss) and not e.is_dying for e in enemies)

                # Condições para spawn do boss
                can_spawn_boss = self.boss_can_spawn

                if  self.last_boss_death_time is not None and elapsed_time - self.last_boss_death_time >= self.boss_respawn_delay:
                    return True  # Respawn após morte"""

                if can_spawn_boss:
                    self.boss = ZombieBoss(2000, 3700)  # Posição inicial do boss
                    enemies.append(self.boss)
                    self.boss_can_spawn = False  # Desabilita o spawn do boss após o primeiro spawn
                
                if self.boss is not None:
                    print("Boss Spawned at:", self.boss.x, self.boss.y)
                #enemies.append(Enemy_one(random.randint(1000, 2550), random.randint(1500, 3300)))

                cracha_radius = self.active_weapons['Cracha'].radius

                

                self.last_spawn = elapsed_time

                spawn_rate += 1



        # Move Enemies

        current_time = pygame.time.get_ticks() / 1000

        for enemy in enemies:

            enemy.move(player, self.mask)

            enemy.update_death(current_time)
            enemy.draw(self.display, offset_x, offset_y)


        # Check if enemies hit player

        for enemy in enemies:

            # Cálculo da distância
            distance = math.hypot(player.x - enemy.x, player.y - enemy.y)

            # Início do ataque (só acontece uma vez)
            if distance < 35 and not player.invulnerable and not enemy.is_dying and not enemy.atack:
                enemy.atack = True
                enemy.atack_frame_timer = 0
                enemy.atack_frame_index = 0

            # Atualiza a animação do ataque em todo frame, se estiver atacando
            if enemy.atack:
                enemy.update_atack(current_time, player)




        if player.health <= 0:

            return True


        # Handle enemy death and removal
        for enemy_one in enemies[:]:
            if enemy_one.life <= 0 and not enemy_one.is_dying:
                enemy_one.is_dying = True
                enemy_one.death_frame_timer = 0
            elif enemy_one.marked_for_removal:
                if isinstance(enemy_one, ZombieBoss):
                    self.last_boss_death_time = elapsed_time  # Registra o tempo da morte do boss
                enemies.remove(enemy_one)
                player.xp += 1

        # Mostrar FPS, tempo, vida e XP

        fps = int(self.clock.get_fps())

        fps_text = my_font.render(f"FPS: {fps}", True, (0, 0, 255))

        self.display.blit(fps_text, (10, 10))



        # Mostrar o tempo total de jogo

        #time_text = my_font.render(f'Time: {elapsed_time}s', True, (255, 255, 0))

        #self.display.blit(time_text, (self.w//2, 10))


        # Mostrar a vida do jogador


        health_text = my_font.render(f'Vida: {player.health:.2f}/{player.max_health:.2f}', True, (255, 0, 0), (200,200,200))

        self.display.blit(health_text, (10, self.h - 30))

        # Mostrar a pontuação do jogador

        xp_text = my_font.render(f'XP: {player.xp}', True, (0, 255, 0))

        self.display.blit(xp_text, (self.w//2, self.h - 30))


        pygame.display.flip()

        self.clock.tick(120)


        return False

        #x=2050 a 2210 y= 4600

game = Vampire_Cinvivals(1200, 800)

player = Player(x=2100, y= 4800)

enemies = []

bottles = []

game_over = False

try_again = True 

start_time = pygame.time.get_ticks()  # Tempo inicial do jogo


game.main_menu(game)

while try_again:
    
    while not game_over:

        # Calcula o tempo total de jogo em segundos

        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

        game_over = game.play_step(player, enemies, elapsed_time)

        won = game.victory
        if won:
            break
    if won:
        print("Você venceu!")
        game_over = False
        try_again = False
    else:
        try_again, game_over = game.game_over()

  # Ajusta o volume do som de vitóriap

game.victory_screen(game)

pygame.quit()