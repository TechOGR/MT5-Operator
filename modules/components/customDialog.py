from PyQt5.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame
)
from PyQt5.QtGui import (
    QIcon,
    QPainterPath,
    QRegion,
    QDesktopServices
)
from PyQt5.QtCore import (
    Qt,
    QRectF,
    QSize,
    QUrl
)
from functools import partial
from os import path, getcwd

class Dialog(QDialog):
    
    def __init__(self):
        super().__init__()
        self.imagen_path = "img/logo_app.jpeg"
        self.path_img = path.join(getcwd(), "img")
        self.ClasStyles = self.styles()
        
        self.setWindowTitle("Hola Random")
        self.setFixedSize(300,160)
        self.setStyleSheet(self.ClasStyles["main"])
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(self.imagen_path))
        self.setVisible(True)
        
        self.setRounded(15)
        
        layout = QVBoxLayout()
        
        labelInfo = QLabel("Espera 🤚 Lee 👇", self)
        labelInfo.setStyleSheet(self.ClasStyles["labelInfo"])
        
        labelMessage = QLabel("Conectado", self)
        labelMessage.setStyleSheet(self.ClasStyles["labelSMS"])
        
        layout.addWidget(labelInfo, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(labelMessage, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.frameSocial = QFrame(self)
        
        layout.addWidget(self.frameSocial, alignment=Qt.AlignmentFlag.AlignHCenter) 
        
        self.setLayout(layout)
        
        self.footerSocial()
    
    def openURL(self, urlComing):
        print(urlComing)
        url = QUrl(urlComing)
        QDesktopServices.openUrl(url)
     
    def footerSocial(self):
        layoutHorizontal = QHBoxLayout()

        listIcons = []
        for i in range(5):
            listIcons.append(QIcon(path.join(self.path_img,"social",f"{i}-white.png")))

        listSocials = [
            "https://www.facebook.com/profile.php?id=100092376152191",
            "https://github.com/TechOGR/",
            "https://www.instagram.com/onel_crack/",
            "https://www.youtube.com/channel/UCDaHKnOv_YOr4R8OzCU6Aiw",
            "https://x.com/Onel_Crack"
        ]
        
        iconSize = QSize(40,40)
        listButtons = []
        for i in range(5):
            listButtons.append(QPushButton(self))
            listButtons[i].setFixedSize(40,40)
            listButtons[i].setMinimumSize(20,20)
            listButtons[i].setStyleSheet("margin: 10px;background-color: #00000000; color: black;")
            listButtons[i].setIcon(listIcons[i])
            listButtons[i].setIconSize(iconSize)
            listButtons[i].clicked.connect(partial(self.openURL, listSocials[i]))
            
        for i in listButtons:
            layoutHorizontal.addWidget(i)
            
        self.frameSocial.setLayout(layoutHorizontal)
        
        layoutHorizontal.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def styles(self) -> dict:
        mainStyle = """
            background-color: #000;
        """
        
        styleLabelSMS = """
            color: #d2053d;
            font-family: monospace;
            font-size: 30px;
        """
        
        styleLabelInfo = """
            color: #d2053d;
            font-family: monospace;
            font-size: 20px;
        """
        
        return {
            'main': mainStyle,
            'labelSMS': styleLabelSMS,
            'labelInfo': styleLabelInfo
        }
    
    def setRounded(self, ratio):
        rect = QRectF(self.rect())
        
        path = QPainterPath()
        path.addRoundedRect(rect, ratio, ratio)
        
        region = QRegion(path.toFillPolygon().toPolygon())
        
        self.setMask(region)