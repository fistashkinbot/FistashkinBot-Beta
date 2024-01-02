import disnake
import random
import datetime

from disnake.ext import commands
from utils import database, main, enums, constant, paginator, RankCard, Settings, checks
from PIL import ImageColor


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
        self.enum = enums.Enum()

    @commands.slash_command(
        name=disnake.Localized("balance", key="USER_BALANCE_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows the balance of the mentioned user or the user who called the command.",
            key="USER_BALANCE_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def user_balance(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            lambda inter: inter.author,
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        data = await self.db.get_data(member)
        balance = self.enum.format_large_number(data["balance"])
        level = self.enum.format_large_number(data["level"])
        xp = self.enum.format_large_number(data["xp"])
        total_xp = self.enum.format_large_number(data["total_xp"])
        xp_to_lvl = self.enum.format_large_number(500 + 100 * data["level"])

        if not member:
            member = inter.author

        elif member.bot:
            return await self.checks.check_unknown(
                inter, text=f"Ты не можешь взаимодействовать с ботами!"
            )

        else:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(
                description=f"[`💰`] **Баланс {member.mention} составляет:** `{balance}` {self.economy.CURRENCY_NAME}\n"
                f"[`🧸`] **Уровень:** `{level}` [**XP:** `{xp}/{xp_to_lvl}` | **Всего:** `{total_xp}`]",
                color=self.color.MAIN,
            )
            embed.set_author(
                name=f"💳 Отчётность о балансе", icon_url=member.display_avatar.url
            )
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("rank", key="USER_RANK_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows the rank of the mentioned user or the user who called the command.",
            key="USER_RANK_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def user_rank(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            lambda inter: inter.author,
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
    ):
        if not member:
            member = inter.author

        elif member.bot:
            return await self.checks.check_unknown(
                inter, text=f"Ты не можешь взаимодействовать с ботами!"
            )

        else:
            await inter.response.defer(ephemeral=False)
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
            await inter.edit_original_message(
                file=disnake.File(image, filename=f"rank_{user.name}.png")
            )

    @commands.slash_command(
        name=disnake.Localized("pay", key="PAY_COMMAND_NAME"),
        description=disnake.Localized(
            "Transfers money to the user.", key="PAY_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def pay_cash(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member = commands.Param(
            name=disnake.Localized("user", key="TARGET_USER_NAME"),
            description=disnake.Localized(
                "Select a user.", key="TARGET_USER_DESCRIPTION"
            ),
        ),
        amount: int = commands.Param(
            name=disnake.Localized("amount", key="PAY_AMOUNT_NAME"),
            description=disnake.Localized(
                "The amount you want to transfer to the user.",
                key="PAY_AMOUNT_DESCRIPTION",
            ),
        ),
    ):
        data = await self.db.get_data(inter.author)
        if amount is None:
            return await self.checks.check_amount_is_none(inter)

        elif member == inter.author:
            return await self.checks.check_user_author(
                inter, text=f"перевести **{self.economy.CURRENCY_NAME}**"
            )

        elif amount > data["balance"]:
            return await self.checks.check_unknown(
                inter,
                text=f"У вас недостаточно **{self.economy.CURRENCY_NAME}** для перевода!",
            )

        elif amount <= 0:
            return await self.checks.check_unknown(
                inter, text=f"Укажите сумму больше **0 {self.economy.CURRENCY_NAME}**!"
            )

        elif member.bot:
            return await self.checks.check_unknown(
                inter, text=f"Ты не можешь взаимодействовать с ботами!"
            )

        else:
            await inter.response.defer(ephemeral=False)
            await self.db.update_member(
                "UPDATE users SET balance = balance - ? WHERE member_id = ? AND guild_id = ?",
                [amount, inter.author.id, inter.guild.id],
            )
            pay_amount = self.enum.format_large_number(amount)
            comm_amount = self.enum.format_large_number(amount)
            commission = 0
            if amount > 100:
                commission = amount * (self.economy.COMMISSION / 100)
                amount -= commission
                comm_amount = self.enum.format_large_number(amount)

            description = [
                f"[`💱`] **Перевод успешно выполнен!**\n\n",
                # f"=======================================\n",
                f"[`📉`] **Отправитель:** {inter.author.mention}\n",
                f"[`🔴`] **Списано:** - `{pay_amount}` {self.economy.CURRENCY_NAME}\n",
                f"[`📈`] **Получатель:** {member.mention}\n",
                f"[`🟢`] **Получено:** + `{comm_amount}` {self.economy.CURRENCY_NAME}\n",
                f"=======================================\n",
                f"[`⚠️`] **Комиссия:** `{commission}` (**{self.economy.COMMISSION}%**)\n"
                f"[`📃`] **Итого переведено:** `{comm_amount}` {self.economy.CURRENCY_NAME}",
            ]
            embed = disnake.Embed(
                description=f"".join(description),
                color=self.color.MAIN,
            )
            embed.set_author(
                name="💳 Отчётность о банковской операции",
                icon_url=member.display_avatar.url,
            )
            await self.db.update_member(
                "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                [amount, member.id, inter.guild.id],
            )
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("leadersboard", key="LEADERBOARD_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows the top ranking of users for something.",
            key="LEADERBOARD_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    async def leadersboard(self, inter: disnake.ApplicationCommandInteraction):
        pass

    @leadersboard.sub_command(
        name=disnake.Localized("balance", key="LEADERBOARD_BALANCE_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows the top rating of users by balance.",
            key="LEADERBOARD_BALANCE_COMMAND_DESCRIPTION",
        ),
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def server_leadersboard_balance(
        self, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer(ephemeral=False)

        data = await self.db.get_data(
            inter.guild.id, all_data=True, filters="ORDER BY balance DESC"
        )
        embeds = []
        counter = 0
        current_embed = disnake.Embed(
            description=f"[`👑`] **Список лидеров по балансу на сервере **`{inter.guild.name}`**!**",
            color=self.color.MAIN,
        )

        for row in data:
            user = self.bot.get_user(row["member_id"])
            member = inter.guild.get_member(row["member_id"])
            if member is not None and not member.bot:
                if counter != 0 and counter % 5 == 0:
                    current_embed.set_author(
                        name=f"👑 Топ лидеров сервера",
                        icon_url=inter.guild.icon.url if inter.guild.icon else None,
                    )
                    current_embed.set_thumbnail(
                        url=inter.guild.icon.url if inter.guild.icon else None
                    )
                    embeds.append(current_embed)
                    current_embed = disnake.Embed(
                        description=f"[`👑`] **Список лидеров по балансу на сервере **`{inter.guild.name}`**!**",
                        color=self.color.MAIN,
                    )

                counter += 1
                balance = self.enum.format_large_number(row["balance"])
                current_embed.add_field(
                    name=f"#{counter} | `{self.bot.get_user(row['member_id'])}`",
                    value=f"**Баланс:** {balance} {self.economy.CURRENCY_NAME}",
                    inline=False,
                )

        if counter % 5 != 0:
            current_embed.set_author(
                name=f"👑 Топ лидеров сервера",
                icon_url=inter.guild.icon.url if inter.guild.icon else None,
            )
            current_embed.set_thumbnail(
                url=inter.guild.icon.url if inter.guild.icon else None
            )
            embeds.append(current_embed)

        view = paginator.Paginator(embeds)
        message = await inter.edit_original_message(embed=embeds[0], view=view)
        view.message = message

    @leadersboard.sub_command(
        name=disnake.Localized("rank", key="LEADERBOARD_RANK_COMMAND_NAME"),
        description=disnake.Localized(
            "Shows the top ranking of users by experience.",
            key="LEADERBOARD_RANK_COMMAND_DESCRIPTION",
        ),
    )
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def server_leadersboard_level(
        self, inter: disnake.ApplicationCommandInteraction
    ):
        await inter.response.defer(ephemeral=False)

        data = await self.db.get_data(
            inter.guild.id, all_data=True, filters="ORDER BY level DESC, xp DESC"
        )
        embeds = []
        counter = 0
        current_embed = disnake.Embed(
            description=f"[`👑`] **Список лидеров по опыту на сервере **`{inter.guild.name}`**!**",
            color=self.color.MAIN,
        )

        for row in data:
            user = self.bot.get_user(row["member_id"])
            member = inter.guild.get_member(row["member_id"])
            if member is not None and not member.bot:
                if counter != 0 and counter % 5 == 0:
                    current_embed.set_author(
                        name=f"👑 Топ лидеров сервера",
                        icon_url=inter.guild.icon.url if inter.guild.icon else None,
                    )
                    current_embed.set_thumbnail(
                        url=inter.guild.icon.url if inter.guild.icon else None
                    )
                    embeds.append(current_embed)
                    current_embed = disnake.Embed(
                        description=f"[`👑`] **Список лидеров по опыту на сервере **`{inter.guild.name}`**!**",
                        color=self.color.MAIN,
                    )

                counter += 1
                level = self.enum.format_large_number(row["level"])
                xp = self.enum.format_large_number(row["xp"])
                total_xp = self.enum.format_large_number(500 + 100 * row["level"])
                current_embed.add_field(
                    name=f"#{counter} | `{self.bot.get_user(row['member_id'])}`",
                    value=f"**Уровень:** {level} | **Опыт:** {xp}/{total_xp}",
                    inline=False,
                )

        if counter % 5 != 0:
            current_embed.set_author(
                name=f"👑 Топ лидеров сервера",
                icon_url=inter.guild.icon.url if inter.guild.icon else None,
            )
            current_embed.set_thumbnail(
                url=inter.guild.icon.url if inter.guild.icon else None
            )
            embeds.append(current_embed)

        view = paginator.Paginator(embeds)
        message = await inter.edit_original_message(embed=embeds[0], view=view)
        view.message = message

    @commands.slash_command(
        name=disnake.Localized("shop", key="SHOP_COMMAND_NAME"),
        description=disnake.Localized(
            "A store where you can buy roles.", key="SHOP_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def view_shop(self, inter):
        await inter.response.defer(ephemeral=False)

        data = await self.db.get_shop_data(inter.guild.id, all_data=True)
        role_buttons = []
        role_pages = []

        for i, row in enumerate(data):
            if i % 6 == 0:
                page = disnake.Embed(color=self.color.MAIN)
                page.set_thumbnail(
                    url=inter.guild.icon.url if inter.guild.icon else None
                )
                page.set_author(
                    name=f"Магазин ролей сервера {inter.guild.name}",
                    icon_url=inter.guild.icon.url if inter.guild.icon else None,
                )

            if inter.guild.get_role(row["role_id"]) is not None:
                counter = i + 1
                role_cost = self.enum.format_large_number(row["cost"])
                page.add_field(
                    name=f"`Товар #{counter}`",
                    value=f"**Роль:** {inter.guild.get_role(row['role_id']).mention}\n"
                    f"**Стоимость:** `{role_cost}` {self.economy.CURRENCY_NAME}",
                    inline=True,
                )

                # Создаем кнопку для каждой роли
                button_label = f"Товар #{str(counter)}"
                role_button = disnake.ui.Button(
                    style=disnake.ButtonStyle.blurple,
                    label=button_label,
                    custom_id=f"buy_role_{row['role_id']}",
                )
                role_buttons.append(role_button)

            if i % 6 == 5 or i == len(data) - 1:
                role_pages.append(page)

        if not role_pages:
            embed = disnake.Embed(
                description="😶‍🌫️ Извините, но... магазин пуст.", color=self.color.MAIN
            )
            embed.set_thumbnail(url=inter.guild.icon.url if inter.guild.icon else None)
            embed.set_author(
                name=f"Магазин ролей сервера {inter.guild.name}",
                icon_url=inter.guild.icon.url if inter.guild.icon else None,
            )
            await inter.edit_original_message(embed=embed)
            return

        view = paginator.Paginator(embeds=role_pages)
        # Добавляем кнопки к представлению
        for role_button in role_buttons:
            view.add_item(role_button)

        message = await inter.edit_original_message(embed=role_pages[0], view=view)
        view.message = message

    @commands.Cog.listener("on_button_click")
    async def shop_buttons_callback(self, inter: disnake.MessageInteraction):
        data = await self.db.get_shop_data(inter.guild.id, all_data=True)
        balance = await self.db.get_data(inter.author)
        if inter.component.custom_id.startswith("buy_role_"):
            role_id = int(inter.component.custom_id.split("_")[2])
            role = disnake.utils.get(inter.guild.roles, id=role_id)
            role_data = next(
                (item for item in data if item["role_id"] == role_id), None
            )

            if role_data:
                if balance["balance"] < role_data["cost"]:
                    embed = disnake.Embed(
                        title=f"{self.otheremojis.WARNING} Ошибка!",
                        description=f"❌ У вас недостаточно {self.economy.CURRENCY_NAME} для покупки роли!",
                        color=self.color.RED,
                    )
                    await inter.response.send_message(embed=embed, ephemeral=True)

                elif role in inter.author.roles:
                    embed = disnake.Embed(
                        description=f"❌ У вас имеется данная роль!",
                        color=self.color.RED,
                    )
                    await inter.response.send_message(embed=embed, ephemeral=True)

                elif balance["balance"] <= 0:
                    embed = disnake.Embed(
                        description=f"❌ Недостаточно {self.economy.CURRENCY_NAME}!",
                        color=self.color.RED,
                    )
                    await inter.response.send_message(embed=embed, ephemeral=True)

                else:
                    embed = disnake.Embed(
                        description=f"✅ Вы успешно купили роль {role.mention} за {role_data['cost']} {self.economy.CURRENCY_NAME}!",
                        color=self.color.MAIN,
                    )
                    embed.set_author(
                        name="Покупка роли", icon_url=inter.author.display_avatar.url
                    )
                    await self.db.update_member(
                        "UPDATE users SET balance = balance - ? WHERE member_id = ? AND guild_id = ?",
                        [role_data["cost"], inter.author.id, inter.guild.id],
                    )
                    await self.db.update_member(
                        "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                        [role_data["cost"], self.bot.user.id, inter.guild.id],
                    )
                    await inter.author.add_roles(role)
                    await inter.response.send_message(embed=embed)

            else:
                await inter.response.send_message("❌ Такой роли не существует.")

    @commands.slash_command(
        name=disnake.Localized("slot", key="SLOT_MACHINE_COMMAND_NAME"),
        description=disnake.Localized(
            "Slot machine game.", key="SLOT_MACHINE_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def slot(
        self,
        inter: disnake.ApplicationCommandInteraction,
        amount: int = commands.Param(
            name=disnake.Localized("amount", key="SLOT_MACHINE_COMMAND_TEXT_NAME"),
            description=disnake.Localized(
                "Specify the amount you are going to play for.",
                key="SLOT_MACHINE_COMMAND_TEXT_DESCRIPTION",
            ),
        ),
    ):
        data = await self.db.get_data(inter.author)
        slot_amount = self.enum.format_large_number(amount)
        if amount > data["balance"]:
            return await self.checks.check_unknown(
                inter, text=f"У вас недостаточно денег для игры!"
            )

        elif amount < 10:
            return await self.checks.check_unknown(
                inter, text=f"Укажите сумму больше 10 {self.economy.CURRENCY_NAME}!"
            )

        else:
            reels = self.otheremojis.REELS
            random.shuffle(reels)

            result = []
            for _ in range(3):
                symbol = random.choice(reels)
                result.append(symbol)
            random.shuffle(reels)
            ligne1 = []
            for _ in range(3):
                symbol = random.choice(reels)
                ligne1.append(symbol)
            ligne2 = []
            for _ in range(3):
                symbol = random.choice(reels)
                ligne2.append(symbol)

            slotmachine = [
                f"┏━━━━━━━━━━┓\n"
                f"**| `{ligne1[0]} | {ligne1[1]} | {ligne1[2]}` |**\n"
                f"**>**``{result[0]} | {result[1]} | {result[2]}``**<**\n"
                f"**| `{ligne2[0]} | {ligne2[1]} | {ligne2[2]}` |**\n"
                f"┗━━━━━━━━━━┛\n\n"
            ]
            final = "".join(slotmachine)

            if result[0] == result[1] == result[2]:
                await inter.response.defer(ephemeral=False)
                description = [
                    f"Сумма, внесенная в лот Вами составила: `{slot_amount}` {self.economy.CURRENCY_NAME}\n\n",
                    f"{inter.author.mention}, внеся определенную сумму и запустив «Слот-машину», Вы наблюдаете перед собой следующую выпавшую Вам комбинацию:\n\n",
                    f"{final}",
                    f"🥳 Поздравляю! Вы сорвали джекпот и преумножили вашу ставку в `5` раз! (Ваш выигрыш составляет `{slot_amount * 5}` {self.economy.CURRENCY_NAME})",
                ]
                await self.db.update_member(
                    "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                    [
                        amount * 5,
                        inter.author.id,
                        inter.guild.id,
                    ],
                )

            elif (
                (result[0] == result[1])
                or (result[1] == result[2])
                or (result[0] == result[2])
            ):
                await inter.response.defer(ephemeral=False)
                description = [
                    f"Сумма, внесенная в лот Вами составила: `{amount}` {self.economy.CURRENCY_NAME}\n\n",
                    f"{inter.author.mention}, внеся определенную сумму и запустив «Слот-машину», Вы наблюдаете перед собой следующую выпавшую Вам комбинацию:\n\n",
                    f"{final}",
                    f"🥳 Поздравляю! Вы выиграли и преумножили вашу ставку в `2` раза! (Ваш выигрыш составляет `{amount * 2}` {self.economy.CURRENCY_NAME})",
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
                    f"Сумма, внесенная в лот Вами составила: `{slot_amount}` {self.economy.CURRENCY_NAME}\n\n",
                    f"{inter.author.mention}, внеся определенную сумму и запустив «Слот-машину», Вы наблюдаете перед собой следующую выпавшую Вам комбинацию:\n\n",
                    f"{final}",
                    f"😢 Увы, но данная комбинация оказалась проигрышной! `{slot_amount}` {self.economy.CURRENCY_NAME} были списаны с личного счёта!",
                ]
                await self.db.update_member(
                    "UPDATE users SET balance = balance - ? WHERE member_id = ? AND guild_id = ?",
                    [
                        amount,
                        inter.author.id,
                        inter.guild.id,
                    ],
                )

            embed = disnake.Embed(
                description=f"".join(description), color=self.color.MAIN
            )
            embed.set_author(
                name="«Слот-машина»", icon_url=inter.author.display_avatar.url
            )
            await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("bonus", key="BONUS_COMMAND_NAME"),
        description=disnake.Localized(
            "Issues a bonus to the user.", key="BONUS_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def bonus(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer(ephemeral=False)
        random_amount = random.randint(10, 100)
        cooldown_time = datetime.datetime.now() + datetime.timedelta(seconds=int(43200))
        dynamic_time = disnake.utils.format_dt(cooldown_time, style="R")
        embed = disnake.Embed(
            description=f"[`🎉`] **Вы получили** `{random_amount*8}` {self.economy.CURRENCY_NAME}\n\n"
            f"[`🕘`] **В следующий раз бонус можно получить {dynamic_time}.**",
            color=self.color.MAIN,
        )
        embed.set_author(
            name="🧸 Бонус успешно активирован!",
            icon_url=inter.author.display_avatar.url,
        )
        await self.db.update_member(
            "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
            [random_amount * 8, inter.author.id, inter.guild.id],
        )
        await inter.edit_original_message(embed=embed)

    @commands.slash_command(
        name=disnake.Localized("coin", key="COIN_COMMAND_NAME"),
        description=disnake.Localized(
            "Cool game of heads or tails.", key="COIN_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def coin_game(
        self,
        inter: disnake.ApplicationCommandInteraction,
        amount: int = commands.Param(
            name=disnake.Localized("amount", key="COIN_COMMAND_TEXT_NAME"),
            description=disnake.Localized(
                "Specify the amount you are going to play for.",
                key="COIN_COMMAND_TEXT_DESCRIPTION",
            ),
        ),
    ):
        data = await self.db.get_data(inter.author)
        if amount > data["balance"]:
            return await self.checks.check_unknown(
                inter,
                text=f"У вас недостаточно {self.economy.CURRENCY_NAME} для игры в монетку! (Не хватает ещё {amount - data['balance']} {self.economy.CURRENCY_NAME})",
            )
        elif amount < 10:
            return await self.checks.check_unknown(
                inter, text=f"Укажите сумму больше 10 {self.economy.CURRENCY_NAME}!"
            )
        else:
            await inter.response.defer(ephemeral=False)
            coin_embed = disnake.Embed(
                description=f"Множитель: **{self.economy.MULTIPLIER}** \n Твоя задача выбрать одну из сторон монетки, если угадываешь - умножаешь свою ставку на множитель!",
                color=self.color.MAIN,
            )
            coin_embed.add_field(value=amount, name="Ставка")
            coin_embed.set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/272/272525.png"
            )
            coin_embed.set_author(
                name="Монетка", icon_url=inter.author.display_avatar.url
            )
            view = CoinButtons(self.bot)
            message = await inter.edit_original_message(embed=coin_embed, view=view)
            view.message = message

    @commands.slash_command(
        name=disnake.Localized("fight_club", key="FIGHT_CLUB_COMMAND_NAME"),
        description=disnake.Localized(
            "The first rule of Fight Club...", key="FIGHT_CLUB_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def fight_club_game(
        self,
        inter: disnake.ApplicationCommandInteraction,
        amount: int = commands.Param(
            name=disnake.Localized("amount", key="FIGHT_CLUB_COMMAND_TEXT_NAME"),
            description=disnake.Localized(
                "Specify the amount you are going to play for.",
                key="FIGHT_CLUB_COMMAND_TEXT_DESCRIPTION",
            ),
        ),
    ):
        data = await self.db.get_data(inter.author)
        if amount > data["balance"]:
            return await self.checks.check_unknown(
                inter,
                text=f"У вас недостаточно {self.economy.CURRENCY_NAME} для битвы бойцовского клуба! (Не хватает ещё {amount - data['balance']} {self.economy.CURRENCY_NAME})",
            )
        elif amount < 10:
            return await self.checks.check_unknown(
                inter, text=f"Укажите сумму больше 10 {self.economy.CURRENCY_NAME}!"
            )
        else:
            await inter.response.defer(ephemeral=False)
            fight_embed = disnake.Embed(
                description=f"*Первое правило бойцовского клуба - никому не рассказывай про бойцовский клуб...* \n "
                f"**Стоимость вступления в поединок - {amount} {self.economy.CURRENCY_NAME}. ** \n "
                f"Тебе дают возможность сделать удар первым, если ты хорошо реализуешь его, то получишь {amount * self.economy.MULTIPLIER} {self.economy.CURRENCY_NAME}, если противник защитится, соболезную тебе...",
                color=self.color.MAIN,
            )
            fight_embed.add_field(value=amount, name="Ставка")
            fight_embed.set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/6264/6264793.png"
            )
            fight_embed.set_author(
                name="Бойцовский клуб", icon_url=inter.author.display_avatar.url
            )
            view = FightButton(self.bot)
            message = await inter.edit_original_message(embed=fight_embed, view=view)
            view.message = message

    @commands.slash_command(
        name=disnake.Localized("case", key="CASE_COMMAND_NAME"),
        description=disnake.Localized(
            "Open cases with pleasant bonuses.", key="CASE_COMMAND_DESCRIPTION"
        ),
        dm_permission=False,
    )
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def open_case(self, inter: disnake.ApplicationCommandInteraction):
        data = await self.db.get_data(inter.author)
        if 500 > data["balance"]:
            return await self.checks.check_unknown(
                inter,
                text=f"У вас недостаточно **{self.economy.CURRENCY_NAME}** для открытия кейса! (Не хватает ещё {500 - data['balance']} {self.economy.CURRENCY_NAME})",
            )
        else:
            await inter.response.defer(ephemeral=False)
            case_embed = disnake.Embed(
                description=f'Для открытия кейса нажми на "Открыть кейс" \n **В кейсах большие шансы на выигрыш!**',
                color=self.color.MAIN,
            )
            case_embed.set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/10348/10348893.png"
            )
            case_embed.set_author(
                name="Кейсы", icon_url=inter.author.display_avatar.url
            )
            view = CaseButtons(self.bot)
            message = await inter.edit_original_message(embed=case_embed, view=view)
            view.message = message


class CoinButtons(disnake.ui.View):
    message: disnake.Message

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)
        self.db = database.DataBase()
        self.color = enums.Color()
        self.checks = checks.Checks(self.bot)
        super().__init__(timeout=120.0)

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=None)

    @disnake.ui.button(label="Орёл", emoji="🪙", style=disnake.ButtonStyle.primary)
    async def orel_button_callback(self, button: disnake.ui.Button, inter):
        if not inter.user == inter.author:
            return await inter.response.send_message(
                "❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                ephemeral=True,
            )
        data = await self.db.get_data(inter.author)
        await self.db.update_member(
            "UPDATE users SET balance = balance - ? WHERE member_id = ? AND guild_id = ?",
            [
                int(inter.message.embeds[0].fields[0].value),
                inter.author.id,
                inter.guild.id,
            ],
        )
        if bool(random.getrandbits(1)):
            await inter.response.defer(ephemeral=False)
            await self.db.update_member(
                "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                [
                    int(inter.message.embeds[0].fields[0].value)
                    * self.economy.MULTIPLIER,
                    inter.author.id,
                    inter.guild.id,
                ],
            )
            embed = disnake.Embed(
                title="Успех!",
                description=f"**Ты успешно выиграл {str(round(int(inter.message.embeds[0].fields[0].value) * self.economy.MULTIPLIER))} {self.economy.CURRENCY_NAME}!**",
                color=self.color.GREEN,
            )
            embed.set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/272/272525.png"
            )
            embed.set_author(name="Монетка", icon_url=inter.author.display_avatar.url)
            await inter.edit_original_message(embed=embed, view=None)
        else:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(
                title="Промах!",
                description=f"Ты проиграл **{inter.message.embeds[0].fields[0].value} {self.economy.CURRENCY_NAME}!**",
                color=self.color.RED,
            )
            embed.set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/272/272525.png"
            )
            embed.set_author(name="Монетка", icon_url=inter.author.display_avatar.url)
            await inter.edit_original_message(embed=embed, view=None)

    @disnake.ui.button(label="Решка", emoji="🪙", style=disnake.ButtonStyle.primary)
    async def reshka_button_callback(self, button: disnake.ui.Button, inter):
        if not inter.user == inter.author:
            return await inter.response.send_message(
                "❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                ephemeral=True,
            )
        data = await self.db.get_data(inter.author)
        await self.db.update_member(
            "UPDATE users SET balance = balance - ? WHERE member_id = ? AND guild_id = ?",
            [
                int(inter.message.embeds[0].fields[0].value),
                inter.author.id,
                inter.guild.id,
            ],
        )
        if bool(random.getrandbits(1)):
            await inter.response.defer(ephemeral=False)
            await self.db.update_member(
                "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
                [
                    int(inter.message.embeds[0].fields[0].value)
                    * self.economy.MULTIPLIER,
                    inter.author.id,
                    inter.guild.id,
                ],
            )
            embed = disnake.Embed(
                title="Успех!",
                description=f"**Ты успешно выиграл {str(round(int(inter.message.embeds[0].fields[0].value) * self.economy.MULTIPLIER))} {self.economy.CURRENCY_NAME}!**",
                color=self.color.GREEN,
            )
            embed.set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/272/272525.png"
            )
            embed.set_author(name="Монетка", icon_url=inter.author.display_avatar.url)
            await inter.edit_original_message(embed=embed, view=None)
        else:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(
                title="Промах!",
                description=f"Ты проиграл **{inter.message.embeds[0].fields[0].value} {self.economy.CURRENCY_NAME}!**",
                color=self.color.RED,
            )
            embed.set_thumbnail(
                url="https://cdn-icons-png.flaticon.com/512/272/272525.png"
            )
            embed.set_author(name="Монетка", icon_url=inter.author.display_avatar.url)
            await inter.edit_original_message(embed=embed, view=None)


class FightButton(disnake.ui.View):
    message: disnake.Message

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)
        super().__init__(timeout=120.0)

    async def on_timeout(self, inter):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=None)

    @disnake.ui.button(
        label="Удар в ноги",
        emoji="🦵",
        custom_id="legs_hit",
        style=disnake.ButtonStyle.primary,
    )
    async def legs_button_callback(self, button: disnake.ui.Button, inter):
        if not inter.user == inter.author:
            return await inter.response.send_message(
                "❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                ephemeral=True,
            )
        return await self.economy.hit(
            inter, "удар в ноги", amount=int(inter.message.embeds[0].fields[0].value)
        )

    @disnake.ui.button(
        label="Удар в живот",
        emoji="👊",
        custom_id="torso_hit",
        style=disnake.ButtonStyle.primary,
    )
    async def torso_button_callback(self, button: disnake.ui.Button, inter):
        if not inter.user == inter.author:
            return await inter.response.send_message(
                "❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                ephemeral=True,
            )
        return await self.economy.hit(
            inter, "удар в живот", amount=int(inter.message.embeds[0].fields[0].value)
        )

    @disnake.ui.button(
        label="Удар в голову",
        emoji="🤕",
        custom_id="head_hit",
        style=disnake.ButtonStyle.primary,
    )
    async def head_button_callback(self, button: disnake.ui.Button, inter):
        if not inter.user == inter.author:
            return await inter.response.send_message(
                "❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                ephemeral=True,
            )
        return await self.economy.hit(
            inter, "удар в голову", amount=int(inter.message.embeds[0].fields[0].value)
        )


