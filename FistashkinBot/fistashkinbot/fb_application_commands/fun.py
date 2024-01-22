import disnake
import random
import json
import requests
import aiohttp

from disnake.ext import commands
from utils import constant, main, enums, checks
from bs4 import BeautifulSoup
from typing import Optional
from helpers.fun_helper import MineswiperView
from itertools import repeat
from services import waifu_pics


class Fun(commands.Cog, name="😄 Развлечение"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.rp = constant.RolePlay()
        self.main = main.MainSettings()
        self.eightball = constant.EightBall()
        self.color = enums.Color()
        self.checks = checks.Checks(self.bot)

    NSFW_DESCRIPTIONS = {
        "Задницы (ass)": "ass",
        "БДСМ (bdsm)": "bdsm",
        "Кам) (cum)": "cum",
        "Девушки-доминаторы (femdom)": "femdom",
        "Хентай (hentai)": "hentai",
        "Инцест (incest)": "incest",
        "Мастурбация (masturbation)": "masturbation",
        "Эротика (ero)": "ero",
        "Оргия (orgy)": "orgy",
        "Юри (yuri)": "yuri",
        "Трусики (pantsu)": "pantsu",
        "Очко (очки) (glasses)": "glasses",
        "Работа ручками (handjob)": "handjob",
        "Блоуджоб (blowjob)": "blowjob",
        "Работа грудью (boobjob)": "boobjob",
        "Просто грудь (boobs)": "boobs",
        "Ножки (footjob)": "footjob",
        "Ещё больше хентая (hentai gifs)": "gif",
        "Ахегао (ahegao)": "ahegao",
        "Школьницы и не только... (uniform)": "uniform",
        "Щупальца (tentacles)": "tentacles",
        "Бёдра (thighs)": "thighs",
        "Кошко-девочки (nsfw neko)": "nsfwNeko",
        "Юбочки (zettai ryouiki)": "zettaiRyouiki",
    }

    ANIME_GIRLS = {
        "Мегумин": "megumin",
        "Шинобу": "shinobu",
        "Ававо": "awoo",
        "Неко": "neko",
        "Поке": "poke",
    }

    RP_DESCRIPTIONS = {
        "pat": "Погладил(-а) {user}",
        "hug": "Обнял(-а) {user}",
        "kiss": "Поцеловал(-а) {user}",
        "lick": "Облизнул(-а) {user}",
        "cuddle": "Прижал(-а) к себе {user}",
        "handhold": "Взял(-а) за руку {user}",
        "nom": "Покормил(-а) {user}",
        "slap": "Дал(-а) пощечину {user}",
        "bite": "Сделал(-а) кусь {user}",
        "highfive": "Дал(-а) пять {user}",
    }

    RP_DESCRIPTIONS_MYSELF = {
        "pat": "Погладил(-а) себя",
        "hug": "Обнял(-а) себя",
        "kiss": "Поцеловал(-а) себя",
        "lick": "Облизнул(-а) себя",
        "cuddle": "Прижал(-а) себя к себе",
        "handhold": "Взял(-а) себя за руку",
        "nom": "Покормил(-а) себя",
        "slap": "Дал(-а) себе пощёчину",
        "bite": "Укусил(-а) себя",
        "highfive": "Дал(-а) себе пять",
    }

    RP_DESCRIPTIONS_FISTASHKIN = {
        "pat": "Погладил(-а) {user}",
        "hug": "Обнял(-а) {user}",
        "kiss": "Поцеловал(-а) {user}",
        "lick": "Облизнул(-а) {user}",
        "cuddle": "Прижал(-а) к себе {user}",
        "handhold": "Взял(-а) за руку {user}",
        "nom": "Покормил(-а) {user}",
        "slap": "Дал(-а) пощечину {user}",
        "bite": "Ай... За шо? qwq",
        "highfive": "🖐️",
    }

    @commands.slash_command(
        name=disnake.Localized("ball", key="EIGHT_BALL_COMMAND_NAME"),
        description=disnake.Localized(
            "Answers a users question.", key="EIGHT_BALL_COMMAND_DESCRIPTION"
        ),
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
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
    @commands.cooldown(1, 15, commands.BucketType.user)
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
            description=f"**{descriptions[choice].format(user=member.display_name)}**",
            color=self.color.MAIN,
        )
        embed.set_image(url=await waifu_pics.get_image("sfw", choice))
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("cat", key="CAT_COMMAND_NAME"),
        description=disnake.Localized(
            "Show a random picture with a cat.", key="CAT_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def cat(self, inter: disnake.ApplicationCommandInteraction):
        req = requests.get("https://api.thecatapi.com/v1/images/search")
        if req.status_code != 200:
            return await self.checks.check_unknown(inter, text=f"Ошибка API!")

        await inter.response.defer(ephemeral=False)

        catlink = json.loads(req.text)[0]
        rngcat = catlink["url"]
        embed = disnake.Embed(color=self.color.DARK_GRAY)
        embed.set_image(url=rngcat)
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("dog", key="DOG_COMMAND_NAME"),
        description=disnake.Localized(
            "Show a random picture of a dog.", key="DOG_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def dog(self, inter: disnake.ApplicationCommandInteraction):
        req = requests.get("http://random.dog/")
        if req.status_code != 200:
            return await self.checks.check_unknown(inter, text=f"Ошибка API!")

        await inter.response.defer(ephemeral=False)

        doglink = BeautifulSoup(req.text, "html.parser")
        rngdog = "http://random.dog/" + doglink.img["src"]
        embed = disnake.Embed(color=self.color.DARK_GRAY)
        embed.set_image(url=rngdog)
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("nsfw", key="NSFW_COMMAND_NAME"),
        description=disnake.Localized(
            "Well... It was not bad.", key="NSFW_COMMAND_DESCRIPTION"
        ),
    )
    @commands.is_nsfw()
    @commands.cooldown(1, 15, commands.BucketType.user)
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
            return await self.checks.check_unknown(inter, text=f"Ошибка API!")

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
    @commands.cooldown(1, 15, commands.BucketType.user)
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
    @commands.cooldown(1, 15, commands.BucketType.user)
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
    @commands.cooldown(1, 15, commands.BucketType.user)
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


def setup(bot):
    bot.add_cog(Fun(bot))
