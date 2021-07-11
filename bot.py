# bot.py
import asyncio
import os
import re

import discord
from dotenv import load_dotenv

import CourseOpenings
import Stocks
import Sudoku
import Tictactoe

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

client = discord.Client()

tictactoe_games = []


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Listening to c!help"))
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    content = message.content
    if re.search(r'^c!request \d{5}$', content):
        crn = re.findall(r'\d{5}', content)[0]
        await message.channel.send(f'Tracking CRN: {crn} for {message.author.name}')
        output = await CourseOpenings.show_course_status(message, crn)
        attempts = 1
        while 'CLOSED' in output:
            attempts += 1
            await message.channel.send(f'Tracking CRN: {crn} Attempt {attempts} for {message.author.name}')
            output = await CourseOpenings.show_course_status(message, crn)
        if attempts != 1:
            await message.channel.send(f'CRN: {crn} is OPEN <@{message.author.id}>')
        await message.channel.send('Closing request. Thanks for using Course Openings Bot!')
    # Add elif for Course Subject (Space) Number
    # elif re.search('^c!clearall$', content):
    #     await message.channel.send('Clearing all active requests!')
    #     CourseOpenings.close_all()
    elif re.search(r'^c!request', content):
        await message.channel.send('Not proper usage of c!request, please use the format "c!request XXXXX".')
    elif re.search(r'^c!stock \w{1,5}', content):
        ticker = re.search(r'^c!stock (\w+)', content)[1]
        try:
            await Stocks.plot_stock(message, ticker)
        except:
            await message.channel.send('Not a valid stock ticker, please try a valid stock ticker')
    elif content == 'c!tictactoe' or content == 'c!ttt':
        if message.author.id not in tictactoe_games:
            tictactoe_games.append(message.author.id)

            def check(react, usr):
                if usr == message.author and react.message.channel == message.channel:
                    return str(react.emoji) == '🇽' or str(react.emoji) == '🇴'
                return False

            try:
                turn_choose = await message.channel.send('What am I playing, X or O?')
                await turn_choose.add_reaction('🇽')
                await turn_choose.add_reaction('🇴')
                reaction, user = await client.wait_for('reaction_add', check=check, timeout=30)  # 30 seconds to react
                await Tictactoe.run_game(message, client, '.' * 9, 'X' if str(reaction.emoji) == '🇽' else 'O')
                tictactoe_games.remove(message.author.id)
            except asyncio.TimeoutError:
                await message.channel.send("Sorry, you didn't reply in time! Try c!tictactoe or c!ttt again!")
                tictactoe_games.remove(message.author.id)
                return
    elif re.search(r'^c!sudoku (?:\w|\d|.)+$', content):
        puzzle = content[9:]
        try:
            await Sudoku.sudoku_solve(message, puzzle)
        except:
            await message.channel.send('Not a valid puzzle, please try a valid puzzle')
    elif content == 'c!help':
        await build_embed(message)
    elif content == 'c!invite':
        await message.channel.send('Bot invite link: https://discord.com/api/oauth2/authorize?client_id'
                                   '=805551570342117417&permissions=355392&scope=bot')
    elif content == 'c!hi':
        await message.channel.send('Greetings nerd!')


async def build_embed(message):
    embed = discord.Embed(title='You have reached help!',
                          description='Welcome to Course Openings Bot! A free alternative to those paid '
                                      'course-trackers you might be throwing away money into.',
                          color=discord.Color.blue())

    embed.set_author(name='Course Openings Bot',
                     icon_url='https://www.hr.vt.edu/content/hr_vt_edu/en/working-at-vt/welcome-to-vt/_jcr_content'
                              '/article-image.transform/m-medium/image.jpg')

    embed.set_thumbnail(
        url='https://hr.vt.edu/content/dam/hr_vt_edu/_images/HokieBird.jpg.transform/l-medium/image.jpg')

    embed.add_field(name='Track a course', value='Use "**c!request CRN**" without the quotes and CRN being the 5 digit '
                                                 'CRN of the course you want to track. It will keep checking until '
                                                 'the course is open and will tag you when the course is open. Yes, '
                                                 'you can track multiple courses at once.', inline=False)
    embed.add_field(name='Track a stock over a 1-day period', value='Use "**c!stock TICKR**" without the quotes and '
                                                                    'TICKR being the 1 to 5 character stock ticker '
                                                                    'for the stock you want to track. Note: Not '
                                                                    'case-sensitive', inline=False)
    embed.add_field(name='Play tic-tac-toe against an AI!', value='Use "**c!tictactoe** or **c!ttt**" without the quote'
                                                                  's and input when asked to play tic-tac-toe against a'
                                                                  'n AI ', inline=False)
    embed.add_field(name='Use the bot to solve sudoku puzzles very quickly!', value='Use "**c!sudoku PUZZLE** without'
                                                                                    'the quotes and PUZZLE being the'
                                                                                    'sudoku puzzle to solve (Note: use'
                                                                                    '"." without the quotes for'
                                                                                    'empty/blank spaces',
                    inline=False)
    embed.add_field(name='Magic command', value='Use "**c!hi**" without the quotes for a surprise :open_mouth:.',
                    inline=False)
    embed.add_field(name='Invite link to bring the bot to your own server', value='Use "**c!invite**" without the '
                                                                                  'quotes to get the invite link to '
                                                                                  'invite Course Openings Bot to your '
                                                                                  'own server', inline=False)
    embed.add_field(name='SECRET', value='Who knows what is supposed to go here :smirk:.', inline=False)

    embed.set_footer(text='Thanks for using Course Openings Bot!')

    await message.channel.send(embed=embed)


client.run(TOKEN)
