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

  @app_commands.command(name='editlist', description='Edit the name of a list')
  async def editlist(self, interaction: discord.Interaction, originalname: str, newname: str):   
    embed_message = discord.Embed()
    async with self.client.db.acquire() as connection:
      check = await connection.fetchrow(
      '''
      SELECT EXISTS(
        SELECT 
        FROM lists 
        WHERE list_name=($1)
      );
      ''',
      originalname)
      if check['exists'] == False:
        embed_message.add_field(name='ERROR', value='**'+originalname+'** list does not exist!')
        await interaction.response.send_message(embed=embed_message)
        await self.client.db.release(connection)
        return
      await connection.execute('UPDATE lists SET list_name = ($1) WHERE list_name = ($2);', newname, originalname)
    embed_message.add_field(name='', value='**'+originalname+'** has been renamed to **'+newname+'**')
    await self.client.db.release(connection)
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='editfilm', description='Edit the title of a film')
  async def editfilm(self, interaction: discord.Interaction, originaltitle: str, newtitle: str):
    embed_message = discord.Embed()
    async with self.client.db.acquire() as connection:
      check = await connection.fetchrow(
      '''
      SELECT EXISTS(
        SELECT 
        FROM films
        WHERE title=($1)
      );
      ''',
      originaltitle)
      if check['exists'] == False:
        embed_message.add_field(name='ERROR', value='**'+originaltitle+'** does not exist in film master list!')
        await interaction.response.send_message(embed=embed_message)
        await self.client.db.release(connection)
        return
      await connection.execute('UPDATE films SET title = ($1) WHERE title = ($2);', newtitle, originaltitle)
    await self.client.db.release(connection)
    embed_message.add_field(name='', value='**'+originaltitle+'** has been renamed to **'+newtitle+'**')
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='setstatus', description='Mark the watch status of a film from not watched to watched and vice versa')
  async def setstatus(self, interaction: discord.Interaction, filmtitle: str):
    embed_message = discord.Embed()
    async with self.client.db.acquire() as connection:
      check = await connection.fetchrow(
      '''
      SELECT EXISTS(
        SELECT 
        FROM films
        WHERE title=($1)
      );
      ''',
      filmtitle)
      if check['exists'] == False:
        embed_message.add_field(name='ERROR', value='**'+filmtitle+'** does not exist in film master list!')
        await interaction.response.send_message(embed=embed_message)
        await self.client.db.release(connection)
        return
      await connection.execute('UPDATE films SET watch_status = NOT watch_status WHERE title=($1);', filmtitle)
    await self.client.db.release(connection)
    embed_message.add_field(name='', value='Watch status of **'+filmtitle+'** has been changed')
    await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Update(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])