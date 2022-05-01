import argparse
from random import randrange, choice
from Hero import Hero
from ConnectionDataStructures import ConnectionDataStructures
from ConnectionSQLite import ConnectionSQLite


class Simulation(object):
    def __init__(self, debug):
        self.connection = ConnectionSQLite()
        # self.connection = ConnectionDataStructures()
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

        self.connection.close()

    def add_armors(self):
        self.connection.add_armor('Padded', 1, 5, 5)
        self.connection.add_armor('Leather', 1, 10, 5)
        self.connection.add_armor('Studded Leather', 2, 45, 5)
        self.connection.add_armor('Hide', 2, 10, 2)
        self.connection.add_armor('Chain Shirt', 3, 50, 2)
        self.connection.add_armor('Scale Mail', 4, 50, 2)
        self.connection.add_armor('Ring Mail', 4, 30, 5)
        self.connection.add_armor('Chain Mail', 6, 75, 5)

    def add_hero(self, hero_id):
        gold = 150
        shield_cost = 10
        shield_armor = 2
        pot_cost = 25

        weapon_name = self.connection.get_random_weapon_name()
        gold -= self.connection.get_weapon_cost(weapon_name)
        
        armor_name = self.connection.get_random_armor_name()
        gold -= self.connection.get_armor_cost(armor_name)
        ac = 10 + self.connection.get_armor_class(armor_name)
        
        two_handed = self.connection.is_weapon_two_handed(weapon_name)
        
        if(two_handed):
            shielded = False
        else:
            shielded = True
            gold -= shield_cost
            ac += shield_armor

        self.connection.add_hero(
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
            max_potions = int(gold / pot_cost),
        )
        
    def add_weapons(self):
        self.connection.add_weapon('Club', 4, 0, 1, False)
        self.connection.add_weapon('Dagger', 4, 2, 1, False)
        self.connection.add_weapon('Axe', 6, 5, 1, False)
        self.connection.add_weapon('Mace', 6, 5, 1, False)
        self.connection.add_weapon('Battle Axe', 8, 1, 1, True)
        self.connection.add_weapon('Glaive', 10, 20, 1, True)
        self.connection.add_weapon('Morning Star', 8, 15, 1, False)
        self.connection.add_weapon('Shortsword', 6, 10, 1, False)
        self.connection.add_weapon('Greatsword', 6, 50, 2, True)

    def fight(self, hero_1_id, hero_2_id):
        hero_1 = Hero(self.connection, hero_1_id)
        hero_2 = Hero(self.connection, hero_2_id)

        while(hero_1.health > 0 and hero_2.health > 0):
            hero_1.attack(hero_2)
            if(hero_2.health > 0):
                hero_2.attack(hero_1)
        if(hero_1.health > 0):
            self.result(hero_1.id, hero_2.id)
        else:
            self.result(hero_2.id, hero_1.id)

    def result(self, winner, loser):
        self.connection.log_results(winner, loser)


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
