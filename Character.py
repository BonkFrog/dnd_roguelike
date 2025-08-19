import json 
import os
import loot_generator as loot

# Create basic classes for the characters
class chara:

    # This spaces out the text in a nice format.
    # just make it accept a tuple, its just easier that way.
    def spacing(self, tuple_array, spacing = 2):
        str_count = [len(item[0]) for item in tuple_array]
        
        text_array = []
        for item in tuple_array:
            spacing = item[-1]
            max_spaces = max(str_count) + spacing
            text_array.append(f"{item[0]}".ljust(max_spaces) + "|  " + f"{item[1]}")
        return text_array
               
    # Constructor to create my class object
    def __init__(self, player = "", chara_name = "", chara_class = "", save_file = ""):
        self.player = player
        self.chara_name = chara_name
        self.chara_class = chara_class
        self.level = 1
        self.proficiency = 2
        self.AC = 10
        self.speed = 30
        self.initiative = 0
        self.gold = 5
        self.ability_score = {"STR":10, "DEX":10, "CON":10, "INT":10, "WIS":10, "CHA":10}
        self.inventory = []
        self.__save_file = save_file if save_file != "" else ""
        self.__save_item_choice = []

    # defines how a class gets represented for the user.
    def __str__(self):
        character_info = [(key, value) for key, value in self]
        character_info = []
        for key, value in self:
            if key == 'ability_score':
                character_info.append((key, "", 2))
                for score_name, score_va1ue in value.items():
                    score_name = "  " + score_name
                    ability_score_tuple = (score_name, score_va1ue, -5)
                    character_info.append(ability_score_tuple)
                continue
            
            if key.startswith("_"):
                continue
            base_character_tuple = (key, value, 2)
            character_info.append(base_character_tuple)

        new_list = self.spacing(character_info)
        return "\n".join([line for line in new_list])

    # This is how to may my object iterable
    def __iter__(self):
        # the object needs a return iterator with the iter() function
        return iter(vars(self).items())
    
    def save_chara(self, path = ""):
        if self.__save_file != "":
            path = self.__save_file
        else :
            path = path + self.player + "_" +self.chara_name + "_" + self.chara_class + ".json"
        
        # save a dictionary values from the object into 
        with open(path, "w") as json_file:
            json.dump(vars(self), json_file, indent=4)

        if os.path.isfile(path):
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

        if operation == "+":
            self.ability_score[asi_name] += value
        else:
            self.ability_score[asi_name] -= value
        
        self.save_chara()
        return f"{asi_name} is now {self.ability_score[asi_name]}"
    
    def update_property(self, property, operation, value):
        if (property == "ability_score") or (property == "inventory"):
            raise ValueError (f"Invalid Property {property}, please use another one.")
        if property in ['player','chara_name','chara_class']:
            setattr(self, property, value)
            self.save_chara()
            return {f"{property} is now {value}"}
        if not type(value) is int:
            raise ValueError(f"value must be an integer")
        if operation == "+":
            current_value = getattr(self, property)
            setattr(self, property, (current_value + value))
            self.save_chara()
            return f"{property} is now {getattr(self, property)}"
        else:
            current_value = getattr(self, property)
            setattr(self, property, (current_value - value))
            self.save_chara()
            return f"{property} is now {getattr(self, property)}"

    def save_choice(self, items):
        if len(self.__save_item_choice) > 3:
            raise ValueError (f"{self.chara_name} still has to select loot")
        for item in items:
            self.__save_item_choice.append(item)
        self.save_chara()
        return self
    
    def select_choice(self):
        selectable_choices = []
        i = 1
        for choice in self.__save_item_choice:
            choice_format = f"{i}: {choice['name']} | {choice['Category']}"
            selectable_choices.append(choice_format)
            i += 1
        return "\n".join([choice for choice in selectable_choices])

# Check if the environment is windows or linux
if os.name == 'nt':
    save_location = os.path.dirname(__file__) + "\\" + "profiles" + "\\"
if os.name == 'posix':
    save_location = os.path.dirname(__file__) + "/" + "profiles" + "/"

#Test = chara(player = "Derick", chara_name = "Edwin", chara_class = "Warrior")
#Test.save_chara(path=save_location)

Test = chara(player = "Dedrick", chara_name = "Edwin", chara_class = "Warrior")
Test.load_chara(path="/home/agave/Repos/dnd_roguelike/profiles/Dedrick_Edwin_Warrior.json")
#Test.save_chara(path=save_location)
g_loots = loot.generate_loot(3)
print(Test)
#for g_loot in g_loots:
#    print(g_loot)
#

#Test.save_choice(g_loots)
#Test.save_chara(path=save_location)
#print(Test.select_choice())
#print(Test.update_property(property="gold", operation="+",value= 10))