from environs import Env

env = Env()
env.read_env(override=True)

TOKEN=env.str('TOKEN')
CHAT_IDS=env.list('CHAT_IDS')
DB_URL=env.str('DB_URL')
