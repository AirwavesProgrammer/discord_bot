from discord.ext import commands
import sqlite3
from services.portfolio_checker import get_stock_price  # Importiere get_stock_price

class Track(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def track(self, ctx, url: str, preis: float):
        """Speichert ein Produkt mit Zielpreis in der Datenbank."""
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (url, target_price) VALUES (?, ?)",
            (url, preis)
        )
        conn.commit()
        conn.close()
        await ctx.send(f"Produkt gespeichert!\nURL: {url}\nZielpreis: {preis}€")

    @commands.command()
    async def list(self, ctx):
        """Zeigt alle gespeicherten Produkte an."""
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT id, url, target_price FROM products")
        products = cursor.fetchall()
        conn.close()

        if not products:
            await ctx.send("Es sind noch keine Produkte gespeichert.")
            return

        message = "**Gespeicherte Produkte:**\n"
        for pid, url, price in products:
            message += f"ID: {pid} | URL: {url} | Zielpreis: {price}€\n"

        await ctx.send(message)

    @commands.command()
    async def remove(self, ctx, product_id: int):
        """Löscht ein Produkt anhand seiner ID aus der Datenbank."""
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM products WHERE id = ?", (product_id,))
        result = cursor.fetchone()

        if not result:
            await ctx.send(f"Kein Produkt mit ID {product_id} gefunden.")
            conn.close()
            return

        url = result[0]
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        conn.close()

        await ctx.send(f"Produkt entfernt:\nURL: {url}\nID: {product_id}")

    @commands.command()
    async def aktie(self, ctx, symbol: str):
        """Zeigt den aktuellen Aktienkurs eines Symbols."""
        price = get_stock_price(symbol)
        await ctx.send(price)

# Setup-Funktion zum Laden der Cog
async def setup(bot):
    await bot.add_cog(Track(bot))