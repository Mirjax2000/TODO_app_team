import app_construction
from app_construction import *
from dataclasses import dataclass, field
import csv
import os
from config import settings


# TODO udelat slovnik ci funkci s chybovyma hlasenima ???
# TODO jako argument predat jen stringem chybu
class TaskManager:
    """Trida pro správu úkolů"""

    def __init__(self, parent):
        self.parent = parent
        self.tasks: list[dict] = []
        self.id: int = 0

    # methods
    def add_task(self, event=None):
        """add task function"""
        entry: str = self.parent.input_task.get()
        if entry:
            self.id += 1
            new_tasks = Task(self.parent.display_frame, entry)
            self.tasks.append({self.id: new_tasks})
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
            list_name: str = "list"
        else:
            list_name = self.parent.footer_entry.get().replace(" ", "_")
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

    parent: any
    task_name: str
    status: str = field(default="Not Started")
    user: str = field(default="Not Assigned")
    description: str = field(default="")

    def __post_init__(self):
        frame = TaskFrame(self.parent, self.task_name, self.status, self.user)


if __name__ == "__main__":
    print(f"App version: {settings.version}")
    app = App()
    app.mainloop()
