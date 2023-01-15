import sys
from PyQt5.QtWidgets import QApplication
from ui.UI import AutoUI

if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ui = AutoUI()    
    sys.exit(app.exec_())  