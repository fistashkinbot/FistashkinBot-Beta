import disnake

from utils import constant, main


class Links(disnake.ui.View):
    def __init__(self):
        self.otheremoji = constant.OtherEmojis()
        self.main = main.MainSettings()

        super().__init__()
        self.add_item(
            disnake.ui.Button(
                label="Наш Сайт",
                url=self.main.BOT_SITE,
                emoji="🍪",
            )
        )


class Support_Link(disnake.ui.View):
    def __init__(self):
        self.otheremoji = constant.OtherEmojis()
        self.main = main.MainSettings()

        super().__init__()
        self.add_item(
            disnake.ui.Button(
                label="Сервер поддержки",
                url=self.main.DISCORD_BOT_SERVER,
                emoji=self.main.BOT_EMOJI,
            )
        )


class BotMonitoring(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(
            disnake.ui.Button(
                label="Top.gg",
                url="https://top.gg/bot/991338113630752928",
            )
        ),
        self.add_item(
            disnake.ui.Button(
                label="BotiCord",
                url="https://boticord.top/bot/991338113630752928",
            )
        )
        self.add_item(
            disnake.ui.Button(
                label="SD.C",
                url="https://bots.server-discord.com/991338113630752928",
            )
        )


class Developer_Link(disnake.ui.View):
    def __init__(self):
        self.otheremoji = constant.OtherEmojis()
        self.main = main.MainSettings()

        super().__init__()
        self.add_item(
            disnake.ui.Button(
                label="Разработчик",
                url="https://discord.com/users/668453200457760786",
                emoji=self.main.BOT_EMOJI,
            )
        )
