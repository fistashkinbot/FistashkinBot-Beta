import disnake

from disnake.ext import commands
from utils import enums, main


class Dropdown(disnake.ui.StringSelect):
    def __init__(self):
        self.color = enums.Color()
        self.main = main.MainSettings()

        options = [
            disnake.SelectOption(label="Информация", emoji="📚"),
            disnake.SelectOption(label="Модерирование", emoji="🏆"),
            disnake.SelectOption(label="Экономика", emoji="🍃"),
            disnake.SelectOption(label="Развлечения", emoji="🎮"),
        ]

        super().__init__(
            placeholder="Выберите группу…",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if self.values[0] == "Информация":
            embed = disnake.Embed(
                title=f"Доступные команды группы Информация 📚",
                colour=self.color.MAIN,
                timestamp=inter.created_at,
            )
            embed.add_field(
                name=f"</хелп:1046871805186555985>",
                value=f"Справка по всем командам и категориям.",
                inline=False,
            )
            embed.add_field(
                name=f"</юзер:1137843670008201269>",
                value=f"Показывает информацию об участнике.",
                inline=False,
            )
            embed.add_field(
                name=f"</сервер:1137843670008201270>",
                value=f"Показывает информацию о сервере.",
                inline=False,
            )
            embed.add_field(
                name=f"</аватар:1046871805186555988>",
                value=f"Показывает аватар упомянутого участника или участника, вызвавшего команду.",
                inline=False,
            )
            embed.add_field(
                name=f"</роли:1046871805186555989>",
                value=f"Показывает все роли сервера.",
                inline=False,
            )
            embed.add_field(
                name=f"</инфо:1046871805186555990>",
                value=f"Показывает интересную информацию о боте.",
                inline=False,
            )
            embed.add_field(
                name=f"</стат:1066444943012401174>",
                value=f"Показывает статистику бота.",
                inline=False,
            )
            embed.add_field(
                name=f"</вопрос:1058971805064376400>",
                value=f"Смотрите наиболее часто задаваемые вопросы.",
                inline=False,
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/991338113630752928/f3fd00030752cc638726b6118ab79299.png?size=1024"
            )
            embed.set_footer(
                text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "Модерирование":
            embed = disnake.Embed(
                title=f"Доступные команды группы Модерирование 🏆",
                colour=self.color.MAIN,
            )
            embed.add_field(
                name=f"</мьют:1046871805186555991>",
                value=f"Отправляет участника подумать о своём поведении.",
                inline=False,
            )
            embed.add_field(
                name=f"/размьют", value=f"Снимает наказание с участника.", inline=False
            )
            embed.add_field(
                name=f"</бан:1046871805186555993>",
                value=f"Изгоняет указанного участника с сервера навсегда.",
                inline=False,
            )
            embed.add_field(
                name=f"</разбан:1046871805249474681>",
                value=f"Разбанивает указанного участника на сервере по его ID, имени или тегу.",
                inline=False,
            )
            embed.add_field(
                name=f"</кик:1046871805186555992>",
                value=f"Изгоняет указанного участника с сервера с возможностью возвращения.",
                inline=False,
            )
            embed.add_field(
                name=f"</очистить:1046871805249474688>",
                value=f"Очищает определенное количество сообщений в канале.",
                inline=False,
            )
            embed.add_field(
                name=f"</выдатьроль:1046871805249474684>",
                value=f"Выдает указанную роль участнику.",
                inline=False,
            )
            embed.add_field(
                name=f"</снятьроль:1046871805249474685>",
                value=f"Снимает указанную роль участнику.",
                inline=False,
            )
            embed.add_field(
                name=f"</создатьроль:1046871805249474683>",
                value=f"Создание роли на сервере.",
                inline=False,
            )
            embed.add_field(
                name=f"</клист:1046871805249474687>",
                value=f"Выводит список участников с определенной ролью.",
                inline=False,
            )
            embed.add_field(
                name=f"</задержка:1046871805249474686>",
                value=f"Устанавливает задержку на общение в чате.",
                inline=False,
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/991338113630752928/f3fd00030752cc638726b6118ab79299.png?size=1024"
            )
            embed.set_footer(
                text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "Экономика":
            embed = disnake.Embed(
                title=f"Доступные команды группы Экономика 🍃", colour=self.color.MAIN
            )
            embed.add_field(
                name=f"</баланс:1046871804985213072>",
                value=f"Показывает баланс участника или участника, вызвавшего команду.",
                inline=False,
            )
            embed.add_field(
                name=f"</перевести:1046871804985213073>",
                value=f"Перевеводит деньги участнику.",
                inline=False,
            )
            embed.add_field(
                name=f"</купитьроль:1046871804985213077>",
                value=f"Покупка роли с магазина ролей.",
                inline=False,
            )
            embed.add_field(
                name=f"</магазин:1046871804985213076>",
                value=f"Магазин, в котором можно покупать роли.",
                inline=False,
            )
            embed.add_field(
                name=f"</лидеры:1046871804985213074>",
                value=f"Показывает топ рейтинга участников по балансу.",
                inline=False,
            )
            embed.add_field(
                name=f"</слот:1046871805186555984>",
                value=f"Игра в слот машину.",
                inline=False,
            )

            embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/991338113630752928/f3fd00030752cc638726b6118ab79299.png?size=1024"
            )
            embed.set_footer(
                text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

        elif self.values[0] == "Развлечения":
            embed = disnake.Embed(
                title=f"Доступные команды группы Развлечения 🎮", colour=self.color.MAIN
            )
            embed.add_field(
                name=f"</шар:1046871804985213068>",
                value=f"Отвечает на вопрос участника.",
                inline=False,
            )
            embed.add_field(
                name=f"</пинг:1046871804985213069>",
                value=f"Проверка на работоспособность бота и задержки.",
                inline=False,
            )
            embed.add_field(
                name=f"</ник:1046871805249474682>",
                value=f"Изменяет никнейм на сервере участнику, вызвавшего команду.",
                inline=False,
            )
            embed.add_field(
                name=f"</калькулятор:1055794544463069275>",
                value=f"Простой обычный калькулятор.",
                inline=False,
            )
            embed.add_field(
                name=f"</поцеловать:1058381090877878352>",
                value=f"Поцеловать участника.",
                inline=False,
            )
            embed.add_field(
                name=f"</обнять:1058381090877878353>",
                value=f"Обнять участника.",
                inline=False,
            )
            embed.add_field(
                name=f"</шлепнуть:1058382633815523388>",
                value=f"Шлепнуть участника.",
                inline=False,
            )
            embed.add_field(
                name=f"</ударить:1058383187010650153>",
                value=f"Ударить участника.",
                inline=False,
            )
            embed.set_thumbnail(
                url="https://cdn.discordapp.com/avatars/991338113630752928/f3fd00030752cc638726b6118ab79299.png?size=1024"
            )
            embed.set_footer(
                text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR
            )
            await inter.response.send_message(embed=embed, ephemeral=True)

        else:
            await inter.response.send_message(
                f"Группа {self.values[0]} временно не доступна", ephemeral=True
            )


class DropdownView(disnake.ui.View):
    message: disnake.Message

    def __init__(self):
        super().__init__(timeout=120.0)
        self.add_item(Dropdown())

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, disnake.ui.StringSelect):
                child.disabled = True
        await self.message.edit(view=self)


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
        view = DropdownView()

        def get_command_mention(self, name: str):
            command = self.bot.get_slash_command(name)
            return f"</{command.name}:{command.id}>" if command else f"/{name}"

        command_number = 1

        embed = disnake.Embed(
            description=f"Вы можете получить детальную справку по каждой из **{command_number} команд**, выбрав группу в меню снизу.",
            colour=self.color.MAIN,
        )
        embed.set_author(
            name=inter.author.name, icon_url=inter.author.display_avatar.url
        )

        for c in self.bot.cogs:
            cog = self.bot.get_cog(c)
            if len([cog.application_commands()]):
                embed.add_field(
                    name=f"__**{cog.qualified_name}**__",
                    value=f", ".join(
                        f"</{command.name}:{command.id}>"
                        for command in (
                            cog.global_application_commands
                            and cog.global_slash_commands
                        )
                    ),
                    inline=True,
                )
                command_number += 1

        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.set_author(
            name=f"Доступные команды бота {self.bot.user.name}",
            icon_url=self.bot.user.display_avatar.url,
        )
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)
        message = await inter.edit_original_message(embed=embed, view=view)
        view.message = message


def setup(bot):
    bot.add_cog(Slash_Help(bot))
