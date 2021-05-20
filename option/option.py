import json
import os

RESOURCE_DIR = 'resource'

class Option:

    def __init__(self, opt_name: str):
        base = os.path.abspath(__file__)
        if opt_name.find('.') == -1:
            opt_name += ".json"
        opt_path = os.path.join(base, RESOURCE_DIR, opt_name)

        with open(opt_path, 'r', encoding='utf-8', errors='replace') as f:
            option = json.loads(f.read())
        
        vars(self).update(option)
