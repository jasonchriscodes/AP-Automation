
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
from bpe.ss import SupplierSelection

g = Gen(backend)

g.start_app(r"C:\Program Files (x86)\Baseplan\BPEnterprise.exe")

lg = Login()
#g.print_ele_details(lg.company_drop())
lg.company_drop()