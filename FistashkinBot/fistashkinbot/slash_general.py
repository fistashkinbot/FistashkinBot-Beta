import disnake
import random
import datetime
import os
import platform
import json
import requests

from disnake.ext import commands
from core import config
from bs4 import BeautifulSoup
from utils import constant, enums, main, links, database, paginator, checks


class General(commands.Cog, name="Утилиты"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.profile = constant.ProfileEmojis()
        self.main = main.MainSettings()
        self.server = constant.ServerEmojis()
        self.color = enums.Color()
        self.db = database.DataBase()
        self.economy = main.EconomySystem(self.bot)
        self.checks = checks.Checks(self.bot)
        self.config = config.Config()
        self.enum = enums.Enum()

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
        name=disnake.Localized("faq", key="FAQ_COMMAND_NAME"),
        description=disnake.Localized(
            "See the most frequently asked questions.", key="FAQ_COMMAND_DESCRIPTION"
        ),
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def faq(
        self,
        inter: disnake.ApplicationCommandInteraction,
        question: str = commands.Param(
            name=disnake.Localized("question", key="FAQ_QUESTION_COMMAND_NAME"),
            description=disnake.Localized(
                "Choose your question here.", key="FAQ_QUESTION_COMMAND_DESCRIPTION"
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
        name=disnake.Localized("userinfo", key="USER_INFO_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows user information.", key="USER_INFO_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def userinfo(
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

        data = await self.db.get_data(member)
        registerf = disnake.utils.format_dt(member.created_at, style="f")
        registerr = disnake.utils.format_dt(member.created_at, style="R")
        joinedf = disnake.utils.format_dt(member.joined_at, style="f")
        joinedr = disnake.utils.format_dt(member.joined_at, style="R")

        level = self.enum.format_large_number(data["level"])
        xp = self.enum.format_large_number(data["xp"])
        total_xp = self.enum.format_large_number(data["total_xp"])
        xp_to_lvl = self.enum.format_large_number(500 + 100 * data["level"])
        balance = self.enum.format_large_number(data["balance"])
        bio = await self.db.get_bio(member)

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
            f"**Имя пользователя:** {member} ({member.mention})",
            f"**Статус:** {self.profile.STATUS[member.status]}",
            f"**Присоединился:** {joinedf} ({joinedr})",
            f"**Дата регистрации:** {registerf} ({registerr})",
        ]
        if not member.bot:
            if member.activities:
                for activity in member.activities:
                    if activity.type == disnake.ActivityType.playing:
                        description.append(f"**Играет в:** {activity.name}")
                    if activity.type == disnake.ActivityType.streaming:
                        description.append(f"**Стримит:** {activity.name}")
                    if activity.type == disnake.ActivityType.watching:
                        description.append(f"**Смотрит:** {activity.name}")
                    if activity.type == disnake.ActivityType.listening:
                        if isinstance(activity, disnake.Spotify):
                            description.append(
                                f"**Cлушает Spotify:** {self.profile.SPOTIFY} [{activity.artist} - {activity.title}]({activity.track_url})"
                            )
                        else:
                            description.append(f"**Слушает:** {activity.name}")

        if member.top_role == member.guild.default_role or member.bot:
            color = self.color.DARK_GRAY
        else:
            color = member.top_role.color

        if (
            member.bot
            or member != inter.author
            and bio
            == "Вы можете добавить сюда какую-нибудь полезную информацию о себе командой `/осебе`"
        ):
            bio = None

        embed = disnake.Embed(
            description=bio,
            color=color,
            timestamp=inter.created_at,
        )

        embed.add_field(
            name="Основная информация",
            value=f"\n".join(description),
            inline=False,
        )
        if not member.bot:
            embed.add_field(
                name="Уровень",
                value=f"{level} | Опыт: {xp}/{xp_to_lvl}\n(всего: {total_xp})",
                inline=True,
            )
            embed.add_field(
                name="Экономика",
                value=f"Баланс:\n {balance} {self.economy.CURRENCY_NAME}",
                inline=True,
            )

            if response is not None:
                embed.add_field(name="Значки", value=" ".join(response), inline=True)

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=user.banner.url if user.banner else None)
        embed.set_footer(text=f"ID: {member.id}", icon_url=member.display_avatar.url)
        embed.set_author(
            name=f"Информация о пользователе {member.display_name}",
            icon_url=member.display_avatar.url,
        )
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("serverinfo", key="SERVER_INFO_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows server information.", key="SERVER_INFO_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def serverinfo(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        embed = disnake.Embed(color=self.color.MAIN, timestamp=inter.created_at)

        total_members = self.enum.format_large_number(len(inter.guild.members))
        members = self.enum.format_large_number(
            len(list(filter(lambda m: m.bot == False, inter.guild.members)))
        )
        bots = self.enum.format_large_number(
            len(list(filter(lambda m: m.bot == True, inter.guild.members)))
        )

        members_online = self.enum.format_large_number(
            len(list(filter(lambda m: str(m.status) == "online", inter.guild.members)))
        )
        members_idle = self.enum.format_large_number(
            len(list(filter(lambda m: str(m.status) == "idle", inter.guild.members)))
        )
        members_dnd = self.enum.format_large_number(
            len(list(filter(lambda m: str(m.status) == "dnd", inter.guild.members)))
        )
        members_offline = self.enum.format_large_number(
            len(list(filter(lambda m: str(m.status) == "offline", inter.guild.members)))
        )

        total_channels = self.enum.format_large_number(len(inter.guild.channels))
        text_channels = self.enum.format_large_number(len(inter.guild.text_channels))
        voice_channels = self.enum.format_large_number(len(inter.guild.voice_channels))

        members_field = [
            f"{self.server.MEMBERS_TOTAL} Всего: **{total_members}**",
            f"{self.server.MEMBERS} Людей: **{members}**",
            f"{self.server.BOT} Ботов: **{bots}**",
        ]
        if inter.guild.premium_subscribers:
            members_field.append(
                f"Бустеров: **{len(inter.guild.premium_subscribers)}**"
            )

        members_field_status = [
            f"{self.profile.ONLINE} В сети: **{members_online}**",
            f"{self.profile.IDLE} Неактивен: **{members_idle}**",
            f"{self.profile.DND} Не беспокоить: **{members_dnd}**",
            f"{self.profile.OFFLINE} Не в сети: **{members_offline}**",
        ]
        channels_field = []
        if inter.guild.channels:
            channels_field.append(
                f"{self.server.CHANNELS_TOTAL} Всего: **{total_channels}**"
            )
        if inter.guild.text_channels:
            channels_field.append(
                f"{self.server.TEXT_CHANNEL} Текстовых: **{text_channels}**"
            )
        if inter.guild.voice_channels:
            channels_field.append(
                f"{self.server.VOICE_CHANNEL} Голосовых: **{voice_channels}**"
            )
        if inter.guild.stage_channels:
            channels_field.append(f"Трибун: **{len(inter.guild.stage_channels)}**")
        if inter.guild.forum_channels:
            channels_field.append(f"Форумов: **{len(inter.guild.forum_channels)}**")

        embed.add_field(
            name="Участники:",
            value="\n".join(members_field),
            inline=True,
        )
        embed.add_field(
            name="По статусам:",
            value="\n".join(members_field_status),
            inline=True,
        )
        embed.add_field(
            name="Каналы:",
            value="\n".join(channels_field),
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
        if inter.guild.premium_tier != 0:
            embed.add_field(
                name="Уровень Бустов:",
                value=f"{inter.guild.premium_tier}",
                inline=True,
            )

        embed.set_thumbnail(url=inter.guild.icon.url if inter.guild.icon else None)
        embed.set_image(url=inter.guild.banner.url if inter.guild.banner else None)
        embed.set_footer(
            text=f"ID: {inter.guild.id} | shard_id: {inter.guild.shard_id}",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )
        embed.set_author(
            name=f"Информация о сервере {inter.guild.name}",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("avatar", key="AVATAR_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows the avatar of the mentioned user or the user who called the command.",
            key="AVATAR_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def avatar(
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
        name=disnake.Localized("roles", key="ROLES_LIST_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows all server roles.", key="ROLES_LIST_COMMAND_DESCRIPTION"
        ),
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
        roles_count = self.enum.format_large_number(len(inter.guild.roles[:-1]))
        for i, page in enumerate(pages):
            embed = disnake.Embed(
                description="\n".join([role.mention for role in page]),
                timestamp=inter.created_at,
            )
            embed.set_author(
                name=f"Роли сервера {inter.guild.name} [{roles_count}]",
                icon_url=inter.guild.icon.url if inter.guild.icon else None,
            )
            embed_pages.append(embed)

        view = paginator.Paginator(embeds=embed_pages)
        message = await inter.edit_original_message(embed=embed_pages[0], view=view)
        view.message = message

    @commands.slash_command(
        name=disnake.Localized("botinfo", key="BOT_INFO_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows interesting information about the bot.",
            key="BOT_INFO_COMMAND_DESCRIPTION",
        ),
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def botinfo(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)
        developer = await self.bot.fetch_user(self.main.DEVELOPER_ID)
        embed = disnake.Embed(
            description=f"👋 Привет! Меня зовут Фисташкин! Я небольшой бот с кучкой небольших команд!\n"
            f"Детальная информация о моих возможностях по команде `/хелп`",
            colour=self.color.MAIN,
            timestamp=inter.created_at,
        )
        embed.set_author(
            name=f"Информация о боте {self.bot.user.name}",
            icon_url=self.bot.user.display_avatar.url,
        )
        embed.add_field(
            name="Сборка:",
            value=self.main.BOT_VERSION,
            inline=True,
        )
        embed.add_field(
            name="Мой разработчик:",
            value=f"<:riverya4life:1065581416357826560> [{developer}](https://discord.com/users/{developer.id})",
            inline=True,
        )
        embed.add_field(
            name="Дата создания:",
            value=f"<t:{round(self.bot.user.created_at.timestamp())}:D> (<t:{round(self.bot.user.created_at.timestamp())}:R>)",
            inline=False,
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)
        await inter.edit_original_message(embed=embed, view=links.Links())

    @commands.slash_command(
        name=disnake.Localized("stats", key="BOT_STATS_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows bot statistics.", key="BOT_STATS_COMMAND_DESCRIPTION"
        ),
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def stats(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)

        channels_count = 0
        total_connections = 0
        for guild in self.bot.guilds:
            channels_count += len(guild.channels)
            for voice_channel in guild.voice_channels:
                if (
                    voice_channel.members
                ):  # Если в канале есть участники, то считаем его активным
                    total_connections += 1

        bot_guilds = self.enum.format_large_number(len(self.bot.guilds))
        bot_guilds_members = self.enum.format_large_number(len(self.bot.users))
        bot_guilds_channels = self.enum.format_large_number(int(channels_count))
        bot_active_voice_connections = self.enum.format_large_number(
            int(total_connections)
        )

        uptimebot = disnake.utils.format_dt(os.path.getatime("./main.py"), style="R")
        command_counter = await self.db.get_command_count()
        formatted_command_counter_result = self.enum.format_large_number(
            command_counter
        )

        embed = disnake.Embed(
            description=f"**Версия:** {self.main.BOT_VERSION} | Python {platform.python_version()} | {disnake.__title__} {disnake.__version__}",
            colour=self.color.MAIN,
            timestamp=inter.created_at,
        )
        embed.set_author(
            name=f"Статистика {self.bot.user.name}",
            icon_url=self.bot.user.display_avatar.url,
        )
        embed.add_field(
            name="Основная",
            value=f"**Серверов:** {bot_guilds}\n"
            f"**Участников:** {bot_guilds_members}\n"
            f"**Каналов:** {bot_guilds_channels}\n"
            f"**Голосовых соединений:** {bot_active_voice_connections}",
            inline=True,
        )
        embed.add_field(
            name="Платформа",
            value=f"**Обработано команд:** {formatted_command_counter_result}\n"
            f"**Задержка:** {round(self.bot.latency * 1000)} мс\n"
            f"**Запущена**: {uptimebot}\n",
            inline=True,
        )
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("ping", key="BOT_PING_COMMAND_NAME"),
        description=disnake.Localized(
            "Testing bot functionality and delays.", key="BOT_PING_COMMAND_DESCRIPTION"
        ),
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)
        embed = disnake.Embed(
            description=f"{inter.author.mention}, я живой и кушаю фисташки! "
            f"Мой пинг: {round(self.bot.latency * 1000)} мс!",
            color=self.color.MAIN,
        )
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("clist", key="CLIST_COMMAND_NAME"),
        description=disnake.Localized(
            "Displays a list of members with a specific role.",
            key="CLIST_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clist(
        self,
        inter: disnake.ApplicationCommandInteraction,
        role: disnake.Role = commands.Param(
            name=disnake.Localized("role", key="TARGET_ROLE_NAME"),
            description=disnake.Localized(
                "Select a role.", key="TARGET_ROLE_DESCRIPTION"
            ),
        ),
    ):
        await inter.response.defer(ephemeral=False)
        data = [(member.mention or member.nick) for member in role.members]
        member_count = self.enum.format_large_number(len(role.members))

        counter = 0
        paginated_data = []
        for i in range(0, len(data), 10):
            paginated_data.append("\n".join(data[i : i + 10]))

        embeds = []
        for i, page_data in enumerate(paginated_data):
            embed = disnake.Embed(
                title=f"Все участники с ролью {role} [{member_count}]\n",
                description=f"{page_data}\n",
                color=role.color,
                timestamp=inter.created_at,
            )
            embeds.append(embed)
        view = paginator.Paginator(embeds)
        message = await inter.edit_original_message(embed=embeds[0], view=view)
        view.message = message

    @commands.slash_command(
        name=disnake.Localized("bio", key="USER_BIO_COMMAND_NAME"),
        description=disnake.Localized(
            "Changes the biography of the user.", key="USER_BIO_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def bio(
        self,
        inter: disnake.ApplicationCommandInteraction,
    ):
        await inter.response.defer(ephemeral=True)
        user = await self.bot.fetch_user(inter.author.id)
        bio = await self.db.get_bio(inter.author)
        if (
            bio
            == "Вы можете добавить сюда какую-нибудь полезную информацию о себе командой `/осебе`"
        ):
            bio = "Биография отсутствует."

        embed = disnake.Embed(
            description=bio,
            color=self.color.MAIN,
        )
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        embed.set_image(url=user.banner.url if user.banner else None)
        embed.set_author(
            name=f"Биография {inter.author}", icon_url=inter.author.display_avatar.url
        )
        view = BioButtons(self.bot)
        message = await inter.edit_original_message(embed=embed, view=view)
        view.message = message

    @commands.slash_command(
        name=disnake.Localized("github", key="GITHUB_COMMAND_NAME"),
        description=disnake.Localized(
            "Github repository information.", key="GITHUB_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def github(
        self,
        inter: disnake.ApplicationCommandInteraction,
        arg: str = commands.Param(
            name=disnake.Localized("repository", key="GITHUB_ARG_NAME"),
            description=disnake.Localized(
                "Specify the name of the repository in the format nick/repository.",
                key="GITHUB_ARG_DESCRIPTION",
            ),
        ),
    ):
        req = requests.get(f"https://api.github.com/repos/{arg}")
        apijson = json.loads(req.text)
        if req.status_code == 200:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(color=self.color.DARK_GRAY)
            embed.set_author(
                name=apijson["owner"]["login"],
                icon_url=apijson["owner"]["avatar_url"],
                url=apijson["owner"]["html_url"],
            )
            embed.set_thumbnail(url=apijson["owner"]["avatar_url"])
            embed.add_field(
                name="Репозиторий:",
                value=f"[{apijson['name']}]({apijson['html_url']})",
                inline=True,
            )
            embed.add_field(name="Язык:", value=apijson["language"], inline=True)

            try:
                license_url = f"[{apijson['license']['spdx_id']}]({json.loads(requests.get(apijson['license']['url']).text)['html_url']})"
            except:
                license_url = "None"
            embed.add_field(name="Лицензия:", value=license_url, inline=True)
            if apijson["stargazers_count"] != 0:
                embed.add_field(
                    name="Звёзд:", value=apijson["stargazers_count"], inline=True
                )
            if apijson["forks_count"] != 0:
                embed.add_field(
                    name="Форков:", value=apijson["forks_count"], inline=True
                )
            if apijson["open_issues"] != 0:
                embed.add_field(
                    name="Проблем:", value=apijson["open_issues"], inline=True
                )
            embed.add_field(
                name="Описание:", value=apijson["description"], inline=False
            )

            for meta in BeautifulSoup(
                requests.get(apijson["html_url"]).text, features="html.parser"
            ).find_all("meta"):
                try:
                    if meta.attrs["property"] == "og:image":
                        embed.set_image(url=meta.attrs["content"])
                        break
                except:
                    pass

            await inter.edit_original_message(embed=embed)
        elif req.status_code == 404:
            return await self.checks.check_unknown(
                inter, text=f"Репозиторий не найден!"
            )
        elif req.status_code == 503:
            return await self.checks.check_unknown(inter, text=f"Гитхаб упал!")
        else:
            return await self.checks.check_unknown(
                inter, text=f"Неизвестная ошибка при получении информации репозитория!"
            )


class BioButtons(disnake.ui.View):
    message: disnake.Message

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = database.DataBase()
        self.color = enums.Color()
        self.checks = checks.Checks(self.bot)
        super().__init__(timeout=120.0)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=None)

    @disnake.ui.button(
        label="Установить биографию", emoji="✨", style=disnake.ButtonStyle.green
    )
    async def set_bio(self, button: disnake.ui.Button, inter):
        await inter.response.send_modal(modal=InputSetBioUser())

    @disnake.ui.button(
        label="Удалить биографию", emoji="❎", style=disnake.ButtonStyle.red
    )
    async def remove_bio(self, button: disnake.ui.Button, inter):
        await self.db.remove_bio(inter.author)
        embed = disnake.Embed(
            description="✅ Информация успешно удалена, проверьте командой `/юзер`, либо опять вызовите эту команду.",
            color=self.color.MAIN,
        )
        embed.set_author(
            name=f"Биография {inter.author}", icon_url=inter.author.display_avatar.url
        )
        await inter.response.edit_message(embed=embed, view=None)


class InputSetBioUser(disnake.ui.Modal):
    message: disnake.Message

    def __init__(self):
        self.otheremojis = constant.OtherEmojis()
        self.db = database.DataBase()
        self.color = enums.Color()

        components = [
            disnake.ui.TextInput(
                label="Текст",
                placeholder="Напишите текст...",
                custom_id="set_bio",
                style=disnake.TextInputStyle.paragraph,
                max_length=95,
            )
        ]
        super().__init__(
            title="Биография",
            components=components,
            custom_id="set_bio_modal",
        )

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            text_bio = str(inter.text_values["set_bio"])
            await self.db.set_bio(inter.author, text_bio)

            embed = disnake.Embed(
                description="✅ Информация успешно обновлена, проверьте командой `/юзер`, либо опять вызовите эту команду.",
                color=self.color.MAIN,
            )
            embed.set_author(
                name=f"Биография {inter.author}",
                icon_url=inter.author.display_avatar.url,
            )
            await inter.response.edit_message(embed=embed, view=None)

        except ValueError:
            return await self.checks.check_value_error(inter)


def setup(bot):
    bot.add_cog(General(bot))
