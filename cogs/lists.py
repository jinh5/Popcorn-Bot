import discord
from discord.ext import commands

class Lists(commands.Cog):
  """Commands for organizing lists"""
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print("lists.py is ready") 

async def setup(client):
  await client.add_cog(Lists(client))