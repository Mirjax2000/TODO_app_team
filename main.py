from dataclasses import dataclass, field
import csv
import os

import app_construction
from app_construction import *


class TaskManager:
    """Trida pro správu úkolů"""

    def __init__(self, parent):
        self.parent = parent
        self.tasks: list = []
        self.remove: list = []

    # methods

    def add_task(self):
        pass

    def edit_task(self):
        """Funkce pro editaci task labelu"""
        pass

    def remove_task(self):
        """Smaze vybrane tasky z seznamu a odstrani je z disple"""
        for task_frame in self.remove:
            task_description = task_frame.label_description.cget("text")
            task_to_remove = next(
                (task for task in self.tasks if task.description == task_description),
                None,
            )

            if task_to_remove:
                self.tasks.remove(task_to_remove)
            task_frame.destroy()

        self.remove.clear()
        for child in self.parent.display.display_frame.winfo_children():
            child.destroy()
        self.new_multi_labels(self.tasks)

    def load_list(self):
        """Načte úkoly z CSV souboru"""
        self.tasks.clear()
        file_path: str = os.path.join(
            os.path.dirname(__file__), "load_list", "import_tasks.csv"
        )
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:
                if len(row) >= 2:
                    description, status = row
                    self.tasks.append(Task(description, status, self.parent))
        self.new_multi_labels(self.tasks)

    def save_list(self):
        """Uloží všechny úkoly do CSV souboru"""
        if self.parent.footer.footer_entry.get() == "":
            list_name: str = "list"
        else:
            list_name = self.parent.footer.footer_entry.get().replace(" ", "_")
        file_path = os.path.join(
            os.path.dirname(__file__), "load_list", f"{list_name}.csv"
        )
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow(["description", "status"])
            for task in self.tasks:
                writer.writerow([task.description, task.status])

    def extend_list(self):
        """Funkce pro zvetseni pocet polozek v listu"""
        pass

    def clear_list(self):
        """Funkce na vymazani hlavniho listu a smazani textu v display"""
        self.tasks.clear()
        for child in self.parent.display.display_frame.winfo_children():
            child.destroy()

    def exit(self):
        """"""
        self.parent.destroy()

    def create_task_frame(self):
        pass


@dataclass
class Task:
    """Trida pro uchování jednoho úkolu"""

    task_name: str
    parent: TaskManager = field(default=None)
    status: str = field(default="Not started")
    description: str = field(default="")


if __name__ == "__main__":
    app: App = App()
    print(f"App version: {version}")
    app.mainloop()
