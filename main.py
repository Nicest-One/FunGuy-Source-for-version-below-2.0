import discord
from discord.ext import commands
from discord.ext import tasks
import os
from replit import db
import random
import asyncio
import math
import datetime
import pytz
from item_dictionary_info import item_info_list
from quests_file_thing import all_quests_dict
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils import manage_components
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle, ContextMenuType
from discord_slash.utils.manage_components import create_select, create_select_option, ComponentContext
from discord_slash.context import MenuContext


prefix = "F!"

#rich presence below

total_users_use_funguy = len(db["totalplayers"])

activity_game = discord.Game(name=f"with {total_users_use_funguy} players! | F!help")

client = commands.Bot(command_prefix=prefix, help_command=None, activity=activity_game)

slash = SlashCommand(client, sync_commands=True)
#add back #sync_commands=True to above

#for later
#dbl_token = os.environ['dblsecret']
#db['RDB'] = {}
#RDB = db["RDB"]

#slash commands code begins
#see line 552 for "F!"

colors = [0x00ffff]

class cooldowns:
  def __init__(self):
    self.bucket = {}

  def add_cooldown(self, name, seconds, id):
    if name in self.bucket.keys():
      self.bucket[name][id] = seconds
    else:
      self.bucket[name] = {}
      self.bucket[name][id] = seconds

  def del_coodlown(self, name, id):
    try:
      self.bucket[name].pop(id)
    except:
      pass

  def clear_cooldown(self, name):
    self.bucket.pop(name)

  def modify_cooldown(self, name, change_in_seconds, id):
    try:
      self.bucket[name][id] += change_in_seconds
    except:
      return False

  def get_cooldown(self, name, id):
    try:
      return self.bucket[name][id]
    except:
      return 0

  def check_if_cooldown(self, name, id):
    try:
      if self.bucket[name][id] > 0:
        return True
    except:
      return False


Cooldowns = cooldowns()



@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))
  await manage_cooldowns.start()


@tasks.loop(seconds = 1)
async def manage_cooldowns():
  while True:
    await asyncio.sleep(1)
    
    for group in list(Cooldowns.bucket):
      for user in list(Cooldowns.bucket[group]):
        Cooldowns.bucket[group][user] -= 1
        if Cooldowns.bucket[group][user] < 1:
          Cooldowns.bucket[group].pop(user)

@slash.slash(name="vote", description="Help Support FunGuy! If you want to...", guild_ids=[871734308652593172, 801083422201479178])
async def slash_vote(ctx: SlashContext):
  temp_user = RDB[str(ctx.author.id)]['s']
  lv = temp_user[4][1]
  
  time_vote = datetime.datetime(lv[0], lv[1], lv[2], lv[3], lv[4], lv[5], lv[6])


  when_vote = time_vote + datetime.timedelta(hours=12)
  time_left = when_vote - datetime.datetime.now()

  tseconds = time_left.total_seconds()
  hours = tseconds // 3600
  minutes = (tseconds % 3600) // 60
  seconds = tseconds % 60
  if tseconds > 0:
    formater = ':timer: Vote Again In: '
    if hours > 1:
      formater += f'**{hours}** Hours, **{minutes}** Minutes'
    else:
      formater += f'**{minutes}** Minutes, **{seconds}** Seconds'
  else:
    formater = ':white_check_mark: You Are Ready To Vote!'


  em = discord.Embed(title='Vote For Rewards!', description=f"**Vote Status**\n{formater}\n**Rewards**\n`1` <:chest:936386255942475797> Chest", color=0xff00ff)
  await ctx.send(embeds=[em])



  

@slash.slash(name="use", description="Use a Item :)", guild_ids=[871734308652593172, 801083422201479178])
async def slash_craft(ctx: SlashContext):
  pass


@slash.slash(name="craft", description="Craft some cool items! Some might be useless but oh`well", guild_ids=[871734308652593172, 801083422201479178])
async def slash_craft(ctx: SlashContext):

  craft_menu = discord.Embed(title="Crafting Recipes", description=":stew: **Fish Soup**\n`On Crafting:`\n-1 :turtle: **Turtle**\n-2 :fish: **Blue Fish**\n+1 :stew: **Fish Soup**\n`Usage:`\n/use Fish Soup\n`On Usage:`\n+4 :heart: **Health**", color=0x964B00)

  
  buttons = [
    create_button(style=ButtonStyle.green, label="Craft: Fish Soup", custom_id='Craft'),   
]
  action_row = create_actionrow(*buttons)
  await ctx.send(embeds=[craft_menu], components=[action_row])

def random_damage(chance, data):
  if random.randint(0,100) < chance:
    my_hp = data[4][0]
    damage = random.randint(1, my_hp + 1)
    if damage == my_hp:
      return damage, True
    else:
      return damage, False #did not leave player to 0 hp
    
  else:
    return False

@slash.slash(name="help", description="Help Needed? Don't worry!", guild_ids=[871734308652593172, 801083422201479178])
async def slash_help(ctx: SlashContext):
  all_embeds = {'a':discord.Embed(title='***:information_source: FunGuy Info***', description="**FunGuy is a rich economy discord bot with tons of commands so you won't get bored!**\n\nMaintainers:\n```\nNice One#1736 - Developer\nSpekie#0752 - Server Manager / Ideator\n```\nSupport Server: https://discord.gg/WByYtSKJQe", color=0xff00ff), 'b':discord.Embed(title='***<:slash_icon:924813729340735578>*** /start', description="Use this command before any other!\nUsage: **/start**\nOptions: **None**", color=0xff00ff), 'c':discord.Embed(title='***<:slash_icon:924813729340735578>*** /inventory', description="You can use this command to see your inventory, as well as throw unwanted items!\nUsage: **/inventory**\nOptions: **None**", color=0xff00ff), 'd':discord.Embed(title='***<:slash_icon:924813729340735578>*** /gather', description="Collect Some Items :) Fast and Easy!\nUsage: **/gather**\nOptions: **None**", color=0xff00ff)}
  
  
  


  select = create_select(
    options=[
        create_select_option("FunGuy Info", value="a", emoji="ℹ️"),
        create_select_option("/start", value="b", emoji="🇨"),
        create_select_option("/inventory", value="c", emoji="🇨"),
        create_select_option("/gather", value="d", emoji="🇨")
    ],
    placeholder="Choose A Catagory To get help about!",
    min_values=1,
    max_values=1
)
  
  dead_menu = create_select(
    options = [
      create_select_option("FunGuy Info", value="a", emoji="🗺️")
    ],
    disabled=True,
    placeholder="Choose A Catagory To get help about!"
  )

  action_row = create_actionrow(select)
  disabled = create_actionrow(dead_menu)

  main = await ctx.send(embeds=[all_embeds['a']], components=[action_row])
  
  

  try:
    await asyncio.wait_for(setup_help(action_row, all_embeds), timeout=180.0)
  except asyncio.TimeoutError:
    await main.edit(components=[disabled])

async def setup_help(action_row, help_list):
  
  while True:
    button_ctx: ComponentContext = await manage_components.wait_for_component(client, components=action_row)
    
    await button_ctx.edit_origin(embeds=[help_list[button_ctx.selected_options[0]]])




@slash.slash(name="gather", description="The most efficient way to get materials!", guild_ids=[871734308652593172, 801083422201479178])
async def slash_gather(ctx: SlashContext):
  if not await check_account(ctx.author.id):
    have_acc = discord.Embed(title=':x: Uhh Oh!', description="You have not started your adventure!\nType: `/start`", color=0xff0000)
    await ctx.send(embeds=[have_acc])
    return


  temp_user = RDB[str(ctx.author.id)]['s']
  print(temp_user)
  tf = temp_user[0]
  tm = temp_user[1]
  tc = temp_user[2]
  td = temp_user[3]
  #.format - level, cooldown, luck, amount of items, points, xp

  await check_account(ctx.author.id)

  gather_embed = discord.Embed(title=f"{ctx.author.name}'s Resource Gathering!", description="click on a button below to perform that action and get materials:", color=0x964B00)
  gather_embed.add_field(name=":fishing_pole_and_fish: Fishing!", value=f"Provides: :fish: | :tropical_fish: | :turtle:\nTool Stats: :timer: `{tf[1]}`m | :medal: `{tf[2]}`% | :part_alternation_mark: `{tf[3]}`\nLevel 1: <:leb:924770012554727474><:meb:924770052518060042><:meb:924770052518060042><:reb:924770034721636442> `{tf[5]}`/10", inline=False)

  gather_embed.add_field(name=":pick: Mining!", value=f"Provides: :knot: | :coin: | :gem:\nTool Stats: :timer: `{tm[1]}`m | :medal: `{tm[2]}` | :part_alternation_mark: `{tm[3]}`\nLevel 1: <:leb:924770012554727474><:meb:924770052518060042><:meb:924770052518060042><:reb:924770034721636442> `{tm[5]}`/10", inline=False)

  gather_embed.add_field(name=":axe: Chopping!", value=f"Provides: :wood: | :four_leaf_clover: | :apple:\nTool Stats: :timer: `{tc[1]}`m | :medal: `{tc[2]}`% | :part_alternation_mark: `{tc[3]}`\nLevel 1: <:leb:924770012554727474><:meb:924770052518060042><:meb:924770052518060042><:reb:924770034721636442> `{tc[5]}`/10", inline=False)

  gather_embed.add_field(name=":hook: Digging!", value=f"Provides: :oil: | <:dirt:925204439978106950> | <:clay:925206473838055475>\nTool Stats: :timer: `{td[1]}`m | :medal: `{td[2]}`% | :part_alternation_mark: `{td[3]}`\nLevel 1: <:leb:924770012554727474><:meb:924770052518060042><:meb:924770052518060042><:reb:924770034721636442> `{td[5]}`/10", inline=False)

  buttons = [
    create_button(style=ButtonStyle.green, label="Fish", custom_id='Fish'),
    create_button(style=ButtonStyle.green, label="Mine", custom_id='Mine'),
    create_button(style=ButtonStyle.green, label="Chop", custom_id='Chop'),
    create_button(style=ButtonStyle.green, label="Dig", custom_id='Dig')
]
  dead_menu = [
    create_button(style=ButtonStyle.green, label="Fish", disabled=True),
    create_button(style=ButtonStyle.green, label="Mine", disabled=True),
    create_button(style=ButtonStyle.green, label="Chop", disabled=True),
    create_button(style=ButtonStyle.green, label="Dig", disabled=True)
]


  action_row = create_actionrow(*buttons)
  disabled = create_actionrow(*dead_menu)

  main = await ctx.send(embeds=[gather_embed], components=[action_row])

  try:
    await asyncio.wait_for(setup_gather(action_row, ctx), timeout=60.0)
  except asyncio.TimeoutError:
    await main.edit(components=[disabled])



async def setup_gather(action_row, ctx):
  buttons = [
    create_button(style=ButtonStyle.blue, emoji='⏱️', custom_id='a'),
    create_button(style=ButtonStyle.blue, emoji='🏅', custom_id='b'),
    create_button(style=ButtonStyle.blue, emoji='〽️', custom_id='c'),
    create_button(style=ButtonStyle.green, emoji='📦', custom_id='d', disabled=True)
]
  upgrade_row = create_actionrow(*buttons)


  while True:
    button_ctx: ComponentContext = await manage_components.wait_for_component(client, components=action_row)

    item_drops = {'Fish':[':fish: **Blue Fish**', ':tropical_fish: **Large Tropical Fish**', ':turtle: **Turtle**'], 'Mine':[':knot: **Iron**', ':coin: **Gold**', ':gem: **Diamond**'], 'Chop':[':wood: **Wood**', ':four_leaf_clover: **Leaf**', ':apple: **Apple**'],'Dig':[':oil: **Fossil Fuel**', '<:dirt:925204439978106950> **Dirt**', '<:clay:925206473838055475> **Clay**']}

    assets = {'Fish':':fishing_pole_and_fish: | Fishing Results!', 'Mine':':pick: | Mining Results!', 'Chop':':axe: | Chopping Results!', 'Dig':':hook: | Digging Results!'}


    
    index_of_cmd = {'Fish':0, 'Mine':1, 'Chop':2, 'Dig':3}
    index_adder = {'Fish':0, 'Mine':3, 'Chop':6, 'Dig':9}

    if Cooldowns.check_if_cooldown(button_ctx.custom_id, ctx.author.id):
        await button_ctx.reply(content="You are on cooldown")


    else:
      Cooldowns.add_cooldown(button_ctx.custom_id, 50*5, ctx.author.id)
      
      

      item_got = random.choice(item_drops[button_ctx.custom_id])
      
      index_m = item_drops[button_ctx.custom_id].index(item_got)
      
      item_index = index_m + index_adder[button_ctx.custom_id]
      print(item_index)

      await give_item(str(ctx.author.id), item_index, 1)

      RDB[str(ctx.author.id)]['s'][index_of_cmd[button_ctx.custom_id]][5] += 1
      db["RDB"] = RDB

      r_embed = discord.Embed(title=assets[button_ctx.custom_id], description=f"**Updated Attributes**\n`+1` {item_got}\n`5` minute cooldown", color=0x0000ff)
      
      if RDB[str(ctx.author.id)]['s'][index_of_cmd[button_ctx.custom_id]][5] == 10:
        r_embed.add_field(name=':arrow_up: Tool Upgraded!', value="Congratulations your tool is now level `2`! Please Select A upgrade for your tool:\n:timer: -1 minute cooldown\n:medal: +20% chance to get better items\n:part_alternation_mark: +1 item drops\n:package: Save Upgrade Point (WIP)")
        
        
        msg = await button_ctx.reply(embeds=[r_embed], components=[upgrade_row])

      else:

        msg = await button_ctx.reply(embeds=[r_embed])
      
      
      

      








def get_contents_seperated(data, names):
  display = ""
  
  index = 0
  for i in data:
    if i > 0:
      display += f"`{i}` **{names[index]}** | Index: {index}\n"
    index += 1
  display += f'Data: {data}'
  return display 



@slash.slash(name="inventory", description="See and Sell the items you have!", guild_ids=[871734308652593172, 801083422201479178])
async def slash_inventory(ctx: SlashContext):
  if not await check_account(ctx.author.id):
    have_acc = discord.Embed(title=':x: Uhh Oh!', description="You have not started your adventure!\nType: `/start`", color=0xff0000)
    await ctx.send(embeds=[have_acc])
    return

  hp = RDB[str(ctx.author.id)]['s'][4][0]
  empty = [':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:', ':black_large_square:']
  index = 0
  for i in range(0, hp):
    empty[index] = ':red_square:'
    index += 1

  hp_display = ""
  for i in empty:
    hp_display += i

  
  profile_em = discord.Embed(title=f'{ctx.author} Inventory', description=f"Health: {hp_display} | `{hp}`/`5`", color=0xff0000)


  inv = discord.Embed(title=f"{ctx.author.name}'s Inventory", description="**Your Items:**")
  user = ctx.author.id


  index_finder = {0:':fish: Blue Fish', 1:':tropical_fish: Large Tropical Fish', 2:':turtle: Turtle', 3:':knot: Iron', 4:':coin: Gold', 5:':gem: Diamond', 6:':wood: Wood', 7:':four_leaf_clover: Leaf', 8:':apple: Apple', 9:':oil: Fossil Fuel', 10:'<:dirt:925204439978106950> Dirt', 11:'<:clay:925206473838055475> Clay', 12:'<:chest:936386255942475797> Chest'}
  temp_inv = RDB[str(user)]['i']
  
  inv = get_contents_seperated(temp_inv, index_finder)
 
  display = discord.Embed(description=inv, color=ctx.author.color)
 
  await ctx.send(embeds=[profile_em, display])
 
  buttons = [
    create_button(style=ButtonStyle.blue, label="Inventory"),
    create_button(style=ButtonStyle.blue, label="Recycle Bin")
]

  

  action_row = create_actionrow(*buttons)

















@slash.slash(name="start", description="A adventure awaits!", guild_ids=[871734308652593172, 801083422201479178])
async def slash_start(ctx: SlashContext):
  if await check_account(ctx.author.id):
    have_acc = discord.Embed(title=':x: Uhh Oh!', description="You have already started your adventure!", color=0xff0000)
    await ctx.send(embeds=[have_acc])
    return
  await create_account(ctx.author.id)

  p = ctx.author.name
  buttons_next = [
    create_button(style=ButtonStyle.blue, label="Next", custom_id='next', emoji='➡️'),
  ]
  buttons_done = [
    create_button(style=ButtonStyle.green, label="Done", custom_id='done', emoji='✅'),
  ]

  start1 = discord.Embed(title='The Start?', color=ctx.author.color)
  start1.add_field(name="Storyline 1/4", value=f"{p}: *Wakes Up*\n{p}: where... where, am I?\n{p}: Why is the whole world pixelated?\n{p}: This is not how I remember it...")
  start1.set_image(url="https://cdn.discordapp.com/attachments/868503928357154847/933121697794646056/funguy-story-1.png")
  
  start2 = discord.Embed(title='The Start?', color=ctx.author.color)
  start2.add_field(name="Storyline 2/4", value=f"{p}: *Walks outside*\n{p}: *hears a meeting going on in the townhall and walks inside*\nFunGuy: Our world is under a curse from The Bug!\nFunGuy: We will need one brave adventurer to save us.")
  start2.set_image(url="https://cdn.discordapp.com/attachments/868503928357154847/933124315312967770/funguy-story-2.png")
  
  start3 = discord.Embed(title='The Start?', color=ctx.author.color)
  start3.add_field(name="Storyline 3/4", value=f"{p}: *says softley*: I will be the one...")
  start3.set_image(url="https://cdn.discordapp.com/attachments/868503928357154847/933133960605745212/funguy-story-3.png")
  
  start4 = discord.Embed(title='The Start?', color=ctx.author.color)
  start4.add_field(name="Storyline 4/4", value=f"*Along the way you find out that you are not just the only one...*")
  start4.set_image(url="https://cdn.discordapp.com/attachments/868503928357154847/933137686376640603/funguy-story-4.png")

  end_embed = discord.Embed(title='The Start?', color=ctx.author.color)
  end_embed.add_field(name="A startoff kit!", value=f"1 :fishing_pole_and_fish: Fishing Pole\n1 :pick: Pickaxe\n1 :axe: Axe\n1 :hook: Digging Hook\n5 <:AdventureTokens:924787621358608445> Tokens")
  
  action_row = create_actionrow(*buttons_next)
  done_row = create_actionrow(*buttons_done)

  
  await ctx.send(embeds=[start1], components=[action_row])
  
  button_ctx: ComponentContext = await manage_components.wait_for_component(client, components=action_row)
  await button_ctx.edit_origin(embeds=[start2], components=[action_row])

  button_ctx: ComponentContext = await manage_components.wait_for_component(client, components=action_row)
  await button_ctx.edit_origin(embeds=[start3], components=[action_row])

  button_ctx: ComponentContext = await manage_components.wait_for_component(client, components=action_row)
  await button_ctx.edit_origin(embeds=[start4], components=[done_row])

  button_ctx: ComponentContext = await manage_components.wait_for_component(client, components=done_row)
  await button_ctx.edit_origin(embeds=[end_embed], components=[])
  

async def create_account(user):
  d_est = datetime.datetime.now()

  RDB[str(user)] = {'i':[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], 's':[[1, 5, 0, 1, 0, 0], [1, 5, 0, 1, 0, 0], [1, 5, 0, 1, 0, 0], [1, 5, 0, 1, 0, 0], [5, [d_est.year, d_est.month, d_est.day, d_est.hour, d_est.minute, d_est.second, d_est.microsecond], 15000, 15000], ['', 0]]}
  db["RDB"] = RDB

async def give_item(user, item, amount):
  RDB[user]['i'][item] += amount

  db["RDB"] = RDB


async def check_account(user):
  if str(user) not in RDB:
    return False
  else:
    return True

async def process_vote(uid):
  await give_item(uid, 12, 1)
  d_est = datetime.datetime.now()
  RDB[uid]['s'][4][1] = [d_est.year, d_est.month, d_est.day, d_est.hour, d_est.minute, d_est.second, d_est.microsecond]
  db["RDB"] = RDB


  
#db['RDB'] = {}
RDB = db["RDB"]

"""
d_est = datetime.datetime.now()
for i in list(RDB.keys()):

  RDB[str(i)]['s'][4] = [5, [d_est.year, d_est.month, d_est.day, d_est.hour, d_est.minute, d_est.second, d_est.microsecond], 15000, 15000]
"""
"""
for i in list(RDB.keys()):
  RDB[str(i)]['s'].append(['', 0])
db["RDB"] = RDB
"""
#print(db['RDB'])

@slash.slash(name="API", description="Are YOU a Developer? Use our Application Programming Interface!", guild_ids=[871734308652593172, 801083422201479178])
async def slash_api(ctx: SlashContext):
  embed = discord.Embed(title="<:APIKEY:946488112522100817> API", description="", color=0x429bb8)
  await ctx.send(embed=embed)

























































#
#
#
#ABOVE (FUNGUY "/" COMMANDS)
#############################
#BELOW (FUNGUY "F!" COMMANDS)
#
#
#













@client.command()
async def rdb(ctx):
  await ctx.send(db["RDB"])





















