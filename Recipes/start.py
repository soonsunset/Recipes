import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from auth import Authentication
from profile import UserProfile
from databaseactions import DataBaseActions


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.auth = Authentication()
        self.auth.login_acc_db_but.clicked.connect(self.check_fields_login)
        self.auth.create_acc_db_but.clicked.connect(self.check_fields_password)
        self.auth.show()

    def db_user_log(self):
        login, password = self.auth.get_login_and_password()
        self.db_info = DataBaseActions(login, password)

    def check_fields_login(self):
        if self.auth.login_field.text() == "" or self.auth.password_field.text() == "":
            QMessageBox.warning(self.auth, "Внимание", "Заполните необходимую информацию.")
        else:
            self.evt_db_request_login()

    def check_fields_password(self):
        if self.auth.login_field.text() == "" or self.auth.password_field.text() == "":
            QMessageBox.warning(self.auth, "Внимание", "Заполните необходимую информацию.")
        else:
            self.evt_db_create_acc()

    def evt_db_request_login(self):
        self.db_user_log()
        returned_answer = self.db_info.login_request()
        if returned_answer == 1:
            QMessageBox.information(self.auth, "Внимание", "Такого аккаунта нет.\nВам необходимо зарегистрироваться.")
            self.auth.login_acc_db_but.hide()
            self.auth.update_auth_page()
        elif returned_answer == 3:
            QMessageBox.critical(self.auth, "Внимание", "Введен неверный пароль!")
            self.auth.clear_login_and_password_fields()
        else:
            self.auth.login_acc_db_but.hide()
            self.auth.update_auth_page()
            self.auth.hide()
            self.profile_creation()

    def evt_db_create_acc(self):
        self.db_user_log()
        self.db_info.create_acc_request()
        self.auth.create_acc_db_but.hide()
        self.auth.update_auth_page()
        self.auth.hide()
        self.profile = UserProfile(self.db_info.login, self.db_info.id)
        self.profile.show()

    def profile_creation(self):
        self.profile = UserProfile(self.db_info.login, self.db_info.id)
        self.profile.log_out_but.clicked.connect(self.log_out_but_clicked)
        self.profile.show()

    def log_out_but_clicked(self):
        self.profile.hide()
        self.auth.show()


app = QApplication(sys.argv)
main_window = MainWindow()
sys.exit(app.exec())
