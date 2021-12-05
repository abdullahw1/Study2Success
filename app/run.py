#!/usr/bin/env python3
import threading
import webbrowser
from myapp import myapp_obj, db

DEBUG = True
PORT_NUMBER = 5000

def launch_browser():
    webbrowser.open(f'http://localhost:{PORT_NUMBER}', new=0)


# Create *.db file from schema (if doesn't exists)
db.create_all()

if not DEBUG:
    threading.Timer(1, launch_browser).start()
# Run flask app server
myapp_obj.run(debug=DEBUG, port=PORT_NUMBER)
