from discord import Client

from .config import Config
from .messages import WELCOME


bot = Client()
bot.config = config = Config('config.json')
config.load()


@bot.event
async def on_message(message):
    if message.content == 'Roomie, initialize here.':
        channel = message.channel

        if bot.config.welcome_message_id is not None:
            await channel.send(
                "I'm sorry Dave. I'm afraid I can't do that.",
                delete_after=5,
            )
            return

        welcome_message = await channel.send(WELCOME)
        bot.config.welcome_message_id = welcome_message.id
        bot.config.save()
