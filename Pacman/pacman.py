import pygame
from abc import ABCMeta, abstractmethod
import random

pygame.init()

screen = pygame.display.set_mode((560, 580), 0)
fonte = pygame.font.SysFont("arial", 24, True, False)

AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
LARANJA = (255, 165, 0)
ROSA = (255, 105, 180)
CIANO = (0, 206, 209)
BRANCO = (255, 255, 255)
VELOX = 1
CIMA = 1
BAIXO = 2
DIREITA = 3
ESQUERDA = 4


class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass

    @abstractmethod
    def calcular_regras(self):
        pass

    @abstractmethod
    def processar_eventos(self, eventos):
        pass


class Movimento(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass

    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass


class Cenario(ElementoJogo):
    def __init__(self, tamanho, pacmanzim):
        self.pacman = pacmanzim
        self.personagens = []
        self.tamanho = tamanho
        self.pontos = 0
        # Possiveis estados para pausar o jogo -- 0 - play / 1 - pause / 2 - game over / 3 - win
        self.estado = 0
        self.life = 5
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    def adicionar_movimento(self, personage):
        self.personagens.append(personage)

    def pintar_score(self, tela):
        pontos_x = 30 * self.tamanho
        img_pontos = fonte.render("Score: {}".format(self.pontos), True, AMARELO)
        img_vidas = fonte.render("Lifes: {}".format(self.life), True, AMARELO)
        tela.blit(img_pontos, (10, 555))
        tela.blit(img_vidas, (150, 555))

    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha):
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            half = self.tamanho // 2
            cor = PRETO
            if coluna == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, AMARELO, (x + half, y + half),
                                   self.tamanho // 10, 0)

    def pintar(self, tela):
        if self.estado == 0:
            self.pintar_play(tela)
        elif self.estado == 1:
            self.pintar_play(tela)
            self.pintar_pause(tela)
        elif self.estado == 2:
            self.pintar_play(tela)
            self.pintar_gameover(tela)
        elif self.estado == 3:
            self.pintar_play(tela)
            self.pintar_win(tela)

    def pintar_texto_centro(self, tela, texto):
        texto_img = fonte.render(texto, True, AMARELO)
        texto_x = (tela.get_width() - texto_img.get_width()) // 2
        texto_y = (tela.get_height() - texto_img.get_height()) // 2
        tela.blit(texto_img, (texto_x, texto_y))

    def pintar_win(self, tela):
        self.pintar_texto_centro(tela, "Y O U  W O N !")

    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, "G A M E  O V E R")

    def pintar_pause(self, tela):
        self.pintar_texto_centro(tela, "P A U S E")

    def pintar_play(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_score(tela)

    def get_direcao(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(CIMA)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(BAIXO)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIREITA)
        return direcoes

    def calcular_regras(self):
        if self.estado == 0:
            self.calcular_regras_play()
        elif self.estado == 1:
            self.calcular_regras_pause()
        elif self.estado == 2:
            self.calcular_regras_gameover()

    def calcular_regras_gameover(self):
        pass

    def calcular_regras_pause(self):
        pass

    def calcular_regras_play(self):
        for movimento in self.personagens:
            lin = int(movimento.linha)
            col = int(movimento.coluna)
            lin_intencao = int(movimento.linha_intencao)
            col_intencao = int(movimento.coluna_intencao)
            direcoes = self.get_direcao(lin, col)
            if len(direcoes) >= 3:
                movimento.esquina(direcoes)
            if isinstance(movimento, Fantasma) and \
                    movimento.linha == self.pacman.linha and \
                    movimento.coluna == self.pacman.coluna:
                self.life -= 1
                if self.life <= 0:
                    self.estado = 2
                else:
                    self.pacman.linha = 1
                    self. pacman.coluna = 1
            else:
                if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and \
                        self.matriz[lin_intencao][col_intencao] != 2:
                    movimento.aceitar_movimento()
                    if isinstance(movimento, Pacman) and self.matriz[lin][col] == 1:
                        self.pontos += 1
                        self.matriz[lin][col] = 0
                        if self.pontos >= 305:
                            self.estado = 3
                else:
                    movimento.recusar_movimento(direcoes)

    def processar_eventos(self, event):
        for e in event:
            if e.type == pygame.QUIT:
                exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.estado == 0:
                        self.estado = 1
                    else:
                        self.estado = 0


class Pacman(ElementoJogo, Movimento):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.vel_x = 0
        self.vel_y = 0
        self.raio = self.tamanho // 2
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.movimento_boca = 0
        self.veloxboca = 1

    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)

    def pintar(self, tela):
        # Desenhar o corpo do Pacman
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio, 0)

        # Movimento boca do pacman
        self.movimento_boca += self.veloxboca
        if self.movimento_boca > self.raio:
            self.veloxboca = -1
        if self.movimento_boca <= 0:
            self.veloxboca = 1

        # Desenhar a boca do Pacman
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.movimento_boca)
        labio_inferior = (self.centro_x + self.raio, self.centro_y + self.movimento_boca)
        pontos = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos, 0)

        # Desenhar o Olho do Pacman
        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.70)
        olho_raio = int(self.raio / 10)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)

    def processar_eventos(self, eventos):
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = VELOX
                elif e.key == pygame.K_LEFT:
                    self.vel_x = -VELOX
                elif e.key == pygame.K_UP:
                    self.vel_y = -VELOX
                elif e.key == pygame.K_DOWN:
                    self.vel_y = VELOX
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = 0
                elif e.key == pygame.K_LEFT:
                    self.vel_x = 0
                elif e.key == pygame.K_UP:
                    self.vel_y = 0
                elif e.key == pygame.K_DOWN:
                    self.vel_y = 0

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna

    def esquina(self, direcoes):
        pass


