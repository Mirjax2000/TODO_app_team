import tkinter as tk
import customtkinter as ctk
import os
import csv

ctk.set_default_color_theme("dark-blue")
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

        # Vstupní pole pro zadání úkolu
        self.input_task = ctk.CTkEntry(
            self, placeholder_text="Enter a task", font=parent.font_normal
        )
        self.input_task.focus()
        self.input_task.bind(
            "<FocusIn>", self.clear_placeholder
        )  # Kliknutím na pole se aktivuje
        self.input_task.bind("<Return>", self.parent.task.add_task)
        self.input_task.grid(row=0, column=0, padx=(0, 20), sticky="ew")

        # Tlačítko pro přidání úkolu
        self.input_btn = ctk.CTkButton(
            self,
            text="Add Task",
            font=parent.font_normal,
            command=self.parent.task.add_task,
        )
        self.input_btn.grid(row=0, column=1, sticky="e")

        # Grid konfigurace
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=0, uniform="b")

    def clear_placeholder(self, event):
        """Vymaže textové pole a obnoví výchozí barvu textu a placeholderu při kliknutí."""
        if self.input_task.get() == "Please enter a task":
            self.input_task.delete(0, ctk.END)  # Vymaže textové pole
            self.input_task.configure(
                placeholder_text="Enter a task",
                placeholder_text_color="#888888",  # Standardní šedá barva pro placeholder
                text_color="#000000",  # Standardní barva textu černá
            )


