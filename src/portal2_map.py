from src.sheets import GoogleSheet
from src.portal2_query import Portal2Query

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

        self.id = MapProperty("id","A",self.row,self.sheet,map_dict.get("id",None))
        self.name = MapProperty("name","B",self.row,self.sheet,map_dict.get("name",None))
        self.status = MapProperty("status","C",self.row,self.sheet,map_dict.get("status",None))
        self.start_time = MapProperty("start_time","D",self.row,self.sheet,map_dict.get("start_time",None))
        self.end_time = MapProperty("end_time","E",self.row,self.sheet,map_dict.get("end_time",None))
        self.elapsed_time = MapProperty("elapsed_time","F",self.row,self.sheet,map_dict.get("elapsed_time",None))
        self.elapsed_net_time = MapProperty("elapsed_net_time","G",self.row,self.sheet,map_dict.get("elapsed_net_time",None))

    def end(self):
        self.end_time.set(self.actual_hour)
        self.status.set("Si")

    def start(self):
        self.start_time.set(self.actual_hour)

    def pause(self):
        update_formula = f"=I25-H25"

        self.sheet.update_value("I25",self.actual_hour)

        if self.is_paused():
            update_formula+=f"+{self.elapsed_net_time.cell()}"
        else:
            self.sheet.update_value("H25",self.start_time.get())

        self.sheet.update_value(f"I23",update_formula,is_formula=True)

        self.status.set("Pausado")
        self.elapsed_net_time.set(load_value(self.sheet,"I23"))

    def is_paused(self):
        return self.status.get()=="Pausado"

    def unpause(self):
        self.sheet.update_value("H25",self.actual_hour)

class MapList():
    def __init__(self,sheet:GoogleSheet,actual_hour):
        self.sheet = sheet
        self.actual_hour = actual_hour

    def add(self,title_map:str):
        last_row = len(self.sheet.column("B"))
        new_row = last_row+1

        start_cell = f"B{new_row}"

        elapsed_time_cell = f'=IF(D{new_row}="";"";IF(E{new_row}="";NOW();E{new_row})-D{new_row})'
        elapsed_net_time_cell = f"=F{new_row}"

        values = [title_map,"","",""]

        if load_value(self.sheet,f"A{new_row}")=="":
            start_cell = f"A{new_row}"
            values = [f"=A{last_row}+1"] + values

        self.sheet.update_row(start_cell,values)

        self.sheet.update_value(f"F{new_row}",elapsed_time_cell,is_formula=True)
        self.sheet.update_value(f"G{new_row}",elapsed_net_time_cell,is_formula=True)

    def map(self,id=None,row=None,name=None,lazy=False):
        if id:
            row = self.map_number_row_by_id(str(id))
        elif name:
            row = self.map_number_row_by_name(name)

        data = {"row":row}

        if not lazy:
            columns=["id","name","status","start_time","end_time","elapsed_time","elapsed_net_time"]
            values = load_value(self.sheet,str(row))

            for i,v in enumerate(values):
                data.update({columns[i]:v})

        return Map(map_dict=data,sheet=self.sheet,actual_hour=self.actual_hour)

    def next(self):
        next_row = self.latest_played().row+1
        return self.map(row=next_row)

    def map_number_row_by_id(self,id:str):
        ids_column = self.sheet.column("A")
        return ids_column.index(id)+1

    def map_number_row_by_name(self,name:str):
        name_column = self.sheet.column("B")
        return name_column.index(name)+1

    def latest_played(self):
        return self.map(row=len(self.sheet.column("C")))

    def earliest_paused(self):
        try:
            return self.map(row=self.sheet.column("C").index("Pausado")+1)
        except ValueError as _:
            return None

    def query(self):
        return Portal2Query(self.sheet)

def load_value(sheet,key):
    if isinstance(key, (int, float, complex)) or key.isnumeric():
        return sheet.row(int(key))
    return sheet.value(key)