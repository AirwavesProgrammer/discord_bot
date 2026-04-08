import discord
from discord.ext import commands, tasks
import asyncio
import sqlite3

from config import DISCORD_TOKEN, DISCORD_CHANNEL_ID
from services.price_checker import get_price
from services.portfolio_checker import get_stock_price
from database.db import get_all_products, get_all_stocks

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ist online als {bot.user}")
    price_check_loop.start() 

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

@tasks.loop(minutes=1)
async def price_check_loop():
    products = get_all_products()
    stocks = get_all_stocks()

    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if not channel:
        return

    for url, target_price in products:
        current_price = await get_price(url)
        if current_price is None:
            continue
        if current_price <= target_price:
            await channel.send(
                f"Deal Alert!\nURL: {url}\nAktueller Preis: {current_price}€ (Ziel: {target_price}€)"
            )

    for stock_symbol, target_price in stocks:
        current_price = get_stock_price(stock_symbol)
        if current_price is None:
            continue
        await channel.send(
            f"Aktien-Alert!\nAktueller Preis von {stock_symbol}: {current_price}\nZiel: {target_price} USD"
        )

async def main():
    async with bot:
        await bot.load_extension("cogs.track")
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())