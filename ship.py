import pygame

class Ship():
    """Класс для управления кораблем"""
    def __init__(self, ai_game):
        """Инициализирует корабль и задает его начальную позицию"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        #Загружает изображение корабля и получает прямоугольник.
        self.image = pygame.image.load('images/crash_course12-01.png')
        self.rect = self.image.get_rect()
        #Каждый новый корабль появляется у нижнего крапя экрана.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """рисует корабль в текущей позиции"""
        self.screen.blit(self.image, self.rect)
        