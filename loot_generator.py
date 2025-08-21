import os
import csv
import random
import json

def read_csv(csv_file):
    # Had to change the encoding to utf-8-sig to remove the \ufeff prefix
    with open(csv_file, mode="r",newline="",encoding='utf-8-sig') as reward_csv:
        Reader = csv.DictReader(reward_csv)
        data = list(Reader)
    return data

def read_json(json_file_path):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)
    return json_data

def enchant_item(item):
    if os.name == 'nt':
        enchantments_db = os.path.dirname(__file__) + "\\dbs\\Enchantments.csv"
    if os.name == 'posix':
        enchantments_db = os.path.dirname(__file__) + "/dbs/Enchantments.csv"
        
    if "Weapon" == item['Category']:
        item_category = item['Weapon_Type']
    if "Armor" == item['Category']:
        item_category = "Armor"

    def add_affix(item, enchant):
        if enchant['Affix'] == "Prefix":
            item['name'] = enchant['Enchantments'] + " " + item['name']
            item.update({"enchant_description": enchant['Description']})
        else:
            item['name'] = item['name'] + " " + enchant['Enchantments']
            item.update({"enchant_description": enchant['Description']})
        return item

    # will probably change this into a json file to be imported later instead.
    # I had a 1 in the enchantment weights, it didnt produce the enchantments I wanted.
    enchant_weights = [0.6, 0.3, 0.1]
    chosen_weight = random.choices(enchant_weights, weights=enchant_weights, k=1)[0]
    enchantment_list = read_csv(enchantments_db)

    if chosen_weight != 1:

        filtered_enchantments = [enchant for enchant in enchantment_list if float(enchant['Weight']) == float(chosen_weight)]
        enchantment_weights = [float(enchant['Weight']) for enchant in enchantment_list if float(enchant['Weight']) == float(chosen_weight)]
        chosen_enchantment = random.choices(filtered_enchantments, weights=enchantment_weights, k=1)[0]
        while chosen_enchantment['Category'] != item_category:
            chosen_enchantment = random.choices(filtered_enchantments, weights=enchantment_weights, k=1)[0]

    match chosen_weight:
        case _ if chosen_weight == 1:
            item['name'] = item['name'] + " +1"
            return item
        case _ if chosen_weight == 0.6:
            Item_Rarity = random.randint(0,1)
            if Item_Rarity == 0:
                item['name'] = item['name'] + " +1"
                return item
            else:
                add_affix(item, chosen_enchantment)
                return item
        case _ if chosen_weight == 0.3:
            Item_Rarity = random.randint(0,1)
            if Item_Rarity == 0:
                item['name'] = item['name'] + " +2"                    
                return item
            if Item_Rarity == 1:
                add_affix(item, chosen_enchantment)
                item['name'] = item['name'] + " +1"
                return item
        case _ if chosen_weight == 0.1:
            Item_Rarity = random.randint(0,1)
            if Item_Rarity == 0:
                item['name'] = item['name'] + " +3"                    
                return item
            if Item_Rarity == 1:
                add_affix(item, chosen_enchantment)
                item['name'] = item['name'] + " +2"
                return item

def grab_spell_scroll():
    if os.name == 'nt':
        spell_db = os.path.dirname(__file__) + "\\dbs\\Spells.csv"
    if os.name == 'posix':
        spell_db = os.path.dirname(__file__) + "/dbs/Spells.csv"

    # will probably change this into a json file to be imported later instead.
    spell_weights_legend = [
        {"Level": 0, "Weight": 0.6},
        {"Level": 1, "Weight": 0.7},
        {"Level": 2, "Weight": 0.6},
        {"Level": 3, "Weight": 0.5},
        {"Level": 4, "Weight": 0.4},
        {"Level": 5, "Weight": 0.2},
        {"Level": 6, "Weight": 0.1},
        {"Level": 7, "Weight": 0.05},
        {"Level": 8, "Weight": 0.025},
        {"Level": 9, "Weight": 0.001}
    ]
    # Pull randomized item weights for spell levels
    spell_weights = [float(spell_type["Weight"]) for spell_type in spell_weights_legend]
    spell_levels = [spell_type["Level"] for spell_type in spell_weights_legend]
    selected_spell_level = random.choices(spell_levels, weights=spell_weights, k=1)[0]

    # Grab a random spell within the chosen spell level
    spells = read_csv(spell_db)
    spell_list = [spell for spell in spells if int(spell['level']) == int(selected_spell_level)]
    selected_spell = random.choice(spell_list)

    # Add the prefix "Scroll of"
    spell_scroll_name = "Scroll of " + selected_spell['name']
    selected_spell['name'] = spell_scroll_name

    # Add Scroll Mechanics in the description.
    scroll_description = "You can cast the inscribed spell on this scroll with the inscribed spell's cast time. Any class can cast the spell. If the spell requires a ability modifier or saving throw (8 + ability modifier), use the following ability modifier: WIS, CHA, INT. Once casted, the scroll embers away."
    selected_spell.update({"scroll_description": scroll_description})
    return selected_spell

