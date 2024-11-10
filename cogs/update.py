import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Update(commands.Cog):
  '''Commands for editing and changing data'''
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('update.py is ready') 

  '''
  @app_commands.command(name='', description='')
  async def (self, interaction: discord.Interaction):
    await self.client.db.execute(
    )
    embed_message = discord.Embed()
    embed_message.add_field(name='', value='')
    await interaction.response.send_message(embed=embed_message)
  '''



async def setup(client):
  await client.add_cog(Update(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])