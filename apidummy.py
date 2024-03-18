from genapi import genApiHandler
import json
import sqlite3

with open("api_conf.json", "r") as f:
    file = f.read()

conf = json.loads(file)
sqliteConnection = sqlite3.connect('database.db')

handler = genApiHandler(None, conf)
r = handler.handle_request("GET","/no",{})
print(r)