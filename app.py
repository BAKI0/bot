from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Flask Telegram Bot!"

@app.route('/health')
def health_check():
    return "Bot is running!"

def run_flask():
    app.run(port=5000)

def main():
    # Create Updater and pass in your bot token
    updater = Updater("YOUR_BOT_TOKEN")

    # Command handler example
    def start(update: Update, context: CallbackContext):
        update.message.reply_text("Hello! I'm your bot.")

    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Start Flask in a separate thread
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()