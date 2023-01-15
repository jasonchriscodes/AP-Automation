from pywinauto.application import Application 
from pywinauto import backend
from pywinauto import mouse
from pywinauto import win32structures
from lib.Gen import Obj

import time
import os,sys

class Popup(Obj):
    def __init__(self,par=None,l=None):
        super(Popup,self).__init__("frmBPMessage",par,l)
        if (par):
            self.win = par.win.child_window(title='frmBPMessage',  control_type="Window")
            #self.win.print_control_identifiers()
            self.win.set_focus()
    
    def get_popup_message(self):
        #child_window(title="There is no Reference are you sure you wish to continue posting?", auto_id="lblMsg", control_type="Text")
        msg = ""
        try:
            msg = self.win.child_window(auto_id="MainContentLayoutPanel", control_type="Pane").Static0.window_text()
            self.l.add("Message in popup :  " + msg)
        except Exception as e:
            self.l.add("Problem occured when getting message from popup")
        return msg


    def get_title(self):
        msg = ""
        try:
            msg =  self.win.child_window(auto_id="TitlebarPanel", control_type="Pane").Static2.window_text()
            self.l.add("Title of popup:" + msg)
        except Exception as e:
            self.l.add("Problem occured when getting title from popup")

        return msg

    def yes_btn(self):
        return self.win. child_window(title="Yes", auto_id="cmdYes", control_type="Button")

    def ok_btn(self):
        return self.win. child_window(title="OK", auto_id="cmdOK",  control_type="Button")

    def no_btn(self):
        return self.win.child_window(title="No", auto_id="cmdNo", control_type="Button")

    def click_ok(self):
        try:
            self.ok_btn().click()
            self.l.add("Clicked OK button on popup")
        except Exception as e:
            self.l.add("Could not click OK button on popup")
            raise e

    def click_yes(self):
        try:
            self.yes_btn().click()
            self.l.add("Clicked yes button on popup")
        except Exception as e:
            self.l.add("Could not click Yes button on popup")
            raise e

    def click_no(self):
        try:
            self.no_btn().click()
            self.l.add("Clicked No button on popup")
        except Exception as e:
            self.l.add("Could not click No button on popup")
            raise e
