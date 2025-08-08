import os
import csv
import random

def read_csv(csv_file):
    with open(csv_file, mode="r",newline="",encoding='utf-8') as reward_csv:
        Reader = csv.DictReader(reward_csv)
        rows = list(Reader)
    return rows

# Parameters set for loot generation.
if os.name == 'nt':
    reward_db_location = os.path.dirname(__file__) + "\\" + "Reward_DB.csv"
    weapon_db = os.path.dirname(__file__) + "\\" + "Weapons.csv"
    spell_db = os.path.dirname(__file__) + "\\" + "Spells.csv"
    armors_db = os.path.dirname(__file__) + "\\" + "Armors.csv"
    enchantments_db = os.path.dirname(__file__) + "\\" + "Enchantments.csv"

if os.name == 'posix':
    reward_db_location = os.path.dirname(__file__) + "/" + "Reward_DB.csv"
    weapon_db = os.path.dirname(__file__) + "/" + "Weapons.csv"
    spell_db = os.path.dirname(__file__) + "/" + "Spells.csv"
    armors_db = os.path.dirname(__file__) + "/" + "Armors.csv"
    enchantments_db = os.path.dirname(__file__) + "/" + "Enchantments.csv"

reward_db = read_csv(reward_db_location)

# we can slightly change the weights probably by adding more weight to one but that can be a later mechanic.

ItemCategory_Weights = [{"Category": "Weapon", "Weight": 0.4},
    {"Category": "Armor", "Weight": 0.4},
    {"Category": "Blessing", "Weight": 0.2},
    {"Category": "Consumable", "Weight": 0.6},
    {"Category": "Accessory", "Weight": 0.5},] # Change this depending if there is a limit to how many magic items a player can equip. (current thought is 5)

itemType = [lootType['Category'] for lootType in ItemCategory_Weights]
item_Weights = [lootType['Weight'] for lootType in ItemCategory_Weights]

generated_loot_types = random.choices(itemType, weights=item_Weights, k=3)
for loot_type in generated_loot_types:
    if loot_type == "Accessory":
        accessories = [item for item in reward_db if item['Category'] == "Accessory"]
        accessories_weights = [float(item['Weight']) for item in accessories]
        accessory = random.choices(accessories, weights=accessories_weights, k=1)[0]
        #print(accessory)
    
    if loot_type == "Blessing":
        blessings = [item for item in reward_db if item['Category'] == "Blessing"]
        blessing_weights = [float(item['Weight']) for item in blessings]
        blessing = random.choices(blessings, weights=blessing_weights, k=1)[0]
        #print(blessing)

    if loot_type == "Weapon":
        weapons = read_csv(weapon_db)
        random.choice(weapons)
    
    if loot_type == "Armor":
        armors = read_csv(armors_db)
        armor_weights = [float(armor['Weight']) for armor in armors]
        selected_armor = random.choices(armors, weights=armor_weights, k=1)[0]
        #print(selected_armor)

    if loot_type == "Consumable":
        # Want to randomize between spell scrolls and consumables.
        consumable_type = [{"Category": "Consumable", "Weight": 0.7},{"Category": "Spells", "Weight": 0.6}]
        consumable_weight = [float(item_type["Weight"]) for item_type in consumable_type]
        consumable_type = [item_type["Category"] for item_type in consumable_type]
        item_type = random.choices(consumable_type, weights=consumable_weight)[0]
        if item_type == "Consumable":
            consumables = [item for item in reward_db if item['Category'] == "Consumable"]
            consumable_weight = [float(item["Weight"]) for item in reward_db if item['Category'] == "Consumable"]
            selected_consumable = random.choices(consumables, weights=consumable_weight, k=1)[0]
            #print(selected_consumable)
        else:
            spell_weights = [
                {"Level": 0, "Weight": 0.6},
                {"Level": 1, "Weight": 0.6},
                {"Level": 2, "Weight": 0.5},
                {"Level": 3, "Weight": 0.4},
                {"Level": 4, "Weight": 0.3},
                {"Level": 5, "Weight": 0.2},
                {"Level": 6, "Weight": 0.1},
                {"Level": 7, "Weight": 0.05},
                {"Level": 8, "Weight": 0.025},
                {"Level": 9, "Weight": 0.001}
            ]



#print(generated_loot_types)
# just checking item spread.
#for i in range(0, 100):
#    print(random.choices(itemType, weights=item_Weights, k=3))



#for loot_type in generated_loot_types:



#for items in enumerate(reward_db):
#    print(items[1]['Weight'])