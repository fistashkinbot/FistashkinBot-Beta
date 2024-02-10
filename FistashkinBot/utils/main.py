import disnake
import random
import datetime

from environs import Env
from .enums import Color
from disnake.ext import commands
from utils import database, main, constant, checks


class MainSettings:
    DEVELOPER_ID = 668453200457760786
    BOT_ID = 991338113630752928
    BOT_VERSION = "v1.7.1710 (<t:1707573002:d>)"
    BOT_EMOJI = "<:fistashkinbot:1145318360196845649>"

    GITHUB_AUTHOR = "https://github.com/riverya4life"
    DISCORD_BOT_SERVER = "https://discord.gg/H9XCZSReMj"
    DISCORD_BOT_SERVER_ID = 1037792926383747143
    BOT_SITE = "https://fistashkinbot.github.io/"
    BOT_INVITE = "https://discord.com/api/oauth2/authorize?client_id=991338113630752928&permissions=8&scope=bot%20applications.commands"
    GITHUB_REPOSITORY = "https://github.com/fistashkinbot/FistashkinBot-Beta"
    PATREON = "https://www.patreon.com/FistashkinBot"
    TELEGRAM = "https://t.me/riverya4lifeoff"

    def get_seasonal_copyright():
        now = datetime.datetime.now()
        if (now.month == 10 and now.day >= 31) or (now.month == 11 and now.day <= 2):
            return f"Риверька © {now.year} Все права защищены 🎃"

        elif (
            25 <= now.day <= 31
            and now.month == 12
            or (1 <= now.day <= 15 and now.month == 1)
        ):
            return f"Риверька © {now.year} Все права защищены ❄️"

        else:
            return f"Риверька © {now.year} Все права защищены 🍪"

    FOOTER_TEXT = get_seasonal_copyright()
    FOOTER_AVATAR = "https://github.com/riverya4life.png"


class EconomySystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = database.DataBase()
        self.otheremojis = constant.OtherEmojis()
        self.checks = checks.Checks(self.bot)

    def get_seasonal_bonus_eco():
        now = datetime.datetime.now()
        if (now.month == 10 and now.day >= 31) or (now.month == 11 and now.day <= 2):
            return {
                "exp": 5 * 4.0,
                "balance": 0.50 * 4.0,
                "multiplier": 4.0,
                "commission": 3,
            }

        elif (
            25 <= now.day <= 31
            and now.month == 12
            or (1 <= now.day <= 15 and now.month == 1)
        ):
            return {
                "exp": 5 * 8.0,
                "balance": 0.50 * 8.0,
                "multiplier": 8.0,
                "commission": 2,
            }

        else:
            return {"exp": 5, "balance": 0.50, "multiplier": 2.0, "commission": 4}

    economy = get_seasonal_bonus_eco()
    MULTIPLIER = economy["multiplier"]
    CURRENCY_NAME = "🍪"
    CURRENCY_EMOJI = "🍪"
    EXP_ACCRUAL = economy["exp"]
    BALANCE_ACCRUAL = economy["balance"]
    COMMISSION = economy["commission"]

    async def hit(self, inter, body_part, amount: int):
        await inter.response.defer(ephemeral=True)
        data = await self.db.get_data(inter.author)
        if amount > data["balance"]:
            return await self.checks.check_unknown(
                inter,
                text=f"У вас недостаточно **{self.CURRENCY_NAME}** для игры!",
            )
        else:
            await self.db.update_member(
                "UPDATE users SET balance = balance - ? WHERE member_id = ? AND guild_id = ?",
                [amount, inter.author.id, inter.guild.id],
            )
            if not random.choice(range(0, 4)):
                await self.db.update_member(
                    "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                    [amount * self.economy.MULTIPLIER, inter.author.id, inter.guild.id],
                )
                embed = disnake.Embed(
                    description=f"**Ты сделал {body_part} и отправил своего соперника в нокаут! Так держать, твой ты получаешь {amount * self.economy.MULTIPLIER} {self.CURRENCY_NAME} на свой баланс!**",
                    color=Color.GREEN,
                )
                embed.set_image(url=random.choice(self.rp.FIGHT_CLUB_VICTORY_IMAGES))
                embed.set_author(
                    name="Бойцовский клуб", icon_url=inter.author.display_avatar.url
                )
                await inter.edit_original_message(embed=embed, view=None)
            else:
                embed = disnake.Embed(
                    description=f"Ты сделал **{body_part}**, но противник защитился и сделал удар. Ты остался без 5 зубов и **{amount} {self.CURRENCY_NAME}**.",
                    color=Color.RED,
                )
                embed.set_image(url=random.choice(self.rp.FIGHT_CLUB_DEFEAT_IMAGES))
                embed.set_author(
                    name="Бойцовский клуб", icon_url=inter.author.display_avatar.url
                )
                await inter.edit_original_message(embed=embed, view=None)
