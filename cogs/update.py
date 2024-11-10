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

  @app_commands.command(name='editlistname', description='Edit the name of a list')
  async def editlistname(self, interaction: discord.Interaction, originalname: str, newname: str):
    originalname_str = ''.join(originalname)
    newname_str = ''.join(newname)
    await self.client.db.execute(
      '''
      UPDATE lists
      SET list_name = ($1)
      WHERE list_name = ($2)
      ''',
      newname_str, originalname_str
    )
    embed_message = discord.Embed()
    embed_message.add_field(name='', value='**'+originalname_str+'** has been renamed to **'+newname_str+'**')
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='editfilmtitle', description='Edit the title of a film')
  async def editfilmtitle(self, interaction: discord.Interaction, originaltitle: str, newtitle: str):
    originaltitle_str = ''.join(originaltitle)
    newtitle_str = ''.join(newtitle)
    await self.client.db.execute(
    '''
      UPDATE films
      SET title = ($1)
      WHERE title = ($2)
      ''',
      newtitle_str, originaltitle_str
    )
    embed_message = discord.Embed()
    embed_message.add_field(name='', value='**'+originaltitle_str+'** has been renamed to **'+newtitle_str+'**')
    await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Update(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])