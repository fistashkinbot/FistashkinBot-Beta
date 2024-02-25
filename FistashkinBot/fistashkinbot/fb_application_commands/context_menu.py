import disnake

from disnake.ext import commands
from utils import database, constant, main, enums, links


class ContextMenu(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = database.DataBase()
        self.main = main.MainSettings()
        self.economy = main.EconomySystem(self.bot)
        self.profile = constant.ProfileEmojis()
        self.color = enums.Color()
        self.enum = enums.Enum()

    @commands.user_command(
        name=disnake.Localized("Avatar", key="CONTEXT_MENU_COMMAND_AVATAR"),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def avatar(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = None,
    ):
        await inter.response.defer(ephemeral=True)
        if not member:
            member = inter.author

        formats = [
            f"[**[PNG]**]({member.display_avatar.replace(format='png', size=4096).url}) | ",
            f"[**[JPG]**]({member.display_avatar.replace(format='jpg', size=4096).url})",
            f" | [**[WebP]**]({member.display_avatar.replace(format='webp', size=4096).url})",
            f" | [**[GIF]**]({member.display_avatar.replace(format='gif', size=4096).url})"
            if member.display_avatar.is_animated()
            else "",
            f"\n[**[Стандартный аватар]**]({member.default_avatar.url})",
        ]
        description_format = "".join(formats)
        embed = disnake.Embed(
            description=f"Нажмите ниже чтобы скачать аватар\n{description_format}",
            color=self.color.MAIN,
        )
        embed.set_image(url=member.display_avatar.url)
        embed.set_author(
            name=f"Аватар {member.display_name}", icon_url=member.display_avatar.url
        )
        await inter.edit_original_message(embed=embed)

    @commands.user_command(
        name=disnake.Localized("UserInfo", key="CONTEXT_MENU_COMMAND_USERINFO"),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def userinfo(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = None,
    ):
        await inter.response.defer(ephemeral=True)
        data = await self.db.get_data(member)
        registerf = disnake.utils.format_dt(member.created_at, style="f")
        registerr = disnake.utils.format_dt(member.created_at, style="R")
        joinedf = disnake.utils.format_dt(member.joined_at, style="f")
        joinedr = disnake.utils.format_dt(member.joined_at, style="R")

        level = self.enum.format_large_number(data["level"])
        xp = self.enum.format_large_number(data["xp"])
        total_xp = self.enum.format_large_number(data["total_xp"])
        xp_to_lvl = self.enum.format_large_number(
            5 * (data["level"] ** 2) + 50 * data["level"] + 100
        )
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
            f"**Имя {'бота' if member.bot else 'участника'}:** {member} ({member.mention})",
            f"**Статус:** {self.profile.STATUS[member.status]}",  # **| Устройство:** {'`📱 Mobile`' if member.is_on_mobile() else '`🖥️ Desktop`'}
            f"**Присоединился:** {joinedf} ({joinedr})",
            f"**Дата регистрации:** {registerf} ({registerr})",
        ]
        view = None
        if not member.bot:
            if member.activities:
                for activity in member.activities:
                    if activity.type == disnake.ActivityType.playing:
                        description.append(
                            f"**Играет в:** {activity.name} | <t:{round(activity.created_at.timestamp())}:R>"
                        )

                    elif activity.type == disnake.ActivityType.streaming:
                        description.append(f"**Стримит:** {activity.name}")

                    elif activity.type == disnake.ActivityType.watching:
                        description.append(f"**Смотрит:** {activity.name}")

                    if activity.type == disnake.ActivityType.listening:
                        if isinstance(activity, disnake.Spotify):
                            description.append(
                                f"**Cлушает Spotify:** {self.profile.SPOTIFY} **[{activity.title} | {', '.join(activity.artists)}]({activity.track_url})**"
                            )
                            view = links.Spotify_Link(url=activity.track_url)
                        else:
                            description.append(f"**Слушает:** {activity.name}")

        if (
            member.bot
            or member != inter.author
            and bio
            == "Вы можете добавить сюда какую-нибудь полезную информацию о себе командой `/осебе`"
        ):
            bio = None

        embed = disnake.Embed(
            description=bio,
            color=user.accent_color,
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
                value=f"{balance} {self.economy.CURRENCY_NAME}",
                inline=True,
            )

            if response is not None:
                embed.add_field(name="Значки", value=" ".join(response), inline=True)

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_image(url=user.banner.url if user.banner else None)
        embed.set_footer(text=f"ID: {member.id}", icon_url=member.display_avatar.url)
        embed.set_author(
            name=f"Информация о {'боте' if member.bot else 'участнике'} {member.display_name}",
            icon_url=member.display_avatar.url,
        )
        await inter.edit_original_message(embed=embed, view=view)


def setup(bot):
    bot.add_cog(ContextMenu(bot))
