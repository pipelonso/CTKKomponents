import types

import customtkinter
from typing import Any, Optional, Union, Tuple, Callable
import math


class CanvasButton:

    theme = 'dark'

    def __init__(self,
                 master: Any,
                 canvas_padding_x: Optional[int] = 5,
                 canvas_padding_y: Optional[int] = 5,
                 fg_color: Optional[Union[str, Tuple[str, str]]] = ('white', 'black'),
                 width: int = 100,
                 height: int = 100,
                 on_click_command=None,
                 on_hover_command=None,
                 on_leave_command=None,
                 on_release_command=None,
                 on_update_callback=None,
                 on_motion_callback=None,
                 background_callback=None,
                 foreground_callback=None,

                 corner_radius: int = 10,
                 automatic_update=True,
                 bg: Optional[Union[str, Tuple[str, str]]] = ('white', 'black'),
                 out_corners_color: Optional[Union[str, Tuple[str, str]]] = ('white', 'black'),
                 border_width=0,
                 border_color: Optional[Union[str, Tuple[str, str]]] = ('white', 'black')
                 ):

        self.is_mouse_pressed = False
        self.is_mouse_moving = False
        self.is_mouse_released = False
        self.is_mouse_enter = False
        self.is_updating = True
        self.is_bg_active = True
        self.is_fg_active = True

        self.disabled = False

        self.fg_color = fg_color

        self.update_callback = on_update_callback

        self.click_callback = on_click_command
        self.hover_callback = on_hover_command
        self.release_callback = on_leave_command
        self.on_release_callback = on_release_command
        self.motion_callback = on_motion_callback

        self.background_callback = background_callback
        self.foreground_callback = foreground_callback

        self.automatic_update = automatic_update

        self.bg = bg
        self.out_corners_color = out_corners_color

        self._background_rendered_layer = {
            "name": "background", "callback": self.background_callback,
            "enabled_layers": [
                {"name": "motion", "enabled": "is_mouse_moving"},
                {"name": "update", "enabled": "is_updating"},
                {"name": "click", "enabled": "is_mouse_pressed"},
                {"name": "release", "enabled": "is_mouse_released"},
                {"name": "leave", "enabled": "!is_mouse_enter"},
                {"name": "hover", "enabled": "is_mouse_enter"},
                {"name": "background", "enabled": "is_bg_active"},
                {"name": "foreground", "enabled": "is_fg_active"}
            ]
        }

        self._click_renderer_layer = {
            "name": "click", "callback": self.click_callback,
            "enabled_layers": [
                {"name": "motion", "enabled": "is_mouse_moving"},
                {"name": "click", "enabled": "is_mouse_pressed"},
                {"name": "background", "enabled": "is_bg_active"},
                {"name": "foreground", "enabled": "is_fg_active"}
            ]
        }

        self._hover_renderer_layer = {
            "name": "hover", "callback": self.hover_callback,
            "enabled_layers": [
                {"name": "motion", "enabled": "is_mouse_moving"},
                {"name": "hover", "enabled": "is_mouse_enter"},
                {"name": "background", "enabled": "is_bg_active"},
                {"name": "foreground", "enabled": "is_fg_active"}
            ]
        }

        self._leave_renderer_layer = {
            "name": "leave", "callback": self.release_callback,
            "enabled_layers": [
                {"name": "motion", "enabled": "is_mouse_moving"},
                {"name": "leave", "enabled": "!is_mouse_enter"},
                {"name": "background", "enabled": "is_bg_active"},
                {"name": "foreground", "enabled": "is_fg_active"}
            ]
        }

        self._release_renderer_layer = {
            "name": "release", "callback": self.on_release_callback,
            "enabled_layers": [
                {"name": "motion", "enabled": "is_mouse_moving"},
                {"name": "release", "enabled": "is_mouse_released"},
                {"name": "background", "enabled": "is_bg_active"},
                {"name": "foreground", "enabled": "is_fg_active"}
            ]
        }

        self._motion_renderer_layer = {
            "name": "motion", "callback": self.motion_callback,
            "enabled_layers": [
                {"name": "motion", "enabled": "is_mouse_moving"},
                {"name": "hover", "enabled": "!is_mouse_pressed"},
                {"name": "click", "enabled": 'is_mouse_pressed'},
                {"name": "release", "enabled": 'is_mouse_released'},
                {"name": "background", "enabled": "is_bg_active"},
                {"name": "foreground", "enabled": "is_fg_active"}
            ]
        }

        self._update_rendered_layer = {
            "name": "update", "callback": self.update_callback,
            "enabled_layers": [
                {"name": "motion", "enabled": "is_mouse_moving"},
                {"name": "update", "enabled": "is_mouse_moving"},
                {"name": "background", "enabled": "is_bg_active"},
                {"name": "foreground", "enabled": "is_fg_active"}
            ]
        }

        self._foreground_rendered_layer = {
            "name": "foreground", "callback": self.foreground_callback,
            "enabled_layers": [
                {"name": "motion", "enabled": "is_mouse_moving"},
                {"name": "update", "enabled": "is_updating"},
                {"name": "click", "enabled": "is_mouse_pressed"},
                {"name": "release", "enabled": "is_mouse_released"},
                {"name": "leave", "enabled": "!is_mouse_enter"},
                {"name": "hover", "enabled": "is_mouse_enter"},
                {"name": "background", "enabled": "is_bg_active"},
                {"name": "foreground", "enabled": "is_fg_active"}
            ]
        }

        self._layers_list = [
            self._background_rendered_layer,
            self._motion_renderer_layer,
            self._click_renderer_layer,
            self._hover_renderer_layer,
            self._leave_renderer_layer,
            self._release_renderer_layer,
            self._update_rendered_layer,
            self._foreground_rendered_layer
        ]

        self.width = width
        self.height = height

        self.canvas_width = width - canvas_padding_x
        self.canvas_height = height - canvas_padding_y

        self.corner_radius_ul = 0
        self.corner_radius_ur = 0
        self.corner_radius_dl = 0
        self.corner_radius_dr = 0

        self.general_frame = customtkinter.CTkFrame(
            master,
            fg_color=fg_color,
            width=width,
            height=height,
            corner_radius=corner_radius,
            border_width=border_width,
            border_color=border_color
        )

        bg_canvas = 'white'

        if isinstance(self.bg, str):
            bg_canvas = self.bg
        elif isinstance(self.bg, tuple):
            bg_canvas = self.bg[0]

        self.canvas = customtkinter.CTkCanvas(self.general_frame,
                                              width=self.canvas_width,
                                              height=height,
                                              highlightthickness=0,
                                              bg=bg_canvas
                                              )
        self.canvas.pack(padx=canvas_padding_x, pady=canvas_padding_y, fill='both', expand=True)

        if self.hover_callback is not None:
            self.canvas.bind('<Enter>', self._on_enter)

        if self.release_callback is not None:
            self.canvas.bind('<Leave>', self._on_leave)

        if self.click_callback is not None:
            self.canvas.bind('<Button-1>', self._on_click)

        self.canvas.bind('<ButtonRelease>', self._on_release)

        if self.motion_callback is not None:
            self.canvas.bind('<Motion>', self._on_canvas_motion)

        if self.update_callback is not None or self.automatic_update:
            self.canvas.bind('<Configure>', self._on_canvas_resize)

        pass

    def _on_canvas_resize(self, event):

        self.canvas_width = self.canvas.winfo_width()
        self.canvas_height = self.canvas.winfo_height()
        self._on_update_callback(event)

        pass

    def _make_callbacks(self, action: dict, event):

        if action.get('callback') is not None or self.automatic_update:

            self.canvas.delete('all')
            runnable_layers = []

            for layer in self._layers_list:
                layer_name = layer.get("name")  # Guardamos el valor de "name" para evitar múltiples accesos

                for enabled_layer in action.get("enabled_layers"):
                    if enabled_layer["name"] == layer_name:
                        enabled_value = enabled_layer["enabled"]

                        if enabled_value[0] == '!':
                            atr_name = enabled_value[1:]
                            if not getattr(self, atr_name):
                                runnable_layers.append(layer)
                        else:
                            if getattr(self, enabled_value):
                                runnable_layers.append(layer)

            for run_layer in runnable_layers:
                callback = run_layer.get("callback")
                if isinstance(callback, types.LambdaType):
                    callback()
                elif isinstance(callback, Callable):
                    callback(event)

            self.draw_out_corners(self.corner_radius_ul, self.corner_radius_ur, self.corner_radius_dl,
                                  self.corner_radius_dr)

        pass

    def set_disabled(self, value: bool):
        self.disabled = value
        pass

    def _on_canvas_motion(self, event):
        self.is_mouse_moving = True
        if self.motion_callback is not None:
            self._make_callbacks(self._motion_renderer_layer, event)

    def _on_update_callback(self, event):
        if self.update_callback is not None or self.automatic_update:
            self._make_callbacks(self._update_rendered_layer, event)
        pass

    def update_theme(self, theme: str):
        self.theme = theme

        frame_theme = 'white'

        if isinstance(self.bg, str):
            frame_theme = self.bg
        elif theme == 'light':
            if isinstance(self.bg, tuple):
                frame_theme = self.bg[0]
        else:
            if isinstance(self.bg, tuple):
                frame_theme = self.bg[1]

        if isinstance(frame_theme, tuple):
            if self.theme == "dark":
                self.canvas.configure(bg=frame_theme[1])
            else:
                self.canvas.configure(bg=frame_theme[0])
                pass
            pass
        else:
            self.canvas.configure(bg=frame_theme)

        self.draw_out_corners(self.corner_radius_ul, self.corner_radius_ur, self.corner_radius_dl,
                              self.corner_radius_dr)

    def _on_enter(self, event):
        if not self.is_mouse_pressed:
            self.is_mouse_enter = True

        if self.hover_callback is not None:
            self._make_callbacks(self._hover_renderer_layer, event)
        pass

    def _on_leave(self, event):
        self.is_mouse_moving = False
        self.is_mouse_enter = False
        if self.release_callback is not None:
            self._make_callbacks(self._leave_renderer_layer, event)
        pass

    def _on_release(self, event):
        self.is_mouse_pressed = False
        self.is_mouse_released = True
        if self.on_release_callback is not None:
            self._make_callbacks(self._release_renderer_layer, event)
        pass

    def _on_click(self, event):
        if not self.disabled:
            self.is_mouse_pressed = True
            self.is_mouse_released = False
            if self.click_callback is not None:
                self._make_callbacks(self._click_renderer_layer, event)

        pass

    def draw_out_corners(self, radius=0,
                         radius_two=0,
                         radius_three=0,
                         radius_four=0
                         ):

        color = 'white'
        if isinstance(self.out_corners_color, tuple):
            if self.theme == 'light':
                color = self.out_corners_color[0]
            else:
                color = self.out_corners_color[1]
        if isinstance(self.out_corners_color, str):
            color = self.out_corners_color

        if color == 'transparent':
            color = 'white'

        self.corner_radius_ul = radius
        self.corner_radius_ur = radius_two
        self.corner_radius_dl = radius_three
        self.corner_radius_dr = radius_four

        if self.corner_radius_ul > 0:

            corner_ul_x_point = self.corner_radius_ul
            corner_ul_y_point = self.corner_radius_ul

            for deg in range(91, 181):
                rad = math.radians(deg)

                x = corner_ul_x_point + int(self.corner_radius_ul * math.cos(rad))
                y = corner_ul_y_point - int(self.corner_radius_ul * math.sin(rad))

                self.canvas.create_line(x - 1, corner_ul_y_point - self.corner_radius_ul, x - 1, y, fill=color)

        pass

        if self.corner_radius_ur > 0:

            corner_ur_x_point = self.canvas_width - self.corner_radius_ur
            corner_ur_y_point = self.corner_radius_ur

            for deg in range(0, 91):
                rad = math.radians(deg)

                x = corner_ur_x_point + int(self.corner_radius_ur * math.cos(rad))
                y = corner_ur_y_point - int(self.corner_radius_ur * math.sin(rad))

                self.canvas.create_line(x, corner_ur_y_point - self.corner_radius_ur, x, y, fill=color)

        if self.corner_radius_dl > 0:

            corner_dl_x_point = self.corner_radius_dl
            corner_dl_y_point = self.canvas_height - self.corner_radius_dl

            for deg in range(181, 271):
                rad = math.radians(deg)

                x = corner_dl_x_point + int(self.corner_radius_dl * math.cos(rad))
                y = corner_dl_y_point - int(self.corner_radius_dl * math.sin(rad))

                self.canvas.create_line(x - 1, corner_dl_y_point + self.corner_radius_dl, x - 1, y, fill=color)

        if self.corner_radius_dr > 0:

            corner_dr_x_point = self.canvas_width - self.corner_radius_dr
            corner_dr_y_point = self.canvas_height - self.corner_radius_dr

            for deg in range(271, 360):
                rad = math.radians(deg)

                x = corner_dr_x_point + int(self.corner_radius_dr * math.cos(rad))
                y = corner_dr_y_point - int(self.corner_radius_dr * math.sin(rad))

                self.canvas.create_line(x, corner_dr_y_point + self.corner_radius_dr, x, y, fill=color)

    pass

    def get_canvas(self) -> customtkinter.CTkCanvas:
        return self.canvas

    def pack(self, **kwargs):
        self.general_frame.pack(**kwargs)

    def place(self, **kwargs):
        self.general_frame.place(**kwargs)
