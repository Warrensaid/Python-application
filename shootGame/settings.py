class Settings():
    '''the settings of the game'''

    def __init__(self):
        # screen setting
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230,230,230)
        # tank settings
        self.tank_limits = 3

        # bullets settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_number = 5
        # enemies settings
        self.fleet_speed_factor = 30
        # game speed scale
        self.speedup_scale = 1.1
        # enemy score scale
        self.score_scale = 2
        # highest score
        self.high_score = 0
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.tank_speed_factor = 2
        self.bullet_speed_factor = 5
        self.enemy_speed_factor = 1
        # 1 is right, -1 is left
        self.fleet_direction = 1
        self.enemy_points = 5

    def increase_speed(self):
        '''increase the game speed'''
        self.tank_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.enemy_speed_factor *= self.speedup_scale

        self.enemy_points = int(self.enemy_points * self.score_scale)
        print(self.enemy_points)