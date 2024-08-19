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

    # # ujub na spatne umisteny scrollbar
    # def padding_in_scrollable(display_frame: ctk.CTkScrollableFrame):
    #     """Adds padding to scrollbar of a scrollable frame."""
    #     if scrollbar := getattr(display_frame, "_scrollbar", None):
    #         padding = display_frame.cget("border_width") * 1
    #         ctk.CTkScrollbar.grid_configure(scrollbar, padx=padding)


if __name__ == "__main__":
    pass
