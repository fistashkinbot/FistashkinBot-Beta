import disnake
from disnake.ext import commands

from config import *
import random
import asyncio


class HelpCMDSlash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name = 'хелп', description = 'Показывает список доступных команд бота.', usage = 'хелп')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, inter):
        emb = disnake.Embed(
            title = '👾 Доступные команды', 
            description = 'Вы можете получить детальную справку по каждой команде, выбрав группу в меню снизу.', 
            colour = botmaincolor, 
            timestamp=inter.message.created_at
        )
        emb.set_author(name = inter.author.name, icon_url = inter.author.display_avatar.url)
        emb.add_field(name = '📚 Информация', value = f'`/хелп` `/юзер` `/сервер` `/аватар` `/роли` `/инфо`', inline=False)
        emb.add_field(name = '🎮 Прочее', value = f'`/шар` `/пинг` `/ник`', inline=False)
        emb.set_thumbnail(url = self.bot.user.display_avatar.url)
        emb.set_footer(text = f'{footerbyriverya4life}', icon_url = avatarbyfooterbyriverya4life)

        await inter.response.send_message(embed = emb, view=view)


def setup(bot):
    bot.add_cog(HelpCMDSlash(bot))
