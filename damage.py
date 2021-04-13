import math
import random

def effective_raw(true_raw: int, sharpness: str, affinity: int, crit_boost=False):
    '''
    Takes final (after skills applied) values for raw, sharpness color and crit boost (yes no only level 3)
    returns effective raw
    '''
    sharpness_values = {
    'R': 0.50,
    'O': 0.75,
    'Y': 1.00,
    'G': 1.05,
    'B': 1.20,
    'W': 1.32,
    'P': 1.44
    }
    sharpness_adjusted = true_raw*sharpness_values[sharpness]
    crit_multiplier = 1.40 if crit_boost else 1.25
    affinity = min(affinity, 100)/100
    effective_damage = sharpness_adjusted * (1 - affinity + crit_multiplier * affinity)
    return int(effective_damage)

def attack_boost(base_raw: int, level: int):
    if level in (0, 1, 2, 3):
        return base_raw + level*3
    elif level in (4, 5):
        return base_raw * (1.01 + level/100) + level + 3
    elif level == 6:
        return base_raw * 1.08 + 9
    else:
        return base_raw * 1.10 + 10

def crit_boost(base_raw: int, affinity: int, level: int):
    affinity = min(affinity, 100)
    return base_raw + (base_raw * (0.25 + 0.05*level) * affinity/100)

def main_loop_basic_effective_raw():
        while True:
            values = input("Type [raw value], [sharpness letter], [affinity] and enter, q for quitting.\n").split()
            if 'q' in values:
                break
            assert len(values) >= 3
            raw, sharpness, affinity = int(values[0]), values[1].upper(), int(values[2])
            print(f"Effective raw is: {effective_raw(raw, sharpness, affinity)}")

def print_crit_boosted_values(raws: list, affinities: list):
    crit_boost_levels = range(4)
    for r in raws:
        out = f'Base raw: {r},'
        for i in crit_boost_levels:
            out += f' CB Level {i}:'
            for a in affinities:
                out += f' {int(crit_boost(r, a, i))}'
            out += ' | '
        print(out)

def print_attack_boosted_values(raws: list):
    attack_boost_levels = range(8)
    for r in raws:
        out = f'Base raw: {r}, attack boosted:'
        for i in attack_boost_levels:
            out += f' {int(attack_boost(r, i))}'
        print(out)

def test_brutal_strike_dps(raw: int, negative_affinity: int):
    damage_dealt = 0
    brutal_strike_chance = 20
    rounds = 100000
    no_aff_damage = raw * rounds
    non_brutal_damage = 0
    for _ in range(rounds):
        roll_crit = random.randint(1, 100)
        if roll_crit <= negative_affinity:
            non_brutal_damage += raw * 0.75
            roll_brutal = random.randint(1, 100)
            if roll_brutal <= brutal_strike_chance:
                damage_dealt += raw * 1.5
            else:
                damage_dealt += raw * 0.75
        else:
            non_brutal_damage += raw
            damage_dealt += raw
    print(f'Brutal damage dealt = {damage_dealt}, Non brutal damage = {non_brutal_damage}, No affinity damage = {no_aff_damage}')
    print(f'Damage multiplier vs non brutal: {damage_dealt/non_brutal_damage}')

    # When negative affinity = 100 this has the meaning of 'effective affinity multiplier'. 
    # Negative crits become effectively ~90% damage rather than 75%. 
    # The lower the negative affinity, the closer it is to 100%, decreasing to 90% when affinity is -100
    print(f'Damage multiplier vs zero affinity: {damage_dealt/no_aff_damage}') 
    
    print(f'Non brutal multiplier vs zero affinity: {non_brutal_damage/no_aff_damage}')

if __name__ == "__main__":
    #test_brutal_strike_dps(263, 5)
    #quit()
    #raws = [100, 130, 170, 200, 230]
    #affinities= [10, 30, 50, 70, 100]
    #263print_attack_boosted_values(raws)
    
        
    main_loop_basic_effective_raw()