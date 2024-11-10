import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Read(commands.Cog):
  '''Commands for viewing and accessing data'''
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('read.py is ready') 

  @app_commands.command(name='viewlists', description='View all the lists that have been created')
  async def viewlists(self, interaction: discord.Interaction):
    data = await self.client.db.fetch(
      '''
      SELECT list_name
      FROM lists;
      '''
    )
    embed_message = discord.Embed()
    embed_message = discord.Embed(title='Lists')
    for row in data:
      embed_message.add_field(name='', value=row['list_name'], inline=False)
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='viewlist', description='View all films in the specified list')
  async def viewlist(self, interaction: discord.Interaction, listname: str):
    listname_str = ''.join(listname)
    data = await self.client.db.fetch(
      '''
      SELECT title
      FROM lists JOIN lists_films ON lists_films.list_id=lists.list_id JOIN films ON films.film_id=lists_films.film_id
      WHERE lists_films.list_id = (
        SELECT list_id
        FROM lists
        WHERE list_name = ($1)
      );
      ''',
      listname_str
    )
    embed_message = discord.Embed()
    embed_message = discord.Embed(title=listname_str)
    for row in data:
      embed_message.add_field(name='', value=row['title'], inline=False)
    await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Read(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])