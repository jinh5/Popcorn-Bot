import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Misc(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('misc.py is ready')

  @commands.command()
  async def sync(self, ctx):
    fmt = await ctx.bot.tree.sync(guild=ctx.guild)
    await ctx.send(f'Synced {len(fmt)} command(s)')

  @app_commands.command(name='help')
  async def help(self, interaction: discord.Interaction):
    embed_message = discord.Embed(title='Help Desk for Popcorn Bot', description='List of all commands for Popcorn Bot. Note: all film entries will be added to a master list of films.')
    embed_message.add_field(name='createlist [name]', value='Create a new list', inline=False)
    embed_message.add_field(name='addfilm [title]', value='Adds a film to the master list', inline=False)
    embed_message.add_field(name='add [film title] [list name]', value='Add a film to the specified list', inline=False)
    embed_message.add_field(name='lists', value='View all the lists that have been created', inline=False)
    embed_message.add_field(name='viewlist [list name]', value='View all films in the specified list', inline=False)
    embed_message.add_field(name='viewmisc', value='View all films that are not in lists', inline=False)
    embed_message.add_field(name='status [film title]', value='See if a film has been watched', inline=False)
    embed_message.add_field(name='editlist [original name] [new name]', value='Edit the name of a list', inline=False)
    embed_message.add_field(name='editfilm [original title] [new title]', value='Edit the title of a film', inline=False)
    embed_message.add_field(name='setstatus [film title]', value='Mark the watch status of a film from not watched to watched and vice versa', inline=False)
    embed_message.add_field(name='deletelist [name]', value='Delete the specified list', inline=False)
    embed_message.add_field(name='deletefilm [title]', value='Delete the specified film', inline=False)
    embed_message.add_field(name='delete [film title] [list name]', value='Delete a film from the specified list', inline=False)
    await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Misc(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])