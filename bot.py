import requests
from bs4 import BeautifulSoup
import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import pickle
import os
from datetime import datetime

BOT_TOKEN = '8373116013:AAFLZaCXXhHwEXQIVqgClCvL_5gVm8-EclQ'
CHAT_ID_STORAGE_FILE = 'chat_id.pkl'
URL_TO_PARSE = 'https://it.fut.ru/internship'
PREVIOUS_INTERNSHIPS_STORAGE_FILE = 'previous_internships.pkl'
INTERNSHIP_DIV_CLASS = 'sc-897afcd6-2 cqKYHt'

def load_chat_id():
    if os.path.exists(CHAT_ID_STORAGE_FILE):
        with open(CHAT_ID_STORAGE_FILE, 'rb') as file_object:
            return pickle.load(file_object)
    return None


def save_chat_id(chat_id):
    with open(CHAT_ID_STORAGE_FILE, 'wb') as file_object:
        pickle.dump(chat_id, file_object)


async def start_command(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat.id
    save_chat_id(chat_id)
    await update.message.reply_text(
        f"Hello! Your chat ID ({chat_id}) has been saved. "
        f"You will now receive internship updates from this bot."
    )
    print(f"Chat ID saved: {chat_id}")


def fetch_internships() -> set:
    response = requests.get(URL_TO_PARSE)
    response.raise_for_status()  # Raise error if fetch fails

    internships : list = BeautifulSoup(response.text, 'html.parser').find_all('div', class_=INTERNSHIP_DIV_CLASS)
    
    current_internships = set()
    for item in internships:
        title = item.find('h2').text.strip() if item.find('h2') else 'Unknown Title'
        link = item.find('a')['href'] if item.find('a') else ''
        current_internships.add(f"{title}|{link}")
    
    return current_internships


def load_previous_internships() -> set:
    if os.path.exists(PREVIOUS_INTERNSHIPS_STORAGE_FILE):
        with open(PREVIOUS_INTERNSHIPS_STORAGE_FILE, 'rb') as file_object:
            return pickle.load(file_object)
    return set()


def save_internships(internships):
    with open(PREVIOUS_INTERNSHIPS_STORAGE_FILE, 'wb') as file_object:
        pickle.dump(internships, file_object)


async def send_telegram_message(bot, message, chat_id):
    if chat_id:
        await bot.send_message(chat_id=chat_id, text=message)
    else:
        print("No chat ID found. User needs to start the bot first with /start command.")


def check_and_send_updates():
    bot = telegram.Bot(token=BOT_TOKEN)
    chat_id = load_chat_id()

    if not chat_id:
        print("No chat ID found. User needs to start the bot first with /start command.")
        return

    current_internships : set = fetch_internships()
    new_internships : set = current_internships - load_previous_internships()
    save_internships(current_internships)

    if new_internships:
        update_message = f"New internships found on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n"
        for item in new_internships:
            title, link = item.split('|')
            update_message += f"- {title}: {link}\n"
        
        import asyncio
        asyncio.run(send_telegram_message(bot, update_message, chat_id))
        print("Update sent to Telegram.")
    else:
        print("No new internships found.")


def main():
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start_command))

    print("Bot is running. Send /start to register your chat ID.")
    print("Press Ctrl+C to stop the bot.")

    application.run_polling()
    

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        check_and_send_updates()
    else:
        main()
