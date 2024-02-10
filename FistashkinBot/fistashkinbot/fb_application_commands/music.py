import disnake
import wavelink
import re
import os
import asyncio

from disnake.ext import commands
from wavelink.ext import spotify
from disnake.enums import ButtonStyle
from utils import main, enums, constant
from core import config
from loguru import logger
from utils import checks


class CustomPlayer(wavelink.Player):
    def __init__(self):
        super().__init__()
        self.queue = wavelink.Queue()


class ControlPanel(disnake.ui.View):
    message: disnake.Message

    def __init__(self, vc, inter):
        super().__init__(timeout=None)
        self.vc = inter.guild.voice_client
        self.inter = inter
        self.color = enums.Color()

    @disnake.ui.button(style=disnake.ButtonStyle.gray, emoji="⏸️")
    async def resume_and_pause(self, button: disnake.ui.Button, inter):
        if not inter.user == self.inter.author:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description=f"❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                    color=self.color.DARK_GRAY,
                ),
                ephemeral=True,
            )
        if self.vc.is_paused():
            await self.vc.resume()
            await inter.response.send_message(
                embed=disnake.Embed(
                    description=f"⏯ | Возобновлено!", color=self.color.DARK_GRAY
                ),
                ephemeral=True,
            )
        else:
            await self.vc.pause()
            await inter.response.send_message(
                embed=disnake.Embed(
                    description=f"⏸ | На паузе!", color=self.color.DARK_GRAY
                ),
                ephemeral=True,
            )

    @disnake.ui.button(style=disnake.ButtonStyle.gray, emoji="⏭️")
    async def skip(self, button: disnake.ui.Button, inter):
        if not inter.user == self.inter.author:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description=f"❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                    color=self.color.DARK_GRAY,
                ),
                ephemeral=True,
            )
        if self.vc.queue.is_empty:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description=f"❌ | Ничего не играет или очередь пуста!",
                    color=self.color.DARK_GRAY,
                ),
                ephemeral=True,
            )
        await self.vc.seek(self.vc.track.length * 1000)
        await inter.response.send_message(
            embed=disnake.Embed(
                description=f"⏭️ | Пропущено!", color=self.color.DARK_GRAY
            ),
            ephemeral=True,
        )
        await asyncio.sleep(5)
        embed = disnake.Embed(
            title=self.vc.source.title,
            url=self.vc.source.uri,
            description=f"Сейчас играет `{self.vc.source.title}` в {self.vc.channel.mention}\n"
            f"Длительность: `{int(self.vc.source.length // 60)}:{int(self.vc.source.length % 60)}`",
            color=self.color.DARK_GRAY,
        )
        embed.set_thumbnail(self.vc.source.thumb)
        embed.set_author(name=self.vc.source.author)
        view = ControlPanel(self.vc, inter)
        await self.message.edit(embed=embed, view=view)

    @disnake.ui.button(style=disnake.ButtonStyle.gray, emoji="💠")
    async def queue(self, button: disnake.ui.Button, inter):
        if not inter.user == self.inter.author:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description=f"❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                    color=self.color.DARK_GRAY,
                ),
                ephemeral=True,
            )
        if self.vc.queue.is_empty:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description=f"❌ | Очередь пуста!", color=self.color.DARK_GRAY
                ),
                ephemeral=True,
            )

        button.disabled = False
        em = disnake.Embed(title="Очередь", color=self.color.DARK_GRAY)
        queue = self.vc.queue.copy()
        trackCount = 0

        for track in queue:
            trackCount += 1
            em.add_field(
                name=f"Трек №{str(trackCount)}",
                value=f"[{track}]({track.uri})",
                inline=False,
            )
        await inter.response.send_message(embed=em, ephemeral=True)

    @disnake.ui.button(style=disnake.ButtonStyle.red, emoji="⏹️")
    async def disconnect(self, button: disnake.ui.Button, inter):
        await inter.response.defer()
        if not inter.user == self.inter.author:
            return await inter.response.send_message(
                embed=disnake.Embed(
                    description=f"❌ | Вы не можете этого сделать. запустите команду самостоятельно, чтобы использовать эти кнопки.",
                    color=self.color.DARK_GRAY,
                ),
                ephemeral=True,
            )
        for child in self.children:
            child.disabled = True
            if self.vc:
                await self.vc.disconnect()
                await inter.message.edit(
                    content="Бот отключен от голосового канала.", view=self
                )
            else:
                await inter.response.send_message(
                    embed=disnake.Embed(
                        description=f"Как я могу отключиться, когда я не подключен?",
                        color=self.color.DARK_GRAY,
                    )
                )


