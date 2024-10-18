import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

def main():
  load_dotenv()
  intents = discord.Intents.default()  
  intents.message_content = True
  client = commands.Bot(command_prefix='$', intents=intents)
  token = os.getenv('TOKEN')

  @client.event
  async def on_ready():
    print(f"{client.user.name} has connected to Discord")

  @client.command()
  async def createlist(ctx):
    """Create a new list"""
    pass

  @client.command()
  async def lists(ctx):
    """View all lists"""
    pass

  @client.command()
  async def add(ctx):
    """Add a movie/tv show to a list"""
    pass

  @client.command()
  async def remove(ctx):
    """Remove a movie/tv show from a list"""
    pass

  client.run(token)

if __name__ == '__main__':
  main()