@client.command()
@commands.cooldown(1, 60 * 3, commands.BucketType.user)
async def fish(ctx):

  tempid = ctx.author.id

  if tempid in players:

    gametag = players.index(tempid)
    

    if peoplecharacters[gametag][0] == "Fish" and peoplecharacters[gametag][2] != "claimed":
      
      peoplecharacters[gametag][2] += 1
      db["charactersofall"] = peoplecharacters

    

    userid = ctx.author.id
    username = ctx.author
    useravatar = ctx.author.avatar_url

    e1 = ":black_large_square:"
    e2 = ":blue_square:"

    fishbar = [e1, e1, e1]

    embedVar = discord.Embed(title="<:fishing_pole:808352721275060314> | Fishing Game", description="React with [:fishing_pole_and_fish:] to cast your rod.\nAfter casting your rod react with the corresponding arrow emote to the word displayed.\nWhen the fish bar is full you are done!", color=0x0000ff)

    embedVar.add_field(name="Fish bar", value=f"{fishbar[0]}{fishbar[1]}{fishbar[2]}", inline=False)
    
    embedVar.set_footer(icon_url=useravatar, text=f"{username}, Is fishing")
    msg = await ctx.send(embed=embedVar)

    await msg.add_reaction('⬅️')
    await msg.add_reaction('➡️')
    await msg.add_reaction('🔼')
    await msg.add_reaction('🔽')
    await msg.add_reaction('🎣')

    pmovements = ["left", "right", "up", "down"]
    rmovements = ['⬅️', '➡️', '🔼', '🔽', '🎣']

    imovements = [4]
    imovements.append(random.randint(0, 3))
    imovements.append(random.randint(0, 3))
    imovements.append(random.randint(0, 3))
    imovements.append(random.randint(0, 3))

    counter = 0

    done = False
      
    while not done:
      try:
        reaction, user = await client.wait_for('reaction_add', timeout=20.0)
      except asyncio.TimeoutError:
        embedVar = discord.Embed(title="OH NOO!", description=f"The fish swam away, {username}!", color=0xff0000)
        await msg.edit(embed=embedVar)
        done = True
      else:
        if str(reaction.emoji) == rmovements[
          imovements[counter]] and user.id == userid:
          await msg.remove_reaction(str(reaction.emoji), user)
          if counter != 0:
            fishbar[counter - 1] = e2

          counter += 1
          wmovement = pmovements[imovements[counter]]

          embedVar = discord.Embed(title="<:fishing_pole:808352721275060314> | Fishing Game", description=f":fish: **|** The fish is currently moving {wmovement}!", color=0x0000ff)

          embedVar.add_field(name="Fish bar", value=f"{fishbar[0]}{fishbar[1]}{fishbar[2]}", inline=False)
    
          embedVar.set_footer(icon_url=useravatar, text=f"{username}, Is fishing")


          await msg.edit(embed=embedVar)
            
          if counter > 3:
            await msg.clear_reactions()
            done = True
            itemsnames = ["<:common_fish:806986714627178496> commonfish", "<:rare_fish:806986792184184853> rarefish", "<:epic_fish:806986882449145888> epicfish", "<:water_bottle:839580961191493634> waterbottle", "<:lily_pad:839564075347869787> lilypad", "<:rock:821101496531681338> rock", "<:iron:821101561157386262> iron", "<:copper:821101604961779712> copper", "bronze", "<:wood_stick:825030799026814997> stick", "<:wood_log:825030291838992504> log", "<:leaf:839564127408095253> leaf", "<:red_apple:839564590949466172> apple", "<:banana:839581019120336987> banana", "<:ruby:839564178637324329> ruby", "<:diamond:839564238099054623> diamond", "sil chest", "golden chest", "po 1", "po 2", "potion 3 (po = potion)", "pres chest", "<:fertilizer:865256293334122506> fertilizer","<:dirt_pile:873278535559692298> dirt","<:sand_pile:873278153978679297> sand","<:gravel_pile:873278030246719499> gravel"]
            loot_draws = [[0, 5],[1, 4],[2, 3],[3, 2],[4, 1],[5, 0],[6, 0],[7, 0],[9, 0],[10, 0],[11, 0],[12, 0],[13, 0],[14, 0],[15, 0],[22, 0],[23, 0],[24, 0],[25, 0]]
            loot = get_loot(loot_draws, 'dig')
        
            loot_string = ""
            for i in loot:
              loot_string = loot_string + f"+{i[0]} {itemsnames[i[1]]}\n"
              iteminventorys[gametag][i[1]] += i[0]
  
            db["itemsofall"] = iteminventorys

            embedVar = discord.Embed(title="You are done fishing!", description=f"User: {ctx.author}", color=0x0000ff)
            embedVar.add_field(name="You Got:", value=f"{loot_string}", inline=False)
            
            
            
            
            
            #prestige and chest drops
            
            extra_got = []

            randomnumi = random.randint(0,99)
            randomnumin = random.randint(0,99)
            
            chest_chance = 25
            xpt = peoplecharacters[players.index(ctx.author.id)][22]
            there_level = math.floor(xpt / 3)
            if there_level >= 1:
              chest_chance = 30
            
            if randomnumi < 25:
              peoplecharacters[gametag][13] += 1
              db["charactersofall"] = peoplecharacters
              extra_got.append("+1 :low_brightness: prestige point")
            if randomnumin < chest_chance:
              iteminventorys[gametag][8] += 1
              db["itemsofall"] = iteminventorys
              extra_got.append("+1 <:bronze_chest_closed:835618525250060388> Bronze Chest")
              
            if len(extra_got) > 0:
              lineyay = ""
              for i in extra_got:
                lineyay = lineyay + i + "\n"
              embedVar.add_field(name="Extra", value=f"{lineyay}", inline=False)
            
            await msg.edit(embed=embedVar)
            
            chance = 5
            if random.randint(0,100) < chance:
              #spawn airdrop
              embedVar = discord.Embed(title="<a:airdrop_emoji:879392658508902410> | Airdrop", description="react with :toolbox: to claim airdrop")
    
              msg = await ctx.send(embed=embedVar)

              await msg.add_reaction('🧰')
              await asyncio.sleep(0.1)
              try:
                reaction, user = await client.wait_for('reaction_add', timeout=50.0)
              except asyncio.TimeoutError:
                embedVar = discord.Embed(title=":negative_squared_cross_mark: |Airdrop", description=f"Noone claimed the airdrop!")
                await msg.edit(embed=embedVar)
              else:
                reaction = str(reaction.emoji)
              if reaction == '🧰':
                embedVar = discord.Embed(title=":white_check_mark: |Airdrop", description=f"{user} has claimed the airdrop!")
                await msg.edit(embed=embedVar)
                await msg.clear_reactions()

                gametag = players.index(user.id)
                peoplecharacters[gametag][25][0] += 1
                db["charactersofall"] = peoplecharacters

        elif str(reaction.emoji) != rmovements[imovements[counter]] and user.id == userid:
          embedVar = discord.Embed(title="OH NOO!", description=f"The fish swam away due to your wrong movement, {username}!", color=0xff0000)
          await msg.edit(embed=embedVar)
          done = True
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@fish.error
async def fish_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    timeleft = math.ceil(error.retry_after / 60)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"looks like your on a cooldown for {timeleft} minutes!\n**User: {ctx.author}**", color=0xff0000)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
  else:
    raise error


























@client.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    #return
    
  
    embedVar = discord.Embed(title=":jack_o_lantern: Evil Pumpkin: OH NOO!", description="looks like I could not find the command you typed!", color=0xff0000)
    await ctx.send(embed=embedVar)
  raise error



@client.event
async def on_message(message):
  if message.channel.id == 867106352357572619:
    msg = message.content.split()

    userid = int(msg[4])

    await process_vote(str(userid))
  
  await client.process_commands(message)








  try:
    ctx = await client.get_context(message)
    normal_text = message.content.split('F!')[1].lower()
    command = client.get_command(message.content.split('F!')[1])
    cbase = {'fish':180.0, 'mine':600.0, 'daily':86400.0, 'train':5400, 'hourly':3600.0, 'dig':900.0}


    cooldown = command.get_cooldown_retry_after(ctx)

    if cbase[normal_text] == cooldown:
      gametag = players.index(message.author.id)
      quest_progress = peoplecharacters[gametag][-1]
      current_quest = all_quests_dict[str(quest_progress[1])]

      
      if current_quest['action'] == normal_text.lower():
        peoplecharacters[gametag][-1][0] += 1
        db["charactersofall"] = peoplecharacters

        
  except:
    pass

@client.command()
async def leave(ctx, id:int):
  toleave = client.get_guild(id)

  channel = toleave.system_channel
  await channel.send("Leaving this server due to inactity! You can invite me back with: https://discord.com/api/oauth2/authorize?client_id=801083957168570388&permissions=2147871808&scope=bot%20applications.commands")
  await toleave.leave()
  


@client.command()
async def te(ctx):
  t = [guild.name for guild in client.guilds]
  t1 = [guild.member_count for guild in client.guilds]
  t2 = [guild.id for guild in client.guilds]
  strings = []
  string = ""
  count = 0
  for i in range(0, len(t)):
    string += f'{t[i]} | {t1[i]} member | ID: {t2[i]}\n'
    count += 1
    if count > 10:
      strings.append(string)
      string = "" 
      count = 0

  embed = discord.Embed(title="Servers")
  for i in strings:
    embed.add_field(name="Servers", value=i)
    

  await ctx.send(embed=embed)
  
  

@client.command()
async def task(ctx, earg=None):
  gametag = players.index(ctx.author.id)
  quest_progress = peoplecharacters[gametag][-1]
  #1 = current quest, 0 = current quest progression
  

  try:
    current_quest = all_quests_dict[str(quest_progress[1])]
    con = True
  except KeyError:
    embedVar = discord.Embed(title="Tasks Progression", description=f"You Have completed every single task!!! :tada:", color=ctx.author.color)
    await ctx.send(embed=embedVar)
    con = False





  if con and earg == None:
  
    emojis = ['<:grey_side:907768968117366845>', '<:green_side:907768920688193546>']
    e_string = [emojis[1], emojis[1], emojis[1]]

    current_reward = math.floor(quest_progress[1] / 3)
    to_reward = peoplecharacters[gametag][-1][1] - (current_reward * 3)

  
    for i in range(0, 3 - to_reward):
      e_string[2- i] = emojis[0]



    embedVar = discord.Embed(title="Tasks Progression", description=f"{e_string[0]} :clipboard: Current Task: `{current_quest['action']}, {current_quest['times']} times`\n{e_string[1]} :chart_with_upwards_trend: My Progression: `{quest_progress[0]}/{current_quest['times']}`\n{e_string[2]} :bulb: Tip: `{current_quest['tip']}`", color=ctx.author.color)
    
    if current_quest['times'] <= quest_progress[0]:
      embedVar.add_field(name="YAY!", value='You completed this task, type `F!task new` to get a new task!')

    await ctx.send(embed=embedVar)
  elif earg.lower() == 'new' and con:
    if current_quest['times'] <= quest_progress[0]:
      embedVar = discord.Embed(title="Tasks Progression", description=f"You now have a new task", color=ctx.author.color)
      await ctx.send(embed=embedVar)
      peoplecharacters[gametag][-1][1] += 1
      peoplecharacters[gametag][-1][0] = 0
      db["charactersofall"] = peoplecharacters
    else:
      embedVar = discord.Embed(title="Tasks Progression", description=f"You must complete the current task inorder to get a new one", color=ctx.author.color)
      await ctx.send(embed=embedVar)

@client.command()
async def start(ctx):
  tempid = ctx.author.id

  if tempid in players:
   embedVar = discord.Embed(title="OH NOO!", description="looks like you already have a account", color=0xff0000)
   await ctx.send(embed=embedVar)
  
  else:

    embedVar = discord.Embed(title="YAY!", description="You can now use other commands", color=0x00ff00)
    await ctx.send(embed=embedVar)
		
    players.append(ctx.author.id)
    db["totalplayers"] = players
		
    moneybags.append(15)
    db["moneybagsofall"] = moneybags
		
    iteminventorys.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    db["itemsofall"] = iteminventorys
		
    peoplecharacters.append(["none", 0, 0, 0, 0, 0, 3, 1, 4, 45, 1, [1], 0, 0, 0, 0, [0], 0, [0], [0], 0, 0, 0, [0, 0], [1, 1], [0, 0, 0, 0], 0, 0, [0, 1]])
    db["charactersofall"] = peoplecharacters

@client.command()
async def spawnboost(ctx):
  cha_boosters[0] = 0

  random_b = random.randint(0, 50)

  
  cha_boosters[1][1] = random_b

  embedVar = discord.Embed(title=':detective: | Trade NPC', description=f'The Trade NPC Dropped A Mysterious Potion!\nEffects: +{random_b}% coins from selling\nType **F!boost** to drink the potion\nYou will also get 250 candy :candy:')
  channel = client.get_channel(885518165289885788)
  await channel.send(embed=embedVar)
  
  
  db["booster_data"] = cha_boosters



@client.command()
async def boost(ctx):
  if ctx.channel.id == 885518165289885788:
    if cha_boosters[0] == 0:
      gametag = players.index(ctx.author.id)
      await ctx.send(f':dizzy_face: | You drank the potion, effects: +{cha_boosters[1][1]}% coins from selling')
      cha_boosters[0] = ctx.author.id
      db["booster_data"] = cha_boosters
      peoplecharacters[gametag][25][3] += 250
      db["charactersofall"] = peoplecharacters

    else:
      await ctx.send('boost already claimed!')

@client.command()
async def api(ctx):
  api_reactions = ['1️⃣', None, None]
  a_emoji = [':one:', ':lock:', ':lock:']
  gametag = players.index(ctx.author.id)
  if peoplecharacters[gametag][27] != 0:
    api_reactions[0] = None
    api_reactions[1] = '2️⃣'
    a_emoji[0] = ':lock:'
    a_emoji[1] = ':two:'

  embedVar = discord.Embed(title='<a:yellow_test:884417251237847070> | API KEY', description=f"**Select a option**\n{a_emoji[0]} Create API key\n{a_emoji[1]} View your Api key\n{a_emoji[2]} Api documentation", color=0xe79005)

  msg = await ctx.send(embed=embedVar)

  for i in api_reactions:
    if i != None:
      await msg.add_reaction(i)

  done = False
  starting = False
  while not done:
    try:
      reaction, user = await client.wait_for('reaction_add', timeout=20.0) 
    except asyncio.TimeoutError:
      embedVar = discord.Embed(title='<a:yellow_test:884417251237847070> | API KEY', description="Timed Out", color=0xe79005)
      await msg.edit(embed=embedVar)
      await msg.clear_reactions()
      done = True
    else:
      if user.id == ctx.author.id:
        react = str(reaction.emoji)
        if react == '1️⃣':
          await msg.clear_reactions()

          embedVar = discord.Embed(title='<a:yellow_test:884417251237847070> | API KEY', description='**Are you sure** you want to create a API key? This action is irreversible!\nReact with :white_check_mark: to procced, otherwise react with :x: to cancel', color=0xe79005)

          await msg.edit(embed=embedVar)
          await msg.add_reaction('✅')
          await msg.add_reaction('❌')
          starting = True
        if react == '✅' and starting == True:
          
          await msg.clear_reactions()

          embedVar = discord.Embed(title='<a:yellow_test:884417251237847070> | API KEY', description='Api Key Created!\nYour api key has been sent via dms', color=0xe79005)

          api_k = random.randint(100001, 999999)
          peoplecharacters[gametag][27] = api_k
          db["charactersofall"] = peoplecharacters
          
          await user.send(f'Your api key is: {api_k}')
          await msg.edit(embed=embedVar)
          done = True
        if react == '❌' and starting == True:
          
          await msg.clear_reactions()

          embedVar = discord.Embed(title='<a:yellow_test:884417251237847070> | API KEY', description='Api Key Creation Cancelled!', color=0xe79005)

          await msg.edit(embed=embedVar)
          done = True
        if react == '2️⃣':
          await msg.clear_reactions()
          embedVar = discord.Embed(title='<a:yellow_test:884417251237847070> | API KEY', description='Api Key has been sent via dms', color=0xe79005)

          await msg.edit(embed=embedVar)
          

          api_k = peoplecharacters[gametag][27]
          
          await user.send(f'Your api key is: {api_k}')
          done = True

@client.command(aliases=['t'])
async def tribe(ctx, action1 = None, action2 = None):


  gametag = players.index(ctx.author.id)
  if action1 == 'create':
    if peoplecharacters[gametag][26] != 0:
      embedVar = discord.Embed(title="OH NOO", description="You already own or are in a tribe!")
      await ctx.send(embed=embedVar)
      return
    
    embedVar = discord.Embed(title="Creating a tribe (step 1/1),", description="Please type your tribe name")
    #embedVar.set_footer(text='You can highly customize your tribe later with F!tribe settings')
    msg = await ctx.send(embed=embedVar)
    done = False
    while not done:
      try:
        response = await client.wait_for('message', timeout=60.0)
      except asyncio.TimeoutError:
        embedVar = discord.Embed(title="Creating a tribe (step 1/1)", description="tribe creation cancelled due to timeout")
        await msg.edit(embed=embedVar)
        done = True
      else:
        if response.author.id == ctx.author.id:
          done = True
          

          tribe_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

          num1 = random.randint(0,9)
          num2 = random.randint(0,9)
          char = random.choice(tribe_letters)
          tag = str(num1) + char + str(num2)

          clans_list.append([response.content, [['owner', '11111'], ['member', '00000']], [[gametag, 0]], [':flags:', tag]])
          
          embedVar = discord.Embed(title="Creating a tribe (step 1/1)", description="created tribe!")
          
          await msg.edit(embed=embedVar)

          peoplecharacters[gametag][26] = len(clans_list)
          db["charactersofall"] = peoplecharacters
          db["clans"] = clans_list
  




  if action1 == 'list':
    empty_list = []
    for i in clans_list:
      empty_list.append([i[0], len(i[2]),  i[3][0], i[3][1]])
    
    embedVar = discord.Embed(title=f"showing all {len(empty_list)} Tribes", description=f'Join a tribe with F!tribe join <tag>')
    for i in empty_list:
      embedVar.add_field(name=f"{i[2]} {i[0]}", value=f"Members: {i[1]}/10\nTag: {i[3]}")


    await ctx.send(embed=embedVar)







  if action1 == None:
    if peoplecharacters[gametag][26] != 0:
      clan_id = peoplecharacters[gametag][26] - 1
      clan_data = clans_list[clan_id]

      embedVar = discord.Embed(title=f"{clan_data[3][0]} {clan_data[0]}", description=f"Members: {len(clan_data[2])}/10\nTag: {clan_data[3][1]}", color=0x37b887)

      await ctx.send(embed=embedVar)

    else:
      await ctx.send('you are not in a tribe yet, type F!tribe list to join one.')
  





  if action1 == 'join' and action2 != None:
    if peoplecharacters[gametag][26] != 0:
      await ctx.send('You are already in a tribe, leave your current tribe with F!t leave')

    else:
      all_tags = []
      for i in clans_list:
        all_tags.append(i[3][1])

      c_tag = all_tags.index(action2)

      await ctx.send('joined tribe')

      peoplecharacters[gametag][26] = c_tag + 1
      clans_list[c_tag][2].append([gametag, 1])
      db["charactersofall"] = peoplecharacters
      db["clans"] = clans_list






  if action1 == 'leave':

    if peoplecharacters[gametag][26] != 0:
      clan_id = peoplecharacters[gametag][26] - 1
      clan_data = clans_list[clan_id]
      if clan_data[2][0][0] == gametag:
        msg = await ctx.send(f'You can not leave a clan you make, so you will have to delete your tribe!\nAre you sure you want to delete your tribe?\nType: **yes** or **no**')
        done = False
        while not done:
          try:
            response = await client.wait_for('message', timeout=60.0)
          except asyncio.TimeoutError:
            await msg.edit(content='You did not delete your tribe, because of timeout')
            done = True
          else:
            if response.author.id == ctx.author.id:
              done = True
              if response.content.lower() == 'no':
                await msg.edit(content='You did not delete your tribe!')
              elif response.content.lower() == 'yes':
                await msg.edit(content='You deleted your tribe!')
                clans_list.pop(clan_id)
                db["clans"] = clans_list
                peoplecharacters[gametag][26] = 0
                db["charactersofall"] = peoplecharacters
 
      else:
        await ctx.send(f'you have left your tribe!')
        peoplecharacters[gametag][26] = 0
        db["charactersofall"] = peoplecharacters
      
    else:
      await ctx.send('You cant leave a tribe, because you are not in any of them')
  






  if action1 == 'roles':
    
    if peoplecharacters[gametag][26] != 0:
      clan_id = peoplecharacters[gametag][26] - 1
      clan_data = clans_list[clan_id]
    
    
      #[response.content, [['owner', '11111'], ['member', '00000']], [[gametag, 0]], [':flags:', tag]]
      t_roles = clan_data[1]
      t_perms = ['start war', 'kick members', 'give roles to users', 'use tribe currency', 'change clan info']
      t_perms_e = [':white_check_mark:', ':negative_squared_cross_mark:']
      embedVar = discord.Embed(title='Tribe Roles')
      for roles in t_roles:
        te_string = ""
        perms = list(roles[1])
        t_count = 0
        for temp_perm in perms:
          if temp_perm == '1':
            te_string = te_string + t_perms_e[0] + ' ' + t_perms[t_count] + '\n'
            t_count += 1
          else:
            te_string = te_string + t_perms_e[1] + ' ' + t_perms[t_count] + '\n'
            t_count += 1


        embedVar.add_field(name=roles[0], value=te_string)



      await ctx.send(embed=embedVar)


    else:
      await ctx.send('not in tribe!')

@client.command()
async def setting(ctx):
  
  
  gametag = players.index(ctx.author.id)
  
  settings_preset = peoplecharacters[gametag][24]
  status = [':red_circle: Disabled', ':green_circle: Enabled']
  settings_ui = []
  for i in settings_preset:
    if i == 0:
      settings_ui.append(status[0])
    else:
      settings_ui.append(status[1])
  
 
  embedVar = discord.Embed(title=f":gear: | {ctx.author} Settings", description="Type the index of the section you want to toggle\nExample: type **1** to toggle **Dm Notifications**", color=0x828282)
  embedVar.add_field(name=":one: | Dm Notifications", value=f":arrow_up: | {settings_ui[0]}", inline=False)
  embedVar.set_footer(text="type exit to close this menu")
  
  msg = await ctx.send(embed=embedVar)


  

  done = False
  while not done:
    try:
      response = await client.wait_for('message', timeout=30.0)
    except asyncio.TimeoutError:
      done = True
      embedVar = discord.Embed(title=f":gear: | {ctx.author} Settings", description="Closed Settings Menu due to inactivity!", color=0xff0000)
      await msg.edit(embed=embedVar)
    else:
      if response.author.id == ctx.author.id:
        if response.content == '1':
          if settings_preset[0] == 1:
            peoplecharacters[gametag][24][0] = 0
            db["charactersofall"] = peoplecharacters
            settings_preset[0] = 0
            settings_ui[0] = ':red_circle: Disabled'

          elif settings_preset[0] == 0:
            peoplecharacters[gametag][24][0] = 1
            db["charactersofall"] = peoplecharacters
            settings_preset[0] = 1
            settings_ui[0] = ':green_circle: Enabled'
            
        

          embedVar = discord.Embed(title=f":gear: | {ctx.author} Settings", description="Type the index of the section you want to toggle\nExample: type **1** to toggle **Dm Notifications**", color=0x828282)
          embedVar.add_field(name=":one: | Dm Notifications", value=f":arrow_up: | {settings_ui[0]}", inline=False)
        
          embedVar.set_footer(text="type exit to close this menu")
  
          await msg.edit(embed=embedVar)
        if response.content == 'exit':
          done = True
          embedVar = discord.Embed(title=f":gear: | {ctx.author} Settings", description="Closed Settings Menu!", color=0xff0000)
          await msg.edit(embed=embedVar)
        
  

async def find_top_voter(playerlist, playervotexp):

  listtoreturn = []
  index = 0
  for i in playerlist:

    
    listtoreturn.append([playervotexp[index][22], str(playerlist[index])])
    index += 1
  

  listtoreturn.sort(reverse = True)
  return listtoreturn


