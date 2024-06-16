import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QDialog, QMessageBox
from PyQt5.QtCore import QTimer
import pickle
import os

# Global variables for storing value and value per second
value = 0
value_per_second = 0
label = None  # Declare label as global
auto_save_interval = 5  # Auto save interval in seconds

class StoreWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Store')
        self.setGeometry(150, 150, 300, 200)

        self.init_ui()

    def init_ui(self):
        global value
        
        self.layout = QVBoxLayout()

        self.info_label = QLabel(f'Value: {value}')
        self.layout.addWidget(self.info_label)

        self.buttons = []

        # Define button configurations (cost and value per second)
        button_configs = [
            {"text": "Button 1 (cost 25, gives 2 value per second)", "cost": 25, "rate": 2},
            {"text": "Button 2 (cost 50, gives 5 value per second)", "cost": 50, "rate": 5},
            {"text": "Button 3 (cost 100, gives 25 value per second)", "cost": 100, "rate": 25}
        ]

        for config in button_configs:
            button = QPushButton(config["text"])
            button.clicked.connect(lambda checked, cfg=config: self.buy_value_per_second(cfg["cost"], cfg["rate"]))
            self.layout.addWidget(button)
            self.buttons.append(button)

        self.setLayout(self.layout)

    def buy_value_per_second(self, cost, rate):
        global value, value_per_second
        if value >= cost:
            value -= cost
            value_per_second += rate
            save_value_per_second()  # Save value per second after purchase
            self.info_label.setText(f'Value: {value}')
            label.setText(f'Value: {value}')
        else:
            self.info_label.setText('Not enough value')

def save_value_per_second():
    global value_per_second
    save_dir = os.path.expanduser("~/Documents/hamsterkombat")
    os.makedirs(save_dir, exist_ok=True)  # Create folder if it doesn't exist
    save_path = os.path.join(save_dir, 'value_per_second.pkl')
    
    try:
        with open(save_path, 'wb') as f:
            pickle.dump(value_per_second, f)
            print(f"Saved value_per_second {value_per_second} to {save_path}")
    except Exception as e:
        print(f"Error saving value_per_second: {e}")

def load_value_per_second():
    global value_per_second
    save_path = os.path.expanduser("~/Documents/hamsterkombat/value_per_second.pkl")

    try:
        with open(save_path, 'rb') as f:
            value_per_second = pickle.load(f)
            print(f"Loaded value_per_second {value_per_second} from {save_path}")
    except FileNotFoundError:
        print(f"Save file not found: {save_path}")

def save_value():
    global value
    save_dir = os.path.expanduser("~/Documents/hamsterkombat")
    os.makedirs(save_dir, exist_ok=True)  # Create folder if it doesn't exist
    save_path = os.path.join(save_dir, 'value.pkl')
    
    try:
        with open(save_path, 'wb') as f:
            pickle.dump(value, f)
            print(f"Saved value {value} to {save_path}")
    except Exception as e:
        print(f"Error saving value: {e}")

def load_value():
    global value
    save_path = os.path.expanduser("~/Documents/hamsterkombat/value.pkl")

    try:
        with open(save_path, 'rb') as f:
            value = pickle.load(f)
            print(f"Loaded value {value} from {save_path}")
    except FileNotFoundError:
        print(f"Save file not found: {save_path}")

def main():
    global label, value, value_per_second

    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle('Hamster Kombat')
    window.setGeometry(100, 100, 300, 200)

    # Create the label
    global label
    label = QLabel('Value: ' + str(value))

    # Create the main vertical layout
    vbox = QVBoxLayout()

    # Add the label
    vbox.addWidget(label)

    # Create the "Hamster" button
    hamster_button = QPushButton('Hamster')
    vbox.addWidget(hamster_button)

    # Create the store button
    store_button = QPushButton('Store')
    vbox.addWidget(store_button)

    # Set the main layout in the main window
    window.setLayout(vbox)

    # Connect button events to functions
    hamster_button.clicked.connect(on_button_clicked)
    store_button.clicked.connect(on_store_button_clicked)

    # Load initial value and value_per_second from file
    load_value()
    load_value_per_second()

    # Show the main window
    window.show()

    # Start value_per_second incrementation
    QTimer.singleShot(0, lambda: start_value_per_second_increment())

    # Run the application
    sys.exit(app.exec_())

def start_value_per_second_increment():
    global value_per_second, value
    value += value_per_second
    label.setText(f'Value: {value}')
    QTimer.singleShot(1000, start_value_per_second_increment)  # Call itself every second

def on_button_clicked():
    global value, label
    value += 1
    label.setText('Value: ' + str(value))
    save_value()  # Save value on button click

def on_store_button_clicked():
    store_window = StoreWindow()
    store_window.exec_()

if __name__ == "__main__":
    main()
