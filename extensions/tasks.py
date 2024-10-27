import datetime
import os
from dotenv import load_dotenv

from discord.ext import commands, tasks
from discord import errors

utc = datetime.timezone.utc

load_dotenv()

# If no tzinfo is given then UTC is assumed.
time = datetime.time(hour=3, minute=0, tzinfo=utc)

class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.post_upcoming_events.start()
        self.delete_past_events.start()

    def cog_unload(self):
        self.post_upcoming_events.cancel()
        self.delete_past_events.cancel()

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
    
    @tasks.loop(time=time)
    async def delete_past_events(self):
        """deletes events that have already happened"""

        try:
            await self.bot.load_extension('extensions.database')
        except Exception as e:
            print(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            print('**`SUCCESSFULLY LOADED EXTENSION`**')

        db=self.bot.get_cog('Database')

        past_event_channel_ids="""
            SELECT channel_id from discord_events.events where DATE_TRUNC('day',events.end_date) < DATE_TRUNC('day', current_timestamp); 
        """

        if db is not None:
            query_results = await db.get_query_results(past_event_channel_ids)

        if len(query_results) > 0:
            for result in query_results:
                try:
                    channel = await self.bot.fetch_channel(int(result[0]))
                except (errors.NotFound):
                    pass
                try:
                    await channel.delete()
                except (errors.NotFound):
                    pass

                await db.execute_statement(["DELETE FROM discord_events.events where channel_id = %s"],result)
    
async def setup(bot):
    await bot.add_cog(Tasks(bot))
   