import tkinter as tk
import customtkinter as ctk


class App(ctk.CTk):
    # constants
    font_big = ("Arial", 30, "bold")
    font_normal = ("Arial", 20, "normal")
    font_small = ("Arial", 16, "normal")

    # constructor
    def __init__(self):
        super().__init__()
        self.title("TODO-List")
        self.iconbitmap("./assets/ico.ico")
        self.center_window()
        self.resizable(False, False)

        self.header = Header(self)

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
        parent = parent
        super().__init__(parent)
        self.pack(side="top", fill="x", pady=20, padx=20)

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


if __name__ == "__main__":
    app = App()
    app.mainloop()