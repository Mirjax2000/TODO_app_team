import tkinter as tk
import customtkinter as ctk


class App(ctk.CTk):  # Main app
    # constants
    font_big = ("Arial", 30, "normal")
    font_normal = ("Arial", 20, "normal")
    font_small = ("Arial", 16, "normal")

    # constructor
    def __init__(self):
        super().__init__()
        self.title("TODO-List")
        self.iconbitmap("./assets/ico.ico")
        self.center_window()
        self.resizable(False, False)

        # Frames
        self.header = Header(self)
        self.display = Display(self)
        self.footer = Footer(self)

    def center_window(self):
        self.update_idletasks()
        width = 800
        height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = screen_width // 2 - width // 2
        y = screen_height // 2 - height // 2
        self.geometry(f"{width}x{height}+{x}+{y}")


class Header(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.pack(side="top", fill="x", pady=20, padx=20)

        # widgets input, button
        self.input_task = ctk.CTkEntry(
            self, placeholder_text="Enter task", font=parent.font_normal
        )
        self.input_task.get()
        self.input_task.focus()
        self.input_task.bind("<FocusIn>", self.clear_text)
        self.input_task.bind("<Return>", self.add_task)
        self.input_task.grid(row=0, column=0, sticky="ew", padx=(0, 10))

        self.input_btn = ctk.CTkButton(
            self, text="Add Task", font=parent.font_normal, command=self.add_task
        )
        self.input_btn.grid(row=0, column=1)

        self.columnconfigure(0, weight=1, uniform="a")
        self.columnconfigure(1, weight=0, uniform="a")

    def add_task(self, event=None):
        user_input = self.input_task.get()
        print(f"Added task: {user_input}")

    @staticmethod
    def clear_text(event):
        event.widget.delete(0, ctk.END)


class Display(ctk.CTkFrame):
    def __init__(self, parent):
        self.parent = parent
        self.btns_text = ["Remove task", "Edit task", "Save list", "Load list", "Exit"]
        super().__init__(parent)
        self.pack(side="top", fill="x", pady=20, padx=20)

        for item in self.btns_text:
            row_set = self.btns_text.index(item)
            self.btn = ctk.CTkButton(
                self,
                font=parent.font_normal,
                text=item,
                command=getattr(self, item.lower().replace(" ", "_")),
            )
            self.btn.grid(row=row_set, column=1)

    def remove_task(self):
        pass

    def edit_task(self):
        pass

    def save_list(self):
        pass

    def load_list(self):
        pass

    def exit(self):
        app.destroy()


class Footer(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(side="top", fill="x", pady=20, padx=20)


if __name__ == "__main__":
    app = App()
    app.mainloop()

