import json

with open(f"config.json", "r") as cf:
    config = json.load(cf)
    cf.close()

token = config['client']['token']
prefix = config['client']['prefix']
cogs = config['client']['cogs']
owners = config['client']['owners']