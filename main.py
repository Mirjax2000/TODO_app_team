import app_construction
from app_construction import *
import os
from config import settings
import pickle


class TaskManager:
    """Trida pro správu úkolů"""

    def __init__(self, parent):
        self.parent = parent
        self.tasks: list[Task] = []

    # remove error
    def remove_error(self):
        self.parent.error_label.grid_remove()

    # methods
    def add_task(self, event=None):
        """add task function"""

        entry: str = self.parent.input_task.get()
        if entry:
            new_tasks = Task(entry)
            self.tasks.append(new_tasks)
            # taskframe z posledniho itemu z listu self.tasks
            path = self.tasks[-1]
            self.create_frame(path.task_name, path.status, path.user)
            self.parent.input_task.delete(0, "end")

            # stav widgetu on/off
            self.parent.btn_state(self.parent, **settings.active_state)

        else:
            self.parent.error_msg("Error: Task name cannot be empty.")

    def edit_task(self):
        """Funkce pro editaci task labelu"""
        # TODO: new window dialog
        pass

    def remove_task(self):
        """Smaze vybrane tasky z seznamu a odstrani je z displeje"""
        pass

    def load_list(self):
        """Načte úkoly z pickle souboru"""
        self.tasks.clear()

        file_path: str = self.parent.load_dialog()
        with open(file_path, "rb") as file:
            self.tasks = pickle.load(file)
            for task in self.tasks:
                self.create_frame(task.task_name, task.status, task.user)
                # stav widgetu on/off
                self.parent.btn_state(self.parent, **settings.active_state)
        if not self.tasks:
            self.parent.error_msg("Error: No tasks found.")
        else:
            self.remove_error()

    def save_list(self):
        """Uloží všechny úkoly do CSV souboru"""
        if self.parent.footer_entry.get() == "":
            list_name: str = "default_list"
        else:
            list_name = self.parent.footer_entry.get().replace(" ", "_")
        file_path = os.path.join(os.path.dirname(__file__), "lists", f"{list_name}.pkl")
        with open(file_path, "wb") as file:
            pickle.dump(self.tasks, file)

    def extend_list(self):
        """Funkce pro zvetseni pocet polozek v listu"""
        # TODO pridat load dialog s vyberem souboru
        file_path: str = os.path.join(os.path.dirname(__file__), "lists", "list.csv")
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:
                if len(row) >= 2:
                    task_name, description, status = row
                    self.tasks.append(Task(task_name, status, description))

    def clear_list(self):
        """Funkce na vymazani hlavniho listu a smazani textu v display"""
        # TODO confirm dialog, are you sure?
        pass

    def user_group(self):
        """Groups and users"""
        # Todo new window for group and users
        pass

    def settings(self):
        """nastaveni aplikace"""
        for item in self.tasks:
            print(item.id)

    # TODO very important !!!
    # TODO new display s nastavenim aplikace, width,height, font sizes, themes, etc.
    # TODO a pak ulozit do souboru settings, bud jako class nebo csc, json

    def exit(self):
        """Exit self.parent"""
        self.parent.destroy()

    def clear_error(self, event):
        self.parent.error_label.grid_remove()

    def create_frame(self, *data):
        parent = self.parent.display_frame
        frame = app_construction.TaskFrame(parent, *data)


class Task:
    """Trida pro uchování jednoho úkolu"""

    _id_counter: int = 1

    def __init__(
        self,
        task_name: str,
        status: str = "Not Started",
        user: str = "Not Assigned",
        description: str = "",
    ):
        self.id = Task._id_counter
        Task._id_counter += 1
        self.task_name = task_name
        self.status = status
        self.user = user
        self.description = description


if __name__ == "__main__":
    app = App()
    app.mainloop()
