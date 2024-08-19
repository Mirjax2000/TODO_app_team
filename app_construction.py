import customtkinter as ctk
from main import TaskManager, Task
from PIL import Image
from pywinstyles import set_opacity
from mixiny import mixiny

print(ctk.__file__)

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
good_color: str = "#08ff00"
btn_color_dark: str = "#14375e"
btn_color_light: str = "#144870"
border_color: str = "#696969"
started_color: str = "#00519e"
not_started_color: str = "#c86300"
complete_color: str = "#059400"
fg_started_color: str = "#001021"
on_hold_color: str = "#ffee4c"
fg_on_hold_color: str = "#241f0f"


ctk.set_default_color_theme("blue")
ctk.set_appearance_mode("Dark")
ctk.set_window_scaling(1.0)
ctk.set_widget_scaling(1.0)


class App(ctk.CTk):
    """Main App"""

    def __init__(self, task_manager):
        self.task_manager: TaskManager = task_manager
        super().__init__()
        self.title("TODO-List")
        self.iconbitmap("./assets/ico.ico")
        mixiny.center_window(self)
        self.resizable(False, False)
        self.configure(fg_color=outer_color)

        # region HEADER
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

        # Tlačítko pro přidání úkolu
        self.input_button = ctk.CTkButton(
            self.header,
            text="Add Task",
            font=font_normal,
            command=task_manager.add_task,
        )
        self.input_button.grid(row=0, column=1, sticky="e")

        # # Grid konfigurace headru
        self.header.columnconfigure(0, weight=1, uniform="a")
        self.header.columnconfigure(1, weight=0, uniform="b")
        self.header.rowconfigure(0, weight=0, uniform="a")
        # endregion
        #
        #
        # region BODY
        # a main frame
        self.display = ctk.CTkFrame(self, fg_color=outer_color)
        self.display.pack(side="top", fill="both", padx=20, expand=True)
        #
        # left btn frame
        self.display_frame = ctk.CTkScrollableFrame(
            self.display,
            fg_color=inner_color,
            border_width=1,
            border_color=border_color,
            corner_radius=8,
        )
        # ujub na spatne umisteny scrollbar
        mixiny.padding_in_scrollable(self.display_frame)
        #
        #  right btn frame
        self.display_buttons = ctk.CTkFrame(
            self.display, fg_color=outer_color, width=140
        )
        # right and left frame activated
        self.display_frame.grid(row=0, column=0, sticky="nsew")
        self.display_buttons.grid(row=0, column=1, sticky="nsew", padx=(20, 0))
        # right and left frame configure
        self.display.rowconfigure(0, weight=1, uniform="c")  # both frames
        self.display.columnconfigure(0, weight=1, uniform="a")  # left frame
        self.display.columnconfigure(1, weight=0, uniform="b")  # right frame
        #
        # buttons frames top, mid, bottom
        self.button_frame = {  # config for all buttons
            "master": self.display_buttons,  # parent
            # "width": 140,
            "fg_color": outer_color,
        }
        # Buttons top frame
        self.display_buttons_top = ctk.CTkFrame(**self.button_frame)
        # Buttons mid frame
        self.display_buttons_mid = ctk.CTkFrame(**self.button_frame)
        # Buttons bottom frame
        self.display_buttons_btm = ctk.CTkFrame(**self.button_frame)
        # activace widgetu pro btn framy
        self.display_buttons_top.grid(row=0, column=0, sticky="ns")
        self.display_buttons_mid.grid(row=1, column=0, sticky="ns", pady=20)
        self.display_buttons_btm.grid(row=2, column=0, sticky="ns")
        #
        # grid pro tlacitkovy framy
        self.display_buttons.rowconfigure(0, weight=0, uniform="a")
        self.display_buttons.rowconfigure(1, weight=1, uniform="b")
        self.display_buttons.rowconfigure(2, weight=1, uniform="c")
        self.display_buttons.columnconfigure(0, weight=0, uniform="a")
        #
        # Create buttons dynamically
        btn_text = [
            "Remove task",
            "Edit task",
            "Load list",
            "Extend list",
            "Save list",
            "Clear list",
            "Users/Groups",
            "Exit",
        ]
        path = self.task_manager
        self.button_configs = [
            (
                self.display_buttons_top,
                btn_text[0],
                path.remove_task,
                "btn_1",
            ),  # remove task
            (
                self.display_buttons_top,
                btn_text[1],
                path.edit_task,
                "btn_2",
            ),  # edit task
            (
                self.display_buttons_mid,
                btn_text[2],
                path.load_list,
                "btn_3",
            ),  # load list
            (
                self.display_buttons_mid,
                btn_text[3],
                path.extend_list,
                "btn_4",
            ),  # extend list
            (
                self.display_buttons_mid,
                btn_text[4],
                path.save_list,
                "btn_5",
            ),  # save list
            (
                self.display_buttons_mid,
                btn_text[5],
                path.clear_list,
                "btn_6",
            ),  # clear list
            (
                self.display_buttons_btm,
                btn_text[6],
                path.user_group,
                "btn_7",
            ),  # users/groups
            (self.display_buttons_btm, btn_text[7], path.exit, "btn_8"),  # exit
        ]

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

        self.label_settings = ctk.CTkLabel(
            self.display_buttons_btm,
            font=font_small,
            text="Settings",
            fg_color=inner_color,
            corner_radius=10,
        )
        # activation
        # create buttons and grid placement
        for parent, text, command, attr_name in self.button_configs:
            button = ctk.CTkButton(
                parent,
                text=text,
                font=font_normal,
                command=command,
                corner_radius=8,
            )
            setattr(self, attr_name, button)
        # task operations: top frame
        self.label_tasks.grid(row=0, column=0, sticky="ew")  # Task operations
        self.btn_1.grid(row=1, column=0, sticky="ew")  # Remove task
        self.btn_2.grid(row=2, column=0, sticky="ew")  # Edit task
        # list operations: mid frame
        self.label_lists.grid(row=0, column=0, sticky="ew")  # List operations
        self.btn_3.grid(row=1, column=0, sticky="ew")  # Load list
        self.btn_4.grid(row=2, column=0, sticky="ew")  # Extend list
        self.btn_5.grid(row=3, column=0, sticky="ew")  # Save list
        self.btn_6.grid(row=4, column=0, sticky="ew")  # Clear list
        # settings operations: btm frame
        self.label_settings.grid(row=0, column=0, sticky="ew")  # Settings operations
        self.btn_7.grid(row=1, column=0, sticky="ewn")  # Users/Groups
        self.btn_8.grid(row=2, column=0, sticky="ews")  # Exit

        # config
        self.display_buttons_top.rowconfigure(0, weight=0, uniform="b")
        self.display_buttons_mid.rowconfigure(0, weight=0, uniform="b")
        self.display_buttons_btm.rowconfigure(0, weight=0, uniform="b")
        self.display_buttons_btm.rowconfigure(1, weight=0, uniform="b")
        self.display_buttons_btm.rowconfigure(2, weight=1, uniform="b")
        # endregion
        #
        #  region FOOTER
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
        #  endregion


