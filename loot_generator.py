import os
import csv
import random

def read_loot_csv(reward_db_location):
    with open(reward_db_location, mode="r",newline="") as reward_csv:
        Reader = csv.DictReader(reward_csv)
        rows = list(Reader)
    return rows
if os.name == 'nt':
    reward_db_location = os.path.dirname(__file__) + "\\" + "Reward_DB.csv"
if os.name == 'posix':
    reward_db_location = os.path.dirname(__file__) + "/" + "Reward_DB.csv"

reward_db = read_loot_csv(reward_db_location)

ItemCategory_Weights = [{"Category": "Weapon", "Weight": 0.4},
    {"Category": "Armor", "Weight": 0.4},
    {"Category": "Blessing", "Weight": 0.2},
    {"Category": "Consumable", "Weight": 0.6},
    {"Category": "Accessory", "Weight": 0.5},] # Change this depending if there is a limit to how many magic items a player can equip. (current thought is 5)

itemType = [lootType['Category'] for lootType in ItemCategory_Weights]
item_Weights = [lootType['Weight'] for lootType in ItemCategory_Weights]

# just checking item spread.
#for i in range(0, 100):
#    print(random.choices(itemType, weights=item_Weights, k=3))

#for items in enumerate(reward_db):
#    print(items[1]['Weight'])