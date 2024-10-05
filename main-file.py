import os
import google.generativeai as genai
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
from io import StringIO
import requests
from datetime import datetime
import pytz
import json

# configure gemini
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# set up google sheets client
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
google_credentials_json = os.environ['GOOGLE_CREDENTIALS']
creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(google_credentials_json), scope)
client = gspread.authorize(creds)

# open the sheet
sheet_id = os.environ['SHEET_ID']
sheet = client.open_by_key(sheet_id).sheet1

# get all values
values = sheet.get_all_values()

# convert to csv string
csv_buffer = StringIO()
csv_writer = csv.writer(csv_buffer)
csv_writer.writerows(values)
csv_string = csv_buffer.getvalue()

# get current date and time in mountain standard time
mst = pytz.timezone('US/Mountain')
current_datetime = datetime.now(mst).strftime("%A, %Y-%m-%d %H:%M:%S")

# create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=f"It is currently {current_datetime}. This assistant will always base its responses on this date and time accurately. This assistant will be texting the user and owner of this calendar over a messaging app. It should address them directly, and have a human voice and friendly demeanor. It should not use bolds or indented text.",
)

# start chat session with csv data
chat_session = model.start_chat(
    history=[
        {
            "role": "user",
            "parts": [
                csv_string,
                "Attached is a spreadsheet with my calendar for the next week. Write a memo telling me what I should focus on preparing for, particularly focusing on what is happening tomorrow, but tell me if I have something that sounds significant coming up that might be worth preparing for sooner. Make the message long and detailed, specifically focus on any deadlines.",
            ],
        },
    ]
)

response = chat_session.send_message("What should I focus on?")

# telegram bot configuration
TELEGRAM_BOT_TOKEN = os.environ['TELEGRAM_BOT_TOKEN']
TELEGRAM_CHAT_ID = os.environ['TELEGRAM_CHAT_ID']

# send message via telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, json=payload)

# send the response via telegram
send_telegram_message(response.text)

print("Message sent via Telegram!")
