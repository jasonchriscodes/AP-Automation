import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit,  QTextEdit, QGridLayout, QApplication,QPushButton,QMainWindow,QDesktopWidget)
from lib.prop import Prop

class SettingWindow(QMainWindow):
    
    def __init__(self,settingsPath,parent=None):
        super().__init__(parent)
        self.widget = QWidget(self)
        self.settingsPath = settingsPath
        self.p = Prop(self.settingsPath)        
        self.initUI()
                
    def initUI(self):
        
        generalSettings = QLabel('General Settings:')
        appURL = QLabel('App URL')
        appUser = QLabel('App User')
        appPass = QLabel('App Password')
        stopLbl = QLabel('Stop')
        notifyTo = QLabel('Notify To')



        dbSettings = QLabel('Database Settings:')
        dbHost = QLabel('Host')
        dbName = QLabel('Name')
        dbUser = QLabel('User')
        dbPass = QLabel('Password')


        locations = QLabel('Locations:')
        locLogs = QLabel('Logs Folder')
        locResults = QLabel('Results Folder')


        urlEdit = QLineEdit()
        appUserEdit = QLineEdit()
        appPassEdit = QLineEdit()
        stopEdit = QLineEdit()
        notifyToEdit = QLineEdit()

        dbHostEdit = QLineEdit()
        dbNameEdit = QLineEdit()
        dbUserEdit = QLineEdit()
        dbPassEdit = QLineEdit()

        locLogsEdit = QLineEdit()
        locResultsEdit = QLineEdit()

        saveBtn = QPushButton("Save")
        saveBtn.clicked.connect(self.save)

        grid = QGridLayout()
        grid.setSpacing(10)

    
        #DB settings related objects
        grid.addWidget(dbSettings, 1, 2)

        
        grid.addWidget(dbHost, 2, 2)
        grid.addWidget(dbHostEdit, 2, 3)
        dbHostEdit.setText(self.p.get("db","host"))

        grid.addWidget(dbName, 3, 2)
        grid.addWidget(dbNameEdit, 3, 3)
        dbNameEdit.setText(self.p.get("db","db"))

        grid.addWidget(dbUser, 4, 2)
        grid.addWidget(dbUserEdit, 4, 3)
        dbUserEdit.setText(self.p.get("db","user"))

        grid.addWidget(dbPass, 5, 2)
        grid.addWidget(dbPassEdit, 5, 3)        
        dbPassEdit.setText(self.p.get("db","pass"))

        #Location settings realted objects
        grid.addWidget(locations, 1, 4)

        grid.addWidget(locLogs, 2, 4)
        grid.addWidget(locLogsEdit, 2, 5)
        locLogsEdit.setText(self.p.get("locations","logs"))

        grid.addWidget(locResults, 3, 4)
        grid.addWidget(locResultsEdit, 3, 5)
        locResultsEdit.setText(self.p.get("locations","results"))

        # general settings related objects
        grid.addWidget(generalSettings, 1, 0)

        grid.addWidget(appURL, 2, 0)
        grid.addWidget(urlEdit, 2, 1)
        urlEdit.setText(self.p.get("general","app_url"))

        grid.addWidget(appUser, 3, 0)
        grid.addWidget(appUserEdit, 3, 1)
        appUserEdit.setText(self.p.get("general","app_user"))

        grid.addWidget(appPass, 4, 0)
        grid.addWidget(appPassEdit, 4, 1)
        appPassEdit.setText(self.p.get("general","app_pass"))

        grid.addWidget(stopLbl, 5, 0)
        grid.addWidget(stopEdit, 5, 1)        
        stopEdit.setText(self.p.get("general","stop"))
        
        grid.addWidget(notifyTo, 6, 0)
        grid.addWidget(notifyToEdit, 6, 1)        
        notifyToEdit.setText(self.p.get("general","notify_to"))
        
        grid.addWidget(saveBtn,7,5)
        
        self.widget.setLayout(grid) 
        self.setCentralWidget(self.widget)
        self.setGeometry(300, 300, 800, 100)
        self.setWindowTitle('Settings')    
             
        
        print("All objects are added")
        self.center()
        self.show()      

    def center(self):
        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())        


    def save(self):
        self.close()

"""        
if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ui = SettingWindow("")    
    sys.exit(app.exec_())          
"""    