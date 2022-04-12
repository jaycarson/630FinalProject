import argparse
from random import randrange, choice


class Simulation(object):
    def __init__(self, debug):
        cursor = None
        self.weapons = Weapons(cursor)
        self.armors = Armors(cursor)
        self.heroes = []
        hero_count = 50

        for x in range(hero_count):
            hero = Hero(x)
            self.weapons.equip(hero)
            self.armors.equip(hero)
            hero.save()
            self.heroes.append(hero)

    def __call__(self):
        fights = 50

        for x in range(fights):
            hero_1 = choice(self.heroes)
            hero_2 = choice(self.heroes)

            while(hero_1 == hero_2):
                hero_2 = choice(self.heroes)

            self.fight(hero_1, hero_2)

    def fight(self, hero_1, hero_2):
        hero_1.health = hero_1.max_health
        hero_2.health = hero_2.max_health

        while(hero_1.health > 0 and hero_2.health > 0):
            hero_1.attack(hero_2)
            if(hero_2.health > 0):
                hero_2.attack(hero_1)
        if(hero_1.health > 0):
            self.result(hero_1, hero_2)
        else:
            self.result(hero_2, hero_1)

    def result(self, winner, loser):
        print('Winner: ' + str(winner.id))
        print('Loser: ' + str(loser.id))


class Hero(object):
    def __init__(self, hero_id):
        self.id = hero_id
        self.attack_roll = 5
        self.weapon_name = ''
        self.weapon_roll = 0
        self.weapon_rolls = 1
        self.armor_name = 0
        self.armor_class = 10
        self.gold = 1000

        self.strength = randrange(1, 7) + randrange(1, 7) + randrange(1, 7)
        self.dexterity = randrange(1, 7) + randrange(1, 7) + randrange(1, 7)
        self.constitution = randrange(1, 7) + randrange(1, 7) + randrange(1, 7)
        self.intelligence = randrange(1, 7) + randrange(1, 7) + randrange(1, 7)
        self.wisdom = randrange(1, 7) + randrange(1, 7) + randrange(1, 7)
        self.charisma = randrange(1, 7) + randrange(1, 7) + randrange(1, 7)

        self.max_health = 50 + ((self.constitution - 10) // 2) * 5
        self.health = self.max_health

    def attack(self, target):
        if((randrange(1, 21) + self.attack_roll) >= target.armor_class):
            for x in range(self.weapon_rolls):
                damage = randrange(1, self.weapon_roll + 1)
                target.health -= damage
                print("    " + str(self.id) + ": Damage Done: " + str(damage) + " / " + str(target.health))

    def save(self):
        return


class Weapons(object):
    def __init__(self, cursor):
        self.weapons = {}
        self.cursor = cursor
        self.weapon_names = ['Club', 'Dagger', 'Axe', 'Mace', 'Battle Axe', 'Glaive', 'Morning Star', 'Shortsword', 'Greatsword']

        self.add('Club', 4, 0)
        self.add('Dagger', 4, 2)
        self.add('Axe', 6, 5)
        self.add('Mace', 6, 5)
        self.add('Battle Axe', 8, 10, two_handed=True)
        self.add('Glaive', 10, 20, True)
        self.add('Morning Star', 8, 15)
        self.add('Shortsword', 6, 10)
        self.add('Greatsword', 6, 50, rolls=2, two_handed=50)

    def add(self, name, roll, cost, rolls=1, two_handed=False):
        self.weapons[name] = {'roll': roll, 'cost': cost, 'rolls': rolls, 'two-handed': two_handed}

    def equip(self, hero):
        weapon_name = choice(self.weapon_names)
        weapon = self.weapons[weapon_name]
        hero.weapon_name = weapon_name
        hero.weapon_roll = weapon['roll']
        hero.gold -= weapon['cost']
        hero.two_handed = weapon['two-handed']


class Armors(object):
    def __init__(self, cursor):
        self.armors = {}
        self.cursor = cursor
        self.armor_names = ['Padded', 'Leather', 'Studded Leather', 'Hide', 'Chain Shirt', 'Scale Mail', 'Ring Mail', 'Chain Mail']

        self.add('Padded', 1, 5)
        self.add('Leather', 1, 10)
        self.add('Studded Leather', 2, 45)
        self.add('Hide', 2, 10, 2)
        self.add('Chain Shirt', 3, 50, 2)
        self.add('Scale Mail', 4, 50, 2)
        self.add('Ring Mail', 4, 30)
        self.add('Chain Mail', 6, 75)

        self.shield_ac = 2
        self.shield_cost = 10

    def add(self, name, ac, cost, max_dex=4):
        self.armors[name] = {'ac': ac, 'cost': cost, 'dex': max_dex}

    def equip(self, hero):
        armor_name = choice(self.armor_names)
        armor = self.armors[armor_name]
        hero.armor_name = armor_name
        hero.armor_class += armor['ac']
        hero.gold -= armor['cost']
        if not hero.two_handed:
            hero.armor_class += self.shield_ac
            hero.gold -= self.shield_cost


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
