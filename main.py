from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from Scanner import Scanner

css = """QMainWindow {
    background-color: #333;
    color: #fff;
}

QTextEdit, QLineEdit {
    background-color: #444;
    color: #fff;
    border: 1px solid #555;
    selection-background-color: #666;
    font-size: 16px;
}

QPushButton {
    background-color: #222;
    color: #fff;
    border: 1px solid #333;
    padding: 10px 20px;
    font-size: 16px;
}

QPushButton:hover {
    background-color: #444;
}

QLabel {
    color: #fff;
}

QTableWidget {
    background-color: #444;
    color: #fff;
}

QTableWidget QHeaderView::section {
    background-color: #333;
    color: #fff;
}

QTableWidget::item {
    background-color: #444;
    color: #fff;
    font-size: 16px;
}

QTableWidget::item:selected {
    background-color: #666;
}
"""


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()

        # Creating the main window
        self.setGeometry(100, 100, 850, 600)
        self.setWindowTitle("Scanner Application")

        # Center the main window on the screen
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = ((screen.width() - size.width()) // 2) - 50
        y = ((screen.height() - size.height()) // 2) - 50
        self.move(x, y)

        # Load icon from the file
        icon = QIcon("icon.png")
        self.setWindowIcon(icon)

        # Load the css
        self.setStyleSheet(css)

        # Creating the widgets
        main_widget = QWidget(self)
        left_widget = QWidget(self)
        middle_widget = QWidget(self)
        right_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Creating the layouts
        layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        middle_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        layout.addWidget(left_widget)
        layout.addWidget(middle_widget)
        layout.addWidget(right_widget)

        # Input label
        self.input_label = QLabel("Input:")
        left_layout.addWidget(self.input_label)

        # Text box for code input
        self.code_editor = QTextEdit()
        left_layout.addWidget(self.code_editor)

        # Load File button
        load_button = QPushButton("Load File")
        load_button.clicked.connect(self.loadFile)
        middle_layout.addWidget(load_button)

        # Scan button
        scan_button = QPushButton("Scan")
        scan_button.clicked.connect(self.scanCode)
        middle_layout.addWidget(scan_button)

        # Parse button
        parse_button = QPushButton("Parse")
        parse_button.clicked.connect(self.parseCode)
        middle_layout.addWidget(parse_button)

        # Export button
        export_button = QPushButton("Export File")
        export_button.clicked.connect(self.exportFile)
        middle_layout.addWidget(export_button)

        # Output label
        self.output_label = QLabel("Output:")
        right_layout.addWidget(self.output_label)

        # Table for output display
        self.output_table = QTableWidget(self)
        self.output_table.setColumnCount(2)  # Two columns for the tuple elements
        self.output_table.setHorizontalHeaderLabels(["Token", "Type"])  # Column headers
        self.output_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        right_layout.addWidget(self.output_table)

        # Setting the layout
        left_widget.setLayout(left_layout)
        middle_widget.setLayout(middle_layout)
        right_widget.setLayout(right_layout)
        main_widget.setLayout(layout)

    def loadFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "All Files (*);;Text Files (*.txt)", options=options
        )

        if file_name:
            with open(file_name, "r", encoding='utf-8') as file:
                file_contents = file.read()
                self.code_editor.setPlainText(file_contents)

    def scanCode(self):
        scanner.another_code(self.code_editor.toPlainText().rstrip())
        scanner_output = scanner.scan()

        # Clear the table before adding new data
        self.output_table.setRowCount(0)

        for item in scanner_output:
            # Add a new row to the table
            rowPosition = self.output_table.rowCount()
            self.output_table.insertRow(rowPosition)

            # Set the values from the tuple into the columns
            self.output_table.setItem(rowPosition, 0, QTableWidgetItem(str(item[0])))
            self.output_table.setItem(rowPosition, 1, QTableWidgetItem(str(item[1])))

    def parseCode(self):
        pass

    def exportFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save File", "", "Text Files (*.txt)", options=options
        )

        if file_name:
            with open(file_name, "w") as file:
                # Export the table data
                for row in range(self.output_table.rowCount()):
                    column1 = self.output_table.item(row, 0).text()
                    column2 = self.output_table.item(row, 1).text()
                    file.write(f"{column1}\t{column2}\n")


if __name__ == "__main__":
    scanner = Scanner()
    app = QApplication([])
    window = MyGUI()
    window.show()
    app.exec()