def grab_consumable():
    #This function does not include spell scrolls despite both being a consumable.
    if os.name == 'nt':
        reward_db_location = os.path.dirname(__file__) + "\\dbs\\Reward_DB.csv"
    if os.name == 'posix':
        reward_db_location = os.path.dirname(__file__) + "/dbs/Reward_DB.csv"

    reward_db = read_csv(reward_db_location)

    consumables = [item for item in reward_db if item['Category'] == "Consumable"]
    consumable_weight = [float(item["Weight"]) for item in reward_db if item['Category'] == "Consumable"]
    selected_consumable = random.choices(consumables, weights=consumable_weight, k=1)[0]
    return selected_consumable

def generate_blessings(k=3):
    if os.name == 'nt':
        reward_db_location = os.path.dirname(__file__) + "\\dbs\\Reward_DB.csv"
    if os.name == 'posix':
        reward_db_location = os.path.dirname(__file__) + "/dbs/Reward_DB.csv"
    
    list_of_loot = []
    reward_db = read_csv(reward_db_location)

    for i in range(0,k):
        blessings = [item for item in reward_db if item['Category'] == "Blessing"]
        blessings_weight = [float(item["Weight"]) for item in reward_db if item['Category'] == "Blessing"]
        selected_blessing = random.choices(blessings, weights=blessings_weight, k=1)[0]
        list_of_loot.append(selected_blessing)
    
    return list_of_loot

def generate_accessories(k=3):
    if os.name == 'nt':
        reward_db_location = os.path.dirname(__file__) + "\\dbs\\Reward_DB.csv"
    if os.name == 'posix':
        reward_db_location = os.path.dirname(__file__) + "/dbs/Reward_DB.csv"
    
    list_of_loot = []
    reward_db = read_csv(reward_db_location)

    for i in range(0,k):
        accessory_list = [item for item in reward_db if item['Category'] == "Accessory"]
        accessory_weight = [float(item["Weight"]) for item in reward_db if item['Category'] == "Accessory"]
        selected_accessory = random.choices(accessory_list, weights=accessory_weight, k=1)[0]
        list_of_loot.append(selected_accessory)
    
    return list_of_loot

def generate_consumables(k=3,mix=True,consumable=False,spell=False):
    # Set parameters
    list_of_loot = []

    if consumable == True and spell == True:
        raise ValueError(f"Both spell and consumable parameters cannot be true.")
    
    # This sets mix to false if any of the other parameters are true.
    if ((consumable == True) or (spell == True)):
        mix = False

    for i in range(0,k):
        if mix == True:
            consumable_type = [{"Category": "Consumable", "Weight": 0.7},{"Category": "Spells", "Weight": 0.6}]
            consumable_weight = [float(item_type["Weight"]) for item_type in consumable_type]
            consumable_type = [item_type["Category"] for item_type in consumable_type]
            item_type = random.choices(consumable_type, weights=consumable_weight)[0]
            if item_type == "Consumable":
                list_of_loot.append(grab_consumable())
            else:
                list_of_loot.append(grab_spell_scroll())
        if consumable == True:
            list_of_loot.append(grab_consumable())
        if spell == True:
            list_of_loot.append(grab_spell_scroll())
    return list_of_loot

