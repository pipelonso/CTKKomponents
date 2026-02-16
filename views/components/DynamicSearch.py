import customtkinter
import tkinter
import difflib
from typing import Union, Tuple, Optional, Any
from customtkinter import CTkFont

from views.components.DynamicSearchItem import DynamicSearchItem


class DynamicSearch:
    general_frame = None
    accuracy = 80
    text_variable = None
    input_text = None
    btn_search = None

    def __init__(self,
                 master: Any,
                 general_border_radius: Optional[int] = 2,
                 show_search_bar: Optional[bool] = True,
                 search_on_write: Optional[bool] = False,
                 show_search_button: Optional[bool] = True,
                 search_button_text: Optional[str] = '🔎',
                 search_bar_corner_radius: Optional[int] = 2,
                 search_button_corner_radius: Optional[int] = 2,
                 search_button_position: Optional[str] = 'right',  # options: left, right
                 search_button_border_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'black'),
                 search_button_border_width: Optional[int] = 0,
                 search_bar_border_width: Optional[int] = 0,
                 search_bar_border_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'black'),
                 search_button_hover_color: Optional[Union[str, Tuple[str, str]]] = ('white', 'gray'),
                 accuracy_percentage: Optional[int] = 90,  # minimum 0 maximum 100,
                 search_bar_fg_color: Optional[Union[str, Tuple[str, str]]] = ('gray', 'black'),
                 search_bar_bg_color: Optional[Union[str, Tuple[str, str]]] = ('gray', 'black'),
                 search_button_fg_color: Optional[Union[str, Tuple[str, str]]] = ('gray', 'black'),
                 search_button_bg_color: Optional[Union[str, Tuple[str, str]]] = ('gray', 'black'),
                 border_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'white'),
                 border_width: Optional[int] = 1,
                 placeholder_text: Union[str, None] = None,
                 font: Optional[Union[tuple, CTkFont]] = None,
                 state: str = tkinter.NORMAL,
                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 width: int = 140,
                 height: int = 28,
                 text_variable: Union[tkinter.Variable, None] = None,
                 search_button_text_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'white'),
                 search_bar_text_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'white'),
                 search_button_height: Optional[int] = 28,
                 search_button_width: Optional[int] = 100,
                 search_bar_height: Optional[int] = 28,
                 search_bar_width: Optional[int] = 140,
                 placeholder_text_color: Optional[Union[str, Tuple[str, str]]] = ('white', 'gray'),
                 ):

        self.secure_list = []
        self.dynamic_list = []
        self.accuracy = accuracy_percentage

        gen_frame = customtkinter.CTkFrame(master, fg_color='transparent',
                                           height=height,
                                           width=width)
        self.general_frame = gen_frame

        base_frame = customtkinter.CTkFrame(gen_frame, fg_color=border_color,
                                            corner_radius=general_border_radius,
                                            bg_color=bg_color,
                                            height=height,
                                            width=width)

        base_frame.pack(padx=0, pady=0, fill='both', expand=True)

        input_frame = customtkinter.CTkFrame(base_frame,
                                             corner_radius=search_bar_corner_radius,
                                             fg_color=search_bar_border_color,
                                             bg_color='transparent',
                                             height=height)

        search_button_frame = customtkinter.CTkFrame(base_frame,
                                                     corner_radius=search_button_corner_radius,
                                                     fg_color=search_button_border_color,
                                                     bg_color='transparent',
                                                     height=height)

        if search_button_position == 'left':
            if show_search_bar:
                input_frame.pack(padx=border_width, pady=border_width, fill='x', side='right', expand=True)
            if show_search_button:
                search_button_frame.pack(padx=border_width, pady=border_width, fill='both', side='left')
        else:
            if show_search_bar:
                input_frame.pack(padx=border_width, pady=border_width, fill='x', side='left', expand=True)
            if show_search_button:
                search_button_frame.pack(padx=border_width, pady=border_width, fill='both', side='right')
        pass

        btn_search = customtkinter.CTkButton(search_button_frame, text=search_button_text,
                                             corner_radius=search_button_corner_radius,
                                             fg_color=search_button_fg_color,
                                             bg_color=search_button_bg_color,
                                             font=font,
                                             hover_color=search_button_hover_color,
                                             state=state,
                                             text_color=search_button_text_color,
                                             height=search_button_height,
                                             width=search_button_width,
                                             command=self.execute_search)

        self.btn_search = btn_search

        btn_search.pack(padx=search_button_border_width, pady=search_button_border_width, fill='both', expand=True)

        input_text = customtkinter.CTkEntry(input_frame, corner_radius=search_bar_corner_radius,
                                            placeholder_text=placeholder_text,
                                            fg_color=search_bar_fg_color,
                                            bg_color=search_bar_bg_color,
                                            font=font,
                                            border_width=0,
                                            state=state,
                                            textvariable=text_variable,
                                            text_color=search_bar_text_color,
                                            height=search_bar_height,
                                            width=search_bar_width,
                                            placeholder_text_color=placeholder_text_color
                                            )

        self.input_text = input_text

        input_text.pack(padx=search_bar_border_width, pady=search_bar_border_width, fill='both', expand=True)
        if search_on_write:
            self.register_binding()

    def pack(self, **kwargs):
        self.general_frame.pack(**kwargs)
        pass

    def place(self, **kwargs):
        self.general_frame.place(**kwargs)

    def register_binding(self):
        self.input_text.bind('<KeyRelease>', self.execute_bind)
        pass

    def execute_bind(self, event):
        self.execute_search()
        pass

    def execute_search(self):
        if len(self.secure_list) > 0:
            search_per_word = True
            if search_per_word == '' or search_per_word == '0':
                self.accuracy = 80
                for i in self.secure_list:
                    find_words = self.input_text.get().split(' ')
                    words = i.text.split('_')
                    ratio = 0
                    for w in words:
                        for f in find_words:
                            matcher = difflib.SequenceMatcher(None, f, w)
                            current_ratio = matcher.ratio()

                            if ratio < current_ratio:
                                ratio = current_ratio

                    if ratio * 100 < self.accuracy:
                        if i.component is not None:
                            if i.component.winfo_exists():
                                i.component.pack_forget()

                    if ratio * 100 >= self.accuracy:
                        if i.component is not None:
                            if i.component.winfo_exists():
                                i.component.pack(**i.get_pack_props())

                    if ratio * 100 == 0:
                        if i.component is not None:
                            if i.component.winfo_exists():
                                i.component.pack(**i.get_pack_props())
            else:
                for i in self.secure_list:
                    find_word = self.input_text.get().lower()

                    contains = i.text.lower().find(find_word)

                    if contains > -1 or find_word == '':
                        if i.component is not None:
                            if i.component.winfo_exists():
                                i.component.pack(**i.get_pack_props())
                    if contains < 0 and find_word != '':
                        if i.component is not None:
                            if i.component.winfo_exists():
                                i.component.pack_forget()
                pass

        pass

    def register_item(self, item: DynamicSearchItem):
        self.secure_list.append(item)

    def delete_item(self, item: DynamicSearchItem):
        rational_list = []
        for i in self.secure_list:
            if i != item:
                rational_list.append(i)

        self.secure_list = rational_list

    def delete_item_by_component(self, component):
        rational_list = []
        for i in self.secure_list:
            if i.component != component:
                rational_list.append(i)

        self.secure_list = rational_list

