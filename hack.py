import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5.QtCore import QTimer
import pickle
import os

# Global variables to be saved
value = 99999999999
value_per_second = 99999999999

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        # Timer for save_value_per_second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.save_value_per_second)
    
    def initUI(self):
        layout = QVBoxLayout()
        
        self.save_button = QPushButton('Накрутить Value', self)
        self.save_button.clicked.connect(self.save_value)
        layout.addWidget(self.save_button)
        
        self.save_per_second_button = QPushButton('Накрутить Value Per Second', self)
        self.save_per_second_button.clicked.connect(self.save_value_per_second)
        layout.addWidget(self.save_per_second_button)
        
        self.message_label = QLabel('Надо закрыть игру!', self)
        layout.addWidget(self.message_label)
        
        self.setLayout(layout)
        
        self.setWindowTitle('Hack Hamster kombat')
        self.setGeometry(300, 300, 300, 200)
        self.show()
    
    def save_value(self):
        global value
        save_dir = os.path.expanduser(r"~\Documents\hamsterkombat")
        os.makedirs(save_dir, exist_ok=True)  # Create folder if it doesn't exist
        save_path = os.path.join(save_dir, 'value.pkl')
    
        try:
            with open(save_path, 'wb') as f:
                pickle.dump(value, f)
            print(f"Saved value {value} to {save_path}")
        except Exception as e:
            print(f"Error saving value: {e}")
    
    def save_value_per_second(self):
        global value_per_second
        save_dir = os.path.expanduser(r"~\Documents\hamsterkombat")
        os.makedirs(save_dir, exist_ok=True)  # Create folder if it doesn't exist
        save_path = os.path.join(save_dir, 'value_per_second.pkl')
    
        try:
            with open(save_path, 'wb') as f:
                pickle.dump(value_per_second, f)
            print(f"Saved value_per_second {value_per_second} to {save_path}")
        except Exception as e:
            print(f"Error saving value_per_second: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
