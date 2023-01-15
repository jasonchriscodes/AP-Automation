
from pywinauto.application import Application 
from pywinauto import backend
from pywinauto import mouse
from pywinauto import win32structures
import time
import os,sys

from lib.Gen import Gen
from lib.mail import Mailing
from bpe.login import Login
from bpe.bpe import BPE
from bpe.inv import Invoicing
from bpe.ss import SupplierSelection

g = Gen(backend)

g.start_app(r"C:\Program Files (x86)\Baseplan\Enterprise\BPEnterprise.exe")

lg = Login()
lg.log_user("ap.automation","Office47")

be = BPE()
be.nav("Invoicing")

invoicing = Invoicing()
invoicing.click_tool_bar("Add New")

invoicing.select_po_number("124064")
invoicing.set_inv_det_date("11/01/2019")
invoicing.select_action("Select")

invoicing = Invoicing()
ss = SupplierSelection(invoicing)
#ss.click_select_all_btn()
#ss.click_ok_btn()
