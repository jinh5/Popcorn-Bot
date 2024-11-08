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
    print("misc.py is ready")

  @commands.command()
  async def sync(self, ctx) -> None:
    fmt = await ctx.bot.tree.sync(guild=ctx.guild)
    await ctx.send(f'Synced {len(fmt)} command(s)')

  @app_commands.command(name="help")
  async def help(self, interaction: discord.Interaction):
    help_embed = discord.Embed(title="Help Desk for Popcorn Bot", description="List of all commands for Popcorn Bot. Note: all entries will be documented in a master list containing everything.")
    help_embed.add_field(name="create [list name]", value="Create a new list", inline=False)
    help_embed.add_field(name="add [entry name] [list name]", value="Add a new entry to the specified list", inline=False)
    help_embed.add_field(name="remove [entry name] [list name]", value="Remove an entry from the specified list (And the masterlist)", inline=False)
    help_embed.add_field(name="move [entry name] [list 1] [list 2]", value="Move an entry from list 1 to list 2", inline=False)
    help_embed.add_field(name="viewlists", value="View the names of all the lists", inline=False)
    help_embed.add_field(name="view [list name]", value="View all entries in the specified list", inline=False)
    help_embed.add_field(name="changewatchstatus [entry name]", value="Change the status of an entry from unwatched to watched and vice versa", inline=False)
    help_embed.add_field(name="help", value="Shows this command", inline=False)
    await interaction.response.send_message(embed=help_embed)

async def setup(client):
  await client.add_cog(Misc(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])