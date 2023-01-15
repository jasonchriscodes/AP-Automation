import sys
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication, QDesktopWidget
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QIcon
import datetime

from lib.db import DB
from lib.prop import Prop
import configparser
from ui.settings import SettingWindow

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

class Communicate(QObject):    
    closeApp = pyqtSignal()      

class AutoUI(QMainWindow):
    def __init__(self):
        super().__init__()        
        self.initUI()        
        self.settingsPath = "settings.cfg"
        self.p = Prop(self.settingsPath)                          

    def initUI(self):

        self.c = Communicate()
        self.c.closeApp.connect(self.close)

        playAct = QAction(QIcon('ui/play.png'), 'Play', self)
        playAct.setShortcut('Ctrl+N')
        playAct.triggered.connect(self.play)

        stopAct = QAction(QIcon('ui/stop.png'), 'Stop', self)
        stopAct.setShortcut('Ctrl+C')
        stopAct.triggered.connect(self.stop)

        settingsAct = QAction(QIcon('ui/settings.png'), 'Settings', self)
        settingsAct.setShortcut('Ctrl+T')
        settingsAct.triggered.connect(self.showSettings)

        logAct = QAction(QIcon('ui/log.png'), 'Log', self)
        logAct.setShortcut('Ctrl+D')
        logAct.triggered.connect(qApp.quit)        


        statusAct = QAction(QIcon('ui/table.png'), 'Status', self)
        statusAct.setShortcut('Ctrl+L')
        statusAct.triggered.connect(qApp.quit) 

        exitAct = QAction(QIcon('ui/exit.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(qApp.quit)
        
        playAct.setToolTip("Start Processing")
        stopAct.setToolTip("Stop Procesing after current PO is processed")
        settingsAct.setToolTip("Change settings")
        logAct.setToolTip("View logs")
        statusAct.setToolTip("View PO Statuses")
        exitAct.setToolTip("Stop abruptly and exit application")

        self.toolbar = self.addToolBar('Tool Bar')
        
        self.toolbar.addAction(playAct)
        self.toolbar.addAction(stopAct)        
        self.toolbar.addAction(statusAct)     
        self.toolbar.addAction(logAct)        
        self.toolbar.addAction(settingsAct)

        self.toolbar.addAction(exitAct)
        
        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle('Automation Manager')    

        self.center()
        self.show()      

    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def stop(self):
              
        stopValue = self.p.get("general","stop")
        print("Stop value is:" + stopValue) 
        self.p.setOption("general","stop","no")
        stopValue = self.p.get("general","stop")
        print("Stop value is:" + stopValue)
        self.p.setOption("general","new","checking")
        stopValue = self.p.get("general","new")
        print("new Option value is:" + stopValue)
    def showSettings(self):
        stWin = SettingWindow(self.settingsPath,self)


    def play(self):

        dt = datetime.datetime.now()
        today = str(dt.day)+"/"+str(dt.month)+"/"+str(dt.year)
        print("Triggered play button:" + today)
        #Start the log with date details and store in a file. 
        db = DB("SQLSERVER")
        dbhost = self.p.get("db","host")
        dbname = self.p.get("db","db")
        dbuser = self.p.get("db","user")
        dbpass = self.p.get("db","pass")

        print("host["+dbhost+"]")
        print("name["+dbname+"]")
        print("user["+dbuser+"]")
        print("pass["+dbpass+"]")
        #dbhost="cfaksql\\ferret"
        #if(db.connect('cfaksql\\ferret','FerretAP','Apautomation','Office47')):
        if(db.connect(dbhost,dbname,dbuser,dbpass)):
            db.execute("select * from PO_Ferret where Status='PartlyRecd' and PERIOD<='201901'")
            db.setColumns({"Supplier":0,"PO_Number":1,"Status":2,"Ordered_By":3,"BranchCode":4,"Site":5,"Delivery_Addresss":6,"Warehouse":7,"Authorized_By":8,"UserConfirmed":9,"DateCreated":10,"POType":11,"PERIOD":12})
            #print("Number of records are:"+str(db.rowCount))
            rowCnt = db.rowCount
            ind = 0
            for ind in range (1,rowCnt):
                db.getRow(ind)
                po_num = str(db.getValue("PO_Number"))
                print ("PO Number["+str(ind)+"]:" + po_num )


                g = Gen(backend)

                g.start_app(self.p.get("general","app_url"))

                lg = Login()
                lg.log_user(self.p.get("general","app_user"),self.p.get("general","app_pass"))

                be = BPE()
                be.nav("Invoicing")

                invoicing = Invoicing()
                invoicing.click_tool_bar("Add New")

                invoicing.select_po_number(po_num)
                invoicing.set_inv_det_date(today)
                invoicing.select_action("Select")

                invoicing = Invoicing()
                ss = SupplierSelection(invoicing)
                #ss.click_select_all_btn()
                #ss.click_ok_btn()




                if(ind==1):
                    break
            db.close()
        """
        Iterate through all the records, process them eacha and report the stauts. 
        Start of each iteration, we need to check if there is any configuration that says to stop the execution other wise it can continue to process.                 
        """
        #self.c.closeApp.emit()