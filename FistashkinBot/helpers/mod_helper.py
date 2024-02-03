import disnake
import datetime

from disnake.ext import commands
from utils import enums, database


class ModerationHelper:
    def __init__(self):
        self.color = enums.Color()
        self.db = database.DataBase()

    async def check_time_muted(
        self, inter, member, time, reason, send_to_member: bool = False
    ):
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
            description=f"✅ Участник {member.mention} замьючен! 🙊",
            color=self.color.MAIN,
            timestamp=inter.created_at,
        )
        embed.add_field(name="Модератор", value=inter.author.mention, inline=True)
        embed.add_field(name="Наказание будет снято", value=dynamic_time, inline=True)
        embed.add_field(name="Причина", value=reason, inline=False)

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(
            text="Команда по безопасности Discord сервера",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )

        dm_embed = disnake.Embed(
            description=f"Вам была выдана заглушка чата на сервере `{inter.guild.name}`!",
            color=self.color.MAIN,
            timestamp=inter.created_at,
        )

        dm_embed.add_field(
            name="Модератор",
            value=f"{inter.author.mention}\n`[ID: {inter.author.id}]`",
            inline=True,
        )
        dm_embed.add_field(
            name="Наказание будет снято", value=dynamic_time, inline=True
        )
        dm_embed.add_field(name="Причина", value=reason, inline=False)

        dm_embed.set_thumbnail(url=member.display_avatar.url)
        dm_embed.set_footer(
            text="Команда по безопасности Discord сервера",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )

        log_channel = await self.db.get_log_channel(inter.guild.id)
        if log_channel is not None:
            channel_id = log_channel["log_channel_id"]
            channel = disnake.utils.get(inter.guild.channels, id=channel_id)
            if channel:
                log_embed = disnake.Embed(
                    description=f"Участник {member.mention} замьючен! 🙊",
                    color=self.color.MAIN,
                    timestamp=inter.created_at,
                )
                log_embed.add_field(
                    name="Модератор", value=inter.author.mention, inline=True
                )
                log_embed.add_field(
                    name="Наказание будет снято", value=dynamic_time, inline=True
                )
                log_embed.add_field(name="Причина", value=reason, inline=False)

                log_embed.set_thumbnail(url=member.display_avatar.url)
                log_embed.set_footer(
                    text=f"ID {'бота' if member.bot else 'участника'}: {member.id}"
                )
                await channel.send(embed=log_embed)

        await member.timeout(until=dynamic_durations, reason=reason)
        if send_to_member:
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

    async def send_embed_punishment(
        self,
        inter,
        member: disnake.Member,
        reason,
        punish,
        dm_punish,
        send_to_member: bool = False,
    ):
        await inter.response.defer(ephemeral=False)

        embed = disnake.Embed(
            description=punish,
            color=self.color.MAIN,
            timestamp=inter.created_at,
        )

        embed.add_field(name="Модератор", value=inter.author.mention)
        embed.add_field(name="Причина", value=reason)

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(
            text="Команда по безопасности Discord сервера",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )

        dm_embed = disnake.Embed(
            description=dm_punish,
            color=self.color.MAIN,
            timestamp=inter.created_at,
        )

        dm_embed.add_field(
            name="Модератор", value=f"{inter.author.mention}\n`[ID: {inter.author.id}]`"
        )
        dm_embed.add_field(name="Причина", value=reason)

        dm_embed.set_footer(
            text="Команда по безопасности Discord сервера",
            icon_url=inter.guild.icon.url if inter.guild.icon else None,
        )

        log_channel = await self.db.get_log_channel(inter.guild.id)
        if log_channel is not None:
            channel_id = log_channel["log_channel_id"]
            channel = disnake.utils.get(inter.guild.channels, id=channel_id)
            if channel:
                log_embed = disnake.Embed(
                    description=punish[2:],
                    color=self.color.MAIN,
                    timestamp=inter.created_at,
                )

                log_embed.add_field(name="Модератор", value=inter.author.mention)
                log_embed.add_field(name="Причина", value=reason)

                log_embed.set_thumbnail(url=member.display_avatar.url)
                log_embed.set_footer(
                    text=f"ID {'бота' if member.bot else 'участника'}: {member.id}"
                )
                await channel.send(embed=log_embed)

        if send_to_member == True:
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
        else:
            pass

        if punish == f"✅ Участник {member.mention} был забанен.":
            await inter.guild.ban(user=member, reason=reason)
        elif punish == f"✅ Участник {member.mention} был изгнан с сервера.":
            await inter.guild.kick(user=member, reason=reason)
        elif punish == f"✅ С участника {member.mention} сняты ограничения! 🐵":
            await member.timeout(until=None, reason=reason)
        elif punish == f"✅ Участник {member.mention} получил предупреждение!":
            await self.db.add_warn(member, inter.author.id, reason)

        await inter.edit_original_message(embed=embed)
