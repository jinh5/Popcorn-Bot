import os
import discord
from discord import app_commands
from discord.ext import commands
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
    password=os.getenv('PASSWORD')
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