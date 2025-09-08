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

def get_player_loot_scheme(player_level=1, category="level"):
    if os.name == 'nt':
        player_level_weights_location = os.path.dirname(__file__) + "\\configs\\loot_level_weights.json"
        spell_level_weights_location = os.path.dirname(__file__) + "\\configs\\spell_level_drop_rate.json"
    if os.name == 'posix':
        player_level_weights_location = os.path.dirname(__file__) + "/configs/loot_level_weights.json"
        spell_level_weights_location = os.path.dirname(__file__) + "/configs/spell_level_drop_rate.json"

    if category == "level":
        loot_weights = read_json(player_level_weights_location)
    if category == "spell":
        loot_weights = read_json(spell_level_weights_location)

    for loot_weight in loot_weights:
        if loot_weight['Level'] == player_level:
            loot_scheme = loot_weight
    return loot_scheme

def enchant_item(item, player_level=1):
    if os.name == 'nt':
        enchantments_db = os.path.dirname(__file__) + "\\dbs\\Enchantments.csv"
    if os.name == 'posix':
        enchantments_db = os.path.dirname(__file__) + "/dbs/Enchantments.csv"

    # Get Player loot scheme
    loot_scheme = get_player_loot_scheme(player_level=player_level)
    valid_rarities   = [r for r, w in loot_scheme['Weights'].items() if w > 0]
    valid_weights    = [w for r, w in loot_scheme['Weights'].items() if w > 0]

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
    chosen_rarity = random.choices(valid_rarities, weights=valid_weights, k=1)[0]
    enchantment_list = read_csv(enchantments_db)

    if chosen_rarity != "Common":

        filtered_enchantments = [enchant for enchant in enchantment_list if enchant['Rarity'] == chosen_rarity]
        #enchantment_weights = [float(enchant['Rarity']) for enchant in enchantment_list if enchant['Rarity'] == chosen_rarity]
        enchant_pool = []
        enchant_weight = []
        for f_enchant in filtered_enchantments:
            if f_enchant['Rarity'] in valid_rarities:
                match f_enchant['Rarity']:
                    case "Common":
                        f_enchant['Rarity'] = valid_weights[0]
                        enchant_weight.append(valid_weights[0])
                    case "Uncommon":
                        f_enchant['Rarity'] = valid_weights[1]
                        enchant_weight.append(valid_weights[1])
                    case "Rare":
                        f_enchant['Rarity'] = valid_weights[2]
                        enchant_weight.append(valid_weights[2])
                    case "Legendary":
                        f_enchant['Rarity'] = valid_weights[3]
                        enchant_weight.append(valid_weights[3])
                enchant_pool.append(f_enchant)
                
        chosen_enchantment = random.choices(enchant_pool, weights=enchant_weight, k=1)[0]
        while chosen_enchantment['Category'] != item_category:
            chosen_enchantment = random.choices(enchant_pool, weights=enchant_weight, k=1)[0]

    match chosen_rarity:
        case _ if chosen_rarity == "Common":
            item['name'] = item['name'] + " +1"
            return item
        case _ if chosen_rarity == "Uncommon":
            Item_Rarity = random.randint(0,1)
            if Item_Rarity == 0:
                item['name'] = item['name'] + " +1"
                return item
            else:
                add_affix(item, chosen_enchantment)
                return item
        case _ if chosen_rarity == "Rare":
            Item_Rarity = random.randint(0,1)
            if Item_Rarity == 0:
                item['name'] = item['name'] + " +2"                    
                return item
            if Item_Rarity == 1:
                add_affix(item, chosen_enchantment)
                item['name'] = item['name'] + " +1"
                return item
        case _ if chosen_rarity == "Legendary":
            Item_Rarity = random.randint(0,1)
            if Item_Rarity == 0:
                item['name'] = item['name'] + " +3"                    
                return item
            if Item_Rarity == 1:
                add_affix(item, chosen_enchantment)
                item['name'] = item['name'] + " +2"
                return item

