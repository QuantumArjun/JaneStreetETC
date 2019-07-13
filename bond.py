def bondEval(max_limit, position, pending):
    #determine how many to sell
    num_to_buy = max_limit[0] - (position[0] + pending[0])
    num_to_sell = position[0] - pending[0]
    return num_to_buy, num_to_sell
    {"type": "add", "order_id": 5, "symbol": "BOND", "dir": "BUY", "price": 999, "size": num_to_buy}
    {"type": "add", "order_id": 5, "symbol": "BOND", "dir": "SELL", "price": 1001, "size": num_to_sell}


#determine how many orders you have
#fullfill the rest with buy orders and sell orders



order_id = {5, [3, -4]}