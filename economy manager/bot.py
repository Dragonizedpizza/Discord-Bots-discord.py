import discord
from discord.ext import commands
import os
import random
import json
import asyncio

os.chdir("") #put your directory
client = commands.Bot(command_prefix = "e!", case_insensitive = True)

mainshop = [
{"name" : "Laptop", "price" : 5000, "description" : "Allows you to post memes and create businesses"},
{"name" : "PC", "price" : 20000, "description" : "Allows you to upload videos and make money!"},
{"name" : "Lock", "price" : 10000, "description" : "Pesky robbers stealing ya! Well this will make them fail 10 times!"}
]


@client.event
async def on_ready():
    print("Ready!")

@client.command()
async def support(ctx):
    await ctx.send("")

@client.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title = "You do not have the permissions!", color = discord.Color.purple())
        await ctx.send(embed = embed)
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title = "MissingRequiredArgument", color = discord.Color.purple())
        embed.add_field(name = "Missing Argument", value = "You put a missing argument which was required to execute the command!")
        await ctx.send(embed = embed)

@client.command()
async def invite(ctx):
    await ctx.send("The invite link:\nhttps://discordapp.com/oauth2/authorize?&client_id=768695035092271124&scope=bot&permissions=2147483383")

@client.remove_command('help')
@client.command()
async def help(ctx, command : str = None):
    if command == None:
        embed = discord.Embed(title = 'Help',description = "Write `help {command}` to know more!", color = discord.Color.purple())
        embed.add_field(name = "Commands:", value = "`Balance`, `Withdraw`, `Deposit`, `Slots`, `Rob`, `Serve`, `Bankrob`, `Dice`, `Shop`, `Buy`, `Sell`")
        embed.add_field(name = "Additional Commands", value = "`invite`, `botinfo`")
        await ctx.send(embed = embed)
    else:
        command = str(command)
        command = command.lower()

        if command == "balance":
            embed = discord.Embed(title = "Help Balance", color = discord.Color.purple())
            embed.add_field(name = "Balance:", value = 'Use this command to show your or others\' balance!')
            await ctx.send(embed = embed)
        elif command == "withdraw":
            embed = discord.Embed(title = "Help Withdraw", color = discord.Color.purple())
            embed.add_field(name = "Withdraw:", value = 'Use this command to withdraw money from the bank!')
            await ctx.send(embed = embed)
        elif command == "deposit":
            embed = discord.Embed(title = "Help Deposit", color = discord.Color.purple())
            embed.add_field(name = "Deposit:", value = 'Use this command to deposit your precious money!')
            await ctx.send(embed = embed)
        elif command == "slots":
            embed = discord.Embed(title = "Help Slots", color = discord.Color.purple())
            embed.add_field(name = "Slots:", value = 'Use this command to bet some money on slots')
            await ctx.send(embed = embed)
        elif command == "rob":
            embed = discord.Embed(title = "Help Rob", color = discord.Color.purple())
            embed.add_field(name = "Rob:", value = 'Use this command to simply rob someones\' wallet!' )
            await ctx.send(embed = embed)
        elif command == "serve":
            embed = discord.Embed(title = "Help Serve", color = discord.Color.purple())
            embed.add_field(name = "Serve:", value = 'If you **serve** the current **serve**r your in. You get money!!!')
            await ctx.send(embed = embed)
        elif command == "bankrob":
            embed = discord.Embed(title = "Help Bankrob", color = discord.Color.purple())
            embed.add_field(name = "Bankrob:", value = 'Rob peoples\' banks! ')
            await ctx.send(embed = embed)
        elif command == "dice":
            embed = discord.Embed(title = "Help Dice", color = discord.Color.purple())
            embed.add_field(name = "Dice:", value = 'Play a game of dice!')
            await ctx.send(embed = embed)
        elif command == "Shop":
            embed = discord.Embed(title = "Help Shop", color = discord.Color.purple())
            embed.add_field(name = "Shop:", value = 'See what\'s avalible to buy!')
            await ctx.send(embed = embed)
        elif command == "Buy":
            embed = discord.Embed(title = "Help Buy", color = discord.Color.purple())
            embed.add_field(name = "Buy:", value = 'Just buy an item in the shop')
            await ctx.send(embed = embed)
        elif command == "Sell":
            embed = discord.Embed(title = "Help Shop", color = discord.Color.purple())
            embed.add_field(name = "Sell:", value = 'Sell something that you bought earlier')
            await ctx.send(embed = embed)

