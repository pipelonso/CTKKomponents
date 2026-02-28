from views.components.CanvasButton import CanvasButton
from typing import Any
from PIL import Image, ImageTk


class CanvasInGlowingButton:
    def __init__(self,
                 master: Any,
                 click_order=None,
                 enter_order=None,
                 leave_order=None,
                 text: str = '',
                 width=35,
                 height=40,
                 text_y=0
                 ):
        self.corner_radius_ul = 0
        self.corner_radius_ur = 0
        self.corner_radius_dl = 0
        self.corner_radius_dr = 0
        self.text_y = text_y
        self._canvas_img_list = []

        image_path_glow_64 = "views/components/glow_64.png"
        image_glow_64 = Image.open(image_path_glow_64)
        self.image_glow_64 = image_glow_64.resize((120, 120))
        self.glowing_photo = ImageTk.PhotoImage(self.image_glow_64)
        self._canvas_img_list.append(self.glowing_photo)

        self.click_command = click_order
        self.enter_command = enter_order
        self.leave_command = leave_order
        self.text = text

        self.canvas_button = CanvasButton(
            master,
            on_motion_callback=self.on_motion_callback,
            on_click_command=self.on_click_callback,
            on_hover_command=self.enter_callback,
            on_leave_command=self.leave_callback,
            foreground_callback=self.foreground_callback,
            on_release_command=self.release_callback,
            height=height,
            width=width,
            canvas_padding_y=0,
            canvas_padding_x=0,
            fg_color='white',
            bg=('white', 'white'),
            out_corners_color=('#CFCFCF', '#333333'),
            border_width=0,
            border_color=('black', 'white')
        )

        pass

    def on_motion_callback(self, event):
        # self.canvas_button.get_canvas().configure(bg='#333333')
        self.canvas_button.get_canvas().create_image(event.x, event.y, image=self.glowing_photo)
        pass

    def on_click_callback(self, event):
        canvas = self.canvas_button.get_canvas()
        canvas.create_text(12, self.text_y, text=self.text, fill='#273746', anchor='nw')
        canvas.create_line(5, 0, 5, 100, fill='gray', width=1)
        canvas.create_line(7, 0, 7, 100, fill='gray', width=1)
        canvas.create_line(7, self.text_y + 10, 13, self.text_y + 10, fill='gray', width=1)
        canvas.configure(bg='#fdf2e9')
        self.canvas_button.draw_out_corners(
            self.canvas_button.corner_radius_ul,
            self.canvas_button.corner_radius_ur,
            self.canvas_button.corner_radius_dl,
            self.canvas_button.corner_radius_dr
        )
        if self.click_command is not None:
            self.click_command()
        pass

    def foreground_callback(self, event):
        canvas = self.canvas_button.get_canvas()
        canvas.create_text(12, self.text_y, text=self.text, fill='#273746', anchor='nw')
        canvas.create_line(5, 0, 5, 100, fill='gray', width=1)
        canvas.create_line(7, 0, 7, 100, fill='gray', width=1)
        canvas.create_line(7, self.text_y + 10, 13, self.text_y + 10, fill='gray', width=1)

    def draw_out_corners(self, radius=0,
                         radius_two=0,
                         radius_three=0,
                         radius_four=0
                         ):
        self.corner_radius_ul = radius
        self.corner_radius_ur = radius_two
        self.corner_radius_dl = radius_three
        self.corner_radius_dr = radius_four

        self.canvas_button.draw_out_corners(self.corner_radius_ul, self.corner_radius_ur, self.corner_radius_dl,
                                            self.corner_radius_dr)

        pass

    def enter_callback(self, event):
        self.canvas_button.get_canvas().configure(bg='white')
        if self.enter_command is not None:
            self.enter_command(event)
        pass

    def leave_callback(self, event):
        if self.leave_command is not None:
            self.leave_command(event)
        pass

    def release_callback(self, event):
        self.canvas_button.get_canvas().configure(bg='white')
        pass

    def pack(self, **kwargs):
        self.canvas_button.pack(**kwargs)
        pass

    def update_theme(self, theme: str):
        self.canvas_button.update_theme(theme)

    def set_disabled(self, value: bool):
        self.canvas_button.set_disabled(value)
        pass
