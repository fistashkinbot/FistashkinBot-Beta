import disnake
import random
import aiohttp

from disnake.ext import commands
from utils import constant, main, enums, CustomError
from bs4 import BeautifulSoup
from typing import Optional, Union
from helpers.fun_helper import MineswiperView
from itertools import repeat
from services import waifu_pics
from io import BytesIO
from googletrans import Translator


async def translator(word, lang):
    return Translator().translate(word, dest=lang).text


class Fun(commands.Cog, name="😄 Развлечение"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.main = main.MainSettings()
        self.eightball = constant.EightBall()
        self.color = enums.Color()

    NSFW_DESCRIPTIONS = {
        "Задницы": "ass",
        "БДСМ": "bdsm",
        "Кам)": "cum",
        "Девушки-доминаторы": "femdom",
        "Хентай": "hentai",
        "Инцест": "incest",
        "Мастурбация": "masturbation",
        "Эротика": "ero",
        "Оргия": "orgy",
        "Юри": "yuri",
        "Трусики": "pantsu",
        "Очко (очки)": "glasses",
        "Работа ручками": "handjob",
        "Блоуджоб": "blowjob",
        "Работа грудью": "boobjob",
        "Просто грудь": "boobs",
        "Ножки": "footjob",
        "Ещё больше хентая": "gif",
        "Ахегао": "ahegao",
        "Школьницы и не только...": "uniform",
        "Щупальца": "tentacles",
        "Бёдра": "thighs",
        "Кошко-девочки": "nsfwNeko",
        "Юбочки": "zettaiRyouiki",
    }

    ANIME_GIRLS = {
        "Мегумин": "megumin",
        "Шинобу": "shinobu",
        "Ававо": "awoo",
        "Неко": "neko",
        "Поке": "poke",
        "Рандом вайфу": "waifu",
    }

    RP_DESCRIPTIONS = {
        "pat": "{author} погладил(-а) {user}",
        "hug": "{author} обнял(-а) {user}",
        "kiss": "{author} поцеловал(-а) {user}",
        "lick": "{author} облизнул(-а) {user}",
        "cuddle": "{author} прижал(-а) к себе {user}",
        "handhold": "{author} взял(-а) за руку {user}",
        "nom": "{author} покормил(-а) {user}",
        "slap": "{author} дал(-а) пощечину {user}",
        "bite": "{author} сделал(-а) кусь {user}",
        "highfive": "{author} дал(-а) пять {user}",
    }

    RP_DESCRIPTIONS_MYSELF = {
        "pat": "{author} погладил(-а) себя",
        "hug": "{author} обнял(-а) себя",
        "kiss": "{author} поцеловал(-а) себя",
        "lick": "{author} облизнул(-а) себя",
        "cuddle": "{author} прижал(-а) себя к себе",
        "handhold": "{author} взял(-а) себя за руку",
        "nom": "{author} покормил(-а) себя",
        "slap": "{author} дал(-а) себе пощёчину",
        "bite": "{author} укусил(-а) себя",
        "highfive": "{author} дал(-а) себе пять",
    }

    RP_DESCRIPTIONS_FISTASHKIN = {
        "pat": "{author} погладил(-а) {user}",
        "hug": "{author} обнял(-а) {user}",
        "kiss": "{author} поцеловал(-а) {user}",
        "lick": "{author} облизнул(-а) {user}",
        "cuddle": "{author} прижал(-а) к себе {user}",
        "handhold": "{author} взял(-а) за руку {user}",
        "nom": "{author} покормил(-а) {user}",
        "slap": "{author} ну не надо так со мной :(",
        "bite": "{author} ай... За шо ты так со мной?",
        "highfive": "{author} держи пятюню 🖐️",
    }

    @commands.slash_command(
        name=disnake.Localized("ball", key="EIGHT_BALL_COMMAND_NAME"),
        description=disnake.Localized(
            "Answers a users question.", key="EIGHT_BALL_COMMAND_DESCRIPTION"
        ),
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ball(
        self,
        inter: disnake.ApplicationCommandInteraction,
        question=commands.Param(
            name=disnake.Localized("question", key="EIGHT_BALL_COMMAND_TEXT_NAME"),
            description=disnake.Localized(
                "Enter your question.", key="EIGHT_BALL_COMMAND_TEXT_DESCRIPTION"
            ),
        ),
    ):
        await inter.response.defer(ephemeral=False)
        embed = disnake.Embed(description=question, color=self.color.MAIN)
        embed.add_field(
            name="**Ответ: **",
            value=random.choice(self.eightball.RESPONSES),
            inline=False,
        )
        embed.set_author(name="🎱 Игра 8ball")
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("rp", key="RP_COMMAND_NAME"),
        description=disnake.Localized(
            "Interact with the user.", key="RP_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def rp(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            lambda inter: inter.author,
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
        choice: str = commands.Param(
            name=disnake.Localized("choice", key="RP_COMMAND_CHOICE_NAME"),
            description=disnake.Localized(
                "Choose what interaction you want to do.",
                key="RP_COMMAND_CHOICE_DESCRIPTION",
            ),
            choices=[disnake.OptionChoice(x, x) for x in RP_DESCRIPTIONS.keys()],
        ),
    ):
        await inter.response.defer(ephemeral=False)
        descriptions = (
            self.RP_DESCRIPTIONS
            if member != inter.author and member != inter.bot.user
            else self.RP_DESCRIPTIONS_MYSELF
            if member == inter.author
            else self.RP_DESCRIPTIONS_FISTASHKIN
        )
        embed = disnake.Embed(
            description=f"**{descriptions[choice].format(author=inter.author.display_name, user=member.display_name)}**",
            color=self.color.MAIN,
        )
        embed.set_image(url=await waifu_pics.get_image("sfw", choice))
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("nsfw", key="NSFW_COMMAND_NAME"),
        description=disnake.Localized(
            "Well... It was not bad.", key="NSFW_COMMAND_DESCRIPTION"
        ),
    )
    @commands.is_nsfw()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def nsfw(
        self,
        inter: disnake.ApplicationCommandInteraction,
        choice: str = commands.Param(
            name=disnake.Localized("choice", key="NSFW_COMMAND_CHOICE_NAME"),
            description=disnake.Localized(
                "Choose something from the list.",
                key="NSFW_COMMAND_CHOICE_DESCRIPTION",
            ),
            choices=[disnake.OptionChoice(x, x) for x in NSFW_DESCRIPTIONS.keys()],
        ),
    ):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://hmtai.hatsunia.cfd/nsfw/{self.NSFW_DESCRIPTIONS.get(choice)}"
                ) as response:
                    data = await response.json()
        except:
            raise CustomError("❌ Ошибка API!")

        await inter.response.defer(ephemeral=False)
        embed = disnake.Embed(color=self.color.MAIN)
        embed.set_image(url=data["url"])
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("anime-chan", key="ANIME_CHAN_COMMAND_NAME"),
        description=disnake.Localized(
            "Anime-chan!", key="ANIME_CHAN_COMMAND_DESCRIPTION"
        ),
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def anime_girl(
        self,
        inter: disnake.ApplicationCommandInteraction,
        choice: str = commands.Param(
            name=disnake.Localized("choice", key="ANIME_CHAN_CHOICE_NAME"),
            description=disnake.Localized(
                "Select the tag with anime-chan.", key="ANIME_CHAN_CHOICE_DESCRIPTION"
            ),
            choices=[disnake.OptionChoice(x, x) for x in ANIME_GIRLS.keys()],
        ),
    ):
        await inter.response.defer(ephemeral=False)
        embed = disnake.Embed(
            description=f"Картинка с **{choice.title()}**", color=self.color.MAIN
        )
        image = await waifu_pics.get_image("sfw", self.ANIME_GIRLS.get(choice))
        embed.set_image(url=image)
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("minesweeper", key="MINESWEEPER_COMMAND_NAME"),
        description=disnake.Localized(
            "Play minesweeper mini-game.", key="MINESWEEPER_COMMAND_DESCRIPTION"
        ),
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mine(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)
        board = [["\u200b"] * 5] * 5
        bombs = 0
        bombpositions = []
        for x in repeat(None, random.randint(4, 11)):
            random_index = random.randint(0, 19)
            if random_index not in bombpositions and random_index not in [
                0,
                4,
                20,
                24,
            ]:
                bombpositions.append(random_index)
                bombs += 1

        def ExtractBlocks():
            new_b = []
            for x in board:
                for y in x:
                    new_b.append(y)
            return new_b

        view = MineswiperView(inter, ExtractBlocks(), bombpositions, board)
        message = await inter.edit_original_message(
            f"Всего бомб: `{len(bombpositions)}`",
            view=view,
        )
        view.message = message

    @commands.slash_command(
        name=disnake.Localized("dice", key="ROLLDICE_COMMAND_NAME"),
        description=disnake.Localized(
            "Play a mini-game with rolling a dice.", key="ROLLDICE_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roll_dice(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)
        dice_roll = random.randint(1, 6)

        embed = disnake.Embed(
            description=f"[`🎲`] На кубике выпала цифра: **{dice_roll}**",
            color=self.color.MAIN,
        )
        embed.set_author(name="🎲 Кости")
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        embed.set_footer(text="💝 Оп, оп-ля!")
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("animal", key="ANIMAL_COMMAND_NAME"),
        description=disnake.Localized(
            "It outputs a random photo of the chosen animal.",
            key="ANIMAL_COMMAND_DESCRIPTION",
        ),
    )
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def animal(
        self,
        inter: disnake.ApplicationCommandInteraction,
        animal: str = commands.Param(
            name=disnake.Localized("choice", key="ANIMAL_CHOICE_NAME"),
            description=disnake.Localized(
                "Please choose an animal.", key="ANIMAL_CHOICE_DESCRIPTION"
            ),
            choices={
                "Лиса": "fox",
                "Енот": "raccoon",
                "Кошка": "cat",
                "Собака": "dog",
                "Птица": "bird",
                "Кенгуру": "kangaroo",
                "Коала": "koala",
                "Панда": "panda",
            },
        ),
    ):
        try:
            await inter.response.defer(ephemeral=False)
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"https://some-random-api.com/animal/{animal}"
                ) as resp:
                    data = await resp.json()

            word = data["fact"]
            fact = await translator(word, "ru")
            embed = disnake.Embed(
                description=f"**Факт:** {fact}", color=self.color.MAIN
            )
            embed.set_image(url=data["image"])
            await inter.edit_original_message(embed=embed)
        except Exception as e:
            raise CustomError("Возникла проблема при отправке запроса на сервер!")


def setup(bot):
    bot.add_cog(Fun(bot))
