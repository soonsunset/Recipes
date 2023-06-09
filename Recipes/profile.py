from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QListWidget, QHBoxLayout, QVBoxLayout, QMessageBox, QLineEdit
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QPixmap, QFont
from PyQt5.QtCore import QSize
from pars_recp import ParsingNewRecipe
from open_recp import OpenRecipe
from add_new_recp import AddNewRecipe
from edit_recp import EditRecipe
from databaseactions import DataBaseActions


class UserProfile(QWidget):
    def __init__(self, login, user_id):
        super().__init__()
        self.user_login = login
        self.user_id = user_id
        # |------------------ ОПИСАНИЕ ОКНА -----------------------|
        self.window_height = 700
        self.window_width = 500
        self.resize(self.window_height, self.window_width)
        self.setFixedSize(self.size())
        self.setWindowTitle("Профиль")
        self.setWindowIcon(QIcon('./assets/profile_icon.png'))

        self.auth_image = QImage("./assets/profile_image.PNG")
        self.auth_image = self.auth_image.scaled(QSize(self.window_height, self.window_width))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.auth_image))
        self.setPalette(self.palette)

        # |------------------ ОПИСАНИЕ ПРОФИЛЯ -----------------------|

        self.profile_image_label = QLabel(self)
        self.profile_pixmap = QPixmap("./assets/user_person_profile_avatar_icon.png")
        self.profile_image_label.setPixmap(self.profile_pixmap)
        self.profile_image_label.move(160, 5)
        self.profile_image_label.resize(150, 150)

        self.profile_name_label = QLabel("Пользователь:", self)
        self.profile_name_label.move(330, 33)
        self.profile_name_label_font = QFont("Garamond", 20)
        self.profile_name_label.setFont(self.profile_name_label_font)

        self.profile_login_db = QLabel(self)
        self.profile_login_db.move(330, 83)
        self.profile_login_db.setText(self.user_login)
        self.profile_login_db_font = QFont("Garamond", 19)
        self.profile_login_db.setFont(self.profile_name_label_font)

        self.recipe_list_label = QLabel("Список рецептов", self)
        self.recipe_list_label.move(148, 178)
        self.recipe_list_label_font = QFont("Garamond", 17)
        self.recipe_list_label.setFont(self.recipe_list_label_font)

        self.log_out_but = QPushButton(self)
        self.log_out_but.move(614, 25)
        self.log_out_but.resize(64, 64)
        self.log_out_but.setToolTip("Выйти")
        self.log_out_but.setIcon(QIcon('./assets/log_out.png'))
        self.log_out_but.setIconSize(QSize(64, 64))

        self.descr_styleSheet = """QPushButton {
                                                background-color: rgb(255, 255, 255);
                                                color: black;
                                                border: none;
                                                }

                                   QPushButton:hover {
                                                       background-color: rgb(242, 242, 242);
                                                    }
                                                """

        self.edit_profile_info = QPushButton(self)
        self.edit_profile_info.move(491, 15)
        self.edit_profile_info.resize(20, 20)
        self.edit_profile_info.setToolTip("Редактировать")
        self.edit_profile_info.setIcon(QIcon('./assets/write_pen_icon.png'))
        self.edit_profile_info.setIconSize(QSize(24, 24))
        self.edit_profile_info.setStyleSheet(self.descr_styleSheet)
        self.edit_profile_info.clicked.connect(self.edit_profile_btn_clicked)


        # |---------------- ВИДЖЕТ СПИСКА РЕЦЕПТОВ ----------------|

        widg_for_recipes = WidgetForRecipesList(self.user_login, self.user_id)
        widg_for_recipes.setParent(self)
        widg_for_recipes.move(140, 210)

        self.log_out_but.setStyleSheet(widg_for_recipes.descr_styleSheet)

        widg_for_recipes.show()

    def edit_profile_btn_clicked(self):
        self.profile_name_label.hide()
        self.profile_login_db.hide()
        self.edit_profile_info.hide()

        self.log_pas_change_font = QFont("Garamond", 17)

        self.save_profile_info = QPushButton(self)
        self.save_profile_info.move(491, 15)
        self.save_profile_info.resize(20, 20)
        self.save_profile_info.setToolTip("Сохранить")
        self.save_profile_info.setIcon(QIcon('./assets/check-square.png'))
        self.save_profile_info.setIconSize(QSize(24, 24))
        self.save_profile_info.setStyleSheet(self.descr_styleSheet)
        self.save_profile_info.show()
        self.save_profile_info.clicked.connect(self.save_profile_info_clicked)

        self.login_change_lbl = QLabel("Логин:", self)
        self.login_change_lbl.move(310, 17)
        self.login_change_lbl.setFont(self.log_pas_change_font)
        self.login_change_lbl.show()

        self.password_change_lbl = QLabel("Пароль:", self)
        self.password_change_lbl.move(310, 83)
        self.password_change_lbl.setFont(self.log_pas_change_font)
        self.password_change_lbl.show()

        self.lines_font = QFont("Arial", 12)

        self.login_change_line = QLineEdit(self)
        self.login_change_line.setMaxLength(25)
        self.login_change_line.move(310, 48)
        self.login_change_line.resize(200, 25)
        self.login_change_line.setFont(self.lines_font)
        self.login_change_line.show()

        self.password_change_line = QLineEdit(self)
        self.password_change_line.setMaxLength(25)
        self.password_change_line.move(310, 114)
        self.password_change_line.resize(200, 25)
        self.password_change_line.setFont(self.lines_font)
        self.password_change_line.show()

    def save_profile_info_clicked(self):
        self.new_login = self.login_change_line.text()
        self.new_password = self.password_change_line.text()

        DataBaseActions.update_profile_info_request(self.user_id, self.new_login, self.new_password)

        self.save_profile_info.hide()
        self.login_change_lbl.hide()
        self.password_change_lbl.hide()
        self.login_change_line.clear()
        self.login_change_line.hide()
        self.password_change_line.clear()
        self.password_change_line.hide()

        if self.new_login != "":
            self.profile_login_db.setText(self.new_login)

        self.profile_login_db.show()
        self.profile_name_label.show()
        self.edit_profile_info.show()


