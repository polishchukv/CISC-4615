import socket
import json
import operator
import sys
import binascii
import struct
import threading
import configparser
import copy

def is_diff(obj1, obj2):
    if obj1 == None or obj2 == None:
        return False
    for k in obj1:
        if k == 'node':
            continue
        if obj1[k]['cost'] != obj2[k]['cost']:
            return True
    return False

def print_table(obj):
    if obj == None:
        print(">>>>>> table is empty <<<<<<<<")
        return
    dest1 = obj['link1']['name']
    cost1 = obj['link1']['cost']
    next_hop1 = obj['link1']['next_hop']

    dest2 = obj['link2']['name']
    cost2 = obj['link2']['cost']
    next_hop2 = obj['link2']['next_hop']

    print('>>>> ' + obj['node']['name'] + ' routing table <<<<')
    print('-------------------------------------------------------')
    print('|   destination   |    link cost    |    next hop     |')
    print('|    %-13s|    %-13s|    %-13s|' % (dest1, cost1, next_hop1))
    print('|    %-13s|    %-13s|    %-13s|' % (dest2, cost2, next_hop2))
    print('-------------------------------------------------------')

def print_diff(obj1, obj2):
    if obj1 == None or obj2 == None:
        return
    if is_diff(obj1, obj2):
        print("Before Update Table")
        print_table(obj1)
        print("After Update Table")
        print_table(obj2)

        for k in obj1:
            if k == "node":
                continue
            if obj2[k]['cost'] != obj1[k]['cost']:
                print("Node " + obj2[k]['name'] + " cost changed from " + str(obj1[k]['cost']) + " to " + str(
                    obj2[k]['cost']))
    else:
        print("Node " + obj1['node']['name'] + " routing table not changed")

def save_table(table):
    global node_configs
    node_configs[table['node']['name']] = table

def listen_thread(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("0.0.0.0", port))
    while True:
        data, addr = s.recvfrom(1024)
        print(data)

def send(str, ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.sendto(bytes(str, 'utf8'), (ip, port))

class RecvThread(threading.Thread):
    def __init__(self, port):
        super(RecvThread, self).__init__()
        self.port = port

    def run(self):
        global node_configs, config_dict
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("0.0.0.0", self.port))
        while True:
            data, addr = s.recvfrom(1024)
            print("Recv: ");
            dict = json.loads(str(data, encoding='utf-8'))
            name = dict['node']['name']
            old = None
            if name in node_configs:
                old = node_configs[name]
            reconstruct(config_dict, dict)
            print_diff(old, dict)
            print("Input command(FirstLoad,FirstSend,Bye,MyRoutingTable,UpdateRouteCost):")

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
    table = cf.as_dict()
    table['link1']['next_hop'] = table['link1']['name']
    table['link2']['next_hop'] = table['link2']['name']
    return table

config_dict = load_ini(sys.argv[1])
listen_port = int(config_dict['node']['port'])
# run recv thread
t = RecvThread(int(listen_port))
t.setDaemon(True)
t.start()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

node_configs = {}

def send():
    global s
    # send to link1
    s.sendto(bytes(json.dumps(config_dict), 'utf8'), (config_dict['link1']['ip'], int(config_dict['link1']['port'])))
    # send to link2
    s.sendto(bytes(json.dumps(config_dict), 'utf8'), (config_dict['link2']['ip'], int(config_dict['link2']['port'])))
    print("Send config finished")

def load(ini):
    config_dict = load_ini(ini)
    print("Load config file finished")

def update_cost(node, cost):
    if not cost.isdigit():
        print("Cost is not number")
        return
    found = False
    for k in config_dict:
        if k == "node":
            continue
        v = config_dict[k]
        tmp_name = v['name']
        if tmp_name == name:
            v['cost'] = cost
            found = True
    if not found:
        print("Node <" + name + "> not found in table")
    else:
        send()

def handle(old, dict):
    node = dict['node']['name']
    curr = old['node']['name']
    for link in dict:
        if link == 'node':
            continue
        if dict[link]['name'] == curr:
            for link2 in old:
                if link2 == 'node':
                    continue
                if old[link2]['name'] == node:
                    old[link2]['cost'] = dict[link]['cost']
    save_table(old)
    return old


def reconstruct(old, dict):
    old2 = copy.deepcopy(old)
    new_old = handle(old, dict)
    for k in new_old:
        if k == 'node':
            continue
        for x in dict:
            if x == 'node':
                continue
            if new_old[k]['name'] != dict[x]['name']:
                if int(new_old[x]['cost']) > (int(new_old[k]['cost']) + int(dict[x]['cost'])):
                    new_old[x]['cost']= int(new_old[k]['cost']) + int(dict[x]['cost'])
                    new_old[x]['next_hop'] = new_old[k]['name']
    save_table(new_old)
    if is_diff(old2,new_old):
        send()
    print_table(new_old)

while True:
    print("Input command(FirstLoad,FirstSend,Bye,MyRoutingTable,UpdateRouteCost):")
    text = sys.stdin.readline().strip()
    if text == "FirstSend":
        send()
    elif text == "FirstLoad":
        load(sys.argv[1])
    elif text == "Bye":
        break
    elif text == "MyRoutingTable":
        print_table(config_dict)
    elif text.startswith("UpdateRouteCost"):
        cmds = text.split(" ")
        if len(cmds) != 3:
            print("Update command usage:UpdateRouteCost <node name> <cost>")
            continue
        name = cmds[1]
        cost = cmds[2]
        update_cost(name, cost)
    else:
        print("Invalid command")