import requests
import time
import json
import os


API_URL = 'https://oxide.sensibull.com/v1/compute/verified_by_sensibull/live_positions/snapshot/fascinated-prehnite'
TELEGRAM_BOT_TOKEN = '7402758030:AAE4Sksd-8z9mXGr640Zdc2-8513PHyVGOo'
TELEGRAM_CHAT_ID = '1192571661'

def fetch_api_data():
    response = requests.get(API_URL)
    data=response.json().get("payload").get("position_snapshot_data").get("data")
    final_resp=""
    for item in data:
        for trade in item['trades']:
            symbol = trade['trading_symbol']
            quantity = trade['quantity']
            price = trade['average_price']
            
            # Format the output as requested
            output = f"Symbol: {symbol}  Quantity: {quantity}  Price: {price}\n"
            final_resp+=output
    return final_resp

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

def main():
    previous_data = ''
    
    while True:
        try:
            current_data = fetch_api_data()
            
            if previous_data is not None and current_data != previous_data:
                message = f"Username: Intraday ke Ch***\n{current_data}"
                send_telegram_message(message)
            
            previous_data = current_data
            
            time.sleep(60)  # Wait for 1 minute
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            send_telegram_message(error_message)
            time.sleep(60)  # Wait for 1 minute before retrying

if __name__ == "__main__":
    main()
