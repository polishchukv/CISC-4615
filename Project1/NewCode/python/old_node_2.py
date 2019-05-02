import socket
import json
import operator
import sys
import binascii
import struct
import threading
import configparser

def is_diff(obj1,obj2): # checks whether two nodes are different
    if obj1 == None or obj2 == None: # if blank, return false
        return False
    str1 = json.dumps(obj1) # json.dumps takes an object and produces a string
    str2 = json.dumps(obj2)
    return str1 != str2 # if obj1 is different from obj2, return true

def print_table(obj): # prints out the table for input obj
    if obj == None:
        print(">>>>>> table is empty <<<<<<<<")
        return
    print('>>>> ' + obj['node']['name'] + ' routing table <<<<')
    print('-------------------------------------------------------')
    print('|   destination   |    link cost    |    next hop     |')
    print('|    %-13s|    %-13s|    %-13s|' % (obj['link1']['name'],obj['link1']['cost'],obj['link1']['name']))
    print('|    %-13s|    %-13s|    %-13s|' % (obj['link2']['name'],obj['link2']['cost'],obj['link2']['name']))
    print('-------------------------------------------------------')

def print_diff(obj1,obj2): # checks if the objects are different, if they are then print out changes
    if obj1 == None or obj2 == None:
        return
    if is_diff(obj1,obj2):
        print("Before Update Table")
        print_table(obj1)
        print("After Update Table")
        print_table(obj2)
        
        for k in obj1:
            if k == "node":
                continue
            if obj2[k]['cost'] != obj1[k]['cost']:   # str() converts int to str
                print("Node " + obj2[k]['name'] + " cost changed from " + str(obj1[k]['cost']) + " to " + str(obj2[k]['cost']))
    else:
        print("Node " + obj1['node']['name'] + " routing table not changed")

def save_table(table): 
    global node_configs
    node_configs[table['node']['name']] = table

def listen_thread(port): # UDP constantly listening for incoming data
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", port))
    while True:
        data, addr = s.recvfrom(1024)
        print(data)

def send(str,ip,port): # Sends node info to specified neighboring node (given IP and Port #)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(bytes(str,'utf8'),(ip,port))

class RecvThread(threading.Thread): # Receives data, decodes it and places into dict, then ?? 
    def __init__(self,port):
        super(RecvThread, self).__init__()
        self.port = port

    def run(self):
        global node_configs
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("0.0.0.0", self.port))
        while True:
            data, addr = s.recvfrom(1024)
            print("Recv: ");
            dict = json.loads(str(data,encoding='utf-8')) 
            print_table(dict)
            name = dict['node']['name']
            old = None
            if name in node_configs: # **Clarify w/ professor**
                old = node_configs[name]
            node_configs[name] = dict
            print_diff(old,dict)
            print("Input command(load,send,bye):")

class MyParser(configparser.ConfigParser): # **Overwriting existing imported functionality??**
    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
            d[k].pop('__name__', None)
        return d

if len(sys.argv) != 2: # Checking for correct arguments during launch
    print("Useage: python " + sys.argv[0] + " <confg file>")
    sys.exit(-1)

def load_ini(file): # Self-explanatory, loading in specified (during launch) ini config file and turning it into dict
    cf = MyParser()
    cf.read(file)
    return cf.as_dict()

config_dict = load_ini(sys.argv[1])
listen_port = int(config_dict['node']['port'])
#run recv thread
t = RecvThread(int(listen_port))
t.setDaemon(True)
t.start()
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
node_configs = {}

def send(): # Sends info to neighboring nodes
    global s
    #send to link1
    s.sendto(bytes(json.dumps(config_dict),'utf8'),(config_dict['link1']['ip'],int(config_dict['link1']['port'])))
    #send to link2
    s.sendto(bytes(json.dumps(config_dict),'utf8'),(config_dict['link2']['ip'],int(config_dict['link2']['port'])))
    print("Send config finished")


def load(ini): # Loading specified file through config parser
    config_dict = load_ini(ini)
    print("Load config file finished")

def UpdateRouteCost(node,cost): # Updates local node file
    if not cost.isdigit(): # Check whether cost input is correct
        print("Cost is not number")
        return
    found = False
    for k in config_dict:
        if k == "node":
            continue
        v = config_dict[k]
        tmp_name = v['name']
        if tmp_name.lower() == name:
            v['cost'] = cost
            found = True
    if not found:
        print("Node <" + name + "> not found in table")
    else:
        send()

def ReConstructRoutingTable(): # Function used to execute Bellman Ford Alg + update routing table based on UpdateRouteCost or receiving an update

def SendUpdate(): # Should be called whenever a node has updated your routing table
    # Already exists? This may be the send function already present/used in UpdateRouteCost

def HandleMessage(): # Should be called whenever the node receives a message from neighbors
    # Calls ReConstructRoutingTable?

while True:
    print("Input command(load,send,bye,myroutingtable,update):")
    text = sys.stdin.readline().strip().lower()
    if text == "send":
        send()
    elif text == "load":
        load(sys.argv[1])
    elif text == "bye":
        break
    elif text == "myroutingtable":
        print_table(config_dict)
    elif text.startswith("update"):
        cmds = text.split(" ")
        if len(cmds) != 3:
            print("Update command usage:update <node name> <cost>")
            continue
        name = cmds[1]
        cost = cmds[2]
        UpdateRouteCost(name,cost)           
    elif text == "print":
        print_table(config_dict)
    else:
        print("Invalid command")