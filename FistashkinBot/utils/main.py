import disnake
import random

from environs import Env
from .enums import Color
from disnake.ext import commands
from utils import database, main, constant, checks

class MainSettings:
	FOOTER_TEXT = "Riverya4life © 2023 All rights reserved 🐒"
	FOOTER_AVATAR = "https://github.com/riverya4life.png"
	DEVELOPER_ID = 668453200457760786
	BOT_ID = 991338113630752928
	BOT_VERSION = "v1.4a (<t:1687898840:d>)"
	BOT_EMOJI = "<:fistashkinbot:1145318360196845649>"

	GITHUB_AUTHOR = "https://github.com/riverya4life"
	DISCORD_BOT_SERVER = "https://discord.gg/H9XCZSReMj"
	BOT_SITE = "https://fistashkinbot.github.io/"
	BOT_INVITE = "https://discord.com/api/oauth2/authorize?client_id=991338113630752928&permissions=8&scope=bot%20applications.commands"
	GITHUB_REPOSITORY = "https://github.com/fistashkinbot/FistashkinBot-Beta"
	PATREON = "https://www.patreon.com/FistashkinBot"
	TELEGRAM = "https://t.me/riverya4lifeoff"

class MusicSettings:
	env = Env()
	env.read_env()

	HOST = "127.0.0.1"
	PORT = 7777
	PASSWORD = "N1KE02061992"
	SPOTIFY_CLIENT_ID = env.str("SPOTIFY_CLIENT_ID")
	SPOTIFY_CLIENT_SECRET = env.str("SPOTIFY_CLIENT_SECRET")

