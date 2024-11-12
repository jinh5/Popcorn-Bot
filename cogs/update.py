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

  @app_commands.command(name='editlistname', description='Edit the name of a list')
  async def editlistname(self, interaction: discord.Interaction, originalname: str, newname: str):   
    #check if name exists in lists before update 

    await self.client.db.execute(
      '''
      UPDATE lists
      SET list_name = ($1)
      WHERE list_name = ($2);
      ''',
      newname, originalname
    )
    
    embed_message = discord.Embed()
    embed_message.add_field(name='', value='**'+originalname+'** has been renamed to **'+newname+'**')
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='editfilmtitle', description='Edit the title of a film')
  async def editfilmtitle(self, interaction: discord.Interaction, originaltitle: str, newtitle: str):
    #check if title exists in films before update 
    
    await self.client.db.execute(
      '''
      UPDATE films
      SET title = ($1)
      WHERE title = ($2);
      ''',
      newtitle, originaltitle
    )
    
    embed_message = discord.Embed()
    embed_message.add_field(name='', value='**'+originaltitle+'** has been renamed to **'+newtitle+'**')
    await interaction.response.send_message(embed=embed_message)

  @app_commands.command(name='changewatchstatus', description='Mark the watch status of a film from not watched to watched and vice versa')
  async def changewatchstatus(self, interaction: discord.Interaction, filmtitle: str):
    #check if film exists
    await self.client.db.execute(
      '''
      UPDATE films 
      SET watch_status = NOT watch_status 
      WHERE title=($1)
      ''',
      filmtitle
    )
    embed_message = discord.Embed()
    embed_message.add_field(name='', value='Watch status of **'+filmtitle+'** has been changed')
    await interaction.response.send_message(embed=embed_message)

async def setup(client):
  await client.add_cog(Update(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])