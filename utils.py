from bot_emoji import EMOJI


def calculate_story_points(message):
    sum_votes = 0
    total_votes = 0
    for r in message.reactions:
        reaction_count = r.count - 1
        sum_votes += EMOJI.get(r.emoji, 0) * reaction_count
        total_votes += reaction_count

    if total_votes == 0:
        return 0

    return 0 if total_votes == 0 else sum_votes / total_votes


async def handler_reaction(message, user, client_user):
    if message.author != client_user or user == client_user:
        return

    story_points = calculate_story_points(message)
    content = message.content.split("SP: ")[0]
    content += f"SP: {story_points}"
    await message.edit(content=content)
