import requests
from bs4 import BeautifulSoup
import telegram
import telegram.ext
import pickle
import os
from datetime import datetime

BOT_TOKEN = '8373116013:AAFLZaCXXhHwEXQIVqgClCvL_5gVm8-EclQ'

# Replace with your Telegram chat ID (e.g., your user ID or channel ID)
# To find your chat ID, send a message to your bot and use a service like @getidsbot
CHAT_ID = 'YOUR_CHAT_ID_HERE'

# URL to scrape
URL = 'https://it.fut.ru/internship'

# File to store previous internships for comparison
STORAGE_FILE = 'previous_internships.pkl'

# Assume the internships are in divs with class 'vacancy-card' or similar;
# Inspect the page source to confirm the exact class name
INTERNSHIP_CLASS = 'vacancy-card'  # Placeholder; update based on actual HTML

def fetch_internships():
    response = requests.get(URL)
    response.raise_for_status()  # Raise error if fetch fails
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all elements with the specified class
    internships = soup.find_all('div', class_=INTERNSHIP_CLASS)
    
    # Extract relevant info, e.g., title and link; adjust based on structure
    current_internships = set()
    for item in internships:
        title = item.find('h3').text.strip() if item.find('h3') else 'Unknown Title'
        link = item.find('a')['href'] if item.find('a') else ''
        # Use a unique identifier, e.g., title + link
        identifier = f"{title}|{link}"
        current_internships.add(identifier)
    
    return current_internships

def load_previous_internships():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'rb') as f:
            return pickle.load(f)
    return set()

def save_internships(internships):
    with open(STORAGE_FILE, 'wb') as f:
        pickle.dump(internships, f)

async def send_telegram_message(bot, message):
    await bot.send_message(chat_id=CHAT_ID, text=message)

def main():
    # Initialize the bot [[5]] (GitHub repo for python-telegram-bot)
    bot = telegram.Bot(token=BOT_TOKEN)
    
    # Fetch current internships
    current = fetch_internships()
    
    # Load previous
    previous = load_previous_internships()
    
    # Find new ones
    new_internships = current - previous
    
    if new_internships:
        update_message = f"New internships found on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}:\n"
        for item in new_internships:
            title, link = item.split('|')
            update_message += f"- {title}: {link}\n"
        
        # Send update via Telegram [[7]] (example of sending updates to Telegram bot/channel)
        import asyncio
        asyncio.run(send_telegram_message(bot, update_message))
        print("Update sent to Telegram.")
    else:
        print("No new internships found.")
    
    # Save current as previous for next run
    save_internships(current)

if __name__ == '__main__':
    main()
