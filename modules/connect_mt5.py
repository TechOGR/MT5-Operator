import MetaTrader5 as mt5
from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

imagen_path = "img/logo_app.jpeg"

def initConnect():
    
    response = mt5.initialize(login=86330370, password="Q+Jx2pSd", server="MetaQuotes-Demo")
    
    return response

class Dialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hola Random")
        self.setFixedSize(200,100)
        self.setStyleSheet("background: black;")
        self.setVisible(True)
        
        layout = QVBoxLayout()
        
        label = QLabel("Conectado", self)
        label.setStyleSheet("color: #0f0;")
        
        layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.setLayout(layout)
        
        
        self.setWindowIcon(QIcon(imagen_path))
