def fair_value(VAL):
    #calculate the fair value
    #loop therough last 10 of buys and sells in order to calcualte the fair value
    #return the average divided by 2
    VAL_max = 0
    VAL_min = 999999999999

    for i in range (0, len(VAL)):
        if VAL_buy[i] > max:
            VAL_max = VALE[i]
        if VAL_sell[i] < min:
            VAL_min = VAL[i]

    VAL_fair =  (VAL_min + VAL_max) / 2
    return VAL_fair
