import json 
import os

# Check if the environment is windows or linux
if os.name == 'nt':
    save_location = os.path.dirname(__file__) + "\\" + "profiles"
if os.name == 'posix':
    save_location = os.path.dirname(__file__) + "/" + "profiles"

# Create basic classes for the characters
class chara:

    # Constructor to create my class object
    def __init__(self, player, chara_name, chara_class):
        self.player = player
        self.chara_name = chara_name
        self.chara_class = chara_class
        self.proficiency = 2
        self.AC = 10
        self.speed = 30
        self.initiative = 0
        self.gold = 5
        self.ability_score = [{"STR":10},{"Dex":10},{"CON":10},{"INT":10},{"WIS":10},{"CHA":10}]
        self.inventory = []
        self.gold = 5
    
    # defines how a class gets represented for the user.
    def __str__(self):
        # vars(), this returns properties and values in dictionary format for the variable specified.
        return "\n".join([f"{attr}: {value}" for attr, value in vars(self).items()])

    # This is how to may my object iterable
    def __iter__(self):
        # the object needs a return iterator with the iter() function
        return iter(vars(self).items())
    
Test = chara(player = "Derick", chara_name = "Edwin", chara_class = "Warrior")

str_count = [len(item[0]) for item in Test]
max_spaces = max(str_count) + 2

for item in Test:
    if item[0] == "ability_score":
        ability_score = item[1]
        score_count = [len(score) for score in ability_score]
        max_score_spaces = max(score_count) + 7

        print(f"{item[0]}".ljust(max_spaces))

        for score in ability_score:
            # this is how to seperate the name and values
            score_name, score_value = list(score.items())[0]
            print(f"   {score_name}".ljust(max_score_spaces) + "|  " + f"{score_value}")

        continue

    # Do later when I implement loot.
    if item[0] == "inventory":
        #print(True)
        pass
    print(f"{item[0]}".ljust(max_spaces) + "|  " + f"{item[1]}")