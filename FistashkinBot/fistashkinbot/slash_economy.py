import disnake
import random

from disnake.ext import commands
from utils import database, main, enums, constant, paginator, RankCard, Settings, checks
from PIL import ImageColor


class CasinoView(disnake.ui.View):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)
        super().__init__(timeout=120.0)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @disnake.ui.button(
        label="Монетка", 
        emoji="🪙", 
        custom_id="coin", 
        style=disnake.ButtonStyle.primary
    )
    async def coin_button_callback(self, button, inter):
        return await self.economy.coin_frame(inter, view=CoinButtons(inter))

    @disnake.ui.button(
        label="Кейсы", 
        emoji="📦", 
        custom_id="case", 
        style=disnake.ButtonStyle.primary
    )
    async def case_button_callback(self, button, inter):
        return await self.economy.case_frame(inter, view=CaseButtons(inter))

    @disnake.ui.button(
        label="Бойцовский клуб", 
        emoji="👊", 
        custom_id="fightclub", 
        style=disnake.ButtonStyle.primary
    )
    async def bk_button_callback(self, button, inter):
        return await self.economy.fight_club_frame(inter, view=FightButton(inter))

class CoinButtons(disnake.ui.View):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)
        super().__init__(timeout=120.0)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @disnake.ui.button(
        label="Орёл", 
        emoji="🪙", 
        style=disnake.ButtonStyle.primary
    )
    async def orel_button_callback(self, button, inter):
        return await self.economy.coin_button_callback(inter, view=ReturnCoinButtons(inter))

    @disnake.ui.button(
        label="Решка", 
        emoji="🪙", 
        style=disnake.ButtonStyle.primary
    )
    async def reshka_button_callback(self, button, inter):
        return await self.economy.coin_button_callback(inter, view=ReturnCoinButtons(inter))

    @disnake.ui.button(
        label="Изменить ставку", 
        emoji="💠", 
        style=disnake.ButtonStyle.success
    )
    async def change_bit_button_callback(self, button, inter):
        await inter.response.send_modal(modal=InputBit(self.bot))

    @disnake.ui.button(
        label="Вернуться", 
        emoji="👈", 
        custom_id="back", 
        style=disnake.ButtonStyle.gray
    )
    async def back_button_callback(self, button, inter):
        pass

class InputBit(disnake.ui.Modal):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.otheremojis = constant.OtherEmojis()
        self.economy = main.EconomySystem(self.bot)
        components=[
            disnake.ui.TextInput(
                label="Ставка", 
                placeholder="Введите свою ставку", 
                custom_id="bit", 
                style=disnake.TextInputStyle.short, 
                max_length=50,
            )
        ]
        super().__init__(title="Орёл-решка", components=components, custom_id="money_amount")

    async def callback(self, inter: disnake.ModalInteraction):
        try:
            check = int(inter.text_values["bit"])
            if check > 10:
                return await inter.response.edit_message(
                    embed=self.economy.COIN_FRAME.set_field_at(index=0, value=str(check), name="Ставка")
                )

            await inter.send(
                embed = disnake.Embed(
                    title=f"{self.otheremojis.WARNING} Ошибка!", 
                    description="**Вы ввели некорректные данные, попробуйте ещё раз.**"), 
                ephemeral=True
            )
        except ValueError:
            return await inter.send(
                embed = disnake.Embed(
                    title=f"{self.otheremojis.WARNING} Ошибка!", 
                    description="**Вы ввели некорректные данные, попробуйте ещё раз.**"), 
                ephemeral=True
            )

