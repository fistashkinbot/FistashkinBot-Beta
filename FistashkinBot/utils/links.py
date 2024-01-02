import disnake

from utils import constant, main


class Links(disnake.ui.View):
    def __init__(self):
        self.otheremoji = constant.OtherEmojis()
        self.main = main.MainSettings()

        super().__init__()
        self.add_item(
            disnake.ui.Button(
                label="Репозиторий GitHub",
                url=self.main.GITHUB_REPOSITORY,
                emoji=self.otheremoji.GITHUB,
            )
        )
        self.add_item(
            disnake.ui.Button(
                label="Сервер Discord",
                url=self.main.DISCORD_BOT_SERVER,
                emoji=self.main.BOT_EMOJI,
            )
        )
        self.add_item(
            disnake.ui.Button(
                label="Patreon", url=self.main.PATREON, emoji=self.otheremoji.PATREON
            )
        )
        self.add_item(
            disnake.ui.Button(
                label="Пригласить бота",
                url=self.main.BOT_INVITE,
                emoji=self.main.BOT_EMOJI,
            )
        )
        self.add_item(
            disnake.ui.Button(
                label="Telegram канал",
                url=self.main.TELEGRAM,
                # emoji = self.otheremoji.TELEGRAM
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
