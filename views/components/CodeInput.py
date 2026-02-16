import customtkinter
from typing import Any
from pygments.lexers import get_lexer_by_name
from pygments.styles import get_style_by_name, get_all_styles
from typing import Optional, Union, Tuple


class CodeInput:

    def __init__(self, master: Any,
                 language: str = 'python',
                 theme: str = '',
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 wrap: Optional[str] = 'none',
                 width: Optional[int] = 100,
                 height: Optional[int] = 100,
                 corner_radius: Optional[int] = None,
                 border_width: Optional[int] = None,
                 border_spacing: int = 3,
                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 border_color: Optional[Union[str, Tuple[str, str]]] = None,
                 text_color: Optional[Union[str, str]] = None,
                 scrollbar_button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 scrollbar_button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 ):

        self.master = master
        self.entry = customtkinter.CTkTextbox(self.master,
                                              wrap=wrap,
                                              fg_color=fg_color,
                                              width=width,
                                              height=height,
                                              corner_radius=corner_radius,
                                              border_width=border_width,
                                              border_spacing=border_spacing,
                                              bg_color=bg_color,
                                              border_color=border_color,
                                              text_color=text_color,
                                              scrollbar_button_color=scrollbar_button_color,
                                              scrollbar_button_hover_color=scrollbar_button_hover_color
                                              )
        self.theme = None
        self.language = language

        self.update_ignore_keys = [
            'BackSpace', 'Return', 'space', 'Tab', 'Home', 'End', 'Shift_L', 'Shift_R',
            'Right', 'Down', 'Left', 'Up', 'Control_L', 'Control_R'
        ]

        self.code_trail = ''

        if theme == '':
            theme = 'monokai'

        self.theme = get_style_by_name(theme)
        self.theme.list_styles()
        self.distribute_theme()

        self.register_bind()

    def register_bind(self):
        self.entry.bind("<KeyRelease>", self.key_release)

    def key_release(self, event):
        if event.keysym not in self.update_ignore_keys:
            self.generate_code_highlight()
        pass

    def place(self, **kwargs):
        self.entry.place(**kwargs)

    def pack(self, **kwargs):
        self.entry.pack(**kwargs)

    def distribute_theme(self):
        for key in self.theme:
            if key[1]["color"] != "" and key[1]["color"] is not None:
                color = "#" + key[1]["color"]
                self.entry.tag_config(str(key[0]), foreground=color)

    def generate_code_highlight(self):
        cursor_position = self.entry.index("insert")

        self.code_trail = self.entry.get('1.0', customtkinter.END)

        if self.code_trail.endswith("\n"):
            self.code_trail = self.code_trail[:-1]

        self.entry.delete('1.0', customtkinter.END)

        lexer = get_lexer_by_name(self.language, stripall=True)
        tokens = list(lexer.get_tokens(self.code_trail))

        for text in tokens:
            self.entry.insert("end", text[1], str(text[0]))

        self.entry.mark_set("insert", cursor_position)

    def register_code(self, code: str):
        self.code_trail = code
        self.entry.delete('1.0', customtkinter.END)
        self.entry.insert("1.0", self.code_trail)
        self.generate_code_highlight()

    def freeze_editor(self):
        self.entry.configure(state='disabled')

    def unfreeze_editor(self):
        self.entry.configure(state='normal')

    def set_theme_color(self, theme: str):
        self.theme = get_style_by_name(theme)
        self.theme.list_styles()
        self.distribute_theme()
        self.generate_code_highlight()
        pass

    @staticmethod
    def get_all_editor_styles():
        return list(get_all_styles())

    def clear_editor(self):
        self.entry.delete('1.0', customtkinter.END)
        pass
