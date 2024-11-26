import os
import discord
from discord import app_commands
from bot import Bot
from dotenv import load_dotenv
from asyncio import run
from asyncpg import create_pool

load_dotenv()

async def main():
  async with create_pool(
    host=os.getenv('HOST'),
    database=os.getenv('DATABASE'),
    port=os.getenv('PORT'),
    user=os.getenv('USER'),
    password=os.getenv('PASSWORD'),
    statement_cache_size=0
  ) as pool:
      intents = discord.Intents.default()  
      intents.message_content = True
      async with Bot(
        db=pool,
        command_prefix='$',
        intents=intents,
        application_id = os.getenv('APPLICATION_ID')
      ) as bot:
        intents.message_content = True
        
        @bot.event
        async def on_guild_join(guild):
          system_channel = guild.system_channel
          if system_channel:
            embed_message = discord.Embed(title="Hello! I'm Popcorn Bot!", description=f"Thanks for adding me to **{guild.name}**! I'm here to help you organize lists for discord movie nights!")
            embed_message.add_field(name='Getting Started', value='Type /help to see a list of commands', inline=False)
            embed_message.add_field(name='Code Repository', value='https://github.com/jinh5/Popcorn-Bot', inline=False)
            await system_channel.send(embed=embed_message)

        async def on_tree_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
          if isinstance(error, app_commands.CommandOnCooldown):
            return await interaction.response.send_message(f"Command is currently on cooldown! Try again in **{error.retry_after:.2f}** seconds!")
          elif isinstance(error, app_commands.MissingPermissions):
            return await interaction.response.send_message(f"You're missing permissions to use that")
          else:
            embed_message = discord.Embed()
            embed_message.add_field(name="ERROR", value=error)
            await interaction.response.send_message(embed=embed_message, ephemeral=True)
        bot.tree.on_error = on_tree_error

        await bot.start(token=os.getenv('TOKEN'))

if __name__ == '__main__':
  run(main())