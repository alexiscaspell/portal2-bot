from src.sheets import GoogleSheet
from src.portal2_query import Portal2Query
from src.sheet_mappings import SheetCol,SheetCell


class MapProperty():
    def __init__(self,name,column,row,sheet:GoogleSheet,value=None):
        self._name = name
        self._value = value
        self._row = row
        self._column = column
        self._sheet = sheet

    def cell(self):
        return f"{self._column}{self._row}"

    def get(self):
        if not self._value:
            self._value=self._sheet.value(self.cell())
        return self._value

    def set(self,value,is_formula=False):
        self._value = value
        self._sheet.update_value(self.cell(),value,is_formula=is_formula)

    def __str__(self) -> str:
        return str(self.get())

class Map():
    def __init__(self,map_dict:dict,sheet:GoogleSheet,actual_hour):
        self.row = int(map_dict["row"])
        self.sheet = sheet

        self.actual_hour=actual_hour

        self.id = MapProperty("id",SheetCol.id.value,self.row,self.sheet,map_dict.get("id",None))
        self.name = MapProperty("name",SheetCol.name.value,self.row,self.sheet,map_dict.get("name",None))
        self.status = MapProperty("status",SheetCol.played.value,self.row,self.sheet,map_dict.get("status",None))
        self.start_time = MapProperty("start_time",SheetCol.start.value,self.row,self.sheet,map_dict.get("start_time",None))
        self.end_time = MapProperty("end_time",SheetCol.end.value,self.row,self.sheet,map_dict.get("end_time",None))
        self.elapsed_time = MapProperty("elapsed_time",SheetCol.eltime.value,self.row,self.sheet,map_dict.get("elapsed_time",None))
        self.elapsed_net_time = MapProperty("elapsed_net_time",SheetCol.elnettime.value,self.row,self.sheet,map_dict.get("elapsed_net_time",None))
        self.link = MapProperty("link",SheetCol.link.value,self.row,self.sheet,map_dict.get("link",None))

    def end(self):
        self.end_time.set(self.actual_hour)
        if self.is_paused():
            self.pause() # Setea el tiempo jugado (que trucazo eh!)
        self.status.set("Si")

    def start(self):
        if self.is_paused():
            self.unpause()
        else:
            self.start_time.set(self.actual_hour)
            self.sheet.update_value(SheetCell.activemap.value,self.id.get())

    def pause(self):
        update_formula = f"={SheetCell.paused_map_end.value}-{SheetCell.paused_map_start.value}"

        self.sheet.update_value(SheetCell.paused_map_end.value,self.actual_hour)

        if self.is_paused():
            update_formula+=f"+{self.elapsed_net_time.cell()}"
        else:
            self.sheet.update_value(SheetCell.paused_map_start.value,self.start_time.get())

        self.sheet.update_value(SheetCell.paused_map_elapsed.value,update_formula,is_formula=True)

        self.status.set("Pausado")
        self.elapsed_net_time.set(load_value(self.sheet,SheetCell.paused_map_elapsed.value))

    def is_paused(self):
        return self.status.get()=="Pausado"

    def unpause(self):
        self.sheet.update_value(SheetCell.paused_map_start.value,self.actual_hour)
        self.sheet.update_value(SheetCell.activemap.value,self.id.get())


class MapList():
    def __init__(self,sheet:GoogleSheet,actual_hour):
        self.sheet = sheet
        self.actual_hour = actual_hour

    def add(self,title_map:str,link:str=None):
        last_row = len(self.sheet.column(SheetCol.name.value))
        new_row = last_row+1

        start_cell = f"{SheetCol.name.value}{new_row}"

        elapsed_time_cell = f'=IF({SheetCol.start.value}{new_row}="";"";IF({SheetCol.end.value}{new_row}="";NOW();{SheetCol.end.value}{new_row})-{SheetCol.start.value}{new_row})'
        elapsed_net_time_cell = f"={SheetCol.eltime.value}{new_row}"

        link_cell=f'=HYPERLINK("{link}";"{title_map}")'

        values = [title_map,"","","","",""]

        if load_value(self.sheet,f"{SheetCol.id.value}{new_row}")=="":
            start_cell = f"{SheetCol.id.value}{new_row}"
            values = [f"={SheetCol.id.value}{last_row}+1"] + values

        self.sheet.update_row(start_cell,values)

        self.sheet.update_value(f"{SheetCol.eltime.value}{new_row}",elapsed_time_cell,is_formula=True)
        self.sheet.update_value(f"{SheetCol.elnettime.value}{new_row}",elapsed_net_time_cell,is_formula=True)
        self.sheet.update_value(f"{SheetCol.link.value}{new_row}",link_cell,is_formula=True)

    def map(self,id=None,row=None,name=None,lazy=False):
        if id:
            row = self.map_number_row_by_id(str(id))
        elif name:
            row = self.map_number_row_by_name(name)

        data = {"row":row}

        if not lazy:
            columns=["id","name","status","start_time","end_time","elapsed_time","elapsed_net_time","link"]
            values = load_value(self.sheet,str(row))

            for i,v in enumerate(values):
                data.update({columns[i]:v})

        return Map(map_dict=data,sheet=self.sheet,actual_hour=self.actual_hour)

    def next(self):
        map = self.earliest_paused()

        if map is None:
            next_row = self.latest_played().row+1
            map = self.map(row=next_row)

        return map

    def current(self):
        current_id = load_value(self.sheet,SheetCell.activemap.value)
        return self.map(id=current_id)

    def map_number_row_by_id(self,id:str):
        ids_column = self.sheet.column(SheetCol.id.value)
        return ids_column.index(id)+1

    def map_number_row_by_name(self,name:str):
        name_column = self.sheet.column(SheetCol.name.value)
        return name_column.index(name)+1

    def latest_played(self):
        return self.map(row=len(self.sheet.column(SheetCol.played.value)))

    def earliest_paused(self):
        try:
            return self.map(row=self.sheet.column(SheetCol.played.value).index("Pausado")+1)
        except ValueError as _:
            return None

    def query(self):
        return Portal2Query(self.sheet)

def load_value(sheet,key):
    if isinstance(key, (int, float, complex)) or key.isnumeric():
        return sheet.row(int(key))
    return sheet.value(key)