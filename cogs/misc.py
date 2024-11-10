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
  async def sync(self, ctx) -> None:
    fmt = await ctx.bot.tree.sync(guild=ctx.guild)
    await ctx.send(f'Synced {len(fmt)} command(s)')

  @app_commands.command(name='help')
  async def help(self, interaction: discord.Interaction):
    embed_message = discord.Embed(title='Help Desk for Popcorn Bot', description='List of all commands for Popcorn Bot. Note: all entries will be documented in a master list containing everything.')
    embed_message.add_field(name='', value='', inline=False)
    embed_message.add_field(name='createlist [list name]', value='Create a new list', inline=False)
    embed_message.add_field(name='addfilm [film title]', value='Adds a film to the master list', inline=False)
    embed_message.add_field(name='add [film title] [list name]', value='Add a film to the specified list', inline=False)
    embed_message.add_field(name='viewlists', value='View all the lists that have been created', inline=False)
    embed_message.add_field(name='viewlist [list name]', value='View all films in the specified list', inline=False)
    embed_message.add_field(name='renamelist', value='Change the name of a list', inline=False)
    await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Misc(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])