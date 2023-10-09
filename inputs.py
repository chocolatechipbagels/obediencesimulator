
'''This script is part of the obedience simulator program
It was made to test the chance of success of the protagonist Weezing of Pikasprey Yellow's Oct 6, 2023 youtube video,
   Soft Lock Picking: The Worst Bug Catcher Battle, https://www.youtube.com/watch?v=3DF8XOhsFyg
 As such, it supports the Generation III obedience calculations, for a level 100 Weezing with Explosion and Self-Destruct
    vs a level 9 Weedle with Poison Sting (Poison Physical 15 BP 35 PP 100 Acc, non-intrusive secondary effect) and String Shot (40 PP non-intrusive Status)
 As of 10/8/2023, this script is only built for this specific instance
 This script can be expanded to more general purposes but the work required was deemed outside the scope
 Ways to expand this script are detailed in TODOs sprinkled throughout the functions
 There may be other ways which I did not consider or are outside the scope of even a finished version of this script,
 e.g. expanding to other generations,
 I will probably not do it anytime soon if at all'''


class PKMNInputs:

    def __init__(self):
        self.name = 'Pokemon Inputs for Obedience Simulator'
        self.badge_obedience = [10, 20, 30, 40, 50, 60, 70, 80, 100]
        self.obedience_cap = 0
        self.obedience_modifier = 0
        self.enemy_stats = {'Name': '', 'Type': [''], 'Level': 1, 'HP': 0, 'Atk': 0, 'Def': 0, 'SpAtk': 0, 'SpDef': 0, 'Spd': 0}
        self.enemy_moves = []
        self.player_stats = {'Name': '', 'Type': [''], 'Level': 1, 'HP': 0, 'Atk': 0, 'Def': 0, 'SpAtk': 0, 'SpDef': 0, 'Spd': 0}
        self.player_moves = []
        self.move_template = {'Name': '', 'Type': '', 'Category': '', 'BP': 0, 'PP': 1, 'Accuracy': 0}
        self.possible_categories = ['status', 'physical', 'special']
        # the following variable is hardcoded to my use case
        # TODO: expand the use case
        self.possible_types = ['poison', 'normal', 'bug']


    def save_inputs(self, badges, enemy_stats, enemy_moves, player_stats, player_moves):
        self.enemy_stats = enemy_stats
        self.enemy_moves = enemy_moves
        self.player_stats = player_stats
        self.player_moves = player_moves

        self.obedience_cap = self.badge_obedience[badges]
        self.obedience_modifier = (self.player_stats['Level'] + self.obedience_cap) / 256
        return


    def all_that_was_a_waste_of_time(self):
        self.save_inputs(badges=0,
                         enemy_stats={'Name': 'Weedle', 'Type': ['Bug', 'Poison'], 'Level': 9, 'HP': 28, 'Atk': 14, 'Def': 13, 'SpAtk': 11, 'SpDef': 11, 'Spd': 16},
                         enemy_moves=[{'Name': 'Poison Sting', 'Type': 'Poison', 'Category': 'Physical', 'BP': 15, 'PP': 35, 'Accuracy': 100},
                                      {'Name': 'String Shot', 'Type': 'Bug', 'Category': 'Status', 'BP': 0, 'PP': 40, 'Accuracy': 95}],
                         player_stats={'Name': 'Weezing', 'Type': ['Poison'], 'Level': 100, 'HP': 334, 'Atk': 237, 'Def': 339, 'SpAtk': 206, 'SpDef': 176, 'Spd': 140},
                         player_moves=[{'Name': 'Explosion', 'Type': 'Normal', 'Category': 'Physical', 'BP': 500, 'PP': 5, 'Accuracy': 100}],
                         )
        return 'mission was bypassed successfully'

    def run(self):
        inputs_saved = self.all_that_was_a_waste_of_time()
        if 'succ' not in inputs_saved:
            return 'error'

        return 'mission was completed successfully'






