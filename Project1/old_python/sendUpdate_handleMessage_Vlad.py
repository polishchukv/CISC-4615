def SendUpdate() # My logic was that you could just plop this inside of UpdateRouteCost, and just call it once updates have been made
    #send to link1
    s.sendto(bytes(json.dumps(config_dict),'utf8'),(config_dict['link1']['ip'],int(config_dict['link1']['port'])))

    #send to link2
    s.sendto(bytes(json.dumps(config_dict),'utf8'),(config_dict['link2']['ip'],int(config_dict['link2']['port'])))

    print("\nSent updates to neighbors.")

def HandleMessage()
    # 1) Accept incoming data package - need to modify main while loop to trigger this func whenever transmission is received
    # 2) Check whether received data matches own data --> could probably use the same process as in UpdateRouteCost
    #       2.1) If yes, update own data
    #       2.2) If no, let the user know that the data is the same