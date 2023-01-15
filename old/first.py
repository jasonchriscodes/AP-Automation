from pywinauto.application import Application 
from pywinauto import backend
import time
import os,sys

def get_handle(backend,appname):
    root = backend.registry.backends["uia"].element_info_class()
    handle = 0
    for w in root.children():
        print(w.name)
        if(w.name==appname):
            handle=w.handle
            break
    return handle

#os.system(r"G:\CentraBaseplanRemoteApp.rdp")
app = Application().start(r'"C:\Program Files (x86)\Baseplan\BPEnterprise.exe" forceselectedcompany, Centra')
time.sleep(10)
handle_app = get_handle(backend,"Login (Remote)")
print("Found handle is :" + str(handle_app))
if handle_app!=0:
    app = Application().connect(handle=handle_app)
    login = app.top_window()

    #app.window(title="Login (Remote)").LOGIN.click()
    login.print_control_identifiers()
else:
    print ( "Application did not launch")    