@client.command()
async def vote(ctx, thing = None):
  if thing == None:
    e1 = "<:exp_bar_full:831276964181573643>"
    e2 = "<:exp_bar_empty:831277316859756564>"
    e3 = ":negative_squared_cross_mark:"
    e4 = ":white_check_mark:"

    xpt = peoplecharacters[players.index(ctx.author.id)][22]
    there_level = math.floor(xpt / 3)
    xp = xpt - (there_level * 3)

    embedVar = discord.Embed(title="Vote for Rewards and Perks!", description="You can vote for FunGuy every 12 hours for rewards!\n[Click here](https://top.gg/bot/801083957168570388/vote) to vote", color=0x8f00ff)

    embedVar.add_field(name="Vote Rewards", value="+1 Vote xp\n+1 Bronze chest", inline=False)
  
    xp_list = [e2, e2, e2]
    count = 0
    for i in range(xp):
      if i < 3:
        xp_list[count] = e1
        count += 1
    

    embedVar.add_field(name="Vote Xp", value=f"{xp_list[0]}{xp_list[1]}{xp_list[2]} **|** {xp}/3 xp to level up a tier", inline=False)

    level_list = [e3, e3, e3]
    count = 0
    for i in range(there_level):
      if i < 3:
        level_list[count] = e4
        count += 1

    embedVar.add_field(name=f"Vote Tier Perks (You are tier {there_level})", value=f"{level_list[0]} | Tier 1 - +5% Finding a chest while using Resource Gathering commands\n{level_list[1]} | Tier 2 - +15% Gamble earnings\n{level_list[2]} | Tier 3 - Chests now contain coins", inline=False)

    embedVar.set_footer(text="For every 3 vote xp you will level up a vote tier, and will get a perk!")

    await ctx.send(embed=embedVar)
  elif thing == 'leaderboard':
    toplist = await find_top_voter(players, peoplecharacters)

    p1p = toplist[0][0]
    p2p = toplist[1][0]
    p3p = toplist[2][0]

    p1n = await client.fetch_user(int(toplist[0][1]))
    p2n = await client.fetch_user(int(toplist[1][1]))
    p3n = await client.fetch_user(int(toplist[2][1]))

    embedVar = discord.Embed(title="<:upvote_emoji:867114498173960202> **|** Top Voters", description=f":first_place: {p1n.name} - {p1p} :arrow_up:\n:second_place: {p2n.name} - {p2p} :arrow_up:\n:third_place: {p3n.name} - {p3p} :arrow_up:", color=0x0000ff)

    await ctx.send(embed=embedVar)

  chance = 5
  if random.randint(0,100) < chance:
    #spawn airdrop
    embedVar = discord.Embed(title="<a:airdrop_emoji:879392658508902410> | Airdrop", description="react with :toolbox: to claim airdrop")
    
    msg = await ctx.send(embed=embedVar)

    await msg.add_reaction('🧰')
    await asyncio.sleep(0.1)
    try:
      reaction, user = await client.wait_for('reaction_add', timeout=50.0)
    except asyncio.TimeoutError:
      embedVar = discord.Embed(title=":negative_squared_cross_mark: |Airdrop", description=f"Noone claimed the airdrop!")
      await msg.edit(embed=embedVar)
    else:
      reaction = str(reaction.emoji)
      if reaction == '🧰':
        embedVar = discord.Embed(title=":white_check_mark: |Airdrop", description=f"{user} has claimed the airdrop!")
        await msg.edit(embed=embedVar)
        await msg.clear_reactions()

        gametag = players.index(user.id)
        peoplecharacters[gametag][25][0] += 1
        db["charactersofall"] = peoplecharacters

@client.command()
@commands.cooldown(1, 60 * 15, commands.BucketType.user)
async def dig(ctx):
  gametag = players.index(ctx.author.id)

  itemsnames = ["<:common_fish:806986714627178496> commonfish", "<:rare_fish:806986792184184853> rarefish", "<:epic_fish:806986882449145888> epicfish", "<:water_bottle:839580961191493634> waterbottle", "<:lily_pad:839564075347869787> lilypad", "<:rock:821101496531681338> rock", "<:iron:821101561157386262> iron", "<:copper:821101604961779712> copper", "bronze", "<:wood_stick:825030799026814997> stick", "<:wood_log:825030291838992504> log", "<:leaf:839564127408095253> leaf", "<:red_apple:839564590949466172> apple", "<:banana:839581019120336987> banana", "<:ruby:839564178637324329> ruby", "<:diamond:839564238099054623> diamond", "sil chest", "golden chest", "po 1", "po 2", "potion 3 (po = potion)", "pres chest", "<:fertilizer:865256293334122506> fertilizer","<:dirt_pile:873278535559692298> dirt","<:sand_pile:873278153978679297> sand","<:gravel_pile:873278030246719499> gravel"]
        



  
        
  loot_draws = [[0, 0],[1, 0],[2, 0],[3, 0],[4, 0],[5, 0],[6, 0],[7, 0],[9, 0],[10, 0],[11, 0],[12, 0],[13, 0],[14, 0],[15, 0],[22, 0],[23, 5],[24, 3],[25, 1]]
        
        
  loot = get_loot(loot_draws, 'dig')
        
  loot_string = ""
  for i in loot:
    loot_string = loot_string + f"+{i[0]} {itemsnames[i[1]]}\n"
    iteminventorys[gametag][i[1]] += i[0]
  
  db["itemsofall"] = iteminventorys

  embedVar = discord.Embed(title="You are done digging!", description=f"User: {ctx.author}", color=0x828282)
  embedVar.add_field(name="You Got:", value=f"{loot_string}", inline=False)

  #prestige and chest drops
            
  extra_got = []

  randomnumi = random.randint(0,99)
  randomnumin = random.randint(0,99)
            
  chest_chance = 25
  xpt = peoplecharacters[players.index(ctx.author.id)][22]
  there_level = math.floor(xpt / 3)
  if there_level >= 1:
    chest_chance = 30
            
  if randomnumi < 25:
    peoplecharacters[gametag][13] += 1
    db["charactersofall"] = peoplecharacters
    extra_got.append("+1 :low_brightness: prestige point")
  if randomnumin < chest_chance:
    iteminventorys[gametag][8] += 1
    db["itemsofall"] = iteminventorys
    extra_got.append("+1 <:bronze_chest_closed:835618525250060388> Bronze Chest")
              
  if len(extra_got) > 0:
    lineyay = ""
    for i in extra_got:
      lineyay = lineyay + i + "\n"
    embedVar.add_field(name="Extra", value=f"{lineyay}", inline=False)




  
  
  await ctx.send(embed=embedVar)
  

@dig.error
async def dig_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    timeleft = math.ceil(error.retry_after / 60)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"looks like your on a cooldown for {timeleft} minutes!\nUser: {ctx.author}", color=0xff0000)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
  else:
    raise error

@client.command(aliases=['leaderboards', 'lb'])
async def leaderboard(ctx):

  toplist = await find_top(players, peoplecharacters)

  p1p = toplist[0][0]
  p2p = toplist[1][0]
  p3p = toplist[2][0]

  p1n = await client.fetch_user(int(toplist[0][1]))
  p2n = await client.fetch_user(int(toplist[1][1]))
  p3n = await client.fetch_user(int(toplist[2][1]))

  embedVar = discord.Embed(title=":low_brightness: **|** Prestige Leaderboard (Term 2)", description=f"Resets on: October 25th\n:first_place: {p1n.name} - {p1p} :low_brightness:\n:second_place: {p2n.name} - {p2p} :low_brightness:\n:third_place: {p3n.name} - {p3p} :low_brightness:\n__Top 3 people will get a special reward!__\n+1 <:prestige_chest:821374315546804234> Prestige Chest\n+1 :sloth: Exclusive Pet\n:unlock: | New farm crop, Coin Tree\n__1st Place will get a extra Reward__", color=0x0000ff)

  await ctx.send(embed=embedVar)

async def find_top(playerlist, playerprestige):

  listtoreturn = []
  index = 0
  for i in playerlist:

    #username = await client.fetch_user(playerlist[index])
    listtoreturn.append([playerprestige[index][13], str(playerlist[index])])
    index += 1
  

  listtoreturn.sort(reverse = True)
  return listtoreturn

@client.command()
async def reset(ctx):
  toplist = await find_top(players, peoplecharacters)

  p1p = toplist[0][0]
  p2p = toplist[1][0]
  p3p = toplist[2][0]

  p1n = toplist[0][1]
  p2n = toplist[1][1]
  p3n = toplist[2][1]

  embedVar = discord.Embed(title=":low_brightness: **|** Prestige Leaderboard Has Been Reset", description=f"Congratulations NotLoofy 🌺, ニャ﹏, and expl1ain for being top 3 in the leaderboard!\nYour Rewards have been given", color=0x0000ff)
  
  
  tag1 = players.index(527877350986219521)
  tag2 = players.index(790450328700846090)
  tag3 = players.index(751808635583332412)

  iteminventorys[tag1][-1] += 1
  iteminventorys[tag2][-1] += 1
  iteminventorys[tag3][-1] += 1
  
  peoplecharacters[tag1][11].append(6)
  peoplecharacters[tag2][11].append(6)
  peoplecharacters[tag3][11].append(6)
  

  count = 0
  for ind in peoplecharacters:
    peoplecharacters[count][13] = 0
    count += 1

  db["charactersofall"] = peoplecharacters
  db["itemsofall"] = iteminventorys

  await ctx.send(embed=embedVar)

@client.command()
@commands.cooldown(1, 60 * 60 * 5, commands.BucketType.user)
async def prestige(ctx, usertogive : discord.Member = None):
  tempid = ctx.author.id
  if tempid in players:
    if usertogive == None:
      ctx.command.reset_cooldown(ctx)
      embedVar = discord.Embed(title=f"<a:yellow_star:857366567741423656> | Prestige Point", description=f"The correct format is F!prestige <user>!", color=0xff0000)
      await ctx.send(embed=embedVar)
      
    if usertogive.id == ctx.author.id:
      ctx.command.reset_cooldown(ctx)
      embedVar = discord.Embed(title=f"<a:yellow_star:857366567741423656> | Prestige Point", description=f"You can not give a prestige point to yourself!", color=0xff0000)
      await ctx.send(embed=embedVar)
      
    elif usertogive != None and usertogive.id in players:
      embedVar = discord.Embed(title=f"<a:yellow_star:857366567741423656> | Prestige Point", description=f"You have given a prestige point to {usertogive.name}!", color=0xffff00)
      await ctx.send(embed=embedVar)
      gametag = players.index(usertogive.id)
      peoplecharacters[gametag][13] += 1
      db["charactersofall"] = peoplecharacters
    elif usertogive != None and usertogive.id not in players:
      ctx.command.reset_cooldown(ctx)
      embedVar = discord.Embed(title=f"<a:yellow_star:857366567741423656> | Prestige Point", description=f"You can not give a prestige point to this user!", color=0xff0000)
      await ctx.send(embed=embedVar)
   


  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@prestige.error
async def prestige_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    timeleft = math.ceil(error.retry_after / 60)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"looks like your on a cooldown for {timeleft} minutes!\n**User: {ctx.author}**", color=0xff0000)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
  if isinstance(error, commands.MemberNotFound):
    ctx.command.reset_cooldown(ctx)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"Looks like i could not find the user!", color=0xff0000)
    await ctx.send(embed=embedVar)
  else:
    raise error



@client.command(aliases=['i', 'inv'])
async def inventory(ctx, usermentioned : discord.Member = None):
  if usermentioned == None:
    tempid = ctx.author.id
    usern = ctx.author.name
  else:
    tempid = usermentioned.id
    usern = usermentioned
  

  if tempid in players:
    gametag = players.index(tempid)
    

    

    embedVar = discord.Embed(title=f"{usern}'s Inventory", color=0xffff00)

    tempcfish = iteminventorys[gametag][0]
    temprfish = iteminventorys[gametag][1]
    tempefish = iteminventorys[gametag][2]
    tempwbottle = iteminventorys[gametag][3]

    templpad = iteminventorys[gametag][4]

    temprock = iteminventorys[gametag][5]
    tempiron = iteminventorys[gametag][6]
    tempcopper = iteminventorys[gametag][7]
    tempbchest = iteminventorys[gametag][8]
    tempstick = iteminventorys[gametag][9]
    tempwood = iteminventorys[gametag][10]
    
    templeaf = iteminventorys[gametag][11]
    tempapple = iteminventorys[gametag][12]
    tempbanana = iteminventorys[gametag][13]

    tempruby = iteminventorys[gametag][14]
    tempdiamond = iteminventorys[gametag][15]

    tempschest = iteminventorys[gametag][16]
    tempgchest = iteminventorys[gametag][17]

    tempcp = iteminventorys[gametag][18]
    tempfp = iteminventorys[gametag][19]
    temptp = iteminventorys[gametag][20]
    temppc = iteminventorys[gametag][21]

    templt = iteminventorys[gametag][22]

    tempdp = iteminventorys[gametag][23]
    tempsp = iteminventorys[gametag][24]
    tempgp = iteminventorys[gametag][25]
    #Fish items setting (down)


    itemstorea = [tempcfish, temprfish, tempefish, tempwbottle, templpad]
    itemstoren = [" <:common_fish:806986714627178496> common fish", " <:rare_fish:806986792184184853> rare fish", " <:epic_fish:806986882449145888> epic fish", " <:water_bottle:839580961191493634> water bottle", " <:lily_pad:839564075347869787> lily pad"]
    fishinv = []
    count = 0
    for i in itemstorea:
      if i > 0:
        fishinv.append([i, itemstoren[count]])
      count += 1
    
    
    connectedline1 = connect(fishinv)

    if len(fishinv) > 0:
      embedVar.add_field(name=f"Fish Items", value=f"{connectedline1}")
    

    #Mine items setting (down)


    itemstorea = [temprock, tempiron, tempcopper, tempruby, tempdiamond]
    itemstoren = [" <:rock:821101496531681338> rock", " <:iron:821101561157386262> iron",  " <:copper:821101604961779712> copper",  " <:ruby:839564178637324329> ruby",  " <:diamond:839564238099054623> diamond"]
    mineinv = []
    count = 0
    for i in itemstorea:
      if i > 0:
        mineinv.append([i, itemstoren[count]])
      count += 1
    
    connectedline2 = connect(mineinv)

    if len(mineinv) > 0:
      embedVar.add_field(name=f"Mine Items", value=f"{connectedline2}")



    #Chop items setting (down)


    itemstorea = [tempstick, tempwood, templeaf, tempapple, tempbanana]
    itemstoren = [" <:wood_stick:825030799026814997> stick", " <:wood_log:825030291838992504> log",  " <:leaf:839564127408095253> leaf",  " <:red_apple:839564590949466172> apple",  " <:banana:839581019120336987> banana"]
    chopinv = []
    count = 0
    for i in itemstorea:
      if i > 0:
        chopinv.append([i, itemstoren[count]])
      count += 1
    
    connectedline3 = connect(chopinv)

    if len(chopinv) > 0:
      embedVar.add_field(name=f"Chop Items", value=f"{connectedline3}")

 
    #Chests setting (down)


    itemstorea = [tempbchest, tempschest, tempgchest, temppc]
    itemstoren = ["  <:bronze_chest_closed:835618525250060388> bronze chest", " <:silver_chest_closed:835618762409246720> silver chest", " <:gold_chest_closed:835618687565561936> golden chest", " <:prestige_chest:821374315546804234> prestige chest"]
    cinv = []
    count = 0
    for i in itemstorea:
      if i > 0:
        cinv.append([i, itemstoren[count]])
      count += 1
    
    connectedline4 = connect(cinv)

    if len(cinv) > 0:
      embedVar.add_field(name=f"Chests", value=f"{connectedline4}")

    

    
    
    
    #Potion setting (down)


    itemstorea = [tempcp, tempfp, temptp]
    itemstoren = [" <:cooldown_potion:854858969206095952> Cooldown Potion", " <:farm_potion:854859290375618560> Farm Potion", " <:train_potion:854859149510443028> Train Potion"]
    poinv = []
    count = 0
    for i in itemstorea:
      if i > 0:
        poinv.append([i, itemstoren[count]])
      count += 1
    
    connectedline5 = connect(poinv)

    if len(poinv) > 0:
      embedVar.add_field(name=f"Potions", value=f"{connectedline5}")



    #special items setting (down)


    itemstorea = [templt]
    itemstoren = [" <:fertilizer:865256293334122506> fertilizer"]
    sinv = []
    count = 0
    for i in itemstorea:
      if i > 0:
        sinv.append([i, itemstoren[count]])
      count += 1
    
    connectedline6 = connect(sinv)

    if len(sinv) > 0:
      embedVar.add_field(name=f"Special Items", value=f"{connectedline6}")

    
    
    #dig items setting (down)


    itemstorea = [tempdp, tempsp, tempgp]
    itemstoren = [" <:dirt_pile:873278535559692298> dirt"," <:sand_pile:873278153978679297> sand"," <:gravel_pile:873278030246719499> gravel"]
    dinv = []
    count = 0
    for i in itemstorea:
      if i > 0:
        dinv.append([i, itemstoren[count]])
      count += 1
    
    connectedline7 = connect(dinv)

    if len(dinv) > 0:
      embedVar.add_field(name=f"Dig Items", value=f"{connectedline7}")


    
    embedVar.set_footer(text=f"To see a item type F!sell <amount> <item> | Example: F!sell 6 commonfish")
    await ctx.send(embed=embedVar)

  else:
    if id == None:
      embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
      await ctx.send(embed=embedVar)
    else:
      embedVar = discord.Embed(title="OH NOO!", description=f"looks like {usern} dosen't have a account!", color=0xff0000)
      await ctx.send(embed=embedVar)


def connect(thing):
  finalline = ""
  maxrepeat = len(thing)
  trepeat = 1
  for i in thing:
    if trepeat < maxrepeat:
      finalline = finalline + str(i[0]) + i[1] + "\n"
      trepeat += 1
    else:
      finalline = finalline + str(i[0]) + i[1]
  return finalline

@client.command(aliases=['p', 'bal'])
async def profile(ctx, usermentioned : discord.Member = None):
  if usermentioned == None:
    tempid = ctx.author.id
    usern = ctx.author.name
  else:
    tempid = usermentioned.id
    usern = usermentioned
  if tempid in players:
    gametag = players.index(tempid)
    tempmoney = moneybags[gametag]
    
    unitindex = peoplecharacters[gametag][12]
    unit = travelunit[unitindex]

    characteremoji = "<:rusty_knight:824653099422711889>"

    listofdata = get_users_data(gametag)

    chealth = listofdata[0]
    shealth = listofdata[1]
    damage = listofdata[2]
    dodger = listofdata[3]
    prestigeofplayer = peoplecharacters[gametag][13]

    embedVar = discord.Embed(title=f"{usern}`s Profile", description=f"{prestigeofplayer} :low_brightness:", color=0xffff00)

    embedVar.add_field(name=f"Character", value=f"Character: {characteremoji} Weapon: <:iron_sword:834065954837233696>\n{chealth} :heart: {shealth} :shield: {damage} :boom: {dodger}% :cloud_tornado:\nTravel unit: {unit}", inline=False)

    embedVar.add_field(name=f"Money", value=f"{tempmoney} <:coin:824666710383657010> coins", inline=False)
    if cha_boosters[0] == tempid:
      embedVar.add_field(name=':arrow_up: Boosters', value=f'+{cha_boosters[1][1]}% more coins from selling')
    else:
      embedVar.add_field(name=':arrow_up: Boosters', value='none')


    await ctx.send(embed=embedVar)
  else:
    if id == None:
      embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
      await ctx.send(embed=embedVar)
    else:
      embedVar = discord.Embed(title="OH NOO!", description=f"looks like {usern} dosen't have a account!", color=0xff0000)
      await ctx.send(embed=embedVar)
    


def get_users_data(index):
    d1 = peoplecharacters[index][6]
    d2 = peoplecharacters[index][7]
    d3 = peoplecharacters[index][8]
    d4 = peoplecharacters[index][9]
    
    #d1 = health, d2 = sheild, d3 = damage, d4 = dodge
    ind = peoplecharacters[index][10]
    
  
  
    petlevel = peoplecharacters[index][4]
    amountincrease = (petamounts[ind - 1] / 2) * (petlevel + 2)

    if ind == 1:
      d1 += math.ceil(amountincrease)
    if ind == 2:
      d3 += math.ceil(amountincrease * 3)
    if ind == 4:
      d4 += math.ceil(amountincrease)
    if ind == 6:
      d1 += math.ceil(amountincrease)

    return [d1, d2, d3, d4]

@client.command()
async def sell(ctx, amount, item):
  tempid = ctx.author.id

  if tempid in players:
    if item in items:
      itemindex = items.index(item)
      gametag = players.index(tempid)
      amountofitemtheyhave = iteminventorys[gametag][itemindex]

      if amount == "all":
        amounttosell = amountofitemtheyhave
      else:
        amounttosell = int(amount)

      sellvalue = itemsvalue[itemindex] * amounttosell

      if amountofitemtheyhave >= amounttosell:
        embedVar = discord.Embed(title="Sold", description=f"You sold {amounttosell} {item} for {sellvalue} coins", color=0x00ff00)

        if cha_boosters[0] == ctx.author.id:
          se_bonus = round(sellvalue / 100 * cha_boosters[1][1])
          embedVar.add_field(name=':arrow_up: Booster', value=f'Because of your booster you also gained {se_bonus} coins!')
          moneybags[gametag] += se_bonus


        await ctx.send(embed=embedVar)

        iteminventorys[gametag][itemindex] -= amounttosell
        moneybags[gametag] += sellvalue

        db["itemsofall"] = iteminventorys
        db["moneybagsofall"] = moneybags



      else:
        embedVar = discord.Embed(title="OH NOO!", description=f"You are trying to sell {amounttosell} {item} but you only have {amountofitemtheyhave} {item}", color=0xff0000)
        await ctx.send(embed=embedVar)
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@client.command()
async def help(ctx):

  tempid = ctx.author.id
  if tempid in players:

    embedVar = discord.Embed(title="Command List", description=f"Key: <required_argument> (optional_argument) [unlimited_arguments]", color=0xff00ff)
    embedVar.add_field(name=":ticket: Personal Commands", value="start | profile | inventory (user_id) | quest | cooldowns | pet (action) (action) | train | upgrade | farm (action1) (action2) | brew (action1) (action2)", inline=False)
    embedVar.add_field(name=":coin: Economy Commands", value="sell <amount> <item> | trade <action> | hourly | use <item_name> | forge (action) | shop", inline=False)
    embedVar.add_field(name=":pick: Resource Gathering Commands", value="fish | mine | chop | adventure", inline=False)
    embedVar.add_field(name=":trophy: Competitive Commands", value="arena | leaderboard | prestige <user>", inline=False)
    embedVar.add_field(name=":game_die: Gambling Commands", value="slots <bet> | coinflip <bet> | cups <bet> | scratch", inline=False)
    embedVar.add_field(name=":wrench: Other Commands", value="choose [choices seperated by: (space)] | calculate <operation> <num1> (num2) | map", inline=False)
    embedVar.add_field(name=f":timer: Latency: *{round(client.latency, 3)} seconds*", value="[Join](https://discord.gg/WByYtSKJQe) the official FunGuy Bot server!\n```\n- Join giveaways to win free stuff\n- Report bugs\n- Receive a special prestige leaderboard role\n- Chat with other people\n```", inline=False)

    await ctx.send(embed=embedVar)
  else:
    embedVar = discord.Embed(title="Command List", description=f"Key: <required_argument> (optional_argument) [unlimited_arguments]", color=0xff00ff)
    embedVar.add_field(name=":loudspeaker: Looks Like Your New", value="Type F!start to get access to all the commands!", inline=False)
    embedVar.add_field(name=":ticket: Personal Commands", value="start | profile | inventory (user_id) | quest | cooldowns | pet (action) (action) | train | upgrade | farm (action1) (action2) | brew (action1) (action2)", inline=False)
    embedVar.add_field(name=":coin: Economy Commands", value="sell <amount> <item> | trade <action> | hourly | use <item_name> | forge (action) | shop", inline=False)
    embedVar.add_field(name=":pick: Resource Gathering Commands", value="fish | mine | chop | adventure | dig", inline=False)
    embedVar.add_field(name=":trophy: Competitive Commands", value="arena | leaderboard | prestige <user>", inline=False)
    embedVar.add_field(name=":game_die: Gambling Commands", value="slots <bet> | coinflip <bet> | cups <bet> | scratch", inline=False)
    embedVar.add_field(name=":wrench: Other Commands", value="choose [choices seperated by: (space)] | calculate <operation> <num1> (num2) | map", inline=False)
    embedVar.add_field(name=f":timer: Latency: *{round(client.latency, 3)} seconds*", value="[Join](https://discord.gg/WByYtSKJQe) the official FunGuy Bot server!\n```\n- Join giveaways to win free stuff\n- Report bugs\n- Receive a special prestige leaderboard role\n- Chat with other people\n```", inline=False)

    await ctx.send(embed=embedVar)





