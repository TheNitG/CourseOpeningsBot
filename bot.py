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
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("Listening to c!help"))
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
    elif content == 'c!help':
        await build_embed()
    elif content == 'c!invite':
        await message.channel.send('Bot invite link: https://discord.com/api/oauth2/authorize?client_id'
                                   '=805551570342117417&permissions=355392&scope=bot')
    elif content == 'c!hi':
        await message.channel.send('Greetings nerd!')


async def build_embed():
    embed = discord.Embed(title='You have reached help!',
                          description='Welcome to Course Openings Bot! A free alternative to those paid '
                                      'course-trackers you might be throwing away money into.',
                          color=0x109319)

    embed.set_author(name='Course Openings Bot',
                     icon_url="https://pbs.twimg.com/profile_images/1327036716226646017/ZuaMDdtm_400x400.jpg")

    embed.set_thumbnail(url='https://hr.vt.edu/content/dam/hr_vt_edu/_images/HokieBird.jpg.transform/l-medium/image.jpg')

    embed.add_field(name='Track a course', value='Use "c!request" without the quotes and CRN being the 5 digit '
                                                 'CRN of the course you want to track. It will keep checking until '
                                                 'the course is open and will tag you when the course is open. Yes, '
                                                 'you can track multiple courses at once.',
                    inline=False)
    embed.add_field(name='Magic command', value='Use "c!hi" without the quotes for a surprise :open_mouth:.',
                    inline=False)
    embed.add_field(name='Invite link to bring the bot to your own server', value='Use "c!invite" without the quotes '
                                                                                  'to get the invite link to invite '
                                                                                  'Course Openings Bot to your own '
                                                                                  'server', inline=False)
    embed.add_field(name='SECRET', value='Who knows what is supposed to go here :smirk:.', inline=False)

    embed.set_footer(text='Thanks for using Course Openings Bot!')


client.run(TOKEN)
