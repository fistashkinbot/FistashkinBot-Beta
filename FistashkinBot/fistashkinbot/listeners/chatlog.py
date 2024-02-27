import disnake
import re
import string
import fnmatch

from utils import database, automod
from disnake.ext import commands


class ChatLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = database.DataBase()
        self.automod = automod.Automod()

    @commands.Cog.listener(disnake.Event.message)
    async def on_message(self, message):
        if (
            message.author.bot
            or message.is_system()
            or message.guild is None
            or self.bot.uptime.timestamp() > message.created_at.timestamp()
        ):
            return
        for ban_word in message.content.lower().split():
            for word_pattern in self.automod.BAN_WORDS:
                if fnmatch.fnmatch(ban_word, word_pattern):
                    return
        else:
            record = await self.clean_message(message.clean_content)
            if record:
                await self.db.add_item(message.guild.id, record)

    async def clean_message(self, message):
        text = message.lower()
        text = text.replace(self.bot.user.name.lower(), "")  # Remove bot name
        text = re.sub(
            r"@(\w+)\s*", "", text
        )  # Remove user mentions and keep the rest of the message
        text = re.sub(r"<a?(:\w+:)\d+>", "", text)  # Remove custom emojis
        text = re.sub(r"\b\d{10,}\b", "", text)  # Remove phone numbers
        text = text.replace("codex", "")
        # text = re.sub(r"""(\s)\#\w+""", "", text)
        text = re.sub(
            r"""(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)"""
            r"""(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+"""
            r"""(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|"""
            r"""[^\s`!()\[\]{};:'".,<>?«»“”‘’]))""",
            "",
            text,
        )  # Remove URLs
        depunctuate = str.maketrans("", "", string.punctuation)
        text = text.translate(depunctuate)
        text = " ".join(text.split())
        return text


def setup(bot):
    bot.add_cog(ChatLog(bot))
