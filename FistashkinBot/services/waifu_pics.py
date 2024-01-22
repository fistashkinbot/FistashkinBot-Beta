import aiohttp

__all__ = ["get_image"]
__base = "https://api.waifu.pics"


async def get_image(type: str, category: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{__base}/{type}/{category}") as response:
            data = await response.json()
            return data.get("url")
