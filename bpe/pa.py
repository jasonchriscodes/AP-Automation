from pywinauto.application import Application 
from pywinauto import backend
from pywinauto import mouse
from pywinauto import win32structures
from lib.Gen import Obj

import time
import os,sys

class PostAll(Obj):
    def __init__(self,par=None):
        super(PostAll,self).__init__("CRD Invoices Post All",par)
        if (par):
            self.win = par.win.child_window(title="CRD Invoices Post All",  control_type="Window")
            #self.win.print_control_identifiers()
            self.win.set_focus()
    
    def post_btn(self):
        return self.win.child_window(title="Post",  control_type="Button")


    def click_post_btn(self):
        #print(self.select_all_btn().element_info.name)
        self.post_btn().click()

    