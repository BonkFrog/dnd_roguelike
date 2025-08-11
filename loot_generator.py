import os
import csv
import random

def read_csv(csv_file):
    # Had to change the encoding to utf-8-sig to remove the \ufeff prefix
    with open(csv_file, mode="r",newline="",encoding='utf-8-sig') as reward_csv:
        Reader = csv.DictReader(reward_csv)
        data = list(Reader)
    return data

def enchant(item, enchant_db):
    if "Weapon" in item:
        item_base = "Weapon"
        item_category = item['Category']
    if "Armor" in item:
        item_base = "Armor"
        item_category = "Armor"

    def add_affix(item, item_base, enchant):
        if enchant['Affix'] == "Prefix":
            item[item_base] = enchant['Enchantments'] + " " + item[item_base]
            item.update({"enchant_description": enchant['Description']})
        else:
            item[item_base] = item[item_base] + " " + enchant['Enchantments']
            item.update({"enchant_description": enchant['Description']})
        return item

    # will probably change this into a json file to be imported later instead.
    # I had a 1 in the enchantment weights, it didnt produce the enchantments I wanted.
    enchant_weights = [0.6, 0.3, 0.1]
    chosen_weight = random.choices(enchant_weights, weights=enchant_weights, k=1)[0]
    enchantment_list = read_csv(enchant_db)
    if chosen_weight != 1:
        filtered_enchantments = [enchant for enchant in enchantment_list if float(enchant['Weight']) == float(chosen_weight)]
        enchantment_weights = [float(enchant['Weight']) for enchant in enchantment_list if float(enchant['Weight']) == float(chosen_weight)]
        chosen_enchantment = random.choices(filtered_enchantments, weights=enchantment_weights, k=1)[0]
        while chosen_enchantment['Category'] != item_category:
            chosen_enchantment = random.choices(filtered_enchantments, weights=enchantment_weights, k=1)[0]
    match chosen_weight:
        case _ if chosen_weight == 1:
            item[item_base] = item[item_base] + " +1"
            return print(item)
        case _ if chosen_weight == 0.6:
            Item_Rarity = random.randint(0,1)
            if Item_Rarity == 0:
                item[item_base] = item[item_base] + " +1"
                return print(item)
            else:
                add_affix(item, item_base, chosen_enchantment)
                print(item)
        case _ if chosen_weight == 0.3:
            Item_Rarity = random.randint(0,1)
            if Item_Rarity == 0:
                item[item_base] = item[item_base] + " +2"                    
                return print(item)
            if Item_Rarity == 1:
                add_affix(item, item_base, chosen_enchantment)
                item[item_base] = item[item_base] + " +1"
                return print(item)
        case _ if chosen_weight == 0.1:
            Item_Rarity = random.randint(0,1)
            if Item_Rarity == 0:
                item[item_base] = item[item_base] + " +3"                    
                return print(item)
            if Item_Rarity == 1:
                add_affix(item, item_base, chosen_enchantment)
                item[item_base] = item[item_base] + " +2"
                return print(item)

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
# will probably change this into a json file to be imported later instead.
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
        selected_weapon = random.choice(weapons)
        #print(selected_weapon)
        enchant(selected_weapon, enchantments_db)

    if loot_type == "Armor":
        armors = read_csv(armors_db)
        armor_weights = [float(armor['Weight']) for armor in armors]
        selected_armor = random.choices(armors, weights=armor_weights, k=1)[0]
        #print(selected_armor)
        enchant(selected_armor, enchantments_db)
    if loot_type == "Consumable":
        # Want to randomize between spell scrolls and consumables.
        # will probably change this into a json file to be imported later instead.
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
           #print(selected_spell)
