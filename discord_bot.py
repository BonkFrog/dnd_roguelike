# This example requires the 'message_content' intent.
import discord
from discord.ext import commands
import json
import os 
import logging

# How to get this.
# the on_ready asyc def, do bot.guilds
#guild_id = 

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, messages=True,guilds=True)

### DND Session List ###
party = []

def spacing(tuple_array):
    str_count = [len(item[0]) for item in tuple_array]
    
    text_array = []
    for item in tuple_array:
        spacing = item[-1]
        max_spaces = max(str_count) + spacing
        text_array.append(f"{item[0]}".ljust(max_spaces) + "|  " + f"{item[1]}")
    return "\n".join([choice for choice in text_array])


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
'''    
    # this is hardcoded to operate on my discord server.
    guild = bot.guilds[0]
    
    # load the cache
    await guild.chunk()

    list_of_members = ()
    members = guild.members
    for i, member in enumerate(members, 1):
        Current_Users = (i, member.name, member.nick, member.id)
        '''

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

# Create Party
# Whoever sends this command, becomes the DM.
player_list = []


class PartyPicker(discord.ui.View):
    def __init__(self, members):
        self.members = members
    
    @discord.ui.select(
        placeholder="Pick your party members."
        
    )
    self.add_item()

@bot.command()
async def set_party(ctx):
    author = ctx.author
    player_list.append({'status':'DM', 'user_id':author.id})
    
    # Enumerate Users
    guild = bot.guilds[0]
    await guild.chunk()
    members = guild.members
    list_of_users = []
    for i, member in enumerate(members, 1):
        Current_Users = (f"{i}: {member.name}", member.nick, 2)
        list_of_users.append(Current_Users)
    
    user_list = spacing(list_of_users)
    await ctx.send("```" + user_list + "```")

token_path = os.path.dirname(__file__) + '/token.json'
with open(token_path) as token:
    token = json.load(token)
    token = token['token']

# Logging
log_location = os.path.dirname(__file__) + 'logs/discord.log'
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

bot.run(token, log_handler=handler)
