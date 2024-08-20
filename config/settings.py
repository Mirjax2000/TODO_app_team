import customtkinter as ctk
from PIL import Image
from json import load


def load_settings(entry: str) -> dict:
    with open(entry, "r") as file:
        return load(file)


settings: dict = load_settings("./config/settings.json")
for key, value in settings.items():
    app_width: int = value.get("width", 1000)
    app_height: int = value.get("height", 600)
    inner_color: str = value.get("inner_color", "red")
    outer_color: str = value.get("outer_color", "red")
    label_color: str = value.get("label_color", "red")
    bad_color: str = value.get("bad_color", "red")
    good_color: str = value.get("good_color", "red")
    btn_color_dark: str = value.get("btn_color_dark", "red")
    btn_color_light: str = value.get("btn_color_light", "red")
    border_color: str = value.get("border_color", "red")
    started_color: str = value.get("strted_color", "red")
    not_started_color: str = value.get("not_started_color", "red")
    complete_color: str = value.get("complete_color", "red")
    fg_started_color: str = value.get("fg_started_color", "red")
    on_hold_color: str = value.get("on_hold_color", "red")
    fg_on_hold_color: str = value.get("fg_on_hold_color", "red")


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
