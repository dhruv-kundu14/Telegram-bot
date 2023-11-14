import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = 
RAPIDAPI_KEY = 

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! Thanks for chatting')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I\'m groovie! Thanks for chatting')

async def greet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Greetings! How can I assist you?')

async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = context.args[0] if context.args else None  # Get the location from the command arguments
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

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('greet', greet_command))
    app.add_handler(CommandHandler('weather', weather_command))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
