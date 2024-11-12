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
    if len(data)==0:
      embed_message.add_field(name='', value='No lists have been created')
    else:
      embed_message = discord.Embed(title='Lists')
      for row in data:
        embed_message.add_field(name='', value=row['list_name'], inline=False)
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='viewlist', description='View all films in the specified list')
  #check if list exists first
  async def viewlist(self, interaction: discord.Interaction, listname: str):
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
      listname
    )
    
    embed_message = discord.Embed()
    embed_message = discord.Embed(title=listname)
    if len(data)==0:
      embed_message.add_field(name='', value='No entries in this list')
    else:
      for row in data:
        embed_message.add_field(name='', value=row['title'], inline=False)
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='viewuncategorized', description='View all films that are not in lists')
  async def viewuncategorized(self, interaction: discord.Interaction):
    data = await self.client.db.fetch(
      '''
      SELECT title 
      FROM films 
      WHERE NOT EXISTS (
        SELECT 
        FROM lists_films
        WHERE film_id = films.film_id
      );
      ''')

    embed_message = discord.Embed()
    if len(data)==0:
      embed_message.add_field(name='', value='There are no uncategorized films')
    else:
      embed_message = discord.Embed(title='Uncategorized')
      for row in data:
        embed_message.add_field(name='', value=row['title'], inline=False)
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='watchstatus', description='See if a film has been watched')
  async def watchstatus(self, interaction: discord.Interaction, filmtitle: str):
    data = await self.client.db.fetch(
      '''
      SELECT watch_status
      FROM films
      WHERE title=($1);
      ''',
      filmtitle
    )

    embed_message = discord.Embed()
    if data[0]['watch_status']==False:
      embed_message.add_field(name='', value='**'+filmtitle+'** has not been watched yet')
    elif data[0]['watch_status']==True:
      embed_message.add_field(name='', value='**'+filmtitle+'** has been watched')
    await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Read(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])