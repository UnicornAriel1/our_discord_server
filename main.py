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

class MyBot(commands.Bot):

    async def load_cogs(self):
        for filename in os.listdir('./extensions'):
            if filename.endswith('.py'):
                await self.load_extension(f'extensions.{filename[:-3]}')
        
    async def setup_hook(self):
        await self.load_cogs()

bot = MyBot(command_prefix ='?',intents=intents)        

def convert_to_channel_name(event_name):
    """ Helper function that takes a string name of an event and returns how it has to be formatted for a channel name"""
    channel_name = re.sub(r'[^a-z0-9\-]','',event_name.replace(' ','-').lower())
    return channel_name

async def create_category_if_not_exists(category_name, guild):
    """ Creates a channel category if it doesn't already exist"""
    
    existing_category=get(guild.categories, name=category_name)

    if existing_category == None:
        await guild.create_category(name=category_name)
    else:
        return None

@bot.event
async def on_scheduled_event_create(event): 
    """When an event is created create a text channel, add the event creator to it, 
    and write a row to the database associating the channel and the event
    requires Intents.guild_scheduled_events and manage_channels to be enabled
    """
    # requires Intents.guild_scheduled_events to be enabled
    # requires manage_channels

    guild = event.guild
    category_name = 'Events'

    await create_category_if_not_exists(category_name,guild)

    category = get(guild.categories, name='Events')

    overwrites = {
        bot.user: discord.PermissionOverwrite(read_messages=True,
    send_messages=True, read_message_history = True, view_channel=True),
        event.creator: discord.PermissionOverwrite(read_messages=True,
    send_messages=True, read_message_history = True, view_channel=True),
        guild.default_role: discord.PermissionOverwrite(read_messages=False)
    }

    channel = await guild.create_text_channel(event.name,category=category,overwrites=overwrites)

    event_data = {  
                    "id": event.id,
                    "name": event.name,
                    "start_date": event.start_time,
                    "end_date": event.end_time,
                    "channel_id": channel.id,
                }

    insert_statement = ["""
        INSERT INTO discord_events.events (id, name, start_date, end_date, channel_id)
        VALUES (%(id)s, %(name)s, %(start_date)s, %(end_date)s, %(channel_id)s);
        """]

    db=bot.get_cog('Database')

    await db.execute_statement(insert_statement, event_data)
    
 

@bot.event
async def on_scheduled_event_user_add(event,user):
    """ 
    When a user is added to the event, add the user to the event's text channel.
    """

    guild = event.guild
    channel_name = convert_to_channel_name(event.name)

    channel = get(guild.channels,name=channel_name)

    if user in channel.members and not user.bot:
        return
    else:
        viewer_permissions = {
            "read_message_history":True,
            "read_messages":True,
            "send_messages":True,
            "view_channel":True
        }

        await channel.set_permissions(user, **viewer_permissions)

bot.run(os.getenv('DISCORD_TOKEN'))




