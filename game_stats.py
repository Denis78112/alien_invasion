class GameStats():
    """отслеживание статистики для игры Aliens Invasion"""
    def __init__(self, ai_game):
        """инициализирует статистику"""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """инициализирует статистику изменяющуюся в ходе игры"""
        self.ship_left = self.settings.ship_limit
        