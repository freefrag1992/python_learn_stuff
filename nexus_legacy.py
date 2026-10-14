from dataclasses import dataclass


## ship stats

## UPGRADE MODS (level 0 - 10)
laser_weapon_tech = [1,1.03,1.6,1.09,1.12,1.15,1.18,1.21,1.24,1.27,1.3]
kinetic_weapon_tech = [1,1.03,1.06,1.09,1.12,1.15,1.18,1.21,1.24,1.27,1.3]
fighter_doctrine_tech = [1,1.02,1.04,1.06,1.08,1.1,1.12,1.14,1.16,1.18,1.2]
assault_tactics_tech = [1,1.01,1.02,1.03,1.04,1.05,1.06,1.07,1.08,1.09,1.1]
missile_systems_tech = [1,1.02,1.04,1.06,1.08,1.1,1.12,1.14,1.16,1.18,1.2]

basic_armor_plating_ships_tech = [1,1.02,1.04,1.06,1.08,1.1,1.12,1.14,1.16,1.18,1.2]
shield_theory_tech = [1,0.98,0.96,0.94,0.92,0.9,0.88,0.86,0.84,0.82,0.8]

@dataclass
class Ship:
    hp: int
    shield: int
    atk: int
    speed: int
    cargo: int
    fuel: float
    weapon: str
    armor: str
    crew: int
    ore: int
    silicate: int
    hydrogen: int
    alloys: int
    cryo_ice: int
    plasma_core: int

probe = Ship(30,8,0,25,0,0.5,"none","light",0,50,250,0,0,0,0)
spy_probe = Ship(30,8,0,28,0,0.5,"none","light",0,100,500,30,100,0,0)
stealth_ship = Ship(150,60,5,10,50,2,"laser","light",0,800,1000,400,200,100,0)
scout = Ship(100,25,15,15,20,1,"kinetic","light",1,200,100,0,20,0,0)
fighter = Ship(250,60,30,12,35,1.5,"laser","light",2,500,250,50,100,0,0)
interceptor = Ship(200,50,35,18,50,1.5,"kinetic","light",3,900,500,200,200,0,0)
torpedo_frigate = Ship(180,40,55,14,30,2,"missile","light",5,1200,700,400,300,0,150)

@dataclass
class Fleet:
    probe: int = 0
    spy_probe: int = 0
    stealth_ship: int = 0
    scout: int = 0
    fighter: int = 0
    interceptor: int = 0
    torpedo_frigate: int = 0

    def __add__(self, other):
        return Fleet(
            probe=self.probe + other.probe,
            spy_probe=self.spy_probe + other.spy_probe,
            stealth_ship=self.stealth_ship + other.stealth_ship,
            scout=self.scout + other.scout,
            fighter=self.fighter + other.fighter,
            interceptor=self.interceptor + other.interceptor,
            torpedo_frigate=self.torpedo_frigate + other.torpedo_frigate,
        )

## TEST VALUES

attacker_one = Fleet(probe=6)
# attacker_two = Fleet(fighter=1)
# all_attackers = attacker_one + attacker_two

defender_one = Fleet(fighter=1)


##### Attacker TECH UPGRADES
# offensive
attacker_laser_weapons_level = laser_weapon_tech[0]
attacker_assault_tactics_level = assault_tactics_tech[0]
attacker_fighter_doctrine_level = fighter_doctrine_tech[0]

attacker_kinetic_weapons_level = kinetic_weapon_tech[0]
attacker_missile_systems_level = missile_systems_tech[0]

# defensive
attacker_basic_armor_plating_level = basic_armor_plating_ships_tech[0]
attacker_shield_theory_level = shield_theory_tech[0]

##### Defender TECH UPGRADES
defender_laser_weapons_level = laser_weapon_tech[0]
defender_assault_tactics_level = assault_tactics_tech[0]
defender_fighter_doctrine_level = fighter_doctrine_tech[0]

defender_kinetic_weapons_level = kinetic_weapon_tech[0]
defender_missile_systems_level = missile_systems_tech[0]

# defensive
defender_basic_armor_plating_level = basic_armor_plating_ships_tech[0]
defender_shield_theory_level = shield_theory_tech[0]

### defender attack calc is reverse in brackets (enemy_ship, my ship)

# Damage Calc
def Attacker_Attack_Calculation(attacker_ship, defender_ship):
    armor_damage_mod = 1
    if defender_ship.armor == "light" and attacker_ship.weapon == "kinetic":
        armor_damage_mod = 1.25
    elif defender_ship.armor == "medium" and attacker_ship.weapon == "missile":
        armor_damage_mod = 1.05
    elif defender_ship.armor == "heavy":
        if attacker_ship.weapon == "kinetic":
            armor_damage_mod = 0.85
        elif attacker_ship.weapon == "plasma":
            armor_damage_mod = 0.9
        elif attacker_ship.weapon == "ion":
            armor_damage_mod = 0.85
        else:
            armor_damage_mod = 1
    elif defender_ship.armor == "shielded":
        if attacker_ship.weapon == "plasma":
            armor_damage_mod = 1.25
        elif attacker_ship.weapon == "ion":
            armor_damage_mod = 1.3
        else:
            armor_damage_mod = 1
    else:
        armor_damage_mod = 1

