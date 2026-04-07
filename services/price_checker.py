import aiohttp
from config import RAPIDAPI_KEY, RAPIDAPI_HOST

async def get_price(url: str):
    """
    Holt den aktuellen Preis eines Produkts von der Idealo-API.
    """
    api_url = "https://idealo-api.p.rapidapi.com/price"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": RAPIDAPI_HOST
    }
    params = {"url": url}

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, headers=headers, params=params) as resp:
            data = await resp.json()
            price = data.get("price")  
            return price