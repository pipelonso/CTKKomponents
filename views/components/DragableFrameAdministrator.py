from views.components.DraggableFrame import DraggableFrame
from typing import Optional, Any


class DraggableFrameAdministrator:
    window_list = []
    make_mode = ''
    self_master = None

    def __init__(self,
                 master: Any,
                 make_mode: Optional[str] = ''):

        self.master = master
        self.make = make_mode

        pass

    def get_window_list(self):
        return self.window_list

    def start_change_state_detection(self):
        self.master.bind('<Configure>', self.on_resize)
        pass

    def on_resize(self, event):
        for i in range(0, len(self.window_list)):
            if self.window_list[i].opened:
                self.window_list[i].regenerate_position()

    @staticmethod
    def register_window(window: DraggableFrame):
        DraggableFrameAdministrator.window_list.append(window)

    def left_window(self, window):
        for index, value in enumerate(self.window_list):
            if window == value:
                del self.window_list[index]

    @staticmethod
    def sort_windows(window: DraggableFrame):
        window.border.lift()
        pass