### apply all mods now

    if attacker_ship.weapon == "laser":
        atk = attacker_ship.atk * armor_damage_mod * attacker_laser_weapons_level * attacker_fighter_doctrine_level * attacker_assault_tactics_level
        return atk
    elif attacker_ship.weapon == "kinetic":
        atk = attacker_ship.atk * armor_damage_mod * attacker_kinetic_weapons_level * attacker_assault_tactics_level
        return atk
    elif attacker_ship.weapon == "missile":
        atk = attacker_ship.atk * armor_damage_mod * attacker_missile_systems_level * attacker_assault_tactics_level
        return atk
    elif attacker_ship.weapon == "plasma":
        atk = attacker_ship.atk * armor_damage_mod
        return atk
    elif attacker_ship.weapon == "ion":
        atk = attacker_ship.atk * armor_damage_mod
        return atk
    elif attacker_ship.weapon == "none":
        atk = attacker_ship.atk * armor_damage_mod
        return atk
    else:
        raise ValueError(f"Unbekannter Waffentyp: {attacker_ship.weapon}")
def Defender_Attack_Calculation(defender_ship, attacker_ship):
    armor_damage_mod = 1
    if attacker_ship.armor == "light" and defender_ship.weapon == "kinetic":
        armor_damage_mod = 1.25
    elif attacker_ship.armor == "medium" and defender_ship.weapon == "missile":
        armor_damage_mod = 1.05
    elif attacker_ship.armor == "heavy":
        if defender_ship.weapon == "kinetic":
            armor_damage_mod = 0.85
        elif defender_ship.weapon == "plasma":
            armor_damage_mod = 0.9
        elif defender_ship.weapon == "ion":
            armor_damage_mod = 0.85
        else:
            armor_damage_mod = 1
    elif attacker_ship.armor == "shielded":
        if defender_ship.weapon == "plasma":
            armor_damage_mod = 1.25
        elif defender_ship.weapon == "ion":
            armor_damage_mod = 1.3
        else:
            armor_damage_mod = 1
    else:
        armor_damage_mod = 1

### apply all mods now

    if defender_ship.weapon == "laser":
        atk = defender_ship.atk * armor_damage_mod * defender_laser_weapons_level * defender_fighter_doctrine_level * defender_assault_tactics_level
        return atk
    elif defender_ship.weapon == "kinetic":
        atk = defender_ship.atk * armor_damage_mod * defender_kinetic_weapons_level * defender_assault_tactics_level
        return atk
    elif defender_ship.weapon == "missile":
        atk = defender_ship.atk * armor_damage_mod * defender_missile_systems_level * defender_assault_tactics_level
        return atk
    elif defender_ship.weapon == "plasma":
        atk = defender_ship.atk * armor_damage_mod
        return atk
    elif defender_ship.weapon == "ion":
        atk = defender_ship.atk * armor_damage_mod
        return atk
    elif defender_ship.weapon == "none":
        atk = defender_ship.atk * armor_damage_mod
        return atk
    else:
        raise ValueError(f"Unbekannter Waffentyp: {defender_ship.weapon}")

# Defensive Attacker
def Attacker_HP_Calculation(attacker_ship):
    attacker_hp = attacker_ship.hp * attacker_basic_armor_plating_level
    return attacker_hp
def Attacker_Shield_Calculation(attacker_ship):
    attacker_shield = attacker_ship.shield / attacker_shield_theory_level
    return attacker_shield

# Defensive Defender
def Defender_HP_Calculation(defender_ship):
    defender_hp = defender_ship.hp
    return defender_hp
def Defender_Shield_Calculation(defender_ship):
    defender_shield = defender_ship.shield / defender_shield_theory_level
    return defender_shield







## Fleet Composition Attackers and Defenders

print("scout dmg ohne mods:",scout.atk)
print("Attack_Damage_Calculation = ", Attacker_Attack_Calculation(scout, probe))

print("\n + + + Attacker + + + ")
print (f"HP:{Attacker_HP_Calculation(scout)}\nShield: {Attacker_Shield_Calculation(scout)}")
print("Attack_Damage_Calculation = ", Attacker_Attack_Calculation(scout, probe))
print("\n + + + Defender + + + ")
print (f"HP:{Defender_HP_Calculation(probe)}\nShield: {Defender_Shield_Calculation(probe)}")
print("Attack_Damage_Calculation = ", Defender_Attack_Calculation(probe,scout))
# print(all_attackers)



