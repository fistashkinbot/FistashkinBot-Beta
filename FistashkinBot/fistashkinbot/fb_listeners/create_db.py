import disnake
import random

from disnake.ext import commands
from utils import database, constant, enums, main
from loguru import logger


class DB_Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = database.DataBase()
        self.otheremojis = constant.OtherEmojis()
        self.color = enums.Color()
        self.economy = main.EconomySystem(self.bot)
        self.enum = enums.Enum()

    @commands.Cog.listener(disnake.Event.ready)
    async def on_ready(self):
        await self.db.create_table()
        logger.info(f"[DATABASE] Таблицы успешно созданы!")

        for guild in self.bot.guilds:
            for member in guild.members:
                await self.db.insert_new_member(member)
        logger.info(f"{len(guild.members)} участников было добавлено в базу данных!")

    @commands.Cog.listener(disnake.Event.member_join)
    async def on_member_join(self, member):
        await self.db.insert_new_member(member)
        logger.info(
            f"Участник {member} (ID: {member.id}, Guild: {member.guild.name}, GID: {member.guild.id}) был добавлен в базу данных!"
        )

    @commands.Cog.listener(disnake.Event.guild_join)
    async def on_guild_join(self, guild):
        for member in guild.members:
            await self.db.insert_new_member(member)
        logger.info(
            f"Сервер {guild.name} ({guild.id}) был добавлен в базу данных! Добавлено новых участников: {len(guild.members)}"
        )

    @commands.Cog.listener(disnake.Event.slash_command_completion)
    @commands.Cog.listener(disnake.Event.user_command_completion)
    async def on_command_completion(self, inter: disnake.ApplicationCommandInteraction):
        logger.info(
            f"use: {inter.application_command.qualified_name}, user: {inter.author.name} ({inter.author.id}), guild: {inter.guild.name} ({inter.guild.id})"
        )
        return await self.db.insert_command_count()


def setup(bot):
    bot.add_cog(DB_Event(bot))
