from weapon import Weapon

class ArmorSet():
    
    def __init__(self, weapon: Weapon, active_skills: str):
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
        self.active_skills:         dict = self.parse_skills(active_skills)
        self.apply_skills()         # Applies skills to change the above stats
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
        out = f"Weapon equipped:\n\tAttack: {self.weapon.attack}, Affinity: {self.weapon.affinity}%, " \
              f"Sharpness multiplier: {self.weapon.sharpness_multiplier}"
        out += f"\nSkills affecting effective damage:"
        out += f"\n\t"
        for skill in self.active_skills.keys():
            out += f" {skill}{self.active_skills[skill]},"
        out += f"\nStats after skills:"
        out += f"\n\tAttack: {self.attack}, Affinity: {self.affinity}%, Sharpness multiplier: {self.sharpness_multiplier}"
        out += f"\n\tCrit multiplier: {self.crit_multiplier}"
        out += f"\nEffective Raw: {self.effective_raw}"
        return out

if __name__ == "__main__":
    goss_gs = Weapon(230, -9, 'b')

    armor = ArmorSet(goss_gs, 'AB7 WEX3 CE2 Focus3')
    print(armor)