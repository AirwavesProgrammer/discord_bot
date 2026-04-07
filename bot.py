import discord
from discord.ext import commands, tasks
import asyncio
import sqlite3

from config import DISCORD_TOKEN, DISCORD_CHANNEL_ID
from services.price_checker import get_price

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot ist online als {bot.user}")
    price_check_loop.start()  # Background-Task starten

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@tasks.loop(minutes=1)
async def price_check_loop():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT url, target_price FROM products")
    products = cursor.fetchall()
    conn.close()

    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        return

    for url, target_price in products:
        current_price = await get_price(url)
        if current_price is None:
            continue  # API konnte Preis nicht liefern
        if current_price <= target_price:
            await channel.send(
                f"💰 Deal Alert!\nURL: {url}\nAktueller Preis: {current_price}€ (Ziel: {target_price}€)"
            )

async def main():
    async with bot:
        # Track Command laden
        await bot.load_extension("cogs.track")
        # Bot starten
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())