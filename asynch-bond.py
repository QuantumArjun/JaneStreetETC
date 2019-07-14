#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
import time
from multiprocessing import Process

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name="INDIANPYRAMIDS"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=1
prod_exchange_hostname="production"

port=25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + team_name if test_mode else prod_exchange_hostname

# ~~~~~============== NETWORKING CODE ==============~~~~~
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)

def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")

def read_from_exchange(exchange):
    return json.loads(exchange.readline())


# -===============constants=====================

BOND_buy = []
BOND_sell = []


VALBZ_buy = []
VALBZ_sell = []


VALE_buy = []
VALE_sell = []

GS_buy = []
GS_sell = []

MS_buy = []
MS_sell = []

WFC_buy = []
WFC_sell = []

XLF_buy = []
XLF_sell = []


ACTIVE  = {
'BOND': False,
'VALBZ': False,
'VALE': False,
'GS': False,
'MS':False,
'WFC': False,
'XLF': False,
}
limit_dict = {
'BOND': 100,
'VALBZ': 10,
'VALE': 10,
'GS': 100,
'MS': 100,
'WFC': 100,
'XLF': 100,
}
position_dict = {
'BOND': 0,
'VALBZ': 0,
'VALE': 0,
'GS': 0,
'MS': 0,
'WFC': 0,
'XLF': 0,
}
pending_dict = {
'BOND': 0,
'VALBZ': 0,
'VALE': 0,
'GS': 0,
'MS': 0,
'WFC': 0,
'XLF': 0,
}
order_history = {
'BOND': {},
'VALBZ': {},
'VALE': {},
'GS': {},
'MS': {},
'WFC': {},
'XLF': {},
}
ADR_FEE = 10

ORDER_number = 1
# ~~~~~============== MAIN LOOP ==============~~~~~







def printHelloFromExchange(hello_from_exchange):
    print("type "+ str(hello_from_exchange["type"]))
    for symbol in hello_from_exchange["symbols"]:
        print("type: "+ str(symbol["symbol"]) + "     quantity: " + str(symbol["position"]))




def mean(highest_bid, lowest_offer):
    return (highest_bid+lowest_offer)/2

def parse_from_exchange(from_exchange):
    global ACTIVE
    print(from_exchange.keys())
    if from_exchange["type"] == "hello" :
        printHelloFromExchange(from_exchange)
    if from_exchange["type"] == "open":
        for symbol in from_exchange["symbols"]:
            ACTIVE[symbol] = True
            print(symbol)
    if from_exchange["type"] == "close":
        for symbol in from_exchange["symbols"]:
            ACTIVE[symbol] = False
            print(symbol)
    if from_exchange["type"] == "error":
        print("EEEEEEEEEEERRRRRRRRRRRRRRRRROOOOOOOOOOOR")
        print(from_exchange["error"])
    if from_exchange["type"] == "book":
        cache_symbol = from_exchange["symbol"]
        if cache_symbol == "BOND":
            for i in from_exchange["buy"]:
                BOND_buy.append(i)
            for i in from_exchange["sell"]:
                BOND_sell.append(i)
        if cache_symbol == "VALBZ":
            for i in from_exchange["buy"]:
                VALBZ_buy.append(i)
            for i in from_exchange["sell"]:
                VALBZ_sell.append(i)
        if cache_symbol == "VALE":
            for i in from_exchange["buy"]:
                VALE_buy.append(i)
            for i in from_exchange["sell"]:
                VALE_sell.append(i)
        if cache_symbol == "GS":
            for i in from_exchange["buy"]:
                GS_buy.append(i)
            for i in from_exchange["sell"]:
                GS_sell.append(i)
        if cache_symbol == "MS":
            for i in from_exchange["buy"]:
                MS_buy.append(i)
            for i in from_exchange["sell"]:
                MS_sell.append(i)
        if cache_symbol == "WFC":
            for i in from_exchange["buy"]:
                WFC_buy.append(i)
            for i in from_exchange["sell"]:
                WFC_sell.append(i)
        if cache_symbol == "XLF":
            for i in from_exchange["buy"]:
                XLF_buy.append(i)
            for i in from_exchange["sell"]:
                XLF_sell.append(i)
    if from_exchange["type"] == "trade":
        print("TRADE:"+ from_exchange["symbol"]+ " price "+ str(from_exchange["price"])+" size "+ str(from_exchange["size"]))
    if from_exchange["type"] == "ack":
        print("ORDER NUMBER "+str(from_exchange["order_id"]))
    if from_exchange["type"] == "reject":
        print("reject!!!" + str(from_exchange["order_id"]))
    if from_exchange["type"] == "fill":
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')
        print('=====================================================================')

        print("fill " + str(from_exchange["order_id"]))
        print(from_exchange["symbol"]+" "+from_exchange["dir"]+" "+str(from_exchange["price"])+" "+str(from_exchange["size"]))
        if from_exchange["dir"] == "BUY":
            position_dict[from_exchange["symbol"]] += from_exchange["size"]
            pending_dict[from_exchange["symbol"]] -= from_exchange["size"]
    if from_exchange["type"] == "out":
        print("outttt!!!" + str(from_exchange["order_id"]))


