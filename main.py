import os
import disnake
from disnake.ext import commands

import config
from config import *
import random
from asyncio import sleep

bot = commands.Bot(command_prefix=PREFIX, intents=disnake.Intents.all(), case_insensitive=True)

@bot.event
async def on_ready():
    print("Бот подключен")
    print()
    print(" - Информация о боте - ")
    print("Имя бота: {0.user}".format(bot))
    print(f"ID бота: {bot.user.id}")

    while True:
        await bot.change_presence(status = disnake.Status.dnd, activity = disnake.Game(name = random.choice(gamesnames)))
        await sleep(60)
        await bot.change_presence(status = disnake.Status.dnd, activity = disnake.Streaming(name = random.choice(streamingnames), url = random.choice(streamingurl)))
        await sleep(300)
        await bot.change_presence(status = disnake.Status.dnd, activity = disnake.Activity(name = random.choice(watchingnames), type = disnake.ActivityType.watching))
        await sleep(60)
        await bot.change_presence(status = disnake.Status.dnd, activity = disnake.Activity(name = random.choice(listeningnames), type = disnake.ActivityType.listening))
        await sleep(60)


@bot.event
async def on_resumed():
    print("Бот снова подключен")

@bot.event
async def on_disconnect():
    print("Бот отключен. Перезагрузка...")

@bot.command()
@commands.is_owner()
async def load(ctx, extension):
	bot.load_extension(f"cogs.{extension}")

@bot.command()
@commands.is_owner()
async def reload(ctx, extension):
	bot.reload_extension(f"cogs.{extension}")

@bot.command()
@commands.is_owner()
async def unload(ctx, extension):
	bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
	if filename.endswith(".py"):
		bot.load_extension(f"cogs.{filename[:-3]}")


bot.run(config.TOKEN)