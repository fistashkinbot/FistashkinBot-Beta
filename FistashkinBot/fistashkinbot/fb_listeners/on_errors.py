import disnake
import datetime

from disnake.ext import commands
from utils import CustomError, Support_Link, enums, checks
from loguru import logger

DESCRIPTIONS = {
    commands.MissingPermissions: "❌ У вас нет прав на выполнения этой команды!",
    commands.BotMissingPermissions: "❌ У бота нет прав на выполнения этой команды!",
    commands.UserNotFound: "❌ Указанный участник не найден. Проверьте ID/Тег/Никнейм на правильность.",
    commands.MemberNotFound: "❌ Указанный пользователь не найден., Проверьте ID/Тег/Никнейм на правильность.",
    CustomError: "⚠️ Произошла какая-то ошибка, ошибка выведена в консоль.",
    commands.NSFWChannelRequired: "❌ Эта команда доступна только в каналах с пометкой NSFW!",
    commands.NotOwner: "❌ Ты не являешься владельцем или разработчиком бота, поэтому команда не доступна!",
    commands.RoleNotFound: "❌ Указанная роль не найдена.",
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
}


class OnErrors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = enums.Color()
        self.checks = checks.Checks(self.bot)

    @commands.Cog.listener(disnake.Event.slash_command_error)
    async def on_slash_command_error(
        self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError
    ):
        # error = getattr(error, "original", error)
        logger.error(error)

        if isinstance(error, commands.MissingPermissions):
            return await self.checks.check_missing_permissions(inter, error)

        elif isinstance(error, commands.BotMissingPermissions):
            return await self.checks.check_missing_permissions(inter, error)

        elif isinstance(error, commands.NotOwner):
            return await self.checks.check_not_owner(inter)

        elif isinstance(error, commands.CommandOnCooldown):
            cooldown_time = datetime.datetime.now() + datetime.timedelta(
                seconds=int(round(error.retry_after))
            )
            dynamic_time = disnake.utils.format_dt(cooldown_time, style="R")
            return await self.checks.check_cooldown(
                inter,
                text=f"⏱️ Вы достигли кулдауна этой команды. Вы сможете использовать её вновь {dynamic_time}!",
            )

        elif isinstance(error, commands.errors.MemberNotFound):
            return await self.checks.check_member_not_found(inter)

        elif isinstance(error, commands.NSFWChannelRequired):
            return await self.checks.check_is_nsfw(inter)

        elif isinstance(error, CustomError):
            return await self.checks.check_unknown_exception(
                inter,
                text=f"❌ Произошла неизвестная ошибка, пожалуйста, отправьте ошибку на [сервер технической поддержки](https://discord.com/channels/1037792926383747143/1066328008664813610)\n\n"
                f"**Код ошибки:**\n```{error}```",
            )


def setup(bot):
    bot.add_cog(OnErrors(bot))
