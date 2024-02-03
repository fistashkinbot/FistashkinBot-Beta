import disnake
from disnake.ext import commands

import config
from config import *


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, inter, error):
        print(error)

        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(
                title="Ошибка!",
                description=f"{inter.author.mention}, у вас нет прав на выполнения этой команды!",
                colour=botmaincolor,
            )
            embed.set_footer(
                text=f"{footerbyriverya4life}", icon_url=avatarbyfooterbyriverya4life
            )
            await inter.send(embed=embed)

        if isinstance(error, commands.CommandNotFound):
            embed = disnake.Embed(
                title="Ошибка!",
                description=f"{inter.author.mention}, данной команды не существует! Посмотри список доступных команд по команде **`{PREFIX}хелп`**!",
                colour=botmaincolor,
            )
            embed.set_footer(
                text=f"{footerbyriverya4life}", icon_url=avatarbyfooterbyriverya4life
            )
            await inter.send(embed=embed)

        if isinstance(error, commands.CommandOnCooldown):
            hour = round(error.retry_after / 3600)
            minute = round(error.retry_after / 60)

            if hour > 0:
                embed = disnake.Embed(
                    title="Эээммм полегче!",
                    description=f"**Воууу, полегче {inter.author.mention}!** Похоже, что ты нарушаешь **кулдаун команд!**\nПовтори через `{str(hour)}` час(ов/а)",
                    colour=botmaincolor,
                )
                embed.set_footer(
                    text=f"{footerbyriverya4life}",
                    icon_url=avatarbyfooterbyriverya4life,
                )
                await inter.send(embed=embed)
            elif minute > 0:
                embed = disnake.Embed(
                    title="Эээммм полегче!",
                    description=f"**Воууу, полегче {inter.author.mention}!** Похоже, что ты нарушаешь **кулдаун команд!**\nПовтори через `{str(minute)}` минут(ы)",
                    colour=botmaincolor,
                )
                embed.set_footer(
                    text=f"{footerbyriverya4life}",
                    icon_url=avatarbyfooterbyriverya4life,
                )
                await inter.send(embed=embed)
            else:
                embed = disnake.Embed(
                    title="Эээммм полегче!",
                    description=f"**Воууу, полегче {inter.author.mention}!** Похоже, что ты нарушаешь **кулдаун команд!**\nПовтори через `{error.retry_after :.0f}` секунд(ы)",
                    colour=botmaincolor,
                )
                embed.set_footer(
                    text=f"{footerbyriverya4life}",
                    icon_url=avatarbyfooterbyriverya4life,
                )
                await inter.send(embed=embed)

        if isinstance(error, commands.errors.MemberNotFound):
            embed = disnake.Embed(
                description=f"{inter.author.mention}, указанный пользователь не найден.",
                colour=botmaincolor,
            )
            embed.set_footer(
                text=f"{footerbyriverya4life}", icon_url=avatarbyfooterbyriverya4life
            )
            await inter.send(embed=embed)

        if isinstance(error, commands.UserInputError):
            embed = disnake.Embed(
                title="Ошибка!",
                description=f"**Правильное использование команды:** `{PREFIX}{inter.command.name}`\n**Example:** `{PREFIX}{inter.command.usage}`",
                colour=botmaincolor,
            )
            embed.set_footer(
                text=f"{footerbyriverya4life}", icon_url=avatarbyfooterbyriverya4life
            )
            await inter.send(embed=embed)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        print(error)

        if isinstance(error, commands.MissingPermissions):
            embed = disnake.Embed(
                title="Ошибка!",
                description=f"{inter.author.mention}, у вас нет прав на выполнения этой команды!",
                colour=botmaincolor,
            )
            embed.set_footer(
                text=f"{footerbyriverya4life}", icon_url=avatarbyfooterbyriverya4life
            )
            await inter.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.CommandNotFound):
            embed = disnake.Embed(
                title="Ошибка!",
                description=f"{inter.author.mention}, данной команды не существует! Посмотри список доступных команд по команде **`{PREFIX}хелп`**!",
                colour=botmaincolor,
            )
            embed.set_footer(
                text=f"{footerbyriverya4life}", icon_url=avatarbyfooterbyriverya4life
            )
            await inter.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.CommandOnCooldown):
            hour = round(error.retry_after / 3600)
            minute = round(error.retry_after / 60)

            if hour > 0:
                embed = disnake.Embed(
                    title="Эээммм полегче!",
                    description=f"**Воууу, полегче {inter.author.mention}!** Похоже, что ты нарушаешь **кулдаун команд!**\nПовтори через `{str(hour)}` час(ов/а)",
                    colour=botmaincolor,
                )
                embed.set_footer(
                    text=f"{footerbyriverya4life}",
                    icon_url=avatarbyfooterbyriverya4life,
                )
                await inter.send(embed=embed, ephemeral=True)
            elif minute > 0:
                embed = disnake.Embed(
                    title="Эээммм полегче!",
                    description=f"**Воууу, полегче {inter.author.mention}!** Похоже, что ты нарушаешь **кулдаун команд!**\nПовтори через `{str(minute)}` минут(ы)",
                    colour=botmaincolor,
                )
                embed.set_footer(
                    text=f"{footerbyriverya4life}",
                    icon_url=avatarbyfooterbyriverya4life,
                )
                await inter.send(embed=embed, ephemeral=True)
            else:
                embed = disnake.Embed(
                    title="Эээммм полегче!",
                    description=f"**Воууу, полегче {inter.author.mention}!** Похоже, что ты нарушаешь **кулдаун команд!**\nПовтори через `{error.retry_after :.0f}` секунд(ы)",
                    colour=botmaincolor,
                )
                embed.set_footer(
                    text=f"{footerbyriverya4life}",
                    icon_url=avatarbyfooterbyriverya4life,
                )
                await inter.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.errors.MemberNotFound):
            embed = disnake.Embed(
                description=f"{inter.author.mention}, указанный пользователь не найден.",
                colour=botmaincolor,
            )
            embed.set_footer(
                text=f"{footerbyriverya4life}", icon_url=avatarbyfooterbyriverya4life
            )
            await inter.send(embed=embed, ephemeral=True)

        if isinstance(error, commands.UserInputError):
            embed = disnake.Embed(
                title="Ошибка!",
                description=f"**Правильное использование команды:** `{PREFIX}{inter.command.name}`\n**Example:** `{PREFIX}{inter.command.usage}`",
                colour=botmaincolor,
            )
            embed.set_footer(
                text=f"{footerbyriverya4life}", icon_url=avatarbyfooterbyriverya4life
            )
            await inter.send(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(Events(bot))
