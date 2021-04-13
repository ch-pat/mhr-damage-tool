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
        self.sharpness_multiplier = Weapon.sharpness_values[sharpness.upper()]
        self.name = name