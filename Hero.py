from random import randrange, choice


class Hero(object):
    def __init__(self, connection, hero_id):
        self.id = hero_id
        
        self.weapon_name = connection.get_hero_attr(hero_id, 'weapon_name')
        self.armor_name = connection.get_hero_attr(hero_id, 'armor_name')
        self.potions = connection.get_hero_attr(hero_id, 'max_potions')

        self.strength = connection.get_hero_attr(hero_id, 'str')
        self.dexterity = connection.get_hero_attr(hero_id, 'dex')
        self.constitution = connection.get_hero_attr(hero_id, 'con')

        self.health = 50 + ((self.constitution - 10) // 2) * 5
        self.max_health = self.health
        
        self.attack_roll = connection.get_hero_attr(hero_id, 'attack_roll') + ((self.strength - 10) // 2)
        self.damage_bonus = ((self.strength - 10) // 2)

        self.armor_class = connection.get_armor_class(self.armor_name) + ((self.dexterity - 10 ) // 2)
        
        self.weapon_roll = connection.get_weapon_roll(self.weapon_name)
        self.weapon_rolls = connection.get_weapon_rolls(self.weapon_name)

        self.connection = connection

    def attack(self, target):
        roll = randrange(1, 21) + self.attack_roll
        if(roll >= target.armor_class):
            for x in range(0, self.weapon_rolls):
                damage = randrange(1, self.weapon_roll + 1)
                target.health -= damage
                self.connection.log_hit(
                    self.id,
                    target.id,
                    target.health + damage,
                    -damage, 
                    target.health,
                    roll,
                )
        else:
            self.connection.log_miss(self.id, target.id, roll)
        if((self.health / self.max_health) < 0.5):
            self.heal()

    def heal(self):
        if(self.potions > 0):
            self.potions -= 1
            amount = randrange(1, 9)
            self.health += amount
            self.connection.log_heal(self.id, self.health - amount, amount, self.health)
