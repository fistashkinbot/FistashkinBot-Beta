import disnake
import random
import json
import requests

from disnake.ext import commands
from utils import constant, main, enums, checks
from bs4 import BeautifulSoup


class Fun(commands.Cog, name="Развлечение"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.rp = constant.RolePlay()
        self.main = main.MainSettings()
        self.eightball = constant.EightBall()
        self.color = enums.Color()
        self.checks = checks.Checks(self.bot)

    @commands.slash_command(
        name=disnake.Localized("ball", key="EIGHT_BALL_COMMAND_NAME"),
        description=disnake.Localized(
            "Answers a users question.", key="EIGHT_BALL_COMMAND_DESCRIPTION"
        ),
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
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
        name=disnake.Localized("kiss", key="KISS_COMMAND_NAME"),
        description=disnake.Localized("Kiss the user.", key="KISS_COMMAND_DESCRIPTION"),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def kiss(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        req = requests.get(f"https://nekos.life/api/v2/img/kiss")

        if req.status_code != 200:
            return await self.checks.check_unknown(inter, text=f"Ошибка API!")

        elif member == inter.author:
            return await self.checks.check_interaction_rp(inter, text="поцеловать")

        elif member.bot:
            return await self.checks.check_unknown(
                inter, text=f"Ты не можешь взаимодействовать с ботами!"
            )

        else:
            await inter.response.defer(ephemeral=False)
            api_json = json.loads(req.text)
            url = api_json["url"]
            embed = disnake.Embed(
                description=f"😳 {inter.author.mention} поцеловал участника {member.mention}!",
                color=self.color.MAIN,
            )
            embed.set_image(url=url)
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("cuddle", key="CUDDLE_COMMAND_NAME"),
        description=disnake.Localized(
            "Hug the user.", key="CUDDLE_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def cuddle(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        req = requests.get(f"https://nekos.life/api/v2/img/cuddle")

        if req.status_code != 200:
            return await self.checks.check_unknown(inter, text=f"Ошибка API!")

        elif member == inter.author:
            return await self.checks.check_interaction_rp(inter, text="обнять")

        elif member.bot:
            return await self.checks.check_unknown(
                inter, text=f"Ты не можешь взаимодействовать с ботами!"
            )

        else:
            await inter.response.defer(ephemeral=False)
            api_json = json.loads(req.text)
            url = api_json["url"]
            embed = disnake.Embed(
                description=f"🥰 {inter.author.mention} обнял участника {member.mention}!",
                color=self.color.MAIN,
            )
            embed.set_image(url=url)
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("pet", key="PET_COMMAND_NAME"),
        description=disnake.Localized("Pet the user.", key="PET_COMMAND_DESCRIPTION"),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def pat(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        req = requests.get(f"https://nekos.life/api/v2/img/pat")

        if req.status_code != 200:
            return await self.checks.check_unknown(inter, text=f"Ошибка API!")

        elif member == inter.author:
            return await self.checks.check_interaction_rp(inter, text="погладить")

        elif member.bot:
            return await self.checks.check_unknown(
                inter, text=f"Ты не можешь взаимодействовать с ботами!"
            )

        else:
            await inter.response.defer(ephemeral=False)
            api_json = json.loads(req.text)
            url = api_json["url"]
            embed = disnake.Embed(
                description=f"🥰 {inter.author.mention} погладил участника {member.mention}!",
                color=self.color.MAIN,
            )
            embed.set_image(url=url)
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("tickle", key="TICKLE_COMMAND_NAME"),
        description=disnake.Localized(
            "Tickle the user.", key="TICKLE_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def tickle(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        req = requests.get(f"https://nekos.life/api/v2/img/tickle")

        if req.status_code != 200:
            return await self.checks.check_unknown(inter, text=f"Ошибка API!")

        elif member == inter.author:
            return await self.checks.check_interaction_rp(inter, text="пощекотать")

        elif member.bot:
            return await self.checks.check_unknown(
                inter, text=f"Ты не можешь взаимодействовать с ботами!"
            )

        else:
            await inter.response.defer(ephemeral=False)
            api_json = json.loads(req.text)
            url = api_json["url"]
            embed = disnake.Embed(
                description=f"🥰 {inter.author.mention} пощекотал участника {member.mention}!",
                color=self.color.MAIN,
            )
            embed.set_image(url=url)
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("feed", key="FEED_COMMAND_NAME"),
        description=disnake.Localized("Feed the user.", key="FEED_COMMAND_DESCRIPTION"),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def feed(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        req = requests.get(f"https://nekos.life/api/v2/img/feed")

        if req.status_code != 200:
            return await self.checks.check_unknown(inter, text=f"Ошибка API!")

        elif member == inter.author:
            return await self.checks.check_interaction_rp(
                inter, text="покормить без тяночки"
            )

        elif member.bot:
            return await self.checks.check_unknown(
                inter, text=f"Ты не можешь взаимодействовать с ботами!"
            )

        else:
            await inter.response.defer(ephemeral=False)
            api_json = json.loads(req.text)
            url = api_json["url"]
            embed = disnake.Embed(
                description=f"🥰 {inter.author.mention} накормил участника {member.mention}!",
                color=self.color.MAIN,
            )
            embed.set_image(url=url)
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("slap", key="SLAP_COMMAND_NAME"),
        description=disnake.Localized("Slap the user.", key="SLAP_COMMAND_DESCRIPTION"),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def slap(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        req = requests.get(f"https://nekos.life/api/v2/img/slap")

        if req.status_code != 200:
            return await self.checks.check_unknown(inter, text=f"Ошибка API!")

        elif member == inter.author:
            return await self.checks.check_interaction_rp(inter, text="шлепнуть")

        elif member.bot:
            return await self.checks.check_unknown(
                inter, text=f"Ты не можешь взаимодействовать с ботами!"
            )

        else:
            await inter.response.defer(ephemeral=False)
            api_json = json.loads(req.text)
            url = api_json["url"]
            embed = disnake.Embed(
                description=f"🤭 {inter.author.mention} шлепнул участника {member.mention}!",
                color=self.color.MAIN,
            )
            embed.set_image(url=url)
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("hit", key="HIT_COMMAND_NAME"),
        description=disnake.Localized("Hit the user.", key="HIT_COMMAND_DESCRIPTION"),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def hit(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        req = requests.get(f"https://nekos.life/api/v2/img/slap")

        if req.status_code != 200:
            return await self.checks.check_unknown(inter, text=f"Ошибка API!")

        if member == inter.author:
            return await self.checks.check_interaction_rp(inter, text="ударить")

        elif member.bot:
            return await self.checks.check_unknown(
                inter, text=f"Ты не можешь взаимодействовать с ботами!"
            )

        else:
            await inter.response.defer(ephemeral=False)
            api_json = json.loads(req.text)
            url = api_json["url"]
            embed = disnake.Embed(
                description=f"😡 {inter.author.mention} ударил участника {member.mention}!",
                color=self.color.MAIN,
            )
            embed.set_image(url=url)
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


def setup(bot):
    bot.add_cog(Fun(bot))
