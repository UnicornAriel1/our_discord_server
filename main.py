import os
import re
from datetime import datetime, timedelta

import discord
from discord.ext import commands, tasks
from discord.utils import get
from discord.utils import get

from dotenv import load_dotenv

load_dotenv()

guild_id = int(os.getenv('GUILD_ID'))

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = discord.Client(command_prefix ='?',intents=intents)


def convert_to_channel_name(event_name):
    """ Helper function that takes a string name of an event and returns how it has to be formatted for a channel name"""
    channel_name = re.sub(r'[^a-z0-9\-]','',event_name.replace(' ','-').lower())
    return channel_name

@bot.event
async def on_scheduled_event_create(event): 
    """ 
    When an event is created, create a text channel and add the event creator to it.
    requires Intents.guild_scheduled_events and manage_channels to be enabled
    """
    # requires Intents.guild_scheduled_events to be enabled
    # requires manage_channels
    print("a new event has been created!")
    guild = event.guild
    overwrites = {
        bot.user: discord.PermissionOverwrite(read_messages=True,
    send_messages=True, read_message_history = True, view_channel=True),
        event.creator: discord.PermissionOverwrite(read_messages=True,
    send_messages=True, read_message_history = True, view_channel=True)
    }
    category = get(guild.categories, name="Events")
    await guild.create_text_channel(event.name,category=category)
    
 

@bot.event
async def on_scheduled_event_user_add(event,user):
    """ 
    When a user is added to the event, add the user to the event's text channel.
    """

    guild = event.guild
    channel_name = convert_to_channel_name(event.name)

    channel = get(guild.channels,name=channel_name)

    if user in channel.members:
        print("user already in channel")
        return
    else:
        viewer_permissions = {
            "read_message_history":True,
            "read_messages":True,
            "send_messages":True,
            "view_channel":True
        }

        await channel.set_permissions(user, **viewer_permissions)


@bot.command()
async def get_guild_events(ctx):
    #TODO add arguments for start date and number of days to list
    
    all_events = ctx.guild.scheduled_events

    event_ids = [event.id for event in ctx.guild.scheduled_events]

    events = [ctx.guild.get_scheduled_event(id) for id in event_ids]

    print_date = datetime.today().date()+timedelta(1)

    message = []

    message.append("##  BEHOLD!\n ## This week's events.. \n\n\n")
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

