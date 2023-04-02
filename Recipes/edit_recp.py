from databaseactions import DataBaseActions
from add_new_recp import AddNewRecipe


class EditRecipe(AddNewRecipe):
    def __init__(self, login, user_id, title):
        super().__init__(login, user_id)

        self.setWindowTitle("Редактирование рецепта")

        self.old_title = title

        general_request_text = DataBaseActions.ingredients_and_description_request(user_id, title)

        self.title_rcp_line.setText(title)
        self.ingr_rcp_line.setPlainText(general_request_text[0])
        self.decs_rcp_line.setPlainText(general_request_text[1])

        self.save_changes_but = self.add_new_recp_final_but
        self.save_changes_but.setText("Сохранить изменения")
        self.save_changes_but.resize(200, 30)
        self.save_changes_but.move(305, 350)






