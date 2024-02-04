import disnake

from disnake.ext import commands
from utils import database


class TempVoice(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.db = database.DataBase()

    @commands.Cog.listener(disnake.Event.voice_state_update)
    async def on_voice_state_update(
        self,
        member: disnake.Member,
        before: disnake.VoiceState,
        after: disnake.VoiceState,
    ):
        if after.channel is not None:
            trigger_info = await self.db.get_voice_channel_trigger(
                member.guild.id, after.channel.id
            )
            if trigger_info and after.channel.id == trigger_info["channel_id"]:
                guild = self.bot.get_guild(trigger_info["guild_id"])
                category_id = trigger_info["category_id"]
                main_category = disnake.utils.get(guild.categories, id=category_id)

                # категория создания канала
                private_channel = await guild.create_voice_channel(
                    f"Комната {member.display_name}",  # название канала
                    category=main_category,  # категория в которой создастся канал
                    bitrate=96000,  # установить битрейт 96
                )
                await private_channel.set_permissions(
                    member,
                    connect=False,
                    mute_members=True,
                    move_members=True,
                    manage_channels=True,
                )  # установить права на канал его создателю
                await member.move_to(
                    private_channel
                )  # переместить пользователя в этот канал

                def check(x, y, z):
                    return len(private_channel.members) == 0

                await self.bot.wait_for("voice_state_update", check=check)
                await private_channel.delete()


def setup(bot):
    bot.add_cog(TempVoice(bot))
