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

async def setup(client):
  await client.add_cog(Delete(client), guilds=[discord.Object(id=os.getenv('SERVER_ID'))])