import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Delete(commands.Cog):
  '''Commands for editing and changing data'''
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('delete.py is ready') 

  '''
  @app_commands.command(name='', description='')
  async def (self, interaction: discord.Interaction):
    await self.client.db.execute(
    )
    embed_message = discord.Embed()
    embed_message.add_field(name='', value='')
    await interaction.response.send_message(embed=embed_message)
  '''

  @app_commands.command(name='deletelist', description='Delete the specified list')
  async def deletelist(self, interaction: discord.Interaction, name: str):
    #check if list exists before deleting
    await self.client.db.execute(
      '''
      DELETE FROM lists WHERE list_name = ($1)
      ''',
      name
    )

    embed_message = discord.Embed()
    embed_message.add_field(name='', value='Deleted **'+ name +'**')
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='deletefilm', description='Delete the specified film')
  async def deletefilm(self, interaction: discord.Interaction, title: str):
    #check if title exists before deleting
    await self.client.db.execute(
      '''
      DELETE FROM films WHERE title = ($1)
      ''',
      title
    )

    embed_message = discord.Embed()
    embed_message.add_field(name='', value='Deleted **'+ title +'**')
    await interaction.response.send_message(embed=embed_message)

  # @app_commands.command(name='delete', description='Delete a film from the specified list')
  # async def delete(self, interaction: discord.Interaction, filmtitle: str, listname: str):
  #   filmtitle_str = ''.join(filmtitle)
  #   listname_str = ''.join(listname)
    
  #   await self.client.db.execute(
  #     '''
  #     DELETE FROM films WHERE title = ($1)
  #     ''',
  #   )

  #   embed_message = discord.Embed()
  #   embed_message.add_field(name='', value='Deleted **'+  +'**')
  #   await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Delete(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])