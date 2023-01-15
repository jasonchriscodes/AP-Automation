
from pywinauto.application import Application 
from pywinauto import backend
from pywinauto import mouse
from pywinauto import win32structures
import time
import os,sys

from lib.Gen import Gen
from bpe.login import Login
from bpe.bpe import BPE
from bpe.inv import Invoicing

g = Gen(backend)
g.start_app(r"C:\Program Files (x86)\Baseplan\BPEnterprise.exe")

#app_handle = g.get_handle("Login")
#g.set_window(app_handle)
#g.pcis()

#lg = Login(g.get_window())
lg = Login()
lg.log_user("ap.automation","Tekapo02")

#app_handle = g.get_handle("Baseplan Enterprise")
#g.set_window(app_handle)

#be = BPE(g.get_window())
be = BPE()
be.nav("Invoicing")

#g.pcis()
#app_handle = g.get_handle("Baseplan Enterprise - Supplier Invoices/Credit Notes")
#g.set_window(app_handle)

#invoicing = Invoicing(g.get_window())
invoicing = Invoicing()
invoicing.click_tool_bar("Add New")

#app_handle = g.get_handle("Baseplan Enterprise - Supplier Invoices/Credit Notes")
#g.set_window(app_handle)

#invoicing = Invoicing(g.get_window())
invoicing.select_po_number("138108")
invoicing.set_inv_det_date("14/09/2018")
invoicing.select_action("Select")


#app_handle = g.get_handle("Supplier Selection")
#g.set_window(app_handle)