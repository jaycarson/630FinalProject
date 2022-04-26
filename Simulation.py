import argparse
from random import randrange, choice


class Simulation(object):
    def __init__(self, debug):
        self.cursor = SQLiteCursor()
        self.hero_count = 50
        self.add_armors()
        self.add_weapons()

        for x in range(self.hero_count):
            self.add_hero(x)

    def __call__(self):
        fights = 50

        for x in range(fights):
            hero_id_1 = randrange(0, self.hero_count)
            hero_id_2 = randrange(0, self.hero_count)

            while(hero_id_1 == hero_id_2):
                hero_id_2 = randrange(0, self.hero_count)

            self.fight(hero_id_1, hero_id_2)

    def add_armors(self):
        self.cursor.add_armor('Padded', 1, 5, 5)
        self.cursor.add_armor('Leather', 1, 10, 5)
        self.cursor.add_armor('Studded Leather', 2, 45, 5)
        self.cursor.add_armor('Hide', 2, 10, 2)
        self.cursor.add_armor('Chain Shirt', 3, 50, 2)
        self.cursor.add_armor('Scale Mail', 4, 50, 2)
        self.cursor.add_armor('Ring Mail', 4, 30, 5)
        self.cursor.add_armor('Chain Mail', 6, 75, 5)

    def add_hero(self, hero_id):
        gold = 1000
        shield_cost = 10
        shield_armor = 2

        weapon_name = self.cursor.get_random_weapon_name()
        gold -= self.cursor.get_weapon_cost(weapon_name)
        
        armor_name = self.cursor.get_random_armor_name()
        gold -= self.cursor.get_armor_cost(armor_name)
        ac = 10 + self.cursor.get_armor_class(armor_name)
        
        two_handed = self.cursor.is_weapon_two_handed(weapon_name)
        
        if(two_handed):
            shielded = False
        else:
            shielded = True
            gold -= shield_cost
            ac += shield_armor

        self.cursor.add_hero(
            hero_id = hero_id,
            strength = randrange(1, 7) + randrange(1, 7) + 6,
            dexterity = randrange(1, 7) + randrange(1, 7) + 6,
            constitution = randrange(1, 7) + randrange(1, 7) + 6,
            intelligence = randrange(1, 7) + randrange(1, 7) + 6,
            wisdom = randrange(1, 7) + randrange(1, 7) + 6,
            charisma = randrange(1, 7) + randrange(1, 7) + 6,
            attack_roll = 1,
            weapon_name = weapon_name,
            armor_name = armor_name,
            shielded = str(shielded),
            max_potions = int(gold / 50),
        )
        
    def add_weapons(self):
        self.cursor.add_weapon('Club', 4, 0, 1, False)
        self.cursor.add_weapon('Dagger', 4, 2, 1, False)
        self.cursor.add_weapon('Axe', 6, 5, 1, False)
        self.cursor.add_weapon('Mace', 6, 5, 1, False)
        self.cursor.add_weapon('Battle Axe', 8, 1, 1, True)
        self.cursor.add_weapon('Glaive', 10, 20, 1, True)
        self.cursor.add_weapon('Morning Star', 8, 15, 1, False)
        self.cursor.add_weapon('Shortsword', 6, 10, 1, False)
        self.cursor.add_weapon('Greatsword', 6, 50, 2, True)

    def fight(self, hero_1_id, hero_2_id):
        hero_1 = Hero(self.cursor, hero_1_id)
        hero_2 = Hero(self.cursor, hero_2_id)

        while(hero_1.health > 0 and hero_2.health > 0):
            hero_1.attack(hero_2)
            if(hero_2.health > 0):
                hero_2.attack(hero_1)
        if(hero_1.health > 0):
            self.result(hero_1, hero_2)
        else:
            self.result(hero_2, hero_1)

    def result(self, winner, loser):
        print('Winner: ' + str(winner.id) + '    Loser: ' + str(loser.id))


class Hero(object):
    def __init__(self, cursor, hero_id):
        self.id = hero_id
        
        self.weapon_name = cursor.get_hero_attr(hero_id, 'weapon_name')
        self.armor_name = cursor.get_hero_attr(hero_id, 'armor_name')
        self.potions = cursor.get_hero_attr(hero_id, 'max_potions')

        self.strength = cursor.get_hero_attr(hero_id, 'str')
        self.dexterity = cursor.get_hero_attr(hero_id, 'dex')
        self.constitution = cursor.get_hero_attr(hero_id, 'con')

        self.health = 50 + ((self.constitution - 10) // 2) * 5
        self.max_health = self.health
        
        self.attack_roll = cursor.get_hero_attr(hero_id, 'attack_roll') + ((self.strength - 10) // 2)
        self.damage_bonus = ((self.strength - 10) // 2)

        self.armor_class = cursor.get_armor_class(self.armor_name) + ((self.dexterity - 10 ) // 2)
        
        self.weapon_roll = cursor.get_weapon_roll(self.weapon_name)
        self.weapon_rolls = cursor.get_weapon_rolls(self.weapon_name)

    def attack(self, target):
        if((randrange(1, 21) + self.attack_roll) >= target.armor_class):
            for x in range(0, self.weapon_rolls):
                damage = randrange(1, self.weapon_roll + 1)
                target.health -= damage
                print("    " + str(self.id) + ": Damage Done: " + str(damage) + " / " + str(target.health))
        else:
            print("    " + str(self.id) + ": Miss")
        if((self.health / self.max_health) < 0.5):
            self.heal()

    def heal(self):
        if(self.potions > 0):
            self.potions -= 1
            amount = randrange(1, 9)
            self.health += amount
            print('        ' + str(self.id) + ': healing: ' + str(amount))


class SQLiteCursor(object):
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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="""The Game""",
        )
    parser.add_argument(
            "-d", "--debug",
            action="store_true",
            help="Displays additional debugging information",
        )
    args = parser.parse_args()
    sim = Simulation(args.debug)
    sim()
