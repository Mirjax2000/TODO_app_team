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
        width = 1000
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
        self.input_task.grid(row=0, column=0, padx=(0, 20), sticky="ew")

        self.input_btn = ctk.CTkButton(
            self,
            text="Add Task",
            font=parent.font_normal,
            command=self.parent.task.add_task,
        )
        self.input_btn.grid(row=0, column=1, sticky="e")
        # formatovani gridu pro header
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
            row=0, rowspan=len(self.btns_text), column=0, sticky="nsew", padx=(0, 40)
        )
        # zacatek vypisu labelu
        # formatovani gridu pro display_frame label
        self.display_frame.columnconfigure(0, weight=1, uniform="a")
        self.display_frame.columnconfigure(1, weight=0, uniform="b")
        self.display_frame.columnconfigure(2, weight=0, uniform="b")
        self.display_frame.rowconfigure(0, weight=1, uniform="a")

        # side buttons
        for item in self.btns_text:
            self.btn = ctk.CTkButton(
                self,
                font=parent.font_normal,
                text=item,
                command=getattr(self, item.lower().replace(" ", "_")),
            )
            row_config = self.btns_text.index(item)
            self.btn.grid(row=row_config, column=1, sticky="e")

        # formatovani gridu pro vsechny tlacitka
        self.columnconfigure(0, weight=1, uniform="b")
        self.columnconfigure(1, weight=0, uniform="a")
        row_config = tuple(range(len(self.btns_text)))
        self.rowconfigure(row_config, weight=1, uniform="a")

    def remove_task(self):
        pass

    def edit_task(self):
        pass

    def save_list(self):
        pass

    def load_list(self):
        self.parent.task.load_tasks_from_json()

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

        self.footer_label.grid(row=0, column=0, sticky="w")

        self.footer_entry = ctk.CTkEntry(
            self,
            font=parent.font_normal,
            placeholder_text="jmeno listu",
        )
        self.footer_entry.get()
        self.footer_entry.grid(row=0, column=1, sticky="w")

        # formatovani gridu pro footer
        self.columnconfigure(0, weight=0, uniform="a")
        self.columnconfigure(1, weight=0, uniform="b")


class TaskManager:
    def __init__(self, parent):
        self.parent = parent
        self.tasks = []
        self.row_count = 0

    def load_tasks_from_json(self):
        self.tasks.clear()
        file_path = os.path.join(os.path.dirname(__file__), "import_tasks.json")
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
            self.tasks = [Task(item["description"], item["status"]) for item in data]
        self.new_multi_labels()

    def add_task(self, event=None, status="nesplneno"):

        user_input = self.parent.header.input_task.get()
        if not user_input:
            self.parent.header.input_task.configure(
                placeholder_text="Please enter a task",
                placeholder_text_color="#ff7f00",
            )
        else:

            new_task = Task(user_input, status)
            self.tasks.append(new_task)
            item = self.tasks[-1] if self.tasks else None
            description = getattr(item, "description", "Error")
            status = getattr(item, "status", "Error")

            DISPLAY_PATH = self.parent.display.display_frame
            DISPLAY_PATH.label_description = ctk.CTkLabel(
                DISPLAY_PATH,
                text=description,
                font=self.parent.font_normal,
            )
            DISPLAY_PATH.label_description.grid(
                row=self.row_count, column=0, sticky="w"
            )

            DISPLAY_PATH.label_status = ctk.CTkLabel(
                DISPLAY_PATH,
                text=status,
                font=self.parent.font_normal,
                text_color="#ff7f00",
            )
            DISPLAY_PATH.label_status.grid(row=self.row_count, column=1, sticky="ew")

            DISPLAY_PATH.var = ctk.IntVar()
            DISPLAY_PATH.checkbox_status = ctk.CTkCheckBox(
                DISPLAY_PATH,
                variable=DISPLAY_PATH.var,
                onvalue=1,
                offvalue=0,
                font=self.parent.font_normal,
                text="",
                width=0,
            )
            DISPLAY_PATH.checkbox_status.grid(
                row=self.row_count, column=2, sticky="e", padx=10
            )
            self.row_count += 1

    def new_multi_labels(self):

        for item in self.tasks:
            self.row_count += 1
            ic(self.row_count)

            description = getattr(item, "description", "Error")
            status = getattr(item, "status", "Error")

            DISPLAY_PATH = self.parent.display.display_frame
            DISPLAY_PATH.label_description = ctk.CTkLabel(
                DISPLAY_PATH,
                text=description,
                font=self.parent.font_normal,
            )
            DISPLAY_PATH.label_description.grid(
                row=self.row_count, column=0, sticky="w"
            )

            DISPLAY_PATH.label_status = ctk.CTkLabel(
                DISPLAY_PATH,
                text=status,
                font=self.parent.font_normal,
                text_color="#ff7f00",
            )
            DISPLAY_PATH.label_status.grid(row=self.row_count, column=1, sticky="ew")

            DISPLAY_PATH.var = ctk.IntVar()
            DISPLAY_PATH.checkbox_status = ctk.CTkCheckBox(
                DISPLAY_PATH,
                variable=DISPLAY_PATH.var,
                onvalue=1,
                offvalue=0,
                font=self.parent.font_normal,
                text="",
                width=0,
            )
            DISPLAY_PATH.checkbox_status.grid(
                row=self.row_count, column=2, sticky="e", padx=10
            )


class Task:
    def __init__(self, description, status):
        self.description = description
        self.status = status



if __name__ == "__main__":
    app = App()
    app.mainloop()

