def convertnan(file):
    rate_list= []
    for value in file: 
        if str(value['VAT'])=='nan':
            value['VAT']=0
        if str(value['LVY'])=='nan':
            value['LVY']=0
        if str(value['EXC'])=='nan':
            value['EXC']=0
        rate_list.append(value)
    return rate_list