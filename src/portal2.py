import pandas as pd

class Portal2Info():
    def __init__(self,values:pd.DataFrame):
        self.stats = self.load_stats(values)
        self.hora_actual = self.load_value("I3",values)
        self.values = values

    def load_value(self,key,data:pd.DataFrame):
        print(f"obteniendo valor {key}")
        if key.isnumeric():
            print(f"{key} es un numero!!!")
            return data.iloc[[int(key)]]

        print(f"{key} no es numero...")
        print(f"clumna {key[0]}")
        print(f"fila {int(key[1:])}")
        return data[key[0]][int(key[1:])]

    def load_stats(self,values):
        result = {}
        print("Llegue derechupete")
        for n in range(6,14):
            key = self.load_value(f"H{n}",values)
            value = self.load_value(f"I{n}",values)
            result.update({key:value})
        return result