@client.command()
async def slots(ctx, bet: int):
  tempid = ctx.author.id

  if tempid in players:
    gametag = players.index(tempid)
    moneytheyhave = moneybags[gametag]

    if bet <= moneytheyhave and bet > 0:
      embedVar = discord.Embed(title="SLOTS MACHINE!", description="**------------------**\n**| <a:slots_game:852274471590428722> | <a:slots_game:852274471590428722> | <a:slots_game:852274471590428722> |**\n**------------------**", color=0xff0000)
      

      msg = await ctx.send(embed=embedVar)

      await asyncio.sleep(3)
      option_s = [":gem:", ":moneybag:", ":coin:", ":credit_card:"]
      slots_d = []
      slots_d.append(random.choice(option_s))
      slots_d.append(random.choice(option_s))
      slots_d.append(random.choice(option_s))

      embedVar = discord.Embed(title="SLOTS MACHINE!", description=f"**------------------**\n**| {slots_d[0]} | {slots_d[1]} | {slots_d[2]} |**\n**------------------**", color=0xff0000)

      if slots_d[0] == slots_d[1] or slots_d[0] == slots_d[2] or slots_d[1] == slots_d[0] or slots_d[1] == slots_d[2] or slots_d[2] == slots_d[0] or slots_d[2] == slots_d[1]:
        embedVar.add_field(name="**-----YAY!-----**",value=f"You won {bet} coins", inline=False)
        
        
        xpt = peoplecharacters[players.index(ctx.author.id)][22]
        there_level = math.floor(xpt / 3)
        if there_level >= 2:
          bonus_coins = round(bet / 100 * 15)

          embedVar.add_field(name="**<:upvote_emoji:867114498173960202> **|** Vote Bonus**",value=f"You also got {bonus_coins} coins", inline=False)
          moneybags[gametag] += bonus_coins

        moneybags[gametag] += bet
        db["moneybagsofall"] = moneybags

      else:
        embedVar.add_field(name="**---OH NOO!---**",value=f"You lost {bet} coins", inline=False)
        
        moneybags[gametag] -= bet
        db["moneybagsofall"] = moneybags

      await msg.edit(embed=embedVar)

    else:
       embedVar = discord.Embed(title="OH NOO!", description=f"You are trying to bet {bet} coins but you only have {moneytheyhave} coins", color=0xff0000)
       await ctx.send(embed=embedVar)

  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)



@client.command(aliases=['h', 'hour'])
@commands.cooldown(1, 60 * 60, commands.BucketType.user)
async def hourly(ctx):
  tempid = ctx.author.id
  if tempid in players:
    gametag = players.index(tempid)
    iteminventorys[gametag][8] += 1
    db["itemsofall"] = iteminventorys


    peoplecharacters[gametag][25][3] += 30
    db["charactersofall"] = peoplecharacters
    await ctx.send(">>> You have recived a bronze chest!\nYou also got 30 candy :candy:!")
    
    randomnumi = random.randint(0,99)
    if randomnumi < 25:
      peoplecharacters[gametag][13] += 1
      db["charactersofall"] = peoplecharacters
      await ctx.send("You also got +1 :low_brightness: prestige point!")
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@hourly.error
async def hourly_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    timeleft = math.ceil(error.retry_after / 60)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"looks like your on a cooldown for {timeleft} minutes!\n**User: {ctx.author}**", color=0xff0000)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
  else:
    raise error
         

@client.command()
@commands.cooldown(1, 60 * 20, commands.BucketType.user)
async def arena(ctx):
  embedVar = discord.Embed(title="Arena!!", description=f"{ctx.author.name}'s Is enetering the **Arena**\nReact to Join! **|** :stopwatch: Cancels in 20 seconds", color=0x00ffff)

  mainuserid = ctx.author.id
  mainusername = ctx.author.name

  msg = await ctx.send(embed=embedVar)
  await msg.add_reaction('⚔️')
  await asyncio.sleep(1)
  done = False
  while not done:

   try:

     reaction, user = await client.wait_for('reaction_add', timeout=20.0)

   except asyncio.TimeoutError:
      ctx.command.reset_cooldown(ctx)
      embedVar = discord.Embed(title="OH NOO!", description=f"Noone joined the arena, {ctx.author.name}!", color=0xff0000)

      await msg.edit(embed=embedVar)
      done = True

   else:
      if mainuserid != user.id:
        done = True
        
        otheruserid = user.id
        otherusername = user.name

        bossb = ["Snow Biome :mountain_snow:", "Ocean Biome :ocean:",]
        bossn = ["Evil Snowman", "Giant Whale"]
        bossemoji = [":snowman:", ":whale:"]
        bossh = [55,30]
        bossd = [[1,2], [2,3]]
        bosstochoose = [0,1]

        bossi = random.choice(bosstochoose)
        bossstats = [bossh[bossi], bossd[bossi]]

        await msg.clear_reactions()

        embedVar = discord.Embed(title="Players Found!", description=f"{mainusername}\n{otherusername}\n__Fighting {bossn[bossi]}__ **|** Arena will start soon!", color=0x00ffff)

        await msg.edit(embed=embedVar)
        gametag1 = players.index(mainuserid)
        gametag2 = players.index(otheruserid)

        playersstats = []

        listofdata = get_users_data(gametag1)
        playersstats.append([listofdata[0],listofdata[1],listofdata[2],listofdata[3]])
        listofdata = get_users_data(gametag2)
        playersstats.append([listofdata[0],listofdata[1],listofdata[2],listofdata[3]])

        await asyncio.sleep(3)
        #0 = health, 1 = sheild, 2 = damage, 3 = dodge

        embedVar = discord.Embed(title=f"{bossb[bossi]}\n{bossn[bossi]} hp - {bossstats[0]} :heart:", description=f"{bossemoji[bossi]}", color=0x00ffff)
        embedVar.add_field(name="Moves! (type one of these moves when its your turn)", value=f"attack **|** {playersstats[0][2]} damage\ndodge **|** {playersstats[0][3]}% chance", inline=False)
        embedVar.add_field(name="Players", value=f"{mainusername} **|** {playersstats[0][0]} :heart: {playersstats[0][1]} :shield:\n{otherusername} **|** {playersstats[1][0]} :heart: {playersstats[1][1]} :shield:\nTurn: {mainusername}", inline=False)
        await msg.edit(embed=embedVar)

        
        turns = [mainuserid, otheruserid]
        tnames = [mainusername, otherusername]
        turn = 0
        done2 = False
        while not done2:
          try:
            response = await client.wait_for('message', timeout=20.0)
          except asyncio.TimeoutError:
            ctx.command.reset_cooldown(ctx)
            await ctx.send("you did not respond quickly!")
            done2 = True
          else:
            if response.content.startswith('attack') and response.author.id == turns[turn]:
              bossstats[0] -= playersstats[turn][2]
              playersstats[turn][0] -= bossstats[1][random.choice(bosstochoose)]
              if playersstats[turn][0] < 1:
                await ctx.send(f":skull: **|** {tnames[turn]} has died!")
                
              embedVar = discord.Embed(title=f"{bossb[bossi]}\n{bossn[bossi]} hp - {bossstats[0]} :heart:", description=f"{bossemoji[bossi]}", color=0x00ffff)
              embedVar.add_field(name="Moves! (type one of these moves when its your turn)", value=f"attack **|** {playersstats[0][2]} damage\ndodge **|** {playersstats[0][3]}% chance", inline=False)
              embedVar.add_field(name="Players", value=f"{mainusername} **|** {playersstats[0][0]} :heart: {playersstats[0][1]} :shield:\n{otherusername} **|** {playersstats[1][0]} :heart: {playersstats[1][1]} :shield:\nTurn: {tnames[turn]}", inline=False)
              await msg.edit(embed=embedVar)
            if response.content.startswith('dodge') and response.author.id == turns[turn]:
              
              if random.randint(0,100) > playersstats[turn][3]:
                playersstats[turn][0] -= bossstats[1][random.choice(bosstochoose)]
                if playersstats[turn][0] < 1:
                  await ctx.send(f":skull: **|** {tnames[turn]} has died!")
              
              embedVar = discord.Embed(title=f"{bossb[bossi]}\n{bossn[bossi]} hp - {bossstats[0]} :heart:", description=f"{bossemoji[bossi]}", color=0x00ffff)
              embedVar.add_field(name="Moves! (type one of these moves when its your turn)", value=f"attack **|** {playersstats[0][2]} damage\ndodge **|** {playersstats[0][3]}% chance", inline=False)
              embedVar.add_field(name="Players", value=f"{mainusername} **|** {playersstats[0][0]} :heart: {playersstats[0][1]} :shield:\n{otherusername} **|** {playersstats[1][0]} :heart: {playersstats[1][1]} :shield:\nTurn: {tnames[turn]}", inline=False)
              await msg.edit(embed=embedVar)
          
          
          if playersstats[0][0] > 0 or playersstats[0][1] > 0:
            if response.author.id == turns[turn]:
              turn += 1
            if turn == 2:
              turn = 0
          if playersstats[0][0] < 1 and playersstats[1][0] < 1:
            
            await ctx.send("You both died :cry:")
            done2 = True
          if bossstats[0] < 1:
            done2 = True
            await ctx.send(f'Yay {mainusername}, and {otherusername} You won! Reward: 1 silver chest')
            
            iteminventorys[gametag1][16] += 1
            iteminventorys[gametag2][16] += 1
				
            db["itemsofall"] = iteminventorys   

def get_loot(data, num):
  list_to_choose = []
  for i in data:
    for ind in range(i[1]):
      list_to_choose.append(i[0])

  if num == 1:
    chest_loot_indexes = []
    for index in range(3):
      chest_loot_indexes.append(random.choice(list_to_choose))
  if num == 2:
    chest_loot_indexes = []
    for index in range(15):
      chest_loot_indexes.append(random.choice(list_to_choose))
  if num == 3:
    chest_loot_indexes = []
    for index in range(28):
      chest_loot_indexes.append(random.choice(list_to_choose))
  if num == 4:
    chest_loot_indexes = []
    for index in range(75):
      chest_loot_indexes.append(random.choice(list_to_choose))
  if num == 'dig':
    chest_loot_indexes = []
    for index in range(6):
      chest_loot_indexes.append(random.choice(list_to_choose))
  if num == 'minenormal':
    chest_loot_indexes = []
    for index in range(4):
      chest_loot_indexes.append(random.choice(list_to_choose))
  if num == 'mineless':
    chest_loot_indexes = []
    for index in range(2):
      chest_loot_indexes.append(random.choice(list_to_choose))
  
  sorted_loot = get_amount_of(chest_loot_indexes)
  
  return sorted_loot

def get_amount_of(thing):
  group_list = []
  
  search = 0
  count = 0
  got = 0
  for thingy in range(26):
    for i in thing:
      if i == search:
        got += 1
      count += 1
    
    if got > 0:
      group_list.append([got, search])
    count = 0
    got = 0
    search += 1
    
  
  return group_list

    
      

@client.command()
async def use(ctx, chestname):
  tempid = ctx.author.id
  if tempid in players:
    gametag = players.index(tempid)
    if chestname == "bronze":
      bchesttheyhave = iteminventorys[gametag][8]

      if bchesttheyhave > 0:
        itemsnames = ["<:common_fish:806986714627178496> commonfish", "<:rare_fish:806986792184184853> rarefish", "<:epic_fish:806986882449145888> epicfish", "<:water_bottle:839580961191493634> waterbottle", "<:lily_pad:839564075347869787> lilypad", "<:rock:821101496531681338> rock", "<:iron:821101561157386262> iron", "<:copper:821101604961779712> copper", "bronze", "<:wood_stick:825030799026814997> stick", "<:wood_log:825030291838992504> log", "<:leaf:839564127408095253> leaf", "<:red_apple:839564590949466172> apple", "<:banana:839581019120336987> banana", "<:ruby:839564178637324329> ruby", "<:diamond:839564238099054623> diamond", "sil chest", "golden chest", "po 1", "po 2", "potion 3 (po = potion)", "pres chest", "<:fertilizer:865256293334122506> fertilizer"]
        
        
        loot_draws = [[0, 5],[1, 4],[2, 3],[3, 2],[4, 1],[5, 5],[6, 4],[7, 3],[9, 5],[10, 4],[11, 3],[12, 2],[13, 1],[14, 2],[15, 1],[22, 3]]
        
        
        loot = get_loot(loot_draws, 1)
        
        loot_string = ""
        for i in loot:
          loot_string = loot_string + f"+{i[0]} {itemsnames[i[1]]}\n"
          iteminventorys[gametag][i[1]] += i[0]
        
        embedVar = discord.Embed(title=f"You opened a {chestname} chest!", description=f"{loot_string}", color=0x542621)
        await ctx.send(embed=embedVar)

        iteminventorys[gametag][8] -= 1
        
				
        db["itemsofall"] = iteminventorys
      else:
        embedVar = discord.Embed(title="OH NOO!",description=f"looks like you dont have a {chestname} chest!", color=0xff0000)
        await ctx.send(embed=embedVar)

    if chestname == "silver":
      bchesttheyhave = iteminventorys[gametag][16]

      if bchesttheyhave > 0:
        itemsnames = ["<:common_fish:806986714627178496> commonfish", "<:rare_fish:806986792184184853> rarefish", "<:epic_fish:806986882449145888> epicfish", "<:water_bottle:839580961191493634> waterbottle", "<:lily_pad:839564075347869787> lilypad", "<:rock:821101496531681338> rock", "<:iron:821101561157386262> iron", "<:copper:821101604961779712> copper", "bronze", "<:wood_stick:825030799026814997> stick", "<:wood_log:825030291838992504> log", "<:leaf:839564127408095253> leaf", "<:red_apple:839564590949466172> apple", "<:banana:839581019120336987> banana", "<:ruby:839564178637324329> ruby", "<:diamond:839564238099054623> diamond", "sil chest", "golden chest", "po 1", "po 2", "potion 3 (po = potion)", "pres chest", "<:fertilizer:865256293334122506> fertilizer"]
        
        
        loot_draws = [[0, 5],[1, 4],[2, 3],[3, 2],[4, 1],[5, 5],[6, 4],[7, 3],[9, 5],[10, 4],[11, 3],[12, 2],[13, 1],[14, 2],[15, 1],[22, 3]]
        
        
        loot = get_loot(loot_draws, 2)
        
        loot_string = ""
        for i in loot:
          loot_string = loot_string + f"+{i[0]} {itemsnames[i[1]]}\n"
          iteminventorys[gametag][i[1]] += i[0]
        
        embedVar = discord.Embed(title=f"You opened a {chestname} chest!", description=f"{loot_string}", color=0x542621)
        await ctx.send(embed=embedVar)

        iteminventorys[gametag][16] -= 1
        
				
        db["itemsofall"] = iteminventorys
      else:
        embedVar = discord.Embed(title="OH NOO!",description=f"looks like you dont have a {chestname} chest!", color=0xff0000)
        await ctx.send(embed=embedVar)

    if chestname == "golden":
      bchesttheyhave = iteminventorys[gametag][17]

      if bchesttheyhave > 0:
        itemsnames = ["<:common_fish:806986714627178496> commonfish", "<:rare_fish:806986792184184853> rarefish", "<:epic_fish:806986882449145888> epicfish", "<:water_bottle:839580961191493634> waterbottle", "<:lily_pad:839564075347869787> lilypad", "<:rock:821101496531681338> rock", "<:iron:821101561157386262> iron", "<:copper:821101604961779712> copper", "bronze", "<:wood_stick:825030799026814997> stick", "<:wood_log:825030291838992504> log", "<:leaf:839564127408095253> leaf", "<:red_apple:839564590949466172> apple", "<:banana:839581019120336987> banana", "<:ruby:839564178637324329> ruby", "<:diamond:839564238099054623> diamond", "sil chest", "golden chest", "po 1", "po 2", "potion 3 (po = potion)", "pres chest", "<:fertilizer:865256293334122506> fertilizer"]
        
        
        loot_draws = [[0, 5],[1, 4],[2, 3],[3, 2],[4, 1],[5, 5],[6, 4],[7, 3],[9, 5],[10, 4],[11, 3],[12, 2],[13, 1],[14, 2],[15, 1],[22, 3]]
        
        
        loot = get_loot(loot_draws, 3)
        
        loot_string = ""
        for i in loot:
          loot_string = loot_string + f"+{i[0]} {itemsnames[i[1]]}\n"
          iteminventorys[gametag][i[1]] += i[0]
        
        embedVar = discord.Embed(title=f"You opened a {chestname} chest!", description=f"{loot_string}", color=0x542621)
        await ctx.send(embed=embedVar)

        iteminventorys[gametag][17] -= 1
        
				
        db["itemsofall"] = iteminventorys
      else:
        embedVar = discord.Embed(title="OH NOO!",description=f"looks like you dont have a {chestname} chest!", color=0xff0000)
        await ctx.send(embed=embedVar)
    
    if chestname == "prestige":
      pchesttheyhave = iteminventorys[gametag][21]

      if pchesttheyhave > 0:
        #itemsnames = ["commonfish", "rarefish", "epicfish", "waterbottle", "lilypad", "rock", "iron", "copper", "bronze", "stick", "log", "leaf", "apple", "banana", "ruby", "diamond"]
        itemsnames = ["<:common_fish:806986714627178496> commonfish", "<:rare_fish:806986792184184853> rarefish", "<:epic_fish:806986882449145888> epicfish", "<:water_bottle:839580961191493634> waterbottle", "<:lily_pad:839564075347869787> lilypad", "<:rock:821101496531681338> rock", "<:iron:821101561157386262> iron", "<:copper:821101604961779712> copper", "bronze", "<:wood_stick:825030799026814997> stick", "<:wood_log:825030291838992504> log", "<:leaf:839564127408095253> leaf", "<:red_apple:839564590949466172> apple", "<:banana:839581019120336987> banana", "<:ruby:839564178637324329> ruby", "<:diamond:839564238099054623> diamond", "sil chest", "golden chest", "po 1", "po 2", "potion 3 (po = potion)", "pres chest", "<:fertilizer:865256293334122506> fertilizer"]
        
        
        loot_draws = [[0, 5],[1, 4],[2, 3],[3, 2],[4, 1],[5, 5],[6, 4],[7, 3],[9, 5],[10, 4],[11, 3],[12, 2],[13, 1],[14, 2],[15, 1],[22,3]]
        
        
        loot = get_loot(loot_draws, 4)
        
        loot_string = ""
        for i in loot:
          loot_string = loot_string + f"+{i[0]} {itemsnames[i[1]]}\n"
          iteminventorys[gametag][i[1]] += i[0]
        
        embedVar = discord.Embed(title=f"You opened a {chestname} chest!", description=f"{loot_string}", color=0x542621)
        await ctx.send(embed=embedVar)

        iteminventorys[gametag][21] -= 1
        
				
        db["itemsofall"] = iteminventorys
      else:
        embedVar = discord.Embed(title="OH NOO!",description=f"looks like you dont have a {chestname} chest!", color=0xff0000)
        await ctx.send(embed=embedVar)

    #key
    #p_names = ["cooldown", "farm", "train"]
    #p_index = [18, 19, 20]
    if chestname == "cooldown":
      if iteminventorys[gametag][18] > 0:
        embedVar = discord.Embed(title=f"You used a {chestname} potion!",description=f"{ctx.author.name}, Resource Gathering cooldowns reset!", color=0xff0000)
        await ctx.send(embed=embedVar)
        
        iteminventorys[gametag][18] -= 1
        db["itemsofall"] = iteminventorys

        client.get_command('fish').reset_cooldown(ctx)
        client.get_command('mine').reset_cooldown(ctx)
        client.get_command('chop').reset_cooldown(ctx)
        

        
      else:
        embedVar = discord.Embed(title="OH NOO!",description=f"looks like you dont have a {chestname} potion!", color=0xff0000)
        await ctx.send(embed=embedVar)

    if chestname == "train":
      if iteminventorys[gametag][20] > 0:
        embedVar = discord.Embed(title=f"You used a {chestname} potion!",description=f"{ctx.author.name}, Next pet train will give more xp!", color=0xff0000)
        await ctx.send(embed=embedVar)
        
        iteminventorys[gametag][20] -= 1
        peoplecharacters[gametag][17] = 1
        db["itemsofall"] = iteminventorys
        db["charactersofall"] = peoplecharacters
        
      
      else:
        embedVar = discord.Embed(title="OH NOO!",description=f"looks like you dont have a {chestname} potion!", color=0xff0000)
        await ctx.send(embed=embedVar)

    if chestname == "farm":
      if iteminventorys[gametag][19] > 0:
        embedVar = discord.Embed(title=f"You used a {chestname} potion!",description=f"{ctx.author.name}, next farm harvest will give more loot!", color=0xff0000)
        await ctx.send(embed=embedVar)
        
        iteminventorys[gametag][19] -= 1
        peoplecharacters[gametag][17] = 2
        db["itemsofall"] = iteminventorys
        db["charactersofall"] = peoplecharacters
        

        
      else:
        embedVar = discord.Embed(title="OH NOO!",description=f"looks like you dont have a {chestname} potion!", color=0xff0000)
        await ctx.send(embed=embedVar)
      

      #index 17
