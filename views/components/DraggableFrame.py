import time
from typing import Union, Tuple, Optional, Any
import tkinter
import customtkinter
import pyautogui
from views.components import DragableFrameAdministrator
from customtkinter import CTkFont


class DraggableFrame:
    self_button = None
    self_master = None
    border = None
    content_frame = None
    close_button = None
    self_width = 0
    self_height = 0
    align_options_button = None
    align_controls_panel = None
    custom_position = 'center'
    administrator = None
    draggable = True
    opened = False
    resizable = False
    corner = None
    scrollable = False
    anchored = False
    on_close_function = None

    def __init__(self,
                 master: Any,
                 width: int = 600,
                 height: int = 30,
                 window_border_radius: Optional[int] = 0,
                 content_border_radius: Optional[int] = 0,
                 border_width: Optional[int] = 2,
                 header_bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 border_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'white'),
                 header_color: Optional[Union[str, Tuple[str, str]]] = ('white', 'black'),
                 header_radius: Optional[int] = 0,
                 title: Optional[str] = "",
                 title_color: Optional[Union[str, Tuple[str, str]]] = None,
                 hover_header_color: Optional[Union[str, Tuple[str, str]]] = None,
                 content_height: Optional[int] = 200,
                 add_close_button: Optional[bool] = True,
                 is_scrollable: Optional[bool] = False,
                 custom_position: Union[str, Tuple[str, str]] = 'center',
                 # tuple(x,y) or 'center' , 'top' , 'bottom' , 'left' , 'right' , 'left-top' , 'left-bottom' , 'right-top' , 'right-bottom'
                 close_button_color: Optional[Union[str, Tuple[str, str]]] = None,
                 close_button_border_radius: Optional[int] = 0,
                 close_button_hover_color: Optional[Union[str, Tuple[str, str]]] = None,
                 control_buttons_padding: Optional[int] = 0,
                 administrator: Optional[DragableFrameAdministrator.DraggableFrameAdministrator] = None,
                 draggable: Optional[bool] = True,
                 show_align_options: Optional[bool] = True,
                 header_padding_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'white'),
                 header_padding_border_radius: Optional[int] = 0,
                 resizable: Optional[bool] = False,
                 drag_cursor: Optional[str] = 'fleur',
                 resize_corner_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'white'),
                 # Cursors
                 # "arrow", "circle", "clock", "cross", "dotbox", "exchange", "fleur",
                 # "heart", "man", "mouse", "pirate", "plus", "shuttle", "sizing",
                 # "spider", "spraycan", "star", "target", "tcross", "trek", "watch", "xterm"
                 font: Optional[Union[tuple, CTkFont]] = None,
                 align_options_button_fg_color: Optional[Union[str, Tuple[str, str]]] = ('#e5efe5', '#111211'),
                 align_options_button_text_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'white'),
                 align_options_button_hover_color: Optional[Union[str, Tuple[str, str]]] = 'gray',
                 align_options_button_corner_radius: Optional[int] = 0,
                 on_close_function=None
                 ):

        self.on_close_function = on_close_function
        self.administrator = administrator
        self.self_width = width
        self.self_height = height
        self.draggable = draggable
        self.opened = False
        self.resizable = resizable
        self.scrollable = is_scrollable

        self.anchored = isinstance(custom_position, str)

        if isinstance(self.administrator, DragableFrameAdministrator.DraggableFrameAdministrator):
            DragableFrameAdministrator.DraggableFrameAdministrator.register_window(self)

        self.custom_position = custom_position

        border_frame = customtkinter.CTkFrame(master, fg_color=border_color, corner_radius=window_border_radius,
                                              bg_color='transparent')

        self.border = border_frame

        self.self_master = master

        header_frame = customtkinter.CTkFrame(border_frame, fg_color=header_padding_color,
                                              corner_radius=header_padding_border_radius)
        header_frame.pack(pady=border_width, padx=border_width, side=tkinter.TOP)
        self.header = header_frame
        header_button = customtkinter.CTkButton(header_frame, text=title, width=width, height=height,
                                                fg_color=header_color,
                                                text_color=title_color,
                                                hover_color=hover_header_color,
                                                corner_radius=header_radius,
                                                bg_color=header_bg_color,
                                                command=self.remap_z_index,
                                                font=font)

        header_button.configure(cursor=drag_cursor)

        align_button_place = header_frame if height > 25 else self.border
        align_options_button = customtkinter.CTkButton(align_button_place, fg_color=align_options_button_fg_color, text='≣',
                                                       corner_radius=align_options_button_corner_radius, bg_color='transparent',
                                                       hover_color=align_options_button_hover_color,
                                                       height=height,
                                                       width=height,
                                                       command=lambda: self.generate_adjust_controls(
                                                           place='top-left' if height > 25 else 'bottom'),
                                                       text_color=align_options_button_text_color)

        self.align_options_button = align_options_button

        if show_align_options:

            if align_button_place is header_frame:
                align_options_button.pack(padx=control_buttons_padding, pady=control_buttons_padding, side=tkinter.LEFT)
            else:
                align_options_button.pack(padx=control_buttons_padding, pady=control_buttons_padding,
                                          side=tkinter.BOTTOM, fill='x', expand=True)
                pass

        header_button.pack(pady=0, padx=0, side=tkinter.LEFT)
        header_button.bind('<B1-Motion>', self.on_motion)
        self.self_button = header_button

        if add_close_button:

            close_button_place = header_frame if height > 25 else self.border

            close_button = customtkinter.CTkButton(close_button_place, text="x", font=("Arial", 18), height=height,
                                                   width=height, command=self.destroy_window,
                                                   fg_color=close_button_color,
                                                   corner_radius=close_button_border_radius,
                                                   hover_color=close_button_hover_color)

            if height > 25:
                close_button.pack(side=tkinter.RIGHT, padx=control_buttons_padding, pady=control_buttons_padding)
            else:
                close_button.pack(side=tkinter.BOTTOM, padx=control_buttons_padding, pady=control_buttons_padding,
                                  fill='x', expand=True)
                pass

            self.close_button = close_button

        if not is_scrollable:
            content_frame = customtkinter.CTkFrame(border_frame, fg_color=fg_color, corner_radius=content_border_radius,
                                                   height=content_height)
            content_frame.pack(padx=border_width, pady=border_width, side=tkinter.BOTTOM, fill='both', expand=True)

            self.content_frame = content_frame
        else:
            content_frame = customtkinter.CTkScrollableFrame(border_frame, fg_color=fg_color,
                                                             corner_radius=content_border_radius,
                                                             height=content_height)
            content_frame.pack(padx=border_width, pady=border_width, side=tkinter.BOTTOM, fill='both', expand=True)

            self.content_frame = content_frame

        self.border.place(x=-90000, y=-90000)
        self.self_master.update()
        self.border.update()
        self.generate_adjust_controls(place='top-left')

        self.custom_position = custom_position

        if resizable:
            self.corner = customtkinter.CTkButton(self.self_master, text='', height=15, width=15,
                                                  fg_color=resize_corner_color,
                                                  corner_radius=0)

            self.corner.configure(cursor='sizing')
            self.corner.bind('<B1-Motion>', self.on_resize)
            self.corner.bind('<ButtonRelease>', self.on_left_drag)

        pass

    def on_left_drag(self, event):
        self.align_corner()
        pass

    def remap_z_index(self):
        if isinstance(self.administrator, DragableFrameAdministrator.DraggableFrameAdministrator):
            admin = DragableFrameAdministrator.DraggableFrameAdministrator
            admin.sort_windows(self)
            pass
        pass

    def on_resize(self, event):

        if not self.anchored:

            px_cursor = pyautogui.position().x - self.self_master.winfo_x()
            py_cursor = pyautogui.position().y - self.self_master.winfo_y()

            time.sleep(0.01)

            px_cursor_last = pyautogui.position().x - self.self_master.winfo_x()
            py_cursor_last = pyautogui.position().y - self.self_master.winfo_y()

            dif_x = px_cursor - self.corner.winfo_x()
            dif_y = py_cursor - self.corner.winfo_y()

            x_flipper = -1.3 if px_cursor > px_cursor_last else 1.3
            y_flipper = -1.3 if py_cursor > py_cursor_last else 1.3

            x_dis = (px_cursor - px_cursor_last) * x_flipper if px_cursor > px_cursor_last else (
                                                                                                        px_cursor_last - px_cursor) * x_flipper
            y_dis = (py_cursor - py_cursor_last) * y_flipper if py_cursor > py_cursor_last else (

                                                                                                        py_cursor_last - py_cursor) * y_flipper
            pre_current_x_corner_pos = self.border.winfo_width() + self.border.winfo_x()
            pre_current_y_corner_pos = self.border.winfo_height() + self.border.winfo_y()

            if (pre_current_x_corner_pos - self.corner.winfo_x() <= -1000 or pre_current_x_corner_pos - self.corner.winfo_x() >= 1000
                    or pre_current_y_corner_pos - self.corner.winfo_y() <= -1000 or pre_current_y_corner_pos - self.corner.winfo_y() >= 1000):
                self.align_corner()
            else:
                self.corner.place(x=(px_cursor - dif_x + x_dis),
                                  y=(py_cursor - dif_y + y_dis))

            current_x_corner_pos = self.border.winfo_width() + self.border.winfo_x()
            if current_x_corner_pos <= self.corner.winfo_x():
                self.self_button.configure(width=self.border.winfo_width() + (current_x_corner_pos - self.corner.winfo_x()))
                self.content_frame.configure(width=self.border.winfo_width() + (current_x_corner_pos - self.corner.winfo_x()))
            else:
                self.self_button.configure(width=self.border.winfo_width() - (current_x_corner_pos - self.corner.winfo_x()))
                self.content_frame.configure(width=self.border.winfo_width() - (current_x_corner_pos - self.corner.winfo_x()))

            if self.scrollable:
                current_y_corner_pos = self.border.winfo_height() + self.border.winfo_y()

                if current_y_corner_pos <= self.corner.winfo_y():
                    self.content_frame.configure(
                        height=self.border.winfo_height() + (current_y_corner_pos - self.corner.winfo_y()))
                else:
                    self.content_frame.configure(
                        height=self.border.winfo_height() - (current_y_corner_pos - self.corner.winfo_y()))

        pass

    def regenerate_position(self):
        pos = self.custom_position
        if isinstance(pos, str):
            if pos == 'center':
                self.apply_center_position()
            if pos == 'top':
                self.apply_top_position()
            if pos == 'left':
                self.apply_left_position()
            if pos == 'right':
                self.apply_right_position()
            if pos == 'bottom':
                self.apply_bottom_position()
            if pos == 'left-top':
                self.apply_left_top_position()
            if pos == 'left-bottom':
                self.apply_left_bottom_position()
            if pos == 'right-top':
                self.apply_right_top_position()
            if pos == 'right-bottom':
                self.apply_right_bottom_position()
        elif isinstance(pos, tuple):
            self.border.place(x=int(pos[0]), y=int(pos[1]))
        pass

    def generate_adjust_controls(self, place: Optional[str]):

        self.align_options_button.configure(state='disabled')

        adjustment_border_frame = customtkinter.CTkFrame(self.border, fg_color=('black', 'white'), corner_radius=0)

        self.align_controls_panel = adjustment_border_frame

        adjustment_frame = customtkinter.CTkFrame(adjustment_border_frame, corner_radius=0)
        adjustment_frame.pack(padx=1, pady=1)

        top_row_frame = customtkinter.CTkFrame(adjustment_frame, fg_color='transparent')
        top_row_frame.pack(padx=0, pady=0, fill='x', expand=True)

        btn_left_top = customtkinter.CTkButton(top_row_frame, height=10, width=10, text='◤',
                                               text_color=('black', 'white'),
                                               fg_color=('white', 'black'),
                                               corner_radius=0,
                                               hover_color='gray',
                                               font=('Arial', 8),
                                               command=self.apply_left_top_position)

        btn_left_top.pack(padx=0, pady=0, side=tkinter.LEFT)

        btn_top = customtkinter.CTkButton(top_row_frame, height=10, width=10, text='▲',
                                          text_color=('black', 'white'), fg_color=('white', 'black'),
                                          corner_radius=0,
                                          hover_color='gray',
                                          font=('Arial', 8),
                                          command=self.apply_top_position)

        btn_top.pack(padx=0, pady=0, side=tkinter.LEFT)

        btn_right_top = customtkinter.CTkButton(top_row_frame, height=10, width=10, text='◥',
                                                text_color=('black', 'white'), fg_color=('white', 'black'),
                                                corner_radius=0,
                                                hover_color='gray',
                                                font=('Arial', 8),
                                                command=self.apply_right_top_position)

        btn_right_top.pack(padx=0, pady=0, side=tkinter.RIGHT)

        center_row_frame = customtkinter.CTkFrame(adjustment_frame, fg_color='transparent')
        center_row_frame.pack(padx=0, pady=0, fill='x', expand=True)

        btn_left = customtkinter.CTkButton(center_row_frame, height=10, width=10, text='◂',
                                           text_color=('black', 'white'),
                                           fg_color=('white', 'black'),
                                           corner_radius=0,
                                           hover_color='gray',
                                           font=('Arial', 8),
                                           command=self.apply_left_position)

        btn_left.pack(padx=0, pady=0, side=tkinter.LEFT)

        btn_center = customtkinter.CTkButton(center_row_frame, height=10, width=10, text=' ▢ ',
                                             text_color=('black', 'white'), fg_color=('white', 'black'),
                                             corner_radius=0,
                                             hover_color='gray',
                                             font=('Arial', 8),
                                             command=self.apply_center_position)

        btn_center.pack(padx=0, pady=0, side=tkinter.LEFT)

        btn_right = customtkinter.CTkButton(center_row_frame, height=10, width=10, text='▸',
                                            text_color=('black', 'white'), fg_color=('white', 'black'),
                                            corner_radius=0,
                                            hover_color='gray',
                                            font=('Arial', 8),
                                            command=self.apply_right_position)

        btn_right.pack(padx=0, pady=0, side=tkinter.RIGHT)

        down_row_frame = customtkinter.CTkFrame(adjustment_frame, fg_color='transparent')
        down_row_frame.pack(padx=0, pady=0, fill='x', expand=True)

        btn_left_bottom = customtkinter.CTkButton(down_row_frame, height=10, width=10, text='◣',
                                                  text_color=('black', 'white'),
                                                  fg_color=('white', 'black'),
                                                  corner_radius=0,
                                                  hover_color='gray',
                                                  font=('Arial', 8),
                                                  command=self.apply_left_bottom_position)

        btn_left_bottom.pack(padx=0, pady=0, side=tkinter.LEFT)

        btn_center_bottom = customtkinter.CTkButton(down_row_frame, height=10, width=10, text='▼',
                                                    text_color=('black', 'white'), fg_color=('white', 'black'),
                                                    corner_radius=0,
                                                    hover_color='gray',
                                                    font=('Arial', 8),
                                                    command=self.apply_bottom_position)

        btn_center_bottom.pack(padx=0, pady=0, side=tkinter.LEFT)

        btn_right_bottom = customtkinter.CTkButton(down_row_frame, height=10, width=10, text='◢',
                                                   text_color=('black', 'white'), fg_color=('white', 'black'),
                                                   corner_radius=0,
                                                   hover_color='gray',
                                                   font=('Arial', 8),
                                                   command=self.apply_right_bottom_position)

        btn_right_bottom.pack(padx=0, pady=0, side=tkinter.RIGHT)

        if place == 'top-left':
            adjustment_border_frame.place(x=5, y=self.self_height + 7)
        elif place == 'bottom':
            adjustment_border_frame.place(x=self.content_frame.winfo_width() / 2, y=self.border.winfo_height() - 75)
            self.self_master.update()
            adjustment_border_frame.place(
                x=((self.content_frame.winfo_width() / 2) - (adjustment_border_frame.winfo_width() / 3)),
                y=(self.border.winfo_height() - 75))

        pass

    def on_motion(self, event):
        if self.draggable:

            self.anchored = False

            self.align_options_button.configure(state='enabled')
            px_cursor = pyautogui.position().x - self.self_master.winfo_x()
            py_cursor = pyautogui.position().y - self.self_master.winfo_y()

            time.sleep(0.01)

            px_cursor_last = pyautogui.position().x - self.self_master.winfo_x()
            py_cursor_last = pyautogui.position().y - self.self_master.winfo_y()

            dif_x = px_cursor - self.border.winfo_x()
            dif_y = py_cursor - self.border.winfo_y()

            x_flipper = -1.37 if px_cursor > px_cursor_last else 1.37
            y_flipper = -1.37 if py_cursor > py_cursor_last else 1.37

            x_dis = (px_cursor - px_cursor_last) * x_flipper if px_cursor > px_cursor_last else (
                                                                                                        px_cursor_last - px_cursor) * x_flipper
            y_dis = (py_cursor - py_cursor_last) * y_flipper if py_cursor > py_cursor_last else (
                                                                                                        py_cursor_last - py_cursor) * y_flipper

            self.border.place(x=(px_cursor - dif_x + x_dis),
                              y=(py_cursor - dif_y + y_dis))

            self.custom_position = ((px_cursor - dif_x + x_dis), (py_cursor - dif_y + y_dis))

            self.align_corner()

        pass

    def configure(self,
                  width: Optional[int] = None,
                  custom_position: Union[str, Tuple[str, str]] = custom_position,
                  drag_cursor: Optional[str] = 'fleur'
                  ):

        if width is not None:
            self.configure_width(width)

        if custom_position is not self.custom_position:
            self.assign_new_generation_position(pos=custom_position)

        self.self_button.configure(cursor=drag_cursor)

        pass

    def assign_new_generation_position(self, pos):
        self.custom_position = pos

    def configure_width(self, width):
        self.self_button.configure(width=width)

    def apply_center_position(self):
        self.align_options_button.configure(state='disabled')
        self.custom_position = 'center'
        master_width = self.self_master.winfo_width()
        master_height = self.self_master.winfo_height()
        self.border.place(x=((master_width / 2) - (self.border.winfo_width() / 2)),
                          y=((master_height / 2) - (self.border.winfo_height() / 2)))

        self.align_options_button.configure(state='enabled')
        self.align_controls_panel.destroy()

        self.align_corner()
        self.anchored = True
        pass

    def apply_top_position(self):
        self.align_options_button.configure(state='disabled')
        self.custom_position = 'top'
        master_width = self.self_master.winfo_width()
        self.border.place(x=((master_width / 2) - (self.border.winfo_width() / 2)),
                          y=5)
        self.align_options_button.configure(state='enabled')
        self.align_controls_panel.destroy()

        self.align_corner()
        self.anchored = True
        pass

    def apply_bottom_position(self):
        self.align_options_button.configure(state='disabled')
        self.custom_position = 'bottom'
        master_width = self.self_master.winfo_width()
        master_height = self.self_master.winfo_height()
        self.border.place(x=((master_width / 2) - (self.border.winfo_width() / 2)),
                          y=(master_height - self.border.winfo_height() - 2) - 5)
        self.align_options_button.configure(state='enabled')
        self.align_controls_panel.destroy()

        self.align_corner()
        self.anchored = True
        pass

    def apply_left_position(self):
        self.align_options_button.configure(state='disabled')
        self.custom_position = 'left'
        master_height = self.self_master.winfo_height()
        self.border.place(x=5,
                          y=((master_height / 2) - (self.border.winfo_height() / 2)))
        self.align_options_button.configure(state='enabled')
        self.align_controls_panel.destroy()

        self.align_corner()
        self.anchored = True
        pass

    def apply_right_position(self):
        self.align_options_button.configure(state='disabled')
        self.custom_position = 'right'
        master_width = self.self_master.winfo_width()
        master_height = self.self_master.winfo_height()
        self.border.place(x=(master_width - self.border.winfo_width() - 5),
                          y=((master_height / 2) - (self.border.winfo_height() / 2)))
        self.align_options_button.configure(state='enabled')
        self.align_controls_panel.destroy()

        self.align_corner()
        self.anchored = True
        pass

    def apply_left_top_position(self):
        self.align_options_button.configure(state='disabled')
        self.custom_position = 'left-top'
        self.border.place(x=5, y=5)
        self.align_options_button.configure(state='enabled')
        self.align_controls_panel.destroy()

        self.align_corner()
        self.anchored = True
        pass

    def apply_left_bottom_position(self):
        self.align_options_button.configure(state='disabled')
        self.custom_position = 'left-bottom'
        master_height = self.self_master.winfo_height()
        self.border.place(x=5,
                          y=(master_height - self.border.winfo_height() - 5))
        self.align_options_button.configure(state='enabled')
        self.align_controls_panel.destroy()

        self.align_corner()
        self.anchored = True
        pass

    def apply_right_top_position(self):
        self.align_options_button.configure(state='disabled')
        self.custom_position = 'right-top'
        master_width = self.self_master.winfo_width()
        self.border.place(x=(master_width - self.border.winfo_width() - 5),
                          y=5)
        self.align_options_button.configure(state='enabled')
        self.align_controls_panel.destroy()

        self.align_corner()
        self.anchored = True
        pass

    def apply_right_bottom_position(self):
        self.align_options_button.configure(state='disabled')
        self.custom_position = 'right-bottom'
        master_width = self.self_master.winfo_width()
        master_height = self.self_master.winfo_height()
        self.border.place(x=(master_width - self.border.winfo_width() - 5),
                          y=(master_height - self.border.winfo_height() - 5))
        self.align_options_button.configure(state='enabled')
        self.align_controls_panel.destroy()

        self.align_corner()
        self.anchored = True
        pass

    def on_death_function(self):
        if self.on_close_function is not None:
            return self.on_close_function()
        else:
            return None

    def destroy_window(self):
        if self.on_close_function is not None:
            self.on_death_function()
        if self.administrator is not None:
            self.administrator.left_window(self)

            for window in self.administrator.window_list:
                if window.self_master == self.content_frame:
                    self.administrator.left_window(window)

        self.border.destroy()

        if self.resizable:
            self.corner.destroy()

    def hide_window(self):
        self.opened = False
        self.border.place_forget()

    def open_window(self):
        custom_position = self.custom_position
        self.opened = True
        if isinstance(custom_position, tuple):
            self.border.place(x=int(custom_position[0]), y=int(custom_position[1]))

        elif isinstance(custom_position, str):
            if custom_position == 'center':
                self.apply_center_position()
            elif custom_position == 'top':
                self.apply_top_position()
            elif custom_position == 'bottom':
                self.apply_bottom_position()
            elif custom_position == 'left':
                self.apply_left_position()
            elif custom_position == 'right':
                self.apply_right_position()
            elif custom_position == 'left-top':
                self.apply_left_top_position()
            elif custom_position == 'left-bottom':
                self.apply_left_bottom_position()
            elif custom_position == 'right-top':
                self.apply_right_top_position()
            elif custom_position == 'right-bottom':
                self.apply_right_bottom_position()
            else:
                self.apply_center_position()

            self.self_master.update()
            self.border.update()

            self.align_corner()

    def align_corner(self):
        if self.resizable:
            self.corner.place(y=((self.border.winfo_height() + self.border.winfo_y()) - 13),
                              x=((self.border.winfo_width() + self.border.winfo_x()) - 13))

    def get_window_height(self):
        return self.self_height

    def get_window_width(self):
        return self.self_width

    def get_window_pos(self) -> Tuple[int, int]:
        return self.border.winfo_x(), self.border.winfo_y()
