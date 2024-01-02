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
        self.rp = constant.RolePlay()
        self.db = database.DataBase()

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

    async def check_time_muted(
        self, inter, member, time, reason, send_to_member: bool = False
    ):
        await inter.response.defer(ephemeral=False)
        d = time[-1:]
        timemute = int(time[:-1])

        if d == "s" or d == "с":
            dynamic_durations = datetime.datetime.now() + datetime.timedelta(
                seconds=int(timemute)
            )

        if d == "m" or d == "м":
            dynamic_durations = datetime.datetime.now() + datetime.timedelta(
                minutes=int(timemute)
            )

        if d == "h" or d == "ч":
            dynamic_durations = datetime.datetime.now() + datetime.timedelta(
                hours=int(timemute)
            )

        if d == "d" or d == "д":
            dynamic_durations = datetime.datetime.now() + datetime.timedelta(
                days=int(timemute)
            )

        dynamic_time = disnake.utils.format_dt(dynamic_durations, style="R")

        embed = disnake.Embed(
            description=f"✅ Участник {member.mention} замьючен! 🙊",
            color=self.color.MAIN,
            timestamp=inter.created_at,
        )
        embed.add_field(name="Модератор", value=inter.author.mention, inline=True)
        embed.add_field(name="Наказание будет снято", value=dynamic_time, inline=True)
        embed.add_field(name="Причина", value=reason, inline=False)

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(
            text="Команда по безопасности Discord сервера",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )

        dm_embed = disnake.Embed(
            description=f"Вам была выдана заглушка чата на сервере `{inter.guild.name}`!",
            color=self.color.MAIN,
            timestamp=inter.created_at,
        )

        dm_embed.add_field(
            name="Модератор",
            value=f"{inter.author.mention}\n`[ID: {inter.author.id}]`",
            inline=True,
        )
        dm_embed.add_field(
            name="Наказание будет снято", value=dynamic_time, inline=True
        )
        dm_embed.add_field(name="Причина", value=reason, inline=False)

        dm_embed.set_thumbnail(url=member.display_avatar.url)
        dm_embed.set_footer(
            text="Команда по безопасности Discord сервера",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )

        await member.timeout(until=dynamic_durations, reason=reason)
        if send_to_member == True:
            await member.send(
                embed=dm_embed,
                components=[
                    disnake.ui.Button(
                        label=f"Отправлено с {inter.guild.name}",
                        emoji="📨",
                        style=disnake.ButtonStyle.gray,
                        disabled=True,
                    )
                ],
            )
        else:
            pass
        await inter.edit_original_message(embed=embed)

    async def send_embed_punishment(
        self,
        inter,
        member: disnake.Member,
        reason,
        punish,
        dm_punish,
        send_to_member: bool = False,
    ):
        await inter.response.defer(ephemeral=False)

        embed = disnake.Embed(
            description=punish,
            color=self.color.MAIN,
            timestamp=inter.created_at,
        )

        embed.add_field(name="Модератор", value=inter.author.mention)
        embed.add_field(name="Причина", value=reason)

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(
            text="Команда по безопасности Discord сервера",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )

        dm_embed = disnake.Embed(
            description=dm_punish,
            color=self.color.MAIN,
            timestamp=inter.created_at,
        )

        dm_embed.add_field(
            name="Модератор", value=f"{inter.author.mention}\n`[ID: {inter.author.id}]`"
        )
        dm_embed.add_field(name="Причина", value=reason)

        dm_embed.set_footer(
            text="Команда по безопасности Discord сервера",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )

        if send_to_member == True:
            await member.send(
                embed=dm_embed,
                components=[
                    disnake.ui.Button(
                        label=f"Отправлено с {inter.guild.name}",
                        emoji="📨",
                        style=disnake.ButtonStyle.gray,
                        disabled=True,
                    )
                ],
            )
        else:
            pass

        if punish == f"✅ Участник {member.mention} был забанен.":
            await inter.guild.ban(user=member, reason=reason)
        elif punish == f"✅ Участник {member.mention} был изгнан с сервера.":
            await inter.guild.kick(user=member, reason=reason)
        elif punish == f"✅ С участника {member.mention} сняты ограничения! 🐵":
            await member.timeout(until=None, reason=reason)
        elif punish == f"✅ Участник {member.mention} получил предупреждение!":
            await self.db.add_warn(member, inter.author.id, reason)

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

    # event errors
    async def check_missing_permissions(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description="❌ У вас нет прав на выполнения этой команды!",
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

    async def check_bot_missing_permissions(self, inter):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description="❌ Недостаточно прав у бота!",
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

    async def check_unknown_exception(self, inter, text):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description=text,
            color=self.color.RED,
        )
        view = links.Support_Link()
        await inter.edit_original_message(embed=embed, view=view)
