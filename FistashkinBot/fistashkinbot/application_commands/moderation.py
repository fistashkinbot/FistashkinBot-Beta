import disnake
import random
import datetime

from disnake.ext import commands
from utils import main, enums, constant, database
from utils import CustomError
from helpers.mod_helper import ModerationHelper


class Moderation(commands.Cog, name="👮🏻 Модерация"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.main = main.MainSettings()
        self.color = enums.Color()
        self.otheremojis = constant.OtherEmojis()
        self.db = database.DataBase()
        self.enum = enums.Enum()

    @commands.slash_command(
        name=disnake.Localized("timeout", key="MUTE_COMMAND_NAME"),
        description=disnake.Localized(
            "Sends a user to timeout.", key="MUTE_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    # @commands.default_member_permissions(moderate_members=True)
    async def timeout(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
        time: str = commands.Param(
            name=disnake.Localized("time", key="MUTE_COMMAND_TEXT_NAME"),
            description=disnake.Localized(
                "Specify the time (Example: 10m, where s - seconds, m - minutes, h - hours, d - days).",
                key="MUTE_COMMAND_TEXT_DESCRIPTION",
            ),
        ),
        reason: str = commands.Param(
            lambda reason: "не указано",
            name=disnake.Localized("reason", key="TARGET_REASON_NAME"),
            description=disnake.Localized(
                "State the reason.", key="TARGET_REASON_DESCRIPTION"
            ),
        ),
    ):
        d = time[-1:]
        timemute = int(time[:-1])

        if member == self.bot.user:
            raise CustomError(
                f"❌ Ты не можешь **выдавать блокировку чата** {self.bot.user.mention}!"
            )

        elif member == inter.author:
            raise CustomError(
                "❌ Ты не можешь **выдавать блокировку чата** самому себе!"
            )

        elif member.top_role >= inter.author.top_role:
            raise CustomError(
                "❌ Ты не можешь использовать данную команду на участников с более высокой ролью!"
            )

        elif member.top_role >= inter.guild.me.top_role:
            raise CustomError(
                "❌ Роль этого бота недостаточно высока, чтобы использовать данную команду!"
            )

        elif member.current_timeout:
            raise CustomError(f"❌ Участник {member.mention} уже находится в тайм-ауте!")

        elif member.bot:
            raise CustomError("❌ Ты не можешь взаимодействовать с ботами!")

        if d == "s" or d == "с":
            if timemute > 2419000:
                raise CustomError(
                    "❌ Ты не можешь замутить участника больше чем на **28 дней**!"
                )

            return await ModerationHelper.check_time_muted(
                self, inter, member, time, reason, send_to_member=True
            )

        elif d == "m" or d == "м" or d == "х":
            if timemute > 40320:
                raise CustomError(
                    "❌ Ты не можешь замутить участника больше чем на **28 дней**!"
                )

            return await ModerationHelper.check_time_muted(
                self, inter, member, time, reason, send_to_member=True
            )

        elif d == "h" or d == "ч" or d == "г":
            if timemute > 672:
                raise CustomError(
                    "❌ Ты не можешь замутить участника больше чем на **28 дней**!"
                )

            return await ModerationHelper.check_time_muted(
                self, inter, member, time, reason, send_to_member=True
            )

        elif d == "d" or d == "д":
            if timemute > 28:
                raise CustomError(
                    "❌ Ты не можешь замутить участника больше чем на **28 дней**!"
                )

            return await ModerationHelper.check_time_muted(
                self, inter, member, time, reason, send_to_member=True
            )

    @commands.slash_command(
        name=disnake.Localized("untimeout", key="UNMUTE_COMMAND_NAME"),
        description=disnake.Localized(
            "Removes timeout from the user.", key="UNMUTE_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(moderate_members=True)
    @commands.bot_has_permissions(moderate_members=True)
    # @commands.default_member_permissions(moderate_members=True)
    async def untimeout(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
        reason: str = commands.Param(
            lambda reason: "не указано",
            name=disnake.Localized("reason", key="TARGET_REASON_NAME"),
            description=disnake.Localized(
                "State the reason.", key="TARGET_REASON_DESCRIPTION"
            ),
        ),
    ):
        if member.current_timeout == None:
            raise CustomError("❌ Участник не находится в тайм-ауте!")

        elif member.top_role >= inter.author.top_role:
            raise CustomError(
                "❌ Ты не можешь использовать данную команду на участников с более высокой ролью!"
            )

        elif member.top_role >= inter.guild.me.top_role:
            raise CustomError(
                "❌ Роль этого бота недостаточно высока, чтобы использовать данную команду!"
            )

        elif member.bot:
            raise CustomError("❌ Ты не можешь взаимодействовать с ботами!")

        return await ModerationHelper.send_embed_punishment(
            self,
            inter,
            member,
            reason,
            punish=f"✅ С участника {member.mention} сняты ограничения! 🐵",
            dm_punish=f"Вам были сняты ограничения на сервере `{inter.guild.name}`!",
            send_to_member=True,
        )

    @commands.slash_command(
        name=disnake.Localized("kick", key="KICK_COMMAND_NAME"),
        description=disnake.Localized(
            "Kicks the specified user from the server with the possibility of returning.",
            key="KICK_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    # @commands.default_member_permissions(kick_members=True)
    async def kick(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
        reason: str = commands.Param(
            lambda reason: "не указано",
            name=disnake.Localized("reason", key="TARGET_REASON_NAME"),
            description=disnake.Localized(
                "State the reason.", key="TARGET_REASON_DESCRIPTION"
            ),
        ),
    ):
        if member == self.bot.user:
            raise CustomError(f"❌ Ты не можешь **кикнуть** {self.bot.user.mention}!")

        elif member == inter.author:
            raise CustomError("❌ Ты не можешь **кикнуть** самому себе!")

        elif member.top_role >= inter.author.top_role:
            raise CustomError(
                "❌ Ты не можешь использовать данную команду на участников с более высокой ролью!"
            )

        elif member.top_role >= inter.guild.me.top_role:
            raise CustomError(
                "❌ Роль этого бота недостаточно высока, чтобы использовать данную команду!"
            )

        elif member.bot:
            raise CustomError("❌ Ты не можешь взаимодействовать с ботами!")

        return await ModerationHelper.send_embed_punishment(
            self,
            inter,
            member,
            reason,
            punish=f"✅ Участник {member.mention} был изгнан с сервера.",
            dm_punish=f"Вы были изгнаны с сервера `{inter.guild.name}`!",
            send_to_member=True,
        )

    @commands.slash_command(
        name=disnake.Localized("ban", key="BAN_COMMAND_NAME"),
        description=disnake.Localized(
            "Banishes the specified user from the server permanently.",
            key="BAN_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    # @commands.default_member_permissions(ban_members=True)
    async def ban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
        reason: str = commands.Param(
            lambda reason: "не указано",
            name=disnake.Localized("reason", key="TARGET_REASON_NAME"),
            description=disnake.Localized(
                "State the reason.", key="TARGET_REASON_DESCRIPTION"
            ),
        ),
    ):
        if member == self.bot.user:
            raise CustomError(
                f"❌ Ты не можешь **выдавать блокировку** {self.bot.user.mention}!"
            )

        elif member == inter.author:
            raise CustomError("❌ Ты не можешь **выдавать блокировку** самому себе!")

        elif member.top_role >= inter.author.top_role:
            raise CustomError(
                "❌ Ты не можешь использовать данную команду на участников с более высокой ролью!"
            )

        elif member.top_role >= inter.guild.me.top_role:
            raise CustomError(
                "❌ Роль этого бота недостаточно высока, чтобы использовать данную команду!"
            )

        elif member.bot:
            raise CustomError("❌ Ты не можешь взаимодействовать с ботами!")

        return await ModerationHelper.send_embed_punishment(
            self,
            inter,
            member,
            reason,
            punish=f"✅ Участник {member.mention} был забанен.",
            dm_punish=f"Вы были забанены на сервере `{inter.guild.name}`!",
            send_to_member=True,
        )

    async def autocomplete_unban(
        self, inter: disnake.ApplicationCommandInteraction, string: str
    ):
        return [
            disnake.OptionChoice(
                name=f"{ban.user.name} ({ban.user.id})", value=str(ban.user.id)
            )
            async for ban in inter.guild.bans(limit=200)
        ]

    @commands.slash_command(
        name=disnake.Localized("unban", key="UNBAN_COMMAND_NAME"),
        description=disnake.Localized(
            "Unbans the specified user on the server by his ID, name or tag.",
            key="UNBAN_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    # @commands.default_member_permissions(ban_members=True)
    async def unban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.User = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
            autocomplete=autocomplete_unban,
        ),
        reason: str = commands.Param(
            lambda reason: "не указано",
            name=disnake.Localized("reason", key="TARGET_REASON_NAME"),
            description=disnake.Localized(
                "State the reason.", key="TARGET_REASON_DESCRIPTION"
            ),
        ),
    ):
        if user == self.bot.user:
            raise CustomError(
                f"❌ Ты не можешь **выдавать разблокировку** {self.bot.user.mention}!"
            )

        elif user == inter.author:
            raise CustomError("❌ Ты не можешь **выдавать разблокировку** самому себе!")

        elif user.bot:
            raise CustomError("❌ Ты не можешь взаимодействовать с ботами!")

        try:
            await inter.response.defer(ephemeral=False)
            await inter.guild.fetch_ban(user)
            await inter.guild.unban(user=user, reason=reason)

            embed = disnake.Embed(
                description=f"✅ Участник {user.mention} был разбанен.",
                color=self.color.MAIN,
                timestamp=inter.created_at,
            )
            embed.add_field(name="Модератор", value=inter.author.mention)
            embed.add_field(name="Причина", value=reason)

            embed.set_thumbnail(url=user.display_avatar.url)
            embed.set_footer(
                text="Команда по безопасности Discord сервера",
                icon_url=inter.guild.icon.url if inter.guild.icon else None,
            )
            await inter.edit_original_message(embed=embed)
        except:
            raise CustomError(
                f"❌ Участник **{user.mention}** отсутствует в списке банов или произошла ошибка!"
            )

    @commands.slash_command(
        name=disnake.Localized("delay", key="DELAY_CHAT_COMMAND_NAME"),
        description=disnake.Localized(
            "Sets a delay for chatting.", key="DELAY_CHAT_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    # @commands.default_member_permissions(manage_channels=True)
    async def setdelay(
        self,
        inter: disnake.ApplicationCommandInteraction,
        seconds: int = commands.Param(
            name=disnake.Localized("seconds", key="DELAY_CHAT_COMMAND_TEXT_NAME"),
            description=disnake.Localized(
                "Specify the delay time in seconds.",
                key="DELAY_CHAT_COMMAND_TEXT_DESCRIPTION",
            ),
        ),
    ):
        if 0 > seconds:
            raise CustomError(
                f"❌ Значение не может быть меньше нуля!"
            )
            
        if seconds == 0:
            await inter.response.defer(ephemeral=False)
            await inter.channel.edit(slowmode_delay=seconds)
            embed = disnake.Embed(
                description=f"{inter.author.mention} убрал задержку в данном канале!",
                color=self.color.MAIN,
                timestamp=inter.created_at,
            )
            embed.set_author(
                name="Задержка в канале", icon_url=inter.author.display_avatar.url
            )
            embed.set_footer(
                text="Команда по безопасности Discord сервера",
                icon_url=inter.guild.icon.url if inter.guild.icon else None,
            )
            await inter.edit_original_message(embed=embed)
        else:
            await inter.response.defer(ephemeral=False)
            await inter.channel.edit(slowmode_delay=seconds)
            embed = disnake.Embed(
                description=f"{inter.author.mention} установил задержку чата в **`{seconds}`** секунд!",
                color=self.color.MAIN,
                timestamp=inter.created_at,
            )
            embed.set_author(
                name="Задержка в канале", icon_url=inter.author.display_avatar.url
            )
            embed.set_footer(
                text="Команда по безопасности Discord сервера",
                icon_url=inter.guild.icon.url if inter.guild.icon else None,
            )
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("clear", key="CLEAR_COMMAND_NAME"),
        description=disnake.Localized(
            "Clears a specified number of messages in a channel.",
            key="CLEAR_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    # @commands.default_member_permissions(manage_messages=True)
    async def clear(
        self,
        inter: disnake.ApplicationCommandInteraction,
        amount: int = commands.Param(
            name=disnake.Localized("quantity", key="CLEAR_COMMAND_TEXT_NAME"),
            description=disnake.Localized(
                "Specify the number of messages.", key="CLEAR_COMMAND_TEXT_DESCRIPTION"
            ),
        ),
    ):
        await inter.response.defer(ephemeral=True)
        clear_amount = self.enum.format_large_number(amount)
        embed = disnake.Embed(
            description=f"{inter.author.mention}, было очищено **{clear_amount}** сообщений(е)",
            color=self.color.MAIN,
        )
        embed.set_author(name="Очистка чата", icon_url=inter.author.display_avatar.url)
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)
        await inter.channel.purge(limit=int(amount))
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("warn", key="GIVE_WARN_COMMAND_NAME"),
        description=disnake.Localized(
            "Issue a warning to the user.", key="GIVE_WARN_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    # @commands.default_member_permissions(ban_members=True)
    async def give_warn(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
        reason: str = commands.Param(
            lambda reason: "не указано",
            name=disnake.Localized("reason", key="TARGET_REASON_NAME"),
            description=disnake.Localized(
                "State the reason.", key="TARGET_REASON_DESCRIPTION"
            ),
        ),
    ):
        if member == self.bot.user:
            raise CustomError(
                f"❌ Ты не можешь **выдавать предупреждения** {self.bot.user.mention}!"
            )

        elif member == inter.author:
            raise CustomError("❌ Ты не можешь **выдавать предупреждения** самому себе!")

        elif member.top_role >= inter.author.top_role:
            raise CustomError(
                "❌ Ты не можешь использовать данную команду на участников с более высокой ролью!"
            )

        elif member.top_role >= inter.guild.me.top_role:
            raise CustomError(
                "❌ Роль этого бота недостаточно высока, чтобы использовать данную команду!"
            )

        elif member.bot:
            raise CustomError("❌ Ты не можешь взаимодействовать с ботами!")

        warns = await self.db.get_warns(member)
        warnnum = 0
        if warns:
            for table in warns:
                warnnum += 1

        if warnnum == 3:
            await self.db.remove_warns(member=member)
            await ModerationHelper.send_embed_punishment(
                self,
                inter,
                member,
                reason="3/3 предупреждений",
                punish=f"✅ Участник {member.mention} был забанен.",
                dm_punish=f"Вы были забанены на сервере `{inter.guild.name}`!",
                send_to_member=True,
            )
        else:
            return await ModerationHelper.send_embed_punishment(
                self,
                inter,
                member,
                reason,
                punish=f"✅ Участник {member.mention} получил предупреждение!",
                dm_punish=f"Вы получили предупреждение на сервере `{inter.guild.name}`!",
                send_to_member=True,
            )

    @commands.slash_command(
        name=disnake.Localized("warns", key="WARNS_COMMAND_NAME"),
        description=disnake.Localized(
            "Displays all warnings issued to the user.", key="WARNS_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def member_warns(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            lambda inter: inter.author,
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        if not member:
            member = inter.author

        elif member.bot:
            raise CustomError("❌ Ты не можешь взаимодействовать с ботами!")

        await inter.response.defer(ephemeral=False)
        warns = await self.db.get_warns(member)
        embed = disnake.Embed(color=self.color.MAIN)
        embed.set_author(
            name=f"Предупреждения {member.display_name}",
            icon_url=member.display_avatar.url,
        )
        embed.set_thumbnail(url=member.display_avatar.url)

        if warns:
            warnnum = 0
            for table in warns:
                warnnum += 1
                reason = table[0]
                timestamp = disnake.utils.format_dt(table[1], style="f")
                warner = inter.guild.get_member(table[2])
                embed.add_field(
                    name=f"`Пред #{warnnum}`",
                    value=f"**Выдал:** {warner.mention} | **Дата:** {timestamp}\n"
                    f"**Причина:** {reason}",
                    inline=False,
                )
        else:
            embed.description = "Предупреждения отсутствуют."

        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("remwarn", key="REMOVE_WARNS_COMMAND_NAME"),
        description=disnake.Localized(
            "Removes all warnings issued to the user.",
            key="REMOVE_WARNS_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    # @commands.default_member_permissions(ban_members=True)
    async def remove_member_warns(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            lambda inter: inter.author,
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        await inter.response.defer(ephemeral=False)
        if not member:
            member = inter.author

        elif member.bot:
            raise CustomError("❌ Ты не можешь взаимодействовать с ботами!")

        await self.db.remove_warns(member=member)
        embed = disnake.Embed(
            description=f"✅ Предупреждения {member.mention} были успешно сброшены.",
            color=self.color.MAIN,
        )
        embed.set_author(
            name=f"Сброс предупреждений", icon_url=member.display_avatar.url
        )
        await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
