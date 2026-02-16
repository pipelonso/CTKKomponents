from typing import Tuple, Any, Callable
from types import LambdaType


class PlotAreaDetection:

    LEFT_CLICK = 'left_click'
    LEFT_CLICK_RELEASE = 'left_click_release'
    RIGHT_CLICK = 'right_click'
    RIGHT_CLICK_RELEASE = 'right_click_release'
    HOVER = 'hover'
    HOVER_RELEASE = 'hover_release'

    def __init__(self,
                 first_point: Tuple[int, int],
                 second_point: Tuple[int, int],
                 left_click_callback: Any = None,
                 left_click_release_callback: Any = None,
                 right_click_callback: Any = None,
                 right_click_release_callback: Any = None,
                 hover_callback: Any = None,
                 hover_release_callback: Any = None,
                 return_left_click_cords: bool = False,
                 return_left_click_release_cords: bool = False,
                 return_right_click_cords: bool = False,
                 return_right_click_release_cords: bool = False,
                 return_hover_cords: bool = False,
                 return_hover_release_cords: bool = False
                 ):

        self.first_point = first_point
        self.second_point = second_point
        self.left_click_callback = left_click_callback
        self.left_click_release_callback = left_click_release_callback
        self.right_click_callback = right_click_callback
        self.right_click_release_callback = right_click_release_callback
        self.hover_callback = hover_callback
        self.hover_release_callback = hover_release_callback
        self.return_left_click_cords = return_left_click_cords
        self.return_left_click_release_cords = return_left_click_release_cords
        self.return_right_click_cords = return_right_click_cords
        self.return_right_click_release_cords = return_right_click_release_cords
        self.return_hover_cords = return_hover_cords
        self.return_hover_release_cords = return_hover_release_cords

        self.is_active_hover_release = False

    def _run_dynamic(self, callback_name: str, return_cords: bool, event, event_name: str):
        atr = getattr(self, callback_name)
        if atr is not None:
            if isinstance(atr, Callable) or isinstance(atr, LambdaType):
                if return_cords:
                    return atr({
                        "x1": self.first_point[0],
                        "y1": self.first_point[1],
                        "x2": self.second_point[0],
                        "y2": self.second_point[1],
                        "mx": event.x,
                        "my": event.y,
                        "event": event_name
                    })
                else:
                    return atr()
        return None

    def run_left_click_callback(self, event) -> Any | None:
        self._run_dynamic(
            'left_click_callback',
            self.return_left_click_cords,
            event,
            self.LEFT_CLICK
        )

    def run_left_click_release_callback(self, event) -> Any | None:
        self._run_dynamic(
            'left_click_release_callback',
            self.return_left_click_release_cords,
            event,
            self.LEFT_CLICK_RELEASE
        )

    def run_right_click_callback(self, event) -> Any | None:
        self._run_dynamic(
            'right_click_callback',
            self.return_right_click_cords,
            event,
            self.RIGHT_CLICK
        )

    def run_right_click_release_callback(self, event) -> Any | None:
        self._run_dynamic(
            'right_click_release_callback',
            self.return_right_click_release_cords,
            event,
            self.RIGHT_CLICK_RELEASE
        )

    def run_hover_callback(self, event) -> Any | None:
        if not self.is_active_hover_release:
            self._run_dynamic(
                'hover_callback',
                self.return_hover_cords,
                event,
                self.HOVER
            )

    def run_hover_release_callback(self, event) -> Any | None:
        if self.is_active_hover_release:
            self._run_dynamic(
                'hover_release_callback',
                self.return_hover_release_cords,
                event,
                self.HOVER_RELEASE
            )
