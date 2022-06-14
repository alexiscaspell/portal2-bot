
from google.oauth2 import service_account
import string
import gspread
from gspread import Worksheet



SCOPES = ['https://www.googleapis.com/auth/spreadsheets','https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
LETTERS=string.ascii_uppercase

class GoogleSheet():
    def __init__(self,worksheet:Worksheet):
        self.sheet = worksheet

    def row(self,row:int):
        return self.sheet.row_values(row)

    def column(self,column:str):
        return self.sheet.col_values(LETTERS.index(column)+1)

    def value(self,cell:str):
        return self.sheet.cell(int(cell[1:]),LETTERS.index(cell[0])+1)

    def update_row(self,start_cell:str,value_list:list):
        start_column = start_cell[0]
        start_row = int(start_cell[1:])

        end_cell = LETTERS[LETTERS.index(start_column)+len(value_list)-1]+f"{start_row}"

        cell_list = self.sheet.range(f"{start_cell}:{end_cell}")

        for i,cell in enumerate(cell_list):
            cell.value = value_list[i]

        self.sheet.update_cells(cell_list)

    def update_value(self,cell:str,value,is_formula=False):
        if is_formula:
            self.sheet.update_acell(cell, value)

        self.sheet.update_cell(int(cell[1:]),LETTERS.index(cell[0])+1,value)

def load_data(spreadsheet_id:str):
    creds = None

    creds = service_account.Credentials.from_service_account_file('/usr/app/token.json', scopes=SCOPES)

    client = gspread.authorize(creds)
    sheet = client.open_by_key(spreadsheet_id)
    sheet=sheet.sheet1

    return GoogleSheet(sheet)

"A"