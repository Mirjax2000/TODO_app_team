import app_construction
from app_construction import *
import os
from config import settings
from tkinter import filedialog
from pickle import dump, load
from dataclasses import dataclass, field


class TaskManager:
    """Trida pro správu úkolů"""

    counter: int = 0

    def __init__(self, parent):
        self.parent = parent
        self.tasks: list[Task] = []



    # methods
    def add_task(self, event=None):
        """add task function"""

        entry: str = self.parent.input_task.get()
        if entry:
            self.counter += 1
            new_tasks = Task(idecko=self.counter, task_name=entry)
            self.tasks.append(new_tasks)
            # taskframe z posledniho itemu z listu self.tasks
            task = self.tasks[-1]
            user: str = task.user
            status: str = task.status
            idecko: int = task.idecko
            task_name: str = task.task_name
            description: str = task.description
            rozbal: tuple = (idecko, task_name, status, user, description)

            self.create_frame(*rozbal)
            # vymaz vstupní pole
            self.parent.input_task.delete(0, "end")

            # state widgetu na active state
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
        self.tasks.clear()  # Vynuluje seznam tasků
        self.remove_error()

        file_path: str = self.load_dialog()
        self.parent.footer_list_name.configure(
            text=f" {self.cleansing_file_path(file_path):.18}"
        )
        with open(file_path, "rb") as file:
            temp_task = load(file)
            # TODO pohrat si s chybovyma hlasenima pres TRY/EXCEPT
            # _pickle.UnpicklingError: invalid load key, '\xef'.
            # FileNotFoundError: [Errno 2] No such file or directory: ''
            # EOFError: Ran out of input
            for task in temp_task:
                self.counter += 1
                user: str = task.user
                status: str = task.status
                idecko: int = self.counter
                task_name: str = task.task_name
                description: str = task.description
                rozbal: tuple = (idecko, task_name, status, user, description)
                self.tasks.append(Task(*rozbal))
                self.create_frame(*rozbal)
                # state widgetu na active state
                self.parent.btn_state(self.parent, **settings.active_state)

    def save_list(self):
        """Uloží všechny úkoly do pickle souboru"""
        self.parent.footer_list_name.configure(
            text=f" {self.cleansing_file_path(self.save_dialog(self.tasks))}"
        )

    def extend_list(self):
        """Funkce pro zvetseni pocet polozek v listu"""
        file_path: str = self.load_dialog()
        with open(file_path, "rb") as file:
            extend_list: list[Task] = load(file)
            self.tasks.extend(extend_list)
            # TODO pohrat si s chybovyma hlasenima pres TRY/EXCEPT
            # FileNotFoundError: [Errno 2] No such file or directory: ''
            # _pickle.UnpicklingError: invalid load key, '\xef'.
            # EOFError: Ran out of input
            for task in extend_list:
                self.create_frame(task.task_name, task.status, task.user)
                # state widgetu na active state
                self.parent.btn_state(self.parent, **settings.active_state)
        self.remove_error()

    def clear_list(self):
        """vymazani hlavniho listu a smazani frames v display"""
        # state widgetu na default state
        self.parent.btn_state(self.parent, **settings.default_state)
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

    def create_frame(self, *data):
        """Create a new frame for task"""
        parent = self.parent.display_frame
        frame = app_construction.TaskFrame(parent, *data)

    @staticmethod
    def load_dialog():
        file_name = filedialog.askopenfilename(
            initialdir="./lists",
            title="Select a file",
            filetypes=[("list files", "*.pkl")],
        )
        return file_name

    @staticmethod
    def save_dialog(data):
        file_name = filedialog.asksaveasfilename(
            defaultextension=".pkl",
            filetypes=[("pkl files", "*.pkl")],
        )
        if file_name:
            with open(file_name, "wb") as file:
                dump(data, file)
        return file_name

    @staticmethod
    def cleansing_file_path(path: str) -> str:
        return path.split("/")[-1]

    # remove error
    def remove_error(self, event=None):
        """Vypne chybový label"""
        self.parent.error_label.grid_remove()


@dataclass
class Task:
    """Trida pro uchování jednoho úkolu"""

    idecko: int
    task_name: str
    status: str = field(default="Not Started")
    user: str = field(default="Not Assigned")
    description: str = ""


if __name__ == "__main__":
    app = App()
    app.mainloop()
