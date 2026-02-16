import customtkinter
import tkinter
from typing import Union, Tuple, Optional, Any


class Sidebar:
    master = Any
    title = ''
    minimal_tittle = ''
    general_frame = None
    content_frame = None
    minimal_content_frame = None
    sidebar_x_padding = 0
    sidebar_y_padding = 0
    title_component = None
    minimal_width = 32
    width = 100
    generate_tittle = False

    def __init__(self, master: Any,
                 generate_title: Optional[bool] = True,
                 title: Optional[str] = '',
                 general_width: Optional[int] = 100,
                 minimal_width: Optional[int] = 32,
                 sidebar_x_padding: Optional[int] = 0,
                 sidebar_y_padding: Optional[int] = 0,
                 sidebar_fg_color: Optional[Union[str, Tuple[str, str]]] = ('#d8e8d8', '#2b302b'),
                 sidebar_bg_color: Optional[Union[str, Tuple[str, str]]] = 'transparent',
                 sidebar_corner_radius: Optional[int] = 0,
                 minimal_tittle: Optional[str] = ''
                 ):
        self.minimal_width = minimal_width
        self.width = general_width
        self.minimal_tittle = minimal_tittle
        self.sidebar_x_padding = sidebar_x_padding
        self.sidebar_y_padding = sidebar_y_padding
        self.master = master
        self.title = title
        self.generate_tittle = generate_title
        general_frame = customtkinter.CTkFrame(master, width=general_width,
                                               corner_radius=sidebar_corner_radius,
                                               fg_color=sidebar_fg_color,
                                               bg_color=sidebar_bg_color
                                               )
        self.general_frame = general_frame
        if self.generate_tittle:
            self.title_component = customtkinter.CTkLabel(general_frame, text=title, width=general_width)
            self.title_component.pack(padx=5, pady=5, side=tkinter.TOP)

        self.content_frame = customtkinter.CTkFrame(general_frame, width=general_width,
                                                    fg_color=sidebar_fg_color,)

        self.minimal_content_frame = customtkinter.CTkFrame(general_frame, width=minimal_width,
                                                            fg_color=sidebar_fg_color)

        pass

    def pack(self):
        self.general_frame.pack(padx=0, pady=0, fill='both', expand=True)

    def get_content_frame(self):
        return self.content_frame

    def get_minimal_content_frame(self):
        return self.minimal_content_frame

    def show_content(self):
        self.unpack_modes()
        self.content_frame.pack(padx=self.sidebar_x_padding, pady=self.sidebar_y_padding, side=tkinter.BOTTOM, fill='both',
                                expand=True)
        if self.generate_tittle:
            self.title_component.configure(text=self.title, width=self.width)

    def show_minimal_content(self):
        self.unpack_modes()
        self.minimal_content_frame.pack(padx=self.sidebar_x_padding, pady=self.sidebar_y_padding, side=tkinter.BOTTOM,
                                        fill='both',
                                        expand=True)
        if self.generate_tittle:
            self.title_component.configure(text=self.minimal_tittle, width=self.minimal_width)

    def unpack_modes(self):
        self.minimal_content_frame.pack_forget()
        self.content_frame.pack_forget()
