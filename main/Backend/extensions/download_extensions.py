import requests
import os
from main.models import extension

def download_extension(extension_data):
        path = f"{os.getcwd()}/main/Backend/extensions/{extension_data['Name']}/"
        source = requests.get(extension_data["source"])
        print(path)
        if not os.path.exists(path):
            os.mkdir(path)
        with open(path+"source.py", "wb") as script:
            script.write(source.content)
            
        Extension = extension(name=extension_data['Name'], path=path+"source.py")
        Extension.save()

    