class EconomySystem(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.rp = constant.RolePlay()
		self.db = database.DataBase()
		self.otheremojis = constant.OtherEmojis()
		self.checks = checks.Checks(self.bot)

	MULTIPLIER = 2.0
	CURRENCY_NAME = "FC <a:fbDP:1070681790429270046>"
	CURRENCY_EMOJI = "<a:fbDP:1070681790429270046>"

	async def casino_frame(self, inter, view):
		await inter.response.defer(ephemeral=False)
		casino_embed = disnake.Embed(
			description = "*Выбери игру в которую хочешь сыграть*\n**На выбор у тебя есть:**\n"
			f"* Монетка\n* Кейсы\n* Бойцовский клуб", 
			color = Color.MAIN,
		)
		casino_embed.set_thumbnail(url = "https://cdn-icons-png.flaticon.com/512/1055/1055814.png")
		casino_embed.set_author(
            name="Казино", 
            icon_url=inter.author.display_avatar.url
        )
		message = await inter.edit_original_message(embed=casino_embed, view=view)
		view.message = message

	async def coin_frame(self, inter, view):
		await inter.response.defer(ephemeral=False)
		coin_embed = disnake.Embed(
	    	description=f"Множитель: **{self.MULTIPLIER}** \n Твоя задача выбрать одну из сторон монетки, если угадываешь - умножаешь свою ставку на множитель", 
	    	color=Color.MAIN,
	    )
		coin_embed.add_field(value=str(15), name="Ставка")
		coin_embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/272/272525.png")
		coin_embed.set_author(
            name="Монетка", 
            icon_url=inter.author.display_avatar.url
        )
		message = await inter.edit_original_message(embed=coin_embed, view=view)
		view.message = message

	async def case_frame(self, inter, view):
		await inter.response.defer(ephemeral=False)
		case_embed = disnake.Embed(
	    	description=f"Для открытия кейса нажми на \"Открыть кейс\" \n **В кейсах большие шансы на выигрыш!**", 
	    	color=Color.MAIN,
	    )
		case_embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/10348/10348893.png")
		case_embed.set_author(
            name="Кейсы", 
            icon_url=inter.author.display_avatar.url
        )
		message = await inter.edit_original_message(embed=case_embed, view=view)
		view.message = message

	async def fight_club_frame(self, inter, view):
		await inter.response.defer(ephemeral=False)
		fight_embed = disnake.Embed(
	    	description=f"*Первое правило бойцовского клуба - никому не рассказывай про бойцовский клуб...* \n "
	    	f"**Стоимость вступления в поединок - 10 {self.CURRENCY_NAME}. ** \n "
	    	f"Тебе дают возможность сделать удар первым, если ты хорошо реализуешь его, то получишь 15 {self.CURRENCY_NAME}, если противник защитится, соболезную тебе...", 
	    	color=Color.MAIN,
		)
		fight_embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/6264/6264793.png")
		fight_embed.set_author(
            name="Бойцовский клуб", 
            icon_url=inter.author.display_avatar.url
        )
		message = await inter.edit_original_message(embed=fight_embed, view=view)
		view.message = message

	async def hit(self, inter, body_part, view):
		await inter.response.defer(ephemeral=False)
		data = await self.db.get_data(inter.author)
		if (
			10 > data["balance"]
		):
			return await self.checks.check_unknown(
            	inter, 
            	text=f" у вас недостаточно **{self.CURRENCY_NAME}** для игры!",
            )
		else:
			await self.db.update_member(
				"UPDATE users SET balance = balance - ? WHERE member_id = ? AND guild_id = ?", 
				[
					10, 
					inter.author.id, 
					inter.guild.id
				],
			)
			if not random.choice(
				range(0, 4)
			):
				await self.db.update_member(
					"UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?", 
					[
						15, 
						inter.author.id, 
						inter.guild.id
					],
				)
				embed = disnake.Embed(
					description=f"**Ты сделал {body_part} и отправил своего соперника в нокаут! Так держать, твой ты получаешь 15 {self.CURRENCY_NAME} на свой баланс!**",
					color=Color.GREEN,
				)
				embed.set_image(url=random.choice(self.rp.FIGHT_CLUB_VICTORY_IMAGES))
				embed.set_author(
		            name="Бойцовский клуб", 
		            icon_url=inter.author.display_avatar.url
		        )
				message = await inter.edit_original_message(embed=embed, view=view)
				view.message = message
			else:
				embed = disnake.Embed(
					description=f"Ты сделал **{body_part}**, но противник защитился и сделал удар. Ты остался без 5 зубов и **10 {self.CURRENCY_NAME}**.",
					color=Color.RED,
				)
				embed.set_image(url=random.choice(self.rp.FIGHT_CLUB_DEFEAT_IMAGES))
				embed.set_author(
		            name="Бойцовский клуб", 
		            icon_url=inter.author.display_avatar.url
		        )
				message = await inter.edit_original_message(embed=embed, view=view)
				view.message = message

	async def coin_button_callback(self, inter, view):
		await inter.response.defer(ephemeral=False)
		data = await self.db.get_data(inter.author)
		if (
			int(inter.message.embeds[0].fields[0].value) > data["balance"]
		):
			return await self.checks.check_unknown(
				inter, 
				text=f" у вас недостаточно **{self.CURRENCY_NAME}** для игры в монетку!",
            )
		else:
			await self.db.update_member(
				"UPDATE users SET balance = balance - ? WHERE member_id = ? AND guild_id = ?", 
				[
					int(inter.message.embeds[0].fields[0].value), 
					inter.author.id, 
					inter.guild.id
				],
			)
			if bool(
				random.getrandbits(1)
			):
				await self.db.update_member(
					"UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?", 
					[
						int(inter.message.embeds[0].fields[0].value), 
						inter.author.id, 
						inter.guild.id
					],
				)
				embed = disnake.Embed(
					title="Успех!",
					description=f"**Ты успешно выиграл {str(round(int(inter.message.embeds[0].fields[0].value) * self.MULTIPLIER, 1))} {self.CURRENCY_NAME}!**",
					color=Color.GREEN,
				)
				embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/272/272525.png")
				embed.set_author(
		            name="Монетка", 
		            icon_url=inter.author.display_avatar.url
		        )
				message = await inter.edit_original_message(embed=embed, view=view)
				view.message = message
			else:
				embed = disnake.Embed(
					title="Промах!",
					description=f"Ты проиграл **{inter.message.embeds[0].fields[0].value} {self.CURRENCY_NAME}!**",
					color=Color.RED,
				)
				embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/272/272525.png")
				embed.set_author(
		            name="Монетка", 
		            icon_url=inter.author.display_avatar.url
		        )
				message = await inter.edit_original_message(embed=embed, view=view)
				view.message = message

	async def open_case_callback(self, inter, view):
		await inter.response.defer(ephemeral=False)
		data = await self.db.get_data(inter.author)
		if (
			10 > data["balance"]
		):
			return await self.checks.check_unknown(
				inter, 
				text=f" у вас недостаточно **{self.CURRENCY_NAME}** для открытия кейса!",
            )
		else:
			rnd_int = random.randint(0, 50)
			await self.db.update_member(
				"UPDATE users SET balance = balance + ? WHERE member_id = ? AND guild_id = ?", 
				[
					rnd_int, 
					inter.author.id, 
					inter.guild.id
				],
			)
			embed = disnake.Embed(
				title="Кейс успешно открыт!", 
				description=f"**Ваш выигрыш составляет {rnd_int} {self.CURRENCY_NAME}**",
				color=Color.GREEN,
			)
			embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/10348/10348893.png")
			embed.set_author(
	            name="Кейс успешно открыт!", 
	            icon_url=inter.author.display_avatar.url
	        )
			message = await inter.edit_original_message(embed=embed, view=view)
			view.message = message