import app_construction
from app_construction import *
from dataclasses import dataclass, field, InitVar
import os
from config import settings
import pickle


# TODO udelat slovnik ci funkci s chybovyma hlasenima ???
# TODO jako argument predat jen stringem chybu
class TaskManager:
    """Trida pro správu úkolů"""

    def __init__(self, parent):
        self.parent = parent
        self.tasks: list[Task] = []

    # methods
    def add_task(self, event=None):
        """add task function"""

        entry: str = self.parent.input_task.get()
        if entry:
            new_tasks = Task(entry)
            self.tasks.append(new_tasks)
            self.parent.input_task.delete(0, "end")
            self.parent.btn_activate(self.parent.btn_5, self.parent.btn_4)
        else:
            print("error")
            # TODO tady pouzit error funkci

    def edit_task(self):
        """Funkce pro editaci task labelu"""
        # TODO: new window dialog
        pass

    def remove_task(self):
        """Smaze vybrane tasky z seznamu a odstrani je z disple"""
        pass

    def load_list(self):
        """Načte úkoly z CSV souboru"""
        self.tasks.clear()
        # Todo: pridat load dialog s vyberem souboru
        file_path: str = os.path.join(
            os.path.dirname(__file__), "load_list", "list.csv"
        )
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:
                if len(row) >= 2:
                    task_name, description, status = row
                    self.tasks.append(Task(task_name, status, description))

    def save_list(self):
        """Uloží všechny úkoly do CSV souboru"""
        if self.parent.footer_entry.get() == "":
            list_name: str = "default_list"
        else:
            list_name = self.parent.footer_entry.get().replace(" ", "_")
        file_path = os.path.join(
            os.path.dirname(__file__), "load_list", f"{list_name}.pkl"
        )
        with open(file_path, "wb") as file:
            pickle.dump(self.tasks, file)

    def extend_list(self):
        """Funkce pro zvetseni pocet polozek v listu"""
        # TODO pridat load dialog s vyberem souboru
        file_path: str = os.path.join(
            os.path.dirname(__file__), "load_list", "list.csv"
        )
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
        print(self.tasks)

    # TODO very important !!!
    # TODO new display s nastavenim aplikace, width,height, font sizes, themes, etc.
    # TODO a pak ulozit do souboru settings, bud jako class nebo csc, json

    def exit(self):
        """Exit self.parent"""
        self.parent.destroy()


@dataclass
class Task:
    """Trida pro uchování jednoho úkolu"""

    task_name: str
    status: str = field(default="Not Started")
    user: str = field(default="Not Assigned")
    description: str = field(default="")


if __name__ == "__main__":
    print(f"App version: {settings.version}")
    app = App()
    app.mainloop()
