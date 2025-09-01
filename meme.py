import discord
from discord.ext import commands
import os
import random
import json

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

DATA_FILE = 'meme_stats.json'

def load_data():
    """Carga los datos de un archivo JSON."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {"total_memes": 0, "user_counts": {}}

def save_data(data):
    """Guarda los datos en un archivo JSON."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

@bot.event
async def on_ready():
    print(f"Hemos iniciado sesion como {bot.user}")

@bot.command()
async def meme(ctx):
    """
    Envía un meme aleatorio y actualiza las estadísticas.
    """
    data = load_data()
    
    img_name = random.choice(os.listdir("memes"))
    with open(f"memes/{img_name}", 'rb') as f:
        picture = discord.File(f)
        await ctx.send(file=picture)
    
    data['total_memes'] += 1
    user_id = str(ctx.author.id)
    if user_id in data['user_counts']:
        data['user_counts'][user_id] += 1
    else:
        data['user_counts'][user_id] = 1
        
    save_data(data)

@bot.command()
async def memes_enviados(ctx):
    """Muestra el número total de memes que el bot ha enviado."""
    data = load_data()
    total = data.get('total_memes', 0)
    await ctx.send(f"El bot ha enviado un total de **{total}** memes. ¡A seguir pidiendo más!")

@bot.command()
async def mi_cuenta_memes(ctx):
    """Muestra cuántos memes has solicitado."""
    data = load_data()
    user_id = str(ctx.author.id)
    count = data['user_counts'].get(user_id, 0)
    await ctx.send(f"Has solicitado un total de **{count}** memes.")

@bot.command()
async def top_usuarios_memes(ctx):
    """Muestra el top 5 de usuarios que más memes han solicitado."""
    data = load_data()
    user_counts = data['user_counts']
    
    sorted_users = sorted(user_counts.items(), key=lambda item: item[1], reverse=True)
    
    if not sorted_users:
        return await ctx.send("Todavía no hay estadísticas de usuarios. ¡Sé el primero en pedir un meme!")
        
    embed = discord.Embed(
        title="🏆 Top 5 de Solicitantes de Memes",
        color=discord.Color.gold()
    )
    
    for i, (user_id, count) in enumerate(sorted_users[:5], 1):
        user = bot.get_user(int(user_id))
        if user:
            user_name = user.name
        else:
            user_name = f"Usuario Desconocido ({user_id})"
        embed.add_field(name=f"{i}. {user_name}", value=f"Memes solicitados: {count}", inline=False)
        
    await ctx.send(embed=embed)

bot.run('Tu Token aqui we, no te voy a regalar el mio')
