from PyQt5.QtWidgets import (
    QLineEdit,
    QListWidget,
    QListWidgetItem
)
from PyQt5.QtGui import (
    QFont,
    QColor
)

class CustomEditServer(QLineEdit):
    
    def __init__(self, frame=None, mainWindow=None) -> None:
        super().__init__(frame)
        
        self.initComponents()
        
        self.suggestions = QListWidget(mainWindow)
        self.suggestions.setGeometry(168,300,180,150)
        self.suggestions.setStyleSheet(self.styleSuggestions)
        self.suggestions.setVisible(False)
        self.suggestions.itemClicked.connect(self.selectOption)
        
        self.checkEnabled = False
    def initComponents(self):
        self.styleSuggestions = """
            background-color: #000000;
            border-radius: 10px;
            border: 2px solid #d2053d;
        """
        
        self.ItemFont = QFont("monospace", 11,2)

    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        if not self.checkEnabled:
            self.showSuggestions()
            self.checkEnabled = True
        
    def focusOutEvent(self, event):
        super().focusOutEvent(event)
        self.suggestions.setVisible(False)
        self.checkEnabled = False
        
    def showSuggestions(self):
        
        self.suggestions.clear()
        for i in self.getListServers():
            item = QListWidgetItem(i)
            item.setTextAlignment(4)
            item.setFont(self.ItemFont)
            item.setForeground(QColor("#d2053d"))
            
            self.suggestions.addItem(item)

        self.suggestions.setVisible(True)
        
    def selectOption(self, item):
        self.setText(item.text())
        self.suggestions.hide()
        
    def getListServers(self):
        return [
            "FTMO-Demo",
            "FTMO-Demo2",
            "FTMO-Server",
            "FTMO-Server2",
            "FTMO-Server3",
            "FTMO-Server4",
            "MetaQuotes-Demo"
        ]