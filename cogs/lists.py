from discord.ext import commands

class Lists(commands.Cog):
  def __init__(self, client):
    self.client = client
  
  @commands.Cog.listener()
  async def on_ready(self):
    print("lists.py is ready")

  @commands.command()
  async def showlists(self, ctx):
    await ctx.send("Lists:")

async def setup(client):
  await client.add_cog(Lists(client))