class FightButton(disnake.ui.View):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)
        super().__init__(timeout=120.0)

    async def on_timeout(self, inter):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @disnake.ui.button(
        label="Удар в ноги", 
        emoji="🦵", 
        custom_id="legs_hit", 
        style=disnake.ButtonStyle.primary
    )
    async def legs_button_callback(self, button, inter):
        return await self.economy.hit(inter, "удар в ноги", view=ReturnFightClubButtons(inter))

    @disnake.ui.button(
        label="Удар в живот", 
        emoji="👊", 
        custom_id="torso_hit", 
        style=disnake.ButtonStyle.primary
    )
    async def torso_button_callback(self, button, inter):
        return await self.economy.hit(inter, "удар в живот", view=ReturnFightClubButtons(inter))

    @disnake.ui.button(
        label="Удар в голову", 
        emoji="🤕", 
        custom_id="head_hit", 
        style=disnake.ButtonStyle.primary
    )
    async def head_button_callback(self, button, inter):
        return await self.economy.hit(inter, "удар в голову", view=ReturnFightClubButtons(inter))

    @disnake.ui.button(
        label="Вернуться", 
        emoji="👈", 
        custom_id="back", 
        style=disnake.ButtonStyle.gray
    )
    async def back_button_callback(self, button, inter):
        pass

class CaseButtons(disnake.ui.View):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)
        super().__init__(timeout=120.0)

    async def on_timeout(self, inter):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @disnake.ui.button(
        label=f"Открыть кейс (10 FC)", #{self.economy.CURRENCY_NAME[:-28]} 
        #emoji=self.economy.CURRENCY_EMOJI, 
        custom_id="open_case", 
        style=disnake.ButtonStyle.success
    )
    async def open_case_button_callback(self, button, inter):
        return await self.economy.open_case_callback(inter, view=ReopenCaseButtons(inter))

    @disnake.ui.button(
        label="Вернуться", 
        emoji="👈", 
        custom_id="back", 
        style=disnake.ButtonStyle.gray
    )
    async def back_button_callback(self, button, inter):
        pass

class ReopenCaseButtons(disnake.ui.View):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)
        super().__init__(timeout=120.0)

    async def on_timeout(self, inter):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @disnake.ui.button(
        label="Вернуться", 
        emoji="👈", 
        custom_id="back_to_case", 
        style=disnake.ButtonStyle.gray
    )
    async def back_to_case_button_callback(self, button, inter):
        return await self.economy.case_frame(inter, view=CaseButtons(inter))

class ReturnFightClubButtons(disnake.ui.View):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)
        super().__init__(timeout=120.0)

    async def on_timeout(self, inter):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @disnake.ui.button(
        label="Вернуться", 
        emoji="👈", 
        custom_id="back_to_fight_club", 
        style=disnake.ButtonStyle.gray
    )
    async def back_to_fightclub_button_callback(self, button, inter):
        return await self.economy.fight_club_frame(inter, view=FightButton(inter))

class ReturnCoinButtons(disnake.ui.View):
    message: disnake.Message
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)
        super().__init__(timeout=120.0)

    async def on_timeout(self, inter):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @disnake.ui.button(
        label="Вернуться", 
        emoji="👈", 
        custom_id="back_to_coin", 
        style=disnake.ButtonStyle.gray
    )
    async def back_to_coin_button_callback(self, button, inter):
        return await self.economy.coin_frame(inter, view=CoinButtons(inter))


