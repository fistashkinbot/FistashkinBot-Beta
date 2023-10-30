import disnake
import datetime
import random

from disnake.ext import commands
from utils import main, enums, constant, roleplay

class Checks(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.main = main.MainSettings()
		self.color = enums.Color()
		self.otheremojis = constant.OtherEmojis()
		self.rp = roleplay.RolePlay()

	async def check_user_bot(self, inter, text):
		await inter.response.defer(ephemeral=True)
		embed = disnake.Embed(
			title=f"{self.otheremojis.WARNING} Ошибка!",
			description=f"**{inter.author.mention}, ты не можешь {text} {self.bot.user.mention}!**",
			color=self.color.RED,
		)
		await inter.edit_original_message(embed=embed)

	async def check_user_author(self, inter, text):
		await inter.response.defer(ephemeral=True)
		embed = disnake.Embed(
			title=f"{self.otheremojis.WARNING} Ошибка!",
			description=f"**{inter.author.mention}, ты не можешь {text} самому себе!**",
			color=self.color.RED,
		)
		await inter.edit_original_message(embed=embed)

	async def check_user_role(self, inter):
		await inter.response.defer(ephemeral=True)
		embed = disnake.Embed(
			title=f"{self.otheremojis.WARNING} Ошибка!",
			description=f"{inter.author.mention}, ты не можешь использовать данную команду на участников с более высокой ролью!",
			colour=self.color.RED,
		)
		await inter.edit_original_message(embed=embed)

	async def check_bot_role(self, inter):
		await inter.response.defer(ephemeral=True)
		embed = disnake.Embed(
			title=f"{self.otheremojis.WARNING} Ошибка!",
			description=f"{inter.author.mention}, роль этого бота недостаточно высока, чтобы использовать данную команду!",
			colour=self.color.RED,
		)
		await inter.edit_original_message(embed=embed)

	async def check_member_timeout(self, inter, member):
		if member.current_timeout:
			await inter.response.defer(ephemeral=True)
			embed = disnake.Embed(
				title=f"{self.otheremojis.WARNING} Ошибка!",
				description=f"{inter.author.mention}, участник уже находится в тайм-ауте!",
				colour=self.color.RED,
			)
			await inter.edit_original_message(embed=embed)

		if member.current_timeout == None:
			await inter.response.defer(ephemeral=True)
			embed = disnake.Embed(
				title=f"{self.otheremojis.WARNING} Ошибка!",
				description=f"{inter.author.mention}, участник не находится в тайм-ауте!",
				colour=self.color.RED,
			)
			await inter.edit_original_message(embed=embed)

	async def check_timeout_time(self, inter):
		await inter.response.defer(ephemeral=True)
		embed = disnake.Embed(
			title=f"{self.otheremojis.WARNING} Ошибка!",
			description=f"{inter.author.mention}, ты не можешь замутить участника больше чем **28 дней**!",
			color=self.color.RED,
		)
		await inter.edit_original_message(embed=embed)

	async def check_time_muted(self, inter, member, time, reason):
		await inter.response.defer(ephemeral=False)
		d = time[-1:]
		timemute = int(time[:-1])

		if d == "s" or d == "с":
			dynamic_durations = datetime.datetime.now() + datetime.timedelta(
				seconds=int(timemute)
			)

		if d == "m" or d == "м":
			dynamic_durations = datetime.datetime.now() + datetime.timedelta(
				minutes=int(timemute)
			)

		if d == "h" or d == "ч":
			dynamic_durations = datetime.datetime.now() + datetime.timedelta(
				hours=int(timemute)
			)

		if d == "d" or d == "д":
			dynamic_durations = datetime.datetime.now() + datetime.timedelta(
				days=int(timemute)
			)

		dynamic_time = disnake.utils.format_dt(dynamic_durations, style="R")

		embed = disnake.Embed(
			title="🤐 Заглушка чата",
			description=f"**Пользователь:** {member.mention}\n"
			f"**Модератор:** {inter.author.mention}\n"
			f"**Снятие наказания:** {dynamic_time}\n"
			f"**Причина:** `{reason}`\n",
			color=self.color.MAIN,
			timestamp=inter.created_at,
		)
		embed.set_thumbnail(url=member.display_avatar.url)
		embed.set_footer(
			text="Команда по безопасности Discord сервера",
			icon_url=inter.guild.icon.url if inter.guild.icon else None,
		)

		dm_embed = disnake.Embed(
			description=f"**Модератор:** {inter.author.mention} `[ID: {inter.author.id}]`\n"
			f"**Снятие наказания:** {dynamic_time}\n"
			f"**Причина:** {reason}\n"
			f"**Сервер:** {inter.guild.name}",
			color=self.color.MAIN,
			timestamp=inter.created_at,
		)
		dm_embed.set_author(
			name=f"{member.name}, Вам была выдана заглушка чата",
			icon_url=member.display_avatar.url,
		)
		dm_embed.set_footer(
			text="Команда по безопасности Discord сервера",
			icon_url=inter.guild.icon.url if inter.guild.icon else None,
		)

		await member.timeout(until=dynamic_durations, reason=reason)
		await member.send(
			embed=dm_embed,
			components=[
				disnake.ui.Button(
					label=f"Отправлено с {inter.guild.name}",
					emoji="📨",
					style=disnake.ButtonStyle.gray,
					disabled=True,
				)
			],
		)
		await inter.edit_original_message(embed=embed)

	async def send_embed_punishment(self, inter, member, reason, punish, set_author_punish):
		await inter.response.defer(ephemeral=False)
		embed = disnake.Embed(
			title=punish,
			description=f"**Пользователь:** {member.mention}\n"
			f"**Модератор:** {inter.author.mention}\n"
			f"**Причина:** `{reason}`\n",
			color=self.color.MAIN,
			timestamp=inter.created_at,
		)
		embed.set_thumbnail(url=member.display_avatar.url)
		embed.set_footer(
			text="Команда по безопасности Discord сервера",
			icon_url=inter.guild.icon.url if inter.guild.icon else None,
		)

		dm_embed = disnake.Embed(
			description=f"**Модератор:** {inter.author.mention} `[ID: {inter.author.id}]`\n"
			f"**Причина:** {reason}\n"
			f"**Сервер:** {inter.guild.name}",
			color=self.color.MAIN,
			timestamp=inter.created_at,
		)
		dm_embed.set_author(
			name=f"{member.name}, {set_author_punish}",
			icon_url=member.display_avatar.url,
		)
		dm_embed.set_footer(
			text="Команда по безопасности Discord сервера",
			icon_url=inter.guild.icon.url if inter.guild.icon else None,
		)

		await member.send(
			embed=dm_embed,
			components=[
				disnake.ui.Button(
					label=f"Отправлено с {inter.guild.name}",
					emoji="📨",
					style=disnake.ButtonStyle.gray,
					disabled=True,
				)
			],
		)
		if (
			punish == "🕯 Блокировка"
		):
			await inter.guild.ban(user=member, reason=reason)
		elif (
			punish == "💨 Кик"
		):
			await inter.guild.kick(user=member, reason=reason)
		elif (
			punish == "🥳 С участника была снята заглушка чата"
		):
			await member.timeout(until=None, reason=reason)

		await inter.edit_original_message(embed=embed)

	async def check_amount_is_none(self, inter):
		await inter.response.defer(ephemeral=True)
		embed = disnake.Embed(
			title=f"{self.otheremojis.WARNING} Ошибка!",
			description=f"{inter.author.mention}, укажите сумму **{self.economy.CURRENCY_NAME}**, которую желаете начислить на счет участника!",
			color=self.color.RED,
		)
		await inter.edit_original_message(embed=embed)

	async def check_unknown(self, inter, text):
		await inter.response.defer(ephemeral=True)
		embed = disnake.Embed(
			title=f"{self.otheremojis.WARNING} Ошибка!",
			description=f"{inter.author.mention}, {text}",
			color=self.color.RED,
		)
		await inter.edit_original_message(embed=embed)

	async def check_interaction_rp(self, inter, text):
		await inter.response.defer(ephemeral=True)
		embed = disnake.Embed(
			description=f"😥 {inter.author.mention}, ты не можешь сам себя {text}!"
		)
		embed.set_image(url=random.choice(self.rp.SAD_ERROR_IMAGES))
		await inter.edit_original_message(embed=embed)