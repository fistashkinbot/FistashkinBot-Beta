import disnake

from disnake.ext import commands
from random import choice, randint, getrandbits
from utils import main, constant

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

class Casino(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.economy = main.EconomySystem(self.bot)

    @commands.Cog.listener("on_button_click")
    async def help_listener(self, inter):
        if inter.component.custom_id == "back":
            return await self.economy.casino_frame(inter, view=CasinoView(self.bot))

    @commands.slash_command(
        name="казино", 
        description="Место, где вы проведёте время с кайфом.", 
        dm_permission=True
    )
    async def casino_menu(self, inter: disnake.ApplicationCommandInteraction):
        return await self.economy.casino_frame(inter, view=CasinoView(self.bot))

def setup(bot):
    bot.add_cog(Casino(bot))