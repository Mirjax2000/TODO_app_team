import customtkinter as ctk
from pywinstyles import set_opacity
from config import settings


# zakladni nastaveni appky / theme a scaling
def basic_app_settings():
    ctk.set_default_color_theme(settings.theme_color)
    ctk.set_appearance_mode(settings.appearance)
    ctk.set_window_scaling(settings.window_scale)
    ctk.set_widget_scaling(settings.widget_scale)


def app_init(self):
    self.title("TODO-List")
    self.iconbitmap("./assets/ico.ico")
    center_window(self, settings.app_width, settings.app_height)
    self.minsize(width=800, height=543)
    self.resizable(False, True)
    self.configure(fg_color=settings.outer_color)


# centrovani appky uprostred obrazovky a rozmer
def center_window(self, app_width: int, app_height: int):
    """Centers the window on the screen."""
    self.update_idletasks()
    width: int = app_width
    height: int = app_height
    screen_width: int = self.winfo_screenwidth()
    screen_height: int = self.winfo_screenheight()
    x: int = screen_width // 2 - width // 2
    y: int = screen_height // 2 - height // 2
    self.geometry(f"{width}x{height}+{x}+{y}")


# oprava chyby CTK scrollbaru
def padding_in_scrollable(display_frame: ctk.CTkScrollableFrame):
    """Adds padding to scrollbar of a scrollable frame."""
    if scrollbar := getattr(display_frame, "_scrollbar", None):
        padding = display_frame.cget("border_width") * 1
        ctk.CTkScrollbar.grid_configure(scrollbar, padx=padding)


if __name__ == "__main__":
    pass
