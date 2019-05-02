import socket
import json
import operator
import sys
import binascii
import struct
import threading
import configparser

def print_table(obj):
    print('>>>> ' + obj['node']['name'] + ' routing table <<<<')
    print('-------------------------------------------------------')
    print('|   destination   |    link cost    |    next hop     |')
    print('|    %-13s|    %-13s|    %-13s|' % (obj['link1']['name'],obj['link1']['cost'],obj['link1']['name']))
    print('|    %-13s|    %-13s|    %-13s|' % (obj['link2']['name'],obj['link2']['cost'],obj['link2']['name']))
    print('-------------------------------------------------------')

def listen_thread(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", port))
    while True:
        data, addr = s.recvfrom(1024)
        print(data)

def send(str,ip,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(bytes(str,'utf8'),(ip,port))

class RecvThread(threading.Thread):
    def __init__(self,port):
        super(RecvThread, self).__init__()
        self.port = port

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("0.0.0.0", self.port))
        while True:
            data, addr = s.recvfrom(1024)
            print("Recv: ");
            print_table(json.loads(str(data,encoding='utf-8')))
            print("Input command(FirstLoad, FirstSend, Bye, or MyRoutingTable):")

class MyParser(configparser.ConfigParser):
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
            d[k].pop('__name__', None)
        return d

if len(sys.argv) != 2:
    print("Useage: python " + sys.argv[0] + " <confg file>")
    sys.exit(-1)

def load_ini(file):
    cf = MyParser()
    cf.read(file)
    return cf.as_dict()

def UpdateRouteCost(input_node, input_cost):
    # Two tasks:
    # 1) Check whether the node/cost belong to link1 or link2
    # 2) Check whether the cost differs
    #       2.1) If it does, alter cost
    #       2.2) If cost is altered, update neighbors (send function)

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


config_dict = load_ini(sys.argv[1])
listen_port = int(config_dict['node']['port'])
#run recv thread
t = RecvThread(int(listen_port))
t.setDaemon(True)
t.start()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    print("Input command(FirstLoad,Send,Bye, or MyRoutingTable):")
    text = sys.stdin.readline().strip()

    if text == "FirstSend":
        #send to link1
        s.sendto(bytes(json.dumps(config_dict),'utf8'),(config_dict['link1']['ip'],int(config_dict['link1']['port'])))
        #send to link2
        s.sendto(bytes(json.dumps(config_dict),'utf8'),(config_dict['link2']['ip'],int(config_dict['link2']['port'])))
        print("Send config finished")

    elif text == "FirstLoad":
        config_dict = load_ini(sys.argv[1])
        print("Load config file finished")

    elif text == "Bye":
        break

    elif text == "MyRoutingTable":
        print_table(config_dict)

    elif text == ("UpdateRouteCost" + node + cost):   
        UpdateRouteCost(node, cost)

    else:
        print("Invalid command")
