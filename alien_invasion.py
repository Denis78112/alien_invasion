import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienInvasion:
    """Класс для управления ресурсами и поведением игры"""
    def __init__(self):
        """Инициализирует игру и создает игровые ресурсы"""
        pygame.init()
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self. settings.screen_widht = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()


    def run_game(self):
        """Запуск основоного цикла игры"""
        while True:
            #Отлслеживание событий клавиатуры и мыши.
            
            self._check_events()
            self.ship.update()
            self.bullets.update()
            #Удаление снарядов выведших за пределы экрана.
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

           

            self._update_screen()

            #при каждом проходе цикла перерисовывается экран
            self.screen.fill(self.settings.bg_color)


    def _check_events(self):
        """Отрабатывает нажатия клавиш и события мыши"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
                                
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """Реагирует на нажатие клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        

    def _check_keyup_events(self, event):
        """Реагирует на отпускание клавиш."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Создание нового снаряда и включение его в группу bullets."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)       

    def _update_screen(self):
         """Обновляет изображение на экране и отображает новый экран"""
         self.screen.fill(self.settings.bg_color)
         self.ship.blitme()
         for bullet in self.bullets.sprites():
             bullet.draw_bullet()
        

            

        #Отображение последнего прорисованного экрана.
         pygame.display.flip()

            


if __name__ == '__main__':
    #Создание экзепляра класса и запуск игры.
    ai = AlienInvasion()
    ai.run_game()

