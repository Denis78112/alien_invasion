import sys
from time import sleep
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


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

        #Экземпряр для хранения статистики
        #Создание экземпляра класса для хранения игровой статистики.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        #Создание кнопки Play
        self.play_button = Button(self, "PLAY")





    def run_game(self):
        """Запуск основоного цикла игры"""
        while True:
            #Отлслеживание событий клавиатуры и мыши.
            
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()  
            
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """запускает новую игру при нажатии кнопки PLAY"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #Сброс игровых настроек.
            self.settings.initialize_dynamic_settings()
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            #Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            #Создание нового флота и размещение корабля в центре
            self._create_fleet()
            self.ship.center_ship()

            #Указатель мыши скрывается.
            pygame.mouse.set_visible(False)




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

    def _update_aliens(self):
        """Обновляет позиции всех пришельцев."""
        self._check_fleet_edges()
        self.aliens.update()

        #Проверка коллизий пришелец-корабль.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #Проверить добрались ли пришельцы до нижнего края экрана.
        self._check_aliens_bottom()


    def _check_aliens_bottom(self):
        """Проверяет, добрались ли пришельцы до нижнего края экрана"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #Происходит то же, что и при столконовении с кораблем.
                self._ship_hit()
                break
        


    def _ship_hit(self):
        """Обрабатывает столконовения коробля с пришельцами"""
        if self.stats.ship_left > 0:

            #уменьшает ship_left
            self.stats.ship_left -= 1

            #Очистка списков пришельцев и снарядов.
            self.aliens.empty()
            self.bullets.empty()

            #Создание нового флота и размещение корабля в центре.
            self._create_fleet()
            self.ship.center_ship()

            #Пауза
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)



    def _update_bullets(self):
        """Обновляет позиции снарядов и уничтожает снаряды"""
        #обновление позиций снарядов
        self.bullets.update()
            #Удаление снарядов выведших за пределы экрана.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    
    def _check_bullet_alien_collisions(self):
        """Обработка коллизий снарядов с пришельцами"""

        if not self.aliens:
            #Уничтожение существующих снарядов и создание нового флота.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

        #При проверке попаданий пришельцев.
        #При обнурежении попадания удалить снаряд и пришельца.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            


    def _create_fleet(self):
        """Создание флота вторжения"""

        #создание пришельца и вычисление колличества пришельцев в ряду
        # интервал между соседними пришельцами равен ширине пришельца.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_widht - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        """Определяет колличество рядов, помещающихся на экране."""
        ship_height = self.ship.rect.height
        avilable_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = avilable_space_y // (2 * alien_height)

              
        #Создание флота вторжения
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Создание пришельца и размещение его в ряду"""
        #Создание первого ряда пришельцев
        alien = Alien(self)

        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        """"Реагирует на достижение пришельцами края экрана"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        """Опускает весь флот и менят направление флота."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1



    def _update_screen(self):
        """Обновляет изображение на экране и отображает новый экран"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.sb.show_score()

        #Кнопка Play отображается в том случае, если игра не активна
        if not self.stats.game_active:
            self.play_button.draw_button()
          
        #Отображение последнего прорисованного экрана.
        pygame.display.flip()

            


if __name__ == '__main__':
    #Создание экзепляра класса и запуск игры.
    ai = AlienInvasion()
    ai.run_game()

