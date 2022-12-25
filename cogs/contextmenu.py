import disnake
from disnake.ext import commands

from config import *


class ContextMenu(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.user_command(name = 'Аватар', description = 'Показывает аватар упомянутого участника или участника, вызвавшего команду.')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, inter, member: disnake.Member = None):
        if member == None:#если не упоминать участника тогда выводит аватар автора сообщения
            member = inter.author
        embed = disnake.Embed(
            title = f"Аватар участника - {member.name}", 
            description = f"[Нажмите что бы скачать аватар]({member.display_avatar.url})", 
            color = botmaincolor, 
            timestamp=inter.created_at
        )
        embed.set_image(url = member.display_avatar.url)
        embed.set_footer(text=f'{footerbyriverya4life}', icon_url=inter.author.display_avatar.url)
        embed.set_author(name=f'{inter.author.name}', icon_url=inter.author.display_avatar.url)

        await inter.send(embed = embed, ephemeral=True)


    @commands.user_command(name = 'Юзер', description = 'Показывает информацию об участнике.')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def userinfo(self, inter, member: disnake.Member = None):
        if member == None:
            t = inter.author.status
            if t == disnake.Status.online:
                d = f"<:online:1044637024080105482>В сети"
            t = inter.author.status
            if t == disnake.Status.offline:
                d = f"<:offline:1044637025808154654>Не в сети"
            t = inter.author.status
            if t == disnake.Status.idle:
                d = f"<:idle:1044637022490472508>Не активен"
            t = inter.author.status
            if t == disnake.Status.dnd:
                d = f"<:dnd:1044637020951154759>Не беспокоить"
            t = inter.author.status
            if t == disnake.Status.streaming:
                d = f"<:dnd:1044637020951154759>Стримит"

            badgelist = ""

            if inter.author.public_flags.hypesquad_brilliance: #хайпсквад бриллианс
                badgelist += f"<:hypesquadbrilliance:1044757284074565713>"
            elif inter.author.public_flags.hypesquad_bravery: #хайпсквад бравери
                badgelist += f"<:hypesquadbravery:1044757282401038346>"
            elif inter.author.public_flags.hypesquad_balance: #хайпсквад баланс
                badgelist += f"<:hypesquadbalance:1044757278915563600>"
            elif inter.author.public_flags.hypesquad: #золотой хайпсквад
                badgelist += f"<:hypesquadevents:1045664339933274132>"
            elif inter.author.public_flags.early_supporter: #ранее поддержавший
                badgelist += f"<:earlysupporter:1045664335587979326>"
            elif inter.author.public_flags.bug_hunter: #баг хантер
                badgelist += f"<:bughunterlevel1:1045664324842164314>"
            elif inter.author.public_flags.bug_hunter_level_2: #баг хантер 2 уровня
                badgelist += f"<:bughunterlevel2:1045664326536667138>"
            elif inter.author.public_flags.verified_bot_developer: #разработчик верифицированного бота
                badgelist += f"<:earlyverifiedbotdev:1045664337278271539>"
            elif inter.author.public_flags.early_verified_bot_developer: #early разработчик верифицированного бота
                badgelist += f"<:earlyverifiedbotdev:1045664337278271539>"
            elif inter.author.public_flags.partner: #партнёр
                badgelist += f"<:discordpartner:1045664332039598080>"
            elif inter.author.public_flags.staff: #помощник типо
                badgelist += f"<:discordstaff:1045664333901869096>"
            elif inter.author.public_flags.discord_certified_moderator: #модератор дискорда
                badgelist += f"<:certifiedmod:1045664328319254528>"
            else:
                badgelist += f"`❌ Отсутствуют`"

            emb = disnake.Embed(
                title=f"Информация о пользователе {inter.author.display_name}", 
                description=f"**Основная информация**\n🐱‍👤 **Имя пользователя:** {inter.author} ({inter.author.display_name})\n🏋️ **Активность:** {d}\n🎩 **Роль на сервере:** {inter.author.top_role.mention}\n🏆 **Значки:** {badgelist}\n\n📆 **Присоединился:** <t:{round(inter.author.joined_at.timestamp())}:D> (<t:{round(inter.author.joined_at.timestamp())}:R>)\n📆 **Дата регистрации:** <t:{round(inter.author.created_at.timestamp())}:D> (<t:{round(inter.author.created_at.timestamp())}:R>)", 
                color=inter.author.color, 
                timestamp=inter.created_at
            )
            emb.set_thumbnail(url=inter.author.display_avatar.url)
            emb.set_footer(text = f'ID: {inter.author.id}', icon_url = inter.author.display_avatar.url)
            emb.set_author(name=f'{inter.author.name}', icon_url=inter.author.display_avatar.url)
            await inter.send(embed = emb, ephemeral=True)
        elif member == self.bot.user:
            emb = disnake.Embed(
                title = f'👾 Информация о боте {self.bot.user.name}', 
                description = f'👋 Привет! Меня зовут Фисташкин! Я небольшой бот с небольшими командами <:earlysupporter:1045664335587979326>\n\nМой префикс `{PREFIX}`, но так же есть поддержка слэш команд <:supportscommands:1045664343209021490>\nДетальная информация о моих возможностях по команде `.хелп` или `/хелп`.', 
                colour = botmaincolor, 
                timestamp=inter.created_at
            )
            emb.set_author(name = self.bot.user.name, icon_url = self.bot.user.display_avatar.url)
            emb.add_field(name = '👾 Сборка:', value = f'{riverya4lifebotversion}', inline=True)
            emb.add_field(name = '🔮 Мой разработчик:', value = f'<:riverya4life:1044666044599504906> Riverya4life#9515', inline=True)
            emb.add_field(name = '🎊 Дата создания:', value = f'<t:{round(self.bot.user.created_at.timestamp())}:D> (<t:{round(self.bot.user.created_at.timestamp())}:R>)', inline=False)
            emb.add_field(name = '🎃 Полезные ссылки', value = f'[💖 Github](https://github.com/riverya4life) | [🎥 YouTube](https://www.youtube.com/@riverya4lifehomie) | [📱 TikTok](https://www.tiktok.com/@riverya4life)', inline=False)
            emb.set_thumbnail(url = self.bot.user.display_avatar.url)
            emb.set_footer(text = f'{footerbyriverya4life}', icon_url =avatarbyfooterbyriverya4life)
            await inter.send(embed=emb, ephemeral=True)
        else:
            t = member.status
            if t == disnake.Status.online:
                d = f"<:online:1044637024080105482>В сети"
            t = member.status
            if t == disnake.Status.offline:
                d = f"<:offline:1044637025808154654>Не в сети"
            t = member.status
            if t == disnake.Status.idle:
                d = f"<:idle:1044637022490472508>Не активен"
            t = member.status
            if t == disnake.Status.dnd:
                d = f"<:dnd:1044637020951154759>Не беспокоить"
            t = member.status
            if t == disnake.Status.streaming:
                d = f"<:dnd:1044637020951154759>Стримит"

            badgelist = ""

            if member.public_flags.hypesquad_brilliance: #хайпсквад бриллианс
                badgelist += f"<:hypesquadbrilliance:1044757284074565713>"
            elif member.public_flags.hypesquad_bravery: #хайпсквад бравери
                badgelist += f"<:hypesquadbravery:1044757282401038346>"
            elif member.public_flags.hypesquad_balance: #хайпсквад баланс
                badgelist += f"<:hypesquadbalance:1044757278915563600>"
            elif member.public_flags.hypesquad: #золотой хайпсквад
                badgelist += f"<:hypesquadevents:1045664339933274132>"
            elif member.public_flags.early_supporter: #ранее поддержавший
                badgelist += f"<:earlysupporter:1045664335587979326>"
            elif member.public_flags.bug_hunter: #баг хантер
                badgelist += f"<:bughunterlevel1:1045664324842164314>"
            elif member.public_flags.bug_hunter_level_2: #баг хантер 2 уровня
                badgelist += f"<:bughunterlevel2:1045664326536667138>"
            elif member.public_flags.verified_bot_developer: #разработчик верифицированного бота
                badgelist += f"<:earlyverifiedbotdev:1045664337278271539>"
            elif member.public_flags.early_verified_bot_developer: #early разработчик верифицированного бота
                badgelist += f"<:earlyverifiedbotdev:1045664337278271539>"
            elif member.public_flags.partner: #партнёр
                badgelist += f"<:discordpartner:1045664332039598080>"
            elif member.public_flags.staff: #помощник типо
                badgelist += f"<:discordstaff:1045664333901869096>"
            elif member.public_flags.discord_certified_moderator: #модератор дискорда
                badgelist += f"<:certifiedmod:1045664328319254528>"
            else:
                badgelist += f"`❌ Отсутствуют`"

            emb = disnake.Embed(
                title=f"Информация о пользователе {member.display_name}", 
                description=f"**Основная информация**\n🐱‍👤 **Имя пользователя:** {member} ({member.display_name})\n🏋️ **Активность:** {d}\n🎩 **Роль на сервере:** {member.top_role.mention}\n🏆 **Значки:** {badgelist}\n\n📆 **Присоединился:** <t:{round(member.joined_at.timestamp())}:D> (<t:{round(member.joined_at.timestamp())}:R>)\n📆 **Дата регистрации:** <t:{round(member.created_at.timestamp())}:D> (<t:{round(member.created_at.timestamp())}:R>)", 
                color=member.color, 
                timestamp=inter.created_at
            )
            emb.set_thumbnail(url=member.display_avatar.url)
            emb.set_footer(text = f'ID: {member.id}', icon_url = member.display_avatar.url)
            emb.set_author(name=f'{inter.author.name}', icon_url=inter.author.display_avatar.url)
            await inter.send(embed = emb, ephemeral=True)


def setup(bot):
    bot.add_cog(ContextMenu(bot))