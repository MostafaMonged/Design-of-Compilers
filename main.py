import networkx as nx
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from matplotlib.figure import Figure

from Node import Node
from Scanner import Scanner

# Load the .ui file and generate the corresponding class dynamically
Ui_MainWindow, _ = loadUiType("./CompilerGUI.ui")


class MyGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()

        # Set up the user interface
        self.setupUi(self)

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
        self.setStyleSheet(open("css.css").read())

        # Text box for code input
        self.code_editor = self.textEdit

        # Load File button action listener
        self.Load_File.clicked.connect(self.loadFile)

        # Scan button action listener
        self.Scan.clicked.connect(self.scanCode)

        # Parse button action listener
        self.Parse.clicked.connect(self.parseCode)

        # Export button action listener
        self.Export_File.clicked.connect(self.exportFile)

        # Clear button action listener
        self.Clear.clicked.connect(self.clear_all)

        # Table for output display
        self.output_table = self.tableWidget
        self.output_table.setColumnCount(2)  # Two columns for the tuple elements
        self.output_table.setHorizontalHeaderLabels(["Token", "Type"])  # Column headers
        self.output_table.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.output_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def loadFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "Text Files (*.txt)", options=options
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
        # Create a root node
        root_node = Node(tokens=["root", "root_type"])

        # Add some sample structure
        child1 = Node(tokens=["child1", "child1_type"])
        child2 = Node(tokens=["child2", "child2_type"])
        root_node.add_child(child1)

        child1.add_neighbor(child2)

        # Creating the graph
        parse_tree = nx.Graph()

        # Add nodes and edges recursively
        self.addNodesAndEdges(parse_tree, root_node)

        # Creating positions
        pos = self.assignNodePositions(parse_tree, root_node)

        # Display the parse tree in the second tab
        self.clearParseTree()
        self.displayParseTree(parse_tree, pos)
        self.Tab_Widget.setCurrentIndex(1)

    def addNodesAndEdges(self, parse_tree, current_node):
        # Add the current node
        parse_tree.add_node(current_node.tokens[0])

        if current_node.neighbor is not None:
            parse_tree.add_node(current_node.neighbor.tokens[0])
            parse_tree.add_edge(current_node.tokens[0], current_node.neighbor.tokens[0])
            self.addNodesAndEdges(parse_tree, current_node.neighbor)

        i = 0
        # Recursively add nodes and edges for children
        for child in current_node.children:
            parse_tree.add_edge(current_node.tokens[0], current_node.children[i].tokens[0])
            self.addNodesAndEdges(parse_tree, child)
            i = i + 1

    def assignNodePositions(self, parse_tree, current_node, pos=None, level=0, sibling_index=0):
        if pos is None:
            pos = {}

        # Calculate position based on level and sibling index
        x = sibling_index
        y = -level

        # Assign position for the current node
        pos[current_node.tokens[0]] = (x, y)

        pos = self.assignNodePositions(parse_tree, current_node.neighbor, pos, level)

        for i, child in enumerate(current_node.children):
            pos = self.assignNodePositions(parse_tree, child, pos, level + 1, i)

        return pos

    def displayParseTree(self, parse_tree, pos):
        # Create a QGraphicsScene to display the parse tree
        scene = QGraphicsScene()

        # Create a QGraphicsView and set its size policy
        parse_tree_view = QGraphicsView(self.Tab_Widget.widget(1))
        parse_tree_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Draw the parse tree using networkx and matplotlib
        fig = Figure(figsize=(10.4, 6.75))
        ax = fig.add_subplot()

        nx.draw_networkx(parse_tree, pos=pos, with_labels=True, arrows=True, ax=ax, edge_color='black', node_size=3000,
                         node_shape='o')

        # Save the parse tree visualization to a temporary file
        temp_file = "parse_tree.png"
        fig.savefig(temp_file, format="PNG", bbox_inches="tight", pad_inches=0.1)

        # Load the saved image into QPixmap
        pixmap = QPixmap(temp_file)

        # Create a QGraphicsPixmapItem and add it to the scene
        pixmap_item = QGraphicsPixmapItem(pixmap)
        scene.addItem(pixmap_item)

        # Set the scene in the QGraphicsView
        parse_tree_view.setScene(scene)

    def clearParseTree(self):
        # Find the layout in the second tab and remove it
        layout_item = self.Tab_Widget.widget(1).layout()
        if layout_item:
            while layout_item.count():
                child = layout_item.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

        # Find the scene in the second tab and clear it
        parse_tree_view = self.Tab_Widget.widget(1).findChild(QGraphicsView)
        if parse_tree_view:
            scene = parse_tree_view.scene()
            if scene:
                scene.clear()

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
                    file.write(f"{column1}\t\t{column2}\n")

    def clear_all(self):
        self.output_table.setRowCount(0)
        self.code_editor.setPlainText("")


if __name__ == "__main__":
    scanner = Scanner()
    app = QApplication([])
    window = MyGUI()
    window.show()
    app.exec()
