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
            'Очень сомнительно 🤔'
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
