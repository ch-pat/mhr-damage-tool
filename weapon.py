class Weapon():
    sharpness_values = {
    'R': 0.50,
    'O': 0.75,
    'Y': 1.00,
    'G': 1.05,
    'B': 1.20,
    'W': 1.32,
    'P': 1.44
    }
    def __init__(self, attack: int, affinity: int, sharpness: str, name: str = 'NONAME'):
        self.attack: int = attack
        self.affinity: int = affinity
        self.crit_multiplier: float = 1.25
        self.sharpness_multiplier = Weapon.sharpness_values[sharpness.upper()]
        self.name = name
        self.effective_raw = self.calculate_effective_raw()

    def calculate_effective_raw(self) -> int:
        sharpness_adjusted = self.attack*self.sharpness_multiplier
        affinity = min(self.affinity, 100)/100
        effective_damage = sharpness_adjusted * (1 - affinity + self.crit_multiplier * affinity)
        return int(effective_damage)