from dotenv import load_dotenv

from discord.ext import commands, tasks

import psycopg
import os

class Database(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.db_uri=os.getenv("DB_URI")

    async def cog_load(self):
        await self.migrate_schema()

    def get_conn(self):
        return psycopg.AsyncConnection.connect(self.db_uri)

    async def execute_statement(self,statements,*args,**kwargs):

        async with await self.get_conn() as conn:
            async with conn.cursor() as cur:
                for statement in statements:
                    await cur.execute(statement,*args,**kwargs)

    async def get_query_results(self,query):
        
        async with await self.get_conn() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query)
                query_results = await cur.fetchall()
                return query_results
                   

    async def migrate_schema(self):
        
        statements=[
            "CREATE SCHEMA IF NOT EXISTS discord_events",
            """
                CREATE TABLE IF NOT EXISTS discord_events.events (
                    id bigint,
                    name text,
                    start_date timestamp without time zone,
                    end_date timestamp without time zone,
                    channel_id bigint
                )
            """]

        await self.execute_statement(statements)
                
async def setup(bot):
    await bot.add_cog(Database(bot))
