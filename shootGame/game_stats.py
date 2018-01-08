class Game_stats():
    ''' track game statistics'''
    def __init__(self, ai_settings):

        self.game_active = False
        self.ai_settings = ai_settings
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self):
        self.tanks_left = self.ai_settings.tank_limits
        self.score = 0
        self.level = 1