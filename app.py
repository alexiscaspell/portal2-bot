import os
from dotenv import load_dotenv
import discord
from src.portal2 import Portal2Info
from src.sheets import load_data
import requests as req

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SAMPLE_SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')

bot = discord.Bot()
portal_data = None

def load_context():
    global portal_data
    portal_data = Portal2Info(load_data(SAMPLE_SPREADSHEET_ID))

@bot.slash_command(description="/start_map <nombre mapa | nro mapa (default comienza el siguiente en la lista)>")
async def start_map(ctx,mapa:str=None):
    load_context()

    if mapa is None:
        row = portal_data.latest_played_map_number_row()
    elif mapa.isnumeric():
        row = portal_data.map_number_row_by_id(mapa)
    else:
        row = portal_data.map_number_row_by_name(mapa)
    
    portal_data.update_map_start_time(row,portal_data.actual_hour)

    response = "Sssssssse derrechuuu!"
    await ctx.respond(response)

@bot.slash_command(description="Termina el mapa empezado previamente")
async def end_map(ctx):
    load_context()

    row = portal_data.latest_played_map_number_row()
    portal_data.update_map_end_time(row,portal_data.actual_hour)

    response = "Disculpame si te gane muy rapido pero asi es el portal champagne"
    await ctx.respond(response)

@bot.slash_command(description="Obtiene los stats de tiempo de juego")
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

@bot.slash_command(description="/add_map <url mapa>")
async def add_map(ctx,url:str):
    load_context()

    if not url:
        await ctx.respond("Sossss un hijjjo deee, pasame un link!!")
    else:
        title = req.get(url).text.split("</title>")[0].split("<title>")[1]

        if title.startswith("Steam Workshop::"):
            title = title[len("Steam Workshop::"):]

        portal_data.add_map(title)

        response = "Mapa guardado"
        await ctx.respond(response)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)
