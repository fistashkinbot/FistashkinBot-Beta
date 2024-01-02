import disnake
import datetime
import random

from disnake.ext import commands
from utils import database, constant, enums, main, automod, links, checks


class Listeners(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = database.DataBase()
        self.otheremojis = constant.OtherEmojis()
        self.color = enums.Color()
        self.main = main.MainSettings()
        self.economy = main.EconomySystem(self.bot)
        self.automod = automod.Automod()
        self.enum = enums.Enum()
        self.checks = checks.Checks(self.bot)

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

        for member in guild.members:
            await self.db.insert_new_member(member)
        print(
            f"Сервер {guild.name} был добавлен в базу данных! Добавлено новых участников: {len(guild.members)}"
        )

        await self.automod.automod(guild)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or not message.guild or message.author == self.bot.user:
            return

        if len(message.content) >= 6:
            data = await self.db.get_data(message.author)
            if data["xp"] >= 500 + 100 * data["level"]:
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

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter, error):
        error = getattr(error, "original", error)
        print(error)

        if isinstance(error, commands.MissingPermissions):
            return await self.checks.check_missing_permissions(inter)

        elif isinstance(error, commands.NotOwner):
            return await self.checks.check_not_owner(inter)

        elif isinstance(error, commands.BotMissingPermissions):
            return await self.checks.check_bot_missing_permissions(inter)

        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_time = datetime.datetime.now() + datetime.timedelta(
                seconds=int(round(error.retry_after))
            )
            dynamic_time = disnake.utils.format_dt(cooldown_time, style="R")
            return await self.checks.check_cooldown(
                inter,
                text=f"❌ Превышен лимит использования команды! Повтори {dynamic_time}!",
            )

        elif isinstance(error, commands.errors.MemberNotFound):
            return await self.checks.check_member_not_found(inter)

        elif isinstance(error, Exception):
            return await self.checks.check_unknown_exception(
                inter,
                text=f"❌ Произошла неизвестная ошибка, пожалуйста, отправьте ошибку на [сервер технической поддержки](https://discord.com/channels/1037792926383747143/1066328008664813610)\n\n"
                f"**Код ошибки:**\n```{error}```",
            )


def setup(bot):
    bot.add_cog(Listeners(bot))
