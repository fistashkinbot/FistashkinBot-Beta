import disnake
from disnake.ext import commands

from config import *
import random
from disnake.enums import ButtonStyle


class CommandOtherBySlash(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        

    @commands.slash_command(name = 'шар', description = 'Отвечает на вопрос участника.', usage = 'шар Вопрос')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def шар(self, inter, *, question):
        responses = [
            'Это точно 👌',
            'Очень даже вряд-ли 🤨',
            'Нет ❌',
            'Да, безусловно ✔',
            'Вы можете рассчитывать на это 👌',
            'Вероятно 🤨',
            'Перспектива хорошая 🤔',
            'Да ✔',
            'Знаки указывают да 👍',
            'Ответ туманный, попробуйте еще раз 👀',
            'Спроси позже 👀',
            'Лучше не говорить тебе сейчас 🥵',
            'Не могу предсказать сейчас 👾',
            'Сконцентрируйтесь и спросите снова 🤨',
            'Не рассчитывай на это 🙉',
            'Мой ответ - Нет 😕',
            'Мои источники говорят нет 🤨',
            'Перспективы не очень 🕵️‍♂️',
            'Очень сомнительно 🤔',
            'ИДИ НАХУЙ! 🤬'
        ]
        embed = disnake.Embed(
            description=f'🎱 8ball', 
            color=botmaincolor, 
            timestamp=inter.created_at
        )
        embed.add_field(name=f'**Вопрос от {inter.author}:**', value=question, inline=True)
        embed.add_field(name='**Ответ: **', value=random.choice(responses), inline=False)
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        embed.set_footer(text = f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
        await inter.response.send_message(embed=embed)


    @commands.slash_command(name = 'пинг', description = 'Проверка на работоспособность бота и задержки.')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, inter):
        embed = disnake.Embed(
            description=f"{inter.author.mention}, я живой и кушаю фисташки!", 
            color=botmaincolor, 
            timestamp=inter.created_at
        )
        embed.set_footer(text=f'⏳ Пинг: {round(self.bot.latency * 1000)}ms | {footerbyriverya4life}', icon_url= avatarbyfooterbyriverya4life)
        await inter.response.send_message(embed=embed)


    @commands.slash_command(name = 'подключитьбота', description = 'Подключить бота к себе к голосовому каналу.', usage = 'подключитьбота', dm_permission=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.default_member_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def join(self, inter):
        channel = inter.author.voice.channel
        voice = disnake.utils.get(self.bot.voice_clients, guild=inter.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            await channel.connect()
            emb = disnake.Embed(
                description=f"Бот подключился к каналу {channel.mention}!", 
                timestamp=inter.created_at
            )
            emb.set_footer(text = f'{footerbyriverya4life}', icon_url =avatarbyfooterbyriverya4life)
            await inter.response.send_message(embed=emb)


    @commands.slash_command(name = 'отключитьбота', description = 'Отключить бота от голосового канала.', usage = 'отключитьбота', dm_permission=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.default_member_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def leave(self, inter):
        channel = inter.author.voice.channel
        voice = disnake.utils.get(self.bot.voice_clients, guild=inter.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            emb = disnake.Embed(
                description=f"Бот отключился от канала {channel.mention}!", 
                timestamp=inter.created_at
            )
            emb.set_footer(text = f'{footerbyriverya4life}', icon_url =avatarbyfooterbyriverya4life)
            await inter.response.send_message(embed=emb)
        else:
            emb = disnake.Embed(
                description=f"Бот не подключен к голосовому каналу и не может быть отключен!", 
                timestamp=inter.created_at
            )
            emb.set_footer(text = f'{footerbyriverya4life}', icon_url =avatarbyfooterbyriverya4life)
            await inter.response.send_message(embed=emb)


    @commands.slash_command(name = 'эмбед', description = 'Создание эмбеда без вебхуков.', usage = 'эмбед #Канал', dm_permission=False)
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.default_member_permissions(administrator=True)
    @commands.has_permissions(administrator=True)
    async def make_embed(self, inter, channel : disnake.TextChannel):

        def check(message):
            return message.author == inter.author and message.channel == inter.channel

        emb = disnake.Embed(
            description=f'**Привет!\nЯ твой помощник по созданию эмбеда!\nТы выбрал канал {channel.mention} для отправки эмбеда!\n\nДавай начнём с того как будет называться эмбед?**',
            timestamp=inter.created_at,
            color=inter.author.color
        )
        emb.set_footer(text=f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
        await inter.response.send_message(embed=emb, ephemeral=True)
        title = await self.bot.wait_for('message', check=check)
        await inter.channel.purge(limit = 2)
      
        emb = disnake.Embed(
            description=f'**Отлично!\nТы указал в названии эмбеда следующий текст: `{title.content}`\n\nТеперь укажи что будет в описании!**',
            timestamp=inter.created_at,
            color=inter.author.color
        )
        emb.set_footer(text=f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
        await inter.response.send_message(embed=emb, ephemeral=True)
        desc = await self.bot.wait_for('message', check=check)
        await inter.channel.purge(limit = 2)

        emb = disnake.Embed(
            description=f'**Отлично!\nЭмбед отправлен!\n\nНазвание:** {title.content}\n**Описание:** {desc.content}\n\n**Автор новостей:** {inter.author.mention}',
            timestamp=inter.created_at,
            color=inter.author.color
        )
        emb.set_footer(text=f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
        await inter.response.send_message(embed=emb)

        embed = disnake.Embed(title=title.content, description=desc.content, color=inter.author.color, timestamp=inter.created_at)
        embed.set_image(url='https://media.disnakeapp.net/attachments/881476440678350898/1007971296858099752/IMG_20220813_140341.png')
        embed.set_footer(text=f'Автор новостей: {inter.author.display_name} © 2022 | Все права защищены 🐒', icon_url=inter.author.display_avatar.url)

        await channel.send(content=f'||@everyone||\n', embed=embed)


    @commands.slash_command(name = 'калькулятор', description = '+ (сложить), - (вычесть), / (поделить), * (умножить) ** (возвести в степень), % (остаток от деления)')
    async def math(self, inter, firstnum: float, operator, secondnum: float):
        a = firstnum
        b = secondnum
        operations = ['+', '-', '/', '**', '%', '*']
        if operator not in operations:
            embed = disnake.Embed(description=f'{inter.author.mention}, Вы указали неверные действия. Ознакомьтесь с операторами в описании команды', color=botmaincolor, timestamp=inter.created_at)
            embed.set_footer(text = f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
            return await inter.response.send_message(embed=embed)
        elif operator == '+':
            c = a + b
            embed = disnake.Embed(description=f'Сумма `{a}` и `{b}` равна `{c}`.', color=botmaincolor, timestamp=inter.created_at)
            embed.set_footer(text = f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
            return await inter.response.send_message(embed=embed)
        elif operator == '-':
            c = a - b
            embed = disnake.Embed(description=f'Разность `{a}` от `{b}` равна `{c}`.', color=botmaincolor, timestamp=inter.created_at)
            embed.set_footer(text = f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
            return await inter.response.send_message(embed=embed)
        elif operator == '/':
            c = a / b
            embed = disnake.Embed(description=f'Частное `{a}` и `{b}` равно `{c}`.', color=botmaincolor, timestamp=inter.created_at)
            embed.set_footer(text = f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
            return await inter.response.send_message(embed=embed)
        elif operator == '**':
            c = a ** b
            embed = disnake.Embed(description=f'Результат от возведения `{a}` в степень `{b}` равен `{c}`.', color=botmaincolor, timestamp=inter.created_at)
            embed.set_footer(text = f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
            return await inter.response.send_message(embed=embed)
        elif operator == '%':
            c = a % b
            embed = disnake.Embed(description=f'Остаток от деления `{a}` на `{b}` равен `{c}`.', color=botmaincolor, timestamp=inter.created_at)
            embed.set_footer(text = f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
            return await inter.response.send_message(embed=embed)
        elif operator == '*':
            c = a * b
            embed = disnake.Embed(description=f'Произведение `{a}` и `{b}` равно `{c}`.', color=botmaincolor, timestamp=inter.created_at)
            embed.set_footer(text = f'{footerbyriverya4life}', icon_url=avatarbyfooterbyriverya4life)
            return await inter.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(CommandOtherBySlash(bot))