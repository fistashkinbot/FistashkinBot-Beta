import disnake
import random
import datetime
import os
import platform

from disnake.ext import commands
from utils import constant, enums, main, links, database, paginator, checks


class General(commands.Cog, name="Основное"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.profile = constant.ProfileEmojis()
        self.main = main.MainSettings()
        self.server = constant.ServerEmojis()
        self.color = enums.Color()
        self.db = database.DataBase()
        self.economy = main.EconomySystem(self.bot)
        self.checks = checks.Checks(self.bot)

    async def autocomplete_faq(
        inter: disnake.ApplicationCommandInteraction, string: str
    ):
        return list(
            filter(
                lambda question: string in question,
                [i["question"] for i in constant.Faq.FAQ],
            )
        )

    @commands.slash_command(
        name=disnake.Localized("faq", key="FAQ"),
        description=disnake.Localized(
            "See the most frequently asked questions", key="FAQ_DESCR"
        ),
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def faq(
        self,
        inter: disnake.ApplicationCommandInteraction,
        question: str = commands.Param(
            name=disnake.Localized("question", key="FAQ_QUESTION"),
            description=disnake.Localized(
                "Choose your question here.", key="FAQ_QUESTION_DESCR"
            ),
            autocomplete=autocomplete_faq,
        ),
    ):
        if question in [i["question"] for i in constant.Faq.FAQ]:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(
                description=[
                    i["answer"] for i in constant.Faq.FAQ if i["question"] == question
                ][0],
                color=self.color.MAIN,
            )
            embed.set_author(
                name=f"FAQ: {question}", icon_url=self.bot.user.display_avatar.url
            )
            embed.set_footer(
                text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR
            )
            await inter.edit_original_message(embed=embed, view=links.Links())

        else:
            await inter.edit_original_message(
                "Вопрос не найден. Не стесняйтесь задавать свой вопрос на одном из каналов."
            )

    @commands.slash_command(
        name=disnake.Localized("user", key="USER_INFO"),
        description=disnake.Localized(
            "Shows member information.", key="USER_INFO_DESCR"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def userinfo(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            lambda inter: inter.author,
            name=disnake.Localized("member", key="TARGET_MEMBER"),
            description=disnake.Localized("Select member", key="TARGET_MEMBER_DESCR"),
        ),
    ):
        await inter.response.defer(ephemeral=False)
        data = await self.db.get_data(member)
        if (
            not member
        ):  # если не упоминать участника тогда выводит аватар автора сообщения
            member = inter.author

        registerf = disnake.utils.format_dt(member.created_at, style="f")
        registerr = disnake.utils.format_dt(member.created_at, style="R")
        joinedf = disnake.utils.format_dt(member.joined_at, style="f")
        joinedr = disnake.utils.format_dt(member.joined_at, style="R")

        user = await self.bot.fetch_user(member.id)
        response = [
            self.profile.BADGES[badge.name]
            for badge in member.public_flags.all()
            if badge.name in self.profile.BADGES
        ]
        if member.id == self.main.DEVELOPER_ID:
            response.append(self.profile.DEVELOPER)  # Developer
        if member.premium_since:
            response.append(self.profile.NITRO_BOOSTER)  # Nitro Booster
        if member.display_avatar.is_animated() or user.banner:
            response.append(self.profile.BOOSTER_SUBSCRIBER)  # Nitro Subscriber
        if member.discriminator == "0":
            response.append(self.profile.UPDATED_NICKNAME)  # Updated Nickname

        description = [
            f"**Основная информация**",
            f"**Имя пользователя:** {member} ({member.mention})",
            f"**Статус:** {self.profile.STATUS[member.status]}",
            f"**Присоединился:** {joinedf} ({joinedr})",
            f"**Дата регистрации:** {registerf} ({registerr})",
        ]

        if member.top_role == member.guild.default_role:
            color = self.color.DARK_GRAY
            pass
        elif member == member.bot or member == self.bot.user:
            color = self.color.DARK_GRAY
            pass
        elif member.top_role is not None:
            top_role = member.top_role.mention
            color = member.top_role.color
            description.append(f"**Приоритетная роль:** {top_role}")

        if member.activities:
            for activity in member.activities:
                if isinstance(activity, disnake.Spotify):
                    description.append(
                        f"{self.profile.SPOTIFY} **Cлушает Spotify:** [{activity.artist} - {activity.title}]({activity.track_url})"
                    )

        embed = disnake.Embed(
            description=f"\n ".join(description),
            color=color,
            timestamp=inter.created_at,
        )

        if response:
            embed.add_field(name="Значки", value=" ".join(response), inline=True)

        embed.add_field(
            name="Уровень",
            value=f"{data['level']} (Опыт: {data['xp']}/{500 + 100 * data['level']})",
            inline=True,
        )
        embed.add_field(
            name="Экономика",
            value=f"Баланс: {data['balance']} {self.economy.CURRENCY_NAME}",
            inline=True,
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=user.banner.url if user.banner else None)
        embed.set_footer(text=f"ID: {member.id}", icon_url=member.display_avatar.url)
        embed.set_author(
            name=f"Информация о пользователе {member.display_name}",
            icon_url=member.display_avatar.url,
        )
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("server", key="SERVER_INFO"),
        description=disnake.Localized(
            "Shows server information.", key="SERVER_INFO_DESCR"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def serverinfo(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        embed = disnake.Embed(color=self.color.MAIN, timestamp=inter.created_at)
        embed.add_field(
            name="Участники:",
            value="\n".join(
                [
                    f"{self.server.MEMBERS_TOTAL} Всего: **{len(inter.guild.members)}**",
                    f"{self.server.MEMBERS} Людей: **{len(list(filter(lambda m: m.bot == False, inter.guild.members)))}**",
                    f"{self.server.BOT} Ботов: **{len(list(filter(lambda m: m.bot == True, inter.guild.members)))}**",
                ]
            ),
            inline=True,
        )
        embed.add_field(
            name="По статусам:",
            value="\n".join(
                [
                    f"{self.profile.ONLINE} В сети: **{len(list(filter(lambda m: str(m.status) == 'online', inter.guild.members)))}**",
                    f"{self.profile.IDLE} Неактивен: **{len(list(filter(lambda m: str(m.status) == 'idle', inter.guild.members)))}**",
                    f"{self.profile.DND} Не беспокоить: **{len(list(filter(lambda m: str(m.status) == 'dnd', inter.guild.members)))}**",
                    f"{self.profile.OFFLINE} Не в сети: **{len(list(filter(lambda m: str(m.status) == 'offline', inter.guild.members)))}**",
                ]
            ),
            inline=True,
        )
        embed.add_field(
            name="Каналы:",
            value="\n".join(
                [
                    f"{self.server.CHANNELS_TOTAL} Всего: **{len(inter.guild.channels)}**",
                    f"{self.server.TEXT_CHANNEL} Текстовых: **{len(inter.guild.text_channels)}**",
                    f"{self.server.VOICE_CHANNEL} Голосовых: **{len(inter.guild.voice_channels)}**",
                ]
            ),
            inline=True,
        )
        embed.add_field(
            name="Владелец:",
            value=f"{inter.guild.owner}\n{inter.guild.owner.mention}",
            inline=True,
        )
        embed.add_field(
            name="Создан:",
            value=f"<t:{round(inter.guild.created_at.timestamp())}:D>\n"
            f"<t:{round(inter.guild.created_at.timestamp())}:R>",
            inline=True,
        )

        embed.set_thumbnail(url=inter.guild.icon.url if inter.guild.icon else None)
        embed.set_image(url=inter.guild.banner.url if inter.guild.banner else None)
        embed.set_footer(
            text=f"ID: {inter.guild.id}. Shard: {inter.guild.shard_id}",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )
        embed.set_author(
            name=f"Информация о сервере {inter.guild.name}",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("avatar", key="AVATAR"),
        description=disnake.Localized(
            "Shows the avatar of the mentioned member or the member who called the command.",
            key="AVATAR_DESCR",
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def avatar(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            lambda inter: inter.author,
            name=disnake.Localized("member", key="TARGET_MEMBER"),
            description=disnake.Localized("Select member", key="TARGET_MEMBER_DESCR"),
        ),
    ):
        await inter.response.defer(ephemeral=False)
        if (
            not member
        ):  # если не упоминать участника тогда выводит аватар автора сообщения
            member = inter.author

        embed = disnake.Embed(
            description=f"[Нажмите что бы скачать аватар]({member.display_avatar.url})",
            color=self.color.MAIN,
        )
        embed.set_image(url=member.display_avatar.url)
        embed.set_author(
            name=f"Аватар {member.display_name}", icon_url=member.display_avatar.url
        )
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("roles", key="ROLES"),
        description=disnake.Localized("Shows all server roles.", key="ROLES_DESCR"),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def roles(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)
        all_roles = []
        guild = inter.guild
        roles = [
            role
            for role in guild.roles
            if role in inter.guild.roles
            if role != inter.guild.default_role
        ]
        roles.reverse()

        items_per_page = 10  # Set the number of roles per page here
        pages = [
            roles[i : i + items_per_page] for i in range(0, len(roles), items_per_page)
        ]

        embed_pages = []
        for i, page in enumerate(pages):
            embed = disnake.Embed(
                description="\n".join([role.mention for role in page]),
                timestamp=inter.created_at,
            )
            embed.set_author(
                name=f"Роли сервера {inter.guild.name} [{len(inter.guild.roles[:-1])}]",
                icon_url=inter.guild.icon.url if inter.guild.icon else None,
            )
            embed_pages.append(embed)

        await inter.edit_original_message(
            embed=embed_pages[0], view=paginator.Paginator(embeds=embed_pages)
        )

    @commands.slash_command(
        name=disnake.Localized("info", key="INFO"),
        description=disnake.Localized(
            "Shows interesting information about the bot.", key="INFO_DESCR"
        ),
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def botinfo(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        developer = await self.bot.fetch_user(self.main.DEVELOPER_ID)
        embed = disnake.Embed(
            description=f"👋 Привет! Меня зовут Фисташкин! Я небольшой бот с небольшими командами <:earlysupporter:1045664335587979326>\n\n"
            f"Я работаю на слэш командах <:supportscommands:1045664343209021490>\n"
            f"Детальная информация о моих возможностях по команде </хелп:1046871805186555985>.",
            colour=self.color.MAIN,
            timestamp=inter.created_at,
        )
        embed.set_author(
            name=f"👾 Информация о боте {self.bot.user.name}",
            icon_url=self.bot.user.display_avatar.url,
        )
        embed.add_field(name="👾 Сборка:", value=self.main.BOT_VERSION, inline=True)
        embed.add_field(
            name="🔮 Мой разработчик:",
            value=f"<:riverya4life:1065581416357826560> [{developer}]({self.main.GITHUB_AUTHOR})",
            inline=True,
        )
        embed.add_field(
            name="🎊 Дата создания:",
            value=f"<t:{round(self.bot.user.created_at.timestamp())}:D> (<t:{round(self.bot.user.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)
        await inter.edit_original_message(embed=embed, view=links.Links())

    @commands.slash_command(
        name=disnake.Localized("stats", key="STATS_INFO"),
        description=disnake.Localized("Shows bot statistics.", key="STATS_INFO_DESCR"),
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def stats(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()

        channels_count = 0
        for guild in self.bot.guilds:
            channels_count += len(guild.channels)

        uptimebot = disnake.utils.format_dt(os.path.getatime("./main.py"), style="R")

        embed = disnake.Embed(colour=self.color.MAIN, timestamp=inter.created_at)
        embed.set_author(
            name=f"Статистика {self.bot.user.name}",
            icon_url=self.bot.user.display_avatar.url,
        )
        embed.add_field(
            name="Основная",
            value=f"**Серверов:** {len(self.bot.guilds)}\n"
            f"**Участников:** {len(self.bot.users)}\n"
            f"**Каналов:** {int(channels_count)}",
            inline=False,
        )
        embed.add_field(
            name="Платформа",
            value=f"**Аптайм**: {uptimebot}\n"
            f"**Задержка:** {round(self.bot.latency * 1000)} мс\n"
            f"**Версия:** {self.main.BOT_VERSION} | Python {platform.python_version()} | {disnake.__title__} {disnake.__version__}",
            inline=True,
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="пинг",
        description="Проверка на работоспособность бота и задержки.",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)
        embed = disnake.Embed(
            description=f"{inter.author.mention}, я живой и кушаю фисташки!"
            f"Мой пинг: {round(self.bot.latency * 1000)} мс!",
            color=self.color.MAIN,
        )
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="клист",
        description="Выводит список участников с определенной ролью.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def list(
        self,
        inter: disnake.ApplicationCommandInteraction,
        role: disnake.Role = commands.Param(name="роль", description="Выберите роль."),
    ):
        await inter.response.defer(ephemeral=False)
        data = [(member.mention or member.nick) for member in role.members]

        counter = 0
        paginated_data = []
        for i in range(0, len(data), 10):
            paginated_data.append("\n".join(data[i : i + 10]))

        embeds = []
        for i, page_data in enumerate(paginated_data):
            embed = disnake.Embed(
                title=f"Все участники с ролью {role} [{len(role.members)}]\n",
                description=f"{page_data}\n",
                color=role.color,
                timestamp=inter.created_at,
            )
            embeds.append(embed)
        view = paginator.Paginator(embeds)
        view.message = await inter.edit_original_message(embed=embeds[0], view=view)


def setup(bot):
    bot.add_cog(General(bot))
