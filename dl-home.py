#!/usr/bin/env python

from bottle import abort, route, run, request, static_file
from os import path
import os, subprocess, json, sys
import threading, time

# use your intra guacamole app secret

dl_lock = threading.Lock()

"""
Open and load a file at the json format
"""

CONFIG_FILE = 'config.json'

def open_and_load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as config_file:
            return json.loads(config_file.read())
    else:
        print("File [%s] doesn't exist, aborting." % (CONFIG_FILE))
        sys.exit(1)

def check_login(key, login):
    if (key != config["KEY"]):
        abort(401, "Sorry, access denied.")
    if (not path.exists(config["PATH"] % login)):
        abort(404, "Not found")
        
@route('/dl/<key>/<login>')
def dl(key, login):
    check_login(key, login)
    # one at a time
    if dl_lock.acquire(False):
        subprocess.call(["./img2tgz.sh", login])
        dl_lock.release()
        return static_file("%s.tar.gz" % login, root="/tmp/img2tgz/")
    else:
        abort(503, "Service busy, try again later")

@route('/check/<key>/<login>')
def check(key, login):
    check_login(key, login)
    return "ok"

if __name__ == "__main__":
    config = open_and_load_config()
    run(host=config["HOST"], port=config["PORT"], debug=True)