def grab_spell_scroll(player_level):
    if os.name == 'nt':
        spell_db = os.path.dirname(__file__) + "\\dbs\\Spells.csv"
    if os.name == 'posix':
        spell_db = os.path.dirname(__file__) + "/dbs/Spells.csv"

    # will probably change this into a json file to be imported later instead.
    spell_weights_legend = get_player_loot_scheme(player_level=player_level, category="spell")
    
    valid_level = [r for r, w in spell_weights_legend['Weights'].items() if w > 0]
    valid_weights = [w for r, w in spell_weights_legend['Weights'].items() if w > 0]
    valid_amount = [a for a in spell_weights_legend['Amounts'].values() if int(a) > 0]

    # Pull randomized item weights for spell levels
    #spell_weights = [float(spell_type["Weight"]) for spell_type in spell_weights_legend]
    #spell_levels = [spell_type["Level"] for spell_type in spell_weights_legend]
    selected_spell_level = random.choices(valid_level, weights=valid_weights, k=1)[0]

    # Grab a random spell within the chosen spell level
    spells = read_csv(spell_db)
    spell_list = [spell for spell in spells if int(spell['level']) == int(selected_spell_level)]
    selected_spell = random.choice(spell_list)

    # Add the prefix "Scroll of"
    spell_scroll_name = "Scroll of " + selected_spell['name']
    selected_spell['name'] = spell_scroll_name

    # Add Scroll Mechanics in the description.
    scroll_description = "As an Action you can rip the scroll to cast the inscribed spell on this scroll regardless of the inscribed spell's cast time.\nAny class can cast the spell. If the spell requires a ability modifier or saving throw (8 + ability modifier), use the following ability modifier: WIS, CHA, INT. Once casted, the scroll embers away."
    selected_spell.update({"scroll_description": scroll_description})
    
    index = valid_level.index(selected_spell_level)
    spell_scroll_amount = valid_amount[index]
    selected_spell.update({"Amount": spell_scroll_amount})
    return selected_spell

def grab_consumable(player_level):
    #This function does not include spell scrolls despite both being a consumable.
    if os.name == 'nt':
        reward_db_location = os.path.dirname(__file__) + "\\dbs\\Reward_DB.csv"
    if os.name == 'posix':
        reward_db_location = os.path.dirname(__file__) + "/dbs/Reward_DB.csv"

    reward_db = read_csv(reward_db_location)

    # Get the player's loot scheme.
    loot_scheme = get_player_loot_scheme(player_level=player_level)
    valid_rarities   = [r for r, w in loot_scheme['Weights'].items() if w > 0]
    valid_weights    = [w for r, w in loot_scheme['Weights'].items() if w > 0]
    
    # Generate loot_pool based on character level.
    item_pool = []
    for item in reward_db:
        if item['Rarity'] in valid_rarities:
            match item['Rarity']:
                case "Common":
                    item['Rarity'] = valid_weights[0]
                case "Uncommon":
                    item['Rarity'] = valid_weights[1]
                case "Rare":
                    item['Rarity'] = valid_weights[2]
                case "Legendary":
                    item['Rarity'] = valid_weights[3]
            item_pool.append(item)

    reward_db = item_pool

    consumables = [item for item in reward_db if item['Category'] == "Consumable"]
    consumable_weight = [float(item["Rarity"]) for item in reward_db if item['Category'] == "Consumable"]
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

def generate_weapons(k=1,enchant=False, player_level=1):
    if os.name == 'nt':
        weapon_db = os.path.dirname(__file__) + "\\dbs\\Weapons.csv"
    if os.name == 'posix':
        weapon_db = os.path.dirname(__file__) + "/dbs/Weapons.csv"
    
    weapons = read_csv(weapon_db)

    if k == 1:
        selected_weapon = random.choice(weapons)
        if enchant == True:
            return enchant_item(selected_weapon, player_level=player_level)
        return selected_weapon
    
    weapons = random.sample(weapons, k=min(k, len(weapons)))
    list_of_loot = [] 
    for selected_weapon in weapons:
        if enchant == True: 
            enchanted = enchant_item(selected_weapon, player_level=player_level)
            list_of_loot.append(enchanted)
        else:
            list_of_loot.append(selected_weapon)
    return list_of_loot

