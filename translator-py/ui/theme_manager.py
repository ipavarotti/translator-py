class ThemeManager:
    def __init__(self):
        self.dark_mode = False
        
    def set_dark_mode(self, enabled):
        self.dark_mode = enabled
        
    def get_stylesheet(self):
        if self.dark_mode:
            return """
                QMainWindow, QDialog {
                    background-color: #2D2D30;
                    color: #FFFFFF;
                }
                QWidget {
                    background-color: #2D2D30;
                    color: #FFFFFF;
                }
                QPushButton {
                    background-color: #0078D7;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1C97EA;
                }
                QPushButton:disabled {
                    background-color: #555555;
                    color: #888888;
                }
                QLabel {
                    color: #FFFFFF;
                }
                QGroupBox {
                    border: 1px solid #555555;
                    border-radius: 5px;
                    margin-top: 10px;
                    font-weight: bold;
                    color: #FFFFFF;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
                QComboBox, QLineEdit {
                    background-color: #3C3C3C;
                    color: #FFFFFF;
                    border: 1px solid #555555;
                    padding: 3px;
                    border-radius: 3px;
                }
                QProgressBar {
                    border: 1px solid #555555;
                    border-radius: 3px;
                    background-color: #3C3C3C;
                    color: #FFFFFF;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #0078D7;
                    width: 10px;
                }
                QCheckBox {
                    color: #FFFFFF;
                }
                QCheckBox::indicator {
                    width: 13px;
                    height: 13px;
                }
            """
        else:
            return """
                QMainWindow, QDialog {
                    background-color: #F0F0F0;
                    color: #000000;
                }
                QWidget {
                    background-color: #F0F0F0;
                    color: #000000;
                }
                QPushButton {
                    background-color: #0078D7;
                    color: white;
                    border: none;
                    padding: 5px 10px;
                    border-radius: 3px;
                }
                QPushButton:hover {
                    background-color: #1C97EA;
                }
                QPushButton:disabled {
                    background-color: #CCCCCC;
                    color: #888888;
                }
                QLabel {
                    color: #000000;
                }
                QGroupBox {
                    border: 1px solid #CCCCCC;
                    border-radius: 5px;
                    margin-top: 10px;
                    font-weight: bold;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 3px 0 3px;
                }
                QComboBox, QLineEdit {
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 1px solid #CCCCCC;
                    padding: 3px;
                    border-radius: 3px;
                }
                QProgressBar {
                    border: 1px solid #CCCCCC;
                    border-radius: 3px;
                    background-color: #FFFFFF;
                    color: #000000;
                    text-align: center;
                }
                QProgressBar::chunk {
                    background-color: #0078D7;
                    width: 10px;
                }
                QCheckBox {
                    color: #000000;
                }
                QCheckBox::indicator {
                    width: 13px;
                    height: 13px;
                }
            """