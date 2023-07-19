import re
import os
import time
import requests
from pymongo import MongoClient

# Set up MongoDB connection
mongo_client = MongoClient('mongodb://your_mongodb_uri')
db = mongo_client['your_database_name']
collection = db['reversed_urls']

class REV:
    def reverse(self, cidr):
        total = ""
        page = 0
        urx = f'https://rapiddns.io/s/{cidr}?full=1&down=1#result'
        try:
            r = requests.get(urx, verify=False, allow_redirects=False)
            resp = re.sub("<th scope=\"row \">.*", ">>>>>>>>>>>>>>>>>>urx", r.text).replace(
                "<div style=\"margin: 0 8px;\">Total: <span style=\"color: #39cfca; \">", "XP>>>>>>>>>>>>>").replace(
                "</span></div>", "")
            urxc = resp.splitlines()
            urls = ""
            nm = 0
            for xc in urxc:
                nm += 1
                if ">>>>>>>>>>>>>>>>>>urx" in xc:
                    urls = urls + urxc[nm] + "\n"

            # Store data in MongoDB
            data = {
                "cidr": cidr,
                "urls": urls.replace("<td>", "").replace("</td>", "")
            }
            collection.insert_one(data)
            print(f"[SAVED] : {cidr}")
        except Exception as e:
            print(e)

if __name__ == '__main__':
    # Read the input from the text file
    with open('iplistted.txt', 'r') as urlList:
        argFile = urlList.read().splitlines()

    for data in argFile:
        REV().reverse(data)
        time.sleep(10)
