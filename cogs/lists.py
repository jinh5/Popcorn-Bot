import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Lists(commands.Cog):
  """Commands for organizing lists"""
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print("lists.py is ready") 

  @app_commands.command(name="create")
  async def create(self, interaction: discord.Interaction, list_name: str):
    join_list_name = ''.join(list_name)
    await self.client.db.execute(
      'INSERT INTO lists(name) VALUES ($1)',
      list_name
    )
    embed_message = discord.Embed()
    embed_message.add_field(name=join_list_name, value='has been created')
    await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Lists(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])