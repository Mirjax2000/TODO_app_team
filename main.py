import csv
import os
from assets.app_construction import *


class TaskManager:
    """Trida pro správu úkolů"""

    def __init__(self, parent):
        self.parent = parent
        self.tasks: list = []
        self.remove: list = []

    # methods

    def add_task(self, event=None, status: str = "Not Completed"):
        """Prida novy ukol do seznamu a vypise na display"""

        user_input = self.parent.header.input_task.get().strip()
        self.parent.header.input_task.delete(0, ctk.END)
        if not user_input:
            self.parent.footer.message_label.configure(text="Please enter a task.")
        else:
            new_task = Task(user_input, status, self.parent)
            self.tasks.append(new_task)
            item = self.tasks[-1] if self.tasks else None
            self.create_task_frame(item, len(self.tasks) - 1)
            self.parent.footer.message_label.configure(text="")

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
        """Ukonceni appky"""
        self.parent.destroy()

    def create_task_frame(self, item, index):
        """Vytvoří label pro úkol"""
        description = getattr(item, "description", "Error")
        status = getattr(item, "status", "Error")

        display_path = self.parent.display.display_frame  # cesta k display framu

        display_path.label_frame = ctk.CTkFrame(display_path)
        display_frame = display_path.label_frame
        display_frame.pack(side="top", fill="x", pady=(0, 7), ipady=5)

        # Label description
        display_frame.label_description = ctk.CTkLabel(
            display_frame,
            text=description,
            font=font_normal,
        )
        display_frame.label_description.grid(row=0, column=0, sticky="w", padx=5)

        # label status
        display_frame.label_status = ctk.CTkLabel(
            display_frame,
            text=status,
            font=font_normal,
            width=140,
            anchor="w",
        )
        display_frame.label_status.grid(
            row=0,
            column=1,
            sticky="w",
        )

        # checkbox
        display_frame.var = ctk.StringVar(value="off")
        display_frame.checkbox_status = ctk.CTkCheckBox(
            display_frame,
            variable=display_frame.var,
            onvalue="on",
            offvalue="off",
            font=font_normal,
            text="",
            width=0,
            # command=self.check_status,
        )
        display_frame.checkbox_status.grid(row=0, column=2, sticky="e", padx=10)
        display_frame.columnconfigure(0, weight=1, uniform="a")
        display_frame.columnconfigure(1, weight=0, uniform="b")
        display_frame.columnconfigure(2, weight=0, uniform="c")
        display_frame.rowconfigure(0, weight=1, uniform="a")

        if status == "Completed":
            display_frame.label_status.configure(text_color="#00ff00")
            display_frame.var.set("on")

        else:
            display_frame.label_status.configure(text_color="#ff7f00")
            display_frame.var.set("off")

        bind_1: tuple = ("<Button-1>", lambda event: self.on_label_click(event, index))
        display_frame.bind(*bind_1)
        display_frame.label_description.bind(*bind_1)
        display_frame.label_status.bind(*bind_1)

    def add_task(self, event=None, status: str = "Not Completed"):
        """Prida novy ukol do seznamu a vypise na display"""

        user_input = self.parent.header.input_task.get().strip()
        self.parent.header.input_task.delete(0, ctk.END)
        if not user_input:
            self.parent.footer.message_label.configure(text="Please enter a task.")
        else:
            new_task = Task(user_input, status, self.parent)
            self.tasks.append(new_task)
            item = self.tasks[-1] if self.tasks else None
            self.create_task_frame(item, len(self.tasks) - 1)
            self.parent.footer.message_label.configure(text="")

    def new_multi_labels(self, seznam):
        """predává všechny položky na disply a do hlavniho seznamu"""
        for index, item in enumerate(seznam):
            self.create_task_frame(item, index)

    def on_label_click(self, event, index):
        """Kliknuti na task label a zmeni jeho barvu"""
        parent = event.widget.master
        while not isinstance(parent, ctk.CTkFrame):
            parent = parent.master
        background = parent.cget("fg_color")

        if background == "#277bc6":
            parent.configure(fg_color="#2b2b2b")
            self.remove.remove(parent)
        else:
            parent.configure(fg_color="#277bc6")
            self.remove.append(parent)
        print(f"Index: {index}, Description: {self.tasks[index].description}")


class Task:
    """Trida pro uchování jednoho úkolu"""

    def __init__(self, description: str, status: str, parent):
        """Inicializuje ukol"""
        self.parent = parent
        self.description = description
        self.status = status

    def __str__(self) -> str:
        return f"Description: {self.description}, Status: {self.status}"

    def print_task(self):
        """Vypise ukol primo z classy Task"""
        for task in self.parent.task.tasks:
            print(f"__str__: {str(task)}")


if __name__ == "__main__":
    app: App = App()
    print(f"App version: {version}")
    app.mainloop()