def generate_weapons(k=1,enchant=False):
    if os.name == 'nt':
        weapon_db = os.path.dirname(__file__) + "\\dbs\\Weapons.csv"
    if os.name == 'posix':
        weapon_db = os.path.dirname(__file__) + "/dbs/Weapons.csv"
    
    weapons = read_csv(weapon_db)

    if k == 1:
        selected_weapon = random.choice(weapons)
        if enchant == True:
            return enchant_item(selected_weapon)
        return selected_weapon

    list_of_loot = [] 
    for i in range(0,k):
        selected_weapon = random.choice(weapons)
        if enchant == True: 
            list_of_loot.append(enchant_item(selected_weapon))
        else:
            list_of_loot.append(enchant_item(selected_weapon))
    return list_of_loot

def generate_armors(k=1,enchant=False):
    if os.name == 'nt':
        armors_db = os.path.dirname(__file__) + "\\dbs\\Armors.csv"
    if os.name == 'posix':
        armors_db = os.path.dirname(__file__) + "/dbs/Armors.csv"

    armors = read_csv(armors_db)
    if k == 1:
        selected_armors = random.choice(armors)
        if enchant == True:
            return enchant_item(selected_armors)
        return selected_armors

    list_of_loot = [] 
    for i in range(0,k):
        selected_armors = random.choice(armors)
        if enchant == True: 
            list_of_loot.append(enchant_item(selected_armors))
        else:
            list_of_loot.append(enchant_item(selected_armors))
    return list_of_loot

# Milestone: Lets add some character level logic in next time. because this shit is way over powered for lower levels!
def generate_loot(player_level=1, k=3):
# Parameters set for loot generation.
    if os.name == 'nt':
        reward_db_location = os.path.dirname(__file__) + "\\dbs\\Reward_DB.csv"
        item_category_weights_location = os.path.dirname(__file__) + "\\configs\\item_category_drop_rates.json"
        player_level_weights_location = os.path.dirname(__file__) + "\\configs\\loot_level_weights.json"
    
    if os.name == 'posix':
        reward_db_location = os.path.dirname(__file__) + "/dbs/Reward_DB.csv"
        item_category_weights_location = os.path.dirname(__file__) + "/configs/item_category_drop_rates.json"
        player_level_weights_location = os.path.dirname(__file__) + "/configs/loot_level_weights.json"
    
    list_of_loot = []
    reward_db = read_csv(reward_db_location)

    # Finally added the json file import to make adjustments easier.
    ItemCategory_Weights = read_json(item_category_weights_location) 

    itemType = [lootType['Category'] for lootType in ItemCategory_Weights]
    item_Weights = [lootType['Weight'] for lootType in ItemCategory_Weights]

    generated_loot_types = random.choices(itemType, weights=item_Weights, k=k)
    for loot_type in generated_loot_types:
        if loot_type == "Accessory":
            accessories = [item for item in reward_db if item['Category'] == "Accessory"]
            accessories_weights = [float(item['Weight']) for item in accessories]
            accessory = random.choices(accessories, weights=accessories_weights, k=1)[0]
            list_of_loot.append(accessory)

        if loot_type == "Blessing":
            blessings = [item for item in reward_db if item['Category'] == "Blessing"]
            blessing_weights = [float(item['Weight']) for item in blessings]
            blessing = random.choices(blessings, weights=blessing_weights, k=1)[0]
            list_of_loot.append(blessing)

        if loot_type == "Weapon":
            list_of_loot.append(generate_weapons(k=1, enchant=True))

        if loot_type == "Armor":
            list_of_loot.append(generate_armors(k=1, enchant=True))

        if loot_type == "Consumable":
            # Want to randomize between spell scrolls and consumables.
            # will probably change this into a json file to be imported later instead.
            consumable_type = [{"Category": "Consumable", "Weight": 0.7},{"Category": "Spells", "Weight": 0.6}]
            consumable_weight = [float(item_type["Weight"]) for item_type in consumable_type]
            consumable_type = [item_type["Category"] for item_type in consumable_type]
            item_type = random.choices(consumable_type, weights=consumable_weight)[0]
            if item_type == "Consumable":
                list_of_loot.append(grab_consumable())
            else:
                list_of_loot.append(grab_spell_scroll())
    return list_of_loot

configs = '/home/agave/Repos/dnd_roguelike/configs/item_drop_rates.json'
print(read_json(configs))