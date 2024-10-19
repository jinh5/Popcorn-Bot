import discord
from discord.ext import commands

class Lists(commands.Cog):
  """Commands for organizing lists"""
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print("lists.py is ready")

  @commands.command()
  async def showlists(self, ctx):
    lists=["movie 1", "movie 2", "movie 3"]
    embed_message = discord.Embed(title="Lists:")
    embed_message.add_field(name="Movie List", value="\n".join(lists), inline=True)
    await ctx.send(embed = embed_message)

async def setup(client):
  await client.add_cog(Lists(client))