import disnake
import random

from core import FistashkinBot


class Activity:
    GAMES_NAMES = [
        "Dota 2",
        "Half-Life",
        "Half-Life: Source",
        "Half-Life 2",
        "Half-Life 2: Lost Coast",
        "Half-Life 2: Episode One",
        "Half-Life 2: Episode Two",
        "Black Mesa",
        "Grand Theft Auto San Andreas",
        "Mobile Legends",
        "Cyberpunk 2077",
        "Silent Hill",
        "Silent Hill 2",
        "Manhunt",
        "Manhunt 2",
        "Doom",
        "очке своим пальчиком",
        "самого себя",
        "Party Hard",
        "Hotline Miami",
        "Hotline Miami 2",
        "Warcraft III",
        "Unreal 2 - The Awakening",
        "Neon Drive",
        "Counter-Strike 2",
    ]

    STREAMING_NAMES = [
        "Dota 2",
        "Grand Theft Auto San Andreas",
        "Dota 2",
        "Half-Life",
        "Half-Life: Source",
        "Half-Life 2",
        "Half-Life 2: Lost Coast",
        "Half-Life 2: Episode One",
        "Half-Life 2: Episode Two",
        "Black Mesa",
        "Grand Theft Auto San Andreas",
        "Mobile Legends",
        "Cyberpunk 2077",
        "Silent Hill",
        "Silent Hill 2",
        "Manhunt",
        "Manhunt 2",
        "Doom",
        "Counter-Strike 2",
    ]

    STREAMING_URL = [
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://www.youtube.com/watch?v=16y1AkoZkmQ",
        "https://www.youtube.com/watch?v=eNvUS-6PTbs",
        "https://www.youtube.com/watch?v=L_jWHffIx5E",
        "https://www.youtube.com/watch?v=pVHKp6ffURY",
        "https://www.youtube.com/watch?v=K5DALXwOe0s",
        "https://www.youtube.com/watch?v=aTJncWndUB8",
        "https://www.youtube.com/watch?v=5dkpk1gmaDc",
        "https://www.youtube.com/watch?v=9c5yPIQ3LQI",
        "https://www.youtube.com/watch?v=KQ6zr6kCPj8",
        "https://www.youtube.com/watch?v=5qm8PH4xAss",
        "https://www.youtube.com/watch?v=SRcnnId15BA",
        "https://www.youtube.com/watch?v=_CL6n0FJZpk",
        "https://www.youtube.com/watch?v=QZXc39hT8t4",
        "https://www.youtube.com/watch?v=h4UqMyldS7Q",
        "https://www.youtube.com/watch?v=fJuapp9SORA",
        "https://www.youtube.com/watch?v=TMZi25Pq3T8",
        "https://www.youtube.com/watch?v=zaaoFbNsyf4",
        "https://www.youtube.com/watch?v=15nMlfogITw",
        "https://www.youtube.com/watch?v=hBP9txbREWI",
        "https://www.youtube.com/watch?v=GtUVQei3nX4",
    ]

    WATCHING_NAMES = [
        "за птичками",
        "Gachimuchi",
        "YouTube",
        "Netflix",
        "аниме",
        "Neon Genesis Evangelion",
        "The End of Evangelion",
        "Tokyo Ghoul",
        "Squid Game",
        "Cowboy Bebop",
        "Serial Experiments Lain",
        "Breaking Bad",
        "Better Call Saul",
        "El Camino: Breaking Bad",
        "The Boys",
        "Fight Club",
    ]

    LISTENING_NAMES = ["Spotify", "Soundcloud", "Apple Music"]

    COMPETING_NAMES = ["Dota 2", "Gachimuchi", "спидране Half-Life"]


class BotActivity:
    ACTIVITY = [
        disnake.Game(name=random.choice(Activity.GAMES_NAMES)),
        disnake.Streaming(
            name=random.choice(Activity.STREAMING_NAMES),
            url=random.choice(Activity.STREAMING_URL),
        ),
        disnake.Activity(
            name=random.choice(Activity.WATCHING_NAMES),
            type=disnake.ActivityType.watching,
        ),
        disnake.Activity(
            name=random.choice(Activity.LISTENING_NAMES),
            type=disnake.ActivityType.listening,
        ),
    ]

    STATUS = [disnake.Status.idle, disnake.Status.online, disnake.Status.dnd]
