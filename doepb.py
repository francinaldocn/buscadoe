#!/usr/bin/env python3
# Example script to search for terms in DOEPB.
"""Importing dependencies."""
import locale
import os
import sys

from datetime import datetime
from pathlib import Path

import utils

from dotenv import load_dotenv
from send_telegram_msg import send_message


# Set locale to pt_BR
locale.setlocale(locale.LC_TIME, "pt_BR.utf8")

# Date variables
current_date = datetime.now()
current_date_text = current_date.strftime("%d-%m-%Y")
current_month_text = current_date.strftime("%B")
current_year_text = current_date.strftime("%Y")
current_day = current_date.weekday()
current_day_text = current_date.strftime("%A")


# Root folder
root_folder = Path(__file__).parent

# Temporary folder
temp_folder = Path(root_folder, "tmp")

# If not exist, create temp folder
if not os.path.exists(temp_folder):
    os.makedirs(temp_folder)
    f"{temp_folder} created successfully"

# Mount document URL
# DOE base URL
BASE_URL = "https://auniao.pb.gov.br/servicos/doe"

# Full DOE URL
doe_url = f"{BASE_URL}/{current_year_text}/{current_month_text}/diario-oficial-{current_date_text}.pdf"


# Get DOE PDF
# Input file path
in_file_path = f"{temp_folder}/diario-oficial-{current_date_text}.pdf"

# Get DOE PDF
if utils.is_valid_url(doe_url):
    pdf_file = utils.get_file(doe_url, in_file_path)
else:
    f"URL {doe_url} NOT FOUND"
    sys.exit()


# Split documment per page (Split pdf pages)
list_of_files = utils.split_pdf(temp_folder, in_file_path)


# Terms to search in converted file
# search_term = [input("Enter a term you want to search in file: ")]
search_terms = ["Term 1", "Term 2", "Term..."]

# Create dic to store terms
term_search = {}

# Insert terms in dict
for term in search_terms:
    term_search[term] = []

# Convert PDF pages to text and search terms
for file in list_of_files:
    if utils.verify_if_pdf_is_text_or_image(temp_folder, file):
        # Convert pdf pages to text
        text = utils.convert_pdf_to_text(temp_folder, file)

        # Search terms in text and return text page number
        result = utils.search_in_text(text, search_terms, term_search, file)
    else:
        # Convert pdf pages to image
        utils.convert_pdf_to_image(temp_folder, file, dpi=150)

        # Convert image to text
        text = utils.convert_img_to_text(temp_folder, file)

        # Search terms in text and return text page number
        result = utils.search_in_text(text, search_terms, term_search, file)


# Formatting the results to send to Telegram
MSG_HEADER_L1 = f'<a href="{doe_url}"><b>DOEPB Search Result for {current_date_text}\
    </b></a>\n\n'
MSG_HEADER_L2 = "<b><u>Terms found in the search:</u></b>\n\n"

MSG_BODY = ""

for k, v in result.items():
    if len(v) > 0:
        MSG_BODY = MSG_BODY + f"* <b>{k.upper()}</b> <i>was found in pages</i> <b> {v} </b>\n"


if MSG_BODY == "":
    message = MSG_HEADER_L1 + "<b>The search terms were not found in today's DOE" + " edition.</b>"
else:
    message = MSG_HEADER_L1 + MSG_HEADER_L2 + MSG_BODY


# Send results to Telegram
# Load credentials
load_dotenv()
token = os.getenv("TOKEN")
receive_id = os.getenv("RECEIVE_ID")

# Send message to Telegram
send_message(token, receive_id, message)
