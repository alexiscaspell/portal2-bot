import imp
import os
from dotenv import load_dotenv
import discord
from src.portal2 import Portal2Info
from src.sheets import load_data

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SAMPLE_SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

SAMPLE_RANGE_NAME = 'A1:I'

bot = discord.Bot()
portal_data = None

def load_context():
    global portal_data
    portal_data = Portal2Info(load_data(SAMPLE_SPREADSHEET_ID,SAMPLE_RANGE_NAME))

@bot.slash_command(description="/start_map <nombre mapa | nro mapa (default comienza el siguiente en la lista)>")
async def start_map(ctx):
    load_context()
    response = "Sssssssse derrechuuu!"
    await ctx.respond(response)

@bot.slash_command()
async def end_map(ctx):
    load_context()
    response = "Disculpame si te gane muy rapido pero asi es el portal champagne"
    await ctx.respond(response)

@bot.slash_command()
async def stats(ctx):
    load_context()
    response="########## **STATS** ##########\n"
    for k in portal_data.stats:
        response+=f"***{k}:*** {portal_data.stats[k]}\n"

    response+="#########################"

    await ctx.respond(response)

@bot.slash_command()
async def pause_map(ctx):
    load_context()
    response = "Jiji todavia no se hacer eso"
    await ctx.respond(response)

@bot.slash_command()
async def add_map(ctx):
    load_context()
    # <title>Steam Workshop::Bounding Box - A Series of Chambers Exploring Repulsion Gel Cubes</title>
    response = "Jiji todavia no se hacer eso"
    await ctx.respond(response)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
