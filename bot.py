# bot.py
import asyncio
import os
import discord
from dotenv import load_dotenv
import re
import CourseOpenings

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')


@client.event
async def on_message(message):
    content = message.content
    if re.search(r'^c!request \d{5}$', content):
        crn = re.findall(r'\d{5}', content)[0]
        await message.channel.send(f'Tracking CRN: {crn}')
        output = await CourseOpenings.show_course_status(message, crn)
        attempts = 1
        while 'CLOSED' in output:
            attempts += 1
            await message.channel.send(f'Tracking CRN: {crn} Attempt {attempts} in approximately one minute')
            await asyncio.sleep(60)
            output = await CourseOpenings.show_course_status(message, crn)
        if attempts != 1:
            await message.channel.send(f'CRN: {crn} is OPEN <@{message.author.id}>')
        await message.channel.send('Closing request. Thanks for using Course Openings Bot!')
    # Add elif for Course Subject (Space) Number
    # Add elif for Invalid crn but has c!request
    # elif re.search('^c!clearall$', content):
    #     await message.channel.send('Clearing all active requests!')
    #     CourseOpenings.close_all()
    elif re.search('^c!hi$', content):
        await message.channel.send('Greetings nerd!')


client.run(TOKEN)
