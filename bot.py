import os
from discord.ext import commands
from asyncpg import Pool

class Bot(commands.Bot):
  def __init__(self, db: Pool, **kwargs):
    super().__init__(**kwargs)
    self.db=db

  async def setup_hook(self):
    self.remove_command('help')
    
    for filename in os.listdir("./cogs"):
      if filename.endswith(".py"):
        await self.load_extension(f"cogs.{filename[:-3]}")

      async with self.db.acquire() as conn:
        with open('./sql/schemas.sql','r') as sql:
          await conn.execute(sql.read())

  async def on_ready(self):
    print(f"{self.user.name} has connected to Discord")
    
