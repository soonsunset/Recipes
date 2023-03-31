import base64
from io import BytesIO
from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QImage, QPalette, QBrush, QFont
from PyQt5.QtCore import QSize
import re
import requests
from bs4 import BeautifulSoup


class ParsingNewRecipe(QDialog):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

        self.window_height = 550
        self.window_width = 400
        self.resize(self.window_height, self.window_width)
        self.setFixedSize(self.size())

        self.setWindowTitle("Поиск рецепта")
        self.setWindowIcon(QIcon('./assets/search_icon.png'))

        self.add_rec_image = QImage("./assets/add_new_rec_page.PNG")
        self.add_rec_image = self.add_rec_image.scaled(QSize(self.window_height, self.window_width))
        self.palette = QPalette()
        self.palette.setBrush(QPalette.Window, QBrush(self.add_rec_image))
        self.setPalette(self.palette)

        self.labels_font = QFont("Arial", 12)
        self.labels_font.setBold(True)

        self.note_lbl = QLabel("Загрузите в приложение любой рецепт с сайта Eda.ru,\nвставив в поле URL страницы рецепта.", self)
        self.note_lbl.move(30, 50)
        self.note_lbl.setFont(self.labels_font)
        self.note_lbl.setStyleSheet("color: rgb(56, 21, 99)")

        self.url_field = QLineEdit(self)
        self.url_field.setPlaceholderText("Например: https://eda.ru/recepty/supy/sup-harcho-33916")
        self.url_field.move(30, 120)
        self.url_field.resize(380, 25)

        self.descr_styleSheet = """
                                            QPushButton {
                                                background-color: rgb(65, 142, 242);
                                            }

                                            QPushButton {
                                                color: white;
                                            }

                                            QPushButton:hover {
                                                background-color: rgb(125, 177, 245);
                                            }
                                        """

        self.buts_font = QFont("Garamond", 12)
        self.buts_font.setBold(True)

        self.find_btn = QPushButton("Найти", self)
        self.find_btn.setStyleSheet(self.descr_styleSheet)
        self.find_btn.setFont(self.buts_font)
        self.find_btn.clicked.connect(self.find_btn_clicked)
        self.find_btn.move(420, 118)
        self.find_btn.resize(100, 30)

        self.ad_descr_styleSheet = """
                                                    QPushButton {
                                                        background-color: rgba(0, 0, 0, 0);
                                                    }

                                                    QPushButton {
                                                        color: rgb(56, 21, 99);
                                                    }

                                                    QPushButton:hover {
                                                        background-color: rgb(125, 177, 245);
                                                    }
                                                """
        self.found_btn = QPushButton("Рецепт найден. Загрузить его?", self)
        self.found_btn.setStyleSheet(self.ad_descr_styleSheet)
        self.found_btn.setFont(self.buts_font)
        self.found_btn.move(75, 170)
        self.found_btn.resize(300, 30)
        self.found_btn.hide()

    def find_btn_clicked(self):
        url_regex = r"^https://eda\.ru/recepty/..*$"
        url = self.url_field.text()

        if re.match(url_regex, url):
            self.find_info_from_website(url)
        else:
            QMessageBox.warning(self, "Внимание", "Введите URL адрес в соответствии со следующим шаблоном:\n"
                                                  "https://eda.ru/recepty/...")
            self.url_field.clear()

    def find_info_from_website(self, url):
        req = requests.get(url)
        html = BeautifulSoup(req.content, "lxml")

        recipe_name = html.find("h1")

        recipe_name_text = recipe_name.text

        all_ingr = html.find_all("span", class_="emotion-mdupit")
        all_ingr_text = [i.text for i in all_ingr]

        all_ingr_amount = html.find_all("span", class_="emotion-bsdd3p")
        all_ingr_amount_text = [i.text for i in all_ingr_amount]

        final_all_ingr_amount = [f"{all_ingr_text[i]} ({all_ingr_amount_text[i]})," for i in range(len(all_ingr))]
        final_all_ingr_amount_join = '\n'.join(final_all_ingr_amount)

        all_texts = html.find_all("span", class_="emotion-wdt5in")
        all_texts_text = [i.text for i in all_texts]
        final_all_texts = [f"{i + 1}. {all_texts_text[i]}" for i in range(len(all_texts_text))]
        final_all_texts_join = '\n'.join(final_all_texts)

        pars_image_obj = ParsingImage(url)

        encoded_image = pars_image_obj.encoded_string

        self.found_btn.show()
        self.recipe_title = recipe_name_text
        self.all_ingrdnts = final_all_ingr_amount_join
        self.recipe_desciption = final_all_texts_join
        self.enc_img = encoded_image


class ParsingImage:
    def __init__(self, url):
        pattern1 = r'<img loading="lazy" decoding="async" src="https://eda\.ru/img/eda/.*?\.jpg" width=".*?" .*?height="'
        pattern2 = r'width="[4-9]\d{2}px"'
        pattern3 = "https://eda\.ru/img/eda/.*\.jpg"

        req = requests.get(url)
        req_content = req.content
        str_content = req_content.decode('utf-8')

        first_matches = re.findall(pattern1, str_content)

        final_list = []
        for i in range(len(first_matches)):
            second_matches = re.search(pattern2, first_matches[i])
            if second_matches:
                final_list.append(first_matches[i])

        first_number = list()
        for el in final_list:
            first_number.append(el[-15])

        first_number.sort()

        final_el = ''
        for el in final_list:
            if el[-15] == first_number[-1]:
                final_el = el

        final_url_for_image = re.findall(pattern3, final_el)
        self.final_url_for_image = final_url_for_image[0]

        self.get_binary_image(self.final_url_for_image)

    def get_binary_image(self, url):
        url_for_image = url

        response = requests.get(url_for_image)
        if response.status_code == 200:
            image_data = BytesIO(response.content)

            self.encoded_string = base64.b64encode(image_data.read())