class CaseButtons(disnake.ui.View):
    message: disnake.Message

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)
        self.db = database.DataBase()
        self.color = enums.Color()
        super().__init__(timeout=120.0)

    async def on_timeout(self, inter):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=None)

    @disnake.ui.button(
        label=f"Открыть кейс (500 FC)",
        emoji="🍪",
        custom_id="open_case",
        style=disnake.ButtonStyle.success,
    )
    async def open_case_button_callback(self, button: disnake.ui.Button, inter):
        if not inter.user == inter.author:
            return await inter.response.send_message(
                "❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                ephemeral=True,
            )
        await inter.response.defer(ephemeral=False)
        data = await self.db.get_data(inter.author)
        rnd_int = random.randint(100, 1500)
        await self.db.update_member(
            "UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?",
            [rnd_int * self.economy.MULTIPLIER, inter.author.id, inter.guild.id],
        )
        embed = disnake.Embed(
            title="Кейс успешно открыт!",
            description=f"**Ваш выигрыш составляет {rnd_int * self.economy.MULTIPLIER} {self.economy.CURRENCY_NAME}**",
            color=self.color.GREEN,
        )
        embed.set_thumbnail(
            url="https://cdn-icons-png.flaticon.com/512/10348/10348893.png"
        )
        embed.set_author(name="Кейсы", icon_url=inter.author.display_avatar.url)
        await inter.edit_original_message(embed=embed, view=None)


def setup(bot):
    bot.add_cog(Economy(bot))