def bondEval(exchange):
    global ORDER_number
    global limit_dict

    #determine how many to sell
    num_to_buy = limit_dict["BOND"] - (position_dict["BOND"] + pending_dict["BOND"])
    num_to_sell = position_dict["BOND"]
    print(" num to but, sell, position, pending")
    print(num_to_buy)
    print(num_to_sell)
    print(position_dict["BOND"])
    print(pending_dict["BOND"])
    if(position_dict["BOND"] > -20):
        write_to_exchange(exchange, {"type": "add", "order_id": ORDER_number, "symbol": "BOND", "dir": "SELL", "price": 1001, "size": num_to_sell})
        ORDER_number += 1
        read_from_exchange(exchange)
        print("ORDER EXEC")
    #position_dict["BOND"] -= 5
    if num_to_buy > 0 and (position_dict["BOND"] - pending_dict["BOND"]) < 20:
        write_to_exchange(exchange, {"type": "add", "order_id": ORDER_number, "symbol": "BOND", "dir": "BUY", "price": 999, "size": num_to_buy})
        ORDER_number += 1
        pending_dict["BOND"] += 5
        read_from_exchange(exchange)
        print("ORDER EXEC BUY")
    print("position for bonds: "+str(position_dict["BOND"]))

def adrEval(exchange):
    global ORDER_number
    global VALBZ_buy
    global VALBZ_sell
    global VALE_buy
    global VALE_sell
    global PROD
    global ADR_FEE
    CONVERSION_NUMBER = 2
    fair_VALE = int(fair_value(VALE_buy, VALE_sell))
    fair_VALBZ = mean(VALBZ_sell)
    print(str(fair_VALE)+ " "+ str(fair_VALBZ))
    print("please i am here")
    if (fair_VALBZ*CONVERSION_NUMBER) < ((fair_VALE*CONVERSION_NUMBER)+ADR_FEE):
        print("============================================================================")
        print("herer")
        print(str(fair_VALE) + " " + str(fair_VALBZ))
        ORDER_number += 1
        write_to_exchange(exchange, {"type": "add", "order_id": ORDER_number, "symbol": "VALE", "dir": "BUY", "price": fair_VALE  + 1, "size": CONVERSION_NUMBER})
        read_from_exchange(exchange)
        ORDER_number += 1
        write_to_exchange(exchange, {"type": "convert", "order_id": ORDER_number, "symbol": "VALE", "dir": "SELL",  "size": CONVERSION_NUMBER})
        read_from_exchange(exchange)
        ORDER_number += 1
        if position_dict["VALBZ"] > 2:
            write_to_exchange(exchange, {"type": "add", "order_id": ORDER_number, "symbol": "VALBZ", "dir": "SELL", "price": fair_VALBZ - 1, "size": 2})
            read_from_exchange(exchange)
            ORDER_number += 1
    if position_dict["VALBZ"] > 2:
        write_to_exchange(exchange, {"type": "add", "order_id": ORDER_number, "symbol": "VALBZ", "dir": "SELL", "price": fair_VALBZ - 1, "size": 2})
        read_from_exchange(exchange)
        ORDER_number += 1


