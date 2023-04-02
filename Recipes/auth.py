from PyQt5.QtCore import QSize
from PyQt5.QtGui import QImage, QPalette, QBrush, QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit


class Authentication(QWidget):
    def __init__(self):
        super().__init__()
        # |-------------------ОПИСАНИЕ ОКНА -----------------------|
        self.window_height = 700
        self.window_width = 500
        self.resize(self.window_height, self.window_width)
        self.setFixedSize(self.size())
        self.setWindowTitle("Программа 'Рецепты'")
        self.setWindowIcon(QIcon('./assets/main_window_icon.png'))

        self.auth_image = QImage("./assets/auth_final_page.PNG")
        self.auth_image = self.auth_image.scaled(QSize(self.window_height, self.window_width))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.auth_image))
        self.setPalette(self.palette)

        self.buts_font = QFont("Garamond", 23)
        self.buts_font.setBold(True)
        self.descr_styleSheet = """
                                    QPushButton {
                                        background-color: rgb(125, 190, 70);
                                    }

                                    QPushButton {
                                        color: white;
                                    }

                                    QPushButton:hover {
                                        background-color: rgb(177, 227, 136);
                                    }
                                """

        # |------------------- СОЗДАТЬ АККАУНТ КНОПКА ---------------------|

        self.create_acc_but = QPushButton("СОЗДАТЬ АККАУНТ", self)
        self.create_acc_but.move(194, 300)
        self.create_acc_but.resize(320, 60)
        self.create_acc_but.setFont(self.buts_font)
        self.create_acc_but.setStyleSheet(self.descr_styleSheet)

        self.create_acc_but.clicked.connect(self.evt_create_acc_clicked)

        # |-------------- ВОЙТИ В АККАУНТ КНОПКА -----------------|

        self.login_acc_but = QPushButton("ВОЙТИ", self)
        self.login_acc_but.move(194, 400)
        self.login_acc_but.resize(320, 60)
        self.login_acc_but.setFont(self.buts_font)
        self.login_acc_but.setStyleSheet(self.descr_styleSheet)

        self.login_acc_but.clicked.connect(self.evt_login_acc_clicked)

        # |--------------- ПОЛЯ ВВОДА ЛОГИНА/ПАРОЛЯ ---------------|

        self.login_field = QLineEdit(self)
        self.login_field.hide()
        self.login_field.setMaxLength(30)
        self.login_field.setPlaceholderText("Введите логин")
        self.login_field.move(239, 280)
        self.login_field.resize(280, 40)
        self.login_field_font = QFont("Arial", 18)
        self.login_field.setFont(self.login_field_font)

        self.password_field = QLineEdit(self)
        self.password_field.hide()
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setMaxLength(30)
        self.password_field.setPlaceholderText("Введите пароль")
        self.password_field.move(239, 340)
        self.password_field.resize(280, 40)
        self.password_field_font = QFont("Arial", 18)
        self.password_field.setFont(self.password_field_font)

        self.log_icon_lbl = QLabel(self)
        pixmap_for_log_icon_lbl = QPixmap('./assets/log_auth_icon.png')
        pixmap_for_log_icon_lbl = pixmap_for_log_icon_lbl.scaled(46, 46)
        self.log_icon_lbl.setPixmap(pixmap_for_log_icon_lbl)
        self.log_icon_lbl.resize(50, 50)
        self.log_icon_lbl.move(181, 274)
        self.log_icon_lbl.hide()

        self.pas_icon_lbl = QLabel(self)
        pixmap_for_pas_icon_lbl = QPixmap('./assets/lock_auth_icon.png')
        pixmap_for_pas_icon_lbl = pixmap_for_pas_icon_lbl.scaled(46, 46)
        self.pas_icon_lbl.setPixmap(pixmap_for_pas_icon_lbl)
        self.pas_icon_lbl.resize(50, 50)
        self.pas_icon_lbl.move(181, 333)
        self.pas_icon_lbl.hide()

        self.back_but = QPushButton(self)
        self.back_but.hide()
        self.back_but.move(614, 25)
        self.back_but.resize(64, 64)
        self.back_but.setToolTip("Вернуться")
        self.back_but.setIcon(QIcon('./assets/arrow-left.png'))
        self.back_but.setIconSize(QSize(64, 64))
        self.back_but.setStyleSheet(self.descr_styleSheet)
        self.back_but.clicked.connect(self.back_but_clicked)

        # |-------- DataBase КНОПКИ ВХОДА/СОЗДАНИЯ АККАУНТА ---------|

        self.create_acc_db_but = QPushButton(self)
        self.create_acc_db_but.hide()
        self.create_acc_db_but.move(302, 410)
        self.create_acc_db_but.resize(100, 60)
        self.create_acc_db_but.setIcon(QIcon('./assets/user-plus.png'))
        self.create_acc_db_but.setIconSize(QSize(70, 70))
        self.create_acc_db_but.setStyleSheet(self.descr_styleSheet)

        self.login_acc_db_but = QPushButton(self)
        self.login_acc_db_but.hide()
        self.login_acc_db_but.move(302, 410)
        self.login_acc_db_but.resize(100, 60)
        self.login_acc_db_but.setIcon(QIcon('./assets/log-in.png'))
        self.login_acc_db_but.setIconSize(QSize(50, 50))
        self.login_acc_db_but.setStyleSheet(self.descr_styleSheet)

    def input_fields_display(self):
        self.login_acc_but.hide()
        self.create_acc_but.hide()
        self.login_field.show()
        self.password_field.show()
        self.log_icon_lbl.show()
        self.pas_icon_lbl.show()
        self.back_but.show()

    def evt_login_acc_clicked(self):
        self.login_acc_db_but.show()
        self.input_fields_display()

    def evt_create_acc_clicked(self):
        self.create_acc_db_but.show()
        self.input_fields_display()

    def get_login_and_password(self):
        login = self.login_field.text()
        password = self.password_field.text()
        return login, password

    def clear_login_and_password_fields(self):
        self.password_field.clear()
        self.login_field.clear()

    def update_auth_page(self):
        self.clear_login_and_password_fields()
        self.login_field.hide()
        self.log_icon_lbl.hide()
        self.password_field.hide()
        self.pas_icon_lbl.hide()
        self.back_but.hide()
        self.create_acc_but.show()
        self.login_acc_but.show()

    def back_but_clicked(self):
        if self.login_acc_db_but.isVisible():
            self.login_acc_db_but.hide()
        if self.create_acc_db_but.isVisible():
            self.create_acc_db_but.hide()
        self.update_auth_page()

