from turtle import width
from src.sheets import GoogleSheet
from src.portal2_map import MapList
from src.sheet_mappings import SheetCol,SheetCell

class Portal2Info():
    def __init__(self,sheet:GoogleSheet):
        self.sheet = sheet
        self.stats = self.load_stats()
        self.actual_hour = self.load_value(SheetCell.now.value)
        self.maps = MapList(sheet,actual_hour=self.actual_hour)

    def load_value(self,key):
        if key.isnumeric():
            return self.sheet.row(int(key))
        return self.sheet.value(key)

    def load_stats(self):
        result = {}
        columna_keys = self.sheet.column(SheetCol.statheaders.value)
        columna_values = self.sheet.column(SheetCol.statvals.value)
        for n in range(6,14):
            key = columna_keys[n-1]
            value = columna_values[n-1]
            result.update({key:value})
        return result

    # def update_paused_map_start_time(self,value):
    #     self.sheet.update_value(f"H25",value)

    # def update_paused_map_end_time(self,value):
    #     self.sheet.update_value(f"H25",value)