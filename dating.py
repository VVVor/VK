
from dating_bot import DatingBot
from config import access_token, community_token, db_config

bot = DatingBot(access_token, community_token, db_config)
bot.listen()

print("Start dating")