class Display(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        self.btns_text = [
            "Remove task",
            "Edit task",
            "Load list",
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
        self.display_btns_top = ctk.CTkFrame(
            self.display_btns, fg_color="#333333", height=100, width=140
        )
        self.display_btns_mid = ctk.CTkFrame(
            self.display_btns, fg_color="#333333", height=100, width=140
        )
        self.display_btns_btm = ctk.CTkFrame(
            self.display_btns, fg_color="#333333", height=100, width=140
        )
        self.display_btns_top.grid(row=0, column=0, sticky="ns")
        self.display_btns_mid.grid(row=1, column=0, sticky="ns", pady=20)
        self.display_btns_btm.grid(row=2, column=0, sticky="s")
        #
        self.display_btns.columnconfigure(0, weight=0, uniform="a")
        self.display_btns.rowconfigure(0, weight=1, uniform="a")
        self.display_btns.rowconfigure(1, weight=1, uniform="b")
        self.display_btns.rowconfigure(2, weight=1, uniform="c")
        #  region
        self.btn_1 = ctk.CTkButton(
            self.display_btns_top,
            text=self.btns_text[0],
            font=parent.font_normal,
            command=self.remove_task,
        )
        self.btn_2 = ctk.CTkButton(
            self.display_btns_top,
            text=self.btns_text[1],
            font=parent.font_normal,
            command=self.edit_task,
        )
        self.btn_3 = ctk.CTkButton(
            self.display_btns_mid,
            text=self.btns_text[2],
            font=parent.font_normal,
            command=self.load_list,
        )
        self.btn_4 = ctk.CTkButton(
            self.display_btns_mid,
            text=self.btns_text[3],
            font=parent.font_normal,
            command=self.save_list,
        )
        self.btn_5 = ctk.CTkButton(
            self.display_btns_mid,
            text=self.btns_text[4],
            font=parent.font_normal,
            command=self.clear_list,
        )
        self.btn_6 = ctk.CTkButton(
            self.display_btns_btm,
            text=self.btns_text[5],
            font=parent.font_normal,
            command=self.exit,
        )
        # endregion
        self.btn_1.grid(row=0, column=0, sticky="new", pady=(0, 10))
        self.btn_2.grid(row=1, column=0, sticky="new")
        self.btn_3.grid(row=2, column=0, sticky="new")
        self.btn_4.grid(row=3, column=0, sticky="new", pady=10)
        self.btn_5.grid(row=4, column=0, sticky="new")
        self.btn_6.grid(row=5, column=0, sticky="sew")

    def remove_task(self):
        self.parent.task.remove_task()

    def edit_task(self):
        pass

    def save_list(self):
        self.parent.task.save_tasks_to_csv()

    def load_list(self):
        self.parent.task.load_tasks_from_csv()

    def clear_list(self):
        self.parent.task.tasks.clear()
        for child in self.parent.display.display_frame.winfo_children():
            child.destroy()

    def exit(self):
        self.parent.destroy()


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
        self.message_label = ctk.CTkLabel(
            self,
            font=parent.font_small,
            text_color="#ff7f00",
            text="",
        )
        self.message_label.grid(row=0, column=2, sticky="w")
        self.columnconfigure(0, weight=0, uniform="a")
        self.columnconfigure(1, weight=0, uniform="b")
        self.columnconfigure(2, weight=1, uniform="c")


class TaskManager:
    def __init__(self, parent):
        self.parent = parent
        self.tasks = []
        self.remove = []  # Inicializujeme self.remove

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

    def toggle_task_status(self, task_frame, index):
        task = self.tasks[index]
        if task.status == "Completed":
            task.status = "Not Completed"
        else:
            task.status = "Completed"
        task_frame.label_status.configure(
            text=task.status,
            text_color="#00ff00" if task.status == "Completed" else "#ff7f00",
        )
        if task.status == "Completed":
            task_frame.checkbox_var.set("on")
        else:
            task_frame.checkbox_var.set("off")

    def create_task_frame(self, item, index):
        description = getattr(item, "description", "Error")
        status = getattr(item, "status", "Error")
        DISPLAY_PATH = self.parent.display.display_frame  # cesta k display framu
        DISPLAY_PATH.label_frame = ctk.CTkFrame(DISPLAY_PATH)
        DISPLAY_FRAME = DISPLAY_PATH.label_frame
        DISPLAY_FRAME.pack_propagate(True)
        DISPLAY_FRAME.pack(side="top", fill="x", pady=(0, 7), ipady=5)

        label_description = ctk.CTkLabel(
            DISPLAY_FRAME,
            text=description,
            font=self.parent.font_normal,
        )
        label_description.grid(row=0, column=0, sticky="w", padx=5)

        label_status = ctk.CTkLabel(
            DISPLAY_FRAME,
            text=status,
            font=self.parent.font_normal,
            width=140,
            anchor="w",
        )
        label_status.grid(row=0, column=1, sticky="w")

        var = ctk.StringVar(value="off")
        checkbox_status = ctk.CTkCheckBox(
            DISPLAY_FRAME,
            variable=var,
            onvalue="on",
            offvalue="off",
            font=self.parent.font_normal,
            text="",
            width=0,
        )
        checkbox_status.grid(row=0, column=2, sticky="e", padx=10)

        DISPLAY_FRAME.label_description = label_description
        DISPLAY_FRAME.label_status = label_status
        DISPLAY_FRAME.checkbox_var = var

        if status == "Completed":
            label_status.configure(text_color="#00ff00")
            var.set("on")
        else:
            label_status.configure(text_color="#ff7f00")
            var.set("off")

        DISPLAY_FRAME.bind(
            "<Button-1>", lambda event: self.toggle_task_status(DISPLAY_FRAME, index)
        )
        label_description.bind(
            "<Button-1>", lambda event: self.toggle_task_status(DISPLAY_FRAME, index)
        )
        label_status.bind(
            "<Button-1>", lambda event: self.toggle_task_status(DISPLAY_FRAME, index)
        )

        DISPLAY_FRAME.columnconfigure(0, weight=1, uniform="a")
        DISPLAY_FRAME.columnconfigure(1, weight=0, uniform="b")
        DISPLAY_FRAME.columnconfigure(2, weight=0, uniform="c")
        DISPLAY_FRAME.rowconfigure(0, weight=1, uniform="a")

    def add_task(self, event=None, status="Not Completed"):
        user_input = self.parent.header.input_task.get().strip()
        self.parent.header.input_task.delete(0, ctk.END)
        if not user_input:
            self.parent.footer.message_label.configure(text="Please enter a task.")
        else:
            new_task = Task(user_input, status)
            self.tasks.append(new_task)
            item = self.tasks[-1] if self.tasks else None
            self.create_task_frame(item, len(self.tasks) - 1)
            self.parent.footer.message_label.configure(text="")

    def warning_input_task(self):
        """Resetuje vstupní pole do stavu varování."""
        self.parent.header.input_task.configure(
            placeholder_text="Please enter a task",
            placeholder_text_color="#ff7f00",
            text_color="#ff7f00",
        )

    def new_multi_labels(self, seznam):
        for index, item in enumerate(seznam):
            self.create_task_frame(item, index)

    def remove_task(self):
        for task_frame in self.parent.display.display_frame.winfo_children():
            if task_frame.checkbox_var.get() == "on":
                task_description = task_frame.label_description.cget("text")
                task_to_remove = next(
                    (
                        task
                        for task in self.tasks
                        if task.description == task_description
                    ),
                    None,
                )
                if task_to_remove:
                    self.tasks.remove(task_to_remove)
                task_frame.destroy()

        # Aktualizace zobrazení
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
