import discord
from discord.ext import commands

class Help(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print("help.py is ready")

  @commands.command()
  async def help(self, ctx):
    help_embed = discord.Embed(title="Help Desk for Popcorn Bot", description="List of all commands for Popcorn Bot. Note: all entries will be documented in a master list containing everything. An entry may only be categorized under one specified list.")

    help_embed.add_field(name="add [entry name]", value="Add a new entry to the master list", inline=False)
    help_embed.add_field(name="add [entry name] [list name]", value="Add a new entry to the specified list", inline=False)
    help_embed.add_field(name="remove [entry name]", value="Remove an entry from the master list", inline=False)
    help_embed.add_field(name="remove [entry name] [list name]", value="Remove an entry from the specified list", inline=False)
    help_embed.add_field(name="move [entry name] [list 1] [list 2]", value="Move an entry from list 1 to list 2", inline=False)
    help_embed.add_field(name="viewlists", value="View the names of all the lists", inline=False)
    help_embed.add_field(name="view [list name]", value="View all entries in the specified list", inline=False)
    help_embed.add_field(name="changewatchstatus [entry name]", value="Change the status of an entry from unwatched to watched and vice versa", inline=False)

    await ctx.send(embed = help_embed)

async def setup(client):
  await client.add_cog(Help(client))