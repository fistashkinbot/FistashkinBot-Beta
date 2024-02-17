import disnake
import datetime
import random

from disnake.ext import commands
from utils import main, enums, constant, database, links


class Checks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.main = main.MainSettings()
        self.color = enums.Color()
        self.otheremojis = constant.OtherEmojis()
        self.db = database.DataBase()

    # WIP
    async def check_is_wip(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description=f"❌ Эта функция находится в стадии разработки!\n"
            f"Пожалуйста, следите за обновлениями на наших ветках обновлениях [здесь]({self.main.GITHUB_REPOSITORY})!",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)
