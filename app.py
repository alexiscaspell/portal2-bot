import os
from dotenv import load_dotenv
import discord
from src.portal2 import Portal2Info,Portal2Query
from src.sheets import load_data
import requests as req
from src.pinterest import PinterestImageScraper
from random import randint
from discord import ApplicationContext
import time
from src.string_util import make_str_table
from io import BytesIO


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
SAMPLE_SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
ADMIN_USERS = os.getenv('ADMIN_USERS',None)
ADMIN_USERS= ADMIN_USERS.split(",") if ADMIN_USERS else []

bot = discord.Bot()
portal_data = None

def load_context():
    global portal_data
    portal_data = Portal2Info(load_data(SAMPLE_SPREADSHEET_ID))

async def send_response(ctx:ApplicationContext,message):
    try:
        await ctx.respond(message)
    except Exception as _:
        await ctx.channel.send(message)

async def validate_permissions(ctx:ApplicationContext):
    message_user = ctx.author.name

    print(f"{message_user} me acaba de invocar")

    if len(ADMIN_USERS)>0 and message_user not in ADMIN_USERS:
        await ctx.respond(f"**{message_user}** papu, no tenes permisos")
        raise RuntimeError(f"El usuario {message_user} no tiene permisos de admin")


@bot.slash_command(description="/start_map <nombre mapa | nro mapa (default comienza el siguiente en la lista)>")
async def start_map(ctx,mapa:str=None):
    await validate_permissions(ctx)

    load_context()

    if mapa is None:
        row = portal_data.latest_played_map_number_row()
        row+=1
    elif mapa.isnumeric():
        row = portal_data.map_number_row_by_id(mapa)
    else:
        row = portal_data.map_number_row_by_name(mapa)

    portal_data.start_map_by_row(row)
    time.sleep(1)
    load_context()
    portal_data.start_map_by_row(row)
    response = "Sssssssse derrechuuu!"
    await send_response(ctx,response)

@bot.slash_command(description="Termina el mapa empezado previamente")
async def end_map(ctx):
    await validate_permissions(ctx)

    load_context()

    row = portal_data.latest_played_map_number_row()+1

    portal_data.end_map_by_row(row)
    time.sleep(1)
    load_context()
    portal_data.end_map_by_row(row)


    response = "Disculpame si te gane muy rapido pero asi es el portal champagne"
    await send_response(ctx,response)

@bot.slash_command(description="Obtiene los stats de tiempo de juego")
async def stats(ctx):
    load_context()

    response=f"`{make_str_table(portal_data.stats)}`"

    await send_response(ctx,response)

@bot.slash_command(description="Pausa el mapa empezado previamente")
async def pause_map(ctx):
    await validate_permissions(ctx)

    load_context()

    row = portal_data.latest_played_map_number_row()+1

    # portal_data.pause_map_by_row(row)

    response = "Jiji todavia no se hacer eso"
    await send_response(ctx,response)


@bot.slash_command(description="Envia meme random de <key> (default 'portal2 meme')")
async def meme(ctx:ApplicationContext,key="portal2 hilarious meme"):

    await ctx.respond("Ahi te lo busco papa")

    async with ctx.typing():
        links = PinterestImageScraper().scrape_links(key)

        selected_index = randint(0,len(links)-1)

        response = links[selected_index]

    await ctx.interaction.edit_original_message(content=response)

@bot.slash_command(description="/add_map <url mapa>")
async def add_map(ctx,url:str):

    await validate_permissions(ctx)

    load_context()

    title = req.get(url).text.split("</title>")[0].split("<title>")[1]

    if title.startswith("Steam Workshop::"):
        title = title[len("Steam Workshop::"):]

    portal_data.add_map(title)

    response = f"Mapa {title} guardado"
    await send_response(ctx,response)

@bot.slash_command(description="Devuelve le siguiente mapa a jugar")
async def next_map(ctx):
    load_context()

    response = portal_data.next_map()
    response = "No hay mapa vieja" if response=="" else response

    await send_response(ctx,response)

@bot.slash_command(description="Hace una consulta de los mapas")
async def query_maps(ctx,played:bool=None,name=None,id:int=None,start_date=None,end_date=None):
    load_context()

    await ctx.respond("Buscando ...")

    query = Portal2Query(portal_data)

    query = query.filter_by_played(played).filter_by_name(name).filter_by_id(id)
    query = query.filter_by_start_date(start_date).filter_by_end_date(end_date)
    result = query.result()

    response = make_str_table(result)

    if len(response)<2000:
        response = f"`{response}`"
        await ctx.interaction.edit_original_message(content=response)
    else:
        await ctx.interaction.edit_original_message(content="Resultado",file=discord.File(BytesIO(bytes(response,'UTF-8')), "query.md"))


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

bot.run(TOKEN)