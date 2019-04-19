# -*- coding: utf-8 -*-
''' 
Axe Slayer is a RPG where a hero needs to battle against evil forces using his axe
'''
import sys 
import os
import random
import pickle
import time

weapons = {"Great Axe":40}
global turn
turn = 0

class Player:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 100
        self.health = self.maxhealth
        self.base_attack = 10
        self.magic = 20
        self.gold = 30
        self.pots = 0
        self.weap = ["Rusty Axe"]
        self.curweap = ["Rusty Axe"]

    @property 
    def attack(self):
        attack = self.base_attack
        if self.curweap == "Rusty Axe":
            attack += 5

        if self.curweap == "Great Axe":
            attack += 15

        return attack


class Goblin:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 50
        self.health = self.maxhealth
        self.attack = 5
        self.goldgain = 10
GoblinIG = Goblin("Goblin")

class Zombie:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 70
        self.health = self.maxhealth
        self.attack = 7
        self.goldgain = 15
ZombieIG = Zombie("Zombie")

class Psycho:
    def __init__(self, name):
        self.name = name
        self.maxhealth = 80
        self.health = self.maxhealth
        self.attack = 9
        self.goldgain = 25
PsychoIG = Psycho("Psycho")

def main():
    print "Welcome to Axe Slayer!\n"
    print "1.) Start"
    print "2.) Load"
    print "3.) Exit"
    option = raw_input("-> ")
    if option == "1":
        intro()
    elif option == "2":
        if os.path.exists("savefile") == True:
            with open('savefile', 'rb') as f:
                global PlayerIG
                PlayerIG = pickle.load(f)
            print "Loaded Save State..."
            option = raw_input(' ')
            start1()
        else:
            print "You have no save file for this game."
            option = raw_input(' ')
            main()

    elif option == "3":
        sys.exit()
    else:
        main()

def intro():
    print "Hello, what is your name?"
    option = raw_input("--> ")
    global PlayerIG
    PlayerIG = Player(option)
    print "\nIt's a quiet evening in the deep forest of Finland. You live with your crazy wife Jen and daughter Marie. \
    You have been chopping fire wood whole day and you're ready to hit the sack. You decide to pleasure your wife\
    before bed. Do you fuck her hard or softly? \n"
    time.sleep(3)
    style = raw_input("hard or softly: \n")
    if style == "hard":
        print "You fuck her hard but crazy bitch is not impressed and falls asleep. You go to sleep aswell\n"
    elif style == "softly":
        print "You fuck her softly but crazy bitch complains that you're too soft and punches you in the face. You decide to go to sleep\n"
    else:
        style = raw_input("hard or softly: ")
    print "You woke up by loud noise and see the village priest screaming: Wake up %s.\nYour child has been kidnapped by monsters. They headed to the dark mountains." % PlayerIG.name
    print "You pack up your trusted Axe and head up to the mountains to slay those bloody creatures and save you daughter.\n"
    time.sleep(3)
    start1()

def start1():
    if turn <= 2:
        print "Turn", turn + 1
        print "Name: %s" % PlayerIG.name
        print "Attack: %i" % PlayerIG.attack
        print "Gold: %d" % PlayerIG.gold
        print "Current Weapons: %s" % PlayerIG.curweap
        print "Potions: %d" % PlayerIG.pots
        print "Magic points: %d" % PlayerIG.magic
        print "Health: %i/%i\n" % (PlayerIG.health, PlayerIG.maxhealth)
        print "1.) Fight"
        print "2.) Store"
        print "3.) Save"
        print "4.) Exit"
        print "5.) Inventory"
        option = raw_input("--> ")
        if option == "1":
            prefight()
        elif option == "2":
            store()
        elif option == "3":
            with open('savefile', 'wb') as f:
                pickle.dump(PlayerIG, f)
                print "\nGame has been saved!\n"
            option = raw_input(' ')
            start1()
        elif option == "4":
            sys.exit()
        elif option == "5":
            inventory()
        else:
            start1()
    else:
        ending()

def inventory():
    print "what do you want to do?"
    print "1.) Equip Weapon"
    print "2.) go back"
    option = raw_input(">>> ")
    if option == "1":
        equip()
    elif option == '2':
        start1()

def equip():
    print "What do you want to equip?"
    for weapon in PlayerIG.weap:
        print weapon
    print "2:) Go back"
    option = raw_input(">>> ")
    if option == PlayerIG.curweap:
        print "You already have that weapon equipped"
        option = raw_input(" ")
        equip()
    elif option == "2":
        inventory()
    elif option in PlayerIG.weap:
        PlayerIG.curweap = option
        print "You have equipped %s." % option
        option = raw_input(" ")
        equip()
    else:
        print "You don't have %s in your inventory" % option


