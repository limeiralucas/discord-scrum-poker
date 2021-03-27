from discord import Message, reaction
from client import client
from loguru import logger

from utils import handler_reaction
from bot_emoji import EMOJI


@client.event
async def on_ready():
    logger.info("Bot is ready to rock!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$sbot "):
        title = message.content.split("$sbot ")[-1]
        content = f"Task: {title} | SP: 0"
        sent_msg = await message.channel.send(content)
        for emoji in EMOJI.keys():
            await sent_msg.add_reaction(emoji)


@client.event
async def on_reaction_add(reaction, user):
    await handler_reaction(reaction.message, user, client.user)


@client.event
async def on_raw_reaction_remove(payload):
    channel = client.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    await handler_reaction(message, payload.member, client.user)

if __name__ == "__main__":
    from config import TOKEN

    client.run(TOKEN)
