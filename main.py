from dataclasses import dataclass, field
import csv
import os
from app_construction import *
from config import mixins
from config import settings as set


# TODO udelat slovnik ci funkci s chybovyma hlasenima ???
# TODO jako argument predat jen stringem chybu
class TaskManager:
    """Trida pro správu úkolů"""

    def __init__(self):
        self.tasks: dict = {}
        self.id: int = 0

    # methods
    def add_task(self, event=None):

        if app.input_task.get():
            new_task = Task()
            new_frame = TaskFrame(app.display_frame, app.input_task.get())
            self.id += 1
            self.tasks[self.id] = new_frame
            app.input_task.delete(0, "end")

        else:
            app.error_label.grid(row=0, column=2, sticky="", ipadx=10)
            app.error_label.configure(text="Task name cannot be empty!")

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
        if app.footer_entry.get() == "":
            list_name: str = "list"
        else:
            list_name = app.footer_entry.get().replace(" ", "_")
        file_path = os.path.join(
            os.path.dirname(__file__), "load_list", f"{list_name}.csv"
        )
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["task_name", "status", "description"])
            for task in self.tasks:
                writer.writerow([task.task_name, task.status, task.description])

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
        pass

    # TODO very important !!!
    # TODO new display s nastavenim aplikace, width,height, font sizes, themes, etc.
    # TODO a pak ulozit do souboru settings, bud jako class nebo csc, json

    @staticmethod
    def exit():
        """Exit app"""
        app.destroy()

    @staticmethod
    def clear_error(event):
        """Clears input entry"""
        app.error_label.grid_remove()
        # app.input_task.configure(placeholder_text="")


@dataclass
class Task:
    """Trida pro uchování jednoho úkolu"""

    task_name: str = field(default="")
    status: str = field(default="Not started")
    frame: TaskFrame = TaskFrame(parent=app.display_frame, text=task_name)


if __name__ == "__main__":
    print(f"App version: {set.version}")
    app: App = App(TaskManager())

    app.mainloop()
