import datetime
import os
from dotenv import load_dotenv

from discord.ext import commands, tasks

utc = datetime.timezone.utc

load_dotenv()

# If no tzinfo is given then UTC is assumed.
time = datetime.time(hour=3, minute=0, tzinfo=utc)

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.post_upcoming_events.start()

    def cog_unload(self):
        self.post_upcoming_events.cancel()

    @tasks.loop(time=time)
    async def post_upcoming_events(self):
        """posts upcoming events"""

        current_time = datetime.datetime.now()
        weekday = current_time.weekday()

        channel = self.bot.get_channel(int(os.getenv('CHANNEL_ID')))
        guild = self.bot.get_guild(int(os.getenv('GUILD_ID')))

        if weekday != 0:
            return # it is not monday (week day 0)
            # 0-6 -> monday -> sunday
        
        events = [guild.get_scheduled_event(id) for id in [event.id for event in guild.scheduled_events]]

        date_range = [datetime.datetime.today().date()+datetime.timedelta(1) + datetime.timedelta(days=x) for x in range(7)]

        upcoming_events=[event.url for event in events if event.start_time.date() in date_range]

        message = []

        if len(upcoming_events) == 0:
            message.append("No Events This Week!!!")
        else:
            message.append("##  BEHOLD!\n ## This week's events.. \n\n\n")
            for event in upcoming_events:
                message.append(event)
        
        await channel.send("\n".join([m for m in message]),suppress_embeds=True)
    
    
async def setup(bot):
    await bot.add_cog(Tasks(bot))
