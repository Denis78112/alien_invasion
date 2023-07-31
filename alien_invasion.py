import sys
import pygame
from settings import Settings
from ship import Ship

class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((self.settings.screen_widht, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(screen)


    def run_game(self):
        """Запуск основоного цикла игры"""
        while True:
            #Отлслеживание событий клавиатуры и мыши.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            #при каждом проходе цикла перерисовывается экран
            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            

            #Отображение последнего прорисованного экрана.
            pygame.display.flip()

if __name__ == '__main__':
    #Создание экзепляра класса и запуск игры.
    ai = AlienInvasion()
    ai.run_game()

