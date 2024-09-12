def mainStyles():
    styles_main = """
        * {
            background-color: black;
            color: white;
        }
        QLineEdit {
            background-color: #000000;
            color: #dddddd;
            border: 2px solid #d2053d;
            border-radius: 10px;
            padding: 10px;
            font-size: 16px;
            font-family: 'Courier New', monospace;
            selection-background-color: #ff00ff;
            selection-color: #000000;
        }
            
        QLineEdit:hover {
            border: 2px solid #ff0000;
            color: #ff00ff;
        }

        QLineEdit:focus {
            border: 2px solid #d2053d;
            color: #ffffff;
            background-color: #111111;
        }
        QPushButton {
            background-color: #111111;
        }
        """
    return styles_main