import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMenuBar, QAction, QScrollArea, QFileDialog, QMenu, QDialog, QFormLayout, QDialogButtonBox, QComboBox
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap
import dill as pickle
import random

class AttributeDialog(QDialog):
    def __init__(self, data, meta, parent=None):
        super().__init__(parent)
        self.data = data
        self.meta = meta
        self.setWindowTitle("Edit Attributes")
        self.layout = QFormLayout(self)

        self.editors = []
        for i in range(len(self.data)):
            editor = QLineEdit(str(self.data[i]))
            self.layout.addRow(f"{self.meta[i]}", editor)
            self.editors.append(editor)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def accept(self):
        for i, editor in enumerate(self.editors):
            self.data[i] = editor.text() if editor.text() else None
        super().accept()

class ShortcutDialog(QDialog):
    def __init__(self, shortcuts, parent=None):
        super().__init__(parent)
        self.shortcuts = shortcuts
        self.setWindowTitle("Select Shortcut")
        self.layout = QVBoxLayout(self)

        self.combo_box = QComboBox()
        for key, value in self.shortcuts.items():
            if value:  # Only add non-empty shortcuts
                self.combo_box.addItem(f"{key}: {value[0]}", key)
        self.layout.addWidget(self.combo_box)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        self.layout.addWidget(self.button_box)

    def get_selected_shortcut(self):
        return self.combo_box.currentData()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Grid Editor")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll_area)

        self.grid_layout = QGridLayout(self.scroll_content)
        self.scroll_content.setLayout(self.grid_layout)

        self.grid_size = (100, 100)
        self.cell_size = 50
        self.data = [[["None", None, None] for _ in range(self.grid_size[0])] for _ in range(self.grid_size[1])]
        self.meta = [[["Name", "Save Id", "Sprite Path"] for _ in range(self.grid_size[1])] for _ in range(self.grid_size[0])]

        self.init_grid()

        self.init_menu()

        self.dragging = False
        self.drag_start_position = QPoint()
        self.hovered_cell = None  # Track the hovered cell
        self.shortcuts = self.load_shortcuts()

    def load_shortcuts(self):
        try:
            from editconfig import data, meta, X, Y
        except ImportError:
            print("Editconfig Not found creating template file")
            Output = """class X: pass
                    class Y: pass

                    data = {
                        1: [],
                        2: [],
                        3: [],
                        4: [],
                        5: [],
                        6: [],
                        7: [],
                        8: [],
                        9: [],
                        0: []
                    }

                    meta = {
                        1: [],
                        2: [],
                        3: [],
                        4: [],
                        5: [],
                        6: [],
                        7: [],
                        8: [],
                        9: [],
                        0: []
                    }"""
            with open("editconfig.py", "w") as f:
                f.write(Output)
            from editconfig import data, meta, X, Y

        self.short_data = data
        self.short_meta = meta
        self.short_x = X
        self.short_y = Y

    def init_grid(self):
        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                label = QLabel()
                label.setFixedSize(self.cell_size, self.cell_size)
                label.setAlignment(Qt.AlignCenter)
                label.setStyleSheet("border: 1px solid black;")
                label.setContextMenuPolicy(Qt.CustomContextMenu)
                label.customContextMenuRequested.connect(lambda pos, y=y, x=x: self.show_context_menu(pos, y, x))
                label.installEventFilter(self)  # Install event filter to track hover events
                self.grid_layout.addWidget(label, y, x)
                self.update_label(y, x)

    def update_label(self, y, x):
        label = self.grid_layout.itemAtPosition(y, x).widget()
        if self.data[y][x][2] is not None and self.data[y][x][2] != "None":
            pixmap = QPixmap(self.data[y][x][2])
            pixmap = pixmap.scaled(self.cell_size, self.cell_size, Qt.KeepAspectRatio)
            label.setPixmap(pixmap)
        else:
            label.setText(self.data[y][x][0])

    def submit_name(self):
        name = self.input_text.text()
        self.data[0][0] = name  # Example: Update the first cell with the entered name
        self.update_label(0, 0)

    def init_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        view_menu = menu_bar.addMenu("View")
        generate_menu = menu_bar.addMenu("Generate")

        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)

        open_action.triggered.connect(self.load_file)
        save_action.triggered.connect(self.save_file)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        undo_action = QAction("Undo", self)
        redo_action = QAction("Redo", self)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        zoom_in_action = QAction("Zoom In", self)
        zoom_out_action = QAction("Zoom Out", self)
        zoom_in_action.triggered.connect(self.zoom_in)
        zoom_out_action.triggered.connect(self.zoom_out)

        view_menu.addAction(zoom_in_action)
        view_menu.addAction(zoom_out_action)

        random_single_action = QAction("Random Single", self)
        random_single_action.triggered.connect(self.random_single)

        generate_menu.addAction(random_single_action)

    def random_single(self):
        dialog = ShortcutDialog(self.short_data, self)
        if dialog.exec_():
            key = dialog.get_selected_shortcut()
            chosen_data = self.short_data[key]
            chosen_meta = self.short_meta[key]

        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                i = random.randint(1, 10)
                if i > 5:
                    self.data[y][x] = [item if item not in [self.short_x, self.short_y] else y if item == self.short_y else x for item in chosen_data]
                    self.meta[y][x] = chosen_meta
                else:
                    self.data[y][x] = [item if item not in [self.short_x, self.short_y] else y if item == self.short_y else x for item in self.short_data[1]]
                    self.meta[y][x] = self.short_meta[1]
                self.update_label(y, x)
                

    def load_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Pickle Files (*.pkl)", options=options)
        if file_name:
            print(file_name)
            with open(file_name, "rb") as f:
                self.data = pickle.load(f)

            meta_path = file_name + ":meta"
            with open(meta_path, "rb") as f:
                self.meta = pickle.load(f)

            self.update_grid()

    def save_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Pickle Files (*.pkl)", options=options)
        if file_name:
            with open(file_name, "wb") as f:
                pickle.dump(self.data, f)

            meta_path = file_name + ":meta"
            with open(meta_path, "wb") as f:
                pickle.dump(self.meta, f)

    def zoom_in(self):
        self.cell_size += 10
        self.update_grid()

    def zoom_out(self):
        self.cell_size = max(10, self.cell_size - 10)
        self.update_grid()

    def update_grid(self):
        for y in range(self.grid_size[1]):
            for x in range(self.grid_size[0]):
                self.update_label(y, x)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            delta = event.pos() - self.drag_start_position
            self.scroll_area.horizontalScrollBar().setValue(self.scroll_area.horizontalScrollBar().value() - delta.x())
            self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().value() - delta.y())
            self.drag_start_position = event.pos()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def eventFilter(self, source, event):
        if event.type() == event.Enter and isinstance(source, QLabel):
            pos = self.grid_layout.indexOf(source)
            if pos != -1:
                y, x = divmod(pos, self.grid_size[0])
                self.hovered_cell = (y, x)
        elif event.type() == event.Leave and isinstance(source, QLabel):
            self.hovered_cell = None
        return super().eventFilter(source, event)

    def keyPressEvent(self, event):
        if event.key() in range(Qt.Key_0, Qt.Key_9 + 1):
            if self.hovered_cell:
                y, x = self.hovered_cell
                key = event.key() - Qt.Key_0
                if key in self.short_data and self.short_data[key]:
                    self.data[y][x] = [item if item not in [self.short_x, self.short_y] else y if item == self.short_y else x for item in self.short_data[key]]
                    self.meta[y][x] = self.short_meta[key]
                    self.update_label(y, x)

    def show_context_menu(self, pos, y, x):
        context_menu = QMenu(self)
        edit_action = context_menu.addAction("Edit Attributes")
        copy_action = context_menu.addAction("Copy")
        paste_action = context_menu.addAction("Paste")
        action = context_menu.exec_(self.scroll_content.mapToGlobal(pos))
        if action == edit_action:
            self.edit_attributes(y, x)
        elif action == copy_action:
            self.copy_cell(y, x)
        elif action == paste_action:
            self.paste_cell(y, x)

    def edit_attributes(self, y, x):
        dialog = AttributeDialog(self.data[y][x], self.meta[y][x], self)
        if dialog.exec_():
            self.update_label(y, x)

    def copy_cell(self, y, x):
        self.data_copy = self.data[y][x].copy()
        self.meta_copy = self.meta[y][x].copy()

    def paste_cell(self, y, x):
        if hasattr(self, 'data_copy') and hasattr(self, 'meta_copy'):
            self.data[y][x] = self.data_copy.copy()
            self.meta[y][x] = self.meta_copy.copy()
            self.update_label(y, x)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())