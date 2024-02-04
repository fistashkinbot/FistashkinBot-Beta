import disnake
import datetime
import random
import platform

from disnake.ext import commands, tasks
from utils import enums, main, automod, links, checks, fistashkin_status
from loguru import logger


class Listeners(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.color = enums.Color()
        self.main = main.MainSettings()
        self.activity = fistashkin_status.BotActivity()
        self.automod = automod.Automod()
        self.checks = checks.Checks(self.bot)

    @tasks.loop(minutes=15)
    async def change_activity(self):
        await self.bot.change_presence(
            status=disnake.Status.idle, activity=random.choice(self.activity.ACTIVITY)
        )

    @commands.Cog.listener(disnake.Event.ready)
    async def on_ready(self):
        developer = await self.bot.fetch_user(self.main.DEVELOPER_ID)
        START_MESSAGE = f"""
                     ______   _         _                   _       _      _           ____            _
                    |  ____| (_)       | |                 | |     | |    (_)         |  _ \          | |
                    | |__     _   ___  | |_    __ _   ___  | |__   | | __  _   _ __   | |_) |   ___   | |_
                    |  __|   | | / __| | __|  / _` | / __| | '_ \  | |/ / | | | '_ \  |  _ <   / _ \  | __|
                    | |      | | \__ \ | |_  | (_| | \__ \ | | | | |   <  | | | | | | | |_) | | (_) | | |_
                    |_|      |_| |___/  \__|  \__,_| |___/ |_| |_| |_|\_\ |_| |_| |_| |____/   \___/   \__|
        ----------------------------------------------------------------------------------------------------------------

                                                         Официальный бот!
                                                      ----------------------
                              Discord бот! / Разработчик - {developer.display_name} / Дата создания: {self.bot.user.created_at.strftime("%d.%m.%Y")}
                                                      ----------------------
                              -----------------------/     {self.bot.user.display_name}    \----------------------

        ################################################################################################################

        -
        Разработчик - {developer.display_name} (@{developer} ID: {developer.id})
        Бот - {self.bot.user} (ID: {self.bot.user.id})
        Пинг бота - {round(self.bot.latency * 1000)} мс
        Шардов - {self.bot.shard_count}

        Язык програмирования - Python {platform.python_version()}
        Библиотека разработки - {disnake.__title__} {disnake.__version__}
        -
        """
        self.change_activity.start()
        vc = disnake.utils.get(
            self.bot.get_guild(1037792926383747143).channels, id=1191523826585059419
        )
        await vc.guild.change_voice_state(channel=vc, self_mute=False, self_deaf=False)
        logger.info(START_MESSAGE)

    @commands.Cog.listener(disnake.Event.connect)
    async def on_connect(self):
        logger.info(f"Бот присоединился: {self.bot.user.name} ({self.bot.user.id})")
        logger.info(f"Пинг: {round(self.bot.latency * 1000)}мс")

    @commands.Cog.listener(disnake.Event.disconnect)
    async def on_disconnect(self):
        logger.error(f"Бот отключен")

    @commands.Cog.listener(disnake.Event.member_join)
    async def on_member_join(self, member):
        if member.guild.id == self.main.DISCORD_BOT_SERVER_ID:
            description = [
                f":flag_gb: :flag_us:\n"
                f"Hello, {member.mention}! Welcome to the FistashkinBot community and support guild!"
                f"Please check the ⁠<#1044628885876260865> channel for useful info and rules.\n\n"
                f":flag_ru:\n"
                f"Привет, {member.mention}! Добро пожаловать на сервер поддержки и сообщества пользователей FistashkinBot!"
                f"Пожалуйста, ознакомься с информацией и правилами в канале ⁠<#1044628885876260865>\n\n"
                f":flag_ua:\n"
                f"Привіт, {member.mention}! Ласкаво просимо на сервер підтримки та спільноти користувачів FistashkinBot!"
                f"Будь ласка, ознайомся з інформацією та правилами в каналі <#1044628885876260865>"
            ]
            await member.send(
                embed=disnake.Embed(
                    description="".join(description), color=self.color.MAIN
                ),
                components=[
                    disnake.ui.Button(
                        label=f"Отправлено с {member.guild.name}",
                        emoji="📨",
                        style=disnake.ButtonStyle.gray,
                        disabled=True,
                    )
                ],
            )

    @commands.Cog.listener(disnake.Event.guild_join)
    async def on_guild_join(self, guild):
        developer = await self.bot.fetch_user(self.main.DEVELOPER_ID)
        inviter = await guild.audit_logs(
            action=disnake.AuditLogAction.bot_add, limit=None
        ).flatten()
        inviter_user = inviter[0].user

        embed = disnake.Embed(
            description=f"Привет, **{inviter_user}**! 👋\n\n"
            f"Спасибо, что пригласили меня на **{guild.name}**! ❤\n"
            f"Я небольшой бот с прикольными командами для вашего уютного сообщества!\n"
            f"Я работаю на слеш командах, что упрощает моё использование.\n"
            f"Вот краткий обзор того, что я умею делать:\n\n"
            f"**🎀 Основное**\nВы можете посмотреть информацию про участников сервера и про сам сервер, посмотреть аватар пользователя и саму информацию о боте!\n\n"
            f"**✨ Экономика**\nВы можете наградить своих участников за их активность новой валютой бота, повышаться в ранге в топы сервера!\n\n"
            f"**🛡️ Модерация**\nБот поддерживает AutoMod, с помощью которого создаёт автоматически правила для автомодерации (фильтр запрещённых слов, обычного спама и упоминаний и т.д.), что значительно упрощает модерацию сервера. Кроме этого имеются стандартные команды бан, кик, мьют и прочее.\n\n"
            f"**🎭 Развлечение**\nЕсть также несколько небольших забавных функций, таких как 8ball, казино, взаимодействие с участниками и многое другое.\n\n"
            f"**🤖 Слеш команды**\nБот поддерживает команды косой черты, чтобы облегчить использование команд бота.\n\n"
            f"**❓ Есть вопрос?**\nНаш сервер поддержки Discord: https://discord.gg/H9XCZSReMj",
            color=self.color.MAIN,
        )
        embed.set_author(
            name=self.bot.user.name,
            icon_url=self.bot.user.display_avatar.url,
            url="https://discord.gg/H9XCZSReMj",
        )
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)

        await inviter_user.send(
            embed=embed,
            components=[
                disnake.ui.Button(
                    label=f"С любовью разработчик {developer.display_name}",
                    emoji="❤️",
                    style=disnake.ButtonStyle.gray,
                    disabled=True,
                )
            ],
        )

        await self.automod.automod(guild)

    @commands.Cog.listener(disnake.Event.message)
    async def on_message(self, message):
        if message.author.bot or not message.guild or message.author == self.bot.user:
            return

        if message.content == self.bot.user.mention:
            await message.reply(
                f"Да, да, что такое?\n"
                f"Команды ты можешь посмотреть, введя `/` и найди мою аватарку в списке ботов. Там будут все команды, которые я могу тебе дать!\n\n"
                f"— Ссылка на сервер: [клик!]({self.main.DISCORD_BOT_SERVER})\n— Сайт бота: [клик!]({self.main.BOT_SITE})\n"
                f"— Пригласи меня и на другие сервера, тыкнув на кнопочку в профиле \🥺",
                delete_after=30.0,
            )


def setup(bot):
    bot.add_cog(Listeners(bot))
