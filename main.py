import tkinter as tk
import customtkinter as ctk
import json
import os
import csv
from icecream import ic


class App(ctk.CTk):  # Main app
    # constants
    font_big = ("Arial", 30, "normal")
    font_normal = ("Arial", 20, "normal")
    font_small = ("Arial", 16, "normal")

    # constructor
    def __init__(self):
        super().__init__()
        self.title("TODO-List")
        self.iconbitmap("./assets/ico.ico")
        self.center_window()
        self.resizable(False, False)
        self.configure(fg_color="#2b2b2b")

        # Frames
        self.task = TaskManager(self)
        self.header = Header(self)
        self.display = Display(self)
        self.footer = Footer(self)

    def center_window(self):
        self.update_idletasks()
        width = 800
        height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = screen_width // 2 - width // 2
        y = screen_height // 2 - height // 2
        self.geometry(f"{width}x{height}+{x}+{y}")


class Header(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.pack(side="top", fill="x", padx=20, pady=20)

        # widgets input, button
        self.input_task = ctk.CTkEntry(
            self, placeholder_text="Enter task", font=parent.font_normal
        )
        self.input_task.get()
        self.input_task.focus()
        self.input_task.bind("<FocusIn>", self.clear_text)
        self.input_task.bind("<Return>", self.parent.task.add_task)
        self.input_task.grid(row=0, column=0, padx=(0, 40), sticky="ew")

        self.input_btn = ctk.CTkButton(
            self,
            text="Add Task",
            font=parent.font_normal,
            command=self.parent.task.add_task,
        )
        self.input_btn.grid(row=0, column=1, sticky="e")

        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=0, uniform="a")

    @staticmethod
    def clear_text(event):
        event.widget.delete(0, ctk.END)


class Display(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        self.btns_text = ["Remove task", "Edit task", "Save list", "Load list", "Exit"]
        super().__init__(parent)
        self.pack(side="top", fill="both", padx=20, expand=True)

        self.display_frame = ctk.CTkScrollableFrame(self)
        self.display_frame.grid(
            row=0,
            rowspan=len(self.btns_text),
            column=0,
            sticky="nsew",
        )

        for item in self.btns_text:
            self.btn = ctk.CTkButton(
                self,
                font=parent.font_normal,
                text=item,
                command=getattr(self, item.lower().replace(" ", "_")),
            )
            row_config = self.btns_text.index(item)
            self.btn.grid(row=row_config, column=1, sticky="e")

        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=0, uniform="a")
        row_config = tuple(range(len(self.btns_text)))
        self.rowconfigure(row_config, weight=1, uniform="a")

        self.test_label = ctk.CTkLabel(
            self.display_frame,
            anchor="w",
            text="",
            fg_color="#3e3e3e",
        )
        self.test_label.pack(
            expand=True,
            fill="x",
        )

    def remove_task(self):
        pass

    def edit_task(self):
        pass

    def save_list(self):
        pass

    def load_list(self):
        pass

    @staticmethod
    def exit():
        app.destroy()


class Footer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(side="bottom", fill="x", pady=20, padx=20)

        self.footer_label = ctk.CTkLabel(
            self,
            font=parent.font_normal,
            text="List name: ",
        )
        self.footer_label.grid(row=0, column=0, sticky="e")

        self.footer_label_name = ctk.CTkLabel(
            self, font=parent.font_normal, text="my-name"
        )
        self.footer_label_name.grid(row=0, column=1, sticky="w")

        self.columnconfigure(0, weight=0, uniform="a")
        self.columnconfigure(1, weight=1, uniform="a")


class TaskManager:
    def __init__(self, parent):
        self.parent = parent
        self.tasks = []

    def load_tasks_from_json(self):
        self.tasks.clear()
        file_path = os.path.join(os.path.dirname(__file__), "import_tasks.json")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.tasks = [Task(item["description"], item["status"]) for item in data]

    def add_task(self, status=False, event=None):
        user_input = self.parent.header.input_task.get()
        new_task = Task(user_input, status)
        self.tasks.append(new_task)
        self.vypis()

    def vypis(self):
        for item in self.tasks:
            ic(item)
            description = getattr(item, "description", "nemame")
            status = getattr(item, "status", "nemame")
            self.parent.display.test_label.configure(text=f"{description}: {status}")

    def get_task_list(self):
        return [(task.description, task.status) for task in self.tasks]


class Task:
    def __init__(self, description, status):
        self.description = description
        self.status = status


if __name__ == "__main__":
    app = App()
    app.mainloop()
