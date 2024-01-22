import disnake
import random

from disnake.ext import commands
from utils import database, constant, enums, main


class DB_Event(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = database.DataBase()
        self.otheremojis = constant.OtherEmojis()
        self.color = enums.Color()
        self.economy = main.EconomySystem(self.bot)
        self.enum = enums.Enum()

    @commands.Cog.listener()
    async def on_ready(self):
        await self.db.create_table()

        for guild in self.bot.guilds:
            for member in guild.members:
                await self.db.insert_new_member(member)
        print(f"{len(guild.members)} участников было добавлено в базу данных!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.db.insert_new_member(member)
        print(f"Участник {member} ({member.id}) был добавлен в базу данных!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for member in guild.members:
            await self.db.insert_new_member(member)
        print(
            f"Сервер {guild.name} был добавлен в базу данных! Добавлено новых участников: {len(guild.members)}"
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild or message.author == self.bot.user:
            return

        if len(message.content) >= 6:
            data = await self.db.get_data(message.author)
            if data["xp"] >= 5 * (data["level"] ** 2) + 50 * data["level"] + 100:
                await self.db.update_member(
                    "UPDATE users SET level = level + ? WHERE member_id = ? AND guild_id = ?",
                    [1, message.author.id, message.guild.id],
                )
                await self.db.update_member(
                    "UPDATE users SET xp = ? WHERE member_id = ? AND guild_id = ?",
                    [0, message.author.id, message.guild.id],
                )

                new_level = self.enum.format_large_number(data["level"] + 1)

                LEVEL_UP_TEXT = [
                    f"{random.choice(self.otheremojis.RANKED_UP)} | {message.author.mention}, ты повысил свой уровень на **{new_level} LVL!**",
                    f"{random.choice(self.otheremojis.RANKED_UP)} | {message.author.mention}, ничего себе! Ты апнул свой уровень до **{new_level} LVL!**",
                    f"{random.choice(self.otheremojis.RANKED_UP)} | Полегче {message.author.mention}, ты продвинулся до **{new_level}** уровня! Поздравляю!",
                    f"{random.choice(self.otheremojis.RANKED_UP)} | Воу-воу-воу {message.author.mention}, что ты делаешь? Ты повысил свой уровень до **{new_level} LVL!**",
                    f"{random.choice(self.otheremojis.RANKED_UP)} | {message.author.mention} да ты монстр! Твой уровень был повышен до **{new_level} LVL!**",
                    f"{random.choice(self.otheremojis.RANKED_UP)} | {message.author.mention} Поздравляю! Ты достиг **{new_level} LVL!**",
                    f"{random.choice(self.otheremojis.RANKED_UP)} | Ура! {message.author.mention} только что достиг **{new_level} LVL!** Мои поздравления ^•^",
                ]

                embed = disnake.Embed(
                    description=random.choice(LEVEL_UP_TEXT), color=self.color.MAIN
                )
                embed.set_author(
                    name="Новый уровень!",
                    icon_url=message.author.display_avatar.url,
                )
                await message.channel.send(embed=embed, delete_after=10.0)

            else:
                if (
                    message.guild.premium_subscriber_role in message.author.roles
                    or message.author.premium_since
                ):
                    await self.db.update_member(
                        "UPDATE users SET xp = xp + ? WHERE member_id = ? AND guild_id = ?",
                        [
                            self.economy.EXP_ACCRUAL * self.economy.MULTIPLIER,
                            message.author.id,
                            message.guild.id,
                        ],
                    )
                    await self.db.update_member(
                        "UPDATE users SET total_xp = total_xp + ? WHERE member_id = ? AND guild_id = ?",
                        [
                            self.economy.EXP_ACCRUAL * self.economy.MULTIPLIER,
                            message.author.id,
                            message.guild.id,
                        ],
                    )
                    await self.db.update_member(
                        "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                        [
                            self.economy.BALANCE_ACCRUAL * self.economy.MULTIPLIER,
                            message.author.id,
                            message.guild.id,
                        ],
                    )
                else:
                    await self.db.update_member(
                        "UPDATE users SET xp = xp + ? WHERE member_id = ? AND guild_id = ?",
                        [self.economy.EXP_ACCRUAL, message.author.id, message.guild.id],
                    )
                    await self.db.update_member(
                        "UPDATE users SET total_xp = total_xp + ? WHERE member_id = ? AND guild_id = ?",
                        [self.economy.EXP_ACCRUAL, message.author.id, message.guild.id],
                    )
                    await self.db.update_member(
                        "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                        [
                            self.economy.BALANCE_ACCRUAL,
                            message.author.id,
                            message.guild.id,
                        ],
                    )

    @commands.Cog.listener()
    async def on_slash_command_completion(
        self, inter: disnake.ApplicationCommandInteraction
    ):
        await self.db.insert_command_count()

    @commands.Cog.listener()
    async def on_user_command_completion(
        self, inter: disnake.ApplicationCommandInteraction
    ):
        await self.db.insert_command_count()


def setup(bot):
    bot.add_cog(DB_Event(bot))
