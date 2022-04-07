from flask import Flask, send_file, request, redirect
from flask_cors import CORS
import time
import json

app = Flask(__name__)
cors = CORS(app)
last_online = {}
queue = {}


@app.route('/')
def index():
    return "See https://github.com/GSGTafelManager/ServiceClientData/blob/main/README.md"

@app.route('/file/<path:path>')
def file(path):
    return redirect("https://raw.githubusercontent.com/GSGTafelManager/ServiceClientData/main/" + path)

@app.route('/ifile/<path:path>')
def ifile(path):
    return send_file("./files/" + path)

@app.route('/installer')
def installer_dot_py():
    return file("installer.py")

@app.route('/online/<string:tafelid>')
def online(tafelid):
    try:
        return repr(last_online[tafelid] > (int(time.time()) - 10))
    except KeyError:
        return repr(False)

@app.route('/online')
def online_all():
    result = []
    for tafelid in last_online:
        if last_online[tafelid] > (int(time.time()) - 10):
            result.append({"id": tafelid, "last": last_online[tafelid]})
    return {"online": result, "IMPORTANT! READ THIS": "https://github.com/GSGTafelManager/ServiceClientData/blob/main/README.md"}

@app.route('/send/<string:tafelid>', methods=["POST"])
def send_cmd(tafelid):
    if tafelid not in queue.keys():
        queue[tafelid] = []
    req = request.get_json(force=True)
    if tafelid == "__ignore":
        return {"status": "ignored", "command": req}
    with open("/home/GSGTafelManager/mysite/rights.json", "r") as file:
        rights = json.load(file)["users"]
    for right in rights:
        if req["key"] == right["key"]:
            if any([tafelid.startswith(prefix) for prefix in right["prefixes"]]):
                req.update({"timestamp": time.time()})
                queue[tafelid].append(req)
                return {"status": "sent", "command": req}
            else:
                return {"status": "blocked: forbidden prefix", "command": req}
    return {"status": "blocked: invalid key", "command": req, "IMPORTANT! READ THIS": "https://github.com/GSGTafelManager/ServiceClientData/blob/main/README.md"}


@app.route('/q/<string:tafelid>', methods=["POST"])
def q(tafelid):
    last_online[tafelid] = time.time()
    if tafelid not in queue.keys():
        queue[tafelid] = []
    queue[tafelid] = list(filter(lambda qe: qe["timestamp"] not in request.get_json(force=True)["executed"], queue[tafelid]))
    return {"commands": queue[tafelid], "IMPORTANT! READ THIS": "https://github.com/GSGTafelManager/ServiceClientData/blob/main/README.md"}

if __name__ == "__main__":
    app.run("0.0.0.0", 80)
