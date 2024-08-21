from main import TaskManager, Task
import customtkinter as ctk
from pywinstyles import set_opacity
from config import mixins
from config import settings


class App(ctk.CTk):
    """Main App"""

    # nahrani settings do appky
    mixins.basic_app_settings()

    def __init__(self):
        self.task_manager = TaskManager(self)
        super().__init__()
        self.title("TODO-List")
        self.iconbitmap("./assets/ico.ico")
        mixins.center_window(self, settings.app_width, settings.app_height)
        self.minsize(width=800, height=543)
        self.resizable(False, True)
        self.configure(fg_color=settings.outer_color)

        # region HEADER
        # Header Frame
        self.header = ctk.CTkFrame(self, fg_color=settings.outer_color)
        self.header.pack(side="top", fill="x", padx=20, pady=20)

        # Entre field for input task
        self.input_task = ctk.CTkEntry(
            self.header,
            placeholder_text="Enter a task",
            font=settings.font_normal,
            border_width=1,
            border_color=settings.border_color,
        )
        self.input_task.focus()
        self.input_task.get()
        self.input_task.bind("<Return>", self.task_manager.add_task)
        # self.input_task.bind("<KeyPress>", task_manager.clear_error)
        self.input_task.grid(row=0, column=0, padx=(0, 20), sticky="ew")

        # Tlačítko pro přidání úkolu
        self.input_button = ctk.CTkButton(
            self.header,
            text="Add Task",
            font=settings.font_normal,
            command=self.task_manager.add_task,
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
        self.display = ctk.CTkFrame(self, fg_color=settings.outer_color)
        self.display.pack(side="top", fill="both", padx=20, expand=True)
        #
        # left btn frame
        self.display_frame = ctk.CTkScrollableFrame(
            self.display,
            fg_color=settings.inner_color,
            border_width=1,
            border_color=settings.border_color,
            corner_radius=8,
        )
        # ujub na spatne umisteny scrollbar
        mixins.padding_in_scrollable(self.display_frame)
        #
        #  right btn frame
        self.display_buttons = ctk.CTkFrame(
            self.display, fg_color=settings.outer_color, width=140
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
            "fg_color": settings.outer_color,
        }
        # Buttons top frame
        self.display_buttons_top = ctk.CTkFrame(**self.button_frame)
        # Buttons mid frame
        self.display_buttons_mid = ctk.CTkFrame(**self.button_frame)
        # Buttons bottom frame
        self.display_buttons_btm = ctk.CTkFrame(**self.button_frame)
        # activace widgetu pro btn framy
        self.display_buttons_top.grid(row=0, column=0, sticky="ns")
        self.display_buttons_mid.grid(row=1, column=0, sticky="ns", pady=30)
        self.display_buttons_btm.grid(row=2, column=0, sticky="ns")
        #
        # grid pro tlacitkovy framy
        self.display_buttons.rowconfigure(0, weight=0, uniform="a")
        self.display_buttons.rowconfigure(1, weight=0, uniform="b")
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
            "Settings",
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
            (self.display_buttons_btm, btn_text[7], path.settings, "btn_8"),  # settings
            (self.display_buttons_btm, btn_text[8], path.exit, "btn_9"),  # exit
        ]

        # label task operations
        self.label_tasks = ctk.CTkLabel(
            self.display_buttons_top,
            font=settings.font_small,
            text="Task operations",
            fg_color=settings.inner_color,
            corner_radius=8,
        )

        # label list operations
        self.label_lists = ctk.CTkLabel(
            self.display_buttons_mid,
            font=settings.font_small,
            text="List operations",
            fg_color=settings.inner_color,
            corner_radius=8,
        )

        self.label_settings = ctk.CTkLabel(
            self.display_buttons_btm,
            font=settings.font_small,
            text="Settings",
            fg_color=settings.inner_color,
            corner_radius=8,
        )
        # activation
        # create buttons and grid placement
        for parent, text, command, attr_name in self.button_configs:
            button = ctk.CTkButton(
                parent,
                text=text,
                font=settings.font_normal,
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
        self.btn_8.grid(row=2, column=0, sticky="ewn")  # settings
        self.btn_9.grid(row=3, column=0, sticky="ews")  # Exit

        # config
        self.display_buttons_top.rowconfigure(0, weight=0, uniform="b")
        self.display_buttons_mid.rowconfigure(0, weight=0, uniform="b")
        self.display_buttons_btm.rowconfigure(0, weight=0, uniform="b")
        self.display_buttons_btm.rowconfigure(1, weight=0, uniform="b")
        self.display_buttons_btm.rowconfigure(2, weight=0, uniform="b")
        self.display_buttons_btm.rowconfigure(3, weight=1, uniform="b")
        # odeslano do funkce set_default_opacity pro všechny tlačítka v self.btns_names
        self.btns_names: list = [
            self.btn_1,
            self.btn_2,
            self.btn_3,
            self.btn_4,
            self.btn_5,
            self.btn_6,
        ]
        mixins.set_default_opacity(*self.btns_names)
        # endregion
        #
        #  region FOOTER
        #  Footer frame
        self.footer = ctk.CTkFrame(self, fg_color=settings.outer_color)
        self.footer.pack(side="bottom", fill="x", pady=20, padx=20)

        # Vstupní pole pro zadání jména seznamu
        self.footer_label = ctk.CTkLabel(
            self.footer,
            font=settings.font_normal,
            text="List name: ",
        )

        # Vstupní pole pro zadání jména seznamu
        self.footer_entry = ctk.CTkEntry(
            self.footer,
            width=300,
            font=settings.font_normal,
            placeholder_text="List name: ",
            fg_color=settings.inner_color,
            border_color=settings.border_color,
            border_width=1,
        )
        self.footer_entry.get()

        # error label + img
        self.error_label = ctk.CTkLabel(
            self.footer,
            font=settings.font_small,
            text_color=settings.bad_color,
            fg_color=settings.inner_color,
            text="",
            justify="center",
            corner_radius=10,
            image=settings.img_error,
            compound="left",
        )

        # activation
        self.footer_label.grid(row=0, column=0, sticky="w")
        self.footer_entry.grid(row=0, column=1, sticky="ew")
        self.error_label.grid(row=0, column=2, sticky="", ipadx=10)
        self.error_label.grid_remove()  # skryt error label, defaultně skryte
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

    def __init__(
        self,
        parent,
        text: str,
        status: str = "Not Started",
        user: str = "Not assigned",
    ):
        self.parent = parent
        self.text = text
        self.status = status
        self.user = user
        super().__init__(
            self.parent,
            fg_color=settings.outer_color,
            corner_radius=5,
            border_width=1,
            border_color=settings.not_started_color,
        )
        self.pack(fill="x", padx=10, pady=3, ipady=5)
        set_opacity(self, value=0.8, color="black")

        self.task_label = ctk.CTkLabel(self, font=settings.font_normal, text=self.text)
        self.options_users: list[str] = [
            "Not assigned",
        ]
        self.user_label = ctk.CTkOptionMenu(
            self,
            font=settings.font_small,
            values=self.options_users,
            width=130,
            anchor="center",
            dropdown_font=settings.font_small,
            dynamic_resizing=False,
            dropdown_fg_color=settings.outer_color,
            dropdown_hover_color=settings.btn_color_light,
            corner_radius=8,
        )

        self.user_label.set(self.user)
        self.user_label.get()
        self.options_status: list[str] = [
            "Started",
            "On Hold",
            "Complete",
            "Not Started",
        ]
        self.status_label = ctk.CTkOptionMenu(
            self,
            font=settings.font_small,
            values=self.options_status,
            width=130,
            anchor="center",
            dropdown_font=settings.font_small,
            dynamic_resizing=False,
            dropdown_fg_color=settings.outer_color,
            dropdown_hover_color=settings.btn_color_light,
            corner_radius=8,
            command=self.update_color,
        )

        self.status_label.set(self.status)
        self.status_label.get()
        self.update_color(choice=self.status)  # initial color update

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
                "border_color": settings.not_started_color,
                "fg_color": settings.outer_color,
                "opacity": 0.8,
            },
            "Started": {
                "border_color": settings.started_color,
                "fg_color": settings.fg_started_color,
                "opacity": 1,
            },
            "On Hold": {
                "border_color": settings.on_hold_color,
                "fg_color": settings.fg_on_hold_color,
                "opacity": 0.7,
            },
            "Complete": {
                "border_color": settings.complete_color,
                "fg_color": settings.inner_color,
                "opacity": 0.4,
            },
        }

        config = config_map.get(status, config_map["Complete"])
        self.configure(border_color=config["border_color"], fg_color=config["fg_color"])
        set_opacity(self, value=config["opacity"], color="black")


# endregion


if __name__ == "__main__":
    pass
