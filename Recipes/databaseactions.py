import sqlite3


class DataBaseActions:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.id = None

    def login_request(self):
        with sqlite3.connect("recipedatabase.db") as db:
            cursor = db.cursor()
            query = """SELECT password FROM users WHERE login = ?"""
            cursor.execute(query, (self.login,))
            received_password = cursor.fetchone()

        if received_password is None:
            return 1
        else:
            if received_password[0] == self.password:
                self.request_id()
                return 2
            else:
                return 3

    def create_acc_request(self):
        with sqlite3.connect("recipedatabase.db") as db:
            cursor = db.cursor()
            query = """INSERT INTO users (login, password) VALUES(?, ?)"""
            cursor.execute(query, (self.login, self.password))
            db.commit()

        self.request_id()

    def request_id(self):
        with sqlite3.connect("recipedatabase.db") as db:
            cursor = db.cursor()
            query = """SELECT id FROM users WHERE login = ?"""
            cursor.execute(query, (self.login,))
            received_id = cursor.fetchone()
            self.id = received_id[0]

    @staticmethod
    def request_recipes_list(user_id):
        with sqlite3.connect("recipedatabase.db") as db:
            cursor = db.cursor()
            query = """SELECT title FROM recipes WHERE user_id = ?"""
            cursor.execute(query, (user_id,))
            received_titles = cursor.fetchall()

        titles = list()
        for el1 in received_titles:
            for el2 in el1:
                titles.append(el2)
        return titles

    @staticmethod
    def add_new_recipe_request(user_id, title, ingredients, description, encr_image):
        with sqlite3.connect("recipedatabase.db") as db:
            cursor = db.cursor()
            query = """INSERT INTO recipes (user_id, title, ingredients, description, image) VALUES(?, ?, ?, ?, ?)"""
            cursor.execute(query, (user_id, title, ingredients, description, encr_image))
            db.commit()

    @staticmethod
    def remove_recipe_request(user_id, title):
        with sqlite3.connect("recipedatabase.db") as db:
            cursor = db.cursor()
            query = """DELETE FROM recipes WHERE user_id = ? and title = ?"""
            cursor.execute(query, (user_id, title))
            db.commit()

    @staticmethod
    def ingredients_and_description_request(user_id, title):
        with sqlite3.connect("recipedatabase.db") as db:
            cursor = db.cursor()
            query = """SELECT ingredients, description FROM recipes WHERE user_id = ? and title = ?"""
            cursor.execute(query, (user_id, title))
            received_result = cursor.fetchall()

        request_result = list()
        for el1 in received_result:
            for el2 in el1:
                request_result.append(el2)
        return request_result

    @staticmethod
    def get_recipe_image(user_id, title):
        with sqlite3.connect("recipedatabase.db") as db:
            cursor = db.cursor()
            query = """SELECT image FROM recipes WHERE user_id = ? and title = ?"""
            cursor.execute(query, (user_id, title))
            received_result = cursor.fetchone()

        return received_result[0]

    @staticmethod
    def update_recipe_request(user_id, title, ingr, descr, encoded_image, old_title):
        with sqlite3.connect("recipedatabase.db") as db:
            cursor = db.cursor()
            if encoded_image is None:
                query = """UPDATE recipes SET title = ?, ingredients = ?, description = ? WHERE user_id = ? and title = ?"""
                cursor.execute(query, (title, ingr, descr, user_id, old_title))
            else:
                query = """UPDATE recipes SET title = ?, ingredients = ?, description = ?, image = ? WHERE user_id = ? and title = ?"""
                cursor.execute(query, (title, ingr, descr, encoded_image, user_id, old_title))
            db.commit()

    @staticmethod
    def update_profile_info_request(user_id, login, password):
        with sqlite3.connect("recipedatabase.db") as db:
            cursor = db.cursor()
            if login != "" and password != "":
                query = """UPDATE users SET login = ?, password = ? WHERE id = ?"""
                cursor.execute(query, (login, password, user_id))
            if login == "" and password != "":
                query = """UPDATE users SET password = ? WHERE id = ?"""
                cursor.execute(query, (password, user_id))
            if login != "" and password == "":
                query = """UPDATE users SET login = ? WHERE id = ?"""
                cursor.execute(query, (login, user_id))
            db.commit()



