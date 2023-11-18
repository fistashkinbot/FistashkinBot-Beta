import disnake

from disnake.ext import commands
from utils import enums, main


class Slash_Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.color = enums.Color()
        self.main = main.MainSettings()

    @commands.slash_command(
        name=disnake.Localized("help", key="HELP"),
        description=disnake.Localized(
            "Shows a list of available bot commands.", key="HELP_DESCR"
        ),
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)
        debug = ["OwnerInfo", "Casino", "ContextMenu", "RoleAddToReactionTest", "Listeners", "Slash_Help"]

        embed = disnake.Embed(
            description=f"Вы можете получить детальную справку по каждой из команд, выбрав группу в меню снизу.",
            colour=self.color.MAIN,
        )

        for cog in self.bot.cogs:
            if not isinstance(cog, commands.Cog):
                cog = self.bot.get_cog(cog)

            if cog is None:
                RuntimeError

            if cog.qualified_name in debug:
                continue

            text = ""

            for slash_command in cog.get_application_commands():
                api_slash_command = self.bot.get_global_command_named(name=slash_command.name)
                if api_slash_command is not None:
                    text += f"</{slash_command.name}:{api_slash_command.id}> "
                else:
                    text += f"{slash_command.name} "

            embed.add_field(name=cog.qualified_name, value=cog.description + '\n' + text, inline=False)

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_author(
            name=f"Доступные команды бота {self.bot.user.name}",
            icon_url=self.bot.user.display_avatar.url,
        )
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)
        await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(Slash_Help(bot))
