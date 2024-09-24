import os
import re
import datetime
from datetime import timedelta

import discord
from discord.ext import commands, tasks
from discord.utils import get


from dotenv import load_dotenv

load_dotenv()

guild_id = int(os.getenv('GUILD_ID'))

intents = discord.Intents.all()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix ='?',intents=intents)        

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
    """Print the scheduled events for the next 7 days"""

    events = [ctx.guild.get_scheduled_event(id) for id in [event.id for event in ctx.guild.scheduled_events]]

    date_range = [datetime.datetime.today().date()+timedelta(1) + datetime.timedelta(days=x) for x in range(7)]

    upcoming_events=[event.url for event in events if event.start_time.date() in date_range]

    message = []

    if len(upcoming_events) == 0:
        message.append("No Events This Week!!!")
    else:
        message.append("##  BEHOLD!\n ## This week's events.. \n\n\n")
        for event in upcoming_events:
            message.append(event)
    
    await ctx.send("\n".join([m for m in message]),suppress_embeds=True)

bot.run(os.getenv('DISCORD_TOKEN'))