@client.command()
@commands.cooldown(1, 60 * 10, commands.BucketType.user)
async def mine(ctx):
  username = ctx.author
  tempid = ctx.author.id
  if tempid in players:
    gametag = players.index(tempid)
    minelist = ["", "", ":arrow_left:"]

    if peoplecharacters[gametag][0] == "chop" and peoplecharacters[gametag][2] != "claimed":
      peoplecharacters[gametag][2] += 1
      db["charactersofall"] = peoplecharacters
 
    mineindex = 2
    minetotal = 0

    embedVar = discord.Embed(title=f"You are mining {ctx.author}", description=f"React with :pick: at full power to get more materials!\n**Power:**\n:red_square:{minelist[0]}\n:orange_square:{minelist[1]}\n:yellow_square:{minelist[2]}", color=0xA9A9A9)
    msg = await ctx.send(embed=embedVar)

    await msg.add_reaction('⛏️')

    running = True
    while running and minetotal < 9:
      try:
        reaction, user = await client.wait_for('reaction_add', timeout=1.0)
      except asyncio.TimeoutError:   
        minelist[mineindex] = ""
        mineindex -= 1
        minelist[mineindex] = ":arrow_left:"
			
        if mineindex < 0:
          mineindex = 2

        minetotal += 1
			
        embedVar = discord.Embed(title=f"You are mining {ctx.author}", description=f"React with :pick: at full power to get more materials!\n**Power:**\n:red_square:{minelist[0]}\n:orange_square:{minelist[1]}\n:yellow_square:{minelist[2]}", color=0xA9A9A9)
			
        await msg.edit(embed=embedVar)

        if minetotal > 8:
          await msg.clear_reactions()

          embedVar = discord.Embed(title=f"OH NOO!", description="You got tired of swinging your pickaxe!", color=0xff0000)
			
          await msg.edit(embed=embedVar)
      else:
        if username == user and str(reaction.emoji) == '⛏️':
          running = False

          itemsnames = ["<:common_fish:806986714627178496> commonfish", "<:rare_fish:806986792184184853> rarefish", "<:epic_fish:806986882449145888> epicfish", "<:water_bottle:839580961191493634> waterbottle", "<:lily_pad:839564075347869787> lilypad", "<:rock:821101496531681338> rock", "<:iron:821101561157386262> iron", "<:copper:821101604961779712> copper", "bronze", "<:wood_stick:825030799026814997> stick", "<:wood_log:825030291838992504> log", "<:leaf:839564127408095253> leaf", "<:red_apple:839564590949466172> apple", "<:banana:839581019120336987> banana", "<:ruby:839564178637324329> ruby", "<:diamond:839564238099054623> diamond", "sil chest", "golden chest", "po 1", "po 2", "potion 3 (po = potion)", "pres chest", "<:fertilizer:865256293334122506> fertilizer","<:dirt_pile:873278535559692298> dirt","<:sand_pile:873278153978679297> sand","<:gravel_pile:873278030246719499> gravel"]
          
          
          if mineindex == 2:
            amount = 'mineless'
          if mineindex == 1:
            amount = 'minenormal'
          if mineindex == 0:
            amount = 'dig'
          await msg.clear_reactions()
          
          loot_draws = [[0, 0],[1, 0],[2, 0],[3, 0],[4, 0],[5, 5],[6, 4],[7, 3],[9, 0],[10, 0],[11, 0],[12, 0],[13, 0],[14, 2],[15, 1],[22, 0],[23, 0],[24, 0],[25, 0]]
          loot = get_loot(loot_draws, amount)
        
          loot_string = ""
          for i in loot:
            loot_string = loot_string + f"+{i[0]} {itemsnames[i[1]]}\n"
            iteminventorys[gametag][i[1]] += i[0]
  
          db["itemsofall"] = iteminventorys






          embedVar = discord.Embed(title=f"You are done mining {username}", description=f"You got:\n{loot_string}", color=0xA9A9A9)
      

          #prestige and chest drops
            
          extra_got = []

          randomnumi = random.randint(0,99)
          randomnumin = random.randint(0,99)
            
          chest_chance = 25
          xpt = peoplecharacters[players.index(ctx.author.id)][22]
          there_level = math.floor(xpt / 3)
          if there_level >= 1:
            chest_chance = 30
            
          if randomnumi < 25:
            peoplecharacters[gametag][13] += 1
            db["charactersofall"] = peoplecharacters
            extra_got.append("+1 :low_brightness: prestige point")
          if randomnumin < chest_chance:
            iteminventorys[gametag][8] += 1
            db["itemsofall"] = iteminventorys
            extra_got.append("+1 <:bronze_chest_closed:835618525250060388> Bronze Chest")
              
          if len(extra_got) > 0:
            lineyay = ""
            for i in extra_got:
              lineyay = lineyay + i + "\n"
            embedVar.add_field(name="Extra", value=f"{lineyay}", inline=False)
            
          await msg.edit(embed=embedVar)

          chance = 5
          if random.randint(0,100) < chance:
            #spawn airdrop
            embedVar = discord.Embed(title="<a:airdrop_emoji:879392658508902410> | Airdrop", description="react with :toolbox: to claim airdrop")
    
            msg = await ctx.send(embed=embedVar)

            await msg.add_reaction('🧰')
            await asyncio.sleep(0.1)
            try:
              reaction, user = await client.wait_for('reaction_add', timeout=50.0)
            except asyncio.TimeoutError:
              embedVar = discord.Embed(title=":negative_squared_cross_mark: |Airdrop", description=f"Noone claimed the airdrop!")
              await msg.edit(embed=embedVar)
            else:
              reaction = str(reaction.emoji)
              if reaction == '🧰':
                embedVar = discord.Embed(title=":white_check_mark: |Airdrop", description=f"{user} has claimed the airdrop!")
                await msg.edit(embed=embedVar)
                await msg.clear_reactions()

                gametag = players.index(user.id)
                peoplecharacters[gametag][25][0] += 1
                db["charactersofall"] = peoplecharacters
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@mine.error
async def mine_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    timeleft = math.ceil(error.retry_after / 60)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"looks like your on a cooldown for {timeleft} minutes!\n**User: {ctx.author}**", color=0xff0000)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
  else:
    raise error

@client.command(aliases=['cd', 'cooldown'])
async def cooldowns(ctx):
  
  tempid = ctx.author.id
  gametag = players.index(tempid)



  timelist = []
  elist = []

  fishcommand = client.get_command('fish')
  cooldown1 = fishcommand.get_cooldown_retry_after(ctx)
  cooldown1 = math.ceil(cooldown1 / 60)
  timelist.append(cooldown1)
  
  minecommand = client.get_command('mine')
  cooldown2 = minecommand.get_cooldown_retry_after(ctx)
  cooldown2 = math.ceil(cooldown2 / 60)
  timelist.append(cooldown2)

  hourlycommand = client.get_command('hourly')
  cooldown3 = hourlycommand.get_cooldown_retry_after(ctx)
  cooldown3 = math.ceil(cooldown3 / 60)
  timelist.append(cooldown3)

  chopcommand = client.get_command('chop')
  cooldown4 = chopcommand.get_cooldown_retry_after(ctx)
  cooldown4 = math.ceil(cooldown4 / 60)
  timelist.append(cooldown4)

  traincommand = client.get_command('train')
  cooldown5 = traincommand.get_cooldown_retry_after(ctx)
  cooldown5 = math.ceil(cooldown5 / 60)
  timelist.append(cooldown5)

  questcommand = client.get_command('quest')
  cooldown6 = questcommand.get_cooldown_retry_after(ctx)
  cooldown6 = math.ceil(cooldown6 / 60)
  timelist.append(cooldown6)

  prestigecommand = client.get_command('prestige')
  cooldown7 = prestigecommand.get_cooldown_retry_after(ctx)
  cooldown7 = math.ceil(cooldown7 / 60)
  timelist.append(cooldown7)

  dailycommand = client.get_command('daily')
  cooldown8 = dailycommand.get_cooldown_retry_after(ctx)
  cooldown8 = math.ceil(cooldown8 / 60)
  timelist.append(cooldown8)

  arenacommand = client.get_command('arena')
  cooldown9 = arenacommand.get_cooldown_retry_after(ctx)
  cooldown9 = math.ceil(cooldown9 / 60)
  timelist.append(cooldown9)

  advcommand = client.get_command('adventure')
  cooldown10 = advcommand.get_cooldown_retry_after(ctx)
  cooldown10 = math.ceil(cooldown10 / 60)
  timelist.append(cooldown10)

  claimcommand = client.get_command('claim')
  cooldown11 = claimcommand.get_cooldown_retry_after(ctx)
  cooldown11 = math.ceil(cooldown11 / 60)
  timelist.append(cooldown11)

  digcommand = client.get_command('dig')
  cooldown12 = digcommand.get_cooldown_retry_after(ctx)
  cooldown12 = math.ceil(cooldown12 / 60)
  timelist.append(cooldown12)

  for item in timelist:
    if item == 0:
      elist.append(":ballot_box_with_check:")
    else:
      elist.append(":clock:")
  
  
  plant = peoplecharacters[gametag][15]
  farm_status = ""

  if plant == 0:
    farm_status = ":ballot_box_with_check: -- Farm (F!farm plant)"
  else:
  
    pind = peoplecharacters[gametag][15] - 1
    t_dt = peoplecharacters[gametag][16]

    planted_dt = datetime.datetime(t_dt[0], t_dt[1], t_dt[2], t_dt[3], t_dt[4], t_dt[5], t_dt[6])

    harvest_t = datetime.timedelta(minutes=planted_time[pind])

    d_utc = datetime.datetime.now(tz=pytz.UTC)
    d_est = d_utc.astimezone(pytz.timezone('US/Eastern'))

    naive_est = datetime.datetime(d_est.year, d_est.month, d_est.day, d_est.hour, d_est.minute, d_est.second, d_est.microsecond)

    done_at = planted_dt + harvest_t

    time_left = done_at - naive_est


    if naive_est > done_at:
      farm_status = ":ballot_box_with_check: -- Farm (F!farm harvest)"
    else:
      min_left = round(time_left.total_seconds() / 60, 1)

      farm_status = f":clock: -- Farm ({min_left} minutes)"

  boost_msg = ""
  boosted_hmm = check_booster(ctx)
  if boosted_hmm:
    boost_msg = f"{elist[10]} -- Claim ({cooldown11} minutes)"
    
  




  if boost_msg == "":
    embedVar = discord.Embed(title=f"{ctx.author.name}`s, Cooldowns", description=f":pick: __**Resource Gathering**__\n{elist[0]} -- Fish ({cooldown1} minutes)\n{elist[1]} -- Mine ({cooldown2} minutes)\n{elist[3]} -- Chop ({cooldown4} minutes)\n{elist[11]} -- Dig ({cooldown12} minutes)\n:inbox_tray: __**Rewards**__\n{elist[2]} -- Hourly ({cooldown3} minutes)\n{elist[7]} -- Daily ({cooldown8} minutes)\n:dizzy: __**Special**__\n{elist[4]} -- Train ({cooldown5} minutes)\n{elist[5]} -- Quest ({cooldown6} minutes)\n{elist[6]} -- Prestige ({cooldown7} minutes)\n{elist[8]} -- Arena ({cooldown9} minutes)\n{elist[9]} -- Adventure ({cooldown10} minutes)\n:seedling: __**Farm**__\n{farm_status}", color=0x0000ff)
    await ctx.send(embed=embedVar)
  else:
    embedVar = discord.Embed(title=f"{ctx.author.name}`s, Cooldowns", description=f":pick: __**Resource Gathering**__\n{elist[0]} -- Fish ({cooldown1} minutes)\n{elist[1]} -- Mine ({cooldown2} minutes)\n{elist[3]} -- Chop ({cooldown4} minutes)\n{elist[11]} -- Dig ({cooldown12} minutes)\n:inbox_tray: __**Rewards**__\n{elist[2]} -- Hourly ({cooldown3} minutes)\n{elist[7]} -- Daily ({cooldown8} minutes)\n:dizzy: __**Special**__\n{elist[4]} -- Train ({cooldown5} minutes)\n{elist[5]} -- Quest ({cooldown6} minutes)\n{elist[6]} -- Prestige ({cooldown7} minutes)\n{elist[8]} -- Arena ({cooldown9} minutes)\n{elist[9]} -- Adventure ({cooldown10} minutes)\n{boost_msg}\n:seedling: __**Farm**__\n{farm_status}", color=0x0000ff)
    await ctx.send(embed=embedVar)

@client.command()
@commands.cooldown(1, 60 * 5, commands.BucketType.user)
async def chop(ctx):
  tempid = ctx.author.id
  if tempid in players:
    gametag = players.index(tempid)
    username = ctx.author.name
    
    itemsnames = ["<:common_fish:806986714627178496> commonfish", "<:rare_fish:806986792184184853> rarefish", "<:epic_fish:806986882449145888> epicfish", "<:water_bottle:839580961191493634> waterbottle", "<:lily_pad:839564075347869787> lilypad", "<:rock:821101496531681338> rock", "<:iron:821101561157386262> iron", "<:copper:821101604961779712> copper", "bronze", "<:wood_stick:825030799026814997> stick", "<:wood_log:825030291838992504> log", "<:leaf:839564127408095253> leaf", "<:red_apple:839564590949466172> apple", "<:banana:839581019120336987> banana", "<:ruby:839564178637324329> ruby", "<:diamond:839564238099054623> diamond", "sil chest", "golden chest", "po 1", "po 2", "potion 3 (po = potion)", "pres chest", "<:fertilizer:865256293334122506> fertilizer","<:dirt_pile:873278535559692298> dirt","<:sand_pile:873278153978679297> sand","<:gravel_pile:873278030246719499> gravel"]
    
    loot_draws = [[0, 0],[1, 0],[2, 0],[3, 0],[4, 0],[5, 0],[6, 0],[7, 0],[9, 5],[10, 4],[11, 3],[12, 2],[13, 1],[14, 0],[15, 0],[22, 0],[23, 0],[24, 0],[25, 0]]
    

    if peoplecharacters[gametag][0] == "Chop" and peoplecharacters[gametag][2] != "claimed":
      peoplecharacters[gametag][2] += 1
      db["charactersofall"] = peoplecharacters

    loot = get_loot(loot_draws, 'dig')
        
    loot_string = ""
    for i in loot:
      loot_string = loot_string + f"+{i[0]} {itemsnames[i[1]]}\n"
      iteminventorys[gametag][i[1]] += i[0]
  
    db["itemsofall"] = iteminventorys

    
    
    
    embedVar = discord.Embed(title="You are done chopping!", description=f"User: {ctx.author}", color=0x0000ff)
    embedVar.add_field(name="You Got:", value=f"{loot_string}", inline=False)
  

    

    #prestige and chest drops
            
    extra_got = []

    randomnumi = random.randint(0,99)
    randomnumin = random.randint(0,99)
            
    chest_chance = 25
    xpt = peoplecharacters[players.index(ctx.author.id)][22]
    there_level = math.floor(xpt / 3)
    if there_level >= 1:
      chest_chance = 30
            
    if randomnumi < 25:
      peoplecharacters[gametag][13] += 1
      db["charactersofall"] = peoplecharacters
      extra_got.append("+1 :low_brightness: prestige point")
    if randomnumin < chest_chance:
      iteminventorys[gametag][8] += 1
      db["itemsofall"] = iteminventorys
      extra_got.append("+1 <:bronze_chest_closed:835618525250060388> Bronze Chest")
              
    if len(extra_got) > 0:
      lineyay = ""
      for i in extra_got:
        lineyay = lineyay + i + "\n"
      embedVar.add_field(name="Extra", value=f"{lineyay}", inline=False)
                 
    await ctx.send(embed=embedVar)

    chance = 5
    if random.randint(0,100) < chance:
      #spawn airdrop
      embedVar = discord.Embed(title="<a:airdrop_emoji:879392658508902410> | Airdrop", description="react with :toolbox: to claim airdrop")
    
      msg = await ctx.send(embed=embedVar)

      await msg.add_reaction('🧰')
      await asyncio.sleep(0.1)
      try:
        reaction, user = await client.wait_for('reaction_add', timeout=50.0)
      except asyncio.TimeoutError:
        embedVar = discord.Embed(title=":negative_squared_cross_mark: |Airdrop", description=f"Noone claimed the airdrop!")
        await msg.edit(embed=embedVar)
      else:
        reaction = str(reaction.emoji)
        if reaction == '🧰':
          embedVar = discord.Embed(title=":white_check_mark: |Airdrop", description=f"{user} has claimed the airdrop!")
          await msg.edit(embed=embedVar)
          await msg.clear_reactions()

          gametag = players.index(user.id)
          peoplecharacters[gametag][25][0] += 1
          db["charactersofall"] = peoplecharacters
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@chop.error
async def chop_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    timeleft = math.ceil(error.retry_after / 60)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"looks like your on a cooldown for {timeleft} minutes!\n**User: {ctx.author}**", color=0xff0000)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
  else:
    raise error

@client.command()
async def forge(ctx, part1=None):
  tempid = ctx.author.id
  if tempid in players:
    if part1 == None:
      embedVar = discord.Embed(title=f"Forge Table",  color=0x964b00)
      embedVar.add_field(name="<:wooden_raft:826156013497090098> | __Wooden Raft__", value="Materials Needed:\n12 logs\n3 sticks\nF!forge raft")
      embedVar.add_field(name="<:submarine:860258291116408852> | __Submarine__", value="Materials Needed:\nNot craftable at the moment")
      embedVar.add_field(name=":clock: | __Old Clock__", value="Materials Needed:\nNot craftable at the moment")
      embedVar.add_field(name=":beginner: | __Royal Shield__", value="Materials Needed:\nNot craftable at the moment")

      await ctx.send(embed=embedVar)
    elif part1 == 'raft':
      tempid = ctx.author.id
      gametag = players.index(tempid)

      woodtheyhave = iteminventorys[gametag][10]
      sticktheyhave = iteminventorys[gametag][9]

      if woodtheyhave >= 12 and sticktheyhave >= 3:
        peoplecharacters[gametag][12] = 1
        iteminventorys[gametag][10] -= 12
        iteminventorys[gametag][9] -= 3

        await ctx.send("You have forged a **wooden raft**, it has been auto-equiped.")
        db["itemsofall"] = iteminventorys
        db["charactersofall"] = peoplecharacters
      else:
        await ctx.send(f"You are trying to forge a **wooden raft** for 12 logs and 3 sticks but you only have {woodtheyhave} logs and {sticktheyhave} sticks!")
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@client.command()
@commands.cooldown(1, 60 * 90, commands.BucketType.user)
async def train(ctx):
  tempid = ctx.author.id
  if tempid in players:
    gametag = players.index(tempid)
    emoji = petsemojis[peoplecharacters[gametag][10] - 1]
    ind = peoplecharacters[gametag][10]
    petxp = peoplecharacters[gametag][5]

    if petxp < 5:
      if ind == 5:
    
        itemnames = ["rock", "iron", "copper", "stick", "log"]
        itemindex = [5, 6, 7, 9, 10]
        itemgot = random.choice(itemnames)
        itemnum = itemnames.index(itemgot)
        itemdigit = itemindex[itemnum]
        amount = random.randint(1, 3)

        embedVar = discord.Embed(title=f"<:train_icon:859812981651275797> | Pet Train", description=f"You have trained your {emoji}!\nWhile your :monkey: was training he collected {amount} {itemgot}\nYour pet got 1 xp", color=0x5c4141)
    
        
        iteminventorys[gametag][itemdigit] += amount
        db["itemsofall"] = iteminventorys

      else:
        embedVar = discord.Embed(title=f"<:train_icon:859812981651275797> | Pet Train", description=f"You have trained your {emoji}!\nYour pet got 1 xp", color=0x5c4141)

      
      if peoplecharacters[gametag][17] == 1:
        peoplecharacters[gametag][5] += 2
        peoplecharacters[gametag][17] = 0
        db["charactersofall"] = peoplecharacters
        embedVar.add_field(name="Train Potion", value="Because of your train potion, your pet got 2 xp in total!")
      else:
        peoplecharacters[gametag][5] += 1
        db["charactersofall"] = peoplecharacters


      peoplecharacters[gametag][25][3] += 50
      db["charactersofall"] = peoplecharacters
      embedVar.add_field(name="Halloween Event", value="Your pet found 50 candy :candy: while training!", inline=False)
      await ctx.send(embed=embedVar)



    else:
      ctx.command.reset_cooldown(ctx)
      await ctx.send("Your pet has 5/5 exp use F!upgrade to upgrade your pet!")

@train.error
async def train_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    timeleft = math.ceil(error.retry_after / 60)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"looks like your on a cooldown for {timeleft} minutes!\n**User: {ctx.author}**", color=0xff0000)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
  else:
    raise error

@client.command()
async def pet(ctx, action = None, action2 = None):
  
  tempid = ctx.author.id
  gametag = players.index(tempid)
  ind = peoplecharacters[gametag][10]
  emoji = petsemojis[ind - 1]
  moneytheyhave = moneybags[gametag]
  tempquote = random.choice(petquotestosay[ind - 1])
  petlevel = peoplecharacters[gametag][4]
  effectofpet = peteffects[ind - 1]
  amountincrease = (petamounts[ind - 1] / 2) * (petlevel + 2)

  amountincrease = math.ceil(amountincrease)

  if action == None and action2 == None:
    
    
    

    e1 = "<:exp_bar_full:831276964181573643>"
    e2 = "<:exp_bar_empty:831277316859756564>"
    
    expbar = [e2, e2, e2, e2, e2]

    if peoplecharacters[gametag][5] >= 1:
      expbar[0] = e1
    if peoplecharacters[gametag][5] >= 2:
      expbar[1] = e1
    if peoplecharacters[gametag][5] >= 3:
      expbar[2] = e1
    if peoplecharacters[gametag][5] >= 4:
      expbar[3] = e1
    if peoplecharacters[gametag][5] >= 5:
      expbar[4] = e1


    embedVar = discord.Embed(title=f"{ctx.author.name}`s {emoji}", description=f":speech_balloon: {tempquote}\nEXP: {expbar[0]}{expbar[1]}{expbar[2]}{expbar[3]}{expbar[4]}\nLevel: {petlevel} **|** {(petlevel + 1) * 50} coins to upgrade\nEffects: {effectofpet} {amountincrease})", color=0x5c4141)
    embedVar.set_footer(text="Equip a pet with F!pet equip <pet_name>")
    await ctx.send(embed=embedVar)

  if action == 'equip' and action2 == 'dragon' and 2 in peoplecharacters[gametag][11]:
    await ctx.send("You have equiped your dragon, xp and level were reset!")
    peoplecharacters[gametag][10] = 2
    peoplecharacters[gametag][4] = 0
    peoplecharacters[gametag][5] = 0
    db["charactersofall"] = peoplecharacters

  if action == 'equip' and action2 == 'octopus' and 3 in peoplecharacters[gametag][11]:
    await ctx.send("You have equiped your octopus, xp and level were reset!")
    peoplecharacters[gametag][10] = 3
    peoplecharacters[gametag][4] = 0
    peoplecharacters[gametag][5] = 0
    db["charactersofall"] = peoplecharacters
  
  if action == 'equip' and action2 == 'eagle' and 4 in peoplecharacters[gametag][11]:
    await ctx.send("You have equiped your eagle, xp and level were reset!")
    peoplecharacters[gametag][10] = 4
    peoplecharacters[gametag][4] = 0
    peoplecharacters[gametag][5] = 0
    db["charactersofall"] = peoplecharacters

  if action == 'equip' and action2 == 'monkey' and 5 in peoplecharacters[gametag][11]:
    await ctx.send("You have equiped your monkey, xp and level were reset!")
    peoplecharacters[gametag][10] = 5
    peoplecharacters[gametag][4] = 0
    peoplecharacters[gametag][5] = 0
    db["charactersofall"] = peoplecharacters
  
  if action == 'equip' and action2 == 'cat' and 1 in peoplecharacters[gametag][11]:
    await ctx.send("You have equiped your cat, xp and level were reset!")
    peoplecharacters[gametag][10] = 1
    peoplecharacters[gametag][4] = 0
    peoplecharacters[gametag][5] = 0
    db["charactersofall"] = peoplecharacters

  if action == 'equip' and action2 == 'bug' and 6 in peoplecharacters[gametag][11]:
    await ctx.send("You have equiped your bug, xp and level were reset!")
    peoplecharacters[gametag][10] = 1
    peoplecharacters[gametag][4] = 0
    peoplecharacters[gametag][5] = 0
    db["charactersofall"] = peoplecharacters
  if action == 'collection' and action2 == None:
    c_pet_list = peoplecharacters[gametag][11]
    c_pet_amount = len(c_pet_list)

    pets_emojis_a_name = [':cat2: Cat', ':dragon: Dragon', ':octopus: Octopus', ':eagle: Eagle', ':monkey: Monkey', ':bug: Bug']

    group_list = []
  
    search = 0
    count = 0
    got = 0
    for thingy in range(26):
      for i in c_pet_list:
        if i == search:
          got += 1
        count += 1
    
      if got > 0:
        group_list.append([got, search])
      count = 0
      got = 0
      search += 1
    
    string = ""
    for index in group_list:
      string = string + str(index[0]) + " " + pets_emojis_a_name[index[1] - 1] + "\n"

    embedVar = discord.Embed(title="Pet Collection", description=f"User: {ctx.author}", color=0x0000ff)
    embedVar.add_field(name=f"{c_pet_amount} Pets", value=f"{string}", inline=False)
    await ctx.send(embed=embedVar)


