import customtkinter as ctk
from main import TaskManager

# variables
font_big: tuple[str, int, str] = ("Arial", 30, "normal")
font_normal: tuple[str, int, str] = ("Arial", 20, "normal")
font_small: tuple[str, int, str] = ("Arial", 12, "normal")
version: float = 0.5

inner_color: str = "#292929"
outer_color: str = "#1c1c1c"
bad_color: str = "#ff7f00"
btn_color_dark: str = "#14375e"
btn_color_light: str = "#144870"
border_color: str = "#696969"

# lists
btn_text = [
    "Remove task",
    "Edit task",
    "Load list",
    "Extend list",
    "Save list",
    "Clear list",
    "Exit",
]


ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("Dark")
ctk.set_window_scaling(1.0)
ctk.set_widget_scaling(1.0)

# CTK classes


class App(ctk.CTk):
    """Main App"""

    # constructor
    def __init__(self):

        super().__init__()
        self.title("TODO-List")
        self.iconbitmap("./assets/ico.ico")
        self.center_window()
        self.resizable(False, False)
        self.configure(fg_color=outer_color)

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
        super().__init__(parent, fg_color=outer_color)
        self.pack(side="top", fill="x", padx=20, pady=20)

        # Vstupní pole pro zadání úkolu
        self.input_task = ctk.CTkEntry(
            self,
            placeholder_text="Enter a task",
            font=font_normal,
            border_width=1,
            border_color=border_color,
        )
        self.input_task.get()
        self.input_task.bind("<Return>", self.parent.task.add_task)
        self.input_task.grid(row=0, column=0, padx=(0, 20), sticky="ew")

        # Tlačítko pro přidání úkolu
        self.input_btn = ctk.CTkButton(
            self,
            text="Add Task",
            font=font_normal,
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
        super().__init__(parent, fg_color=outer_color)
        self.pack(side="top", fill="both", padx=20, expand=True)
        # levy frame s tasky
        self.display_frame = ctk.CTkFrame(
            self, fg_color=inner_color, border_width=1, border_color=border_color
        )
        self.display_frame.grid(row=0, column=0, sticky="nsew")
        # pravy frame s tlacitkama
        self.display_btns = ctk.CTkFrame(self, fg_color=outer_color, width=140)
        self.display_btns.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        # grid pro framy pro vsechny tlacitka
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=0, uniform="b")
        self.rowconfigure(0, weight=1, uniform="c")
        # buttons framy top, mid, bottom
        self.frame_config = {
            "master": self.display_btns,
            "width": 140,
            "fg_color": outer_color,
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
        path = parent.task
        self.button_configs = [
            (self.display_btns_top, btn_text[0], path.remove_task, "btn_1"),
            (self.display_btns_top, btn_text[1], path.edit_task, "btn_2"),
            (self.display_btns_mid, btn_text[2], path.load_list, "btn_3"),
            (self.display_btns_mid, btn_text[3], path.save_list, "btn_4"),
            (self.display_btns_mid, btn_text[4], path.extend_list, "btn_5"),
            (self.display_btns_mid, btn_text[5], path.clear_list, "btn_6"),
            (self.display_btns_btm, btn_text[6], path.exit, "btn_7"),
        ]
        #
        for parent, text, command, attr_name in self.button_configs:
            button = ctk.CTkButton(parent, text=text, font=font_normal, command=command)
            setattr(self, attr_name, button)
        #
        for i in range(len(self.button_configs)):
            button = getattr(self, f"btn_{i + 1}")
            button.grid(row=i + 1, column=0, sticky="n", pady=1)

        self.display_btns_mid.rowconfigure(5, weight=1, uniform="a")

        # labels
        self.label_tasks = ctk.CTkLabel(
            self.display_btns_top,
            font=font_small,
            text="Task operations",
            fg_color=inner_color,
            corner_radius=10,
        )
        self.label_tasks.grid(row=0, column=0, sticky="ew")

        self.label_lists = ctk.CTkLabel(
            self.display_btns_mid,
            font=font_small,
            text="List operations",
            fg_color=inner_color,
            corner_radius=10,
        )
        self.label_lists.grid(row=0, column=0, sticky="ew")


class Footer(ctk.CTkFrame):
    """spodni frame pro text a tlacitko pro ulozeni seznamu"""

    def __init__(self, parent):
        super().__init__(parent, fg_color=outer_color)
        self.parent = parent
        self.pack(side="bottom", fill="x", pady=20, padx=20)

        self.footer_label = ctk.CTkLabel(
            self,
            font=font_normal,
            text="List name: ",
        )
        self.footer_label.grid(row=0, column=0, sticky="w")
        self.footer_entry = ctk.CTkEntry(
            self,
            width=300,
            font=font_normal,
            placeholder_text="List name: ",
            fg_color=inner_color,
            border_color=border_color,
            border_width=1,
        )
        self.footer_entry.get()
        self.footer_entry.grid(row=0, column=1, sticky="ew")

        self.message_label = ctk.CTkLabel(
            self, font=font_small, text_color=bad_color, text=""
        )
        self.message_label.grid(row=0, column=2, sticky="ew")
        self.columnconfigure(0, weight=0, uniform="a")
        self.columnconfigure(1, weight=0, uniform="b")
        self.columnconfigure(2, weight=1, uniform="c")


if __name__ == "__main__":
    pass
