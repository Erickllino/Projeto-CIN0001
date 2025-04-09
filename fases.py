import pygame
import random

class Fase:
    def __init__(self, dados_fase):
        self.numero = dados_fase["numero"]
        self.objetivos = dados_fase["objetivos"]
        self.instrucoes = dados_fase["instrucoes"]
        self.esta_concluida = False
        self.circulos = []
        self.tempo_inicial = 0
        self.contador = 0
        

    def iniciar(self):
        if self.numero == 1:
            self.circulos = [{
                "posicao": (600, 900),  # Coordenada do grad5
                "raio": 100,  # Aumentado para melhor visibilidade
            }]

        elif self.numero == 2:
            self.circulos = [{
                "posicao": (1200, 1200),  # Coordenada do grad4
                "raio": 100,  # Aumentado para melhor visibilidade
            }, {
                "posicao": (1400, 1250),  # Coordenada do grad2
                "raio": 100,  # Aumentado para melhor visibilidade
            }]


        elif self.numero == 3:
            self.circulos = [{
                "posicao": (600, 2750),  # Coordenada do grad4
                "raio": 20,  # Aumentado para melhor visibilidade
            }, {
                "posicao": (3150, 3200),  # Coordenada do grad2
                "raio": 20,  # Aumentado para melhor visibilidade
            }, {
                "posicao": (1900, 4600),  # Coordenada do grad2
                "raio": 20,  # Aumentado para melhor visibilidade
            }]

        elif self.numero == 4:
            self.circulos = [{
                "posicao": (3550, 4500),  # Coordenada próxima ao spawn do jogador
                "raio": 20,  # Aumentado para melhor visibilidade
            }]
    
    # essa função ta criando círculos aleatório pelo mapa
    #quando estiver com o mapa pronto e os objetos, tem que setar valores fixos para a criação dos círculos
    def _criar_circulos(self, quantidade):
        # Posição mais central no mapa
        self.circulos = [{
            "posicao": (random.randint(2000,3000), 3150),  # Coordenada próxima ao spawn do jogador
            "raio": 100,  # Aumentado para melhor visibilidade
        } for _ in range(quantidade)]

    def atualizar(self, posicao_jogador, tempo_atual):

        if self.esta_concluida:
            return

        if self.numero == 1 or self.numero == 2 or self.numero == 3 or self.numero == 4:
            # Verifica se o jogador está dentro de algum círculo

            jogador_dentro = False

            for circulo in self.circulos:
                distancia = pygame.math.Vector2(posicao_jogador).distance_to(circulo["posicao"])
                if distancia < circulo["raio"]:
                    jogador_dentro = True
                    break
 
            # Atualiza o contador de tempo para as questões 1 e 2
            if self.numero == 1 or self.numero == 2:
                if jogador_dentro:
                    if self.tempo_inicial == 0:
                        self.tempo_inicial = tempo_atual
                    else:
                        # Calcula o tempo decorrido desde que entrou no círculo
                        if tempo_atual - self.tempo_inicial >= 1:
                            self.tempo_inicial = tempo_atual
                            self.contador += 1

                else:

                    self.tempo_inicial = 0

            # para as questões 3 e 4 apenas é necessário checar a colisão
            elif self.numero == 3 or self.numero == 4:
                if jogador_dentro:
                    # Se o jogador estiver dentro do círculo, adiciona um ponto
                    self.contador += 1
                    self.circulos.remove(circulo)  # Remove o círculo coletado

            # Verifica se concluiu o tempo necessário
            if self.contador >= self.objetivos:
                self.esta_concluida = True
                self.circulos = []

            print(tempo_atual, self.tempo_inicial, self.contador)

    def desenhar(self, tela, offset_x, offset_y):

        fonte = pygame.font.Font(None, 36)
        texto = fonte.render(self.instrucoes, True, (200, 200, 200))  # Cinza
        tela.blit(texto, (20, 20))

        # Timer na tela
        if (self.numero == 1 or self.numero == 2) and not self.esta_concluida:
            tempo_restante = max(0, self.objetivos - self.contador)
            timer_texto = fonte.render(f"Tempo necessário restante: {tempo_restante}s", True, (200, 200, 200))
            tela.blit(timer_texto, (20, 60))

        elif (self.numero == 3 or self.numero == 4)and not self.esta_concluida:
            objetos_restantes =  self.objetivos - self.contador
            timer_texto = fonte.render(f"Objetivos não coletados: {objetos_restantes}s", True, (200, 200, 200))
            tela.blit(timer_texto, (20, 60))

        for circulo in self.circulos:
            x = circulo["posicao"][0] - offset_x
            y = circulo["posicao"][1] - offset_y

            surface = pygame.Surface((circulo["raio"] * 2, circulo["raio"] * 2), pygame.SRCALPHA)
            pygame.draw.circle(surface, (255, 0, 0, 150), (circulo["raio"], circulo["raio"]), circulo["raio"])
            tela.blit(surface, (x - circulo["raio"], y - circulo["raio"]))

# Configuração ajustada
dados_fase1 = {
    "numero": 1,
    "objetivos": 20,  # 30 segundos dentro do círculo
    "instrucoes": "Fique no círculo vermelho por 10 segundos!"
}

dados_fase2 = {
    "numero": 2,
    "objetivos": 40,  # 10 segundos dentro do círculo
    "instrucoes": "Um zumbi louco atacou a energia do grad em que você estava, vá para um novo grad e termine a segunda questão da lista!!"
}

dados_fase3 = {

    "numero": 3,
    "objetivos": 3,  # 10 segundos dentro do círculo
    "instrucoes": "você já tinha feito o código anteriormente, porém foi no papel a agora deve coletar os papéis rasgados pelo mapa para finalizar a questão 3!!!"
}

dados_fase4 = {
    "numero": 4,
    "objetivos": 1,  # 10 segundos dentro do círculo
    "instrucoes": "você achou a questão 4 muito difícil, procure um monitor que não tenha virado zumbi para lhe ajudar a finalizar a questão!!!"
}
