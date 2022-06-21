from turtle import width
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

    def next_map(self):
        return self.sheet.value(f"B{self.latest_played_map_number_row()+1}")


    def add_map(self,title_map:str):
        last_row = len(self.sheet.column("B"))
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

class Portal2Query():
    def __init__(self,portal_data:Portal2Info):
        self.portal_data = portal_data
        self.data=[]

        self.querys=[]

        width,_ = GoogleSheet.cell_to_index("G1")

        for i in range(1,portal_data.sheet.count_rows()+1):
            self.data.append(portal_data.sheet.eager_row(i)[0:width])

        self.headers=self.data[0]
        self.data=self.data[1:]

    def filter_by_start_date(self,date:str=None):
        if date is None:
            return self

        self.add_is_in_filter("D",date)

        return self

    def filter_by_end_date(self,date:str=None):
        if date is None:
            return self

        self.add_is_in_filter("E",date)

        return self

    def filter_by_name(self,name:str=None):
        if name is None:
            return self

        self.add_is_in_filter("B",name)

        return self

    def filter_by_played(self,played:bool=None):
        if played is None:
            return self

        valid_values=["No",""]

        if played:
            valid_values=["Si","Ya jogado antes de los primeros 50"]

        def fun(data,x):
            return data[x] in valid_values

        self.add_filter("C",fun)
        self.add_not_empty_filter("B")

        return self

    def add_filter(self,column,some_function):
        x,_ = GoogleSheet.cell_to_index(f"{column}1")
        self.querys.append((x,some_function))

    def filter_by_id(self,id:int=None):
        if id is None:
            return self

        self.add_equal_filter("A",str(id))
        return self

    def add_is_in_filter(self,column,value):

        def fun(e,x):
            return value in e[x]

        self.add_filter(column,fun)

        return self

    def add_equal_filter(self,column,value):
        def fun(e,x):
            return e[x]==value

        self.add_filter(column,fun)

    def add_not_empty_filter(self,column):
        def fun(e,x):
            return e[x] not in ["",None ] 

        self.add_filter(column,fun)

    def valid(self,data):
        for t in self.querys:
            x=t[0]
            fun=t[1]
            if not fun(data,x):
                return False
        return True

    def result(self):
        return [self.headers]+list(filter(lambda e: self.valid(e),self.data))