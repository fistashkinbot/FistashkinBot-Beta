import os
import traceback
import disnake

from disnake.ext import commands


class FistashkinBot(commands.AutoShardedInteractionBot):
    def __init__(self, *args):
        super().__init__(
            intents=disnake.Intents.all(),
            sync_commands_debug=False,
            chunk_guilds_at_startup=False,
            reload=True,
            *args,
        )

    def load_extensions(self):
        for filename in os.listdir("./fistashkinbot"):
            if filename.endswith(".py"):
                try:
                    self.load_extension(f"fistashkinbot.{filename[:-3]}")
                except Exception as e:
                    traceback.format_exc(e)