def prefight():
    global enemy
    enemynum = random.randint(1, 3)
    if enemynum == 1:
        enemy = GoblinIG
    elif enemynum == 2:
        enemy = ZombieIG
    else:
        enemy = PsychoIG
    fight()

def fight():
    print "%s     vs      %s" % (PlayerIG.name, enemy.name)
    print "%s's Health: %d/%d    %s's Health: %i/%i" % (PlayerIG.name, PlayerIG.health, PlayerIG.maxhealth, enemy.name, enemy.health, enemy.maxhealth)
    print "Potions %i\n" % PlayerIG.pots
    print "Magic points %i\n" % PlayerIG.magic
    print "1.) Attack"
    print "2.) Drink Potion"
    print "3.) Use Magic"
    print "4.) Run"
    option = raw_input(' ')
    if option == "1":
        attack()
    elif option == "2":
        drinkpot()
    elif option == "3":
        magic_attack()
    elif option == "4":
        run()
    else:
        fight()

def attack():
    PAttack = random.randint(PlayerIG.attack / 2, PlayerIG.attack)
    EAttack = random.randint(enemy.attack / 2, enemy.attack)
    if PAttack == PlayerIG.attack / 2:
        print "You miss!"
    else:
        enemy.health -= PAttack
        print "You deal %i damage!" % PAttack
    option = raw_input(' ')
    if enemy.health <=0:
        win()
    if EAttack == enemy.attack/2:
        print "The enemy missed!"
    else:
        PlayerIG.health -= EAttack
        print "The enemy deals %i damage!" % EAttack
    option = raw_input(' ')
    if PlayerIG.health <= 0:
        dead()
    else:
        fight()

def magic_attack():
    if PlayerIG.magic >= 5:
        print "\nYou throw thunderbolt directly at %s and deal 15 damage\n" % (enemy.name)
        option = raw_input(' ')
        enemy.health -= 15
        PlayerIG.magic -= 5
        if enemy.health <= 0:
            win()
        fight()
    else:
        print "You don't have enough magic points!"
        fight()

def drinkpot():
    if PlayerIG.pots == 0:
        print "You don't have any potions!"
    else:
        PlayerIG.health += 50
        if PlayerIG.health > PlayerIG.maxhealth:
            PlayerIG.health = PlayerIG.maxhealth
        PlayerIG.pots -= 1
        print "You drank a potion!"
    option = raw_input(' ')
    fight()

def run():
    runnum = random.randint(1, 3)
    if runnum == 1:
        print "You have successfully ran away!"
        option = raw_input(' ')
        start1()
    else:
        print "You failed to get away!"
        option = raw_input(' ')
        EAttack = random.randint(enemy.attack / 2, enemy.attack)
        if EAttack == enemy.attack/2:
            print "The enemy missed!"
        else:
            PlayerIG.health -= EAttack
            print "The enemy deals %i damage!" % EAttack
        option = raw_input(' ')
        if PlayerIG.health <= 0:
            dead()
        else:
            fight()

def win():
    enemy.health = enemy.maxhealth
    PlayerIG.gold += enemy.goldgain
    print "You have defeated the %s" % enemy.name
    print "You found %i gold!" % enemy.goldgain
    option = raw_input(' ')
    global turn
    turn += 1
    start1()

def dead():
    print "You have died"
    option = raw_input(' ')

def store():
    print "Welcome to the shop!"
    print "\nWhat would you like to buy?\n"
    print "1.) Great Axe 40 gold"
    print "2.) Health Potion 20 gold"
    print "3.) Back"
    print "Your gold: %i" % PlayerIG.gold
    print " "
    option = raw_input(' ')

    if option == "1":
        if PlayerIG.gold >= weapons["Great Axe"]:
            PlayerIG.gold -= weapons["Great Axe"]
            PlayerIG.weap.append("Great Axe")
            PlayerIG.curweap = "Great Axe"
            print "You have bought Great Axe"
            option = raw_input(' ')
            store()

        else:
            print "You don't have enough gold"
            option = raw_input(' ')
            store()

    elif option == "2":
        if PlayerIG.gold >= 20:
            PlayerIG.pots += 1
            PlayerIG.gold -= 20
            print "You have bought one health potion\n"
            option = raw_input(' ')
            store()
        else:
            print "Not enough gold! Potion cost 20 gold"
            store()

    elif option == "3":
        start1()

    else:
        print "That item does not exist"
        option = raw_input(' ')
        store()

def ending():
    print "Gongratulations! You have slayed all the monsters who took your daughter\n and saved her. Although your wife hanged herself during your adventure, so all worked out.\n"
    sys.exit()

main()