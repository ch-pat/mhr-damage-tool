# MON-HUN RISE Damage tool

`damage.py` contains miscellaneous scripts and experimentation, should not be used for comfortable interaction.

`armorset.py` contains most of the logic.

## How to use
Currently no interface is given. a `if __name__ == "__main__":` section is included in `armorset.py` in which you can:
- define a 'Weapon' by specifying its raw, affinity and sharpness color (after rampage skills and after handicraft)
- define an 'ArmorSet' by specifying a `Weapon` object and a string of space-separated skill, expressed as their shorthands with their level as suffix.
  - example: 'WEX3 AB7' represents the skills 'Weakness Exploit' level 3 and 'Attack Boost' level 7
- print the defined `ArmorSet` instance to show some stats, and most importantly, the 'Effective Raw' of the set, which takes into account all damage altering skills (conditionals are considered active) to obtain a value that summarizes in a single number the 'strength' of the set, the higher the better.

## TODO
- An user friendly interface
- Element
- Add all skills
- More interesting stats (variance, non-conditional vs conditional effective raw, whatever comes to mind)