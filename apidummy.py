from genapi import genApiHandler
import json
import sqlite3

with open("api_conf.json", "r") as f:
    file = f.read()

conf = json.loads(file)
sqliteConnection = sqlite3.connect('database.db')

handler = genApiHandler(None, conf)
r = handler.handle_request("GET","/seller",{'fields': ['seller_id'], "filters": [{"seller_id": 123}, {"seller_id": 324, "contact_number": "aaa"}]})
print(r)