class Fantasma(ElementoJogo):
    def __init__(self, cor, tamanho):
        # Onde nasce os fantasmas
        self.coluna = 13.0
        self.linha = 15.0
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.veloxfantasma = 1
        self.direcao = BAIXO
        self.cor = cor
        self.tamanho = tamanho

    def pintar(self, tela):
        fatia = self.tamanho // 8
        pixel_x = int(self.coluna * self.tamanho)
        pixel_y = int(self.linha * self.tamanho)
        contorno = [(pixel_x, pixel_y + self.tamanho),
                    (pixel_x + fatia, pixel_y + fatia * 2),
                    (pixel_x + fatia * 2, pixel_y + fatia // 2),
                    (pixel_x + fatia * 3, pixel_y),
                    (pixel_x + fatia * 5, pixel_y),
                    (pixel_x + fatia * 6, pixel_y + fatia // 2),
                    (pixel_x + fatia * 7, pixel_y + fatia * 2),
                    (pixel_x + self.tamanho, pixel_y + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno, 0)

        olho_raio_ext = fatia
        olho_raio_int = fatia // 2

        olho_esq_x = int(pixel_x + fatia * 2.5)
        olho_esq_y = int(pixel_y + fatia * 2.5)

        olho_dir_x = int(pixel_x + fatia * 5.5)
        olho_dir_y = int(pixel_y + fatia * 2.5)

        pygame.draw.circle(tela, BRANCO, (olho_esq_x, olho_esq_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_esq_x, olho_esq_y), olho_raio_int, 0)
        pygame.draw.circle(tela, BRANCO, (olho_dir_x, olho_dir_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_dir_x, olho_dir_y), olho_raio_int, 0)

    def calcular_regras(self):
        if self.direcao == CIMA:
            self.linha_intencao -= self.veloxfantasma
        elif self.direcao == BAIXO:
            self.linha_intencao += self.veloxfantasma
        elif self.direcao == ESQUERDA:
            self.coluna_intencao -= self.veloxfantasma
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.veloxfantasma

    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)

    def processar_eventos(self, event):
        pass


if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    cenario = Cenario(size, pacman)
    blinky = Fantasma(VERMELHO, size)
    inky = Fantasma(CIANO, size)
    clyde = Fantasma(LARANJA, size)
    pinky = Fantasma(ROSA, size)
    cenario.adicionar_movimento(pacman)
    cenario.adicionar_movimento(blinky)
    cenario.adicionar_movimento(inky)
    cenario.adicionar_movimento(clyde)
    cenario.adicionar_movimento(pinky)

    while True:
        # Regras
        pacman.calcular_regras()
        blinky.calcular_regras()
        inky.calcular_regras()
        clyde.calcular_regras()
        pinky.calcular_regras()
        cenario.calcular_regras()

        # Tela
        screen.fill(PRETO)
        cenario.pintar(screen)
        pacman.pintar(screen)
        blinky.pintar(screen)
        inky.pintar(screen)
        clyde.pintar(screen)
        pinky.pintar(screen)
        pygame.display.update()
        pygame.time.delay(100)

        # Eventos
        eventos = pygame.event.get()
        pacman.processar_eventos(eventos)
        cenario.processar_eventos(eventos)
