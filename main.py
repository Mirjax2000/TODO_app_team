import csv
import os
import customtkinter as ctk
from icecream import ic
from pywinstyles import set_opacity

ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("Dark")


class App(ctk.CTk):
    """Main App"""

    font_big: tuple = ("Arial", 30, "normal")
    font_normal: tuple = ("Arial", 20, "normal")
    font_small: tuple = ("Arial", 16, "normal")

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
        """Centers the window on the screen."""
        self.update_idletasks()
        width: int = 1000
        height: int = 600
        screen_width: int = self.winfo_screenwidth()
        screen_height: int = self.winfo_screenheight()
        x: int = screen_width // 2 - width // 2
        y: int = screen_height // 2 - height // 2
        self.geometry(f"{width}x{height}+{x}+{y}")


class Header(ctk.CTkFrame):
    """Frame pro hlavičku"""

    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.pack(side="top", fill="x", padx=20, pady=20)

        # Vstupní pole pro zadání úkolu
        self.input_task = ctk.CTkEntry(
            self, placeholder_text="Enter a task", font=parent.font_normal
        )
        self.input_task.get()
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


class Display(ctk.CTkFrame):
    """Frame pro zobrazeni seznamu úkolů"""

    def __init__(self, parent):
        self.parent = parent
        self.btns_text: list = [
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
        self.frame_config: dict = {
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
        self.button_configs: list = [
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
        """Funkce pro odebrani tasku z listu a odstraneni jeho labelu"""
        self.parent.task.remove_task()

    def edit_task(self):
        """Funkce pro editaci task labelu"""
        pass

    def save_list(self):
        """Ulozeni tasku do csv souboru"""
        self.parent.task.save_tasks_to_csv()

    def load_list(self):
        """nacitani tasku z csv souboru a vytvoreni labelu"""
        self.parent.task.load_tasks_from_csv()

    def extend_list(self):
        """Funkce pro zvetseni pocet polozek v listu"""
        pass

    def clear_list(self):
        """Funkce na vymazani hlavniho listu a smazani textu v display"""
        self.parent.task.tasks.clear()
        for child in self.parent.display.display_frame.winfo_children():
            child.destroy()

    @staticmethod
    def exit():
        """Ukonceni appky"""
        app.destroy()


class Footer(ctk.CTkFrame):
    """spodni frame pro text a tlacitko pro ulozeni seznamu"""

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
            width=300,
            font=parent.font_normal,
            placeholder_text="List name: ",
        )
        self.footer_entry.get()
        self.footer_entry.grid(row=0, column=1, sticky="ew")

        self.message_label = ctk.CTkLabel(
            self, font=parent.font_small, text_color="#ff7f00", text=""
        )
        self.message_label.grid(row=0, column=2, sticky="ew")
        self.columnconfigure(0, weight=0, uniform="a")
        self.columnconfigure(1, weight=0, uniform="b")
        self.columnconfigure(2, weight=1, uniform="c")


class TaskManager:
    """Trida pro správu úkolů"""

    def __init__(self, parent):
        self.parent = parent
        self.tasks: list = []
        self.remove: list = []  # Inicializujeme self.remove

    def save_tasks_to_csv(self):
        """Uloží všechny úkoly do CSV souboru"""
        list_name = ""
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

    def load_tasks_from_csv(self):
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
            font=self.parent.font_normal,
        )
        display_frame.label_description.grid(row=0, column=0, sticky="w", padx=5)

        # label status
        display_frame.label_status = ctk.CTkLabel(
            display_frame,
            text=status,
            font=self.parent.font_normal,
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
            font=self.parent.font_normal,
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

        bind_1 = ("<Button-1>", lambda event: self.on_label_click(event, index))
        display_frame.bind(*bind_1)
        display_frame.label_description.bind(*bind_1)
        display_frame.label_status.bind(*bind_1)

    def add_task(self, event=None, status="Not Completed"):
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


class Task:
    """Trida pro uchování jednoho úkolu"""

    def __init__(self, description, status, parent):
        """Inicializuje ukol"""
        self.parent = parent
        self.description = description
        self.status = status

    def __str__(self):
        return f"Description: {self.description}, Status: {self.status}"

    def print_task(self):
        """Vypise ukol primo z classy Task"""

        for task in self.parent.task.tasks:
            print(f"__str__: {str(task)}")


if __name__ == "__main__":
    app: App = App()
    app.mainloop()
