import os
from io import StringIO
from pathlib import Path
import customtkinter
from customtkinter import CTkToplevel
import tkinter
from typing import Union, Tuple, Callable, Optional, Any
import threading


class FileExplorer:

    def __init__(self,
                 master: Optional[Any] = None,
                 top_level: bool = True,
                 title: Optional[str] = 'Select files',
                 fg_color: Optional[Union[str, Tuple[str, str]]] = ('#ecf0f1', '#2c3e50'),
                 initial_dir: str | None = None,
                 select_button_text: Optional[str] = 'Select',
                 mode: Optional[str] = 'file'  # file, folder
                 ):

        if mode != 'file' and mode != 'folder':
            raise Exception(f'File explorer mode not valid "{mode}", use one [file, folder] keywords')

        if master is not None and top_level:
            # TopLevel definitions
            win = CTkToplevel(fg_color=fg_color)
            win.title(title)
            win.grab_set()
            win.focus_force()
        else:
            win = master

        self.master = win

        sup_bar = customtkinter.CTkFrame(win)
        sup_bar.pack(padx=2, pady=2, fill='x')

        return_button = customtkinter.CTkButton(sup_bar, text='◀', width=30)
        return_button.pack(padx=2, pady=2, side=tkinter.LEFT)

        self.search_input_var = customtkinter.Variable()

        self.search_input = customtkinter.CTkEntry(sup_bar, textvariable=self.search_input_var)
        self.search_input.pack(padx=2, pady=2, fill='x', side=tkinter.RIGHT, expand=True)

        self.selector_frame = customtkinter.CTkScrollableFrame(win)
        self.selector_frame.pack(padx=2, pady=2, fill='both', expand=True)

        control_frame = customtkinter.CTkFrame(win)
        control_frame.pack(padx=2, pady=2, fill='x')

        accept_button = customtkinter.CTkButton(control_frame, text=select_button_text)
        accept_button.pack(padx=2, pady=2, fill='y', side=tkinter.RIGHT)

        self.path_to_load = os.path.expanduser('~')

        if initial_dir is not None:
            if not os.path.exists(initial_dir):
                raise Exception(f'The path "{initial_dir}" does not exists')
                pass
            else:
                self.path_to_load = initial_dir

        general_list = self.get_general_list_from_specific_folder(self.path_to_load)
        self.render_file_and_folder_trail(general_list)

        pass

    @staticmethod
    def get_folder_list_from_specific_path(path):
        ruta_path = Path(path)
        directories = [d.name for d in ruta_path.iterdir() if d.is_dir()]
        return directories

    @staticmethod
    def get_file_list_from_specific_folder(path):
        ruta_path = Path(path)
        files = [d.name for d in ruta_path.iterdir() if d.is_file()]
        return files

    @staticmethod
    def get_general_list_from_specific_folder(path):
        ruta_path = Path(path)
        files = [(d.name, d.is_file()) for d in ruta_path.iterdir()]
        return files

    @staticmethod
    def start_threat(method):
        thread_method = threading.Thread(target=method)
        thread_method.start()
        pass

    def render_file_and_folder_trail(self, folder_general_list: list):

        winfo_width = self.master.winfo_width()
        print(winfo_width)

        for file_folder in folder_general_list:

            icon = '📂'
            if file_folder[1]:
                icon = '📦'

            frame = customtkinter.CTkFrame(self.selector_frame, border_color=('black', 'white'), border_width=3, fg_color='transparent')
            selector_button = customtkinter.CTkButton(frame,
                                                      text=(icon + ' ' + str(file_folder[0])),
                                                      command=lambda e=file_folder:  self.resolve_open_folder(e[0]),
                                                      fg_color='transparent'
                                                      )
            selector_button.pack(padx=2, pady=2, fill='x', expand=True)
            frame.pack(padx=2, pady=2, fill='x', expand=True)

    def resolve_open_folder(self, folder_name: str):
        if isinstance(self.master, customtkinter.CTkFrame) or isinstance(self.master, CTkToplevel):

            path = os.path.join(self.path_to_load, folder_name)
            self.path_to_load = path
            self.search_input_var.set(path)
            general_folder_list = self.get_general_list_from_specific_folder(path)

            for i in self.selector_frame.winfo_children():
                i.destroy()

            self.render_file_and_folder_trail(general_folder_list)

        pass
    pass

