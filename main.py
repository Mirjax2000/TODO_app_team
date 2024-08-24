import app_construction
from app_construction import *
import os
from config import settings
from tkinter import filedialog
from pickle import dump, load


class TaskManager:
    """Trida pro správu úkolů"""

    def __init__(self, parent):
        self.parent = parent
        self.tasks: list[Task] = []

    # remove error
    def remove_error(self):
        """Vypne chybový label"""
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
        self.tasks.clear()  # Vynuluje seznam tasků
        self.remove_error()

        file_path: str = self.load_dialog()
        self.parent.footer_list_name.configure(
            text=f" {self.cleansing_file_path(file_path):.18}"
        )
        with open(file_path, "rb") as file:
            self.tasks = load(file)
            # TODO pohrat si s chybovyma hlasenima pres TRY/EXCEPT
            # _pickle.UnpicklingError: invalid load key, '\xef'.
            # EOFError: Ran out of input
            for task in self.tasks:
                self.create_frame(task.task_name, task.status, task.user)
                # stav widgetu on/off
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
            # _pickle.UnpicklingError: invalid load key, '\xef'.
            # EOFError: Ran out of input
            for task in extend_list:
                self.create_frame(task.task_name, task.status, task.user)
                # stav widgetu on/off
                self.parent.btn_state(self.parent, **settings.active_state)
        self.remove_error()

    def clear_list(self):
        """vymazani hlavniho listu a smazani frames v display"""
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
        """Remove error label"""
        self.parent.error_label.grid_remove()

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