#
# region TaskFrame
class TaskFrame(ctk.CTkFrame):
    """Single task frame"""

    def __init__(self, parent):
        self.parent = parent
        super().__init__(
            self.parent,
            fg_color=outer_color,
            corner_radius=5,
            border_width=1,
            border_color=not_started_color,
        )
        self.pack(fill="x", padx=10, pady=3, ipady=5)
        set_opacity(self, value=0.8, color="black")

        self.task_label = ctk.CTkLabel(self, font=font_normal, text="Task 1")
        self.options_users: list[str] = [
            "Not assigned",
        ]
        self.user_label = ctk.CTkOptionMenu(
            self,
            font=font_small,
            values=self.options_users,
            width=130,
            anchor="center",
            dropdown_font=font_small,
            dynamic_resizing=False,
            dropdown_fg_color=outer_color,
            dropdown_hover_color=btn_color_light,
            corner_radius=8,
        )

        self.user_label.set("Not asigned")
        self.user_label.get()
        self.options_status: list[str] = [
            "Started",
            "On Hold",
            "Complete",
            "Not Started",
        ]
        self.status_label = ctk.CTkOptionMenu(
            self,
            font=font_small,
            values=self.options_status,
            width=130,
            anchor="center",
            dropdown_font=font_small,
            dynamic_resizing=False,
            dropdown_fg_color=outer_color,
            dropdown_hover_color=btn_color_light,
            corner_radius=8,
            command=self.update_color,
        )

        self.status_label.set("Not Started")
        self.status_label.get()

        # activation
        self.task_label.grid(row=0, column=0, sticky="w", padx=20, pady=(10, 0))
        self.user_label.grid(row=0, column=1, sticky="e", padx=(0, 10), pady=(10, 0))
        self.status_label.grid(row=0, column=2, sticky="e", padx=(0, 10), pady=(10, 0))
        # grid config
        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=0, uniform="b")
        self.columnconfigure(2, weight=0, uniform="b")
        self.rowconfigure(0, weight=0, uniform="a")

    def update_color(self, choice: str) -> None:
        status = choice

        config_map = {
            "Not Started": {
                "border_color": not_started_color,
                "fg_color": outer_color,
                "opacity": 0.8,
            },
            "Started": {
                "border_color": started_color,
                "fg_color": fg_started_color,
                "opacity": 1,
            },
            "On Hold": {
                "border_color": on_hold_color,
                "fg_color": fg_on_hold_color,
                "opacity": 0.7,
            },
            "Complete": {
                "border_color": complete_color,
                "fg_color": inner_color,
                "opacity": 0.4,
            },
        }

        config = config_map.get(status, config_map["Complete"])
        self.configure(border_color=config["border_color"], fg_color=config["fg_color"])
        set_opacity(self, value=config["opacity"], color="black")


# endregion


if __name__ == "__main__":
    pass
