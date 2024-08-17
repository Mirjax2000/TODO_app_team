import customtkinter as ctk
from main import TaskManager, Task
from PIL import Image

# variables
font_big: tuple[str, int, str] = ("Arial", 30, "normal")
font_normal: tuple[str, int, str] = ("Arial", 20, "normal")
font_small: tuple[str, int, str] = ("Arial", 16, "normal")
version: float = 0.5

img_error = ctk.CTkImage(
    light_image=Image.open("./assets/exclamation2.png"), size=(30, 30)
)

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

    def __init__(self, task_manager):
        self.task_manager: TaskManager = task_manager
        super().__init__()
        self.title("TODO-List")
        self.iconbitmap("./assets/ico.ico")
        self.center_window()
        self.resizable(False, False)
        self.configure(fg_color=outer_color)

        # Frames
        # Header Frame
        self.header = ctk.CTkFrame(self, fg_color=outer_color)
        self.header.pack(side="top", fill="x", padx=20, pady=20)

        # Entre field for input task
        self.input_task = ctk.CTkEntry(
            self.header,
            placeholder_text="Enter a task",
            font=font_normal,
            border_width=1,
            border_color=border_color,
        )
        self.input_task.get()
        # self.input_task.bind("<Return>", self.add_task) # Todo dopln Funkci
        self.input_task.grid(row=0, column=0, padx=(0, 20), sticky="ew")

        # # Tlačítko pro přidání úkolu
        self.input_button = ctk.CTkButton(
            self.header,
            text="Add Task",
            font=font_normal,
            # command=, # Todo dopln funkci
        )
        self.input_button.grid(row=0, column=1, sticky="e")

        # # Grid konfigurace headru
        self.header.columnconfigure(0, weight=1, uniform="a")
        self.header.columnconfigure(1, weight=0, uniform="b")
        self.header.rowconfigure(0, weight=0, uniform="a")

        # a main frame: body
        self.display = ctk.CTkFrame(self, fg_color=outer_color)
        self.display.pack(side="top", fill="both", padx=20, expand=True)
        # left btn frame
        self.display_frame = ctk.CTkFrame(
            self.display,
            fg_color=inner_color,
            border_width=1,
            border_color=border_color,
        )
        #
        # # right btn frame
        self.display_buttons = ctk.CTkFrame(
            self.display, fg_color=outer_color, width=140
        )
        # right and left frame activated
        self.display_frame.grid(row=0, column=0, sticky="nsew")
        self.display_buttons.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        # right and left frame configure
        self.display.columnconfigure(0, weight=1, uniform="a")
        self.display.columnconfigure(1, weight=0, uniform="b")
        self.display.rowconfigure(0, weight=1, uniform="c")
        #
        # buttons frames top, mid, bottom
        self.button_frame = {  # config for all buttons
            "master": self.display_buttons,  # parent
            "width": 140,
            "fg_color": outer_color,
        }
        # Buttons in top
        self.display_buttons_top = ctk.CTkFrame(**self.button_frame)
        # Buttons in mid
        self.display_buttons_mid = ctk.CTkFrame(**self.button_frame)
        # Buttons in bottom
        self.display_buttons_btm = ctk.CTkFrame(**self.button_frame)
        # activace widgetu pro btn framy
        self.display_buttons_top.grid(row=0, column=0, sticky="ns")
        self.display_buttons_mid.grid(row=1, column=0, sticky="ns", pady=20)
        self.display_buttons_btm.grid(row=2, column=0, sticky="s")
        #
        # grid pr tlacitkovy framy
        self.display_buttons.rowconfigure(0, weight=1, uniform="a")
        self.display_buttons.rowconfigure(1, weight=1, uniform="b")
        self.display_buttons.rowconfigure(2, weight=1, uniform="c")
        self.display_buttons.columnconfigure(0, weight=0, uniform="a")
        #
        # Create buttons dynamically
        path = self.task_manager
        self.button_configs = [
            (self.display_buttons_top, btn_text[0], path.remove_task, "btn_1"),
            (self.display_buttons_top, btn_text[1], path.edit_task, "btn_2"),
            (self.display_buttons_mid, btn_text[2], path.load_list, "btn_3"),
            (self.display_buttons_mid, btn_text[3], path.extend_list, "btn_4"),
            (self.display_buttons_mid, btn_text[4], path.save_list, "btn_5"),
            (self.display_buttons_mid, btn_text[5], path.clear_list, "btn_6"),
            (self.display_buttons_btm, btn_text[6], path.exit, "btn_7"),
        ]
        #
        for parent, text, command, attr_name in self.button_configs:
            button = ctk.CTkButton(parent, text=text, font=font_normal, command=command)
            setattr(self, attr_name, button)
        # grid config
        for i in range(len(self.button_configs)):
            button = getattr(self, f"btn_{i + 1}")
            button.grid(row=i + 1, column=0, sticky="n", pady=1)
        # clear list config
        self.display_buttons_mid.rowconfigure(5, weight=1, uniform="a")

        # label task operations
        self.label_tasks = ctk.CTkLabel(
            self.display_buttons_top,
            font=font_small,
            text="Task operations",
            fg_color=inner_color,
            corner_radius=10,
        )

        # label list operations
        self.label_lists = ctk.CTkLabel(
            self.display_buttons_mid,
            font=font_small,
            text="List operations",
            fg_color=inner_color,
            corner_radius=10,
        )
        # activation
        self.label_tasks.grid(row=0, column=0, sticky="ew")
        self.label_lists.grid(row=0, column=0, sticky="ew")
        # label config
        self.display_buttons_top.rowconfigure(0, weight=0, uniform="b")
        self.display_buttons_mid.rowconfigure(0, weight=0, uniform="b")

        #  Footer frame
        self.footer = ctk.CTkFrame(self, fg_color=outer_color)
        self.footer.pack(side="bottom", fill="x", pady=20, padx=20)

        # Vstupní pole pro zadání jména seznamu
        self.footer_label = ctk.CTkLabel(
            self.footer,
            font=font_normal,
            text="List name: ",
        )

        # Vstupní pole pro zadání jména seznamu
        self.footer_entry = ctk.CTkEntry(
            self.footer,
            width=300,
            font=font_normal,
            placeholder_text="List name: ",
            fg_color=inner_color,
            border_color=border_color,
            border_width=1,
        )
        self.footer_entry.get()

        # error label + img

        self.error_label = ctk.CTkLabel(
            self.footer,
            font=font_small,
            text_color=bad_color,
            fg_color=inner_color,
            text="error message",
            justify="center",
            corner_radius=10,
            image=img_error,
            compound="left",
        )

        # activation
        self.footer_label.grid(row=0, column=0, sticky="w")
        self.footer_entry.grid(row=0, column=1, sticky="ew")
        self.error_label.grid(row=0, column=2, sticky="", ipadx=10)
        self.error_label.grid_remove()  # skryt error label
        # grid config
        self.footer.columnconfigure(0, weight=0, uniform="a")
        self.footer.columnconfigure(1, weight=0, uniform="b")
        self.footer.columnconfigure(2, weight=1, uniform="c")
        self.footer.rowconfigure(0, weight=0, uniform="a")

    def center_window(self):  # center screen in the middle
        """Centers the window on the screen."""
        self.update_idletasks()
        width: int = 1000
        height: int = 600
        screen_width: int = self.winfo_screenwidth()
        screen_height: int = self.winfo_screenheight()
        x: int = screen_width // 2 - width // 2
        y: int = screen_height // 2 - height // 2
        self.geometry(f"{width}x{height}+{x}+{y}")


class TaskFrame(ctk.CTkFrame):
    """frame na jednotlive tasky"""

    def __init__(self, parent):
        self.parent = parent.display_frame
        super().__init__(self.parent, fg_color="white")
        self.pack(fill="x", padx=20, pady=20)

        self.task_label = ctk.CTkLabel(self, font=font_normal, text="Task 1")
        self.status_label = ctk.CTkLabel(self, font=font_normal, text="Not Started")
        self.checkbox = ctk.CTkLabel(self, text="| |", font=font_normal)

        self.task_label.grid(row=0, column=0, sticky="ew")
        self.status_label.grid(row=0, column=1, sticky="ew")
        self.checkbox.grid(row=0, column=2, sticky="ew")


if __name__ == "__main__":
    pass
