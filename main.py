import tkinter as tk
import customtkinter as ctk
import json
import os
import csv
from icecream import ic

ctk.set_default_color_theme("blue")

ctk.set_appearance_mode("Dark")


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
            self, placeholder_text="Enter a task", font=parent.font_normal
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
        self.columnconfigure(1, weight=0, uniform="b")

    @staticmethod
    def clear_text(event):
        event.widget.delete(0, ctk.END)


class Display(ctk.CTkFrame):

    def __init__(self, parent):
        self.parent = parent
        self.btns_text = [
            "Remove task",
            "Edit task",
            "Load list",
            "Extend list",
            "Save list",
            "Clear list",
            "Exit",
        ]

        super().__init__(parent)
        self.pack(side="top", fill="both", padx=20, expand=True)

        self.display_frame = ctk.CTkScrollableFrame(self)
        self.display_frame.grid(row=0, column=0, sticky="nsew")

        self.display_btns = ctk.CTkFrame(self, fg_color="#2b2b2b", width=140)
        self.display_btns.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        # grid pro framy pro vsechny tlacitka
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=0, uniform="b")
        self.rowconfigure(0, weight=1, uniform="c")

        # framy top, mid, bottom
        self.frame_config = {
            "master": self.display_btns,
            "width": 140,
        }
        self.display_btns_top = ctk.CTkFrame(**self.frame_config)
        self.display_btns_mid = ctk.CTkFrame(**self.frame_config)
        self.display_btns_btm = ctk.CTkFrame(**self.frame_config)
        #
        self.display_btns_top.grid(row=0, column=0, sticky="ns")
        self.display_btns_mid.grid(row=1, column=0, sticky="ns", pady=20)
        self.display_btns_btm.grid(row=2, column=0, sticky="s")
        #
        self.display_btns.rowconfigure(0, weight=1, uniform="a")
        self.display_btns.rowconfigure(1, weight=1, uniform="b")
        self.display_btns.rowconfigure(2, weight=1, uniform="c")
        #
        # Create buttons dynamically
        self.button_configs = [
            (self.display_btns_top, self.btns_text[0], self.remove_task, "btn_1"),
            (self.display_btns_top, self.btns_text[1], self.edit_task, "btn_2"),
            (self.display_btns_mid, self.btns_text[2], self.load_list, "btn_3"),
            (self.display_btns_mid, self.btns_text[3], self.save_list, "btn_4"),
            (self.display_btns_mid, self.btns_text[4], self.extend_list, "btn_5"),
            (self.display_btns_mid, self.btns_text[5], self.clear_list, "btn_6"),
            (self.display_btns_btm, self.btns_text[6], self.exit, "btn_7"),
        ]
        #
        for parent, text, command, attr_name in self.button_configs:
            button = ctk.CTkButton(
                parent, text=text, font=self.parent.font_normal, command=command
            )
            setattr(self, attr_name, button)
        #
        for i in range(len(self.button_configs)):
            button = getattr(self, f"btn_{i + 1}")
            button.grid(row=i, column=0, sticky="n", pady=1)

        self.display_btns_mid.rowconfigure(4, weight=1, uniform="a")
        #
        # methods

    def remove_task(self):
        self.parent.task.remove_task()

    def edit_task(self):
        pass

    def save_list(self):
        self.parent.task.save_tasks_to_csv()

    def load_list(self):
        self.parent.task.load_tasks_from_csv()

    def extend_list(self):
        pass

    def clear_list(self):
        self.parent.task.tasks.clear()
        for child in self.parent.display.display_frame.winfo_children():
            child.destroy()

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
        self.remove = []

    def save_tasks_to_csv(self):
        list_name = ""
        if self.parent.footer.footer_entry.get() == "":
            list_name = "list"
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

    def load_tasks_from_csv(self):
        self.tasks.clear()
        file_path = os.path.join(
            os.path.dirname(__file__), "load_list", "import_tasks.csv"
        )
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            for row in reader:
                if len(row) >= 2:
                    description, status = row
                    self.tasks.append(Task(description, status))
        self.new_multi_labels(self.tasks)

    def create_task_frame(self, item, index):
        description = getattr(item, "description", "Error")
        status = getattr(item, "status", "Error")

        DISPLAY_PATH = self.parent.display.display_frame  # cesta k display framu

        DISPLAY_PATH.label_frame = ctk.CTkFrame(DISPLAY_PATH)
        DISPLAY_FRAME = DISPLAY_PATH.label_frame
        DISPLAY_FRAME.pack_propagate(True)
        DISPLAY_FRAME.pack(side="top", fill="x", pady=(0, 7), ipady=5)

        # Label description
        DISPLAY_FRAME.label_description = ctk.CTkLabel(
            DISPLAY_FRAME,
            text=description,
            font=self.parent.font_normal,
        )
        DISPLAY_FRAME.label_description.grid(row=0, column=0, sticky="w", padx=5)

        # label status
        DISPLAY_FRAME.label_status = ctk.CTkLabel(
            DISPLAY_FRAME,
            text=status,
            font=self.parent.font_normal,
            width=140,
            anchor="w",
        )
        DISPLAY_FRAME.label_status.grid(
            row=0,
            column=1,
            sticky="w",
        )

        # checkbox
        DISPLAY_FRAME.var = ctk.StringVar(value="off")
        DISPLAY_FRAME.checkbox_status = ctk.CTkCheckBox(
            DISPLAY_FRAME,
            variable=DISPLAY_FRAME.var,
            onvalue="on",
            offvalue="off",
            font=self.parent.font_normal,
            text="",
            width=0,
            # command=self.check_status,
        )
        DISPLAY_FRAME.checkbox_status.grid(row=0, column=2, sticky="e", padx=10)
        DISPLAY_FRAME.columnconfigure(0, weight=1, uniform="a")
        DISPLAY_FRAME.columnconfigure(1, weight=0, uniform="b")
        DISPLAY_FRAME.columnconfigure(2, weight=0, uniform="c")
        DISPLAY_FRAME.rowconfigure(0, weight=1, uniform="a")

        if status == "Completed":
            DISPLAY_FRAME.label_status.configure(text_color="#00ff00")
            DISPLAY_FRAME.var.set("on")

        else:
            DISPLAY_FRAME.label_status.configure(text_color="#ff7f00")
            DISPLAY_FRAME.var.set("off")

        bind_1 = ("<Button-1>", lambda event: self.on_label_click(event, index))
        DISPLAY_FRAME.bind(*bind_1)
        DISPLAY_FRAME.label_description.bind(*bind_1)
        DISPLAY_FRAME.label_status.bind(*bind_1)

    def add_task(self, event=None, status="Not Completed"):
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
            self.parent.header.input_task.delete(0, ctk.END)
            self.create_task_frame(item, len(self.tasks) - 1)

    def new_multi_labels(self, seznam):
        for index, item in enumerate(seznam):
            self.create_task_frame(item, index)

    def on_label_click(self, event, index):
        parent = event.widget.master
        while not isinstance(parent, ctk.CTkFrame):
            parent = parent.master
            children = parent.winfo_children()
        background = parent.cget("fg_color")

        if background == "#277bc6":
            parent.configure(fg_color="#2b2b2b")
            self.remove.remove(parent)
        else:
            parent.configure(fg_color="#277bc6")
            self.remove.append(parent)
        print(f"Index: {index}, Description: {self.tasks[index].description}")

    def remove_task(self):
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


class Task:
    def __init__(self, description, status):
        self.description = description
        self.status = status


if __name__ == "__main__":
    app = App()
    app.mainloop()
