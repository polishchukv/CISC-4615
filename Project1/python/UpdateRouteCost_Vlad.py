def UpdateRouteCost(input_node, input_cost):
    # Two tasks:
    # 1) Check whether the node/cost belong to link1 or link2
    # 2) Check whether the cost differs
    #       2.1) If it does, alter cost
    #       2.2) If cost is altered, update neighbors (sendUpdate function)

    if config_dict['link1']['name'] == input_node: # Check if belongs to link1

        if config_dict['link1']['cost'] != input_cost: # Only update cost if it isn't the same
            config_dict.set('link1', 'cost', input_cost) #Set new cost, now need to update file **UNSURE ABOUT CODE BELOW**

            with open('a.ini', 'w') as configfile:
                config_dict.write(configfile)

            send(json.dumps(config_dict), config_dict['link1']['ip'], config_dict['link1']['port']) # Update neighbors, **UNSURE ABOUT PARAMETERS**

        else:
            print("\nCost is unchanged, will not alter. User must enter a different cost.")

    elif config_dict['link2']['name'] == input_node: # Check if belongs to link2
        
        if config_dict['link2']['cost'] != input_cost: # Only update cost if it isn't the same
            config_dict.set('link2', 'cost', input_cost) #Set new cost, now need to update file **UNSURE ABOUT CODE BELOW**

            with open('a.ini', 'w') as configfile:
                config_dict.write(configfile)

            send(json.dumps(config_dict), config_dict['link2']['ip'], config_dict['link2']['port']) # Update neighbors, **UNSURE ABOUT PARAMETERS**

        else:
            print("\nCost is unchanged, will not alter. User must enter a different cost.")

    else: # Otherwise: incorrect input, specifying own node
        print("\nCannot update route cost, specified node is open one.")

def SendUpdate()
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