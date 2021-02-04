#hornyBot.py
#Created by Ben Briles
#Do whatever the fuck you want with this code
#If you find a way to make money off of it or something then more power to you

import os
import random
import discord
from discord.ext import commands
import discord.utils
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

#INVOKE THE BOT
bot = commands.Bot(command_prefix = '!')

#define the ever-growing list of horny words that will result in a warning from hornyBot
horny_words = ['sex', 'fuck', 'sexy', 'suck', 'dick', 'ass', 'butt', 'fucking', 'horny', 'hot', 'hawt', 'hard', 'wet', 'thirsty', 'fucked', 'nail', 'nailed']

#define the dictionary that will be used to automatically imprison users when their number is up
warned_users = {}

#create the !imprison commands, which allows users to place other users into Horny Jail when they're being horny
@bot.command(pass_context=True)
async def imprison(ctx, *, user: discord.Member):
    #specify which guild characteristics the bot will search (current guild)
    guild = ctx.guild
    #capture and define the HornyJail role so that it can be assigned to users
    role = discord.utils.get(guild.roles, name='HornyJail')
    #stops users from putting hornyBot in jail
    if user.display_name == 'hornyBot':
        await ctx.send('I\'m a god. How can you kill a god?')
        return
    #check to see if the user in question is already in Horny Jail, and if they are, send a message informing everyone that they are already imprisoned
    if role in user.roles:
        await ctx.send(f'{user.display_name} is already being punished for their horny sins.')
    #if user is not in Horny Jail, they are placed there swiftly and effectively
    else:
        await user.add_roles(role)
        await ctx.send(f'{ctx.author.display_name} has put {user.display_name} in Horny Jail.')

#create the !free command, which allows users to free others from Horny Jail. Users are not able to free themselves from Horny Jail.
@bot.command(pass_context=True)
async def free(ctx, *, user: discord.Member):
    #specify which guild characteristics the bot will search (current guild)
    guild = ctx.guild
    #capture and define the HornyJail role so that it can be assigned to users
    role = discord.utils.get(guild.roles, name='HornyJail')

    #checks to see if the user that invoked the !free command is trying to free themselves, which is not allowed.
    if user.id == ctx.author.id:
        await ctx.send('What, you think you can break your way out of here? You will be released when you\'ve learned to control your carnal instincts.')
        return
    #check to see if user is in Horny Jail. if they aren't, a message is displayed explaining that they cannot be freed if they are not imprisoned for horny crimes
    if role not in user.roles:
        await ctx.send(f'We haven\'t caught {user.display_name} being horny... yet.')
    #if a user has done their time (or if another user bails them out), they are promptly released from Horny Jail
    else:
        await user.remove_roles(role)
        await ctx.send(f'{ctx.message.author.display_name} has absolved {user.display_name} of their horny crimes!')


#creates the !warn command, which allows users to inform other users that their horniness is not going unnoticed and that if it continues, it will not go unpunished.
@bot.command(pass_context=True)
async def warn(ctx, *, user: discord.Member):
    #define the list of warnings that the user in question may be presented with
    warning_list = [
    f'Careful, {user.display_name}... you\'re being awful horny.',
    f'You\'re getting within bonk distance, {user.display_name}',
    f'Keep it in your pants, {user.display_name}.',
    f'Chasteness is next to godliness, {user.display_name}.',
    f'"Hard ons" get "hard no\'s" from me, {user.display_name}.',
    f'ur fixin to get bonked {user.display_name}',
    f'This is horny-free zone, {user.display_name}.',
    f'Keep talking like that and you\'ll end up with a one-way ticket to the horny slammer, {user.display_name}.',
    f'Thou shalt not desire to copulate, {user.display_name}.',
    f'{user.display_name} you need to COOL IT.',
    ]
    #sends a randomly-chosen message informing the warned user to check themselves
    await ctx.send(random.choice(warning_list))

#creates the !about command which tells everybody the virtures of hornyBot and instructs them on how to invoke this most righteous crusader
@bot.command(pass_context=True)
async def about(ctx):
    await ctx.send("""```Welcome to hornyBot!

    Here are the commands that you can use to keep things holy in your good Christian Discord server:

    !imprison <user> - puts a user in Horny Jail, where they will remain until freed

    !free <user> - releases a user from Horny Jail. Remember, you can put yourself in Horny Jail, but you can't let yourself out ;)

    !warn <user> - Think someone is getting a little too hot under the collar? Let them know that their actions are not above reproach and that hornyBot will bonk them if need be```""")

#informs everyone that hornyBot is here to put an end to their sexual impulses
@bot.event
async def on_ready():
    print('hornyBot is here to crack some heads')

#instructs the bot to monitor the content of each message that gets sent to the chat and issue a warning to users that appear to be getting horny
@bot.event
async def on_message(message):
    #tells the bot to pay attention to commands before trying to do anything with the message content
    await bot.process_commands(message)
    guild = message.guild
    role = discord.utils.get(guild.roles, name='HornyJail')
    channel = message.channel
    #redefines the list of warnings that can be given since there are slight differences in how the user is referred to. (I'm sure there's a better way to do this, but I don't know what it is)
    warning_list = [
    f'Careful, {message.author.display_name}... you\'re being awful horny.',
    f'You\'re getting within bonk distance, {message.author.display_name}',
    f'Keep it in your pants, {message.author.display_name}.',
    f'Chasteness is next to godliness, {message.author.display_name}.',
    f'"Hard ons" get "hard no\'s" from me, {message.author.display_name}.',
    f'ur fixin to get bonked {message.author.display_name}',
    f'This is horny-free zone, {message.author.display_name}.',
    f'Keep talking like that and you\'ll end up with a one-way ticket to the horny slammer, {message.author.display_name}.',
    f'Thou shalt not desire to copulate, {message.author.display_name}.',
    f'{message.author.display_name} you need to COOL IT.',
    ]
    #creates a variable that holds the random number that determines whether or not this code will proc. Higher numbers = smaller chance and vice versa
    chance = random.randrange(4)

    #keep the bot from replying to itself (not that it ever should).
    if message.author == bot.user:
        return


    #checks to see if this code will execute at all. If it does, it will scan the content of the message to see if there are horny words in it. if there are, a warning is issued to the user
    if chance == 1 and role not in message.author.roles:
        if any(word in message.content.lower() for word in horny_words):
            await message.channel.send(random.choice(warning_list))
            #code that will put users in horny jail automatically if they have been warned twice previously previously
            if  message.author.display_name not in warned_users:
                warned_users[message.author.display_name] = 1
                #outputs warned users to shell just for fun
                print(warned_users)
                return
            else:
                warned_users[message.author.display_name] = warned_users[message.author.display_name] + 1
                if (warned_users[message.author.display_name] % 3) == 0:
                    await message.author.add_roles(role)
                    print(warned_users)
                    await channel.send(f'That\'s it, {message.author.display_name}! You\'ve popped your last boner!!')
                    return
        else:
            return

#RUNS THE BOT
bot.run(TOKEN)