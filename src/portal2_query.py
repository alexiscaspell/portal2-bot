from src.sheets import GoogleSheet

class Portal2Query():
    def __init__(self,sheet:GoogleSheet):
        self.data=[]

        self.querys=[]

        width,_ = GoogleSheet.cell_to_index("G1")

        for i in range(1,sheet.count_rows()+1):
            self.data.append(sheet.eager_row(i)[0:width])

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