mainshop = [
{"name" : "Computer", "price" : 10000, "description" : "The computer can post memes and make ya money!"},
{"name" : "Fishing Rod", "price" : 50000, "description" : "The fishing rod, can easily fish and make ya money!"},
{"name" : "Hunting Rifle", "price" : 100000, "description" : "Rifle can easily make you money!"}
]

@client.command(aliases = ["balance"])
async def bal(ctx, member : discord.Member = None):
    if member == None:
        member = ctx.author
    await open_account(member)
    user = member
    users = await get_bank_data()

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    embed = discord.Embed(title = f"{member.name}'s Balance", color = discord.Color.purple())
    embed.add_field(name = "Wallet Balance", value = wallet_amt)
    embed.add_field(name = "Bank Balance", value = bank_amt)

    await ctx.send(embed = embed)

@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def beg(ctx):

    await open_account(ctx.author)
    users = await get_bank_data()
    user = ctx.author

    wallet_amt = users[str(user.id)]["wallet"]
    bank_amt = users[str(user.id)]["bank"]

    list = ['money']
    reward_type = random.choice(list)
    if reward_type == "money":
        earnings = random.randint(0, 100)
        users[str(user.id)]["wallet"] += earnings

        with open("mainbank.json", "w") as f:
            json.dump(users, f)

        await ctx.send(f"Well you earned {earnings} coins")

