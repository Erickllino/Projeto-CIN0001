# gerenciador_fases.py
class GerenciadorFases:
    def __init__(self):
        self.fase_atual = None
        self.fases = []
        self.fases_concluidas = []
        self.fase1_timer = 0
        self.fase1_completa = False  

    def adicionar_fase(self, fase):
        self.fases.append(fase)
    
    def iniciar_proxima_fase(self):
        if self.fases:
            self.fase_atual = self.fases.pop(0)
            self.fase_atual.iniciar()
            return True
        return False
    
    def atualizar(self, posicao_jogador, delta_tempo):
        if self.fase_atual and not self.fase_atual.esta_concluida:
            self.fase_atual.atualizar(posicao_jogador, delta_tempo)
    
    def desenhar(self, tela, offset_x, offset_y):
        if self.fase_atual:
            self.fase_atual.desenhar(tela, offset_x, offset_y)