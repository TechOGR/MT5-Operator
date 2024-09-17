from PyQt5.QtWidgets import (
    QMainWindow,
    QLabel,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QWidget, 
    QGraphicsBlurEffect,
    QGraphicsDropShadowEffect,
    QLineEdit,
    QPushButton,
    QShortcut
)
from PyQt5.QtCore import (
    Qt,
    QRectF,
    QPoint,
    QSize,
    QUrl
)
from PyQt5.QtGui import (
    QPixmap,
    QFont,
    QFontDatabase,
    QPainterPath,
    QColor,
    QRegion,
    QIcon,
    QDesktopServices
)
from functools import partial
from modules.styles import mainStyles
from modules.connect_mt5 import (
    initConnect
)
from modules.ctrl_data import (
    saveData,
    loadData
)
from modules.components.customEditServer import CustomEditServer
from os import path


class Window(QMainWindow):
    
    def __init__(self, path) -> None:
        super().__init__()
        
        self.fullPath = path
        
        self.initComponents()
        
        self.old_pos = None

    def initComponents(self):
        self.path_img = path.join(self.fullPath, "img")
        self.path_fonts = path.join(self.fullPath, "fonts")
        
        self.image_wallpaper = QPixmap(path.join(self.path_img,"wallpaper.png"))
        self.logo_app = QPixmap(path.join(self.path_img, "logo_app.jpeg"))
        
        with open("log.txt", "w") as f:
            f.write(self.fullPath)
            f.close()
        width, height = 500, 700
        
        self.setGeometry(100, 100, width, height)
        self.setWindowTitle("MT5 Operator")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setStyleSheet(mainStyles())
        self.setWindowIcon(QIcon(self.logo_app))

        self.round_corners(15)
        
        self.components()

    # Starting Components
    def components(self):
        self.styleComponents()
        self.effectsComponents()
        
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        
        self.layout_central_widget = QVBoxLayout(self.centralWidget)
        
        # Frames ---------------------
        self.frameTop = QFrame(self)
        self.frameTop.setObjectName("FrameTop")
        self.frameTop.setMaximumHeight(int((self.height() / 2) / 3))
        self.frameTop.setStyleSheet("background-color: #00000000;")
        
        self.frameButtom = QFrame(self)
        self.frameButtom.setStyleSheet("background-color: #00000000;")
        
        self.frameSocial = QFrame(self)
        self.frameSocial.setStyleSheet("background-color: #00000000;")
        self.frameSocial.setMaximumHeight(100)
        
        self.layout_central_widget.addWidget(self.frameTop)
        self.layout_central_widget.addWidget(self.frameButtom)
        self.layout_central_widget.addWidget(self.frameSocial)
        # ----------------------------
        
        # Main Font Title -------------------
        self.TitleFontPath = path.join(self.path_fonts,"Glitcher.ttf")
        
        fontData = QFontDatabase()
        font_id = fontData.addApplicationFont(self.TitleFontPath)
        
        self.TitleFont = QFont()
        
        if font_id != -1:
            family_font = fontData.applicationFontFamilies(font_id)[0]
            self.TitleFont = QFont(family_font, 50)
        else:
            print("ERROR AL CARGAR LA FUENTE")
        # ------------------------------------
        
        # Layout and Elements -----------------------------
        self.layout_frame_top = QVBoxLayout(self.frameTop)
        self.layout_frame_top.addStretch()
        
        self.labelTitle = QLabel("MT OPERATOR", self.frameTop)
        self.labelTitle.setFont(self.TitleFont)
        self.labelTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelTitle.setStyleSheet("color: #d2053d;")
        
        self.layout_frame_top.addWidget(self.labelTitle)
        self.layout_frame_top.addStretch()
        self.layout_frame_top.setAlignment(self.labelTitle, Qt.AlignmentFlag.AlignVCenter)
        
        self.layout_frame_buttom = QVBoxLayout(self.frameButtom)
        
        self.frame_buttom_items = QFrame(self.frameButtom)
        self.frame_buttom_items.setStyleSheet("background-color: #00000000;")
        
        self.labelSubTitle = QLabel("TRADE SAFE", self.frame_buttom_items)
        self.labelSubTitle.setFont(self.TitleFont)
        self.labelSubTitle.setGeometry(-20, 0, self.width(), 80)
        self.labelSubTitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labelSubTitle.setStyleSheet("color: #d2052d; font-size: 40px;")
        
        self.userEdit = QLineEdit(self.frame_buttom_items)
        self.userEdit.setMaximumSize(int(self.width() / 3), 50)
        self.userEdit.setGeometry(50, 150, 180, 50)
        self.userEdit.setPlaceholderText("User")
        self.userEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.userEdit.setStyleSheet("background-color: black;")
        
        self.passwordEdit = QLineEdit(self.frame_buttom_items)
        self.passwordEdit.setMaximumSize(int(self.width() / 3), 50)
        self.passwordEdit.setGeometry(250, 150, 180, 50)
        self.passwordEdit.setPlaceholderText("Password")
        self.passwordEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.passwordEdit.setStyleSheet("background-color: black;")
        self.passwordEdit.setEchoMode(QLineEdit.Password)

        self.serverEdit = CustomEditServer(self.frame_buttom_items, self)
        self.serverEdit.setMaximumSize(int(self.width() / 2), 50)
        self.serverEdit.setGeometry(150, 250, 180, 50)
        self.serverEdit.setPlaceholderText("Server-MT5")
        self.serverEdit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.serverEdit.setStyleSheet("background-color: black;")
        
        self.buttonSave = QPushButton("Save",self.frame_buttom_items)
        self.buttonSave.setGeometry(55,330, 70, 50)
        self.buttonSave.setStyleSheet(self.styleButtons)
        self.buttonSave.clicked.connect(self.toSave)
        
        self.buttonConnect = QPushButton("Connect",self.frame_buttom_items)
        self.buttonConnect.setGeometry(205,370, 70, 50)
        self.buttonConnect.setStyleSheet(self.styleButtons)
        self.buttonConnect.clicked.connect(self.connectMT5)
        
        self.buttonLoad = QPushButton("Load",self.frame_buttom_items)
        self.buttonLoad.setGeometry(355,330, 70, 50)
        self.buttonLoad.setStyleSheet(self.styleButtons)
        self.buttonLoad.clicked.connect(self.toLoad)
        
        self.layout_frame_buttom.addWidget(self.frame_buttom_items)
        
        # Shorcut Keys ------------
        shorcutClear = QShortcut(Qt.CTRL + Qt.SHIFT + Qt.Key_C, self)
        shorcutClear.activated.connect(self.clearEdits)
        
        shortcutShowPassword = QShortcut (Qt.CTRL + Qt.SHIFT + Qt.Key_H, self)
        shortcutShowPassword.activated.connect(self.showHidePassword)
        # -------------------------
        self.checkPasswordHide = False
        self.footerSocial()
        # ----------------------------------------------------
        
        label_background = QLabel(self.centralWidget)
        pixmap = QPixmap(self.image_wallpaper)

        label_background.setPixmap(pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        label_background.setGeometry(self.rect())
        label_background.setGraphicsEffect(self.blur_effect)
        label_background.lower()

        self.apply_shadow()
    
    # Save and Load Data --------------------------
    def toSave(self):
        userData = (self.userEdit.text(), self.passwordEdit.text(), self.serverEdit.text())
        
        saveData(self.fullPath,userData)
        
    def toLoad(self):
        try:
            data = loadData()
            
            user = data["User"]
            passwd = data["Pass"]
            server = data["Server"]
            
            self.userEdit.setText(str(user)),
            self.passwordEdit.setText(passwd)
            self.serverEdit.setText(server)
            
        except (FileNotFoundError, FileExistsError):
            
            self.userEdit.setText("ERROR")
            self.passwordEdit.setText("ERROR")
            self.serverEdit.setText("ERROR")
        
        
        print(data)

    # ----------------------------------------------

    # Connecting to MT5
    def connectMT5(self):
        
        user = self.userEdit.text()
        password = self.passwordEdit.text()
        server = self.serverEdit.text()
        dataUser = (user, password, server)
        
        access = self.testingUserData(dataUser)
        
        if access:
            initConnect(dataUser)
        else:
            print("Something has gone wrong")

    # Check data is correct
    def testingUserData(self,data):
        MIN_CHAR = 8
        MAX_CHAR = 15
        
        user, password, server = data
        
        if len(user) < MIN_CHAR or len(user) > MAX_CHAR:
            # Aquí mostraré una alerta, creando una clase Dialog
            print("User exceeds the limit")
            return False
        elif len(password) < MIN_CHAR or len(password) > MAX_CHAR:
            print("Password exceeds the limit")
            return False
        elif len(server) == 0:
            print("Please select one Server from the Server List")
            return False
        else:
            return True

        # Continuar las verificaciones
    
    # Opening Urls
    def openURL(self, urlComing):
        url = QUrl(urlComing)
        QDesktopServices.openUrl(url)
    
    # Social Links
    def footerSocial(self):
        layoutHorizontal = QHBoxLayout()

        listIcons = []
        for i in range(5):
            listIcons.append(QIcon(path.join(self.path_img,"social",f"{i}.png")))

        listSocials = [
            "https://www.facebook.com/profile.php?id=100092376152191",
            "https://github.com/TechOGR/",
            "https://www.instagram.com/onel_crack/",
            "https://www.youtube.com/channel/UCDaHKnOv_YOr4R8OzCU6Aiw",
            "https://x.com/Onel_Crack"
        ]
        
        iconSize = QSize(60,60)
        listButtons = []
        for i in range(5):
            listButtons.append(QPushButton(self.frameSocial))
            listButtons[i].setFixedSize(70,70)
            listButtons[i].setMinimumSize(70,70)
            listButtons[i].setStyleSheet("margin: 10px;background-color: #00000000; color: black;")
            listButtons[i].setIcon(listIcons[i])
            listButtons[i].setIconSize(iconSize)
            listButtons[i].clicked.connect(partial(self.openURL, listSocials[i]))
            
        for i in listButtons:
            layoutHorizontal.addWidget(i)
            
        self.frameSocial.setLayout(layoutHorizontal)
        
        layoutHorizontal.setAlignment(Qt.AlignmentFlag.AlignCenter)
    
    # Effects for every components
    def effectsComponents(self):
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(1)

    def styleComponents(self):
        self.styleButtons = """
            background-color: black;
            color: #d2053d;
            border: 2px solid #d2053d;
            border-radius: 10px;
            font-family: monospace;
            font-size: 15px;
        """

    # Setting Rounded Borders
    def round_corners(self, radius):
        rect = QRectF(self.rect())

        path = QPainterPath()
        path.addRoundedRect(rect, radius, radius)

        region = QRegion(path.toFillPolygon().toPolygon())

        self.setMask(region)

    # Shadow Effect for Main Window
    def apply_shadow(self):
        shadow_effect = QGraphicsDropShadowEffect(self)
        shadow_effect.setBlurRadius(20)
        shadow_effect.setXOffset(0)
        shadow_effect.setYOffset(0)
        shadow_effect.setColor(QColor(0, 0, 0, 150))
        
        self.centralWidget.setGraphicsEffect(shadow_effect)

    # Shortcuts --------------------------------------
    # Clear QLineEdits
    def clearEdits(self):
        self.userEdit.setText("")
        self.passwordEdit.clear()
        self.serverEdit.clear()
    
    # ShowHidePassword
    def showHidePassword(self):
        if self.checkPasswordHide:
            self.passwordEdit.setEchoMode(QLineEdit.Password)
            self.checkPasswordHide = False
        else:
            self.passwordEdit.setEchoMode(QLineEdit.Normal)
            self.checkPasswordHide = True
        
    # -----------------------------------------------

    # Events for Frame --------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = QPoint(event.globalPos() - self.old_pos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.old_pos = None
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    # --------------------------------