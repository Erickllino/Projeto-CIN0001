import pygame

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
        self.frame = 0
        self.animation_speed = 0.1
        self.last_update = 0
        self.direction = 'right'
        self.moving = False
        self.sprites = {
            "right": [pygame.image.load(f"sprites/personagem_direita/frame{i}.png") for i in range(8)],
            "left": [pygame.image.load(f"sprites/personagem_esquerda/frame{i}.png") for i in range(8)]
        }
        self.sprite_width = 64
        self.sprite_height = 64
        for direction in self.sprites:
            self.sprites[direction] = [pygame.transform.scale(sprite, (self.sprite_width, self.sprite_height)) 
                                     for sprite in self.sprites[direction]]

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
        self.moving = False

        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.direction = 'left'
            self.moving = True
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            self.direction = 'right'
            self.moving = True
        if keys[pygame.K_UP]:
            dy = -self.speed    
            self.moving = True
        if keys[pygame.K_DOWN]:
            dy = self.speed
            self.moving = True
        if keys[pygame.K_TAB]:
            pygame.quit()


        new_x = max(self.radius, min(map_size[0] - self.radius, self.x + dx))
        new_y = max(self.radius, min(map_size[1] - self.radius, self.y + dy))

        # Check collision with map
        if not mask.overlap_area(pygame.mask.Mask((self.radius * 2, self.radius * 2), fill=True), (new_x - self.radius, self.y - self.radius)):
            self.x = new_x
        if not mask.overlap_area(pygame.mask.Mask((self.radius * 2, self.radius * 2), fill=True), (self.x - self.radius, new_y - self.radius)):
            self.y = new_y




    def update_animation(self, current_time):
        if self.moving:
            
            if current_time -self.last_update >= self.animation_speed:
                self.frame = (self.frame + 1) %8 #8 frames de animação
                self.last_update = current_time
        else:
            self.frame = 0 #volta pro primeirp frma quando para
            
    def update_som_catraca(self):
        if 2050 <= self.x <= 2210 and 4600 < self.y < 4500:

            if not self.som_catraca_tocado:     
                self.som_catraca.play()
                self.som_catraca.play()
                self.som_catraca_tocado = True
        else:
            self.som_catraca_tocado = False
                         
    def draw(self, game_window, center, map_size, window_size, offset_x, offset_y):
    # Atualiza a animação com o tempo atual
        current_time = pygame.time.get_ticks() / 1000  # Em segundos
        self.update_animation(current_time)

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
        
        # Desenha o sprite animado do jogador
        
        current_sprite = self.sprites[self.direction][self.frame]
        sprite_rect = current_sprite.get_rect(center=(int(draw_x), int(draw_y)-15))
        game_window.blit(current_sprite, sprite_rect)



