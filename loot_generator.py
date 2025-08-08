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
    if loot_type == "Weapon":
        weapons = read_csv(weapon_db)
        random.choice(weapons)
    if loot_type == "Armor":
        armors = read_csv(armors_db)
        armor_weights = [float(armor['Weight']) for armor in armors]
        selected_armor = random.choices(armors, weights=armor_weights, k=1)[0]
        #print(selected_armor)
    if loot_type == "Blessing":
        blessings = [item for item in reward_db if item['Category'] == "Blessing"]
        blessing_weights = [float(item['Weight']) for item in blessings]
        blessing = random.choices(blessings, weights=blessing_weights, k=1)[0]
        print(blessing)

    if loot_type == "Consumable":
        # Want to randomize between spell scrolls and consumables.
        consumable_type = [{"Category": "Consumable", "Weight": 0.7},{"Category": "Spells", "Weight": 0.6}]
        consumable_weight = [float(item_type["Weight"]) for item_type in consumable_type]
        consumable_type = [item_type["Category"] for item_type in consumable_type]
        item_type = random.choices(consumable_type, weights=consumable_weight)
    if loot_type == "Accessory":
        pass

#print(generated_loot_types)
# just checking item spread.
#for i in range(0, 100):
#    print(random.choices(itemType, weights=item_Weights, k=3))



#for loot_type in generated_loot_types:



#for items in enumerate(reward_db):
#    print(items[1]['Weight'])