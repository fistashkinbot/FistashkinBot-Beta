import disnake
import datetime

from disnake.ext import commands
from utils import database, enums


class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = database.DataBase()
        self.color = enums.Color()

    @commands.Cog.listener(disnake.Event.member_join)
    async def on_member_join(self, member):
        log_channel = await self.db.get_log_channel(member.guild.id)
        if log_channel is not None:
            channel_id = log_channel["log_channel_id"]
            channel = disnake.utils.get(member.guild.channels, id=channel_id)
            if channel:
                registerf = disnake.utils.format_dt(member.created_at, style="f")
                registerr = disnake.utils.format_dt(member.created_at, style="R")
                embed = disnake.Embed(
                    description=f"{'Бот' if member.bot else 'Участник'} **{member}** ({member.mention}) присоединился к серверу",
                    color=self.color.MAIN,
                    timestamp=datetime.datetime.fromtimestamp(
                        datetime.datetime.now().timestamp()
                    ),
                )
                embed.add_field(
                    name="Дата регистрации",
                    value=f"{registerf} ({registerr})",
                    inline=True,
                )
                embed.set_footer(
                    text=f"ID {'бота' if member.bot else 'участника'}: {member.id}"
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=embed)

    @commands.Cog.listener(disnake.Event.member_remove)
    async def on_member_remove(self, member):
        log_channel = await self.db.get_log_channel(member.guild.id)
        if log_channel is not None:
            channel_id = log_channel["log_channel_id"]
            channel = disnake.utils.get(member.guild.channels, id=channel_id)
            if channel:
                roles = int(len(member.roles) - 1)
                role_list = [r.mention for r in member.roles][1:]
                role_list.reverse()
                role_string = " | ".join(role_list)
                embed = disnake.Embed(
                    description=f"{'Бот' if member.bot else 'Участник'} **{member}** ({member.mention}) покинул сервер",
                    color=self.color.MAIN,
                    timestamp=datetime.datetime.fromtimestamp(
                        datetime.datetime.now().timestamp()
                    ),
                )
                if not member.top_role == member.guild.default_role:
                    embed.add_field(
                        name=f"{'Роли' if roles > 1 else 'Роль'} при выходе",
                        value=role_string,
                        inline=False,
                    )
                embed.set_footer(
                    text=f"ID {'бота' if member.bot else 'участника'}: {member.id}"
                )
                embed.set_thumbnail(url=member.display_avatar.url)
                await channel.send(embed=embed)

    @commands.Cog.listener(disnake.Event.message_delete)
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        else:
            log_channel = await self.db.get_log_channel(message.guild.id)
            if log_channel is not None:
                channel_id = log_channel["log_channel_id"]
                channel = disnake.utils.get(message.guild.channels, id=channel_id)
                if channel:
                    embed = disnake.Embed(
                        description=f"Сообщение было удалено",
                        color=self.color.MAIN,
                        timestamp=datetime.datetime.fromtimestamp(
                            datetime.datetime.now().timestamp()
                        ),
                    )
                    embed.add_field(
                        name="Сообщение", value=f"```{message.content}```", inline=False
                    )
                    embed.add_field(
                        name="Автор",
                        value=f"**{message.author.name}** ({message.author.mention})",
                        inline=True,
                    )
                    embed.add_field(
                        name="Канал",
                        value=f"**{message.channel.name}** ({message.channel.mention})",
                        inline=True,
                    )
                    embed.set_footer(text=f"ID сообщения: {message.id}")
                    embed.set_thumbnail(url=message.author.display_avatar.url)

                    if message.attachments:
                        embed.add_field(
                            name="Изображение",
                            value=f"[Тык]({message.attachments[0].proxy_url})",
                            inline=False,
                        )
                        embed.set_image(url=message.attachments[0].proxy_url)

                    await channel.send(embed=embed)

    @commands.Cog.listener(disnake.Event.message_edit)
    async def on_message_edit(self, before, after):
        if after.content == before.content:
            return
        elif len(after.content) > 4096 or len(before.content) > 4096:
            return
        elif after.author.bot:
            return

        else:
            log_channel = await self.db.get_log_channel(after.guild.id)
            if log_channel is not None:
                channel_id = log_channel["log_channel_id"]
                channel = disnake.utils.get(after.guild.channels, id=channel_id)
                if channel:
                    embed = disnake.Embed(
                        description=f"[Сообщение]({after.jump_url}) было отредактировано",
                        color=self.color.MAIN,
                        timestamp=datetime.datetime.fromtimestamp(
                            datetime.datetime.now().timestamp()
                        ),
                    )
                    embed.add_field(
                        name="Старое содержимое:",
                        value=f"```{before.content}```",
                        inline=False,
                    )
                    embed.add_field(
                        name="Новое содержимое:",
                        value=f"```{after.content}```",
                        inline=False,
                    )
                    embed.add_field(
                        name="Автор",
                        value=f"**{after.author.name}** ({after.author.mention})",
                        inline=True,
                    )
                    embed.add_field(
                        name="Канал",
                        value=f"**{after.channel.name}** ({after.channel.mention})",
                        inline=True,
                    )
                    embed.set_footer(text=f"ID сообщения: {after.id}")
                    embed.set_thumbnail(url=after.author.display_avatar.url)

                    if after.attachments:
                        embed.set_image(
                            url=after.attachments[0].proxy_url
                            if bool(after.attachments)
                            else disnake.embeds.EmptyEmbed
                        )

                    await channel.send(embed=embed)

    @commands.Cog.listener(disnake.Event.member_update)
    async def on_member_update(self, before, after):
        if before.display_name != after.display_name:
            log_channel = await self.db.get_log_channel(after.guild.id)
            if log_channel is not None:
                channel_id = log_channel["log_channel_id"]
                channel = disnake.utils.get(after.guild.channels, id=channel_id)
                if channel:
                    embed = disnake.Embed(
                        description=f"Никнейм {'бота' if after.bot else 'участника'} **{after}** ({after.mention}) был изменен",
                        color=self.color.MAIN,
                        timestamp=datetime.datetime.fromtimestamp(
                            datetime.datetime.now().timestamp()
                        ),
                    )
                    embed.set_footer(
                        text=f"ID {'бота' if after.bot else 'участника'}: {after.id}"
                    )
                    embed.set_thumbnail(url=after.display_avatar.url)
                    embed.add_field(
                        name="Старый никнейм:", value=before.display_name, inline=True
                    )
                    embed.add_field(
                        name="Новый никнейм:", value=after.display_name, inline=True
                    )
                    await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Logs(bot))
