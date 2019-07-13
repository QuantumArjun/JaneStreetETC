def fair_value(VAL_buy, VAL_sell):
    #calculate the fair value
    #loop therough last 10 of buys and sells in order to calcualte the fair value
    #return the average divided by 2
    VAL_max = 0
    VAL_min = 999999999999

    for i in range (0, len(VAL_buy)):
        if VAL_buy[i] > max:
            VAL_max = VALE_buy[i]

    for i in range (0, len(VAL_sell)):
        if VAL_sell[i] < min:
            VAL_min = VALE_sell[i]


    VAL_fair =  (VAL_min + VAL_max) / 2
    return VAL_fair
