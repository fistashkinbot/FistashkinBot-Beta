from environs import Env


class Config:
    env = Env()
    env.read_env()
    TOKEN = env.str("TOKEN")
    MONGODB_LINK = env.str("MONGODB_LINK")
    SPOTIFY_CLIENT_ID = env.str("SPOTIFY_CLIENT_ID")
    GIFHY_API_KEY = env.str("GIFHY_API_KEY")
    SPOTIFY_CLIENT_SECRET = env.str("SPOTIFY_CLIENT_SECRET")
    WEATHER_API_TOKEN = env.str("WEATHER_API_TOKEN")

    LAVALINK_SETTINGS = {
        "host": "hp8.nexcord.com",
        "port": 10216,
        "password": "N1KE02061992",
    }
