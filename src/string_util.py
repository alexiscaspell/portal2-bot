from table2ascii import table2ascii as t2a, PresetStyle

def make_str_table_old(data,title=None):

    if isinstance(data,dict):
        data_tuple = [(k, v) if isinstance(v,str) else (k,)+tuple(v) for k, v in data.items()]
    else:
        data_tuple = [e if isinstance(e,list) or isinstance(e,tuple) else [e] for e in data]
    
    max_widths=[]

    tuple_len = len(data_tuple[0])

    for i in range(tuple_len):
        max_widths.append(max(list(map(lambda e:len(str(e)),list(map(lambda t:t[i],data_tuple))))))

    for x in range(tuple_len):
        for y in range(len(data_tuple)):
            list_val=list(data_tuple[y])
            list_val[x] =   " "+data_tuple[y][x]+" "*(max_widths[x]-len(data_tuple[y][x]))+" "
            list_val[x]=list_val[x].replace("\n","")
            data_tuple[y]=list_val

    str_table = " "+"-"* (2*len(max_widths)+sum(max_widths)+1)+" \n"

    for t in data_tuple:
        str_table+= "|"+"|".join(t)+"|\n"
        str_table+= " "+"-"* (2*len(max_widths)+sum(max_widths)+1)+" \n"

    return str_table

def make_str_table(data,title=None):
    if isinstance(data,dict):
        data_list = [[k, v] if isinstance(v,str) else [k]+list(v) for k, v in data.items()]
    else:
        data_list = [list(e) if isinstance(e,list) or isinstance(e,tuple) else [e] for e in data]

    headers = data_list.pop(0)

    # In your command:
    return t2a(header=headers,
        body=data_list,
        style=PresetStyle.thick_box
    )