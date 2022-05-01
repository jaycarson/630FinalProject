from random import choice


class ConnectionDataStructures(object):
    def __init__(self):
        self.heroes = {}
        self.weapons = {}
        self.armors = {}

    def add_hero(self, hero_id, strength, dexterity, constitution, intelligence, wisdom, charisma, attack_roll, weapon_name, armor_name, shielded, max_potions):
        self.heroes[hero_id] = {
            'str': strength,
            'dex': dexterity,
            'con': constitution,
            'int': intelligence,
            'wis': wisdom,
            'cha': charisma,
            'attack_roll': attack_roll,
            'weapon_name': weapon_name,
            'armor_name': armor_name,
            'shielded': shielded,
            'max_potions': max_potions,
        }

    def add_weapon(self, name, roll, cost, rolls, two_handed):
        self.weapons[name] = {
            'roll': roll,
            'cost': cost,
            'rolls': rolls,
            'two_handed': two_handed,
        }

    def add_armor(self, name, ac, cost, max_dex):
        self.armors[name] = {
            'ac': ac,
            'cost': cost,
            'max_dex': max_dex,
        }
    
    def close(self):
        return

    def get_hero_attr(self, hero_id, attr):
        return self.heroes[hero_id][attr]

    def get_hero_attrs(self, hero_id):
        return self.heroes[hero_id]

    def get_armor_cost(self, name):
        return self.armors[name]['cost']

    def get_armor_class(self, name):
        return self.armors[name]['ac']

    def get_random_armor_name(self):
        return choice(list(self.armors.keys()))

    def get_random_weapon_name(self):
        return choice(list(self.weapons.keys()))

    def get_weapon_cost(self, name):
        return self.weapons[name]['cost']

    def get_weapon_roll(self, name):
        return self.weapons[name]['roll']

    def get_weapon_rolls(self, name):
        return self.weapons[name]['rolls']

    def is_weapon_two_handed(self, name):
        return self.weapons[name]['two_handed']
