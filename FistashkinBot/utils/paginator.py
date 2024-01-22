import os
import disnake

from disnake.ext import commands
from typing import List
from utils import enums


class Paginator(disnake.ui.View):
    def __init__(self, inter: disnake.Interaction, embeds: List[disnake.Embed]):
        super().__init__(timeout=120.0)
        self.inter = inter
        self.embeds = embeds
        self.index = 0
        self.color = enums.Color()

        for i, embed in enumerate(self.embeds):
            embed.set_footer(text=f"Страница {i + 1} из {len(self.embeds)}")

        self._update_state()

    async def interaction_check(self, inter: disnake.Interaction):
        if inter.user.id != self.inter.author.id:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description=f"❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                    color=self.color.DARK_GRAY,
                ),
                ephemeral=True,
            )
        return True

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, disnake.ui.Button):
                child.disabled = True
        await self.message.edit(view=self)

    def _update_state(self) -> None:
        self.first_page.disabled = self.prev_page.disabled = self.index == 0
        self.last_page.disabled = self.next_page.disabled = (
            self.index == len(self.embeds) - 1
        )

    @disnake.ui.button(emoji="⏪", style=disnake.ButtonStyle.secondary)
    async def first_page(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.index = 0
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(emoji="◀", style=disnake.ButtonStyle.secondary)
    async def prev_page(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.index -= 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(emoji="▶", style=disnake.ButtonStyle.secondary)
    async def next_page(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.index += 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(emoji="⏩", style=disnake.ButtonStyle.secondary)
    async def last_page(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        self.index = len(self.embeds) - 1
        self._update_state()

        await inter.response.edit_message(embed=self.embeds[self.index], view=self)

    @disnake.ui.button(emoji="🗑️", style=disnake.ButtonStyle.red)
    async def remove(
        self, button: disnake.ui.Button, inter: disnake.MessageInteraction
    ):
        await inter.response.edit_message(view=None)
