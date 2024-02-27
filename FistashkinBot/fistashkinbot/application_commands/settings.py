import disnake

from disnake.ext import commands
from utils import enums
from utils import CustomError
from helpers.settings_helper import *


class Settings(commands.Cog, name="⚙️ Настройки"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.color = enums.Color()

    @commands.slash_command(
        name=disnake.Localized("settings", key="SETTING_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows settings view.", key="SETTING_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.default_member_permissions(administrator=True)
    async def settings(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @settings.sub_command(
        name=disnake.Localized("voice", key="SETTING_VOICE_COMMAND_NAME"),
        description=disnake.Localized(
            "Set up private voice rooms for the server.",
            key="SETTING_VOICE_COMMAND_DESCRIPTION",
        ),
    )
    async def voice_settings(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title="Приватные Голосовые Комнаты",
            description="Преимуществом этой функции является возможность создания и настройки приватных голосовых комнат для вашего сервера.\n\n"
            "Чтобы настроить данную функцию нужно:\n"
            "1. Включить режим разработчика в **Настройки -> Расширенные -> Режим разработчика** для копирования ID (Нужно для первого или последнего пункта).\n"
            "2. Создать для этого канал с категорией в которой будут созданы приватные каналы или же установить обычный триггер в существующие.\n"
            "3. Чтобы удалить триггер кликните на менюшку ниже.",
            color=self.color.DARK_GRAY,
        )
        view = TempVoiceButtons(inter)
        message = await inter.edit_original_message(embed=embed, view=view)
        view.message = message

    @settings.sub_command(
        name=disnake.Localized("shop", key="SETTING_SHOP_COMMAND_NAME"),
        description=disnake.Localized(
            "Set up a role store for the server.",
            key="SETTING_SHOP_COMMAND_DESCRIPTION",
        ),
    )
    async def role_shop_settings(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title="Магазин ролей",
            description=f"Было бы круто, если за валюту можно купить крутую роль? {self.bot.user.display_name} это может вам организовать!\n\n"
            "Чтобы настроить магазин нужно:\n"
            "1. Включить режим разработчика в **Настройки -> Расширенные -> Режим разработчика** для копирования ID.\n"
            "2. Добавить роли, указывая за них стоимость.\n"
            "3. Готово!",
            color=self.color.DARK_GRAY,
        )
        view = RoleShopButtons(inter)
        message = await inter.edit_original_message(embed=embed, view=view)
        view.message = message

    @settings.sub_command(
        name=disnake.Localized("logs", key="SETTING_LOGS_COMMAND_NAME"),
        description=disnake.Localized(
            "Setting logs for the server.", key="SETTING_LOGS_COMMAND_DESCRIPTION"
        ),
    )
    async def logging_settings(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title="Логгирование",
            description=f"Логгирование - полезная вещь для модерации сервера. {self.bot.user.display_name} всё это настроит!\n"
            "Пока система логов не будет работать, но вы можете заранее её настроить!\n\n"
            "Чтобы настроить систему логгирования нужно:\n"
            "1. Включить режим разработчика в **Настройки -> Расширенные -> Режим разработчика** для копирования ID.\n"
            "2. Добавить ID канала для логгов.\n"
            "3. Готово!",
            color=self.color.DARK_GRAY,
        )
        view = LogsSetupButtons(inter)
        message = await inter.edit_original_message(embed=embed, view=view)
        view.message = message


def setup(bot):
    bot.add_cog(Settings(bot))
