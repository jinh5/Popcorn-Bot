import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import asyncio 

load_dotenv()
intents = discord.Intents.default()  
intents.message_content = True
client = commands.Bot(command_prefix='$', intents=intents)
token = os.getenv('TOKEN')

client.remove_command("help")

@client.event
async def on_ready():
  print(f"{client.user.name} has connected to Discord")

async def load():
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      await client.load_extension(f"cogs.{filename[:-3]}")

async def main():
  async with client:
    await load()
    await client.start(token)

asyncio.run(main())