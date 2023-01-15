from pywinauto.application import Application 
from pywinauto import backend
from pywinauto import mouse
from pywinauto import win32structures
from pywinauto import findwindows
from lib.Gen import Obj

import time
import os,sys

class BPE(Obj):
    def __init__(self,par=None):
        super(BPE,self).__init__("Baseplan Enterprise",par)

    def search_nav(self):
        return self.win.child_window(auto_id="SearchMainMenuTextBox", control_type="Edit")

    def clear_nav(self):
        try:
            navEle = self.search_nav()           
            self.type_element(navEle,'^a{BACKSPACE}')
            time.sleep(self.minwait)
            self.l.add("Cleared content in navigation field")
        except Exception as e:
            self.l.add("Problem occurred to clear the navigation text field")
            raise e
            
    def nav(self,path):
        #self.win.Pane15.Pane16.Pane17.ListBox2.print_control_identifiers()
        #self.win.Pane15.Pane16.Pane17.ListBox2.child_window(title=path,control_type='ListItem').print_control_identifiers()
        #self.win.Pane15.Pane16.Pane17.ListBox2.child_window(title=path,control_type='ListItem').draw_outline(colour='red',thickness=1)
        #rect = self.win.Pane15.Pane16.Pane17.ListBox2.child_window(title=path,control_type='ListItem').rectangle()
        try:        
            #self.clear_nav()
            self.clear_field(self.search_nav())
            self.search_nav().type_keys(path,with_spaces=True)            
            time.sleep(self.minwait*2)

            curr = 0 
            rect = self.win.child_window(title=path,control_type='ListItem').rectangle()
            mouse.click(coords=(rect.left+10,rect.top+5))
            
        except Exception as e:
            # someimes the list item with Invoicing is more than 1 , in that caess we need to handle this way, not the best of ways though
            #print ( str(e))
            #self.win.print_control_identifiers()
            rect = self.win.Invoicing2.rectangle()
            mouse.click(coords=(rect.left+10,rect.top+5))
        time.sleep(self.minwait*2)
        self.l.add("Navigated to path " + path)