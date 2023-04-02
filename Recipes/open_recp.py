import base64
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QPlainTextEdit, QWidget, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QFont, QPixmap
from PyQt5.QtCore import QSize, Qt
from databaseactions import DataBaseActions


class OpenRecipe(QDialog):
    def __init__(self, user_id, title):
        super().__init__()
        self.user_id = user_id
        self.title = title

        self.window_height = 550
        self.window_width = 400
        self.resize(self.window_height, self.window_width)
        self.setFixedSize(self.size())

        self.setWindowTitle("Описание рецепта")
        self.setWindowIcon(QIcon('./assets/book_open_icon.png'))

        self.add_rec_image = QImage("./assets/add_new_rec_page.PNG")
        self.add_rec_image = self.add_rec_image.scaled(QSize(self.window_height, self.window_width))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.add_rec_image))
        self.setPalette(self.palette)

        self.titlefont = QFont("Arial", 13)
        self.titlefont.setBold(True)

        self.labs_font = QFont("Arial", 12)

        self.title_lbl = QLabel(self)
        self.title_lbl.setWordWrap(True)
        if len(self.title) > 90:
            self.displayed_title = self.title[:90] + "..."
            self.title_lbl.setText(self.displayed_title)
        else:
            self.title_lbl.setText(self.title)
        self.title_lbl.setFont(self.titlefont)
        self.title_lbl.setStyleSheet("color: rgb(56, 21, 99)")
        self.title_lbl.move(30, 10)
        self.title_lbl.resize(500, 40)

        self.ingr_lbl_one_word = QLabel("Ингредиенты", self)
        self.ingr_lbl_one_word.move(30, 60)
        self.ingr_lbl_one_word.setFont(self.labs_font)
        self.ingr_lbl_one_word.setStyleSheet("color: rgb(56, 21, 99)")

        general_request_text = DataBaseActions.ingredients_and_description_request(self.user_id, self.title)

        self.ingr_lbl_descr = QPlainTextEdit(self)
        self.ingr_lbl_descr.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.ingr_lbl_descr.setPlainText(general_request_text[0])
        self.ingr_lbl_descr.move(30, 90)
        self.ingr_lbl_descr.resize(350, 80)
        self.ingr_lbl_descr.setReadOnly(True)

        self.instr_lbl_one_word = QLabel("Инструкция приготовления", self)
        self.instr_lbl_one_word.move(30, 190)
        self.instr_lbl_one_word.setFont(self.labs_font)
        self.instr_lbl_one_word.setStyleSheet("color: rgb(56, 21, 99)")

        self.instr_lbl_descr = QPlainTextEdit(self)
        self.instr_lbl_descr.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.instr_lbl_descr.setPlainText(general_request_text[1])
        self.instr_lbl_descr.move(30, 222)
        self.instr_lbl_descr.resize(487, 152)
        self.instr_lbl_descr.setReadOnly(True)

        self.open_img_btn = QPushButton(self)
        self.open_img_btn.setIcon(QIcon('./assets/open_img_icon.png'))
        self.open_img_btn_styleSheet = """
                                                            QPushButton {
                                                                border: none;
                                                            }

                                                            QPushButton:hover {
                                                                background-color: rgb(247, 252, 252);
                                                            }
                                                        """
        self.open_img_btn.setStyleSheet(self.open_img_btn_styleSheet)
        self.open_img_btn.setIconSize(QSize(80, 80))
        self.open_img_btn.resize(80, 80)
        self.open_img_btn.setToolTip("Открыть изображение блюда")
        self.open_img_btn.move(415, 89)

        self.open_img_btn.clicked.connect(self.open_img_btn_clicked)

    def open_img_btn_clicked(self):
        result_from_db = DataBaseActions.get_recipe_image(self.user_id, self.title)
        if result_from_db is None:
            QMessageBox.warning(self, "Внимание", "Для данного рецепта отсутствует изображение.")
        else:
            self.open_image = OpenImage(self.user_id, self.title, result_from_db)
            self.open_image.show()


class OpenImage(QWidget):
    def __init__(self, user_id, title, result_from_db):
        super().__init__()
        self.user_id = user_id
        self.title = title

        self.setWindowTitle("Изображение")
        self.setWindowIcon(QIcon('./assets/book_open_icon.png'))

        self.window_width = 600
        self.window_height = 500
        self.resize(self.window_width, self.window_height)
        self.setFixedSize(self.size())

        pixmap = QPixmap()
        pixmap.loadFromData(base64.b64decode(result_from_db))

        pixmap.scaled(400, 350, Qt.KeepAspectRatio)

        self.image_fon = pixmap.toImage()
        self.image_fon = self.image_fon.scaled(QSize(self.window_width, self.window_height))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.image_fon))
        self.setPalette(self.palette)
