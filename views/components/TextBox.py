import customtkinter
from typing import Optional, Union, Tuple, Any
from customtkinter import CTkFont

# CustomTkinter bugfix class -- text_color now accept tuple


class TextBox(customtkinter.CTkTextbox):

    def __init__(self, master: Any,
                 text_color: Optional[Union[str, Tuple[str, str]]] = None,
                 width: int = 200,
                 height: int = 200,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,
                 border_spacing: int = 3,
                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 scrollbar_button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 scrollbar_button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 font: Optional[Union[tuple, CTkFont]] = None,
                 activate_scrollbars: bool = True,
                 **kwargs):
        super().__init__(master,
                         text_color=text_color,
                         width=width,
                         height=height,
                         corner_radius=corner_radius,
                         border_spacing=border_spacing,
                         border_width=border_width,
                         bg_color=bg_color,
                         fg_color=fg_color,
                         border_color=border_color,
                         scrollbar_button_color=scrollbar_button_color,
                         scrollbar_button_hover_color=scrollbar_button_hover_color,
                         font=font,
                         activate_scrollbars=activate_scrollbars,
                         **kwargs)
