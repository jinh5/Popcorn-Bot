import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Films_and_Lists(commands.Cog):
  """Commands for organizing films & lists"""
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print("filmsandlists.py is ready") 

  @app_commands.command(name="createlist")
  async def createlist(self, interaction: discord.Interaction, name: str):
    join_name = ''.join(name)
    embed_message = discord.Embed()
    await self.client.db.execute(
      'INSERT INTO lists(list_name) VALUES ($1)',
      join_name
    )
    embed_message.add_field(name=join_name, value='has been created')
    await interaction.response.send_message(embed=embed_message)
      

async def setup(client):
  await client.add_cog(Films_and_Lists(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])