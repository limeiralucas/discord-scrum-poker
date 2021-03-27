from client import client
from loguru import logger

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
    logger.info("Reaction Received")
    if reaction.message.author != client.user or user == client.user:
        return

    value = EMOJI.get(reaction.emoji)
    if not value:
        return

    sum_votes = 0
    total_votes = 0
    for r in  reaction.message.reactions:
        reaction_count = r.count - 1
        sum_votes += EMOJI.get(r.emoji, 0) * reaction_count
        total_votes += reaction_count

    story_points = sum_votes / total_votes

    content = reaction.message.content.split("SP: ")[0]
    content += f"SP: {story_points}"
    await reaction.message.edit(content=content)


if __name__ == "__main__":
    from config import TOKEN

    client.run(TOKEN)
