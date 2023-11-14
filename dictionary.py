import pyqrcode
import io
import re
import os
import requests
import telebot
from speedtest import Speedtest
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = 'ENTER THE API KEY FROM TELEGRAM BOTFATHER'
RAPIDAPI_KEY = 'ENTER RAPID API KEY'



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! My name is Groovie ')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot_info = """
    I'm groovie! Thanks for chatting with me. Here are some things I can do:

    1. Generate QR Code: Use the /qrcode command followed by the text you want to convert into a QR code. For example: /qrcode Hello World

    2. Get Weather Information: Use the /weather command followed by the location you want to get weather information for. For example: /weather New York

    3. Check Internet Speed: Use the /speed command to check your current internet speed.

    4. Generate Avatar: Use the /avatar command followed by a name to generate a cool avatar based on the name. For example: /avatar John

    Feel free to explore and try out these commands. If you have any questions, feel free to ask!
    """

    await update.message.reply_text(bot_info)


async def greet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Greetings! How can I assist you?')

async def qrcode_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide the input for the QR code.")
        return
    
    input_text = " ".join(context.args)
    url = pyqrcode.create(input_text)
    url.png('myqr.png', scale=6)
    
    with open('myqr.png', 'rb') as qr_file:
        byte_stream = io.BytesIO(qr_file.read())
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=byte_stream)

async def avatar_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a name for the avatar.")
        return

    name = " ".join(context.args)
    try:
        name = re.sub(r"\W", "_", name)
        url = f"https://api.adorable.io/avatars/285/{name.strip()}.png"
        response = requests.get(url)
        response.raise_for_status()
        avatar_image = response.content

        byte_stream = io.BytesIO(avatar_image)
        await context.bot.send_photo(chat_id=update.message.chat_id, photo=byte_stream)
    except requests.exceptions.RequestException as e:
        # Handle the error gracefully
        await update.message.reply_text(f"generating the avatar: {str(e)}")
    except Exception:
        # Handle any other exception that might occur
        await update.message.reply_text("Failed to generate the avatar.")

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = context.args[0] if context.args else None
    if not location:
        await update.message.reply_text("Please provide a location.")
        return

    url = "https://weatherbit-v1-mashape.p.rapidapi.com/current"
    querystring = {"city": location, "units": "metric"}

    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        weather_data = response.json()

        if 'data' in weather_data:
            temperature = weather_data['data'][0]['temp']
            weather_description = weather_data['data'][0]['weather']['description']
            message = f"Weather in {location}: Temperature: {temperature}°C, Description: {weather_description}"
        else:
            message = f"Failed to fetch weather data for {location}."

        await update.message.reply_text(message)
    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Failed to fetch weather data: {str(e)}")

async def speed_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        st = Speedtest()
        download_speed = st.download()
        download_speed_mbps = download_speed / 1000000  # Convert to Mbps
        download_speed_mbps = download_speed_mbps / 8  # Convert to MBps
        await update.message.reply_text(f"Download Speed: {download_speed_mbps:.2f} MBps")
    except Exception as e:
        await update.message.reply_text(f"Failed to check speed: {str(e)}")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('greet', greet_command))
    app.add_handler(CommandHandler('qrcode', qrcode_command))
    app.add_handler(CommandHandler('avatar', avatar_command)) 
    app.add_handler(CommandHandler('weather', weather_command))
    app.add_handler(CommandHandler('speed', speed_command))
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=5)
