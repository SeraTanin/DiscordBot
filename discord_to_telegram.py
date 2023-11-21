import discord
import telebot
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
DISCORD_CHAT_ID = os.getenv('DISCORD_CHAT_ID')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")


@bot.event
async def on_message(message):
    if message.content:
        print(type(message.content))
        news_text = message.content
        send_to_telegram(news_text)
    # await bot.process_commands(message)
    if message.attachments:  # check if the message has any attachments
        for attachment in message.attachments:
            print(type(attachment))
            print(type(message.attachments))
            if attachment.filename.endswith(
                    ('.png', '.jpg', '.jpeg', '.gif')):  # check if the attachment is an image file
                url = attachment.url
                response = requests.get(url)
                news_photo = response.content
                send_photo_to_telegram(news_photo)


def send_to_telegram(news_text):
    bot_t = telebot.TeleBot(token=TELEGRAM_TOKEN)
    bot_t.send_message(chat_id=CHAT_ID, text=news_text)


def send_photo_to_telegram(news_photo):
    bot_t = telebot.TeleBot(token=TELEGRAM_TOKEN)
    bot_t.send_photo(chat_id=CHAT_ID, photo=news_photo)


bot.run(DISCORD_TOKEN)
