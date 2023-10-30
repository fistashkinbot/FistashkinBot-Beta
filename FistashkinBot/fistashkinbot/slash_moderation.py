import disnake
import random
import datetime

from disnake.ext import commands
from utils import main, enums, constant, checks


class Moderation(commands.Cog, name="Модерация"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.main = main.MainSettings()
        self.color = enums.Color()
        self.otheremojis = constant.OtherEmojis()
        self.checks = checks.Checks(self.bot)

    @commands.slash_command(
        name="мьют",
        description="Отправляет участника подумать о своём поведении.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(moderate_members=True)
    @commands.default_member_permissions(moderate_members=True)
    async def timeout(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
        time: str = commands.Param(
            name="время",
            description="Укажите время (Пример: 10м, где с - секунды, м - минуты, ч - часы, д - дни)",
        ),
        reason: str = commands.Param(
            lambda reason: "не указано", name="причина", description="Укажите причину"
        ),
    ):
        d = time[-1:]
        timemute = int(time[:-1])

        if member == self.bot.user:
            return await self.checks.check_user_bot(
                inter, text="выдавать блокировку чата"
            )

        if member == inter.author:
            return await self.checks.check_user_author(
                inter, text="выдавать блокировку чата"
            )

        if member.top_role >= inter.author.top_role:
            return await self.checks.check_user_role(inter)

        if member.top_role >= inter.guild.me.top_role:
            return await self.checks.check_bot_role(inter)

        if member.current_timeout:
            return await self.checks.check_member_timeout(inter, member)

        if d == "s" or d == "с":
            if timemute > 2419000:
                return await self.checks.check_timeout_time(inter)

            else:
                return await self.checks.check_time_muted(inter, member, time, reason)

        if d == "m" or d == "м":
            if timemute > 40320:
                return await self.checks.check_timeout_time(inter)

            else:
                return await self.checks.check_time_muted(inter, member, time, reason)

        if d == "h" or d == "ч":
            if timemute > 672:
                return await self.checks.check_timeout_time(inter)

            else:
                return await self.checks.check_time_muted(inter, member, time, reason)

        if d == "d" or d == "д":
            if timemute > 28:
                return await self.checks.check_timeout_time(inter)

            else:
                return await self.checks.check_time_muted(inter, member, time, reason)

    @commands.slash_command(
        name="размьют",
        description="Снимает наказание с участника.",
        dm_permission=False,
    )
    @commands.has_permissions(moderate_members=True)
    @commands.default_member_permissions(moderate_members=True)
    async def untimeout(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
        reason=commands.Param(
            lambda reason: "не указано", name="причина", description="Укажите причину"
        ),
    ):
        if member.current_timeout == None:
            return await self.checks.check_member_timeout(inter, member)

        else:
            return await self.checks.send_embed_punishment(
                inter, member, reason, punish="🥳 С участника была снята заглушка чата", 
                set_author_punish="Вам была снята заглушка чата"
            )

    @commands.slash_command(
        name="кик",
        description="Изгоняет указанного участника с сервера с возможностью возвращения.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.default_member_permissions(kick_members=True)
    async def kick(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
        reason=commands.Param(
            lambda reason: "не указано", name="причина", description="Укажите причину"
        ),
    ):
        if member == self.bot.user:
            return await self.checks.check_user_bot(inter, text="кикнуть")

        if member == inter.author:
            return await self.checks.check_user_author(inter, text="кикнуть")

        if member.top_role >= inter.author.top_role:
            return await self.checks.check_user_role(inter)

        if member.top_role >= inter.guild.me.top_role:
            return await self.checks.check_bot_role(inter)

        else:
            return await self.checks.send_embed_punishment(
                inter,
                member,
                reason,
                punish="💨 Кик",
                set_author_punish="Вы были кикнуты",
            )

    @commands.slash_command(
        name="бан",
        description="Изгоняет указанного участника с сервера навсегда.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.default_member_permissions(ban_members=True)
    async def ban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
        reason=commands.Param(
            lambda reason: "не указано", name="причина", description="Укажите причину"
        ),
    ):
        if member == self.bot.user:
            return await self.checks.check_user_bot(inter, text="выдавать блокировку")

        if member == inter.author:
            return await self.checks.check_user_author(
                inter, text="выдавать блокировку"
            )

        if member.top_role >= inter.author.top_role:
            return await self.checks.check_user_role(inter)

        if member.top_role >= inter.guild.me.top_role:
            return await self.checks.check_bot_role(inter)

        else:
            return await self.checks.send_embed_punishment(
                inter,
                member,
                reason,
                punish="🕯 Блокировка",
                set_author_punish="Вам выдана блокировка",
            )

    @commands.slash_command(
        name="разбан",
        description="Разбанивает указанного участника на сервере по его ID, имени или тегу.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    @commands.default_member_permissions(ban_members=True)
    async def unban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.User = commands.Param(
            name="участник", description="Выбор участника"
        ),
        reason=commands.Param(
            lambda reason: "не указано", name="причина", description="Укажите причину"
        ),
    ):
        await inter.response.defer(ephemeral=False)
        embed = disnake.Embed(
            title="🥳 Разбан",
            description=f"**Пользователь:** {user.mention}\n"
            f"**Модератор:** {inter.author.mention}\n"
            f"**Причина:** `{reason}`",
            color=self.color.MAIN,
            timestamp=inter.created_at,
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_footer(
            text="Команда по безопасности Discord сервера",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )

        await inter.edit_original_message(embed=embed)
        await inter.guild.unban(user=user, reason=reason)

    @commands.slash_command(
        name="создатьроль",
        description="Создание роли на сервере.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.default_member_permissions(administrator=True)
    async def create_role(
        self,
        inter: disnake.ApplicationCommandInteraction,
        name: str = commands.Param(name="название", description="Название роли."),
        color: disnake.Colour = commands.Param(name="цвет", description="Цвет роли."),
    ):
        await inter.response.defer(ephemeral=True)
        guild = inter.guild
        role = await guild.create_role(name=name, colour=color)
        embed = disnake.Embed(
            description=f"Роль {role.mention}, с цветом {color}, успешно создана!",
            timestamp=inter.created_at,
            color=role.color,
        )
        embed.set_author(
            name="Создание роли на сервере", icon_url=inter.author.display_avatar.url
        )
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="выдатьроль",
        description="Выдает указанную роль участнику.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.default_member_permissions(administrator=True)
    async def getrole(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
        role: disnake.Role = commands.Param(name="роль", description="Выбор роли"),
    ):
        if role in member.roles:
            await inter.response.defer(ephemeral=True)
            embed = disnake.Embed(
                title=f"{self.otheremojis.WARNING} Ошибка!",
                description=f"{inter.author.mention}, у пользователя {member.mention} уже имеется данная роль! (Роль: {role.mention})",
                color=self.color.RED,
            )
            await inter.edit_original_message(embed=embed)

        if member.top_role >= inter.author.top_role:
            return await self.checks.check_user_role(inter)

        if member.top_role >= inter.guild.me.top_role:
            return await self.checks.check_bot_role(inter)

        else:
            await inter.response.defer(ephemeral=False)
            await member.add_roles(role)
            embed = disnake.Embed(
                description=f"**{inter.author.mention} выдал роль {role.mention} пользователю {member.mention}.**",
                timestamp=inter.created_at,
                color=role.color,
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(
                text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR
            )
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="снятьроль",
        description="Снимает указанную роль участнику.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.default_member_permissions(administrator=True)
    async def ungetrole(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
        role: disnake.Role = commands.Param(name="роль", description="Выбор роли"),
    ):
        if member.top_role >= inter.author.top_role:
            return await self.checks.check_user_role(inter)

        if member.top_role >= inter.guild.me.top_role:
            return await self.checks.check_bot_role(inter)

        else:
            await inter.response.defer(ephemeral=False)
            await member.remove_roles(role)
            embed = disnake.Embed(
                description=f"**{inter.author.mention} снял роль {role.mention} пользователю {member.mention}.**",
                timestamp=inter.created_at,
                color=role.color,
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.set_footer(
                text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR
            )
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="задержка",
        description="Устанавливает задержку на общение в чате.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    @commands.default_member_permissions(administrator=True)
    async def setdelay(
        self,
        inter: disnake.ApplicationCommandInteraction,
        seconds: int = commands.Param(
            name="секунды", description="Время задержки в секундах"
        ),
    ):
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
        name="очистить",
        description="Очищает определенное количество сообщений в канале.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    @commands.default_member_permissions(administrator=True)
    async def clear(
        self,
        inter: disnake.ApplicationCommandInteraction,
        amount: int = commands.Param(
            name="количество", description="Количество сообщений"
        ),
    ):
        await inter.response.defer(ephemeral=True)
        embed = disnake.Embed(
            description=f"{inter.author.mention}, было очищено **{amount}** сообщений(е)",
            color=self.color.MAIN,
        )
        embed.set_author(name="Очистка чата", icon_url=inter.author.display_avatar.url)
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)
        await inter.channel.purge(limit=int(amount))
        await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))
