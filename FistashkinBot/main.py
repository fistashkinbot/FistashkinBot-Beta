import disnake
import platform
import random

from disnake.ext import tasks
from core import Config, FistashkinBot
from utils import BotActivity, MainSettings

if __name__ == "__main__":
    bot = FistashkinBot()
    bot.load_extensions()
    bot.i18n.load("./localization")

    @tasks.loop(minutes=30)
    async def change_activity():
        await bot.change_presence(
            status=random.choice(BotActivity.STATUS),
            activity=random.choice(BotActivity.ACTIVITY),
        )

    @bot.event
    async def on_ready():
        developer = await bot.fetch_user(MainSettings.DEVELOPER_ID)
        START_MESSAGE = f"""
                     ______   _         _                   _       _      _           ____            _   
                    |  ____| (_)       | |                 | |     | |    (_)         |  _ \          | |  
                    | |__     _   ___  | |_    __ _   ___  | |__   | | __  _   _ __   | |_) |   ___   | |_ 
                    |  __|   | | / __| | __|  / _` | / __| | '_ \  | |/ / | | | '_ \  |  _ <   / _ \  | __|
                    | |      | | \__ \ | |_  | (_| | \__ \ | | | | |   <  | | | | | | | |_) | | (_) | | |_ 
                    |_|      |_| |___/  \__|  \__,_| |___/ |_| |_| |_|\_\ |_| |_| |_| |____/   \___/   \__|
        ----------------------------------------------------------------------------------------------------------------

                                                         Официальный бот!
                                                      ----------------------
                              Discord бот! / Разработчик - {developer.display_name} / Дата создания: {bot.user.created_at.strftime("%d.%m.%Y")}
                                                      ----------------------
                              -----------------------/     {bot.user.display_name}    \----------------------

        ################################################################################################################

        -
        Разработчик - {developer.display_name} (@{developer} ID: {developer.id})
        Бот - {bot.user} (ID: {bot.user.id})
        Пинг - {round(bot.latency * 1000)} мс

        Создан для официального Discord сервера "Riverya Brotherhood"

        Язык програмирования - Python {platform.python_version()}
        Библиотека разработки - {disnake.__title__} {disnake.__version__}
        -
        """
        print(f"\n - Бот успешно подключен - \n")
        print(START_MESSAGE)
        change_activity.start()

    bot.run(Config.TOKEN)
