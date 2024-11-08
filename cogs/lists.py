import discord
import os
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands

load_dotenv()

class Lists(commands.Cog):
  """Commands for organizing lists"""
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print("lists.py is ready") 

  @app_commands.command(name="createlist")
  async def createlist(self, interaction: discord.Interaction, name: str):
    join_name = ''.join(name)
    embed_message = discord.Embed()
    command = 'CREATE TABLE ' + join_name + ' (film_id INT, title TEXT, CONSTRAINT fk_film_id FOREIGN KEY (film_id) REFERENCES master_list(film_id), CONSTRAINT fk_title FOREIGN KEY (title) REFERENCES master_list(title))' 
    await self.client.db.execute(command)
    command2 = 'ALTER TABLE ' + join_name + ' ENABLE ROW LEVEL SECURITY'
    await self.client.db.execute(command2)
    embed_message.add_field(name=join_name, value='has been created')
    await interaction.response.send_message(embed=embed_message)
      

async def setup(client):
  await client.add_cog(Lists(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])