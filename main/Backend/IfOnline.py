"""
Function to check if there is an active internet connection, 
If True, values from database will be updated

If False, then values from the database will not be updated.
"""

import urllib.request

def connected(host='http://google.com'):
    try:
        urllib.request.urlopen(host) #Python 3.x
        return True
    except:
        return False

# test
# print(connect())