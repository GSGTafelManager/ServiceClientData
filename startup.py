import sentry_sdk
sentry_sdk.init("https://8b78151ad1da4102805eefb4a8fa8606@o1185419.ingest.sentry.io/6303999", release="GSGTMServiceLauncher@1.0.0", traces_sample_rate=1.0)
try:
    import pathlib
    import requests
    code = requests.get("https://gsgtafelmanager.pythonanywhere.com/file/main.py").content
    with open(str(pathlib.Path(__file__).parent / "main.pyw"), "wb") as f:
        f.write(code)
    while True:
        try:
            import main
        except:
            continue
except Exception as e:
    sentry_sdk.capture_exception(e)
