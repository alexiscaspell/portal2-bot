from src.sheets import GoogleSheet

class Portal2Info():
    def __init__(self,sheet:GoogleSheet):
        self.sheet = sheet
        self.stats = self.load_stats()
        self.actual_hour = self.load_value("I3")

    def load_value(self,key):
        if key.isnumeric():
            return self.sheet.row(int(key))
        return self.sheet.value(key)

    def map_number_row_by_id(self,id:str):
        ids_column = self.sheet.column("A")
        return ids_column.index(id)+1

    def map_number_row_by_name(self,name:str):
        ids_column = self.sheet.column("B")
        return ids_column.index(id)+1

    def latest_played_map_number_row(self):
        return len(self.sheet.column("C"))

    def end_map_by_row(self,row:int):
        self.sheet.update_value(f"E{row}",self.actual_hour)
        self.sheet.update_value(f"C{row}","Si")

    def start_map_by_row(self,row:int):
        self.sheet.update_value(f"D{row}",self.actual_hour)


    def add_map(self,title_map:str):
        last_row = self.latest_played_map_number_row()
        new_row = last_row+1

        start_cell = f"B{new_row}"

        elapsed_time_cell = f'=IF(D{new_row}="";"";IF(E{new_row}="";NOW();E{new_row})-D{new_row})'
        elapsed_net_time_cell = f"=F{new_row}"

        values = [title_map,"","",""]

        if self.load_value(f"A{new_row}")=="":
            start_cell = f"A{new_row}"
            values = [f"=A{last_row}+1"] + values

        self.sheet.update_row(start_cell,values)

        self.sheet.update_value(f"F{new_row}",elapsed_time_cell,is_formula=True)
        self.sheet.update_value(f"G{new_row}",elapsed_net_time_cell,is_formula=True)

    def load_stats(self):
        result = {}
        columna_keys = self.sheet.column("H")
        columna_values = self.sheet.column("I")
        for n in range(6,14):
            key = columna_keys[n-1]
            value = columna_values[n-1]
            result.update({key:value})
        return result