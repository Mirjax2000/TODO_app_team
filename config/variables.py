import customtkinter as ctk
from PIL import Image


# variables
font_big: tuple[str, int, str] = ("Arial", 30, "normal")
font_normal: tuple[str, int, str] = ("Arial", 20, "normal")
font_small: tuple[str, int, str] = ("Arial", 16, "normal")
version: float = 0.5
# images
img_error = ctk.CTkImage(
    light_image=Image.open("./assets/exclamation2.png"), size=(25, 25)
)
# colors
inner_color: str = "#292929"
outer_color: str = "#1c1c1c"
label_color: str = "#393939"
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