@client.command()
async def upgrade(ctx):
  tempid = ctx.author.id

  if tempid in players:
    gametag = players.index(tempid)
    moneytheyhave = moneybags[gametag]
    petxp = peoplecharacters[gametag][5]
    petlevel = peoplecharacters[gametag][4]

    emoji = petsemojis[peoplecharacters[gametag][10] - 1]

    if petxp >= 5 and moneytheyhave >= (petlevel + 1) * 50:
      await ctx.send(f">>> you have upgraded your {emoji}")
      
      moneybags[gametag] -= (petlevel + 1) * 50
      
      peoplecharacters[gametag][4] += 1
      peoplecharacters[gametag][5] = 0
      
      db["charactersofall"] = peoplecharacters
      db["moneybagsofall"] = moneybags
    else:
      await ctx.send(f">>> Your {emoji} must have 5 or more xp and you must have enough coins to upgrade your {emoji}")
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@client.command(aliases=['quests', 'q'])
@commands.cooldown(1, 3600 * 24, commands.BucketType.user)
async def quest(ctx):
  tempid = ctx.author.id
  useravatar = ctx.author.avatar_url

  if tempid in players:
    possiblequest = ["Fish", "Chop", "Mine"]
    questgot = random.choice(possiblequest)
    amount = random.randint(3, 5)
    rewardofquest = amount * 3

    gametag = players.index(tempid)

    peoplecharacters[gametag][0] = questgot
    peoplecharacters[gametag][1] = amount
    peoplecharacters[gametag][2] = 0
    peoplecharacters[gametag][3] = rewardofquest
    db["charactersofall"] = peoplecharacters

    embedVar = discord.Embed(title="New quest!", description=f"{questgot} 0/{amount} times\nReward: {rewardofquest} coins!", color=0xff0000)
    embedVar.set_footer(icon_url=useravatar, text="Quest will reset in 24 hours!")
    await ctx.send(embed=embedVar)
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@quest.error
async def quest_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):

    timeleft = math.ceil(error.retry_after / 60)
    tempid = ctx.author.id
    useravatar = ctx.author.avatar_url
    gametag = players.index(tempid)

    questgot = peoplecharacters[gametag][0]
    amount = peoplecharacters[gametag][1]
    amountdone = peoplecharacters[gametag][2]
    rewardofquest = peoplecharacters[gametag][3]

  if amountdone != "claimed":
    if amountdone >= amount:
      peoplecharacters[gametag][2] = "claimed"
      amountdone = "claimed"
      moneybags[gametag] += rewardofquest
      db["charactersofall"] = peoplecharacters
      db["moneybagsofall"] = moneybags

    embedVar = discord.Embed(title="Your quest!", description=f"{questgot} {amountdone}/{amount} times\nReward: {rewardofquest} coins", color=0xff0000)
    embedVar.set_footer(icon_url=useravatar, text=f"Quest will reset in {timeleft} minutes")
    await ctx.send(embed=embedVar)
  else:
    raise error

def get_space(data, num):
  if num == 1 or num == 2:
    len_count = 0
    for i in data:
      len_count += len(str(i))
    return len_count
  else:
    if num == 3 or num == 4:
      len_count = 0
      for i in data:
        for i2 in i:
          len_count += len(str(i2))
      return len_count

@client.command()
async def data(ctx, user : discord.Member = None):
  #players
  #moneybags
  #iteminventorys
  #peoplecharacters
  if user == None:
    total1 = get_space(players, 1)
    total2 = get_space(moneybags, 2)
    total3 = get_space(iteminventorys, 3)
    total4 = get_space(peoplecharacters, 4)
  
    total = total1 + total2 + total3 + total4
    total = round(total * 0.0008 * 1.7, 2)

    embedVar = discord.Embed(title="Data Help", description=f"Some usefull information", color=0xff0000)
    embedVar.add_field(name="Explicit Latency", value=f"*{round(client.latency, 10)} seconds*")
    embedVar.add_field(name="Memory Storage", value=f"*{total}/500 MB*")
    await ctx.send(embed=embedVar)
  else:
    gametag2 = players.index(user.id)


    embedVar = discord.Embed(title=f"{user} Data ({gametag2})", description=f"Raw Json:\n```\n(data_1; '{peoplecharacters[players.index(user.id)]}')\n(data_2; '{moneybags[players.index(user.id)]}')\n(data_3; '{iteminventorys[players.index(user.id)]}')\n```", color=0xff0000)
    await ctx.send(embed=embedVar)
  #if action == '1':
    #await ctx.send(peoplecharacters[7])
  #if action == '2':
    #await ctx.send(players)
  #if action == '3':
    #await ctx.send(moneybags)
  #if action == '4':
    #await ctx.send(iteminventorys)

@client.command()
async def coinflip(ctx, amount: int):
  tempid = ctx.author.id

  if tempid in players:
    gametag = players.index(tempid)
    moneytheyhave = moneybags[gametag]
    if amount <= moneytheyhave and amount >= 0:
      embedVar = discord.Embed(title=":coin: | Coin Flip", description=f"You are betting {amount} coins, chose :yellow_circle: or :orange_circle:!", color=0xffff00)
      msg = await ctx.send(embed=embedVar)
      possibleflips = ['🟠', '🟡']
      choice = random.choice(possibleflips)

      await msg.add_reaction('🟠')
      await msg.add_reaction('🟡')
      done = False
      while not done:
        try:
          reaction, user = await client.wait_for('reaction_add', timeout=20.0)
        except asyncio.TimeoutError:
          embedVar = discord.Embed(title=":coin: | Coin Flip", description=f"Cancelled coinflip due to timeout", color=0xffff00)
          await msg.edit(embed=embedVar)
          done = True
        else:
          if str(reaction.emoji) == choice and tempid == user.id:
            embedVar = discord.Embed(title=":coin: | Coin Flip", description=f"You won {amount} coins", color=0xffff00)

            xpt = peoplecharacters[players.index(ctx.author.id)][22]
            there_level = math.floor(xpt / 3)
            if there_level >= 2:
              bonus_coins = round(amount / 100 * 15)

              embedVar.add_field(name="**<:upvote_emoji:867114498173960202> **|** Vote Bonus**",value=f"You also got {bonus_coins} coins", inline=False)
              moneybags[gametag] += bonus_coins







            await msg.edit(embed=embedVar)
            moneybags[gametag] += amount
            db["moneybagsofall"] = moneybags
            done = True
          elif str(reaction.emoji) != choice and tempid == user.id:
            embedVar = discord.Embed(title=":coin: | Coin Flip", description=f"You lost {amount} coins", color=0xffff00)
            await msg.edit(embed=embedVar)
            moneybags[gametag] -= amount
            db["moneybagsofall"] = moneybags
            done = True
    else:
      embedVar = discord.Embed(title=":coin: | Coin Flip", description=f"You are trying to bet {amount} coins but you only have {moneytheyhave} coins!", color=0xff0000)
      await ctx.send(embed=embedVar)
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@client.command()
async def choose(ctx, *args):
  words = args[0:]
  wordlist = []
  for i in words:
    wordlist.append(i)

  await ctx.send(f"I picked {random.choice(wordlist)}!")

@client.command()
async def trade(ctx, action = None):
  if action == 'create':
    
    userid = ctx.author.id
    
    geti = 0
    givei = 3
    

    tempamount = [0, 0, 0, 0, 0, 0]
    tempitem = ["none", "none", "none", "none", "none", "none"]
    tempindexofitems = [0, 0, 0, 0, 0, 0]

    embedVar = discord.Embed(title=f"{ctx.author.name}`s Trade Template", description="Type **add get (amount) (item), add give (amount) (item), del (give / get)** to add and remove items in this trade. Type **confirm** to finish trade and **exit** to cancel this trade.", color=0xff0000)

    embedVar.add_field(name="Getting:", value=f":one: **|** {tempamount[0]} {tempitem[0]}\n:two: **|** {tempamount[1]} {tempitem[1]}\n:three: **|** {tempamount[2]} {tempitem[2]}", inline=False)
    embedVar.add_field(name="Giving:", value=f":four: **|** {tempamount[3]} {tempitem[3]}\n:five: **|** {tempamount[4]} {tempitem[4]}\n:six: **|** {tempamount[5]} {tempitem[5]}", inline=False)
    
    msg = await ctx.send(embed=embedVar)

    done = False
    while not done:
      try:
        response = await client.wait_for('message', timeout=30.0)
      except asyncio.TimeoutError:
        await ctx.send("Trade canceled due to timeout!")
        done = True
      else:
        if response.author.id == userid:

          wordstheysaid = response.content.split()
          itemtheysay = wordstheysaid[-1]
          

          if response.content.startswith('add get') and itemtheysay in correctitems and geti < 3:
            
            tempindex1 = correctitems.index(itemtheysay)
            tempindex = indexofcorrectitems[tempindex1]

            amountofitem = int(wordstheysaid[-2])
            tempamount[geti] = amountofitem
            tempitem[geti] = itemtheysay
            tempindexofitems[geti] = tempindex
            geti += 1
              
            embedVar = discord.Embed(title=f"{ctx.author.name}`s Trade Template", description="Type **add get (amount) (item), add give (amount) (item), del (give / get)** to add and remove items in this trade. Type **confirm** to finish trade and **exit** to cancel this trade.", color=0xff0000)

            embedVar.add_field(name="Getting:", value=f":one: **|** {tempamount[0]} {tempitem[0]}\n:two: **|** {tempamount[1]} {tempitem[1]}\n:three: **|** {tempamount[2]} {tempitem[2]}", inline=False)
            embedVar.add_field(name="Giving:", value=f":four: **|** {tempamount[3]} {tempitem[3]}\n:five: **|** {tempamount[4]} {tempitem[4]}\n:six: **|** {tempamount[5]} {tempitem[5]}", inline=False)
          

            await msg.edit(embed=embedVar)
          if response.content.startswith('add give') and itemtheysay in correctitems and givei < 6:
            

            tempindex1 = correctitems.index(itemtheysay)
            tempindex = indexofcorrectitems[tempindex1]

            amountofitem = int(wordstheysaid[-2])
            tempamount[givei] = amountofitem
            tempitem[givei] = itemtheysay
            tempindexofitems[givei] = tempindex
            givei += 1
              
            embedVar = discord.Embed(title=f"{ctx.author.name}`s Trade Template", description="Type **add get (amount) (item), add give (amount) (item), del (give / get)** to add and remove items in this trade. Type **confirm** to finish trade and **exit** to cancel this trade.", color=0xff0000)

            embedVar.add_field(name="Getting:", value=f":one: **|** {tempamount[0]} {tempitem[0]}\n:two: **|** {tempamount[1]} {tempitem[1]}\n:three: **|** {tempamount[2]} {tempitem[2]}", inline=False)
            embedVar.add_field(name="Giving:", value=f":four: **|** {tempamount[3]} {tempitem[3]}\n:five: **|** {tempamount[4]} {tempitem[4]}\n:six: **|** {tempamount[5]} {tempitem[5]}", inline=False)
          

            await msg.edit(embed=embedVar)
          if response.content.startswith('del') and itemtheysay == 'give' and givei > 3:
            
            
            givei -= 1
            
            tempamount[givei] = 0
            tempitem[givei] = "none"
            tempindexofitems[givei] = 0
            

            

            embedVar = discord.Embed(title=f"{ctx.author.name}`s Trade Template", description="Type **add get (amount) (item), add give (amount) (item), del (give / get)** to add and remove items in this trade. Type **confirm** to finish trade and **exit** to cancel this trade.", color=0xff0000)

            embedVar.add_field(name="Getting:", value=f":one: **|** {tempamount[0]} {tempitem[0]}\n:two: **|** {tempamount[1]} {tempitem[1]}\n:three: **|** {tempamount[2]} {tempitem[2]}", inline=False)
            embedVar.add_field(name="Giving:", value=f":four: **|** {tempamount[3]} {tempitem[3]}\n:five: **|** {tempamount[4]} {tempitem[4]}\n:six: **|** {tempamount[5]} {tempitem[5]}", inline=False)
          

            await msg.edit(embed=embedVar)
          if response.content.startswith('del') and itemtheysay == 'get' and geti > 0:
            
            geti -= 1
            tempamount[geti] = 0
            tempitem[geti] = "none"
            tempindexofitems[geti] = 0

            embedVar = discord.Embed(title=f"{ctx.author.name}`s Trade Template", description="Type **add get (amount) (item), add give (amount) (item), del (give / get)** to add and remove items in this trade. Type **confirm** to finish trade and **exit** to cancel this trade.", color=0xff0000)
            embedVar.add_field(name="Getting:", value=f":one: **|** {tempamount[0]} {tempitem[0]}\n:two: **|** {tempamount[1]} {tempitem[1]}\n:three: **|** {tempamount[2]} {tempitem[2]}", inline=False)
            embedVar.add_field(name="Giving:", value=f":four: **|** {tempamount[3]} {tempitem[3]}\n:five: **|** {tempamount[4]} {tempitem[4]}\n:six: **|** {tempamount[5]} {tempitem[5]}", inline=False)
            await msg.edit(embed=embedVar)
          if response.content.startswith('exit'):
            done = True
            embedVar = discord.Embed(title=f"{ctx.author.name}`s Trade Template", description="Trade exited.", color=0xff0000)
            await msg.edit(embed=embedVar)
          if response.content.startswith('confirm'):
            done = True
            embedVar = discord.Embed(title=f"{ctx.author.name}`s Trade Template", description=f"Trade confirmed it is now in the trade market!", color=0xff0000)

            everytrade.append([userid, tempamount, tempitem, tempindexofitems])
            
            await msg.edit(embed=embedVar)
  if action == 'market' and len(everytrade) >= 1:
    page = 0
    
    userid = ctx.author.id
    tradeusernameone = await client.fetch_user(everytrade[page][0])
    
    embedVar = discord.Embed(title=f"{tradeusernameone} Trade!", description=f"Trade {page + 1}", color=0xff4f4f)
    
    embedVar.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqz4fdmJ9Oeq22jxCzXitD9J_lKRAzdfmaxw&usqp=CAU")

    

    embedVar.add_field(name=f"giving: {everytrade[page][1][0]} {everytrade[page][2][0]}, {everytrade[page][1][1]} {everytrade[page][2][1]}, {everytrade[page][1][2]} {everytrade[page][2][2]}\ngetting: {everytrade[page][1][3]} {everytrade[page][2][3]}, {everytrade[page][1][4]} {everytrade[page][2][4]}, {everytrade[page][1][5]} {everytrade[page][2][5]}", value=f"React with :stop_button: to accept trade", inline=False)

    msg = await ctx.send(embed=embedVar)
    
    await msg.add_reaction('⬅️')
    await msg.add_reaction('⏹️')
    await msg.add_reaction('➡️')

    done = False
    
    while not done:
      try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0)
      except asyncio.TimeoutError:
        await ctx.send("closed market due to timeout")
        done = True
      else:
        if user.id == userid and str(reaction.emoji) == '⬅️' and page > 0:
          page -= 1
          
          tradeusernameone = await client.fetch_user(everytrade[page][0])
          embedVar = discord.Embed(title=f"{tradeusernameone} Trade!", description=f"Trade {page + 1}", color=0xff4f4f)
    
          embedVar.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqz4fdmJ9Oeq22jxCzXitD9J_lKRAzdfmaxw&usqp=CAU")

          embedVar.add_field(name=f"giving: {everytrade[page][1][0]} {everytrade[page][2][0]}, {everytrade[page][1][1]} {everytrade[page][2][1]}, {everytrade[page][1][2]} {everytrade[page][2][2]}\ngetting: {everytrade[page][1][3]} {everytrade[page][2][3]}, {everytrade[page][2][4]} {everytrade[page][1][4]}, {everytrade[page][1][5]} {everytrade[page][2][5]}", value=f"React with :stop_button: to accept trade", inline=False)

          await msg.edit(embed=embedVar)

        if user.id == userid and str(reaction.emoji) == '➡️' and page < len(everytrade) - 1:
          page += 1
          tradeusernameone = await client.fetch_user(everytrade[page][0])
          embedVar = discord.Embed(title=f"{tradeusernameone} Trade!", description=f"Trade {page + 1}", color=0xff4f4f)
    
          embedVar.set_thumbnail(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSqz4fdmJ9Oeq22jxCzXitD9J_lKRAzdfmaxw&usqp=CAU")

          embedVar.add_field(name=f"giving: {everytrade[page][1][0]} {everytrade[page][2][0]}, {everytrade[page][1][1]} {everytrade[page][2][1]}, {everytrade[page][1][2]} {everytrade[page][2][2]}\ngetting: {everytrade[page][1][3]} {everytrade[page][2][3]}, {everytrade[page][2][4]} {everytrade[page][1][4]}, {everytrade[page][1][5]} {everytrade[page][2][5]}", value=f"React with :stop_button: to accept trade", inline=False)

          await msg.edit(embed=embedVar)

        if user.id == userid and str(reaction.emoji) == '⏹️':
          
          done = True

          thelisttotest = []

          inde = -1
          for every in everytrade[page][2]:
            inde += 1
            if every != 'none' and inde < 3:

              tag1 = players.index(userid)
              tag2 = players.index(everytrade[page][0])

              getitem = everytrade[page][3][inde]
              amount = everytrade[page][1][inde]
              thelisttotest.append(getitem)

              iteminventorys[tag1][getitem] -= amount
              
              iteminventorys[tag2][getitem] += amount
            elif every != 'none':
              tag1 = players.index(userid)
              tag2 = players.index(everytrade[page][0])

              giveitem = everytrade[page][3][inde]
              amount = everytrade[page][1][inde]
              thelisttotest.append(giveitem)

              iteminventorys[tag1][giveitem] += amount
              iteminventorys[tag2][giveitem] -= amount
              
         
              

          
          
          everytrade.pop(page)
          db["itemsofall"] = iteminventorys

          embedVar = discord.Embed(title="YAY!", description=f"This trade has been accepted!", color=0xff0000)

          await msg.edit(embed=embedVar)
  elif action == 'market':
    await ctx.send("there are no trades in the trade market! create one with F!trade create")

  if action == None:
    embedVar = discord.Embed(title="Wrong Usage!", description=f"This command takes 1 argument!\nF!trade market - used to view trades created by other people!\nF!trade create - create your own trade, when done it will appear in the Trade Market", color=0xff0000)
    await ctx.send(embed=embedVar)


@client.command()
async def trade123(ctx):
  embedVar = discord.Embed(title=f"{ctx.author.name}`s Trade Template", description="Type **add get, add give, del (index)** to add and remove items in this trade. Type **confirm** to finish trade and **exit** to cancel this trade.", color=0xff0000)
  embedVar.add_field(name="Giving:", value=f"None **|** Add some items with **add give**", inline=False)
  embedVar.add_field(name="Getting:", value=f"None **|** Add some items with **add get**", inline=False)
  msg = await ctx.send(embed=embedVar)

@client.command()
async def cups(ctx, amount : int):
  tempid = ctx.author.id
  if tempid in players:
    gametag = players.index(tempid)
    moneytheyhave = moneybags[gametag]
    if amount <= moneytheyhave and amount >= 0:

      e1 = ":cup_with_straw:"

      embedVar = discord.Embed(title=f"{e1} | Cups Command", description=f"You are betting {amount} coins\n*Pick a cup*\n{e1} | {e1} | {e1}\n:one: | :two: | :three:", color=0xffff00)
      

      msg = await ctx.send(embed=embedVar)


      await msg.add_reaction('1️⃣')
      await msg.add_reaction('2️⃣')
      await msg.add_reaction('3️⃣')

      possiblechoices = ['1️⃣', '2️⃣', '3️⃣']
      choice = random.choice(possiblechoices)

      done = False
      while not done:
        try:
          reaction, user = await client.wait_for('reaction_add', timeout=20.0)
        except asyncio.TimeoutError:
          embedVar = discord.Embed(title="OH NOO", description="Cancelled betting due to timeout!", color=0xff0000)
          await msg.edit(embed=embedVar)
          done = True
        else:
          if str(reaction.emoji) == choice and tempid == user.id:
            embedVar = discord.Embed(title=f"{e1} | Cups Command", description=f"You won {amount} coins!", color=0xffff00)
            

            xpt = peoplecharacters[players.index(ctx.author.id)][22]
            there_level = math.floor(xpt / 3)
            if there_level >= 2:
              bonus_coins = round(amount / 100 * 15)

              embedVar.add_field(name="**<:upvote_emoji:867114498173960202> **|** Vote Bonus**",value=f"You also got {bonus_coins} coins", inline=False)
              moneybags[gametag] += bonus_coins


            await msg.edit(embed=embedVar)
            moneybags[gametag] += amount
            db["moneybagsofall"] = moneybags
            done = True
          elif str(reaction.emoji) != choice and tempid == user.id:
            embedVar = discord.Embed(title=f"{e1} | Cups Command", description=f"You lost {amount} coins!", color=0xffff00)
            await msg.edit(embed=embedVar)
            
            moneybags[gametag] -= amount
            db["moneybagsofall"] = moneybags
            done = True
    else:
      embedVar = discord.Embed(title="OH NOO", description=f"You are trying to bet {amount} coins, but you only have {moneytheyhave} coins!", color=0xff0000)
      await ctx.send(embed=embedVar)
      
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)


@client.command()
@commands.cooldown(1, 60 * 60 * 18, commands.BucketType.user)
async def adventure(ctx):
  userid = ctx.author.id
  gametag = players.index(userid)
