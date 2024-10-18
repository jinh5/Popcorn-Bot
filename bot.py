import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()  
intents.message_content = True
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix='$', intents=intents)
token = os.getenv('TOKEN')

@client.event
async def on_ready():
  print("Logged in as a bot {0.user}".format(client))

@client.event
async def on_message(message):
  username = str(message.author).split("#")[0]
  channel = str(message.channel.name)
  user_message = str(message.content)

  print(f'Message {user_message} by {username} on {channel}')

  if message.author == client.user:
    return

  if user_message.lower() == "hello" or user_message.lower() == "hi":
    await message.channel.send(f'Hello {username}')
    return
  elif user_message.lower() == "bye":
    await message.channel.send(f'Bye {username}')

bot.add_command(help)
client.run(token)