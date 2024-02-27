import disnake
import datetime

from disnake.ext import commands
from utils import CustomError, Support_Link, enums, checks, main
from loguru import logger

DESCRIPTIONS = {
    commands.MissingPermissions: "❌ У вас нет прав на выполнения этой команды!",
    commands.BotMissingPermissions: "❌ У бота нет прав на выполнения этой команды!",
    commands.UserNotFound: "❌ Указанный участник не найден. Проверьте ID/Тег/Никнейм на правильность.",
    commands.MemberNotFound: "❌ Указанный пользователь не найден., Проверьте ID/Тег/Никнейм на правильность.",
    commands.NSFWChannelRequired: "❌ Эта команда доступна только в каналах с пометкой NSFW!",
    commands.NotOwner: "❌ Ты не являешься владельцем или разработчиком бота, поэтому команда не доступна!",
    commands.RoleNotFound: "❌ Указанная роль не найдена.",
    disnake.Forbidden: "❌ У бота нет прав на выполнения этого действия!",
    50013: "❌ У бота нет прав на выполнения этого действия!",
}

PERMISSIONS = {
    "administrator": "Администратор",
    "ban_members": "Банить участников",
    "kick_members": "Выгонять участников",
    "manage_guild": "Управлять сервером",
    "send_messages": "Отправлять сообщения",
    "manage_members": "Управлять участниками",
    "view_channel": "Просматривать канал",
    "manage_roles": "Управлять ролями",
    "moderate_members": "Управлять участниками",
    "manage_messages": "Управлять сообщениями",
    "manage_channels": "Управлять каналами"
}


class OnErrors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.main = main.MainSettings()
        self.color = enums.Color()

    @commands.Cog.listener(disnake.Event.slash_command_error)
    @commands.Cog.listener(disnake.Event.error)
    async def on_slash_command_error(
        self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError
    ):
        # error = getattr(error, "original", error)
        logger.error(error)

        await inter.response.defer(ephemeral=True)

        embed = disnake.Embed(title=f"Произошла ошибка", color=self.color.RED)
        embed.description = DESCRIPTIONS.get(
            type(error) if not "50013" in str(error) else 50013,
            f"❌ Произошла неизвестная ошибка, пожалуйста, отправьте ошибку на [сервер технической поддержки]({self.main.DISCORD_BOT_SERVER})\n```py\n{str(error)}```",
        )
        view = Support_Link()

        if isinstance(
            error, (commands.MissingPermissions, commands.BotMissingPermissions)
        ):
            embed.add_field(
                name="Недостающие права",
                value=", ".join(
                    [PERMISSIONS.get(i, i) for i in error.missing_permissions]
                ),
            )
            view = None

        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_time = datetime.datetime.now() + datetime.timedelta(
                seconds=int(round(error.retry_after))
            )
            dynamic_time = disnake.utils.format_dt(cooldown_time, style="R")
            embed.description = f"⏱️ Вы достигли кулдауна этой команды. Вы сможете использовать её вновь {dynamic_time}!"
            view = None

        elif isinstance(error, commands.NSFWChannelRequired):
            channels = list(
                map(
                    lambda n: n.mention,
                    filter(lambda x: x.nsfw, inter.guild.text_channels),
                )
            )
            channel_list = " ".join(channels)
            if len(channels) != 0:
                embed.add_field(
                    name="Поэтому воспользуйтесь одним из NSFW-каналов:",
                    value=channel_list,
                )
            view = None

        elif isinstance(error, CustomError):
            embed.description = f"{error}"
            view = None

        await inter.edit_original_message(embed=embed, view=view)


def setup(bot):
    bot.add_cog(OnErrors(bot))
