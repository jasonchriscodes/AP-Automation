
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
from bpe.pop import Popup

inv = Invoicing()

"""
popup = Popup(inv)
print( "title:" + popup.get_title())
print( "message:" + popup.get_popup_message())
popup.click_ok()
"""

"""
#handling popup dialogs
popup = Popup(inv)
print( "title:" + popup.get_title())
print( "message:" + popup.get_popup_message())
popup.click_no()
"""

"""
#Getting content from details and document total fields

#inv.win.child_window(title="Authorised by:", auto_id="tlpTotals", control_type="Pane").print_control_identifiers()

dtlsTotal = inv.win.child_window(title="Authorised by:", auto_id="tlpTotals", control_type="Pane").child_window(title="Authorised by:", auto_id="txtDetailsTotal", control_type="Edit")
docTotal =  inv.win.child_window(title="Authorised by:", auto_id="tlpTotals", control_type="Pane").child_window(title="Authorised by:", auto_id="txtDocTotal", control_type="Edit")
#dtlsTotal.select()
print("Details Total:" + dtlsTotal.get_value())
print("Document Total:" + docTotal.get_value())
"""
#inv.win.print_control_identifiers()
docno = inv.win.child_window( auto_id="tlpDocumentDetails", control_type="Pane").child_window( auto_id="txtTranID", control_type="Edit")
print(str(docno.get_value()))