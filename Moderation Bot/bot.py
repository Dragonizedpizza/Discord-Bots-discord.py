import discord
from discord.ext import commands
import os
import asyncio
import random

client = commands.Bot(command_prefix = ">", case_insensitive = True)

#Defining functions, normal ones
def convert(time):
    pos = ['s', 'm', 'h', 'd']
    time_dict = {
    "s" : 1, "m" : 60, "h" : 3600, "d" : 3600*24
    }
    unit = time[-1]
    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except:
        return -2

    return val * time_dict[unit]

@client.event
async def on_ready():
    print("Ready")

@client.command()
async def ping(ctx):
    await ctx.send('Pong!')

filtered_words = ['idiot', 'die', 'dumb', 'ass', 'fool', 'idiots', 'fools', '']


@client.remove_command('help')
@client.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title = "Missing Permissions", color = discord.Color.purple())
        embed.add_field(name = "An error occured", value = "You don't have the permissions!")
        await ctx.send(embed = embed)
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(title = 'BadArgument', color = discord.Color.purple())
        embed.add_field(name = "An error occured", value = "You put a wrong argument")
        await ctx.send(embed = embed)
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = 'CommandNotFound', color = discord.Color.purple())
        embed.add_field(name = "An error occured", value = "Command doesn't work")
        await ctx.send(embed = embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title = 'MissingRequiredArgument', color = discord.Color.purple())
        embed.add_field(name = "An error occured", value = "You missed a required argument")
        await ctx.send(embed = embed)
    else:
        await ctx.send(f"Unknown error, raising!")
        raise error

@client.command()
async def botinfo(ctx):
    embed = discord.Embed(title = "Information", color = discord.Color.purple())
    embed.add_field(name = "Bot Dev", value = "NightZan999#0194")
    embed.set_footer(text = "More will be added in the future")
    await ctx.send(embed = embed)

@client.command()
async def help(ctx, command = None):
    if command == None:
        embed = discord.Embed(title = "Help", color = discord.Color.purple())


@client.command()
@commands.has_permissions(kick_members = True)
async def kick(ctx, member : discord.Member, *, reason = None):
    embed = discord.Embed(title = f'{ctx.author.name} kicks {member.name}!', color = discord.Color.purple())
    embed.add_field(name = "Moderator", value = f'{ctx.author.mention}')
    if reason == None:
        embed.add_field(name = "Reason", value = f"{reason}")
    await ctx.send(embed = embed)
    try:
        await member.send(f"You were kicked in {ctx.guild.name} by {ctx.author.name}\nReason: {reason}")
    except:
        print(f"{member.name} has DMs off!")
    finally:
        await member.kick(reason = reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason = None):
    embed = discord.Embed(title = f'{ctx.author.name} bans {member.name}!', color = discord.Color.purple())
    embed.add_field(name = "Moderator", value = f'{ctx.author.mention}')
    if reason == None:
        embed.add_field(name = "Reason", value = f"{reason}")
    await ctx.send(embed = embed)
    try:
        await member.send(f"You were banned in {ctx.guild.name} by {ctx.author.name}\nReason: {reason}")
    except:
        print(f"{member.name} has DMs off!")
    finally:
        await member.ban(reason = reason)

@client.command()
@commands.has_permissions(ban_members = True)
async def softban(ctx, member : discord.Member, *, reason = None):
    embed = discord.Embed(title = f'{ctx.author.name} bans {member.name}!', color = discord.Color.purple())
    embed.add_field(name = "Moderator", value = f'{ctx.author.mention}')
    if reason == None:
        embed.add_field(name = "Reason", value = f"{reason}")
    await ctx.send(embed = embed)
    try:
        await member.send(f"You were banned in {ctx.guild.name} by {ctx.author.name}\nReason: {reason}")
    except:
        print(f"{member.name} has DMs off!")
    finally:
        await member.ban(reason = reason)
        await member.unban(reason = reason)

@client.command()
@commands.has_permissions(kick_members = True)
async def warn(ctx, member : discord.Member, *, reason = None):
    if reason == None:
        await ctx.send("You have to provide a reason!")
    else:
        try:
            await member.send(f"You have been warned in {ctx.guild.name}\nBy: {ctx.author.name}\nReason: {reason}")
        except:
            pass
        embed = discord.Embed(title = f"{member.mention} was warned!", color = discord.Color.purple())
        embed.add_field(name = "Reason:", value = reason)
        await ctx.send(embed = embed)

