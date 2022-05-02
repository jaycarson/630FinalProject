from random import choice
import sqlite3


class ConnectionSQLite(object):
    def __init__(self):
        self.heroes = {}
        self.weapons = {}
        self.armors = {}

        self.count = 0
        self.match_count = 0

        open('commands.sql', 'w').close()

        self.conn = sqlite3.connect('test.db')

        try:
            self.conn.execute('DROP TABLE HEROES')
        except:
            pass
        try:
            self.conn.execute('DROP TABLE WEAPONS')
        except:
            pass
        try:
            self.conn.execute('DROP TABLE ARMORS')
        except:
            pass
        try:
            self.conn.execute('DROP TABLE COMBAT_LOG')
        except:
            pass
        try:
            self.conn.execute('DROP TABLE RESULTS')
        except:
            pass

        heroes = '''CREATE TABLE HEROES (
            ID INT PRIMARY KEY         NOT NULL,
            STR            INT         NOT NULL,
            DEX            INT         NOT NULL,
            CON            INT         NOT NULL,
            INT            INT         NOT NULL,
            WIS            INT         NOT NULL,
            CHA            INT         NOT NULL,
            ATTACK_ROLL    INT         NOT NULL,
            WEAPON_NAME    VARCHAR(20) NOT NULL,
            ARMOR_NAME     VARCHAR(20) NOT NULL,
            SHIELDED       INT         NOT NULL,
            MAX_POTIONS    INT         NOT NULL
            );'''

        weapons = '''CREATE TABLE WEAPONS (
            NAME        VARCHAR(20) PRIMARY KEY NOT NULL,
            ROLL        INT                     NOT NULL,
            COST        INT                     NOT NULL,
            ROLLS       INT                     NOT NULL,
            TWO_HANDED  INT                     NOT NULL
            );'''

        armors = '''CREATE TABLE ARMORS (
            NAME        VARCHAR(20) PRIMARY KEY NOT NULL,
            AC          INT                     NOT NULL,
            COST        INT                     NOT NULL,
            MAX_DEX     INT                     NOT NULL
            );'''
        
        logs = '''CREATE TABLE COMBAT_LOG (
            ID              INT PRIMARY KEY NOT NULL,
            TYPE            VARCHAR(10)     NOT NULL,
            SOURCE_ID       INT             NOT NULL,
            TARGET_ID       INT             NOT NULL,
            START_HEALTH    INT,
            CHANGE          INT,
            END_HEALTH      INT,
            ROLL            INT
        );'''

        results = '''CREATE TABLE RESULTS (
            ID          INT PRIMARY KEY NOT NULL,
            WINNER_ID   INT             NOT NULL,
            LOSER_ID    INT             NOT NULL
        );'''

        self.execute(heroes)
        self.execute(weapons)
        self.execute(armors)
        self.execute(logs)
        self.execute(results)

    def add_hero(self, hero_id, strength, dexterity, constitution, intelligence, wisdom, charisma, attack_roll, weapon_name, armor_name, shielded, max_potions):
        insert = 'INSERT INTO HEROES (ID,STR,DEX,CON,INT,WIS,CHA,ATTACK_ROLL,WEAPON_NAME,ARMOR_NAME,SHIELDED,MAX_POTIONS)'
        values = str(hero_id) + ', '
        values += str(strength) + ', '
        values += str(dexterity) + ', '
        values += str(constitution) + ', '
        values += str(intelligence) + ', '
        values += str(wisdom) + ', '
        values += str(charisma) + ', '
        values += str(attack_roll) + ', '
        values += "'" + str(weapon_name) + "', "
        values += "'" + str(armor_name) + "', "
        if shielded:
            values += '1, '
        else:
            value += '0, '
        values += str(max_potions)

        self.execute(insert + ' VALUES (' + values + ');')

    def add_weapon(self, name, roll, cost, rolls, two_handed):
        insert = 'INSERT INTO WEAPONS (NAME,ROLL,COST,ROLLS,TWO_HANDED)'
        values = "'" + str(name) + "', "
        values += str(roll) + ', '
        values += str(cost) + ', '
        values += str(rolls) + ', '
        if two_handed:
            values += '1'
        else:
            values += '0'

        self.execute(insert + ' VALUES (' + values + ');')

    def add_armor(self, name, ac, cost, max_dex):
        insert = 'INSERT INTO ARMORS (NAME,AC,COST,MAX_DEX)'
        values = "'" + str(name) + "', "
        values += str(ac) + ', '
        values += str(cost) + ', '
        values += str(max_dex)

        self.execute(insert + ' VALUES (' + values + ');')

    def close(self):
        self.conn.close()

    def execute(self, command):
        self.conn.execute(command)
        with open('commands.sql', 'a') as fh:
            fh.write(command.replace(';', ';\n'))

    def get_hero_attr(self, hero_id, attr):
        return self.conn.execute('SELECT ' + str(attr) + ' FROM HEROES WHERE ID = ' + str(hero_id)).fetchone()[0]

    def get_armor_cost(self, name):
        return self.conn.execute("SELECT COST FROM ARMORS WHERE NAME='" + str(name) + "'").fetchone()[0]

    def get_armor_class(self, name):
        return self.conn.execute("SELECT AC FROM ARMORS WHERE NAME='" + str(name) + "'").fetchone()[0]

    def get_random_armor_name(self):
        cursor = self.conn.execute('SELECT NAME FROM ARMORS')
        values = []
        for row in cursor:
            values.append(row[0])
        return choice(list(values))

    def get_random_weapon_name(self):
        cursor = self.conn.execute('SELECT NAME FROM WEAPONS')
        values = []
        for row in cursor:
            values.append(row[0])
        return choice(list(values))

    def get_weapon_cost(self, name):
        return self.conn.execute("SELECT COST FROM WEAPONS WHERE NAME='" + name + "'").fetchone()[0]

    def get_weapon_roll(self, name):
        return self.conn.execute("SELECT ROLL FROM WEAPONS WHERE NAME='" + name + "'").fetchone()[0]

    def get_weapon_rolls(self, name):
        return self.conn.execute("SELECT ROLLS FROM WEAPONS WHERE NAME='" + name + "'").fetchone()[0]

    def is_weapon_two_handed(self, name):
        if self.conn.execute("SELECT TWO_HANDED FROM WEAPONS WHERE NAME='" + name + "'").fetchone()[0] == 1:
            return True
        else:
            return False

    def log_hit(self, source, target, start_health, change, end_health, roll):
        insert = 'INSERT INTO COMBAT_LOG (ID,TYPE,SOURCE_ID,TARGET_ID,START_HEALTH,CHANGE,END_HEALTH,ROLL)'
        values = str(self.count) + ', '
        values += "'HIT', "
        values += str(source) + ', '
        values += str(target) + ', '
        values += str(start_health) + ', '
        values += str(change) + ', '
        values += str(end_health) + ', '
        values += str(roll)

        self.execute(insert + ' VALUES (' + values + ');')
        self.count += 1

    def log_miss(self, source, target, roll):
        insert = 'INSERT INTO COMBAT_LOG (ID,TYPE,SOURCE_ID,TARGET_ID,ROLL)'
        values = str(self.count) + ', '
        values += "'MISS', "
        values += str(source) + ', '
        values += str(target) + ', '
        values += str(roll)

        self.execute(insert + ' VALUES (' + values + ');')
        self.count += 1

    def log_heal(self, source, start_health, change, end_health):
        insert = 'INSERT INTO COMBAT_LOG (ID,TYPE,SOURCE_ID,TARGET_ID,START_HEALTH,CHANGE,END_HEALTH)'
        values = str(self.count) + ', '
        values += "'HEAL', "
        values += str(source) + ', '
        values += str(source) + ', '
        values += str(start_health) + ', '
        values += str(change) + ', '
        values += str(end_health)

        self.execute(insert + ' VALUES (' + values + ');')
        self.count += 1

    def log_results(self, winner_id, loser_id):
        insert = 'INSERT INTO RESULTS (ID,WINNER_ID,LOSER_ID)'
        values = str(self.match_count) + ', '
        values += str(winner_id) + ', '
        values += str(loser_id)

        self.execute(insert + ' VALUES (' + values + ');')
        self.match_count += 1