@client.command(aliases = ["with"])
async def withdraw(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Type an amount")

    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount > bal[1]:
        await ctx.send("You can't withdraw more than you have in your bank!")
        return
    if amount <= 0:
        await ctx.send("Amount must be positive!")
    await update_bank(ctx.author, amount)
    await update_bank(ctx.author, -1*amount, "bank")
    await ctx.send(f"You withdrew {amount} coins from your bank")

@client.command(aliases = ["dep"])
async def deposit(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Type an amount")

    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount > bal[0]:
        await ctx.send("You can't deposit more than you have in your wallet!")
        return
    if amount <= 0:
        await ctx.send("Amount must be positive!")
    await update_bank(ctx.author, -1*amount)
    await update_bank(ctx.author,amount, "bank")
    await ctx.send(f"You deposited {amount} coins from your wallet into your bank")

@client.command()
@commands.cooldown(1, 20, commands.BucketType.user)
async def give(ctx, member : discord.Member, amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Type an amount")

    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount > bal[0]:
        await ctx.send("You don't even have that much money, lol")
        return
    if amount <= 0:
        await ctx.send("Amount must be positive!")
    await update_bank(ctx.author, -1*amount, "wallet")
    await update_bank(member,amount, "wallet")
    await ctx.send(f"You give {amount} coins from your wallet to {member.name}'s wallet")

@client.command()
@commands.cooldown(1, 10, commands.BucketType.user)
async def slots(ctx, amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Type an amount")

    amount = int(amount)
    bal = await update_bank(ctx.author)
    if amount > bal[0]:
        await ctx.send("You can't gamble more than you have in your wallet!")
        return
    if amount <= 0:
        await ctx.send("Amount must be positive!")

    final = []
    for i in range(0, 3):
        final.append(random.choice("🎃", "👻", "👾"))

    await ctx.send(final)

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        if final[0] == final[1] and final[1] == final[2]:
            await ctx.send("GRAND PRIZE")
            await update_bank(ctx.author, amount * 3, "wallet")
        else:
            await ctx.send("PRIZE!")
            await update_bank(ctx.author, amount * 2, "wallet")
    else:
        await ctx.send("YOU LOSE!!!")
        await update_bank(ctx.author, amount * -1, "wallet")

@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def serve(ctx):
    await open_account(ctx.author)
    earnings = random.randint(1, 1000)
    await update_bank(ctx.author, earnings)
    await ctx.send(f'You served {ctx.author.guild.name} and got {earnings} coins out of it')

@client.command()
@commands.cooldown(1, 500, commands.BucketType.user)
async def rob(ctx, member : discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    users = await get_bank_data()
    if users[str(user.id)]["wallet"] > 1000:
        a = random.randint(1, 100)
        if a <= 45:
            earnings = random.randint(100, users[str(member.id)]["wallet"])
            await ctx.send(f"You stole {earnings} coins from {member.mention}!")
            update_bank(ctx.author, earnings, "wallet")
            update_bank(member, -1*earnings, "bank")
        else:
            await ctx.send("Sorry you got caught!")
            update_bank(ctx.author, -1000, "wallet")
            update_bank(member, 2000, "bank")
    else:
        await ctx.send("You need 1,000 coin in your wallet to rob!")

@client.command()
async def shop(ctx):
    embed = discord.Embed(title = "Shop", color = discord.Color.purple())
    for item in mainshop:
        name = item["name"]
        price = item["price"]
        description = item["description"]
        embed.add_field(name = name, value = f"${prize} | {description}")
    await ctx.send(embed = embed)

@client.command()
async def buy(ctx, item, amount = 1):
    await open_account(ctx.author)
    result = await buy_this(ctx.author, item, amount)

    if not res[0]:
        if res[1] == 1:
            await ctx.send("Item not in shop!")
            return
        if res[1] == 2:
            await ctx.send("You don't have enough money in your wallet!")
            await ctx.send("**Handy Dandy Tip:**, join one of NightZan999's servers.\nSince there are a ton of giveaways, you might win one!")
            await ctx.send("https://discord.gg/ruQukRC")
            return
    await ctx.send(f"You just bought {amount} {item}")

@client.command()
async def sell(ctx,item,amount = 1):
    await open_account(ctx.author)
    res = await sell_this(ctx.author,item,amount)

    if not res[0]:
        if res[1]==1:
            await ctx.send("Item doesn't exist")
            return
        if res[1]==2:
            await ctx.send(f"You don't have {amount} {item} in your inventory.")
            return
        if res[1]==3:
            await ctx.send(f"You don't have {item} in your inventory.")
            return

    await ctx.send(f"You just sold {amount} {item}.")

@client.command(aliases = ["inv"])
async def inventory(ctx):
    await open_account(ctx.author)
    user = ctx.author
    users = await get_bank_data()

    try:
        bag = users[str(user.id)]["inventory"]
    except:
        bag = []

    embed = discord.Embed(title = 'Inventory', color = discord.Color.purple())
    for item in bag:
        name = item["item"]
        amount = item["amount"]
        embed.add_field(name = name, value = amount)
    await ctx.send(embed = embed)

@client.command()
@commands.cooldown(1, 1000, commands.BucketType.user)
async def bankrob(ctx, member : discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    users = await get_bank_data()
    if users[str(user.id)]["wallet"] > 10000:
        a = random.randint(1, 100)
        if a < 20:
            earnings = random.randint(100, users[str(member.id)]["bank"])
            await ctx.send(f"You stole {earnings} coins from {member.mention}!")
            update_bank(ctx.author, earnings, "wallet")
            update_bank(member, -1*earnings, "bank")
        else:
            await ctx.send("Sorry you got caught!")
            update_bank(ctx.author, -10000, "wallet")
            update_bank(member, 10000, "bank")
    else:
        await ctx.send("You need 10,000 coin in your wallet to bankrob!")

@client.command(aliases = ["lb"])
@commands.cooldown(1, 15, commands.BucketType.user)
async def leaderboard(ctx,x = 10):
    users = await get_bank_data()
    leader_board = {}
    total = []

    for user in users:
        name = int(user)
        total_amount = users[user]["wallet"] + users[user]["bank"]
        leader_board[total_amount] = name
        total.append(total_amount)

    total = sorted(total,reverse=True)

    em = discord.Embed(title = f"Top {x} Richest People" , description = "This is decided on the basis of raw money in the bank and wallet",color = discord.Color(0xfa43ee))
    index = 1
    for amt in total:
        id_ = leader_board[amt]
        member = client.get_user(id_)
        name = member.name
        em.add_field(name = f"{index}. {name}" , value = f"{amt}",  inline = False)
        if index == x:
            break
        else:
            index += 1
    await ctx.send(embed = em)


@client.command()
async def devwith(ctx, amount):
    if ctx.author.id == 575706831192719370:
        amount = int(amount)
        await open_account(ctx.author)
        user = ctx.author
        users = await get_bank_data()

        users[str(user.id)]["wallet"] += amount
        with open("mainbank.json", "w") as f:
            json.dump(users, f)

        await ctx.send(f"Gave you {amount} coins!")
    else:
        await ctx.send("Bruh, your not a bot dev!")

@client.command(aliases = ['pm'])
async def postmeme(ctx, item = "Laptop"):
    users = await get_bank_data()
    try:
        if "Laptop" in users[str(user.id)]["inventory"]:
            await ctx.send(f"You made {earnings} coins in 1 hour.")
            earnings = random.randint(2, 1000)
            users[str(user.id)]["wallet"] += earnings

            with open("mainbank.json", "w") as f:
                json.dump(users, f)

            await asyncio.sleep(60)

            earnings /= 2
            earnings = int(earnings)
            users[str(user.id)]["wallet"] += earnings

            with open("mainbank.json", "w") as f:
                json.dump(users, f)
        else:
            await ctx.send("You don't own a laptop!")
    except:
        await ctx.send("You don't own a laptop!")

#Helperfunctions
async def open_account(user):

    with open("mainbank.json", "r") as f:
        users = json.load(f)

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0 #I want them to get 100 coins
        users[str(user.id)]["bank"]  = 0

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)
    return users

async def update_bank(user, change = 0, mode = "wallet"):
    users = await get_bank_data()
    users[str(user.id)][mode] = users[str(user.id)][mode] + change

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    bal = users[str(user.id)]["wallet"], users[str(user.id)]["bank"]
    return bal

async def buy_this(user, item, amount):
    item_name = item_name.lower()
    name_ = None

    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            price = item["price"]

            break

    if name_ == None:
        return [False,  1]

    cost = price * amount
    users = await get_bank_data()

    bal = await update_bank(user)

    if bal[0] < cost:
        return [False, 2]

    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["inventory"]:
            n = thing["name"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt + amount
                users[str(user.id)]["inventory"][index][amount] = new_amt
                t = 1
                break
            index += 1
        if t == None:
            obj = {"item" : item_name, "amount" : amount}
            users[str(user.id)]["inventory"].append(obj)
    except:
        obj = {"item" : item_name, "amount" : amount}
        users[str(user.id)]["inventory"] = obj

    with open("mainbank.json", "w") as f:
        json.dump(users, f)

    await update_bank(user, cost * -1, "wallet")
    return True

async def sell_this(user,item_name,amount,price = None):
    item_name = item_name.lower()
    name_ = None
    for item in mainshop:
        name = item["name"].lower()
        if name == item_name:
            name_ = name
            if price==None:
                price = 0.9* item["price"]
            break

    if name_ == None:
        return [False,1]

    cost = price*amount

    users = await get_bank_data()

    bal = await update_bank(user)


    try:
        index = 0
        t = None
        for thing in users[str(user.id)]["inventory"]:
            n = thing["item"]
            if n == item_name:
                old_amt = thing["amount"]
                new_amt = old_amt - amount
                if new_amt < 0:
                    return [False,2]
                users[str(user.id)]["inventory"][index]["amount"] = new_amt
                t = 1
                break
            index+=1
        if t == None:
            return [False,3]
    except:
        return [False,3]

    with open("mainbank.json","w") as f:
        json.dump(users,f)

    await update_bank(user,cost,"wallet")
    return [True,"Worked"]

async def ch_pr():
    await client.wait_until_ready()
    statuses = ["The BEST way to make money",
     'e!help',
     f'Making businesses',
     'STONKS',
     f'{len(client.guilds)} servers',
     ]
    while not client.is_closed():
         status = random.choice(statuses)
         await client.change_presence(activity = discord.Streaming(name = status, url = "https://twitch.tv/kraken"))

         await asyncio.sleep(5)


client.loop.create_task(ch_pr())
client.run(BOT_TOKEN)