class Music(commands.Cog, name="🎵 Музыка [WIP]"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.song_queue = {}
        self.config = config.Config()
        self.color = enums.Color()
        self.checks = checks.Checks(self.bot)
        bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(
            bot=self.bot,
            host=self.config.LAVALINK_SETTINGS["host"],
            port=self.config.LAVALINK_SETTINGS["port"],
            password=self.config.LAVALINK_SETTINGS["password"],
            spotify_client=spotify.SpotifyClient(
                client_id=self.config.SPOTIFY_CLIENT_ID,
                client_secret=self.config.SPOTIFY_CLIENT_SECRET,
            ),
        )

    @commands.Cog.listener()
    async def on_wavelink_track_end(
        self, player: CustomPlayer, track: wavelink.Track, reason
    ):
        if not player.queue.is_empty:
            next_track = player.queue.get()
            await player.play(next_track)
        else:
            await player.disconnect()

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        logger.info(f"Node: <{node.identifier}> is ready!")

    @commands.slash_command(
        name=disnake.Localized("play", key="MUSIC_PLAY_COMMAND_NAME"),
        description=disnake.Localized("", key="MUSIC_PLAY_COMMAND_DESCRIPTION"),
        dm_permission=False,
    )
    async def play(
        self,
        inter,
        search: str = commands.Param(
            name=disnake.Localized("search", key="MUSIC_PLAY_TEXT_COMMAND_NAME"),
            description=disnake.Localized(
                "Specify the link or name of the track.",
                key="MUSIC_PLAY_TEXT_COMMAND_DESCRIPTION",
            ),
        ),
    ):
        return await self.checks.check_is_wip(inter)
        """url_type = self.check_string(search)
        action = self.url_type_mapping.get(url_type, None)
        vc = inter.guild.voice_client
        if not vc:
            custom_player = CustomPlayer()
            vc: CustomPlayer = await inter.author.voice.channel.connect(
                cls=custom_player
            )
        if action:
            await action(self, inter, search, vc)
        else:
            await inter.response.defer(ephemeral=True)
            await inter.edit_original_message(
                embed=disnake.Embed(
                    description="Не знаю, эта ссылка неверная. Попробуйте еще раз!",
                    color=self.color.DARK_GRAY,
                )
            )"""

    @commands.slash_command(
        name=disnake.Localized("music_panel", key="MUSIC_PANEL_COMMAND_NAME"),
        description=disnake.Localized(
            "Displays the music panel for controlling the music.",
            key="MUSIC_PANEL_COMMAND_DESCRIPTION",
        ),
        dm_permission=False,
    )
    async def nowplaying(self, inter):
        return await self.checks.check_is_wip(inter)
        """vc = inter.guild.voice_client
        if vc:
            await inter.response.defer(ephemeral=False)
            embed = disnake.Embed(
                title=vc.source.title,
                url=vc.source.uri,
                description=f"Сейчас играет `{vc.source.title}` в {vc.channel.mention}\n"
                f"Длительность: `{int(vc.source.length // 60)}:{int(vc.source.length % 60)}`",
                color=self.color.DARK_GRAY,
            )
            embed.set_thumbnail(vc.source.thumb)
            embed.set_author(name=vc.source.author)
            view = ControlPanel(vc, inter)
            message = await inter.edit_original_message(embed=embed, view=view)
            view.message = message
        else:
            await inter.response.defer(ephemeral=True)
            return await inter.edit_original_message(
                embed=disnake.Embed(
                    description=f"❌| Сейчас ничего не играет!",
                    color=self.color.DARK_GRAY,
                )
            )"""

    async def play_spotify_track(self, inter, track: str, vc: CustomPlayer):
        track = await spotify.SpotifyTrack.search(query=track, return_first=True)
        if vc.is_playing() or not vc.queue.is_empty:
            await inter.response.defer(ephemeral=False)
            vc.queue.put(item=track)
            embed = disnake.Embed(
                title=track.title,
                url=track.uri,
                description=f"В очереди `{track.title}` в {vc.channel.mention}\n"
                f"Длительность: `{int(track.length // 60)}:{int(track.length % 60)}`",
                color=self.color.DARK_GRAY,
            )
            embed.set_thumbnail(track.thumb)
            embed.set_author(name=track.author)
            await inter.edit_original_message(embed=embed)
        else:
            await inter.response.defer(ephemeral=False)
            await vc.play(track)
            embed = disnake.Embed(
                title=track.title,
                url=track.uri,
                description=f"Играет `{track.title}` в {vc.channel.mention}\nДлительность: `{int(track.length // 60)}:{int(track.length % 60)}`",
                color=self.color.DARK_GRAY,
            )
            embed.set_thumbnail(track.thumb)
            embed.set_author(name=track.author)
            await inter.edit_original_message(embed=embed)

    async def play_spotify_playlist(self, inter, playlist: str, vc: CustomPlayer):
        await inter.send(
            embed=disnake.Embed(
                description=f"📃| Загрузка плейлиста...", color=self.color.DARK_GRAY
            )
        )
        async for partial in spotify.SpotifyTrack.iterator(
            query=playlist, partial_tracks=True
        ):
            if vc.is_playing() or not vc.queue.is_empty:
                vc.queue.put(item=partial)
            else:
                await vc.play(partial)
                embed = disnake.Embed(
                    title=vc.source.title,
                    description=f"Играет плейлист `{vc.source.title}` в {vc.channel.mention}\nДлительность: `{int(vc.source.length // 60)}:{int(vc.source.length % 60)}`",
                    color=self.color.DARK_GRAY,
                )
                embed.set_thumbnail(vc.source.thumb)
                embed.set_author(name=vc.source.author)

                await inter.send(embed=embed)

    async def play_youtube_song(self, inter, query: str, vc: CustomPlayer):
        try:
            query = re.sub(r"&t=\d+", "", query)
            logger.info(query)
            track = await wavelink.NodePool.get_node().get_tracks(
                wavelink.YouTubeTrack, query
            )
            track = track[0]
            if vc.is_playing() or not vc.queue.is_empty:
                vc.queue.put(item=track)
                embed = disnake.Embed(
                    title=track.title,
                    url=track.uri,
                    description=f"В очереди `{track.title}` в {vc.channel.mention}\nДлительность: `{int(track.length // 60)}:{int(track.length % 60)}`",
                    color=self.color.DARK_GRAY,
                )
                embed.set_thumbnail(track.thumb)
                embed.set_author(name=track.author)

                await inter.send(embed=embed)
            else:
                await vc.play(track)
                embed = disnake.Embed(
                    title=vc.source.title,
                    url=vc.source.uri,
                    description=f"Играет `{vc.source.title}` в {vc.channel.mention}\nДлительность: `{int(vc.source.length // 60)}:{int(vc.source.length % 60)}`",
                    color=self.color.DARK_GRAY,
                )
                embed.set_thumbnail(vc.source.thumb)
                embed.set_author(name=vc.source.author)

                await inter.send(embed=embed)
        except Exception as e:
            await inter.send(
                embed=disnake.Embed(
                    description="Не знаю, эта ссылка неверная. Попробуйте еще раз!",
                    color=self.color.DARK_GRAY,
                ),
                ephemeral=True,
            )

    async def play_youtube_playlist(inter, playlist: str):
        pass

    async def play_query(self, inter, search: str, vc: CustomPlayer):
        track = await wavelink.YouTubeTrack.search(query=search, return_first=True)
        if vc.is_playing() or not vc.queue.is_empty:
            vc.queue.put(item=track)
            embed = disnake.Embed(
                title=track.title,
                url=track.uri,
                description=f"В очереди `{track.title}` в {vc.channel.mention}\nДлительность: `{int(track.length // 60)}:{int(track.length % 60)}`",
                color=self.color.DARK_GRAY,
            )
            embed.set_thumbnail(track.thumb)
            embed.set_author(name=track.author)
            await inter.send(embed=embed)
        else:
            await vc.play(track)
            embed = disnake.Embed(
                title=vc.source.title,
                url=vc.source.uri,
                description=f"Играет `{vc.source.title}` в {vc.channel.mention}\nДлительность: `{int(vc.source.length // 60)}:{int(vc.source.length % 60)}`",
                color=self.color.DARK_GRAY,
            )
            embed.set_thumbnail(vc.source.thumb)
            embed.set_author(name=vc.source.author)
            await inter.send(embed=embed)

    # Map URL types to their corresponding functions
    url_type_mapping = {
        "Spotify Track": play_spotify_track,
        "Spotify Playlist": play_spotify_playlist,
        "Spotify Album": play_spotify_playlist,
        "YouTube Song": play_youtube_song,
        "YouTube Playlist": play_youtube_playlist,
        "Text": play_query,
    }

    def check_string(self, input_string):
        youtube_pattern = re.compile(
            (
                r"https?://(www\.)?(youtube|youtu)(\.com|\.be)/"
                "(playlist\?list=|watch\?v=|embed/|)([a-zA-Z0-9-_]+)(\&t=\d+s)?"
                "|https://youtu.be/([a-zA-Z0-9-_]+)(\?t=\d+s)?"
            )
        )
        spotify_pattern = re.compile(
            (
                r"https?://open\.spotify\.com/(album|playlist|track)"
                "/([a-zA-Z0-9-]+)(/[a-zA-Z0-9-]+)?(\?.*)?"
            )
        )

        youtube_match = youtube_pattern.match(input_string)
        spotify_match = spotify_pattern.match(input_string)

        if youtube_match:
            return self.get_youtube_pattern(youtube_match)
        elif spotify_match:
            return self.get_spotify_pattern(spotify_match)
        return "Text"

    def get_spotify_pattern(self, spotify_match):
        if spotify_match:
            if "track" in spotify_match.group():
                return "Spotify Track"
            elif "playlist" in spotify_match.group():
                return "Spotify Playlist"
            elif "album" in spotify_match.group():
                return "Spotify Album"
            else:
                return "Spotify URL"

    def get_youtube_pattern(self, youtube_match):
        if youtube_match:
            if (
                "watch?v=" in youtube_match.group()
                or "youtu.be" in youtube_match.group()
            ):
                return "YouTube Song"
            elif "playlist?list=" in youtube_match.group():
                return "YouTube Playlist"
            else:
                return "YouTube URL"


def setup(bot):
    bot.add_cog(Music(bot))
