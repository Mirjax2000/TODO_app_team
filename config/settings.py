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

colors: dict = settings["colors"]
inner_color: str = colors.get("inner_color", "red")
outer_color: str = colors.get("outer_color", "red")
label_color: str = colors.get("label_color", "red")
bad_color: str = colors.get("bad_color", "red")
good_color: str = colors.get("good_color", "red")
btn_color_dark: str = colors.get("btn_color_dark", "red")
btn_color_light: str = colors.get("btn_color_light", "red")
border_color: str = colors.get("border_color", "red")
started_color: str = colors.get("started_color", "red")
not_started_color: str = colors.get("not_started_color", "red")
complete_color: str = colors.get("complete_color", "red")
on_hold_color: str = colors.get("on_hold_color", "red")
fg_started_color: str = colors.get("fg_started_color", "red")
fg_on_hold_color: str = colors.get("fg_on_hold_color", "red")


# variables
font_big: tuple[str, int, str] = ("Arial", 30, "normal")
font_normal: tuple[str, int, str] = ("Arial", 20, "normal")
font_small: tuple[str, int, str] = ("Arial", 16, "normal")
version: float = 0.6
# images
img_error = ctk.CTkImage(
    light_image=Image.open("./assets/exclamation2.png"), size=(25, 25)
)


if __name__ == "__main__":
    pass