def generate_armors(k=1,enchant=False, player_level=1):
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

    armors = random.sample(armors, k=min(k, len(armors)))
    list_of_loot = [] 
    for selected_armors in armors:
        if enchant == True: 
            list_of_loot.append(enchant_item(selected_armors, player_level=player_level))
        else:
            list_of_loot.append(selected_armors)
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
    # Grab the loot category
    ItemCategory_Weights = read_json(item_category_weights_location) 
    itemType = [lootType['Category'] for lootType in ItemCategory_Weights]
    item_Weights = [lootType['Weight'] for lootType in ItemCategory_Weights]
    generated_loot_types = random.choices(itemType, weights=item_Weights, k=k)

    # Get the player's loot scheme.
    loot_scheme = get_player_loot_scheme(player_level=player_level)
    valid_rarities   = [r for r, w in loot_scheme['Weights'].items() if w > 0]
    valid_weights    = [w for r, w in loot_scheme['Weights'].items() if w > 0]
    
    # Generate loot_pool based on character level.
    item_pool = []
    for item in reward_db:
        if item['Rarity'] in valid_rarities:
            match item['Rarity']:
                case "Common":
                    item['Rarity'] = valid_weights[0]
                case "Uncommon":
                    item['Rarity'] = valid_weights[1]
                case "Rare":
                    item['Rarity'] = valid_weights[2]
                case "Legendary":
                    item['Rarity'] = valid_weights[3]
            item_pool.append(item)

    #rename reward_db to the effective loot pool.
    reward_db = item_pool

    for loot_type in generated_loot_types:
        if loot_type == "Accessory":
            accessories = [item for item in reward_db if item['Category'] == "Accessory"]
            accessories_weights = [float(item['Rarity']) for item in accessories]
            accessory = random.choices(accessories, weights=accessories_weights, k=1)[0]
            list_of_loot.append(accessory)

        if loot_type == "Blessing":
            blessings = [item for item in reward_db if item['Category'] == "Blessing"]
            blessing_weights = [float(item['Rarity']) for item in blessings]
            blessing = random.choices(blessings, weights=blessing_weights, k=1)[0]
            list_of_loot.append(blessing)

        if loot_type == "Weapon":
            list_of_loot.append(generate_weapons(k=1, enchant=True, player_level=player_level))

        if loot_type == "Armor":
            list_of_loot.append(generate_armors(k=1, enchant=True, player_level=player_level))

        if loot_type == "Consumable":
            # Want to randomize between spell scrolls and consumables.
            # will probably change this into a json file to be imported later instead.
            consumable_type = [{"Category": "Consumable", "Weight": 0.7},{"Category": "Spells", "Weight": 0.6}]
            consumable_weight = [float(item_type["Weight"]) for item_type in consumable_type]
            consumable_type = [item_type["Category"] for item_type in consumable_type]
            item_type = random.choices(consumable_type, weights=consumable_weight)[0]
            if item_type == "Consumable":
                list_of_loot.append(grab_consumable(player_level))
            else:
                list_of_loot.append(grab_spell_scroll(player_level))
    return list_of_loot

def spacing(tuple_array, spacing = 2):
    str_count = [len(item[0]) for item in tuple_array if item != "New Line"]
    
    text_array = []
    for item in tuple_array:
        if item == "New Line":
            text_array.append("")
            continue
        if len(item) > 2:
            spacing = item[-1]
        max_spaces = max(str_count) + spacing
        text_array.append(f"{item[0]}".ljust(max_spaces) + "|  " + f"{item[1]}")
    return text_array

generated_loot = generate_loot(player_level=1)

print("---Generated Loot Names---")
print("```")
loot_tuple = []
for loot in generated_loot:
    loot_tuple.append((loot['name'], loot['Category'], 2))

printables = spacing(loot_tuple)
print("\n".join([line for line in printables]))
print("```")
print("------------------------------")
for loot in generated_loot:
    print("```")
    loot_tuple = []
    loot_tuple.append(("Name", loot['name']))
    if loot['Category'] == "Armor":
        loot_tuple.append(('Armor Type', loot['armor_type'], 2))
        loot_tuple.append(('AC', loot['AC'], 2))
        if "enchant_description" in loot:
            loot_tuple.append(("Enchantment", loot['enchant_description'], 2))
    
    if loot['Category'] == "Weapon":
        loot_tuple.append(('Weapon Type', loot['Weapon_Type'], 2))
        loot_tuple.append(('Properties', loot['Properties'],2))
        loot_tuple.append(('Damage', loot['Damage'], 2))
        if "enchantment_description" in loot:
            loot_tuple.append(("Enchantment", loot['enchant_description']), 2)
        loot_tuple.append(('Mastery', loot['Mastery'], 2))
        loot_tuple.append(('Mastery Description', loot['Mastery Definition'], 2))
    
    if loot['Category'] in ["Blessing", "Consumable", "Accessory"]:
        loot_tuple.append(("Item Type", loot['Category'], 2))
        if (loot["Amount"] != "") and (loot['Category'] != "Blessing"):
            loot_tuple.append(("Amount", loot['Amount'], 2))
        loot_tuple.append(("Effect", loot['Definition'], 2))
        
    if loot['Category'] == "spell":
        loot_tuple.append(("Item Type", "Consumable", 2))
        loot_tuple.append(('Level', loot['level'], 2))
        loot_tuple.append(("Amount", loot['Amount'], 2))
        loot_tuple.append(('Class', loot['classes'], 2))
        loot_tuple.append(("Cast Time", loot['cast_time'], 2))
        loot_tuple.append(("Range", loot['range'], 2))
        loot_tuple.append(("Duration", loot['duration'], 2))
        
        spell_cast_requirement = []
        if loot['verbal'] == 1:
            spell_cast_requirement.append("Verbal")
        if loot['somatic'] == 1:
            spell_cast_requirement.append("Somatic")
        
        loot_tuple.append(("Components", ",".join(spell_cast_requirement), 2))
        loot_tuple.append(('Scroll Effect', loot['scroll_description'], 2))
        loot_tuple.append("New Line")
        loot_tuple.append(("Effect", loot['description'], 2))

    printables = spacing(loot_tuple)
    print("\n".join([line for line in printables]))
    print("```")
    print()
print()