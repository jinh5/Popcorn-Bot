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

  @app_commands.command(name='deletelist', description='Delete the specified list')
  async def deletelist(self, interaction: discord.Interaction, name: str):
    embed_message = discord.Embed()
    async with self.client.db.acquire() as connection:
      check = await connection.fetchrow(
      '''
      SELECT EXISTS(
        SELECT 1 
        FROM lists 
        WHERE list_name=($1)
      );
      ''',
      name)
      if check['exists'] == False:
        embed_message.add_field(name='ERROR', value='**'+name+'** list does not exist!')
        await interaction.response.send_message(embed=embed_message)
        await self.client.db.release(connection)
        return
      await connection.execute('DELETE FROM lists WHERE list_name = ($1);', name)
    await self.client.db.release(connection)
    embed_message.add_field(name='', value='Deleted **'+ name +'** list')
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='deletefilm', description='Delete the specified film')
  async def deletefilm(self, interaction: discord.Interaction, title: str):
    embed_message = discord.Embed()
    async with self.client.db.acquire() as connection:
      check = await connection.fetchrow(
      '''
      SELECT EXISTS(
        SELECT 1 
        FROM films
        WHERE title=($1)
      );
      ''',
      title)
      if check['exists'] == False:
        embed_message.add_field(name='ERROR', value='**'+title+'** does not exist in film master list!')
        await interaction.response.send_message(embed=embed_message)
        await self.client.db.release(connection)
        return
      await connection.execute('DELETE FROM films WHERE title = ($1);', title)
    await self.client.db.release(connection)
    embed_message.add_field(name='', value='Deleted **'+ title +'** from film master list')
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='delete', description='Delete a film from the specified list')
  async def delete(self, interaction: discord.Interaction, filmtitle: str, listname: str):
    #check if film exists
    #check if list exists
    connection = await self.client.db.acquire()
    async with connection.transaction():
      await self.client.db.execute(
        '''
        DELETE FROM lists_films 
        WHERE film_id = (SELECT film_id FROM films WHERE title=($1))
          AND list_id = (SELECT list_id FROM lists WHERE list_name=($2));
        ''',
        filmtitle, listname
      )
    await self.client.db.release(connection)

    embed_message = discord.Embed()
    embed_message.add_field(name='', value='Deleted **'+filmtitle+'** from **'+listname+'**')
    await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Delete(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])