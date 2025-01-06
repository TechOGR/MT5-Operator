from PyQt5.QtWidgets import QApplication
import sys

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

class HelpMessageText(QFrame):
    def __init__(self):
        super().__init__()
        self.setVisible(True)
        self.setMinimumSize(300, 450)
        self.setMaximumSize(350, 650)
        self.setStyleSheet(self.styleText()["frameStyle"])
        
        self.frameShortCuts = QFrame(self)
        self.frameShortCuts.setMinimumHeight(250)
        self.frameShortCuts.setMaximumHeight(200)
        
        self.shortcutLayout = QVBoxLayout()
        
        self.new_layout = QVBoxLayout()
        
        self.initComponents()
        
    def initComponents(self):
        
        labels = []
        labels_text = [
            "With this software you'll be able to get profits in trading just with one click, you will be able to see the prediction graphics and more... If you have any questions or you wanna help with any donation, visit this site: https://onelcrack.vercel.app/questions | ty",
            "Press CTRL+SHIFT+H to show and hide password",
            "Press CTRL+SHIFT+C to clear all fields",
            "Press ESCAPE to close any window",
            "Como Estás bro",
        ]
        
        for i_text in labels_text:
            label = QLabel()
            label.setStyleSheet(self.styleText()["txtFont"])
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setWordWrap(True)
            label.setText(i_text)
            labels.append(label)
            
        
        for i in range(1,len(labels_text)):
            self.shortcutLayout.addWidget(labels[i])
        
        self.frameShortCuts.setLayout(self.shortcutLayout)
        
        self.new_layout.addWidget(labels[0])
        self.new_layout.addWidget(self.frameShortCuts)
        
            
        self.setLayout(self.new_layout)
        
    def styleText(self) -> dict:
        txtFont = """
            font-size: 15px;
            color: #d2053d;
            
        """
        
        frameStyle = """
            padding: 5px;
        """
        
        return {
            'txtFont': txtFont,
            'frameStyle': frameStyle
        }

class HelpDialog(QDialog):
    
    def __init__(self, msg):
        super().__init__()
        self.sms = msg
        self.imagen_path = "img/logo_app.jpeg"
        self.path_img = path.join(getcwd(), "img")
        self.ClasStyles = self.styles()
        self.frameText = HelpMessageText()
        
        self.setWindowTitle("Help Panel")
        self.setFixedSize(350,600)
        self.setStyleSheet(self.ClasStyles["main"])
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(self.imagen_path))
        self.setVisible(True)
        
        self.setRounded(15)
        
        layout = QVBoxLayout()
        
        labelInfo = QLabel("Welcome To Help Panel", self)
        labelInfo.setStyleSheet(self.ClasStyles["labelInfo"])
        labelInfo.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        labelMessage = QLabel(self.sms, self)
        labelMessage.setStyleSheet(self.ClasStyles["labelSMS"])
        
        layout.addWidget(labelInfo, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(self.frameText, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.frameSocial = QFrame(self)
        
        layout.addWidget(self.frameSocial, alignment=Qt.AlignmentFlag.AlignBottom) 
        
        self.setLayout(layout)
        
        self.footerSocial()
    
    def openURL(self, urlComing):
        print(urlComing)
        url = QUrl(urlComing)
        QDesktopServices.openUrl(url)
    def footerSocial(self):
        layoutHorizontal = QHBoxLayout()

        listIcons = [
            QIcon(
                path.join(self.path_img, "social", f"{i}-white.png")
            ) for i in range(5)
        ]
        
        listSocials = [
            "https://www.facebook.com/profile.php?id=61570586445561",
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
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    dialog = HelpDialog("Welcome to Help Panel")
    dialog.show()
    sys.exit(app.exec_())