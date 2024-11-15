import discord
import os
import asyncpg
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Create(commands.Cog):
  '''Commands for creating new data'''
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print('create.py is ready') 

  @app_commands.command(name='createlist', description='Create a new list')
  async def createlist(self, interaction: discord.Interaction, name: str):
    embed_message = discord.Embed()
    async with self.client.db.acquire() as connection:
      try:
        await connection.execute('INSERT INTO lists(list_name) VALUES ($1);', name)
        embed_message.add_field(name='', value='**'+ name +'** has been created')
      except asyncpg.UniqueViolationError:
        embed_message.add_field(name='ERROR', value='**'+name+'** list already exists!')
      finally:
        await self.client.db.release(connection)
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='addfilm', description='Adds a film to the master list')
  async def addfilm(self, interaction: discord.Interaction, title: str):
    embed_message = discord.Embed()
    async with self.client.db.acquire() as connection:
      try:
        await connection.execute('INSERT INTO films(title) VALUES ($1);', title)
        embed_message.add_field(name='', value='**'+ title +'** has been added to the film master list')
      except asyncpg.UniqueViolationError:
        embed_message.add_field(name='ERROR', value='**'+title+'** already exists in the film master list!')
      finally:
        await self.client.db.release(connection)
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='add', description='Adds a film to the specified list')
  async def add(self, interaction: discord.Interaction, filmtitle: str, listname: str):
    embed_message = discord.Embed()
    async with self.client.db.acquire() as connection:
      try:
        await connection.execute(
          '''
          INSERT INTO films(title)
          SELECT ($1)
          WHERE
            NOT EXISTS (
              SELECT film_id from films WHERE title = ($2)
            );
          ''',
          filmtitle, filmtitle
        )
        await connection.execute(
          '''
          INSERT INTO lists_films(list_id, film_id)
          VALUES (
            (SELECT list_id FROM lists WHERE list_name=($1)),
            (SELECT film_id FROM films WHERE title=($2))
          );
          ''',
          listname, filmtitle 
        )
        embed_message.add_field(name='', value='**'+filmtitle+'** has been added to **'+listname+'** list')
      except asyncpg.NotNullViolationError:
        embed_message.add_field(name='ERROR', value='**'+listname+'** list does not exist!')
      except asyncpg.UniqueViolationError:
        embed_message.add_field(name='ERROR', value='**'+filmtitle+'** is already in **'+listname+'** list!')
      finally:
        await self.client.db.release(connection)
    await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Create(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])