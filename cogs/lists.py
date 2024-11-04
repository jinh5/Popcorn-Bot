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
  async def create(self, ctx, *name_input):
    list_name = ' '.join(name_input)
    await self.client.db.execute(
      'INSERT INTO lists(name) VALUES ($1)',
      list_name
    )
    embed_message = discord.Embed()
    embed_message.add_field(name=list_name, value='has been created')
    await ctx.send(embed = embed_message)

  # @commands.command()
  # async def add(self, ctx):
  #   embed_message = discord.Embed(title="Added entry")
  #   await ctx.send(embed = embed_message)

  # @commands.command()
  # async def remove(self, ctx):
  #   embed_message = discord.Embed(title="Removed entry")
  #   await ctx.send(embed = embed_message)

  # @commands.command()
  # async def move(self, ctx):
  #   embed_message = discord.Embed(title="Moved entry")
  #   await ctx.send(embed = embed_message)
  
  # @commands.command()
  # async def viewlists(self, ctx):
  #   embed_message = discord.Embed(title="")
  #   await ctx.send(embed = embed_message)

  # @commands.command()
  # async def view(self, ctx):
  #   embed_message = discord.Embed(title="")
  #   await ctx.send(embed = embed_message)

  # @commands.command()
  # async def changewatchstatus(self, ctx):
  #   embed_message = discord.Embed(title="")
  #   await ctx.send(embed = embed_message)

async def setup(client):
  await client.add_cog(Lists(client))