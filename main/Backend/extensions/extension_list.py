import requests
import json
import ast
index = "https://raw.githubusercontent.com/Halludba71/Shogun-Extensions/main/extension_list.json"

def ext_list():
        try:
                request = requests.get(index)
                all_extensions = json.loads(request.text)
                return all_extensions
        except:
                return -1
        
    
