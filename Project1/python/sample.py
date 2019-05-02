import configparser

config = configparser.ConfigParser()
print(config.sections())

config.read('a.ini')

print("Sections: ")
print(config.sections())
print("\nWithin node, name: ")
print(config['node']['name'])

config.set('node', 'name', 'Node_test')

with open('a.ini', 'w') as configfile:
	config.write(configfile)
	
print(config['node']['name'])
