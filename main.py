from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()

        # Creating the main window
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Scanner Application')

        # Center the main window on the screen
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        x = ((screen.width() - size.width()) // 2) - 50
        y = ((screen.height() - size.height()) // 2) - 50
        self.move(x, y)

        # Load icon from the file
        icon = QIcon('icon.png')
        self.setWindowIcon(icon)

        # Load the css
        self.setStyleSheet(open("dark_mode.css").read())

        # Creating the main widget
        main_widget = QWidget(self)
        self.setCentralWidget(main_widget)

        # Creating the layout
        layout = QVBoxLayout()

        # Input label
        self.input_label = QLabel('Input:')
        layout.addWidget(self.input_label)

        # Text box for code input
        self.code_editor = QTextEdit()
        layout.addWidget(self.code_editor)

        # Load File button
        load_button = QPushButton('Load File')
        load_button.clicked.connect(self.loadFile)
        layout.addWidget(load_button)

        # Scan button
        scan_button = QPushButton('Scan')
        scan_button.clicked.connect(self.scanCode)
        layout.addWidget(scan_button)

        # Parse button
        parse_button = QPushButton('Parse')
        parse_button.clicked.connect(self.parseCode)
        layout.addWidget(parse_button)

        # Export button
        export_button = QPushButton('Export File')
        export_button.clicked.connect(self.exportFile)
        layout.addWidget(export_button)

        # Output label
        self.output_label = QLabel('Output:')
        layout.addWidget(self.output_label)

        # Text box for output display
        self.output_editor = QTextEdit()
        layout.addWidget(self.output_editor)

        # Setting the layout
        main_widget.setLayout(layout)

    def loadFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'All Files (*);;Text Files (*.txt)',
                                                   options=options)

        if file_name:
            with open(file_name, 'r') as file:
                file_contents = file.read()
                self.code_editor.setPlainText(file_contents)

    def scanCode(self):
        # Implement your scanning logic here
        scanned_output = "Scanning result will be displayed here."
        self.output_editor.setPlainText(scanned_output)

    def parseCode(self):
        # Implement your parsing logic here
        parsed_output = "Parsing result will be displayed here."
        self.output_editor.setPlainText(parsed_output)

    def exportFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt)', options=options)

        if file_name:
            with open(file_name, 'w') as file:
                output_text = self.output_editor.toPlainText()
                file.write(output_text)


if __name__ == "__main__":
    app = QApplication([])
    window = MyGUI()
    window.show()
    app.exec()
