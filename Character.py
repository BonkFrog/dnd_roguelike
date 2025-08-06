import json 
import os

# Check if the environment is windows or linux
if os.name == 'nt':
    save_location = os.path.dirname(__file__) + "\\" + "profiles" + "\\"
if os.name == 'posix':
    save_location = os.path.dirname(__file__) + "/" + "profiles" + "/"

# Create basic classes for the characters
class chara:
    # Constructor to create my class object
    def __init__(self, player = "", chara_name = "", chara_class = "", save_file = ""):
        self.player = player
        self.chara_name = chara_name
        self.chara_class = chara_class
        self.proficiency = 2
        self.AC = 10
        self.speed = 30
        self.initiative = 0
        self.gold = 5
        self.ability_score = [{"STR":10},{"DEX":10},{"CON":10},{"INT":10},{"WIS":10},{"CHA":10}]
        self.inventory = []
        self.__save_file = save_file

    # defines how a class gets represented for the user.
    def __str__(self):
        # Get the max count for the property names string len and add 2 spaces 
        str_count = [len(item[0]) for item in self]
        max_spaces = max(str_count) + 2 
        
        character_sheet = []
        
        for item in self:
            
            # Same thing for ability score cause that is nested dictionary, we want to print it nicely.
            if item[0] == "ability_score":
                # print out the ability score part so it looks nicer.
                character_sheet.append(f"{item[0]}".ljust(max_spaces))

                ability_score = item[1]
                score_count = [len(score) for score in ability_score]
                max_score_spaces = max(score_count) + 7

                for score in ability_score:
                    # this is how to seperate the name and values of a dictionary.
                    score_name, score_value = list(score.items())[0]
                    character_sheet.append(f"   {score_name}".ljust(max_score_spaces) + "|  " + f"{score_value}")
                continue

            # Do later when I implement loot.
            if item[0] == "inventory":
                #print(True)
                pass
            
            # Makes it so we dont print any of the hidden classes.
            if item[0].startswith("_"):
                continue

            character_sheet.append(f"{item[0]}".ljust(max_spaces) + "|  " + f"{item[1]}")
        
        # Chat recommended this way to iterate a print. idk if there are better ways but this is an easy one to return a string.
        return "\n".join([line for line in character_sheet])

    # This is how to may my object iterable
    def __iter__(self):
        # the object needs a return iterator with the iter() function
        return iter(vars(self).items())
    
    def save_chara(self, path = ""):
        if (self.__save_file != "") and (path != ""):
            path = self.__save_file

        # save a dictionary values from the object into 
        save_location = path + self.chara_name + "_" + self.chara_class + ".json"
        with open(save_location, "w") as json_file:
            json.dump(vars(self), json_file, indent=4)

        if os.path.isfile(save_location):
            return True
        else:
            return False
    
    def load_chara(self, path):
        with open(path, 'r') as file:
            data = json.load(file)
            # __dict__ special attribute which describe the object in question in dictionary format. 
            self.__dict__.update(data)
            self.__save_file = path
            file.close()

    def update_asi(self, asi_name: str, operation:str ,value:int):

        # ASI Input Validation
        acceptable_asi_values = ["STR","DEX","CON","INT","WIS","CHA"]
        asi_name = asi_name.upper()
        if not asi_name in acceptable_asi_values:
            raise ValueError(f"Invalid Ability Score: {asi_name} \nPlease use a valid ASI: {acceptable_asi_values}")

        # Operation Input Validation
        acceptable_operation_values = ["+", "-"]
        if not operation in acceptable_operation_values:
            raise ValueError (f"Invalid Operation: {operation} \nPlease use a valid ASI: {acceptable_operation_values}")

        abilitiy_scores = self.ability_score
        for score in abilitiy_scores:
            #index = score[0]
            score_name, score_value = list(score.items())[0]
            return abilitiy_scores[asi_name]
            #if asi_name == score_name:
                #if operation == "-":
                #    self.ability_score
        
#Test = chara(player = "Derick", chara_name = "Edwin", chara_class = "Warrior")
#Test.save_chara(path=save_location)

Test = chara(player = "placeholder", chara_name = "placeholder", chara_class = "placeholder")
Test.load_chara(path="/home/agave/Repos/dnd_roguelike/profiles/_Edwin_Warrior.json")
print(Test.update_asi("con","-",3))