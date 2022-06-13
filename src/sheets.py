
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import pandas as pd
import string

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
LETTERS=string.ascii_uppercase

def load_data(spreadsheet_id:str,sheet_range:str):
    creds = None

    creds = service_account.Credentials.from_service_account_file('token.json', scopes=SCOPES)

    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id,range=sheet_range).execute()

    df = pd.DataFrame(result.get("values",[]))

    df.columns = list(map(lambda e:LETTERS[e],list(df.columns)))
    df.index = list(range(1,df.index.stop+1))

    return df