class WidgetForRecipesList(QWidget):
    def __init__(self, login, user_id):
        super().__init__()
        self.user_login = login
        self.user_id = user_id

        self.buts_font = QFont("Garamond", 14)
        self.buts_font.setBold(True)
        self.descr_styleSheet = """
                                            QPushButton {
                                                background-color: rgb(0, 0, 0);
                                            }

                                            QPushButton {
                                                color: white;
                                            }

                                            QPushButton:hover {
                                                background-color: rgb(255, 138, 54);
                                            }
                                        """

        self.resize(430, 270)

        self.create_recipes_list_and_buttons()

        self.setup_layout()

        self.add_buts_to_buttons_layout()

    def create_recipes_list_and_buttons(self):
        self.recipes_list_widg = QListWidget()
        titles = self.get_list_from_db()
        self.recipes_list_widg.addItems(titles)
        self.recipes_list_widg.sortItems()

        self.open_recipe_btn = QPushButton("Открыть", self)
        self.open_recipe_btn.setToolTip("Открыть описание рецепта")
        self.open_recipe_btn.clicked.connect(self.open_recipe_btn_clicked)
        self.open_recipe_btn.setFont(self.buts_font)
        self.open_recipe_btn.setStyleSheet(self.descr_styleSheet)

        self.edit_recipe_btn = QPushButton("Редактировать", self)
        self.edit_recipe_btn.setToolTip("Редактировать рецепт")
        self.edit_recipe_btn.clicked.connect(self.edit_recipe_btn_clicked)
        self.edit_recipe_btn.setFont(self.buts_font)
        self.edit_recipe_btn.setStyleSheet(self.descr_styleSheet)

        self.add_recipe_btn = QPushButton("Добавить", self)
        self.add_recipe_btn.setToolTip("Самостоятельно добавить новый рецепт")
        self.add_recipe_btn.clicked.connect(self.add_recipe_btn_clicked)
        self.add_recipe_btn.setFont(self.buts_font)
        self.add_recipe_btn.setStyleSheet(self.descr_styleSheet)

        self.find_recipe_btn = QPushButton("Найти", self)
        self.find_recipe_btn.setToolTip("Спарсить новый рецепт")
        self.find_recipe_btn.clicked.connect(self.find_recipe_btn_clicked)
        self.find_recipe_btn.setFont(self.buts_font)
        self.find_recipe_btn.setStyleSheet(self.descr_styleSheet)

        self.remove_recipe_btn = QPushButton("Удалить", self)
        self.remove_recipe_btn.clicked.connect(self.remove_recipe_btn_clicked)
        self.remove_recipe_btn.setFont(self.buts_font)
        self.remove_recipe_btn.setStyleSheet(self.descr_styleSheet)

    def setup_layout(self):
        self.main_layout = QHBoxLayout()
        self.buttons_layout = QVBoxLayout()

        self.add_widgets_and_buts()
        self.setLayout(self.main_layout)

    def add_widgets_and_buts(self):
        self.main_layout.addWidget(self.recipes_list_widg)
        self.main_layout.addLayout(self.buttons_layout)

    def add_buts_to_buttons_layout(self):
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.open_recipe_btn)
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.edit_recipe_btn)
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.add_recipe_btn)
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.find_recipe_btn)
        self.buttons_layout.addStretch()
        self.buttons_layout.addWidget(self.remove_recipe_btn)
        self.buttons_layout.addStretch()

    def open_recipe_btn_clicked(self):
        items_list = self.recipes_list_widg.selectedItems()
        if len(items_list) != 0:
            for item in items_list:
                title = item.text()
                self.open_recp = OpenRecipe(self.user_id, title)
                self.open_recp.show()
        else:
            QMessageBox.warning(self, "Внимание", "Выберите рецепт из списка.")

    def edit_recipe_btn_clicked(self):
        items_list = self.recipes_list_widg.selectedItems()
        if len(items_list) != 0:
            for item in items_list:
                title = item.text()
                self.edit_recipe = EditRecipe(self.user_login, self.user_id, title)
                self.edit_recipe.save_changes_but.clicked.connect(self.change_rcp_clicked)
                self.edit_recipe.show()
        else:
            QMessageBox.warning(self, "Внимание", "Выберите рецепт из списка.")

    def change_rcp_clicked(self):
        title_rcp = self.edit_recipe.title_rcp_line.text()
        ingr_rcp = self.edit_recipe.ingr_rcp_line.toPlainText()
        descr_rcp = self.edit_recipe.decs_rcp_line.toPlainText()
        encoded_image = self.edit_recipe.encoded_string
        old_title = self.edit_recipe.old_title

        if title_rcp != "" and ingr_rcp != "" and descr_rcp != "":
            DataBaseActions.update_recipe_request(self.user_id, title_rcp, ingr_rcp, descr_rcp, encoded_image, old_title)
            self.edit_recipe.hide()
            current_titles = self.get_list_from_db()
            self.recipes_list_widg.clear()
            self.recipes_list_widg.addItems(current_titles)
            self.recipes_list_widg.sortItems()
        else:
            QMessageBox.information(self.edit_recipe, "Внимание", "Заполните необходимую информацию.")

    def add_recipe_btn_clicked(self):
        self.new_recp = AddNewRecipe(self.user_login, self.user_id)
        self.new_recp.add_new_recp_final_but.clicked.connect(self.add_new_recp_btn_clicked)
        self.new_recp.show()

    def add_new_recp_btn_clicked(self):
        title_rcp = self.new_recp.title_rcp_line.text()
        ingr_rcp = self.new_recp.ingr_rcp_line.toPlainText()
        decs_rcp = self.new_recp.decs_rcp_line.toPlainText()
        encoded_image = self.new_recp.encoded_string

        if title_rcp != "" and ingr_rcp != "" and decs_rcp != "":
            DataBaseActions.add_new_recipe_request(self.user_id, title_rcp, ingr_rcp, decs_rcp, encoded_image)
            self.recipes_list_widg.addItem(title_rcp)
            self.new_recp.hide()
        else:
            QMessageBox.information(self.new_recp, "Внимание", "Заполните необходимую информацию.")

    def find_recipe_btn_clicked(self):
        self.find_recp = ParsingNewRecipe(self.user_id)
        self.find_recp.show()

        self.find_recp.found_btn.clicked.connect(self.add_pars_recp_to_db)

    def add_pars_recp_to_db(self):
        user_id = self.user_id
        title = self.find_recp.recipe_title
        ingredients = self.find_recp.all_ingrdnts
        description = self.find_recp.recipe_desciption
        encr_image = self.find_recp.enc_img
        DataBaseActions.add_new_recipe_request(user_id, title, ingredients, description, encr_image)
        QMessageBox.information(self, "Внимание", "Рецепт, расположенный по указанному URL адресу, "
                                                            "добавлен в список вашего профиля.")
        self.recipes_list_widg.addItem(title)
        self.find_recp.found_btn.hide()
        self.find_recp.hide()

    def get_list_from_db(self):
        titles = DataBaseActions.request_recipes_list(self.user_id)
        return titles

    def remove_recipe_btn_clicked(self):
        items_list = self.recipes_list_widg.selectedItems()
        if len(items_list) != 0:
            res = QMessageBox.question(self, "Внимание", "Удалить выбранный рецепт из списка?")
            if res == 16384:
                for item in items_list:
                    self.recipes_list_widg.takeItem(self.recipes_list_widg.row(item))
                    title = item.text()
                    DataBaseActions.remove_recipe_request(self.user_id, title)
        else:
            QMessageBox.warning(self, "Внимание", "Выберите рецепт из списка.")

