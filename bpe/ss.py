from pywinauto.application import Application 
from pywinauto import backend
from pywinauto import mouse
from pywinauto import win32structures
from lib.Gen import Obj

import time
import os,sys

class SupplierSelection(Obj):
    def __init__(self,par=None,l=None):
        super(SupplierSelection,self).__init__("Supplier Selection",par,l)
        if (par):
            self.win = par.win.child_window(title="Supplier Selection", auto_id="frmCRD_RCPTList", control_type="Window")
            #self.win.print_control_identifiers()
            self.win.set_focus()
    
    def filter_all_radio(self):
        return self.win.child_window(title="All", auto_id="optFilterByAll", control_type="RadioButton")
        
    def records(self):
        return self.win.child_window(title='BPGridControl1',control_type='Table')

    def record_count(self):
        cnt = len( self.records().children(control_type='Custom'))
        if(cnt>1):
            cnt = cnt-1
        else:
            cnt = 0
        return cnt

    def select_filter_all(self):
        try:
            self.filter_all_radio().click()
            self.l.add("Selected filter all option.")
        except Exception as e:
            self.l.add("Problem occurred to click on filter all option.")
            raise e

    def select_all_btn(self):
        return self.win.child_window(title="Select All", auto_id="cmdSelectAll", control_type="Button")

    def de_select_all_btn(self):
        return self.win.child_window(title="Deselect All", auto_id="cmdDeSelect", control_type="Button")
    
    def yes_btn(self):
        return self.win.child_window(title="YES", auto_id="cmdYES", control_type="Button")

    def ok_btn(self):
        return self.win.child_window(title="OK", auto_id="cmdOK", control_type="Button")

    def cancel_btn(self):
        return self.win.child_window(title="Cancel", auto_id="cmdCancel", control_type="Button")

    def click_select_all_btn(self):
        try:
            #print(self.select_all_btn().element_info.name)
            self.select_all_btn().click()
            self.l.add("Clicked select all option.")
        except Exception as e:
            self.l.add("Problem occured to click on select all option")
            raise e

    def click_ok_btn(self):
        try:
            self.ok_btn().click()
            self.l.add("Clicked OK button")
        except Exception as e:
            self.l.add("problem occured to click OK button")
            raise e

    def click_yes_btn(self):
        try:
            self.yes_btn().click()
            self.l.add("Clicked yes button")
        except Exception as e:
            self.l.add("Problem occurred to click Yes button")
            raise e

