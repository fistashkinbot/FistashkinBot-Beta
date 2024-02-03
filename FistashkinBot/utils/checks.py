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

    PERMISSIONS = {
        "administrator": "Администратор",
        "ban_members": "Банить участников",
        "kick_members": "Выгонять участников",
        "manage_guild": "Управлять сервером",
        "send_messages": "Отправлять сообщения",
        "manage_members": "Управлять участниками",
        "view_channel": "Просматривать канал",
        "manage_roles": "Управлять ролями",
    }

    async def check_user_bot(self, inter, text):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title=f"{self.otheremojis.WARNING} Ошибка!",
            description=f"❌ Ты не можешь **{text}** {self.bot.user.mention}!",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_user_author(self, inter, text):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title=f"{self.otheremojis.WARNING} Ошибка!",
            description=f"❌ Ты не можешь **{text}** самому себе!",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_user_role(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title=f"{self.otheremojis.WARNING} Ошибка!",
            description=f"❌ Ты не можешь использовать данную команду на участников с более высокой ролью!",
            colour=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_bot_role(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title=f"{self.otheremojis.WARNING} Ошибка!",
            description=f"❌ Роль этого бота недостаточно высока, чтобы использовать данную команду!",
            colour=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_member_timeout(self, inter, member):
        if member.current_timeout:
            await inter.response.defer(ephemeral=True)
            embed = disnake.Embed(
                title=f"{self.otheremojis.WARNING} Ошибка!",
                description=f"❌ Участник уже находится в тайм-ауте!",
                colour=self.color.RED,
            )
            await inter.edit_original_message(embed=embed)

        if member.current_timeout == None:
            await inter.response.defer(ephemeral=True)
            embed = disnake.Embed(
                title=f"{self.otheremojis.WARNING} Ошибка!",
                description=f"❌ Участник не находится в тайм-ауте!",
                colour=self.color.RED,
            )
            await inter.edit_original_message(embed=embed)

    async def check_timeout_time(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title=f"{self.otheremojis.WARNING} Ошибка!",
            description=f"❌ Ты не можешь замутить участника больше чем **28 дней**!",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_bot(self, inter, member):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title=f"{self.otheremojis.WARNING} Ошибка!",
            description=f"❌ Ты не можешь взаимодействовать с ботом {member.mention}",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_amount_is_none(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title=f"{self.otheremojis.WARNING} Ошибка!",
            description=f"❌ Укажите сумму **{self.economy.CURRENCY_NAME}**, которую желаете начислить на счет участника!",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_unknown(self, inter, text):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title=f"{self.otheremojis.WARNING} Ошибка!",
            description=f"❌ {text}",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_value_error(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            title=f"{self.otheremojis.WARNING} Ошибка!",
            description="❌ Вы ввели некорректные данные, попробуйте ещё раз.",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_interaction_rp(self, inter, text):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description=f"😥 Ты не можешь сам себя **{text}**!",
            color=self.color.RED,
        )
        embed.set_image(url=random.choice(self.rp.SAD_ERROR_IMAGES))
        await inter.edit_original_message(embed=embed)

    # Event handler error
    async def check_missing_permissions(self, inter, error):
        await inter.response.defer(ephemeral=True)
        permission_list = ", ".join(
            [self.PERMISSIONS.get(i, i) for i in error.missing_permissions]
        )
        embed = disnake.Embed(
            description=f"❌ У вас нет прав на выполнения этой команды!\nНедостающие права: {permission_list}",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_not_owner(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description="❌ Ты не являешься владельцем или разработчиком бота, поэтому команда не доступна!",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_cooldown(self, inter, text):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description=text,
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    async def check_member_not_found(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description="❌ Указанный пользователь не найден.",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    # NSFW Check
    async def check_is_nsfw(self, inter):
        await inter.response.defer(ephemeral=True)
        channels = list(
            map(
                lambda n: n.mention, filter(lambda x: x.nsfw, inter.guild.text_channels)
            )
        )
        channel_list = " ".join(channels)
        if len(channels) != 0:
            description = f"❌ Эта команда доступна только в каналах с пометкой NSFW!\nПоэтому воспользуйтесь одним из NSFW-каналов: {channel_list}"
        else:
            description = f"❌ Эта команда доступна только в каналах с пометкой NSFW!"

        embed = disnake.Embed(
            description=description,
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    # WIP
    async def check_is_wip(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description=f"❌ Эта функция находится в стадии разработки!\n"
            f"Пожалуйста, следите за обновлениями на наших ветках обновлениях [здесь]({self.main.GITHUB_REPOSITORY})!",
            color=self.color.RED,
        )
        await inter.edit_original_message(embed=embed)

    # Unknown error
    async def check_unknown_exception(self, inter, text):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description=text,
            color=self.color.RED,
        )
        view = links.Support_Link()
        await inter.edit_original_message(embed=embed, view=view)
