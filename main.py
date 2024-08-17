from dataclasses import dataclass, field
import csv
import os
from app_construction import *


class TaskManager:
    """Trida pro správu úkolů"""

    def __init__(self):
        self.tasks: list = []
        self.remove: list = []

    # methods
    @staticmethod
    def add_task():
        new: TaskFrame = TaskFrame(app.display_frame)

    def edit_task(self):
        """Funkce pro editaci task labelu"""
        pass

    def remove_task(self):
        """Smaze vybrane tasky z seznamu a odstrani je z disple"""
        pass

    def load_list(self):
        """Načte úkoly z CSV souboru"""
        self.tasks.clear()
        # Todo pridat load dialog s vyberem souboru
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
        # Todo pridat load dialog s vyberem souboru
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
        pass

    @staticmethod
    def exit():
        """Exit app"""
        app.destroy()

    def create_task_frame(self):
        pass


@dataclass
class Task:
    """Trida pro uchování jednoho úkolu"""

    task_name: str = field(default="")
    status: str = field(default="Not started")
    description: str = field(default="")


if __name__ == "__main__":
    print(f"App version: {version}")
    app: App = App(TaskManager())
    app.mainloop()
