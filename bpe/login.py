from pywinauto.application import Application 
from pywinauto import backend
from pywinauto import mouse
from pywinauto import win32structures
from lib.Gen import Obj

import time
import os,sys

class Login(Obj):
    def __init__(self,par=None):
        super(Login,self).__init__("Login",par)

    def company_drop(self):
        #self.win.print_control_identifiers()
        self.click_element( self.win.child_window(auto_id="cboCompany").child_window(control_type='SplitButton'))
        self.win.print_control_identifiers()
        #self.kids("SplitButton")
        #self.kids("List")

    def user_edit(self):
        return self.win.child_window(auto_id="txtUserID", control_type="Edit")

    def pass_edit(self):
        return self.win.child_window(auto_id="txtPassword", control_type="Edit")

    def login_btn(self):
        return self.win.child_window(title="Login", auto_id="cmdLogin", control_type="Button")

    def log_user(self,username,password):
        try:
            if  (username):
                self.user_edit().set_text(username)
                self.l.add("Entered \"" + username + "\" in username field")
            if (password):
                self.pass_edit().set_text(password)
                self.l.add("Entered \"" + password + "\" in password field")
                    
            self.click_element(self.login_btn())
        except Exception as e:
            self.l.add("Error occurred when trying to login, Exception details:" + str (e))
            raise e
        