import tkinter
import customtkinter
from typing import Union, Tuple, Optional, Any
from customtkinter import CTkFont, CTkImage


class ResponsiveLabel(customtkinter.CTkLabel):

    master = None

    def __init__(self, master: Any, width: int = 0, height: int = 28, corner_radius: Optional[int] = None,
                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None, text: str = "ResponsiveLabel",
                 font: Optional[Union[tuple, CTkFont]] = None, image: Union[CTkImage, None] = None,
                 compound: str = "center", anchor: str = "center", wraplength: int = 300, **kwargs):

        self.master = master
        self.master.bind('<Configure>', self.on_configure)

        super().__init__(master, width, height, corner_radius, bg_color, fg_color, text_color, text_color_disabled,
                         text, font, image, compound, anchor, wraplength, **kwargs)

    def on_configure(self, event):
        if hasattr(self, "_label"):
            self.configure(wraplength=self.master.winfo_width())
        pass
