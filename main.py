import os
import glob
os.remove(__file__)
try:
    for file in glob.glob(str(current / "__pycache__") + r"\*.pyc"):
        os.remove(file)
    os.rmdir(str(current / "__pycache__"))
except:
    pass


import sentry_sdk
sentry_sdk.init("https://8b78151ad1da4102805eefb4a8fa8606@o1185419.ingest.sentry.io/6303999", release="GSGTMService@1.1.2", traces_sample_rate=1.0)


import requests
import time
import pathlib
from selenium import webdriver
import subprocess
from selenium.webdriver.chrome.options import Options
import pyderman
import pynput
import threading

current = pathlib.Path(__file__).parent
path = pathlib.Path(__file__).absolute().parent.parent / "GSGTM"
os.makedirs(str(path), exist_ok=True)
version = ""
for f in filter(os.path.isdir, os.listdir(r"C:\Program Files\Google\Chrome\Application")):
    if f != "SetupMetrics":
        version = f
driver_path = pyderman.install(browser=pyderman.chrome, file_directory=str(path))


try:
    with open(str(path / "tafelid.txt"), "r") as tfid:
        tafelid = tfid.read()
except FileNotFoundError:
    tafelid = "setup-" + str(round(time.time()))
    with open(str(path / "tafelid.txt"), "w") as tfid:
        tfid.write(tafelid)

executed_cmds = []


def execute(command):
    global executed_cmds, tafelid
    try:
        if command["timestamp"] in executed_cmds:
            return
        executed_cmds.append(command["timestamp"])
        if command["exec"] == "changeid":
            tafelid = command["newid"]
            with open(str(path / "tafelid.txt"), "w") as tfid:
                tfid.write(tafelid)
        elif command["exec"] == "py":
            exec(command["code"])
        elif command["exec"] == "popup":
            from tkinter.messagebox import showinfo, showerror, showwarning
            if command["type"] == "info":
                showinfo(command["title"], command["msg"])
            elif command["type"] == "error":
                showerror(command["title"], command["msg"])
            elif command["type"] == "warning":
                showwarning(command["title"], command["msg"])
        elif command["exec"] == "open-url":
            chrome_options = Options()
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            if command["mode"] == "kiosk":
                chrome_options.add_argument("--kiosk");
            if command["mode"] == "fullscreen":
                chrome_options.add_argument("--start-fullscreen");
            service = webdriver.chrome.service.Service(driver_path)
            service.creationflags = subprocess.CREATE_NO_WINDOW
            driver = webdriver.Chrome(executable_path=driver_path, service=service, chrome_options=chrome_options)
            driver.get(command["url"])
            try:
                driver.switch_to.window(driver.window_handles[0])
            except IndexError:
                pass
        elif command["exec"] == "close-app":
            con = pynput.keyboard.Controller()
            con.press(pynput.keyboard.Key.alt)
            con.press(pynput.keyboard.Key.f4)
            con.release(pynput.keyboard.Key.f4)
            con.release(pynput.keyboard.Key.alt)
        elif command["exec"] == "os":
            os.system(command["code"])
    except Exception as e:
        sentry_sdk.capture_exception(e)

while True:
    try:
        for file in glob.glob(str(current / "__pycache__") + r"\*.pyc"):
            os.remove(file)
        os.rmdir(str(current / "__pycache__"))
    except:
        pass
    try:
        commands = requests.post("https://gsgtafelmanager.pythonanywhere.com/q/" + tafelid, json={"executed": executed_cmds}).json()["commands"]
    except JSONDecodeError as e:
        time.sleep(10)
        continue
    except Exception as e:
        sentry_sdk.capture_exception(e)
        time.sleep(10)
        continue
    executed_cmds = []
    for command in commands:
        threading.Thread(target=execute, args=(command,)).start()
    time.sleep(5)
   
