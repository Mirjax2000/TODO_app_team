import customtkinter as ctk
from PIL import Image
from json import load


def load_settings(entry: str) -> dict:
    with open(entry, "r") as file:
        return load(file)


settings: dict = load_settings("./config/settings.json")

app_size: dict = settings["app_size"]
app_width: int = app_size.get("width", 1000)
app_height: int = app_size.get("height", 600)
window_scale: float = app_size.get("window_scale", 1.0)
widget_scale: float = app_size.get("widget_scale", 1.0)

colors: dict = settings["colors"]
error_color: str = "red"
theme_color: str = colors.get("theme_color", "blue")
appearance: str = colors.get("appearance", "Dark")
inner_color: str = colors.get("inner_color", error_color)
outer_color: str = colors.get("outer_color", error_color)
label_color: str = colors.get("label_color", error_color)
bad_color: str = colors.get("bad_color", error_color)
good_color: str = colors.get("good_color", error_color)
btn_color_dark: str = colors.get("btn_color_dark", error_color)
btn_color_light: str = colors.get("btn_color_light", error_color)
border_color: str = colors.get("border_color", error_color)
started_color: str = colors.get("started_color", error_color)
not_started_color: str = colors.get("not_started_color", error_color)
complete_color: str = colors.get("complete_color", error_color)
on_hold_color: str = colors.get("on_hold_color", error_color)
fg_started_color: str = colors.get("fg_started_color", error_color)
fg_on_hold_color: str = colors.get("fg_on_hold_color", error_color)

details: dict = settings["details"]
corner_radius: int = details.get("corner_radius", 8)
opacity: float = details.get("opacity", 0.3)


# variables
font_big: tuple[str, int, str] = ("Arial", 30, "normal")
font_normal: tuple[str, int, str] = ("Arial", 20, "normal")
font_small: tuple[str, int, str] = ("Arial", 16, "normal")
version: float = 0.7
# images
img_error = ctk.CTkImage(
    light_image=Image.open("./assets/exclamation2.png"), size=(25, 25)
)


default_state = {
    "btn_1": "disabled",
    "btn_2": "disabled",
    "btn_3": "normal",
    "btn_4": "disabled",
    "btn_5": "disabled",
    "btn_6": "disabled",
    "footer_label": "disabled",
    "footer_entry": "disabled",
}

active_state = {
    "btn_3": "disabled",
    "btn_4": "normal",
    "btn_5": "normal",
    "btn_6": "normal",
    "footer_label": "normal",
    "footer_entry": "normal",
}

if __name__ == "__main__":
    pass
