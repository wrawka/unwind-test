import os
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Optional

import requests
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from requests.exceptions import ConnectionError
from utils.cache import timed_cache
from utils.logging_config import configure_logging, logging

configure_logging()
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = os.environ.get('SERVICE_ACCOUNT_FILE')
SPREADSHEET_ID = '1dYz1KijuuQvToFfdh2-1OpTdVLpfdCQ8z5mnrMZ0VoI'
SAMPLE_RANGE = '\'_source\'!A1:D'

CBR_TTL = 60 * 60 * 24  # we cache currency data for 24 hours


@timed_cache(CBR_TTL)
def read_currency_value(code: str = 'R01235') -> float:
    """
    Reads a currency exchange rate value (to RUB) from CBR by code `code`.

    Currency codes reference: http://www.cbr.ru/scripts/XML_val.asp?d=0

    `code` value defaults to US dollar.
    """
    today = datetime.today().strftime('%d/%m/%Y')
    url = 'https://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(today)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            root = ET.fromstring(response.content)

            for child in root.findall('Valute'):
                if child.attrib['ID'] == code:
                    return float(child.find('Value').text.replace(',', '.'))

            logging.warning('Failed to find data for {}. Maybe goblins?'.format(code))
        else:
            logging.error('Falied to load data from CBR.')
    except ConnectionError as e:
        logging.error('Failed to reach CBR.', e)

    return 25.5070  # верни мне мой 2007


def read_google_spreadsheet() -> Optional[List]:
    """
    Reads data from Google Spreadsheet file
    and tries to return it as a list of records.
    """
    creds = None

    if os.path.exists(SERVICE_ACCOUNT_FILE):
        creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    if not creds:
        raise FileNotFoundError('Service account credentials not found or invalid.')

    service = build('sheets', 'v4', credentials=creds)

    sheets = service.spreadsheets()
    result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range=SAMPLE_RANGE).execute()
    values = result.get('values')

    return values
