from pywinauto.application import Application 
from pywinauto import backend
from pywinauto import mouse
from pywinauto import win32structures
import time
import os,sys

def get_handle(backend,appname):
    handle = 0
    maxtries = 10
    currtry = 0
    while (handle==0 and currtry<maxtries):
        root = backend.registry.backends["uia"].element_info_class()
        handle = 0
        for w in root.children():
            print(w.name)
            if(w.name==appname):
                handle=w.handle
                break
        time.sleep(1)  
        currtry = currtry + 1      
    return handle

#os.system(r"G:\CentraBaseplanRemoteApp.rdp")
app = Application().start(r'"C:\Program Files (x86)\Baseplan\BPEnterprise.exe" forceselectedcompany, CentraTest')
#app = Application().start(r"C:\Program Files (x86)\Baseplan\BPEnterprise.exe")
#time.sleep(10)
handle_app = get_handle(backend,"Login")
print("Found handle is :" + str(handle_app))

#app.Login.LOGIN.click()
app.Login.Edit2.set_text("Tekapo02")
app.Login.LOGIN.click()

handle_app = get_handle(backend,"Baseplan Enterprise")
app.BasePlanEnterprise.Edit.type_keys("Invoicing",with_spaces=True)
time.sleep(1)
#app.BasePlanEnterprise.print_control_identifiers(depth=2)
#app.BaseplanEnterprise. child_window(auto_id="MainMenuPanelNew", control_type="BPControlSuite3.BPCollapsibleMenuPanel").print_control_identifiers(depth=7,filename="menus.txt")
menu = app.BaseplanEnterprise.child_window(auto_id="MainMenuPanelNew", control_type="BPControlSuite3.BPCollapsibleMenuPanel")
#menu.draw_outline(colour='red',thickness=3)
items = menu.children()
menuResults = ""
#treeObjectClass = "BPControlSuite3.BPTreeView"
treeObjectClass = "BPControlSuite3.BPSearchResultsListView"
print ("-------------getting search results object-----------------------")
for item in items:
    #print("class name:" + item.control_type())
    if(item.control_type()==treeObjectClass):
        #item.draw_outline(colour='red',thickness=5)
        menuResults = item
        break;

rect  = menuResults.rectangle()
temp = win32structures.RECT()
temp.left = rect.left
temp.top = rect.top + 58
temp.right = rect.right
temp.bottom = rect.top + 60 + 12
menuResults.draw_outline(colour='red',thickness=1,rect=temp)
mouse.click(coords=(temp.left + 4,temp.top + 4))
#menuResults.click_input(button='left',coords=(temp.left + 4,temp.top + 4),double=False)

#time.sleep(5)

app.window(title_re="Baseplan Enterprise.*").wait("ready",timeout=60)

inv = app.window(title_re="Baseplan Enterprise.*")
"""
for c in inv.children():
    #print("-------------------")
    print("control type:" + c.control_type()+ " name:" + c.element_info.name)
"""

attempts = 0
maxattempts = 10
inv.child_window(auto_id="txtDate", control_type="BPControlSuite.BPTextBox").wait('visible',timeout=60)
inv.child_window(auto_id="txtDate", control_type="BPControlSuite.BPTextBox").set_text("13/09/2018")


  
#buttons = inv.children(control_type='BPControlSuite.BPButton')
#panes = inv.children(control_type='BPControlSuite3.BPLayoutPanel')
topBar = inv.child_window(auto_id="TopBarPanel", control_type="System.Windows.Forms.Panel")
#topBar.draw_outline(colour='red',thickness=5)

#topBar.print_control_identifiers()

#bars = topBar.children(control_type='System.Windows.Forms.Panel')
bars = topBar.children(control_type='System.Windows.Forms.TableLayoutPanel')

count = 2
curr=1
for bar in bars:
    #bar.draw_outline(colour='red',thickness=3)
    print("------bar info----")
    #print(str(bar.element_info.control_id))
    items = bar.children(control_type='System.Windows.Forms.TableLayoutPanel')
    if curr==1:
        for item in items:
            #item.draw_outline(colour='red',thickness=5)
            print(item.element_info.control_type)
            panels = item.children(control_type='System.Windows.Forms.Panel')
            for p in panels:
                #p.draw_outline(colour='red',thickness=4)
                print(p.element_info.control_type)
                #print(str(len(b.children())))
                buttons = p.children()
                for b in buttons:
                    b.draw_outline(colour='red',thickness=5)
                    print(b.element_info.control_type)
                    print(str(len(b.children())))
        break        
    curr=curr+1        
    #bar.print_control_identifiers()
    #time.sleep(5)

#topBar.child_window(auto_id="UserProfileIcon", control_type="BPControlSuite3.IconWithBadge").click()
"""
panes = inv.children(control_type='System.Windows.Forms.Panel')

for p in panes:
    print("[control_id:" + str(p.element_info.control_id)+",name:"+p.element_info.name + "]")
    p.draw_outline(colour='red',thickness=4)
    time.sleep(5)
    print('---getting buttons----')
    buttons = p.children(control_type='BPControlSuite.BPButton')
    for b in buttons:
        print(b.element_info.name)
        b.draw_outline(colour='white',thickness=4)
"""        