# 0 = grass
# 1 = water
# 2 = character
  if peoplecharacters[gametag][12] == 1:

    emoji_w_b = "<:blue_sea_square:826157113427755019>"
    emoji_r_w = "<:wooden_raft:826156013497090098>"
     
    interactive_box = "Raft - Come back from the adventure"
    got_chest = False
    quest_box = ":small_orange_diamond: Find the treasure and collect it"
    
    embedVar = discord.Embed(title="Off You Go!", description=f"{emoji_w_b}{emoji_w_b}{emoji_w_b}\n{emoji_w_b}{emoji_r_w}{emoji_w_b}\n{emoji_w_b}{emoji_w_b}{emoji_w_b}", color=0xff0000)
    embedVar.add_field(name="Controls", value="These controls are when You arive at the island!\nReact with :arrow_left::arrow_down_small::arrow_left::arrow_up_small: to move\nReact with :boom: to interact\n:compass: **|** Arrival Time: 10 seconds")
    embedVar.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author.name}'s Adventure!")
    msg = await ctx.send(embed=embedVar)

    map_list = [[1,1,1,1,1,1,1,1,1,1],[1,0,0,4,0,1,1,1,1,1],[1,0,0,0,3,0,0,0,4,1,1],[1,0,0,0,0,6,0,0,0,1],[1,0,0,0,0,0,0,0,0,1],[1,0,0,3,0,0,0,0,0,1,1],[1,0,0,3,0,0,0,0,0,1,1],[1,0,4,0,0,0,1,1,1,1],[1,0,0,0,0,1,1,1,1,1],[1,2,0,0,1,1,1,1,1,1],[1,5,1,1,1,1,1,1,1,1]]

    emoji = ['<:grass_square:828642184659992618>','<:sea_blue:826156139023695873>','<:rusty_knight_grass:828649870952235039>','<:tree_grass:844919952368730174>', '<:rock_grass:844920762624245803>', '<:wooden_raft:826156013497090098>', '<:chest_grass:861680600997953557>']
  
    map_to_show = render(map_list, emoji)

    s1 = map_to_show[0][0]
    s2 = map_to_show[0][1]
    s3 = map_to_show[0][2]
    s4 = map_to_show[1][0] 
    s5 = map_to_show[1][1]
    s6 = map_to_show[1][2] 
    s7 = map_to_show[2][0] 
    s8 = map_to_show[2][1] 
    s9 = map_to_show[2][2] 

    await asyncio.sleep(10)

    embedVar = discord.Embed(title="The Adventure Begins!", description=f"{s1}{s2}{s3}\n{s4}{s5}{s6}\n{s7}{s8}{s9}", color=0xff0000)
    embedVar.add_field(name=":scroll: | Quests", value=f"{quest_box}\nWhen done come back to your raft and interact with it")
    embedVar.add_field(name=":boom: | Interactive", value=f"```\n{interactive_box}\n```")
    embedVar.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author.name}'s Adventure!")
    await msg.edit(embed=embedVar)

   

    await msg.add_reaction('⬅️')
    await msg.add_reaction('➡️')
    await msg.add_reaction('🔼')
    await msg.add_reaction('🔽')
    await msg.add_reaction('💥')

    done = False
    no_edit = False
    while not done:
      try:
        reaction, user = await client.wait_for('reaction_add', timeout=30.0)
      except asyncio.TimeoutError:
        done = True
        embedVar = discord.Embed(title="OH NOO!", description=f"Cancelled adventure due to timeout!", color=0xff0000)
        await msg.edit(embed=embedVar)
      else:
        if str(reaction.emoji) == '🔼' and user.id == userid:
  
          updated_map = move_character(map_list, "up")
          map_list = updated_map
  
          map_to_show = render(map_list, emoji)

          s1 = map_to_show[0][0]
          s2 = map_to_show[0][1]
          s3 = map_to_show[0][2]
          s4 = map_to_show[1][0] 
          s5 = map_to_show[1][1]
          s6 = map_to_show[1][2] 
          s7 = map_to_show[2][0] 
          s8 = map_to_show[2][1] 
          s9 = map_to_show[2][2] 
          
          
      
        if str(reaction.emoji) == '🔽' and user.id == userid:
  
          updated_map = move_character(map_list, "down")
          map_list = updated_map
  
          map_to_show = render(map_list, emoji)

          s1 = map_to_show[0][0]
          s2 = map_to_show[0][1]
          s3 = map_to_show[0][2]
          s4 = map_to_show[1][0] 
          s5 = map_to_show[1][1]
          s6 = map_to_show[1][2] 
          s7 = map_to_show[2][0] 
          s8 = map_to_show[2][1] 
          s9 = map_to_show[2][2] 
          
          

        if str(reaction.emoji) == '⬅️' and user.id == userid:
  
          updated_map = move_character(map_list, "left")
          map_list = updated_map
  
          map_to_show = render(map_list, emoji)

          s1 = map_to_show[0][0]
          s2 = map_to_show[0][1]
          s3 = map_to_show[0][2]
          s4 = map_to_show[1][0] 
          s5 = map_to_show[1][1]
          s6 = map_to_show[1][2] 
          s7 = map_to_show[2][0] 
          s8 = map_to_show[2][1] 
          s9 = map_to_show[2][2] 
          
          

        if str(reaction.emoji) == '➡️' and user.id == userid:
  
          updated_map = move_character(map_list, "right")
          map_list = updated_map
  
          map_to_show = render(map_list, emoji)

          s1 = map_to_show[0][0]
          s2 = map_to_show[0][1]
          s3 = map_to_show[0][2]
          s4 = map_to_show[1][0] 
          s5 = map_to_show[1][1]
          s6 = map_to_show[1][2] 
          s7 = map_to_show[2][0] 
          s8 = map_to_show[2][1] 
          s9 = map_to_show[2][2] 
          
          

        current_pos_o_c = find_character(map_list)
        if current_pos_o_c == [1, 9] or current_pos_o_c == [2, 9]:
          interactive_box = "Raft - Come back from the adventure"
        else:
          interactive_box = "none"
        
        if current_pos_o_c == [5, 3]:
          got_chest = True
          quest_box = ":small_blue_diamond: Find the treasure and collect it"

        if str(reaction.emoji) == '💥' and user.id == userid and interactive_box == "Raft - Come back from the adventure":
          no_edit = True
          if got_chest == True:
            embedVar = discord.Embed(title="YAY!", description=f"You have completed your quest and came back!", color=0xff0000)
            
            peoplecharacters[gametag][20] == 1
            db["charactersofall"] = peoplecharacters
            done = True
          else:
            embedVar = discord.Embed(title="OH NOO!", description=f"You did not complete your quest, but you decided to come back!", color=0xff0000)
            done = True
          await msg.edit(embed=embedVar)
        
        if no_edit != True:
          embedVar = discord.Embed(title="The Adventure Begins!", description=f"{s1}{s2}{s3}\n{s4}{s5}{s6}\n{s7}{s8}{s9}", color=0xff0000)
          embedVar.add_field(name=":scroll: | Quests", value=f"{quest_box}\nWhen done come back to your raft and interact with it")
          embedVar.add_field(name=":boom: | Interactive", value=f"```\n{interactive_box}\n```")
          embedVar.set_footer(icon_url=ctx.author.avatar_url, text=f"{ctx.author.name}'s Adventure!")
          await msg.edit(embed=embedVar)
        #await ctx.send(f"{find_character(map_list)}")

  else:
    embedVar = discord.Embed(title="OH NOO!", description="Looks like you cant go on a adventure because you need a travel unit! Forge a wooden raft with F!forge")
    await ctx.send(embed=embedVar)

@adventure.error
async def adventure_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    timeleft = math.ceil(error.retry_after / 60)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"looks like your on a cooldown for {timeleft} minutes!\n**User: {ctx.author}**", color=0xff0000)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
  else:
    raise error

def find_character(updated_map):
  counter = -1
  for i in updated_map:
    counter += 1
    if 2 in i:
      y = counter
      x = updated_map[y].index(2)
  return [x,y]

def render(updated_map, emoji):
  c_pos = find_character(updated_map)



  c_x = c_pos[0]
  c_y = c_pos[1]
  emoji_map = []

  emoji_map.append([emoji[updated_map[c_y + 1][c_x - 1]], emoji[updated_map[c_y + 1][c_x]],emoji[updated_map[c_y + 1][c_x + 1]]])

  emoji_map.append([emoji[updated_map[c_y][c_x - 1]], emoji[updated_map[c_y][c_x]],emoji[updated_map[c_y][c_x + 1]]])

  emoji_map.append([emoji[updated_map[c_y - 1][c_x - 1]], emoji[updated_map[c_y - 1][c_x]],emoji[updated_map[c_y - 1][c_x + 1]]])

  

  return emoji_map

def move_character(updated_map, direction):
  c_pos = find_character(updated_map)
  c_x = c_pos[0]
  c_y = c_pos[1]

  if direction == "up" and updated_map[c_y + 1][c_x] != 1 and updated_map[c_y + 1][c_x] != 3 and updated_map[c_y + 1][c_x] != 4 and updated_map[c_y + 1][c_x] != 6:
    updated_map[c_y][c_x] = 0
    updated_map[c_y + 1][c_x] = 2

  if direction == "down" and updated_map[c_y - 1][c_x] != 1 and updated_map[c_y - 1][c_x] != 3 and updated_map[c_y - 1][c_x] != 4:
    updated_map[c_y][c_x] = 0
    updated_map[c_y - 1][c_x] = 2

  if direction == "left" and updated_map[c_y][c_x - 1] != 1 and updated_map[c_y][c_x - 1] != 3 and updated_map[c_y][c_x - 1] != 4:
    updated_map[c_y][c_x] = 0
    updated_map[c_y][c_x - 1] = 2

  if direction == "right" and updated_map[c_y][c_x + 1] != 1 and updated_map[c_y][c_x + 1] != 3 and updated_map[c_y][c_x + 1] != 4:
    updated_map[c_y][c_x] = 0
    updated_map[c_y][c_x + 1] = 2

  return updated_map


#20    87ceeb
@client.command()
async def map(ctx):
  gametag = players.index(ctx.author.id)
  map_done = peoplecharacters[gametag][20]
  if map_done == 0:
    embedVar = discord.Embed(title="Map", description="These are all the islands as of now!", color=0x87ceeb)
    embedVar.add_field(name=":negative_squared_cross_mark: Island Name: Your Journey Begins", value=f"Description: Its all about collecting treasure!\nRewards: None")
    await ctx.send(embed=embedVar)
  else:
    embedVar = discord.Embed(title="Map", description="These are all the islands as of now!", color=0x87ceeb)
    embedVar.add_field(name=":white_check_mark: Island Name: Your Journey Begins", value=f"Description: Its all about collecting treasure!\nRewards: None")
    await ctx.send(embed=embedVar)

@client.command()
async def calculate(ctx, opt = None, num1 = None, num2 = None):
  possibleopt = ["+", "-", "*", "/", "sqrt", "random"]
  if opt.lower() in possibleopt and num1 != None:
    if opt.lower() == "+" and num2 != None:
      answer = int(num1) + int(num2)
      await ctx.send(f"I got {round(answer, 2)}")
    if opt.lower() == "-" and num2 != None:
      answer = int(num1) - int(num2)
      await ctx.send(f"I got {round(answer, 2)}")
    if opt.lower() == "*" and num2 != None:
      answer = int(num1) * int(num2)
      await ctx.send(f"I got {round(answer, 2)}")
    if opt.lower() == "/" and num2 != None:
      answer = int(num1) / int(num2)
      await ctx.send(f"I got {round(answer, 2)}")
    if opt.lower() == "sqrt" and num2 == None:
      answer = math.sqrt(int(num1))
      await ctx.send(f"I got {round(answer, 2)}")
    if opt.lower() == "random" and num2 != None:
      answer = random.randint(int(num1), int(num2))
      await ctx.send(f"I picked {round(answer, 2)}")

@client.command()
@commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
async def daily(ctx):

  tempid = ctx.author.id
  gametag = players.index(tempid)

  
  display_list = [":small_orange_diamond:", ":small_orange_diamond:", ":small_orange_diamond:", ":small_orange_diamond:", ":small_orange_diamond:"]
  
  streak = peoplecharacters[gametag][14] + 1

  if streak >= 1:
    display_list[0] = ":small_blue_diamond:"
    if streak == 1:
      reward = "1 bronze chest"
      iteminventorys[gametag][8] += 1
    

  if streak >= 2:
    display_list[1] = ":small_blue_diamond:"
    if streak == 2:
      reward = "2 bronze chest"
      iteminventorys[gametag][8] += 2
    

  if streak >= 3:
    display_list[2] = ":small_blue_diamond:"
    if streak == 3:
      reward = "1 silver chest"
      iteminventorys[gametag][16] += 1
    

  if streak >= 4:
    display_list[3] = ":small_blue_diamond:"
    if streak == 4:
      reward = "2 silver chest"
      iteminventorys[gametag][16] += 2

  if streak >= 5:
    display_list[4] = ":small_blue_diamond:"
    if streak == 5:
      reward = "1 golden chest"
      iteminventorys[gametag][17] += 1
  
  embedVar = discord.Embed(title="Daily Reward!", description=f"Rewards:\n{reward}", color=0xffAf00)

  embedVar.add_field(name="Daily Reward Progress", value=f"{display_list[0]} - {display_list[1]} - {display_list[2]} - {display_list[3]} - {display_list[4]}")

  peoplecharacters[gametag][25][3] += 100
  db["charactersofall"] = peoplecharacters
  embedVar.add_field(name="Halloween Event", value="You also claimed 100 candy :candy:")

  await ctx.send(embed=embedVar)
  
  if streak >= 5:
    peoplecharacters[gametag][14] = 0
  else:
    peoplecharacters[gametag][14] += 1
  db["charactersofall"] = peoplecharacters
  db["itemsofall"] = iteminventorys

@daily.error
async def daily_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    timeleft = math.ceil(error.retry_after / 60)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"looks like your on a cooldown for {timeleft} minutes!\n**User: {ctx.author}**", color=0xff0000)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
  else:
    raise error

@client.command()
async def farm(ctx, action1 = None, action2 = None):
  gametag = players.index(ctx.author.id)
  
  if action1 == None and action2 == None:
    
    plant = peoplecharacters[gametag][15]

    if plant == 0:
      embedVar = discord.Embed(title=f"{ctx.author.name}'s Farm", description="planted: :x: None (F!farm plant)", color=0xffAf00)
      await ctx.send(embed=embedVar)

    else:
      embedVar = discord.Embed(title=f"{ctx.author.name}'s Farm", description=f"planted: {planted_name[plant - 1]}", color=0xffAf00)

      pind = peoplecharacters[gametag][15] - 1
      t_dt = peoplecharacters[gametag][16]

      planted_dt = datetime.datetime(t_dt[0], t_dt[1], t_dt[2], t_dt[3], t_dt[4], t_dt[5], t_dt[6])

      harvest_t = datetime.timedelta(minutes=planted_time[pind])

      d_utc = datetime.datetime.now(tz=pytz.UTC)
      d_est = d_utc.astimezone(pytz.timezone('US/Eastern'))

      naive_est = datetime.datetime(d_est.year, d_est.month, d_est.day, d_est.hour, d_est.minute, d_est.second, d_est.microsecond)

      done_at = planted_dt + harvest_t

      time_left = done_at - naive_est


      if naive_est > done_at:
        embedVar.add_field(name=f":stopwatch: | Done (F!farm harvest)", value=f"{planted[plant - 1]}\n:brown_square::brown_square::brown_square:")

        

        await ctx.send(embed=embedVar)

      else:

        min_left = round(time_left.total_seconds() / 60, 1)

        embedVar.add_field(name=f":stopwatch: | Done in: {min_left} minutes", value=f"{planted[plant - 1]}\n:brown_square::brown_square::brown_square:")

        

        await ctx.send(embed=embedVar)

  if action1 == 'plant' and action2 == None:
    embedVar = discord.Embed(title="Farm Plants", description="To plant something: F!farm plant <plant_name>", color=0xffAf00)
     
    embedVar.add_field(name=f"{planted_name[0]}", value=":stopwatch: **|** 1440 minutes\n:package: **|** 10 iron\n<:coin:824666710383657010> **|** 80 coins")

    embedVar.add_field(name=f"{planted_name[1]}", value=":stopwatch: **|** 960 minutes\n:package: **|** 2 ruby\n<:coin:824666710383657010> **|** 50 coins")

    embedVar.add_field(name=f"{planted_name[2]}", value=":stopwatch: **|** 360 minutes\n:package: **|** 3 copper\n<:coin:824666710383657010> **|** 30 coins")

    await ctx.send(embed=embedVar)
  if action1 == 'plant' and action2 in plants_to_choose and peoplecharacters[gametag][15] == 0:

    gametag = players.index(ctx.author.id)
    pind = plants_to_choose.index(action2)

    embedVar = discord.Embed(title=f"{ctx.author.name} Planted A...", description=f"Type: {planted_name[pind]}\nCost: {planted_cost[pind]}\n*Come back in {planted_time[pind]} minutes to harvest, with F!farm harvest!*", color=0xffAf00)
    await ctx.send(embed=embedVar)

    d_utc = datetime.datetime.now(tz=pytz.UTC)
    d_est = d_utc.astimezone(pytz.timezone('US/Eastern'))
    

    peoplecharacters[gametag][15] = pind + 1
    peoplecharacters[gametag][16] = [d_est.year, d_est.month, d_est.day, d_est.hour, d_est.minute, d_est.second, d_est.microsecond]
    db["charactersofall"] = peoplecharacters
  elif action1 == 'plant' and action2 in plants_to_choose and peoplecharacters[gametag][15] != 0:
    embedVar = discord.Embed(title="OH NOO!", description="Looks like you have another plant growing!", color=0xff0000)
    await ctx.send(embed=embedVar)
  
  if action1 == 'harvest' and action2 == None:
    pind = peoplecharacters[gametag][15] - 1
    t_dt = peoplecharacters[gametag][16]

    planted_dt = datetime.datetime(t_dt[0], t_dt[1], t_dt[2], t_dt[3], t_dt[4], t_dt[5], t_dt[6])

    harvest_t = datetime.timedelta(minutes=planted_time[pind])

    d_utc = datetime.datetime.now(tz=pytz.UTC)
    d_est = d_utc.astimezone(pytz.timezone('US/Eastern'))

    naive_est = datetime.datetime(d_est.year, d_est.month,d_est.day, d_est.hour, d_est.minute, d_est.second, d_est.microsecond)

    done_at = planted_dt + harvest_t

    time_left = done_at - naive_est


    if naive_est > done_at:
      embedVar = discord.Embed(title="Harvested!", description="You have harvested your crop!", color=0x0000ff)
      

      plant_har = peoplecharacters[gametag][15] - 1

      

      if plant_har == 2:
        iteminventorys[gametag][7] += 3
        embedVar.add_field(name="You Got:", value="3 copper")
      if plant_har == 1:
        iteminventorys[gametag][14] += 2
        embedVar.add_field(name="You Got:", value="2 ruby")
      if plant_har == 0:
        iteminventorys[gametag][6] += 10
        embedVar.add_field(name="You Got:", value="10 iron")

      if peoplecharacters[gametag][17] == 2:
        peoplecharacters[gametag][17] = 0
        moneytoget = random.randint(200, 600)
        embedVar.add_field(name="Farm Potion", value=f"because of you farm potion you also got {moneytoget} coins!")
        moneybags[gametag] += moneytoget
        db["moneybagsofall"] = moneybags

      await ctx.send(embed=embedVar)
      
      peoplecharacters[gametag][15] = 0
      
      db["charactersofall"] = peoplecharacters
      db["itemsofall"] = iteminventorys


    else:

      embedVar = discord.Embed(title="OH NOO!", description=f"Looks like your plant isnt fully grown yet! Come back in: {time_left}", color=0xff0000)
      await ctx.send(embed=embedVar)

@client.command()
async def scratch(ctx):
  tempid = ctx.author.id
  if tempid in players:
    gametag = players.index(tempid)
    moneytheyhave = moneybags[gametag]
    if 100 <= moneytheyhave:
      embedVar = discord.Embed(title=":dollar: | Scratching your card", description="This action cost 100 coins", color=0x00ff00)
      msg = await ctx.send(embed=embedVar)
       

      moneybags[gametag] -= 100
      db["moneybagsofall"] = moneybags

      await asyncio.sleep(2)

      num_rando = random.randint(0,100)
      if num_rando == 1:
        embedVar = discord.Embed(title=":tada: | Jackpot!", description="You got 1000 coins", color=0x00ff00)
        await msg.edit(embed=embedVar)

        moneybags[gametag] += 1000
        db["moneybagsofall"] = moneybags
      
      if num_rando > 1 and num_rando < 16:
        embedVar = discord.Embed(title=":smiley: | Amazing!", description="You got 500 coins", color=0x00ff00)
        await msg.edit(embed=embedVar)

        moneybags[gametag] += 500
        db["moneybagsofall"] = moneybags

      if num_rando > 15 and num_rando < 36:
        embedVar = discord.Embed(title=":cry: | OH NOO!", description="You got nothing", color=0x00ff00)
        await msg.edit(embed=embedVar)

        

      if num_rando > 35 and num_rando < 96:
        embedVar = discord.Embed(title=":upside_down: | Meh", description="You got your money back", color=0x00ff00)
        await msg.edit(embed=embedVar)

        moneybags[gametag] += 100
        db["moneybagsofall"] = moneybags

      if num_rando > 95:
        embedVar = discord.Embed(title=":smile: | Good!", description="You got 250 coins", color=0x00ff00)
        await msg.edit(embed=embedVar)

        moneybags[gametag] += 250
        db["moneybagsofall"] = moneybags

    else:
      await ctx.send(f"You need 100 coins to scratch a card")
  else:
    embedVar = discord.Embed(title="OH NOO!", description="looks like you Dont have a account, use F!start to create one!", color=0xff0000)
    await ctx.send(embed=embedVar)

@client.command()
async def give(ctx, usertogive : discord.Member = None, amount : int = None):
  tempid = ctx.author.id
  gametag = players.index(tempid)

  moneytheyhave = moneybags[gametag]
  if moneytheyhave >= amount and amount > 0:


    embedVar = discord.Embed(title="Transaction Success", description=f"{ctx.author.name} gave {usertogive.name} {amount} coins!", color=0x0000ff)
    await ctx.send(embed=embedVar)

    gametag2 = players.index(usertogive.id) 
    moneybags[gametag] -= amount
    moneybags[gametag2] += amount
    db["moneybagsofall"] = moneybags


  else:
    embedVar = discord.Embed(title="Transaction Failed", description=f"{ctx.author.name} tried to give {usertogive.name} {amount} coins but only has {moneytheyhave} coins!", color=0xff0000)
    await ctx.send(embed=embedVar)

