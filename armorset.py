from weapon import Weapon

class ArmorSet():
    
    def __init__(self, weapon: Weapon, active_skills: str, powercharm: bool = True, powertalon: bool = True):
        self.skills_dict = {
            'AB'    : self.attack_boost,
            'CE'    : self.critical_eye,
            'WEX'   : self.weakness_exploit,
            'CB'    : self.critical_boost,
            'CD'    : self.critical_draw,
            'RESENTMENT' : self.resentment,
        }
        self.weapon:                Weapon = weapon
        self.attack:                int = weapon.attack
        self.affinity:              int = weapon.affinity
        self.sharpness_multiplier:  float = weapon.sharpness_multiplier
        self.crit_multiplier:       float = 1.25
        self.powercharm:            bool = powercharm
        self.powertalon:            bool = powertalon
        self.active_skills:         dict = self.parse_skills(active_skills)
        self.apply_skills()         # Applies skills to change the above stats 
        self.apply_powercharms()    # Applies powercharm / powertalon buffs after skills
        self.effective_raw:         int = self.calculate_effective_raw()

    def parse_skills(self, skills: str) -> dict:
        skills = skills.replace(',', '').upper().split()
        active_skills = {}
        for skill in skills:
            if not skill[-1].isnumeric:
                continue
            level = int(skill[-1])
            shortened_skill = skill[:-1]
            if shortened_skill in self.skills_dict.keys():
                active_skills[shortened_skill] = level
        return active_skills

    def apply_skills(self):
        for skill in self.active_skills.keys():
            skill_method = self.skills_dict[skill]
            skill_level = self.active_skills[skill]
            skill_method(skill_level)

    def calculate_effective_raw(self) -> int:
        sharpness_adjusted = self.attack*self.sharpness_multiplier
        affinity = min(self.affinity, 100)/100
        effective_damage = sharpness_adjusted * (1 - affinity + self.crit_multiplier * affinity)
        return int(effective_damage)

    def apply_powercharms(self):
        if self.powercharm:
            self.attack += 6
        if self.powertalon:
            self.attack += 9

    # Damage altering skills; these all change the instance attributes that influence damage.
    def attack_boost(self, level: int):
        if level in (0, 1, 2, 3):
            self.attack = int(self.attack + level*3)
        elif level in (4, 5):
            self.attack = int(self.attack * (1.01 + level/100) + level + 3)
        elif level == 6:
            self.attack = int(self.attack * 1.08 + 9)
        else:
            self.attack = int(self.attack * 1.10 + 10)

    def critical_eye(self, level: int):
        if level in (1, 2, 3, 4, 5, 6):
            self.affinity = self.affinity + level*5
        elif level == 7:
            self.affinity = self.affinity + 40

    def weakness_exploit(self, level: int):
        if level in (0, 1, 2):
            self.affinity = self.affinity + 15*level
        elif level == 3:
            self.affinity = self.affinity + 50

    def resentment(self, level: int):
        if level in (1, 2, 3, 4, 5):
            self.attack = self.attack + 5*level

    def critical_boost(self, level: int):
        if level in range(1, 2, 3):
            self.crit_multiplier = self.crit_multiplier + 0.05*level

    def critical_draw(self, level: int):
        if level in (1, 2, 3):
            self.affinity = self.affinity + 10*2**(level-1)

    # Special methods
    def __str__(self):
        out = f"------{self.weapon.name}------"
        out += f"\n\nWeapon equipped:\n\tAttack: {self.weapon.attack}, Affinity: {self.weapon.affinity}%, " \
              f"Sharpness multiplier: {self.weapon.sharpness_multiplier}"
        out += f"\n\nSkills affecting effective damage:"
        out += f"\n\t"
        for skill in self.active_skills.keys():
            out += f" {skill}{self.active_skills[skill]},"
        out += f"\n\nStats after skills:"
        out += f"\n\tAttack: {self.attack}, Affinity: {self.affinity}%, Sharpness multiplier: {self.sharpness_multiplier}"
        out += f"\n\tCrit multiplier: {self.crit_multiplier}"
        out += f"\n\nEffective Raw: {self.effective_raw}\n"
        return out

def compare_armorsets(weapons: list, skillsets: list, verbose: bool = False):
    '''
    If verbose prints every set detail, otherwise only prints the best.
    '''
    best = ArmorSet(Weapon(0, 0, 'R'), '')
    analyzed = []
    for weapon in weapons:
        for skillset in skillsets:
            current = ArmorSet(weapon, skillset)
            analyzed += [current]
            if current.effective_raw > best.effective_raw:
                best = current
    if verbose:
        analyzed = sorted(analyzed, key=lambda x: x.effective_raw)
        for armorset in analyzed:
            print(f"{armorset.weapon.name} with {armorset.active_skills.keys()} = {armorset.effective_raw}")
    return best

if __name__ == "__main__":
    weapons = [
        Weapon(230, -9, 'b',  name='Goss +6 aff'),
        Weapon(218, -15, 'w', name='tig +8 att'),
        Weapon(210, -9, 'w',  name='tig + 6 aff'),
        Weapon(188, 35, 'w',  name='narga +8 att'),
        Weapon(180, 41, 'w',  name='narga + 6 aff'),
    ]

    skillsets = [
        'AB7 WEX3 CE2 Focus3',
        'AB7 WEX3 RESENTMENT2 FOCUS3'
    ]

    print(compare_armorsets(weapons, skillsets, True))
    # Tigrex with 387 is highest with normal skillset
    #print(ArmorSet(goss_gs, basic_skillset))
    #print(ArmorSet(tigrex_gs, basic_skillset))
    #print(ArmorSet(tig_aff, basic_skillset))
    #print(ArmorSet(narga_gs, basic_skillset))
    #print(ArmorSet(narga_aff, basic_skillset))