import disnake
import random

from disnake.ext import commands
from utils import roleplay, main, enums, checks


class Fun(commands.Cog, name="Развлечение"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.rp = roleplay.RolePlay()
        self.main = main.MainSettings()
        self.eightball = roleplay.EightBall()
        self.color = enums.Color()
        self.checks = checks.Checks(self.bot)

    @commands.slash_command(name="шар", description="Отвечает на вопрос участника.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ball(
        self,
        inter: disnake.ApplicationCommandInteraction,
        question=commands.Param(name="вопрос", description="Введите свой вопрос"),
    ):
        await inter.response.defer(ephemeral=False)
        embed = disnake.Embed(color=self.color.MAIN)
        embed.add_field(
            name=f"**Вопрос от {inter.author}:**", value=question, inline=True
        )
        embed.add_field(
            name="**Ответ: **",
            value=random.choice(self.eightball.RESPONSES),
            inline=False,
        )
        embed.set_author(name="🎱 Игра 8ball")
        embed.set_thumbnail(url=inter.author.display_avatar.url)
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="поцеловать", description="Поцеловать участника.", dm_permission=False
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def kiss(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
    ):
        if user == inter.author:
            return await self.checks.check_interaction_rp(inter, text="поцеловать!")
        else:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(
                description=f"😳 {inter.author.mention} поцеловал участника {user.mention} в жаркие уста...",
                color=self.color.MAIN,
            )
            embed.set_image(url=random.choice(self.rp.KISS_IMAGES))
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="обнять", description="Обнять участника.", dm_permission=False
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def embrace(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
    ):
        if user == inter.author:
            return await self.checks.check_interaction_rp(inter, text="обнять!")
        else:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(
                description=f"🥰 {inter.author.mention} обнял участника {user.mention}!",
                color=self.color.MAIN,
            )
            embed.set_image(url=random.choice(self.rp.EMBRACE_IMAGES))
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="шлепнуть", description="Шлепнуть участника.", dm_permission=False
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def slap(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
    ):
        if user == inter.author:
            return await self.checks.check_interaction_rp(inter, text="шлёпнуть!")
        else:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(
                description=f"🤭 {inter.author.mention} шлепнул участника {user.mention}!",
                color=self.color.MAIN,
            )
            embed.set_image(url=random.choice(self.rp.SLAP_IMAGES))
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="ударить", description="Ударить участника.", dm_permission=False
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def beat(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
    ):
        if user == inter.author:
            return await self.checks.check_interaction_rp(inter, text="ударить!")

        else:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(
                description=f"😡 {inter.author.mention} ударил участника {user.mention}!",
                color=self.color.MAIN,
            )
            embed.set_image(url=random.choice(self.rp.BEAT_IMAGES))
            await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))
