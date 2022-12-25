import disnake
from disnake.ext import commands

from config import *
import random
import asyncio


class Dropdown(disnake.ui.StringSelect):
    def __init__(self):
        options = [
            disnake.SelectOption(label="Информация", description="Изучаю местность 🔮", emoji="📚"),
            disnake.SelectOption(label="Прочее", description="Что-то не важное 🎩", emoji="🎮")
        ]

        super().__init__(
            placeholder="Выберите группу…",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, inter: disnake.MessageInteraction):
        if self.values[0] == "Информация":
            embed1 = disnake.Embed(
                title = f'Доступные команды группы Информация 📚', 
                colour = botmaincolor, 
                timestamp=inter.created_at
            )
            embed1.add_field(name = f'{PREFIX}хелп', value = f'Справка по всем командам и категориям.', inline=False)
            embed1.add_field(name = f'{PREFIX}юзер', value = f'Показывает информацию об участнике.', inline=False)
            embed1.add_field(name = f'{PREFIX}сервер', value = f'Показывает информацию о сервере.', inline=False)
            embed1.add_field(name = f'{PREFIX}аватар', value = f'Показывает аватар упомянутого участника или участника, вызвавшего команду.', inline=False)
            embed1.add_field(name = f'{PREFIX}роли', value = f'Показывает все роли сервера.', inline=False)
            embed1.add_field(name = f'{PREFIX}инфо', value = f'Показывает интересную информацию о боте.', inline=False)

            embed1.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/991338113630752928/f3fd00030752cc638726b6118ab79299.png?size=1024')
            embed1.set_footer(text = f'{footerbyriverya4life}', icon_url = avatarbyfooterbyriverya4life)
            await inter.response.send_message(embed = embed1, ephemeral=True)

        elif self.values[0] == "Прочее":
            embed4 = disnake.Embed(
                title = f'Доступные команды группы Прочее 🎮', 
                colour = botmaincolor, 
                timestamp=inter.created_at
            )
            embed4.add_field(name = f'{PREFIX}шар', value = f'Отвечает на вопрос участника.', inline=False)
            #embed2.add_field(name = f'{PREFIX}размьют', value = f'', inline=False)
            embed4.add_field(name = f'{PREFIX}пинг', value = f'Проверка на работоспособность бота и задержки.', inline=False)
            embed4.add_field(name = f'{PREFIX}ник', value = f'Изменяет никнейм на сервере участнику, вызвавшего команду.', inline=False)

            embed4.set_thumbnail(url = 'https://cdn.discordapp.com/avatars/991338113630752928/f3fd00030752cc638726b6118ab79299.png?size=1024')
            embed4.set_footer(text = f'{footerbyriverya4life}', icon_url = avatarbyfooterbyriverya4life)
            await inter.response.send_message(embed = embed4, ephemeral=True)

        else:
            await inter.response.send_message(f"Группа {self.values[0]} временно не доступна", ephemeral=True)


class DropdownView(disnake.ui.View):
    def __init__(self, timeout = 120.0):
        super().__init__(timeout=timeout)
        self.add_item(Dropdown())


class HelpCMD(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = 'хелп', description = 'Показывает список доступных команд бота.', usage = 'хелп')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, inter):
        async with inter.typing():
            view = DropdownView()
            emb = disnake.Embed(
                title = '👾 Доступные команды', 
                description = 'Вы можете получить детальную справку по каждой команде, выбрав группу в меню снизу.', 
                colour = botmaincolor, 
                timestamp=inter.message.created_at
            )
            emb.set_author(name = inter.author.name, icon_url = inter.author.display_avatar.url)
            emb.add_field(name = '📚 Информация', value = f'`{PREFIX}хелп` `{PREFIX}юзер` `{PREFIX}сервер` `{PREFIX}аватар` `{PREFIX}роли` `{PREFIX}инфо`', inline=False)
            emb.add_field(name = '🎮 Прочее', value = f'`{PREFIX}шар` `{PREFIX}пинг` `{PREFIX}ник`', inline=False)
            emb.set_thumbnail(url = self.bot.user.display_avatar.url)
            emb.set_footer(text = f'{footerbyriverya4life}', icon_url = avatarbyfooterbyriverya4life)
            await asyncio.sleep(0.5)

            await inter.send(embed = emb, view=view)


def setup(bot):
    bot.add_cog(HelpCMD(bot))