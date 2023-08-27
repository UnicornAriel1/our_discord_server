import os
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks

from dotenv import load_dotenv

load_dotenv()

#env variables
guild_id = int(os.getenv('GUILD_ID'))


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix = '?',intents=intents)

@bot.command()
async def get_guild_events(ctx):
    #TODO add arguments for start date and number of days to list

    guild = bot.get_guild(guild_id)
    all_events = guild.scheduled_events

    event_ids = [event.id for event in guild.scheduled_events]

    events = [guild.get_scheduled_event(id) for id in event_ids]

    print_date = datetime.today().date()+timedelta(1)

    message = []

    message.append("## It is I, Baphomet... Behold!\n ## This week's events.. \n\n\n")
    for day in range(7):

        if print_date in [event.start_time.date() for event in events]:

            formatted_date = print_date.strftime('%A %B %d')

            message.append(f" \n### {formatted_date}")  

            for event in events:
                if event.start_time.date() == print_date:
                    message.append(event.url)
            
        print_date = print_date+timedelta(1)

    await ctx.send("\n".join([m for m in message]),suppress_embeds=True)

bot.run(os.getenv('DISCORD_TOKEN'))

