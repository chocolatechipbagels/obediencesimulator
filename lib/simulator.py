'''This script is part of the obedience simulator program
It was made to test the chance of success of the protagonist Weezing of Pikasprey Yellow's Oct 6, 2023 youtube video,
   Soft Lock Picking: The Worst Bug Catcher Battle, https://www.youtube.com/watch?v=3DF8XOhsFyg
 As such, it supports the Generation III obedience calculations, for a level 100 Weezing with Explosion and Self-Destruct
    vs a level 9 Weedle with Poison Sting (Poison Physical 15 BP 35 PP 100 Acc, non-intrusive secondary effect) and String Shot (40 PP non-intrusive Status)
 As of 10/8/2023, this script is only built for this specific use case
 This script can be expanded to more general purposes but the work required was deemed outside the scope
 Ways to expand this script are detailed in TODOs sprinkled throughout the functions
 I will probably not do it anytime soon if at all'''

import random
import math
from lib.inputs import PKMNInputs
from lib.analysis import OSAnalysis

class Simulator:

    def __init__(self):
        self.name = 'Obedience Simulator'
        self.inputs = PKMNInputs()
        self.disobedience_thresholds = [
            self.inputs.player_stats['Level'] - self.inputs.obedience_cap,
            2 * (self.inputs.player_stats['Level'] - self.inputs.obedience_cap)]

        # variables overwriting every turn
        self.r1 = 0
        self.r2 = 0
        self.r3 = 0
        self.asleep = False
        self.sleep_counter = 0
        self.weezing_hp = 0
        self.weedle_hp = 0
        self.poisonsting_pp = 0
        self.stringshot_pp = 0



    def obedience_check(self):
        self.r1 = random.randint(0, 255)
        obedience_check = self.inputs.obedience_modifier * self.r1
        # if True, the player's pokemon WILL disobey
        return obedience_check > self.inputs.obedience_cap

    # Because Weezing has only one attack, it cannot disobedient attack (use a different move than the one selected)

    # def disobedient_attack_check(self):
    #     self.r2 = random.randint(0, 255)
    #     disobedient_attack = self.inputs.obedience_modifier * self.r2
    #     return disobedient_attack > self.inputs.obedience_cap

    def disobedient_action(self):
        self.r3 = random.randint(0, 255)
        if self.r3 < self.disobedience_thresholds[0]:
            return 'fall asleep'
        elif self.disobedience_thresholds[0] <= self.r3 < self.disobedience_thresholds[1]:
            return 'confusion damage'
        else:
            return 'nothing'

    def sleep_check(self, sleep_counter):
        wakeup_chance = [0.2, 0.25, 0.333, 0.5, 1]
        #if True, Weezing WILL wake up
        return random.random() <= wakeup_chance[sleep_counter]

    def simulate_turn(self):
        # TODO: these functions have a lot of shortcuts which make this program only useful in this use case
        # this is because the use case is very specific
        # for example, Weezing cannot ever be slower than Weedle even at -6 Speed (0.25 * 140 = 35 > 16)
        # therefore, I will hardcode Weezing always going first
        # as another example, I will not bother to code sleep talk or status effects besides sleep
        weezing_status = self.weezing_turn()
        if weezing_status == 'terminated':
            return 'terminated'
        elif self.weezing_hp <= 0:
            # print("Weezing has been overwhelmed by the might of Weedle")
            return 'overwhelmed'
        else:
            damage = self.weedle_turn()
            if self.weedle_hp <= 0:
                print('Weezing has succeeded!')
                return 'success!'
            elif self.weezing_hp <= 0:
                # print("Weezing has been overwhelmed by the might of Weedle")
                return 'overwhelmed'
            return 'continue'

    def weezing_turn(self):
        # Weezing turn
        # all effects from weezing's turn are saved herein
        if self.asleep:
            if not self.sleep_check(self.sleep_counter):
                self.sleep_counter = self.sleep_counter + 1
                #print('Weezing is still asleep')
                return 'asleep'
            else:
                self.asleep = False
                self.sleep_counter = 0

        if self.obedience_check():
            # print('Weezing has been disobedient')
            effect = self.disobedient_action()
            if effect == 'fall asleep':
                self.asleep = True
                #print('Weezing fell asleep')
                return 'asleep'
            elif effect == 'confusion damage':
                damage = self.attack(self.inputs.player_stats['Level'], self.inputs.player_stats['Atk'], self.inputs.player_stats['Def'], confusion=True, struggle=False)
                self.weezing_hp = self.weezing_hp - damage
                #print('Weezing attacked itself')
                return 'confusion'
            else:
                #self.weezing_hp = self.weezing_hp
                #print('Weezing did nothing')
                return 'nothing'
        else:
            #print(f'Weezing has exploded with {self.weezing_hp} hp remaining')
            return 'terminated'


    def weedle_turn(self):
        # Weedle turn
        # all effects from weedle's turn are saved herein
        if self.poisonsting_pp > 0 and self.stringshot_pp > 0:
            current_attack = random.getrandbits(1)
            if current_attack == 0:
                self.poisonsting_pp = self.poisonsting_pp - 1
                return self.attack(self.inputs.enemy_stats['Level'], self.inputs.enemy_stats['Atk'], self.inputs.player_stats['Def'], confusion=False, struggle=False)
            else:
                self.stringshot_pp = self.stringshot_pp - 1
                return 0
        elif self.poisonsting_pp == 0 and self.stringshot_pp > 0:
            self.stringshot_pp = self.stringshot_pp - 1
            return 0
        elif self.poisonsting_pp > 0 and self.stringshot_pp == 0:
            self.poisonsting_pp = self.poisonsting_pp - 1
            return self.attack(self.inputs.enemy_stats['Level'], self.inputs.enemy_stats['Atk'], self.inputs.player_stats['Def'], confusion=False, struggle=False)
        else:
            damage = self.attack(self.inputs.enemy_stats['Level'], self.inputs.enemy_stats['Atk'], self.inputs.player_stats['Def'], confusion=False, struggle=True)
            if damage / 4 < 1:
                self.weedle_hp = self.weedle_hp - 1
            else:
                self.weedle_hp = self.weedle_hp - int(math.floor(damage / 4))
            return damage


    def attack(self, level, attack, defense, confusion, struggle):
        # TODO: this function has a lot of shortcuts which are only useful in this use case
        # for example, all secondary effects are NOT coded in as none are relevant to the use case
        # all status moves are NOT coded in for the same reason, instead they have their PP subtracted and it is
        #   considered an empty turn
        # all stat modifiers are NOT coded in for the same reason
        # confusion damage is treated separately although it still uses the same formula
        # finally, in this use case weezing cannot be the attacker, as it would instantly lose the match
        # otherwise, the damage calculation is sound

        # DAMAGE = (((( 2 * LEVEL ) / 5) + 2) * BP * ( ATTACK / DEFENSE )) / 50 ) + 2) * CRIT * TYPE EFFECTIVENESS * RANDOMNESS

        crit = 1
        type_eff = 1
        if not confusion and not struggle:
            crit_check = random.random()
            if crit_check <= 0.0625:
                crit = 2
            else:
                crit = 1
            # hardcoded to use case
            type_eff = 0.5
            bp = 15
        elif confusion:
            bp = 40
        else:
            bp = 50

        randomness = random.randint(85, 100) / 100

        damage = (((((( 2 * level) / 5) + 2) * bp * ( attack / defense )) / 50 ) + 2) * crit * type_eff * randomness
        if damage < 1:
            return 1
        else:
            return int(math.floor(damage))

    def run(self):
        self.inputs.run()
        print('Welcome to the Obedience Simulator')
        print('Your Weezing is being very naughty')
        print('In your anger you instruct your pet Weezing to explode')
        print('Can Weezing survive your emotional abuse to defeat Bug Catcher Sammy?')

        terminate = False

        self.disobedience_thresholds = [
            self.inputs.player_stats['Level'] - self.inputs.obedience_cap,
            2 * (self.inputs.player_stats['Level'] - self.inputs.obedience_cap)]

        maxiter_str = input('Enter the total number of attempts you want Weezing to make (start at 1000 if unsure and work your way up) ')
        iter = 0
        try:
            maxiter = int(maxiter_str)
        except Exception as e:
            print(e)
            print('your stupid value has been replaced with one million')
            maxiter = 1000000
        success = [0]*maxiter
        remaining_hp = []

        while iter < maxiter:
            #print(f'Iteration: {iter}')
            self.weezing_hp = self.inputs.player_stats['HP']
            self.weedle_hp = self.inputs.enemy_stats['HP']
            self.poisonsting_pp = self.inputs.enemy_moves[0]['PP']
            self.stringshot_pp = self.inputs.enemy_moves[1]['PP']
            while not terminate:
                status = self.simulate_turn()
                if status == 'terminated':
                    #print('Weezing succumbed')
                    remaining_hp.append(self.weezing_hp)
                    terminate = True
                elif status == 'overwhelmed':
                    terminate = True
                elif status == 'success!':
                    #print('Weezing did it!')
                    success[iter] = 1
                    terminate = True

            terminate = False
            iter = iter + 1

        successes = sum(success)
        winrate = round((successes / len(success)) * 100, 5)
        averagehp = (sum(remaining_hp) / len(remaining_hp))


        output0 = f'Weezing won {successes} of {maxiter} attempts, with a win rate of {winrate}%'
        output1 = f'Weezing had on average {averagehp} / {self.inputs.player_stats["HP"]} hp left at time of detonation'

        outputs = [output0, output1, '\n']
        OSAnalysis().log_outputs(outputs)
        OSAnalysis().print_outputs(outputs)








