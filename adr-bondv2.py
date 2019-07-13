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
test_mode = False

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index=0
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
    print("HERERE")
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

        bondEval(exchange)


    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!


if __name__ == "__main__":
    main()
