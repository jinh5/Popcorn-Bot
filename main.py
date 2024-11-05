import os
import discord
from bot import Bot
from dotenv import load_dotenv
from asyncio import run
from asyncpg import create_pool

load_dotenv()

async def main():
  async with create_pool(
    host=os.getenv('HOST'),
    database=os.getenv('DATABASE'),
    port=os.getenv('PORT'),
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD')
  ) as pool:
      intents = discord.Intents.default()  
      intents.message_content = True
      async with Bot(
        db=pool,
        command_prefix='$',
        intents=intents,
        application_id = os.getenv('APPLICATION_ID')
      ) as bot:
        intents.message_content = True
        await bot.start(token=os.getenv('TOKEN'))

if __name__ == '__main__':
  run(main())