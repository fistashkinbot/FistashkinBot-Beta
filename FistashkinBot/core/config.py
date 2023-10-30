from environs import Env

class Config:

	env = Env()
	env.read_env()
	PREFIX = "f!"
	TOKEN = env.str("TOKEN")
	MONGODB_LINK = env.str("MONGODB_LINK")
	SPOTIFY_CLIENT_ID = env.str("SPOTIFY_CLIENT_ID")
	SPOTIFY_CLIENT_SECRET = env.str("SPOTIFY_CLIENT_SECRET")