def stockEval(exchange):
    global ORDER_number
    global limit_dict
    #determine how many to sell
    for stock_name in ACTIVE.keys():
        num_to_buy = limit_dict[stock_name] - (position_dict[stock_name] + pending_dict[stock_name])
        num_to_sell = position_dict[stock_name]

        if stock_name == "BOND":
            continue
        elif stock_name == "VALBZ":
            buy = VALBZ_buy
            sell = VALBZ_sell
        elif stock_name == "VALE":
            buy = VALE_buy
            sell = VALE_sell

        elif stock_name == "GS":
            buy = GS_buy
            sell = GS_sell

        elif stock_name == "MS":
            buy = MS_buy
            sell = MS_sell

        elif stock_name == "WFC":
            buy = WFC_buy
            sell = WFC_sell
        elif stock_name == "XLF":
            buy = XLF_buy
            sell = XLF_sell

        print(" num to but, sell, position, pending")
        print(num_to_buy)
        print(num_to_sell)
        print(position_dict[stock_name])
        print(pending_dict[stock_name])
        fair_sell = mean(sell)
        fair_buy = fair_value(buy, sell)

        if(position_dict[stock_name] > -20):
            write_to_exchange(exchange, {"type": "add", "order_id": ORDER_number, "symbol": stock_name, "dir": "SELL", "price": fair_buy + 1, "size": num_to_sell})
            ORDER_number += 1
            read_from_exchange(exchange)
            print("ORDER EXEC")
        #position_dict["BOND"] -= 5
        if num_to_buy > 0:
            write_to_exchange(exchange, {"type": "add", "order_id": ORDER_number, "symbol": stock_name, "dir": "BUY", "price": fair_buy - 1 , "size": num_to_buy})
            ORDER_number += 1
            pending_dict[stock_name] += num_to_buy
            read_from_exchange(exchange)
            print("ORDER EXEC BUY")
        print("position for "+stock_name+": "+str(position_dict[stock_name]))

def mean(x):
    if len(x)>10:
        x = x[-10:]
    big_boy = 0
    if len(x) == 0:
        return 0
    for i in x:
        big_boy += i[0]
    return big_boy//len(x)
def fair_value(VAL_buy, VAL_sell):
    #calculate the fair value
    #loop therough last 10 of buys and sells in order to calcualte the fair value
    #return the average divided by 2
    VAL_max = 0
    VAL_min = 999999999999
    if len(VAL_buy)>10 and len(VAL_sell)> 10:
        small_buy = VAL_buy[-10:]
        small_sell = VAL_buy[-10:]
    else:
        small_buy = VAL_buy
        small_sell = VAL_sell
    for one in small_buy:
        if one[0] > VAL_max:
            VAL_max = one[0]

    for one in small_sell:
        if one[0] < VAL_min:
            VAL_min = one[0]


    # for i in range (0, len(VAL_buy)):
    #     if 1.5 * VAL_buy[i] < VAL_max:
    #         VAL_max = VALE_buy[i]


    VAL_fair =  (VAL_min + VAL_max) / 2
    return VAL_fair

def every_exchange_in_one(exchange):
    from_exchange = read_from_exchange(exchange)
    print("read from exchange")
    print(from_exchange)
    parse_from_exchange(from_exchange)

def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    print(read_from_exchange(exchange))
    while True:
        every_exchange_in_one(exchange)
        stockEval(exchange)
        #adrEval(exchange)
        bondEval(exchange)


    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!


if __name__ == "__main__":
    main()
