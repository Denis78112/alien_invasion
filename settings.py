class Settings():
    """Класс для хранения всех настроек игры"""
    def __init__(self):
        """Инициализирует настройки игры"""
        #Параметры экрана
        self.screen_widht = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        #Настройки корабля
        self.ship_limit = 3
        
        #Параметры снаряда
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        #Настройки пришельцев
        self.fleet_drop_speed = 10

        #Темп ускорения игры
        self.speedup_scale = 1.1
        #Темп роста стоимости пришельцев
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Иннициализирует настройки изменяющиеся в ходе игры."""
        self. ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 0.5
        #ПОдсчет очков
        self.alien_points = 50


        # fleet_direction = 1 обозначает движение вправо; а -1 влево
        self.fleet_direction = 1

    def increase_speed(self):
        """Увеичивает настройки скорости"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.aliens_points = int(self.alien_points * self.score_scale)

