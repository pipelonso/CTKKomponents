import customtkinter
import pyautogui
from typing import Any, Optional, Tuple, Dict
import time
import math
from views.components.PlotDetectionArea import PlotAreaDetection


class Plot:

    def __init__(self,
                 master: Any,
                 width: Optional[int] = 1000,
                 height: Optional[int] = 1000,
                 draggable: Optional[bool] = True,
                 camera_position: Optional[Tuple[int, int]] = (0, 0),
                 camera_corner_align: Optional[bool] = False,
                 plot_border_color: Optional[Tuple[str, str]] = '#00ffe4',
                 plot_fg_color: Optional[str] = '#1a1c1c',
                 draw_grid: Optional[bool] = True,
                 grid_x_separation: Optional[int] = 20,
                 grid_y_separation: Optional[int] = 20,
                 x_generation_limit: Optional[int] = 2000,
                 y_generation_limit: Optional[int] = 2000,
                 plot_drag_cursor: Optional[str] = 'fleur',
                 # "arrow", “circle”, “clock”, “cross”, “dotbox”, “exchange”,
                 # “fleur”, “heart”, “heart”, “man”, “mouse”, “pirate”, “plus”, “shuttle”, “sizing”, “spider”,
                 # “spraycan”, “star”, “target”, “tcross”, “trek”, “watch”
                 enable_capture_motion_callback: Optional[bool] = False,
                 enable_capture_click_callback: Optional[bool] = False,
                 enable_capture_click_release_callback: Optional[bool] = False,
                 enable_capture_right_click_callback: Optional[bool] = False,
                 enable_capture_right_click_release_callback: Optional[bool] = False,
                 virtual_void_fg_color: Optional[Tuple[str, str]] = ('#ffffff', '#000000'),
                 enable_canvas_go_out_camera_callback: Optional[bool] = True,
                 enable_plot_area_detection: bool = False
                 ):

        self.master = master

        self.width = width
        self.height = height

        self._update_callbacks = []
        self._drag_callbacks = []
        self._click_callbacks = []
        self._click_release_callbacks = []
        self._canvas_out_windows_callbacks = []

        self._area_detections: list[PlotAreaDetection] = []

        self.debug_mode = False

        self._joiners = []

        self.draggable = draggable
        self.custom_position = camera_position

        self._camera_corner_align = camera_corner_align

        self.draw_grid = draw_grid
        self.grid_x_separation = grid_x_separation
        self.grid_y_separation = grid_y_separation

        self.enable_capture_motion_callback = enable_capture_motion_callback
        self.enable_capture_click_callback = enable_capture_click_callback
        self.enable_capture_click_release_callback = enable_capture_click_release_callback
        self.enable_capture_right_click_callback = enable_capture_right_click_callback
        self.enable_capture_right_click_release_callback = enable_capture_right_click_release_callback
        self.enable_canvas_go_out_camera_callback = enable_canvas_go_out_camera_callback

        self.enable_plot_area_detection = enable_plot_area_detection

        self.x_generation_limit = x_generation_limit
        self.y_generation_limit = y_generation_limit

        self.back_drag = False
        self.origin_x = 0
        self.origin_y = 0

        self.mouse_pos_x = 0
        self.mouse_pos_y = 0

        self.mouse_x_offset = 0
        self.mouse_y_offset = 0

        self.start_mouse_pos_x = 0
        self.start_mouse_pos_y = 0

        self.bg_frame = customtkinter.CTkFrame(
            master,
            width=width,
            height=height,
            fg_color=virtual_void_fg_color
        )

        self.main_frame = customtkinter.CTkFrame(
            self.bg_frame,
            width=width,
            height=height,
            fg_color=plot_border_color
        )

        self.regenerate_canvas_position()

        self.canvas = customtkinter.CTkCanvas(
            master=self.main_frame,
            bg=plot_fg_color, highlightthickness=0,
            width=width,
            height=height,
            cursor=plot_drag_cursor
        )

        self.canvas.pack(padx=2, pady=2, fill='both', expand=True)

        self.register_bind()
        if self.draw_grid:
            self.generate_grid()
        pass

    def register_bind(self):
        self.canvas.bind('<B1-Motion>', self.on_motion)

        if self.enable_capture_click_callback:
            self.canvas.bind('<Button-1>', self.on_canvas_click)

        if self.enable_capture_right_click_callback:
            self.canvas.bind('<Button-3>', self.on_right_click)

        if self.enable_capture_click_release_callback:
            self.canvas.bind('<ButtonRelease-1>', self.on_canvas_click_release)

        if self.enable_capture_right_click_release_callback:
            self.canvas.bind('<ButtonRelease-3>', self.on_right_click_release)

        if self.enable_capture_motion_callback:
            self.canvas.bind("<Motion>", self.on_mouse_move)

        pass

    def on_right_click(self, event):
        for detection in self._area_detections:
            if (
                    detection.first_point[0] < event.x < detection.second_point[0] and
                    detection.first_point[1] < event.y < detection.second_point[1]
            ):
                detection.run_right_click_callback(event)
        pass

    def on_right_click_release(self, event):
        for detection in self._area_detections:
            if (
                    detection.first_point[0] < event.x < detection.second_point[0] and
                    detection.first_point[1] < event.y < detection.second_point[1]
            ):
                detection.run_right_click_release_callback(event)
        pass

    def on_mouse_move(self, event):

        if self.enable_plot_area_detection:
            for detection in self._area_detections:
                if (
                        detection.first_point[0] < event.x < detection.second_point[0] and
                        detection.first_point[1] < event.y < detection.second_point[1]
                ):
                    detection.run_hover_callback(event  )
                    detection.is_active_hover_release = True
                else:
                    detection.run_hover_release_callback(event)
                    detection.is_active_hover_release = False
                pass

        pass

    def set_debug_mode(self, state: bool):
        self.debug_mode = state

    def update(self):
        self.canvas.delete('all')
        if self.draw_grid:
            self.generate_grid()
        for function in self._update_callbacks:
            self._callback_caller(function, None)
        pass

    def get_main_frame(self):
        return self.main_frame

    def get_canvas(self):
        return self.canvas

    def generate_grid(self):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        line_color = "#2a2a2a"

        for x in range(0, canvas_width, self.grid_x_separation):
            self.canvas.create_line(x, 0, x, canvas_height, fill=line_color)

        for y in range(0, canvas_height, self.grid_y_separation):
            self.canvas.create_line(0, y, canvas_width, y, fill=line_color)
        pass

    def register_dragging_callback(
            self,
            callback,
            use_event: Optional[bool] = False,
            *args
    ):
        make_in = (callback, use_event, *args)
        self._drag_callbacks.append(make_in)
        pass

    def register_update_callback(
            self,
            callback,
            use_event: Optional[bool] = False,
            *args
    ):
        make_in = (callback, use_event, *args)
        self._update_callbacks.append(make_in)
        pass

    def register_click_callback(
            self,
            callback,
            use_event: Optional[bool] = False,
            *args
    ):
        make_in = (callback, use_event, *args)
        self._click_callbacks.append(make_in)
        pass

    def register_click_release_callback(
            self,
            callback,
            use_event: Optional[bool] = False,
            *args
    ):
        make_in = (callback, use_event, *args)
        self._click_release_callbacks.append(make_in)
        pass

    def register_canvas_out_camera_callback(
            self,
            callback,
            use_event: Optional[bool] = False,
            *args
    ):
        make_in = (callback, use_event, *args)
        self._canvas_out_windows_callbacks.append(make_in)
        pass

    def on_motion(self, event):

        if self.draggable:
            px_cursor = pyautogui.position().x - self.master.winfo_x()
            py_cursor = pyautogui.position().y - self.master.winfo_y()

            time.sleep(0.01)

            px_cursor_last = pyautogui.position().x - self.master.winfo_x()
            py_cursor_last = pyautogui.position().y - self.master.winfo_y()

            dif_x = px_cursor - self.main_frame.winfo_x()
            dif_y = py_cursor - self.main_frame.winfo_y()

            x_flipper = -2 if px_cursor > px_cursor_last else 2
            y_flipper = -2 if py_cursor > py_cursor_last else 2

            x_dis = (px_cursor - px_cursor_last) * x_flipper if px_cursor > px_cursor_last else (
                                                                                                        px_cursor_last - px_cursor) * x_flipper
            y_dis = (py_cursor - py_cursor_last) * y_flipper if py_cursor > py_cursor_last else (
                                                                                                        py_cursor_last - py_cursor) * y_flipper

            self.main_frame.place(x=(px_cursor - dif_x + x_dis),
                                  y=(py_cursor - dif_y + y_dis))

            self.custom_position = ((px_cursor - dif_x + x_dis), (py_cursor - dif_y + y_dis))

        canvas_width = (
                (self.main_frame.winfo_width() +
                 (self.bg_frame.winfo_width() - (self.main_frame.winfo_x() + self.main_frame.winfo_width()))) - 4
        )

        if canvas_width < self.x_generation_limit:
            self.canvas.configure(width=canvas_width)

        canvas_height = (
                (self.main_frame.winfo_height() +
                 (self.bg_frame.winfo_height() - (self.main_frame.winfo_y() + self.main_frame.winfo_height()))) - 4
        )

        if canvas_height < self.y_generation_limit:
            self.canvas.configure(height=canvas_height)

        self.canvas.delete('all')

        if self.draw_grid:
            self.generate_grid()

        for function in self._drag_callbacks:
            self._callback_caller(function, event)

        if self.enable_canvas_go_out_camera_callback:
            if self.is_canvas_out_of_frame():
                for function in self._canvas_out_windows_callbacks:
                    self._callback_caller(function, event)

            pass

    def regenerate_canvas_position(self):
        if not self._camera_corner_align:
            self.main_frame.place(x=self.custom_position[0] + (self.width / 2),
                                  y=self.custom_position[1] + (self.height / 2))
        else:
            self.main_frame.place(x=self.custom_position[0], y=self.custom_position[1])

        pass

    def is_canvas_out_of_frame(self):
        bg_frame_width, bg_frame_height = self.bg_frame.winfo_width(), self.bg_frame.winfo_height()
        # icons ⊡ ⊢ ⊣ ⊤ ⊥
        return (
                self.custom_position[0] > bg_frame_width  # ⊡ X = sup <-> left   -> ⊣ limit
                or self.custom_position[1] > bg_frame_height  # ⊡ Y = sup <-> left   -> ⊥ limit
                or (self.custom_position[0] + self.canvas.winfo_width()) < 0  # ⊡ X = sup <-> right   -> ⊢ limit
                or (self.custom_position[1] + self.canvas.winfo_height()) < 0  # ⊡ Y = inf <-> left   -> ⊤ limit
        )

    def configure(self, **kwargs):
        if "camera_position" in kwargs:
            pos = kwargs.get('camera_position')
            if isinstance(pos, Tuple):
                if len(pos) < 2:
                    raise Exception(f'Bad argument camera_position value "{pos}", required (int, int)')
                else:
                    for i in pos:
                        if not isinstance(i, int):
                            raise Exception(f'Bad argument camera_position value "{type(i)}", required (int, int)')
                    self.custom_position = pos
            else:
                raise Exception(f'Bad argument camera_position required instance of tuple, {type(pos)} provided')

            pass
        pass

    def create_joiner(self,
                      joiner_id: str,
                      first_point: Tuple[int, int],
                      second_point: Tuple[int, int],
                      style: Optional[str] = 'simple',  # doted, double
                      width: Optional[int] = 2,
                      join_mode: Optional[str] = 'direct',  # direct, indirect, smooth,
                      corner_radius: Optional[int] = 10,
                      first_point_indicator: Optional[str] = 'arrow',  # arrow, dot, circle
                      second_point_indicator: Optional[str] = 'arrow',  # arrow, dot, circle
                      fill: Optional[str] = 'red',
                      dash_offset: Optional[int] = 15,
                      dash: Optional[Tuple[int, int]] = (15, 15)
                      ):

        self._validate_joiner_creation_and_update('create', joiner_id, first_point, second_point, style, width,
                                                  join_mode,
                                                  corner_radius, first_point_indicator, second_point_indicator, fill,
                                                  dash_offset, dash)

        joiner = {
            "joiner_id": joiner_id,
            "first_point": first_point,
            "second_point": second_point,
            "style": style,
            "width": width,
            "join_mode": join_mode,
            "corner_radius": corner_radius,
            "first_point_indicator": first_point_indicator,
            "second_point_indicator": second_point_indicator,
            "fill": fill,
            "dash_offset": dash_offset,
            "dash": dash
        }

        self._joiners.append(joiner)

        pass

    def update_joiner(self,
                      joiner_id: str,
                      first_point: Tuple[int, int] = None,
                      second_point: Tuple[int, int] = None,
                      style: Optional[str] = None,  # doted, double
                      width: Optional[int] = None,
                      join_mode: Optional[str] = None,  # direct, indirect, smooth,
                      corner_radius: Optional[int] = None,
                      first_point_indicator: Optional[str] = None,  # arrow, dot, circle
                      second_point_indicator: Optional[str] = None,  # arrow, dot, circle
                      fill: Optional[str] = 'red',
                      dash_offset=15,
                      dash=(15, 15)
                      ):

        self._validate_joiner_creation_and_update('edit', joiner_id, first_point, second_point, style, width,
                                                  join_mode, corner_radius, first_point_indicator,
                                                  second_point_indicator,
                                                  fill, dash_offset, dash)

        for index, joiner in enumerate(self._joiners):
            if joiner['joiner_id'] == joiner_id:
                self._joiners[index] = {
                    "joiner_id": joiner_id,
                    "first_point": first_point if first_point is not None else joiner["first_point"],
                    "second_point": second_point if second_point is not None else joiner["second_point"],
                    "style": style if style is not None else joiner["style"],
                    "width": width if width is not None else joiner["width"],
                    "join_mode": join_mode if join_mode is not None else joiner["join_mode"],
                    "corner_radius": corner_radius if corner_radius is not None else joiner["corner_radius"],
                    "first_point_indicator": first_point_indicator if first_point_indicator is not None else joiner[
                        "first_point_indicator"],
                    "second_point_indicator": second_point_indicator if second_point_indicator is not None else joiner[
                        "second_point_indicator"],
                    "fill": fill if fill is not None else joiner["fill"],
                    "dash_offset": dash_offset if dash_offset is not None else joiner["dash_offset"],
                    "dash": dash if dash is not None else joiner["dash"]
                }
            pass

        pass

    @staticmethod
    def _make_arrow_head_polygon_map(angle: float, wings_size: int, arrow_size, pos: Tuple[int, int]):

        pass

    @staticmethod
    def _calculate_line_direction_angle(first_pos: Tuple[int, int], second_pos: Tuple[int, int]):

        cateto_horizontal = abs(second_pos[0] - first_pos[0])
        cateto_vertical = abs(second_pos[1] - first_pos[1])
        hipotenusa = math.sqrt(cateto_horizontal ** 2 + cateto_vertical ** 2)

        if first_pos[0] < second_pos[0]:
            if first_pos[1] > second_pos[1]:
                triangle_corner_pos_x = second_pos[0]
            else:
                triangle_corner_pos_x = first_pos[0]
        else:
            if first_pos[1] > second_pos[1]:
                triangle_corner_pos_x = second_pos[0]
            else:
                triangle_corner_pos_x = first_pos[0]

        triangle_corner_pos_y = first_pos[1] if first_pos[1] > second_pos[1] else second_pos[1]

        theta1_rad = math.atan2(cateto_vertical, cateto_horizontal)
        theta2_rad = math.pi / 2 - theta1_rad

        theta1_deg = math.degrees(theta1_rad)
        theta2_deg = math.degrees(theta2_rad)

        return {
            "h_cat": cateto_horizontal,
            "v_cat": cateto_vertical,
            "hipotenusa": hipotenusa,
            "ang1": theta1_deg,
            "ang2": theta2_deg,
            "corner_angle": 90.0,
            "triangle_corner_pos_x": triangle_corner_pos_x,
            "triangle_corner_pos_y": triangle_corner_pos_y,
            "first_point": first_pos,
            "second_point": second_pos
        }

    def _render_debug_from_join_mode_direct(self, calculated_triangle: Dict):

        self.canvas.create_aa_circle(calculated_triangle['triangle_corner_pos_x'],
                                     calculated_triangle['triangle_corner_pos_y'], 5, fill='red')

        self.canvas.create_line(calculated_triangle['triangle_corner_pos_x'] - calculated_triangle["h_cat"],
                                calculated_triangle['triangle_corner_pos_y'],
                                calculated_triangle['triangle_corner_pos_x'] + calculated_triangle["h_cat"],
                                calculated_triangle['triangle_corner_pos_y'],
                                fill='red',
                                dash=(10, 10))

        self.canvas.create_line(calculated_triangle['triangle_corner_pos_x'],
                                calculated_triangle['triangle_corner_pos_y'] - calculated_triangle["v_cat"],
                                calculated_triangle['triangle_corner_pos_x'],
                                calculated_triangle['triangle_corner_pos_y'] + calculated_triangle["v_cat"],
                                fill='red',
                                dash=(10, 10))

        self.canvas.create_text(calculated_triangle['triangle_corner_pos_x'] + 10,
                                calculated_triangle['triangle_corner_pos_y'] - 15,
                                text=f'({calculated_triangle["triangle_corner_pos_x"]}, {calculated_triangle["triangle_corner_pos_y"]})',
                                fill='orange',
                                anchor='w'
                                )

        self.canvas.create_text(calculated_triangle['triangle_corner_pos_x'] + 10,
                                calculated_triangle['triangle_corner_pos_y'] - 30,
                                text=f'h = {calculated_triangle["hipotenusa"]}',
                                fill='orange',
                                anchor='w'
                                )

        self.canvas.create_text(calculated_triangle['triangle_corner_pos_x'] + 10,
                                calculated_triangle['triangle_corner_pos_y'] - 30,
                                text=f'h = {calculated_triangle["hipotenusa"]}',
                                fill='orange',
                                anchor='w'
                                )

        self.canvas.create_text(calculated_triangle['triangle_corner_pos_x'] - 10,
                                calculated_triangle['triangle_corner_pos_y'] - 10,
                                text=f'C1 = {calculated_triangle["v_cat"]} ➤',
                                fill='orange',
                                anchor='w',
                                angle=90
                                )

        self.canvas.create_text(calculated_triangle['triangle_corner_pos_x'] + 10,
                                calculated_triangle['triangle_corner_pos_y'] + 10,
                                text=f'C2 = {calculated_triangle["h_cat"]} ➤',
                                fill='orange',
                                anchor='w'
                                )

        self.canvas.create_text(calculated_triangle['first_point'][0] + (
            15 if calculated_triangle["second_point"][0] > calculated_triangle['triangle_corner_pos_x'] else -15),
                                calculated_triangle['first_point'][1] - 10,
                                text=f'pos = ({calculated_triangle["first_point"][0]}, {calculated_triangle["first_point"][1]})',
                                fill='orange',
                                anchor='w' if calculated_triangle["second_point"][0] > calculated_triangle[
                                    'triangle_corner_pos_x'] else 'e',
                                )

        self.canvas.create_text(calculated_triangle['first_point'][0] + (
            15 if calculated_triangle["second_point"][0] > calculated_triangle['triangle_corner_pos_x'] else -15),
                                calculated_triangle['first_point'][1] - 30,
                                text=f'Ang ➤ {calculated_triangle["ang1"]}',
                                fill='orange',
                                anchor='w' if calculated_triangle["second_point"][0] > calculated_triangle[
                                    'triangle_corner_pos_x'] else 'e',
                                )

        self.canvas.create_text(calculated_triangle['second_point'][0] + (
            15 if calculated_triangle["first_point"][0] > calculated_triangle['triangle_corner_pos_x'] else -15),
                                calculated_triangle['second_point'][1] - 30,
                                text=f'Ang ➤ {calculated_triangle["ang2"]}',
                                fill='orange',
                                anchor='w' if calculated_triangle["second_point"][0] > calculated_triangle[
                                    'triangle_corner_pos_x'] else 'e',
                                )

        self.canvas.create_text(calculated_triangle['second_point'][0] + (
            15 if calculated_triangle["first_point"][0] > calculated_triangle['triangle_corner_pos_x'] else -15),
                                calculated_triangle['second_point'][1] - 50,
                                text=f'pos = ({calculated_triangle["second_point"][0]}, {calculated_triangle["second_point"][1]})',
                                fill='orange',
                                anchor='w' if calculated_triangle["second_point"][0] > calculated_triangle[
                                    'triangle_corner_pos_x'] else 'e',
                                )
        pass

    def render_joiner_list(self):
        for joiner in self._joiners:
            if joiner['join_mode'] == 'direct':
                calculated_triangle = self._calculate_line_direction_angle(joiner['first_point'],
                                                                           joiner['second_point'])
                if joiner['style'] == 'simple':

                    self.canvas.create_line(
                        joiner['first_point'][0], joiner['first_point'][1],
                        joiner['second_point'][0], joiner['second_point'][1],
                        fill=joiner['fill'],
                        width=joiner['width']
                    )

                    if self.debug_mode:
                        self._render_debug_from_join_mode_direct(calculated_triangle)

                if joiner['style'] == 'doted':
                    self.canvas.create_line(
                        joiner['first_point'][0], joiner['first_point'][1],
                        joiner['second_point'][0], joiner['second_point'][1],
                        fill=joiner['fill'],
                        width=joiner['width'],
                        dashoffset=joiner['dash_offset'],
                        dash=joiner['dash']
                    )
            pass
        pass

    @staticmethod
    def _validate_joiner_creation_and_update(
            mode: str,  # create, edit
            joiner_id,
            first_point,
            second_point,
            style,  # doted, double
            width,
            join_mode,  # direct, indirect, smooth,
            corner_radius,
            first_point_indicator,  # arrow, dot, circle
            second_point_indicator,  # arrow, dot, circle
            fill,
            dash_offset,
            dash
    ):
        if mode == 'create':
            if style not in ['simple', 'doted', 'double']:
                raise Exception(
                    f'Wrong value in argument style, [simple, doted, double] required, {style} provided')

            if join_mode not in ['direct', 'indirect', 'smooth']:
                raise Exception(
                    f'Wrong value in argument join_mode, [direct, indirect, smooth] required, {join_mode} provided')

            point_indicators = ['arrow', 'dot', 'circle']
            if second_point_indicator not in point_indicators:
                raise Exception(
                    f'Wrong value in argument second_point_indicator, [arrow, dot, circle] required, {second_point_indicator} provided')
            if first_point_indicator not in point_indicators:
                raise Exception(
                    f'Wrong value in argument second_point_indicator, [arrow, dot, circle] required, {first_point_indicator} provided')

            if isinstance(first_point, Tuple):
                if len(first_point) != 2:
                    raise Exception(
                        f'Wrong value in argument first_point, Tuple[int, int] required, Tuple of size {len(first_point)} provided')
            else:
                raise Exception(
                    f'Wrong value in argument first_point, Tuple[int, int] required, {type(first_point)} provided')

        elif mode == 'edit':

            pass

        return True

    @staticmethod
    def _is_callback_in_list(callback_list, callback):
        for function in callback_list:
            if function == callback:
                return True
        return False

    def is_callback_in_dragging_callback(self, callback):
        return self._is_callback_in_list(self._drag_callbacks, callback)

    def is_callback_in_update_callback(self, callback):
        return self._is_callback_in_list(self._update_callbacks, callback)

    def is_callback_in_click_callback(self, callback):
        return self._is_callback_in_list(self._click_callbacks, callback)

    def is_callback_in_click_release_callback(self, callback):
        return self._is_callback_in_list(self._click_release_callbacks, callback)

    def is_callback_in_canvas_out_window_callback(self, callback):
        return self._is_callback_in_list(self._canvas_out_windows_callbacks, callback)

    @staticmethod
    def _callback_caller(function, event):
        if not function[1]:
            if len(function) > 2:
                arg_priority = function[2]
            else:
                arg_priority = None
        else:
            arg_priority = event

        if arg_priority is not None:
            function[0](arg_priority)
        else:
            function[0]()
        pass

    def on_canvas_click_release(self, event):

        if self.enable_plot_area_detection:
            for detection in self._area_detections:
                if (
                        detection.first_point[0] < event.x < detection.second_point[0] and
                        detection.first_point[1] < event.y < detection.second_point[1]
                ):
                    detection.run_left_click_release_callback(event)
            pass

        if self.draw_grid:
            self.generate_grid()

        for function in self._click_release_callbacks:
            self._callback_caller(function, event)
        pass

    def on_canvas_click(self, event):

        if self.draw_grid:
            self.generate_grid()
        for function in self._click_callbacks:
            self._callback_caller(function, event)

        if self.enable_plot_area_detection:
            for detection in self._area_detections:
                if (
                        detection.first_point[0] < event.x < detection.second_point[0] and
                        detection.first_point[1] < event.y < detection.second_point[1]
                ):
                    detection.run_left_click_callback(event)
            pass

        pass

    def place(self, **kwargs):
        self.bg_frame.place(**kwargs)

    def pack(self, **kwargs):
        self.bg_frame.pack(**kwargs)

    def register_area_detection(self, area_detection: PlotAreaDetection):
        self._area_detections.append(area_detection)

    def clear_area_detections(self):
        self._area_detections.clear()
        pass
