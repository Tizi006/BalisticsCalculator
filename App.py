from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from pynput import mouse, keyboard
from enum import Enum
import sys
from BalisticsCalculation import solve_ballistic_arc
from AppRepo import load_gravity, save_gravity,save_reset_hot_key,load__reset_hot_key


# Global variables------------------------------------------------------------
class Status(Enum):
    READY = "Ready"
    LISTENING = "Listening"
    FINISHED = "Finished"


# Define the application------------------------------------------------------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.status = Status.READY
        self.clicks = []

        self.keyboard_listener = None
        self.mouse_listener = None
        self.init_listeners()

        self.setWindowTitle("Skill Issue")
        self.setGeometry(100, 100, 200, 460)
        # Make the window stay on top
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        # -- Settings Group Box --
        settings_group_box = QGroupBox("Settings")
        settings_group_box.setFixedHeight(130)
        settings_layout = QVBoxLayout()

        # Hotkey input
        self.hotkey_label = QLabel("Reset Hotkey:")
        self.hotkey_label.setFixedHeight(20)
        self.hotkey_input = QLineEdit()
        self.hotkey_input.setText("r")
        self.hotkey_input.setPlaceholderText("Enter hotkey (e.g., 'r')")
        self.hotkey_input.setFixedHeight(20)
        self.hotkey_input.setFixedWidth(70)
        self.hotkey_input.setText(load__reset_hot_key())
        self.hotkey_input.editingFinished.connect(self.on_hotkey_input)

        # Gravity
        self.gravity_label = QLabel("Gravity:")
        self.gravity_input = QLineEdit()
        self.gravity_input.setFixedHeight(20)
        self.gravity_input.setFixedWidth(70)
        self.gravity_input.setPlaceholderText("Not Set")
        self.gravity_input.setText(str(load_gravity()))
        self.gravity_input.editingFinished.connect(self.on_gravity_edit)

        # Add widgets to settings layout
        settings_layout.addWidget(self.hotkey_label)
        settings_layout.addWidget(self.hotkey_input)
        settings_layout.addWidget(self.gravity_label)
        settings_layout.addWidget(self.gravity_input)
        settings_group_box.setLayout(settings_layout)

        # Shooter and Target position labels
        self.shooter_label = QLabel("Shooter position: Not set")
        self.shooter_label.setFixedHeight(20)
        self.target_label = QLabel("Target position: Not set")
        self.target_label.setFixedHeight(20)

        self.clicks_group_box = QGroupBox("Status: " + self.status.value)
        self.clicks_group_box.setFixedHeight(70)
        group_layout = QVBoxLayout()
        group_layout.addWidget(self.shooter_label)
        group_layout.addWidget(self.target_label)
        self.clicks_group_box.setLayout(group_layout)

        # Create a QTableWidget for displaying results
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(3)  # Power, High Angle, Shallow Angle
        self.result_table.setHorizontalHeaderLabels(["Power", "High", "Shallow"])
        self.result_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.result_table.setColumnWidth(0, 50)  # Power column width
        self.result_table.setColumnWidth(1, 50)  # High Angle column width
        self.result_table.setColumnWidth(2, 50)  # Shallow Angle column width

        # Layout to organize widgets vertically
        layout = QVBoxLayout()
        layout.addWidget(settings_group_box)
        layout.addWidget(self.clicks_group_box)
        layout.addWidget(self.result_table)

        # Set central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.clearFocus()

    def init_listeners(self):
        # Mouse listener
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.mouse_listener.start()

        # Keyboard listener
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)
        self.keyboard_listener.start()

    # Util Methods--------------------------------------------------------------------

    def update_status(self, new_status):
        self.status = new_status
        self.clicks_group_box.setTitle("Status: " + self.status.value)

    def reset_clicks(self):
        self.clicks = []  # Clear the click list
        self.mouse_listener.run()
        self.update_status(Status.LISTENING)
        self.shooter_label.setText("Shooter position: Not set")
        self.target_label.setText("Target position: Not set")
        self.result_table.clearContents()
        self.result_table.setRowCount(0)
        print("Counter reset. Ready for new clicks.")

    def update_calculation(self):
        angle_differences = []

        # Loop through each power level from 20 to 100
        for power in range(20, 101):
            # Get the angles for the current power level
            low_ange, high_angle = solve_ballistic_arc(self.clicks[0], self.clicks[1],
                                                       power, float(self.gravity_input.text()))

            if high_angle is not None:  # Only consider valid steep angles
                # Calculate the difference to the nearest whole numbers
                diff_to_whole = abs(high_angle - round(high_angle))

                # Store the difference and the corresponding angle in the list
                angle_differences.append((diff_to_whole, power, high_angle, low_ange))

        # Sort the angles by the smallest difference to a whole number
        angle_differences.sort()

        # Get the 5 best values closest to a whole number (top 5 smallest differences)
        best_angles = angle_differences[:5]

        # Find the first occurrence where power == 100 and append it to best_angles
        for angle in angle_differences:
            if angle[1] == 100:
                best_angles.append(angle)
                break

        for _, power, high_angle, low_ange in best_angles:
            # Add to table
            row = self.result_table.rowCount()
            self.result_table.insertRow(row)
            # Add items to each column
            self.result_table.setItem(row, 0, QTableWidgetItem(f"{power}"))
            self.result_table.setItem(row, 1, QTableWidgetItem(f"{high_angle:.2f}"))
            self.result_table.setItem(row, 2, QTableWidgetItem(f"{low_ange:.2f}"))

    # Event-----------------------------------------------------------r
    def on_press(self, key):
        try:
            if self.hotkey_input.text() and key.char == self.hotkey_input.text()[0]:
                self.reset_clicks()  # Call the reset function
        except AttributeError:
            pass

    def on_click(self, x, y, button, pressed):
        if pressed and self.status != Status.FINISHED:
            # left to is 0/0
            self.clicks.append((x, y))

            if len(self.clicks) == 1:
                self.shooter_label.setText(f"Shooter position: ({x}, {y})")
                self.update_status(Status.LISTENING)
            elif len(self.clicks) == 2:
                self.target_label.setText(f"Target position: ({x}, {y})")
                self.update_status(Status.FINISHED)
                self.mouse_listener.wait()
                self.update_calculation()
            # Debug
            coords = (x, y)
            print(coords)

    def on_gravity_edit(self):
        text = self.gravity_input.text()
        try:
            new_gravity = float(text)
            save_gravity(new_gravity)
        except ValueError:
            print("Invalid input. Gravity must be a number.")
            self.gravity_input.clearMask()

    def on_hotkey_input(self):
        hot_key = self.hotkey_input.text()
        try:
            save_reset_hot_key(hot_key)
        except ValueError:
            print("Invalid input, Error :(")
            self.gravity_input.clearMask()


# Show the window
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
