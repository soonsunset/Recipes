import base64
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QLineEdit, QPlainTextEdit, QFileDialog
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QFont
from PyQt5.QtCore import QSize


class AddNewRecipe(QDialog):
    def __init__(self, login, user_id):
        super().__init__()
        self.user_login = login
        self.user_id = user_id

        self.pixmap_uploaded_image = None
        self.encoded_string = None

        self.window_height = 550
        self.window_width = 400
        self.resize(self.window_height, self.window_width)
        self.setFixedSize(self.size())
        self.setWindowTitle("Новый рецепт")
        self.setWindowIcon(QIcon('./assets/write_pen_icon.png'))

        self.add_rec_image = QImage("./assets/add_new_rec_page.PNG")
        self.add_rec_image = self.add_rec_image.scaled(QSize(self.window_height, self.window_width))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.add_rec_image))
        self.setPalette(self.palette)

        self.labels_font = QFont("Arial", 12)
        self.labels_font.setBold(True)

        self.lines_font = QFont("Arial", 12)

        self.title_rcp_lbl = QLabel("Название рецепта", self)
        self.title_rcp_lbl.setFont(self.labels_font)
        self.title_rcp_lbl.move(40, 15)
        self.title_rcp_lbl.setStyleSheet("color: rgb(56, 21, 99)")

        self.ingr_rcp_lbl = QLabel("Ингредиенты", self)
        self.ingr_rcp_lbl.setFont(self.labels_font)
        self.ingr_rcp_lbl.move(40, 60)
        self.ingr_rcp_lbl.setStyleSheet("color: rgb(56, 21, 99)")

        self.decs_rcp_lbl = QLabel("Описание", self)
        self.decs_rcp_lbl.setFont(self.labels_font)
        self.decs_rcp_lbl.move(40, 115)
        self.decs_rcp_lbl.setStyleSheet("color: rgb(56, 21, 99)")

        self.title_rcp_line = QLineEdit(self)
        self.title_rcp_line.setMaxLength(47)
        self.title_rcp_line.move(207, 14)
        self.title_rcp_line.resize(300, 25)
        self.title_rcp_line.setFont(self.lines_font)

        self.ingr_rcp_line = QPlainTextEdit(self)
        self.ingr_rcp_line.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.ingr_rcp_line.move(207, 59)
        self.ingr_rcp_line.resize(300, 50)

        self.decs_rcp_line = QPlainTextEdit(self)
        self.decs_rcp_line.setLineWrapMode(QPlainTextEdit.WidgetWidth)
        self.decs_rcp_line.move(40, 150)
        self.decs_rcp_line.resize(466, 170)

        self.image_ent_btn = QPushButton(self)
        self.image_ent_btn.setIcon(QIcon('./assets/fileupload_icon.png'))
        self.image_ent_btn_styleSheet = """
                                                    QPushButton {
                                                        border: none;
                                                    }

                                                    QPushButton:hover {
                                                        background-color: rgb(247, 252, 252);
                                                    }
                                                """
        self.image_ent_btn.setStyleSheet(self.image_ent_btn_styleSheet)
        self.image_ent_btn.setIconSize(QSize(40, 33))
        self.image_ent_btn.resize(37, 37)
        self.image_ent_btn.setToolTip("Вставить изображение блюда")
        self.image_ent_btn.move(40, 330)

        self.image_ent_btn.clicked.connect(self.image_ent_btn_clicked)

        self.img_info_label = QLabel("Изображение загружено", self)
        self.img_info_label.move(80, 343)
        self.img_info_label.hide()

        self.add_new_recp_final_but = QPushButton("Добавить рецепт", self)
        self.add_recp_btn_styleSheet = """
                                                    QPushButton {
                                                        background-color: rgb(234, 245, 247);
                                                    }

                                                    QPushButton:hover {
                                                        background-color: rgb(247, 252, 252);
                                                    }
                                                """
        self.add_new_recp_final_but.setStyleSheet(self.add_recp_btn_styleSheet)
        self.add_new_recp_final_but.resize(150, 30)
        self.add_new_recp_final_but.move(356, 350)
        self.add_new_recp_final_but.setFont(self.labels_font)

    def image_ent_btn_clicked(self):
        file_path, _ = QFileDialog.getOpenFileName(
            None, 'Выбрать изображение', '', 'Изображения (*.png *.xpm *.jpg *.bmp *.jpeg)')

        if file_path:
            self.img_info_label.show()
            with open(file_path, "rb") as image_file:
                self.encoded_string = base64.b64encode(image_file.read())