class Economy(commands.Cog, name="Экономика"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.main = main.MainSettings()
        self.economy = main.EconomySystem(self.bot)
        self.db = database.DataBase()
        self.color = enums.Color()
        self.otheremojis = constant.OtherEmojis()
        self.checks = checks.Checks(self.bot)
        self.profile = constant.ProfileEmojis()

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter):
        if inter.component.custom_id == "back":
            return await self.economy.casino_frame(inter, view=CasinoView(self.bot))

    @commands.slash_command(
        name="казино", 
        description="Место, где вы проведёте время с кайфом.", 
        dm_permission=False,
    )
    async def casino_menu(self, inter: disnake.ApplicationCommandInteraction):
        return await self.economy.casino_frame(inter, view=CasinoView(self.bot))

    @commands.slash_command(
        name="баланс",
        description="Показывает баланс участника или участника, вызвавшего команду.",
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def user_balance(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            lambda inter: inter.author, name="участник", description="Выбор участника"
        ),
    ):
        await inter.response.defer()
        data = await self.db.get_data(member)

        if (
            not member
        ):  # если не упоминать участника тогда выводит аватар автора сообщения
            member = inter.author

        embed = disnake.Embed(
            description=f"Баланс {member.mention} составляет **{data['balance']} {self.economy.CURRENCY_NAME}**\n"
            f"Уровень: **{data['level']}** (XP: **{data['xp']}/{500 + 100 * data['level']}**)",
            color=self.color.MAIN,
        )
        embed.set_author(name=f"Баланс участника", icon_url=member.display_avatar.url)
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="ранг",
        description="Показывает ранг участника или участника, вызвавшего команду.",
        dm_permission=False,
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def user_rank(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            lambda inter: inter.author, name="участник", description="Выбор участника"
        ),
    ):
        await inter.response.defer()

        if (
            not member
        ):  # если не упоминать участника тогда выводит аватар автора сообщения
            member = inter.author

        user = await self.bot.fetch_user(member.id)
        data = await self.db.get_data(member)
        if member.top_role == member.guild.default_role:
            hex_color = "#A53143"
        else:
            hex_color = ImageColor.getcolor(str(member.top_role.color), "RGB")
            hex_color = "#{0:02x}{1:02x}{2:02x}".format(*hex_color)

        card_settings = Settings(
            background="https://e0.pxfuel.com/wallpapers/793/114/desktop-wallpaper-haikyuu-kozume-kenma-kageyama-tobio-azumane-asahi-nishinoya-yuu.jpg",
            background_color="#000000",
            text_color="white",
            bar_color="#e39e7e",
        )
        rank = RankCard(
            settings=card_settings,
            avatar=user.display_avatar.url,
            status=member.status,
            level=data["level"],
            current_exp=data["xp"],
            max_exp=500 + 100 * data["level"],
            username=f"@{user.name}",
        )
        image = await rank.card()
        await inter.edit_original_message(file=disnake.File(image, filename="rank.png"))

    @commands.slash_command(
        name="перевести",
        description="Перевеводит деньги участнику.",
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def pay_cash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name="участник", description="Выбор участника"
        ),
        amount: int = commands.Param(
            name="сумма", description="Cумма, которую хотите перевести участнику"
        ),
    ):
        data = await self.db.get_data(inter.author)
        if amount is None:
            return await self.checks.check_amount_is_none(inter)

        if member == inter.author:
            return await self.checks.check_user_author(
                inter, text=f"перевести **{self.economy.CURRENCY_NAME}**"
            )

        if amount > data["balance"]:
            return await self.checks.check_unknown(
                inter,
                text=f"у вас недостаточно **{self.economy.CURRENCY_NAME}** для перевода!",
            )

        if amount <= 0:
            return await self.checks.check_unknown(
                inter, text=f"укажите сумму больше **1 {self.economy.CURRENCY_NAME}**!"
            )

        else:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(
                description=f"{inter.author.mention}, вы успешно перевели **{amount} {self.economy.CURRENCY_NAME}** участнику {member.mention}!",
                color=self.color.MAIN,
            )
            embed.set_author(
                name="Перевод денег участнику", icon_url=member.display_avatar.url
            )
            embed.set_footer(
                text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR
            )
            await self.db.update_member(
                "UPDATE users SET balance = balance - ? WHERE member_id = ? AND guild_id = ?",
                [amount, inter.author.id, inter.guild.id],
            )
            await self.db.update_member(
                "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                [amount, member.id, inter.guild.id],
            )
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="лидеры", description="Показывает топ рейтинга участников по чему-то.", dm_permission=False,
    )
    async def leadersboard(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @leadersboard.sub_command(
        name="баланс",
        description="Показывает топ рейтинга участников по балансу.",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def server_leadersboard_balance(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)

        data = await self.db.get_data(
            inter.guild.id, all_data=True, filters="ORDER BY balance DESC"
        )
        embeds = []
        counter = 0
        current_embed = disnake.Embed(
            description=f"👑 Список лидеров по балансу на сервере {inter.guild.name}!",
            color=self.color.MAIN,
        )

        for row in data:
            user = self.bot.get_user(row["member_id"])
            member = inter.guild.get_member(row["member_id"])
            if member is not None and not member.bot:
                if counter != 0 and counter % 5 == 0:
                    current_embed.set_author(
                        name=f"Топ лидеров сервера",
                        icon_url=inter.guild.icon.url if inter.guild.icon else None,
                    )
                    current_embed.set_thumbnail(
                        url=inter.guild.icon.url if inter.guild.icon else None
                    )
                    embeds.append(current_embed)
                    current_embed = disnake.Embed(
                        description=f"👑 Список лидеров по балансу на сервере {inter.guild.name}!",
                        color=self.color.MAIN,
                    )

                counter += 1
                current_embed.add_field(
                    name=f"#{counter} | `{self.bot.get_user(row['member_id'])}`",
                    value=f"**Баланс:** {row['balance']} {self.economy.CURRENCY_NAME}",
                    inline=False,
                )

        if counter % 5 != 0:
            current_embed.set_author(
                name=f"Топ лидеров сервера",
                icon_url=inter.guild.icon.url if inter.guild.icon else None,
            )
            current_embed.set_thumbnail(
                url=inter.guild.icon.url if inter.guild.icon else None
            )
            embeds.append(current_embed)

        view = paginator.Paginator(embeds)
        view.message = await inter.edit_original_message(embed=embeds[0], view=view)

    @leadersboard.sub_command(
        name="опыт",
        description="Показывает топ рейтинга участников по опыту.",
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def server_leadersboard_level(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)

        data = await self.db.get_data(
            inter.guild.id, all_data=True, filters="ORDER BY level DESC"
        )
        embeds = []
        counter = 0
        current_embed = disnake.Embed(
            description=f"👑 Список лидеров по опыту на сервере {inter.guild.name}!",
            color=self.color.MAIN,
        )

        for row in data:
            user = self.bot.get_user(row["member_id"])
            member = inter.guild.get_member(row["member_id"])
            if member is not None and not member.bot:
                if counter != 0 and counter % 5 == 0:
                    current_embed.set_author(
                        name=f"Топ лидеров сервера",
                        icon_url=inter.guild.icon.url if inter.guild.icon else None,
                    )
                    current_embed.set_thumbnail(
                        url=inter.guild.icon.url if inter.guild.icon else None
                    )
                    embeds.append(current_embed)
                    current_embed = disnake.Embed(
                        description=f"👑 Список лидеров по опыту на сервере {inter.guild.name}!",
                        color=self.color.MAIN,
                    )

                counter += 1
                current_embed.add_field(
                    name=f"#{counter} | `{self.bot.get_user(row['member_id'])}`",
                    value=f"**Уровень:** {row['level']} | **Опыт:** {row['xp']}/{500 + 100 * row['level']}",
                    inline=False,
                )

        if counter % 5 != 0:
            current_embed.set_author(
                name=f"Топ лидеров сервера",
                icon_url=inter.guild.icon.url if inter.guild.icon else None,
            )
            current_embed.set_thumbnail(
                url=inter.guild.icon.url if inter.guild.icon else None
            )
            embeds.append(current_embed)

        view = paginator.Paginator(embeds)
        view.message = await inter.edit_original_message(embed=embeds[0], view=view)

    @commands.slash_command(
        name="магазин", 
        description="Магазин, в котором можно покупать роли.", 
        dm_permission=False,
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def view_shop(self, inter):
        await inter.response.defer(ephemeral=False)
        counter = 0
        embed = disnake.Embed(
            description=f"Купить роль можно прописав команду </купитьроль:1046871804985213077> 💖", 
            color=self.color.MAIN
        )

        data = await self.db.get_shop_data(inter.guild.id, all_data=True)
        for row in data:
            if inter.guild.get_role(row["role_id"]) is not None:
                counter += 1
                embed.add_field(
                    name=f"`Товар #{counter}`",
                    value=f"**Роль:** {inter.guild.get_role(row['role_id']).mention}\n"
                    f"**Стоимость:** {row['cost']} {self.economy.CURRENCY_NAME}",
                    inline=False
                )
            else:
                embed.add_field(
                    name="Извините, но...",
                    value="магазин пуст.",
                    inline=False
                )

        embed.set_thumbnail(url=inter.guild.icon.url if inter.guild.icon else None)
        embed.set_author(
            name=f"Магазин ролей сервера {inter.guild.name}", 
            icon_url=inter.guild.icon.url if inter.guild.icon else None
        )
        embed.set_footer(text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR)
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name="слот",
        description="Игра в слот машину.",
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def slot(
        self,
        inter: disnake.ApplicationCommandInteraction,
        amount: int = commands.Param(
            name="сумма", description="Укажите сумму на которую собираетесь играть"
        ),
    ):
        data = await self.db.get_data(inter.author)
        if amount > data["balance"]:
            return await self.checks.check_unknown(
                inter, text=f"у вас недостаточно денег для игры!"
            )

        if amount < 10:
            return await self.checks.check_unknown(
                inter, text=f"укажите сумму больше **10 {self.economy.CURRENCY_NAME}**!"
            )

        if amount > 500:
            return await self.checks.check_unknown(
                inter,
                text=f"ставка не может превышать максимальную ставку в **500 {self.economy.CURRENCY_NAME}**!",
            )

        else:
            emojis = "🍎🍋🍉🍇"
            a = random.choice(emojis)
            b = random.choice(emojis)
            c = random.choice(emojis)
            d = random.choice(emojis)

            slotmachine = f"**⠀⠀  {a} {b} {c} {d}**"

            if a == b == c == d:
                await inter.response.defer(ephemeral=False)
                description = [
                    f"**Сумма, внесенная в слот составила: `{amount}` {self.economy.CURRENCY_NAME}**\n\n",
                    f"{inter.author.mention}, **потянул за рычаг и наблюдает перед собой следующую комбинацию:**\n\n",
                    f"┏━━━━━━━┓\n{slotmachine}\n┗━━━━━━━┛\n\n",
                    f"🥳 **Поздравляю! Вы сорвали джекпот и преумножили вашу ставку в `5` раз! (Ваш выигрыш составляет {amount * 5} {self.economy.CURRENCY_NAME})**",
                ]
                await self.db.update_member(
                    "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                    [
                        amount * 5,
                        inter.author.id,
                        inter.guild.id,
                    ],
                )
            elif (a == b == c) or (b == c == d) or (a == b == d) or (a == c == d):
                await inter.response.defer(ephemeral=False)
                description = [
                    f"**Сумма, внесенная в слот составила: `{amount}` {self.economy.CURRENCY_NAME}**\n\n",
                    f"{inter.author.mention}, **потянул за рычаг и наблюдает перед собой следующую комбинацию:**\n\n",
                    f"┏━━━━━━━┓\n{slotmachine}\n┗━━━━━━━┛\n\n",
                    f"🥳 **Поздравляю! Вы выиграли и преумножили вашу ставку в `2` раза! (Ваш выигрыш составляет {amount * 2} {self.economy.CURRENCY_NAME})**",
                ]
                await self.db.update_member(
                    "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                    [
                        amount * 2,
                        inter.author.id,
                        inter.guild.id,
                    ],
                )

            else:
                await inter.response.defer(ephemeral=False)
                description = [
                    f"**Сумма, внесенная в слот составила: `{amount}` {self.economy.CURRENCY_NAME}**\n\n",
                    f"{inter.author.mention}, **потянул за рычаг и наблюдает перед собой следующую комбинацию:**\n\n",
                    f"┏━━━━━━━┓\n{slotmachine}\n┗━━━━━━━┛\n\n",
                    f"😢 **Увы, но Вы проиграли, тем самым потеряв {amount} {self.economy.CURRENCY_NAME}!**",
                ]
                await self.db.update_member(
                    "UPDATE users SET balance = balance - ? WHERE member_id = ? AND guild_id = ?",
                    [
                        amount,
                        inter.author.id,
                        inter.guild.id,
                    ],
                )

            embed = disnake.Embed(description=f"".join(description), color=self.color.MAIN)
            embed.set_author(
                name="«Слот-машина»", icon_url=inter.author.display_avatar.url
            )
            embed.set_footer(
                text=self.main.FOOTER_TEXT, icon_url=self.main.FOOTER_AVATAR
            )
            await inter.edit_original_message(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))