@client.command()
@commands.cooldown(1, 60 * 60 * 24, commands.BucketType.user)
async def shop(ctx):

  tempid = ctx.author.id
  if tempid in players:
    gametag = players.index(tempid)

    chest = ["bronze", "silver", "golden"]
    chest_cost = [30, 80, 140]
    chest_index = [8, 16, 17]

    special = ["monkey", "octopus", "dragon"]
    special_cost = [175, 250, 470]
    special_index = [5, 3, 2]

    free_coins = random.randint(5, 25)
    

    sale1 = random.choice(chest)
    sale1i = chest.index(sale1)
    cost1 = chest_cost[sale1i]

    sale2 = random.choice(special)
    sale2i = special.index(sale2)
    cost2 = special_cost[sale2i]

    emoji_list = [":toolbox:", ":star:", ":coin:"]
    moneytheyhave = moneybags[gametag]
    peoplecharacters[gametag][18] = [0, 0, 0]
    peoplecharacters[gametag][19] = [sale1i, sale2i, free_coins]
    db["charactersofall"] = peoplecharacters





    list_if_buy = peoplecharacters[gametag][18]
    if list_if_buy[0] == 1:
      emoji_list[0] = ":ballot_box_with_check:"
    if list_if_buy[1] == 1:
      emoji_list[1] = ":ballot_box_with_check:"
    if list_if_buy[2] == 1:
      emoji_list[2] = ":ballot_box_with_check:"


    embedVar = discord.Embed(title="Shop", description=f"The shop resets every 24 hours\nTo buy a item react with the emoji of the item to buy! (example: react with :toolbox: to buy a {sale1} chest!)\n:ballot_box_with_check: = Already Purchased", color=0xff0000)
    embedVar.add_field(name=f"{emoji_list[0]} Chest", value=f"{sale1} Chest **|** Cost: {cost1} coins")
    embedVar.add_field(name=f"{emoji_list[1]} Special", value=f"{sale2} Pet **|** Cost: {cost2} coins")
    embedVar.add_field(name=f"{emoji_list[2]} Free", value=f"{free_coins} coins | Cost: Free")
    
    embedVar.set_footer(icon_url="https://cdn.discordapp.com/emojis/824666710383657010.png?v=1", text=f"You have {moneytheyhave} coins")
    msg = await ctx.send(embed=embedVar)

    await msg.add_reaction('🧰')
    await msg.add_reaction('⭐')
    await msg.add_reaction('🪙')
  
    done = False
    no_edit = False
    while not done:
      try:
        reaction, user = await client.wait_for('reaction_add', timeout=20.0)
      except asyncio.TimeoutError:
        embedVar = discord.Embed(title="OH NOO", description="Closed shop due to timeout!", color=0xff0000)
        await msg.edit(embed=embedVar)
        done = True
      else:
        if str(reaction.emoji) == '🧰' and tempid == user.id and list_if_buy[0] != 1 and moneytheyhave >= cost1:
          emoji_list[0] = ":ballot_box_with_check:"
          peoplecharacters[gametag][18][0] = 1
          moneybags[gametag] -= cost1
          iteminventorys[gametag][chest_index[sale1i]] += 1

          db["charactersofall"] = peoplecharacters
          db["itemsofall"] = iteminventorys
          db["moneybagsofall"] = moneybags
        elif str(reaction.emoji) == '🧰' and tempid == user.id:
          embedVar = discord.Embed(title="OH NOO!", description=f"You already bought this item or you do not have enoght coins to buy this item!", color=0xff0000)
          await msg.edit(embed=embedVar)
          done = True
          no_edit = True


        #next item
        if str(reaction.emoji) == '⭐' and tempid == user.id and list_if_buy[1] != 1 and moneytheyhave >= cost2:
          emoji_list[1] = ":ballot_box_with_check:"
          peoplecharacters[gametag][18][1] = 1
          peoplecharacters[gametag][11].append(special_index[sale2i])
          db["charactersofall"] = peoplecharacters
          moneybags[gametag] -= cost2
          db["moneybagsofall"] = moneybags
        elif str(reaction.emoji) == '⭐' and tempid == user.id:
          embedVar = discord.Embed(title="OH NOO!", description=f"You already bought this item or you do not have enoght coins to buy this item!", color=0xff0000)
          await msg.edit(embed=embedVar)
          done = True
          no_edit = True

        

        #next item
        if str(reaction.emoji) == '🪙' and tempid == user.id and list_if_buy[2] != 1:
          emoji_list[2] = ":ballot_box_with_check:"
          peoplecharacters[gametag][18][2] = 1
          
          db["charactersofall"] = peoplecharacters
          moneybags[gametag] += free_coins
          db["moneybagsofall"] = moneybags
        elif str(reaction.emoji) == '🪙' and tempid == user.id:
          embedVar = discord.Embed(title="OH NOO!", description=f"You already bought this item or you do not have enoght coins to buy this item!", color=0xff0000)
          await msg.edit(embed=embedVar)
          done = True
          no_edit = True

        #update
        if tempid == user.id and no_edit != True:
          embedVar = discord.Embed(title="Shop", description=f"The shop resets every 24 hours\nTo buy a item react with the emoji of the item to buy! (example: react with :toolbox: to buy a {sale1} chest!)\n:ballot_box_with_check: = Already Purchased", color=0xff0000)
          embedVar.add_field(name=f"{emoji_list[0]} Chest", value=f"{sale1} Chest **|** Cost: {cost1} coins")
          embedVar.add_field(name=f"{emoji_list[1]} Special", value=f"{sale2} Pet **|** Cost: {cost2} coins")
          embedVar.add_field(name=f"{emoji_list[2]} Free", value=f"{free_coins} coins | Cost: Free")
          
          embedVar.set_footer(icon_url="https://cdn.discordapp.com/emojis/824666710383657010.png?v=1", text=f"You have {moneytheyhave} coins")

          await msg.edit(embed=embedVar)
  
@shop.error
async def shop_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    tempid = ctx.author.id
    if tempid in players:
      gametag = players.index(tempid)

      chest = ["bronze", "silver", "golden"]
      chest_cost = [30, 80, 140]
      chest_index = [8, 16, 17]

      special = ["monkey", "octopus", "dragon"]
      special_cost = [175, 250, 470]
      special_index = [5, 3, 2]

      
    
      get_index_shop = peoplecharacters[gametag][19]

      sale1 = chest[get_index_shop[0]]
      sale1i = get_index_shop[0]
      cost1 = chest_cost[sale1i]

      sale2 = special[get_index_shop[1]]
      sale2i = get_index_shop[1]
      cost2 = special_cost[sale2i]

      free_coins = get_index_shop[2]

      emoji_list = [":toolbox:", ":star:", ":coin:"]
      moneytheyhave = moneybags[gametag]
    
      list_if_buy = peoplecharacters[gametag][18]
      if list_if_buy[0] == 1:
        emoji_list[0] = ":ballot_box_with_check:"
      if list_if_buy[1] == 1:
        emoji_list[1] = ":ballot_box_with_check:"
      if list_if_buy[2] == 1:
        emoji_list[2] = ":ballot_box_with_check:"


      embedVar = discord.Embed(title="Shop", description=f"The shop resets every 24 hours\nTo buy a item react with the emoji of the item to buy! (example: react with :toolbox: to buy a {sale1} chest!)\n:ballot_box_with_check: = Already Purchased", color=0xff0000)
      embedVar.add_field(name=f"{emoji_list[0]} Chest", value=f"{sale1} Chest **|** Cost: {cost1} coins")
      embedVar.add_field(name=f"{emoji_list[1]} Special", value=f"{sale2} Pet **|** Cost: {cost2} coins")
      embedVar.add_field(name=f"{emoji_list[2]} Free", value=f"{free_coins} coins | Cost: Free")
      
      embedVar.set_footer(icon_url="https://cdn.discordapp.com/emojis/824666710383657010.png?v=1", text=f"You have {moneytheyhave} coins")
      msg = await ctx.send(embed=embedVar)

      await msg.add_reaction('🧰')
      await msg.add_reaction('⭐')
      await msg.add_reaction('🪙')
  
      done = False
      no_edit = False
      while not done:
        try:
          reaction, user = await client.wait_for('reaction_add', timeout=20.0)
        except asyncio.TimeoutError:
          embedVar = discord.Embed(title="OH NOO", description="Closed shop due to timeout!", color=0xff0000)
          await msg.edit(embed=embedVar)
          done = True
        else:
          if str(reaction.emoji) == '🧰' and tempid == user.id and list_if_buy[0] != 1 and moneytheyhave >= cost1:
            emoji_list[0] = ":ballot_box_with_check:"
            peoplecharacters[gametag][18][0] = 1
            moneybags[gametag] -= cost1
            iteminventorys[gametag][chest_index[sale1i]] += 1
            
            db["charactersofall"] = peoplecharacters
            db["itemsofall"] = iteminventorys
            db["moneybagsofall"] = moneybags
          elif str(reaction.emoji) == '🧰' and tempid == user.id and list_if_buy[0] == 1 and moneytheyhave >= cost1:
            embedVar = discord.Embed(title="OH NOO!", description=f"You already bought this item or you do not have enoght coins to buy this item!", color=0xff0000)
            await msg.edit(embed=embedVar)
            done = True
            no_edit = True

          #next item
          if str(reaction.emoji) == '⭐' and tempid == user.id and list_if_buy[1] != 1 and moneytheyhave >= cost2:
            emoji_list[1] = ":ballot_box_with_check:"
            peoplecharacters[gametag][18][1] = 1
            peoplecharacters[gametag][11].append(special_index[sale2i])
            db["charactersofall"] = peoplecharacters
            moneybags[gametag] -= cost2
            db["moneybagsofall"] = moneybags
          elif str(reaction.emoji) == '⭐' and tempid == user.id:
            embedVar = discord.Embed(title="OH NOO!", description=f"You already bought this item or you do not have enoght coins to buy this item!", color=0xff0000)
            await msg.edit(embed=embedVar)
            done = True
            no_edit = True


          #next item
          if str(reaction.emoji) == '🪙' and tempid == user.id and list_if_buy[2] != 1:
            emoji_list[2] = ":ballot_box_with_check:"
            peoplecharacters[gametag][18][2] = 1
          
            db["charactersofall"] = peoplecharacters
            moneybags[gametag] += free_coins
            db["moneybagsofall"] = moneybags
          elif str(reaction.emoji) == '🪙' and tempid == user.id:
            embedVar = discord.Embed(title="OH NOO!", description=f"You already bought this item or you do not have enoght coins to buy this item!", color=0xff0000)
            await msg.edit(embed=embedVar)
            done = True
            no_edit = True
          
          if tempid == user.id and no_edit != True:
            embedVar = discord.Embed(title="Shop", description=f"The shop resets every 24 hours\nTo buy a item react with the emoji of the item to buy! (example: react with :toolbox: to buy a {sale1} chest!)\n:ballot_box_with_check: = Already Purchased", color=0xff0000)
            embedVar.add_field(name=f"{emoji_list[0]} Chest", value=f"{sale1} Chest **|** Cost: {cost1} coins")
            embedVar.add_field(name=f"{emoji_list[1]} Special", value=f"{sale2} Pet **|** Cost: {cost2} coins")
            embedVar.add_field(name=f"{emoji_list[2]} Free", value=f"{free_coins} coins | Cost: Free")
            
            embedVar.set_footer(icon_url="https://cdn.discordapp.com/emojis/824666710383657010.png?v=1", text=f"You have {moneytheyhave} coins")

            await msg.edit(embed=embedVar)
  else:
    raise error

@client.command()
async def tempshop(ctx):
  await ctx.send(">>> Shop!\nThis shop is currently only to buy the new character\n<:ninja_grass:860542120728854569> Ninja\nCost: 2500 coins\n*To buy the new character type F!buy")
  
@client.command()
async def buy(ctx):
  if ctx.author.id in players:
    gametag = players.index(ctx.author.id)
    if moneybags[gametag] > 2499:
      await ctx.send("You have bought the character ninja! It has been auto equiped.")
      moneybags[gametag] -= 2500
      db["moneybagsofall"] = moneybags
      peoplecharacters[gametag][-1] = 2
      db["charactersofall"] = peoplecharacters
    else:
      await ctx.send("You dont have enough coins!")
  

@client.command()
async def support(ctx):
  embedVar = discord.Embed(title="Support Funguy!", description=f"here are some ways to support funguy:", color=0xee00ff)
  embedVar.add_field(name=f"-Server boosting (Funguy Bot server)", value="Rewards: 100 coins + 5 bronze chests + 3 silver chests + 1 golden chests\n[Click here](https://discord.gg/WByYtSKJQe) to join!")

  embedVar.set_footer(text=f"Type F!claim in the official funguy bot server after supporting the bot in anyway!\nYou can type F!claim every week!")

  await ctx.send(embed=embedVar)

@client.command()
@commands.cooldown(1, 60 * 60 * 24 * 7, commands.BucketType.user)
async def claim(ctx):
    
  check = check_booster(ctx)
  if check:
    embedVar = discord.Embed(title="YAY!", description=f"Thank you so much {ctx.author} for supporting FunGuy!\nRewards: 100 coins + 5 bronze chests + 3 silver chests + 1 golden chests", color=0xee00ff)
    await ctx.send(embed=embedVar)

    gametag = players.index(ctx.author.id)
  
    iteminventorys[gametag][8] += 5
    iteminventorys[gametag][16] += 3
    iteminventorys[gametag][17] += 1
    moneybags[gametag] += 100

    db["itemsofall"] = iteminventorys
    db["moneybagsofall"] = moneybags

  else:

    ctx.command.reset_cooldown(ctx)
    embedVar = discord.Embed(title="OH NOO", description=f"You are not supporting FunGuy in any way, check out some ways to help FunGuy by typing F!support", color=0xee00ff)
    await ctx.send(embed=embedVar)

@claim.error
async def claim_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    timeleft = math.ceil(error.retry_after / 60)
    embedVar = discord.Embed(title=f"OH NOO!", description=f"looks like your on a cooldown for {timeleft} minutes!\nUser: {ctx.author}", color=0xff0000)
    embedVar.set_thumbnail(url=ctx.author.avatar_url)
    await ctx.send(embed=embedVar)
  else:
    raise error




def check_booster(ctx):
  role_id = 853295641764429845
  b_role = discord.utils.get(ctx.guild.roles, id=role_id)
  if ctx.guild.id == 801083422201479178 and b_role in ctx.author.roles:
    return True
  else:
    return False

@client.command()
async def brew(ctx, potion = None):
  tempid = ctx.author.id
  gametag = players.index(tempid)
  p_names = ["cooldown", "farm", "train"]
  p_index = [18, 19, 20]
  amount_needed = [[14, 2], [10, 2], [7, 5]]
  text_p = ["2 ruby", "2 log", "5 copper"]
  if potion == None:
    embedVar = discord.Embed(title="Brewing Stand", description="to brew a potion: F!brew <potion_name>\n**Each potion requires a lily pad to brew!**", color=0x7a461e)    
    embedVar.set_thumbnail(url="https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F774261525363032095.png%3Fv%3D1&w=64&q=75")

    embedVar.add_field(name="<:cooldown_potion:854858969206095952> | Cooldown Potion (Resets **Resource Gathering** cooldowns)", value="ingredients: 2 ruby + 1 water bottle")

    embedVar.add_field(name="<:farm_potion:854859290375618560> | Farm potion (next harvest gives coins)", value="ingredients: 2 log + 1 water bottle")

    embedVar.add_field(name="<:train_potion:854859149510443028> | Train Potion (next train gives more xp)", value="ingredients: 5 copper + 1 water bottle")

    await ctx.send(embed=embedVar)
  elif potion.lower() in p_names:
    p_indext = p_names.index(potion.lower())
    

    if iteminventorys[gametag][3] > 0 and iteminventorys[gametag][4] > 0 and iteminventorys[gametag][amount_needed[p_indext][0]] > amount_needed[p_indext][1] - 1:
      embedVar = discord.Embed(title="Brewing Potion", description=f"<a:wait_loading:855100780201771098> **|** Brewing a **{potion.lower()} potion**!\nDone in: 5 seconds", color=0x7a461e)    
      
      embedVar.set_thumbnail(url="https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F774261525363032095.png%3Fv%3D1&w=64&q=75")
      msg = await ctx.send(embed=embedVar)

      await asyncio.sleep(5)

      embedVar = discord.Embed(title="Brewing Potion", description=f":ballot_box_with_check: **|** Done brewing a **{potion.lower()} potion**!\n*Use with F!use {potion.lower()}*", color=0x7a461e)    
      embedVar.set_thumbnail(url="https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F774261525363032095.png%3Fv%3D1&w=64&q=75")
      await msg.edit(embed=embedVar)

      iteminventorys[gametag][amount_needed[p_indext][0]] -= amount_needed[p_indext][1]
      iteminventorys[gametag][p_index[p_indext]] += 1

      db["itemsofall"] = iteminventorys
    else:
      embedVar = discord.Embed(title="Brewing Failed!", description=f"**Ingredients Needed**\n1 lily pad\n1 water bottle\n{text_p[p_indext]}\n*Type: {potion.lower()} potion*", color=0xff0000)    
      
      embedVar.set_thumbnail(url="https://discords.com/_next/image?url=https%3A%2F%2Fcdn.discordapp.com%2Femojis%2F774261525363032095.png%3Fv%3D1&w=64&q=75")
      await ctx.send(embed=embedVar)

@client.command()
async def info(ctx, search=None):
  if search == None:
    await ctx.send("the correct usage is F!info <search>")
  else:
    results = 0
    s_done = []
    for i in item_info_list:
      if search.lower() in i[0]:
        s_done.append(i)
        results += 1
    if results != 0:
      embedVar = discord.Embed(title=f":mag_right: | Search Done (results: {results})", description=f"{s_done[0][0].title()} **|** Type: {s_done[0][1].title()}", color=0x87ceff)

      embedVar.add_field(name="Description", value=f"{s_done[0][2]}", inline=False)
      embedVar.add_field(name="Arguments", value=f"{s_done[0][3]}")
      embedVar.add_field(name="Aliases", value=f"{s_done[0][4]}")

      await ctx.send(embed=embedVar)
    else:
      await ctx.send("i found nothing")

@client.command()
async def loop(ctx, thing=None, action=None):
  if ctx.author.id == 536687564401147908 and thing == "lottery":
    if action == "start":
      embedVar = discord.Embed(title=f":infinity: | Loop has started", description=f"looping {thing} to reset every 24 hours", color=0x87ceff)
      await ctx.send(embed=embedVar)

      checklot.start(ctx)
    else:
      embedVar = discord.Embed(title=f":infinity: | Loop has stopped", description=f"Stopped looping {thing} to reset every 24 hours", color=0x87ceff)
      await ctx.send(embed=embedVar)
      checklot.cancel()

  else:
    embedVar = discord.Embed(title=f":lock: | OH NOO", description="Looks like you dont have permission to use this command!", color=0xff0000)
    await ctx.send(embed=embedVar)


@tasks.loop(seconds=60)
async def checklot(ctx):
  d_utcnow = datetime.datetime.now(tz=pytz.UTC)
  d_estnow = d_utcnow.astimezone(pytz.timezone('US/Eastern'))

  if d_estnow.hour == 12 and d_estnow.minute == 1:
    totaltickets = get_tickets(peoplecharacters)
    if totaltickets > 0:
      thewinner = get_winner(peoplecharacters)
      reset_tickets()
      user = await client.fetch_user(thewinner[0])
      prize = totaltickets * 15
      
      embedVar = discord.Embed(title="Lottery", description=f"{user}, has won {prize} coins!", color=0xffff00)
      channel = client.get_channel(865611864816877578)
      await channel.send(embed=embedVar)

      moneybags[players.index(user.id)] += prize
      db["moneybagsofall"] = moneybags
    else:
      embedVar = discord.Embed(title="Lottery", description="Noone purchesed any tickets, so there was no winner", color=0xffff00)
      channel = client.get_channel(865611864816877578)
      await channel.send(embed=embedVar)


def reset_tickets():
  count = 0
  for i in peoplecharacters:
    peoplecharacters[count][21] = 0
    count += 1
  db["charactersofall"] = peoplecharacters

def get_winner(data):
  draws = []
  count = 0
  for i in data:
    if i[21] > 0:
      for ind in range(i[21]):
        draws.append([players[count]])

  winner = random.choice(draws)
  return winner

  

def get_tickets(data):
  count = 0
  for i in data:
    count += i[21]

  return count

@client.command()
async def lottery(ctx, act=None, amount=None):
  gametag = players.index(ctx.author.id)
  if act == None and amount == None:
    

    totaltickets = get_tickets(peoplecharacters)

    my_tickets = peoplecharacters[gametag][21]
    prize = totaltickets * 15



    embedVar = discord.Embed(title="Lottery", description=f":moneybag: | Current Prize: {prize} coins\n:gem: | {totaltickets} tickets have been purchased\n:tickets: | You own {my_tickets} tickets\n*Lottery ends at 12:00 PM EST every day*\n", color=0xffff00)
    embedVar.set_footer(text="Buy ticket with F!lottery buy <amount> | Each ticket costs 15 coins")
    await ctx.send(embed=embedVar)
  else:
    if act == "buy":
      moneytheyhave = moneybags[gametag]
      pay = int(amount) * 15
      if moneytheyhave >= pay:
        await ctx.send(f">>> You have purchased {amount} tickets for {pay} coins!")

        moneybags[gametag] -= pay
        peoplecharacters[gametag][21] += int(amount)

        db["charactersofall"] = peoplecharacters
        db["moneybagsofall"] = moneybags
      else:
        await ctx.send(f">>> You are trying to buy {amount} tickets for {pay} coin, but you only have {moneytheyhave} coins!")
      
  

  

  



#reset accounts!!!  -change resetaccounts to 2
resetaccounts = 1
if resetaccounts == 2:
  db["totalplayers"] = []
  db["moneybagsofall"] = []
  db["itemsofall"] = []
  db["charactersofall"] = []
  db["booster_data"] = []
  db["clans"] = []

players = db["totalplayers"]
moneybags = db["moneybagsofall"]
iteminventorys = db["itemsofall"]
peoplecharacters = db["charactersofall"]
cha_boosters = db["booster_data"]
clans_list = db["clans"]



#indexofadding = 0
#for i in peoplecharacters:
  #peoplecharacters[indexofadding][-1] = [0,1]
  #peoplecharacters[indexofadding].append([0,0])
  #iteminventorys[indexofadding].append([1, 1])
  #iteminventorys[indexofadding].append(0)
#iteminventorys[0][17] = 10
  #iteminventorys[indexofadding].append(0)
#iteminventorys[23].append(0)
#iteminventorys[23].append(0)
#iteminventorys[23].append(0)
  #indexofadding += 1
  #peoplecharacters[indexofadding][25] = [0,0,0,0]



#iteminventorys[19][15] += 37
#iteminventorys[6][17] += 5

#peoplecharacters[6][22] += 2
#peoplecharacters[8][22] += 2
#peoplecharacters[-1].append(0)
#peoplecharacters[-2].append(0)
#peoplecharacters[-3].append(0)

#db["charactersofall"] = peoplecharacters
#db["itemsofall"] = iteminventorys
#moneybags[0] = 69693555
#db["moneybagsofall"] = moneybags


e_bosses = [':ghost: The ancient ghost', ':jack_o_lantern: Evil Pumpkin']
e_boss = random.choice(e_bosses)
e_boss_h = random.randint(20, 50)
event_boss = [e_boss, e_boss_h, e_boss_h]

correctitems = ["commonfish", "rarefish", "epicfish", "rock", "iron", "copper", "stick", "log"]
indexofcorrectitems = [0, 1, 2, 5, 6, 7, 9, 10]

everytrade = []

petquotestosay = [["meow", "**N**ot **M**uch **H**ere", "cats have 9 lives!!"], ["fire!", "The dragon lives in a tower", "Frozen Dragon??"], ["OcToPuS", "Watch out!", "ink sac???"], ["Bird`s eye view!", "Fly! like an eagle", "ka-kaw!"], ["banana", "ooh-ooh-ahh-ahh", "umm :banana: ?"], ["B-u-G"]]

petsemojis = [':cat2:', ':dragon:', ':octopus:', ':eagle:', ':monkey:', ':bug:']

peteffects = ["increases health: (amount:", "every attack burns the enemy for 3 seconds: (dps:", "every attack has a chance to stun the enemy for a short time: (duration:", "increases dodge rate: (amount:", "gives you materials when you train it: (amount:", "Increases your hp: (amount:"]

petamounts = [2,1,1,35,1,2]

travelunit = ["none :x:", "<:wooden_raft:826156013497090098> wooden raft"]

planted = [':coconut::seedling::coconut:', ':watermelon::seedling::watermelon:', ':carrot::seedling::carrot:']
planted_name = [':coconut: coconut', ':watermelon: watermelon',':carrot: carrot']
planted_cost = [350, 200, 75]
plants_to_choose = ['coconut', 'watermelon', 'carrot']
planted_time = [1320, 960, 360] 

items = ["commonfish", "rarefish", "epicfish", "waterbottle", "lilypad", "rock", "iron", "copper", "bronze", "stick", "log", "leaf", "apple", "banana", "ruby", "diamond", "silver", "golden"]
itemsvalue = [1, 3, 5, 5, 10, 12, 20, 30, 60, 25, 40, 15, 20, 20, 90, 120, 110, 175]
buyvalue = [2, 6, 10, 10, 20, 24, 40, 60]
dungeonrow1 = ":green_square::green_square::green_square::green_square::green_square:"
my_secret = os.environ['TheSecret']



#BELOW ALL CODE
client.run(my_secret)