@client.command()
@commands.has_permissions(ban_members = True)
async def unban(ctx, user):
    try:
        id = int(user)
        await ctx.guild.unban(discord.Object(id = id))

    except ValueError:
        bans = await ctx.guild.bans()

        # Iterator
        def is_banned(banned_user) -> bool:
            str(banned_user) == user

        users = filter(is_banned, bans)
        users = [i for i in bans if str(i) == user]

        if users:
            await ctx.guild.unban(users[0])

@client.command()
@commands.has_permissions(manage_channels = True)
async def lock(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.message.channel.set_permissions(ctx.guild.default_role, send_messages=False)
    embed = discord.Embed(title = 'This channel has been locked by: ' + str(ctx.message.author), color = discord.Color.purple())
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(manage_channels = True)
async def unlock(ctx, amount = 1):
    await ctx.channel.purge(limit = amount)
    await ctx.message.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    embed = discord.Embed(title = 'This channel has been unlocked by: ' + str(ctx.message.author), color = discord.Color.purple())
    await ctx.send(embed=embed)

@client.command()
@commands.has_permissions(change_nickname = True)
async def nick(ctx,member:discord.Member,name):
    await member.edit(nick = name)
    embed = discord.Embed(title = 'Nick Name Successfully Changed!', color = discord.Color.purple())
    await ctx.send(embed = embed)


@client.command(aliases = ["setslowmode", "slowmode", "setmsgdelay"])
@commands.has_permissions(manage_messages = True)
async def setdelay(ctx, seconds: int):
    await ctx.channel.edit(slowmode_delay=seconds)
    await ctx.send(f"Set the slowmode delay in this channel to {seconds} seconds!")

@client.command(aliases = ['clear', 'delete'])
@commands.has_permissions(manage_messages = True)
async def purge(ctx, amount = 5):
    await ctx.send(f'Purging!')
    await ctx.channel.purge(limit = amount + 1)

@client.command(aliases = ['gstart', 'gsetup', 'g_host'])
@commands.has_permissions(administrator = True)
async def giveaway(ctx):
    await ctx.send("Let's start with this giveaway! Answer these questions within 15 seconds!")
    questions = ["Which channel should it be hosted in?",
                "What should be the duration of the giveaway? (s|m|h|d)",
                "What is the prize of the giveaway?"]
    answers = []
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    for i in questions:
        await ctx.send(i)
        await ctx.send(f"I will wait 30 seconds for the answer to this question!")
        try:
            msg = await client.wait_for('message', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send('You didn\'t answer in time, please be quicker next time!')
            return
        else:
            answers.append(msg.content)
    try:
        c_id = int(answers[0][2:-1])
    except:
        await ctx.send(f"You didn't mention a channel properly. Do it like this {ctx.channel.mention} next time.")
        return

    channel = client.get_channel(c_id)

    time = convert(answers[1])
    if time == -1:
        await ctx.send(f"You didn't answer the time with a proper unit. Use (s|m|h|d) next time!")
        return
    elif time == -2:
        await ctx.send(f"The time must be an integer. Please enter an integer next time")
        return

    prize = answers[2]

    await ctx.send(f"The Giveaway will be in {channel.mention} and will last {answers[1]}!")

    embed = discord.Embed(title = "Giveaway!", description = f"{prize}", color = discord.Color.purple())
    embed.add_field(name = "Hosted by:", value = ctx.author.mention)
    embed.set_footer(text = f"Ends {answers[1]} from now!")

    my_msg = await channel.send(embed = embed)
    await my_msg.add_reaction("🎉")

    await asyncio.sleep(time)
    new_msg = await channel.fetch_message(my_msg.id)

    users = await new_msg.reactions[0].users().flatten()
    users.pop(users.index(client.user))

    winner = random.choice(users)
    await channel.send(f"Congratulations! {winner.mention} won {prize}!")
    try:
        await winner.send(f"Congratulations! you won {prize} in {ctx.guild.name}!")
    except:
        await ctx.send(f"The winner has DMs off and thus can't claim the prize!")
        await ctx.send("Rerolling!")
        users.pop(winner)
        try:
            winner = random.choice(users)
            await ctx.channel.send(f"Congratulations! {winner.mention} won {prize}!")
            try:
                await winner.send(f"Congratulations! you won {prize} in {ctx.guild.name}!")
            except:
                await ctx.send(f"{winner.mention} has DMs off!")
        except:
            await ctx.send("No one else was in the Giveaway! :-(")

async def ch_pr():
    await client.wait_until_ready()
    statuses = ["Kicking and Banning Scrubs",
     '>help',
     f'{len(client.guilds)} servers'
     ]
    while not client.is_closed():
         status = random.choice(statuses)
         await client.change_presence(activity = discord.Streaming(name = status, url = "https://twitch.tv/kraken"))

         await asyncio.sleep(5)


client.loop.create_task(ch_pr())
client.run(BOT_TOKEN)
