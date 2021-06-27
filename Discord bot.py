import random
import os, discord
from discord.ext import commands
from ServerSettings import ServerSettings

from dotenv import load_dotenv
load_dotenv()

All_intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!",intents=All_intents )

TOKEN = os.environ["DISCORD_TOKEN"]

heys = ["hello","hi","hey","wagwan", "yo", "hola"]

commands : str = f"Commands:\n!stat censor/usercount/strikes\n!censor on/off\n"

@bot.event
async def on_ready():
    print(f"{bot.user.name} has connected to Discord!")
    welcomes = [f"What's up party people, {bot.user.name} is here!","Guess who's back!",f"It's me {bot.user.name}!","Wagwan guys!",f"{bot.user.name} is in the house!",f"It's a me - {bot.user.name}!"]

    ServerSettings.LoadServers()
    server : discord.Guild #the 2 typing is for autocompletetion

    for server in bot.guilds:
        ServerSettings.AddServer(server_id=server.id, force=False)
        for channele in server.text_channels:
            if channele.name == "general":
                await channele.send(welcomes[random.randint(0, len(welcomes)-1)])

@bot.event
async def on_guild_join(guild : discord.Guild):
    ServerSettings.AddServer(guild.id, force = False)

@bot.event
async def on_message(message : discord.Message):
    if message.author == bot.user: #checks if msg sender is bot
        return

    serv = ServerSettings.GetServer(message.guild.id)

    if getattr(serv, "cuss") == True: #cussing algo
        if any(cuss in message.content.lower().strip() for cuss in serv.cuss_keys):
            await message.channel.send(f"Don't swear, {message.author.mention}!")
            await message.delete()

            serv.strikes[str(message.author)] = serv.strikes.get(str(message.author), 0) + 1
            await message.channel.send(f"You have {serv.strikes[str(message.author)]} strike(s)! {message.author.mention}")
            return

    await bot.process_commands(message=message)

@bot.command(name="",aliases=heys)
async def helloFunc(ctx, *, message: str = ""):
    await ctx.send(f"Hey to you too! {ctx.author.mention}")
    return

@bot.command(name="censor")
async def cusson(ctx, *, msg:str = ""):
    serv = ServerSettings.GetServer(ctx.guild.id)

    if msg.lower().strip() == "on":
        serv.cuss = True
        await ctx.send(f"Cuss Censorship is on! {ctx.author.mention}")
    elif msg.lower().strip() == "off":
        serv.cuss=False
        await ctx.send(f"Cuss Censorship is off! {ctx.author.mention}")
    else:
        await ctx.send(f"Invalid argument = '{msg}'\nValid arguments = 'on' / 'off'\n{ctx.author.mention}")
    
@bot.command(name="stat")
async def statCheck(ctx, *, msg:str = ""):
    msg = msg.lower().strip()
    serv = ServerSettings.GetServer(ctx.guild.id)
    if msg == "censor":
        prop = getProperty(str(ctx.guild.id), "cuss")
        await ctx.send(f"Cuss censorship status: {prop}! {ctx.author.mention}")
    elif msg == "usercount":
        await ctx.send(f"There are {ctx.guild.member_count} people on this server! {ctx.author.mention}")
    elif msg =="strikes":
        await ctx.send(f"You have {serv.strikes[str(ctx.author)]} strike(s)! {ctx.author.mention}")
    else:
        await ctx.send(f"Invalid arguments\nType '!cmds' for commands! {ctx.author.mention}")
        

@bot.command()
async def cmds(ctx, *, msg:str=""):
    if not msg == "":
        await ctx.send(f"Invalid arguments\nType '!cmds' for commands! {ctx.author.mention}")
    else:
        await ctx.send(f"{commands}{ctx.author.mention}")
    

def getProperty(server_id: str, want: str):
    serv : ServerSettings = ServerSettings.GetServer(server_id=server_id)
    return getattr(serv, want)

bot.run(TOKEN)

ServerSettings.SaveServers()