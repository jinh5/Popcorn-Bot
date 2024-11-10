import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Films_and_Lists(commands.Cog):
  '''Commands for organizing films & lists'''
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('filmsandlists.py is ready') 

  '''
  @app_commands.command(name='')
  async def (self, interaction: discord.Interaction):
    await self.client.db.execute(
    )
    embed_message = discord.Embed()
    embed_message.add_field(name='', value='')
    await interaction.response.send_message(embed=embed_message)
  '''

  @app_commands.command(name='createlist', description='Create a new list')
  async def createlist(self, interaction: discord.Interaction, name: str):
    name_str = ''.join(name)

    await self.client.db.execute(
      'INSERT INTO lists(list_name) VALUES ($1)',
      name_str
    )

    embed_message = discord.Embed()
    embed_message.add_field(name='', value='**'+ name_str +'** has been created', inline=False)
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='addfilm', description='Adds a film to the master list')
  async def add(self, interaction: discord.Interaction, title: str):
    title_str = ''.join(title)

    await self.client.db.execute(
      'INSERT INTO films(title) VALUES ($1)',
      title_str
    )

    embed_message = discord.Embed()
    embed_message.add_field(name='', value='**'+ title_str +'** has been added to the film master list', inline=False)
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='addfilmtolist', description='Adds a film to the specified list')
  async def addfilmtolist(self, interaction: discord.Interaction, filmtitle: str, listname: str):
    filmtitle_str = ''.join(filmtitle)
    listname_str = ''.join(listname)

    await self.client.db.execute(
      '''
      INSERT INTO lists_films(list_id, film_id)
      VALUES (
        (SELECT list_id FROM lists WHERE list_name=($1)),
        (SELECT film_id FROM films WHERE title=($2))
      )
      ''',
      listname_str, filmtitle_str 
    )
    embed_message = discord.Embed()
    embed_message.add_field(name='', value='**'+filmtitle_str+'** has been added to **'+listname_str+'**', inline=False)
    await interaction.response.send_message(embed=embed_message)

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
  await client.add_cog(Films_and_Lists(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])