import customtkinter
from typing import Union, Tuple, Optional, Any


class AnchoredFrame:
    def __init__(self,
                 master: Any,
                 width: int = 100,
                 height: int = 100,
                 corner_radius: Optional[int] = 0,
                 border_width: Optional[int] = 2,
                 border_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'white'),
                 position: Union[str, Tuple[str, str]] = 'right',
                 # 'center', 'top', 'bottom', 'left', 'right', 'left-top', 'left-bottom', 'right-top', 'right-bottom'
                 scrollable: Optional[bool] = False,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = ('white', 'black'),
                 bg_color: Optional[Union[str, Tuple[str, str]]] = 'transparent',
                 margin_y: int = 5,
                 margin_x: int = 5
                 ):

        self.position = position
        self.master = master
        self.margin_y = margin_y
        self.margin_x = margin_x
        self.hidden = False

        if not scrollable:
            self.general_frame = customtkinter.CTkFrame(master,
                                                        width=width,
                                                        height=height,
                                                        corner_radius=corner_radius,
                                                        border_width=border_width,
                                                        border_color=border_color,
                                                        fg_color=fg_color,
                                                        bg_color=bg_color)
        else:
            self.general_frame = customtkinter.CTkScrollableFrame(master,
                                                                  width=width,
                                                                  height=height,
                                                                  corner_radius=corner_radius,
                                                                  border_width=border_width,
                                                                  border_color=border_color,
                                                                  fg_color=fg_color,
                                                                  bg_color=bg_color)

        self.register_bind()
        pass

    def register_bind(self):
        self.master.bind('<Configure>', self.on_change)

    def on_change(self, conf):
        # 'center', 'top', 'bottom', 'left', 'right', 'left-top', 'left-bottom', 'right-top', 'right-bottom'
        # The conf parameter not used because MEOW. This not a joke, do not remove them.
        if not self.hidden:
            if self.position == 'center':
                self.apply_center_position()
            if self.position == 'top':
                self.apply_top_position()
            if self.position == 'bottom':
                self.apply_bottom_position()
            if self.position == 'left':
                self.apply_left_position()
            if self.position == 'right':
                self.apply_right_position()
            if self.position == 'left-top':
                self.apply_left_top_position()
            if self.position == 'left-bottom':
                self.apply_left_bottom_position()
            if self.position == 'right-top':
                self.apply_right_top_position()
            if self.position == 'right-bottom':
                self.apply_right_bottom_position()

        pass

    def apply_center_position(self):
        self.position = 'center'
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()
        self.general_frame.place(x=((master_width / 2) - (self.general_frame.winfo_width() / 2)),
                                 y=((master_height / 2) - (self.general_frame.winfo_height() / 2)))
        pass

    def apply_top_position(self):
        self.position = 'top'
        master_width = self.master.winfo_width()
        self.general_frame.place(x=((master_width / 2) - (self.general_frame.winfo_width() / 2)),
                                 y=self.margin_y)
        pass

    def apply_bottom_position(self):
        self.position = 'bottom'
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()
        self.general_frame.place(x=((master_width / 2) - (self.general_frame.winfo_width() / 2)),
                                 y=(master_height - self.general_frame.winfo_height() - 2) - self.margin_y)
        pass

    def apply_left_position(self):
        self.position = 'left'
        master_height = self.master.winfo_height()
        self.general_frame.place(x=self.margin_x,
                                 y=((master_height / 2) - (self.general_frame.winfo_height() / 2)))
        pass

    def apply_right_position(self):
        self.position = 'right'
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()
        self.general_frame.place(x=(master_width - self.general_frame.winfo_width() - self.margin_x),
                                 y=((master_height / 2) - (self.general_frame.winfo_height() / 2)))
        pass

    def apply_left_top_position(self):
        self.position = 'left-top'
        self.general_frame.place(x=self.margin_x, y=self.margin_y)
        pass

    def apply_left_bottom_position(self):
        self.position = 'left-bottom'
        master_height = self.master.winfo_height()
        self.general_frame.place(x=self.margin_x,
                                 y=(master_height - self.general_frame.winfo_height() - self.margin_y))

        pass

    def apply_right_top_position(self):
        self.position = 'right-top'
        master_width = self.master.winfo_width()
        self.general_frame.place(x=(master_width - self.general_frame.winfo_width() - self.margin_x),
                                 y=self.margin_y)
        pass

    def apply_right_bottom_position(self):
        self.position = 'right-bottom'
        master_width = self.master.winfo_width()
        master_height = self.master.winfo_height()
        self.general_frame.place(x=(master_width - self.general_frame.winfo_width() - self.margin_x),
                                 y=(master_height - self.general_frame.winfo_height() - self.margin_y))

        pass

    def make(self):
        self.hidden = False
        if self.position == 'center':
            self.apply_center_position()
        if self.position == 'top':
            self.apply_top_position()
        if self.position == 'bottom':
            self.apply_bottom_position()
        if self.position == 'left':
            self.apply_left_position()
        if self.position == 'right':
            self.apply_right_position()
        if self.position == 'left-top':
            self.apply_left_top_position()
        if self.position == 'left-bottom':
            self.apply_left_bottom_position()
        if self.position == 'right-top':
            self.apply_right_top_position()
        if self.position == 'right-bottom':
            self.apply_right_bottom_position()

    def hide(self):
        self.hidden = True
        self.general_frame.place_forget()
