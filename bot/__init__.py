from discord import Client

from . import messages, roles
from .config import Config, Guild, Role


bot = Client()
config = Config('config.json')


async def ensure_roles(guild):
    guild_config = config.guilds[guild.id]
    guild_roles = {role.name: role for role in guild.roles}

    for missing_role_name in set(roles.by_name) - set(guild_roles):
        missing_role = roles.by_name[missing_role_name]
        role = await guild.create_role(
            name=missing_role.name,
            color=missing_role.color,
            mentionable=True,
            reason='Initializing reaction bot roles',
        )
        guild_config.roles[missing_role.emoji] = Role(
            emoji=missing_role.emoji,
            role_id=role.id,
        )
        config.save()

    for missing_role_emoji in set(roles.by_emoji) - set(guild_config.roles):
        missing_role = roles.by_emoji[missing_role_emoji]
        guild_config.roles[missing_role_emoji] = Role(
            emoji=missing_role_emoji,
            role_id=guild_roles[missing_role.name].id,
        )
        config.save()


@bot.event
async def on_ready():
    config.load()

    for guild in bot.guilds:
        if guild.id in config.guilds:
            continue

        config.guilds[guild.id] = Guild(guild.id)
        config.save()


@bot.event
async def on_message(message):
    if message.content == 'Roomie, initialize here.':
        channel = message.channel
        guild = channel.guild
        guild_config = config.guilds[guild.id]

        await ensure_roles(guild)

        if guild_config.welcome_message_id is not None:
            await channel.send(
                "I'm sorry Dave. I'm afraid I can't do that.",
                delete_after=5,
            )
            return

        welcome_message = await channel.send(messages.WELCOME)
        guild_config.welcome_message_id = welcome_message.id

        for emoji, role in guild_config.roles.items():
            await welcome_message.add_reaction(emoji)

        config.save()

    elif message.content == 'Roomie, nuke it from orbit.':
        channel = message.channel
        guild_config = config.guilds[channel.guild.id]
        message_id = guild_config.welcome_message_id

        if message_id is None:
            await channel.send(
                'It is not the only way to be sure.',
                delete_after=5,
            )
            return

        message = await channel.fetch_message(message_id)
        await message.delete()

        guild_config.welcome_message_id = None
        config.save()


async def manage_reactions(payload):
    guild_id = payload.guild_id
    guild_config = config.guilds[guild_id]

    if payload.message_id != guild_config.welcome_message_id:
        return

    config_role = guild_config.roles.get(payload.emoji.name)

    if config_role is None:
        return

    guild = bot.get_guild(guild_id)
    role = guild.get_role(config_role.role_id)

    if payload.event_type == 'REACTION_ADD':
        await payload.member.add_roles(role)
    else:
        member = await guild.fetch_member(payload.user_id)
        await member.remove_roles(role)


@bot.event
async def on_raw_reaction_add(payload):
    await manage_reactions(payload)


@bot.event
async def on_raw_reaction_remove(payload):
    await manage_reactions(payload)
