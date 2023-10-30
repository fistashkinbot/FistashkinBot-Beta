import disnake

from disnake.ext import commands
from utils import database, constant, main, enums


class ContextMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = database.DataBase()
        self.main = main.MainSettings()
        self.economy = main.EconomySystem()
        self.profile = constant.ProfileEmojis()
        self.color = enums.Color()

    @commands.user_command(
        name="Аватар",
        description="Показывает аватар упомянутого участника или участника, вызвавшего команду.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
        await inter.response.defer(ephemeral=True)
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

    @commands.user_command(
        name="Юзер",
        description="Показывает информацию об участнике.",
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member = None):
        await inter.response.defer(ephemeral=True)
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
            pass
        elif member.top_role is not None:
            top_role = member.top_role.mention
            description.append(f"**Приоритетная роль:** {top_role}")

        if member.activities:
            for activity in member.activities:
                if isinstance(activity, disnake.Spotify):
                    description.append(
                        f"{self.profile.SPOTIFY} **Cлушает Spotify:** [{activity.artist} - {activity.title}]({activity.track_url})"
                    )

        embed = disnake.Embed(
            description=f"\n ".join(description),
            color=member.color,
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


def setup(bot):
    bot.add_cog(ContextMenu(bot))
