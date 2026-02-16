from enum import Enum
import time
import threading
import customtkinter


class Anchor(Enum):
    N = 'n'
    S = 's'
    E = 'e'
    W = 'w'
    NE = 'ne'
    NW = 'nw'
    SE = 'se'
    SW = 'sw'


class NotificationManager:

    def __init__(self,
                 anchor: Anchor = Anchor.NW,
                 separation: int = 5
                 ):

        self.anchor = anchor
        self.separation: int = separation
        self._notifications: list[dict] = []
        self._queue = []

    def register_notification(
            self,
            frame: customtkinter.CTkFrame | customtkinter.CTkScrollableFrame,
            notification_id: str,
            dismiss_seconds: int | None = 10,
            default_width: int | None = None,
            destroy_on_exit: bool = True
    ):

        notification = {
            "id": notification_id,
            "frame": frame,
            "position": (0, 0),
            "dismiss": dismiss_seconds,
            "active": True,
            "master": frame.master,
            "d_width": default_width,
            'destroy': destroy_on_exit,
            "time_running": False
        }

        self._notifications.append(notification)

    def pop_by_id(self, notification_id: str):

        pop_queue = -1

        for index, i in enumerate(self._queue):
            if i["id"] == notification_id:
                i["frame"].place_forget()
                pop_queue = index

        if pop_queue >= 0:
            if (len(self._queue) - 1) >= pop_queue:
                self._notifications.pop(pop_queue)
            self._queue.pop(pop_queue)

        notification_pop = -1

        for index, i in enumerate(self._notifications):
            if i["id"] == notification_id:
                i["frame"].place_forget()
                notification_pop = index

        if notification_pop >= 0:
            if (len(self._notifications) - 1) >= notification_pop:
                self._notifications.pop(notification_pop)

        self.update()

    def time_warp(self, notification_id: str):

        pop_queue = -1

        for index, i in enumerate(self._queue):
            if i["id"] == notification_id:
                if not i["destroy"]:
                    i["active"] = False
                else:
                    i["frame"].place_forget()
                    pop_queue = index
                    pass

        if pop_queue >= 0:
            self._queue.pop(pop_queue)

        notification_pop = -1

        for index, i in enumerate(self._notifications):
            if i["id"] == notification_id:
                if not i["destroy"]:
                    i["active"] = False
                else:
                    i["frame"].place_forget()
                    notification_pop = index

        if notification_pop >= 0:
            self._notifications.pop(notification_pop)

        self.update()

    def show_by_id(self, notification_id: str = ''):

        for notification in self._notifications:
            if notification["id"] == notification_id:

                if notification not in self._queue:
                    self._queue.append(notification)

                if not notification["time_running"] and notification["dismiss"] is not None:
                    notification['master'].after(notification["dismiss"] * 1000, lambda: self.time_warp(notification_id))

        self.calculate_queue_positions()

        for i in self._queue:
            if i["active"]:
                i["frame"].place(x=i["position"][0], y=i["position"][1])
            else:
                i["frame"].place_forget()
        pass

    def calculate_queue_positions(self):

        masters_pos_y_dict: dict = {}
        masters_cont_height_dict: dict = {}

        for i in self._queue:
            if (
                    isinstance(i["master"], customtkinter.CTkFrame) or
                    isinstance(i["master"], customtkinter.CTk) or
                    isinstance(i["master"], customtkinter.CTkScrollableFrame)
            ):
                # create individual 'y_coordinate' by master instance
                if str(id(i["master"])) not in masters_pos_y_dict:
                    
                    if self.anchor == Anchor.N or self.anchor == Anchor.NE or self.anchor == Anchor.NW:
                        masters_pos_y_dict[str(id(i["master"]))] = self.separation
                        masters_cont_height_dict[str(id(i["master"]))] = 0
                    elif self.anchor == Anchor.S or self.anchor == Anchor.SE or self.anchor == Anchor.SW:
                        w_height = i["master"].winfo_height()
                        masters_pos_y_dict[str(id(i["master"]))] = w_height - self.separation
                        masters_cont_height_dict[str(id(i["master"]))] = 0
                    elif self.anchor == Anchor.E or self.anchor == Anchor.W:
                        w_height = i["master"].winfo_height()
                        masters_pos_y_dict[str(id(i["master"]))] = int(w_height / 2)
                        masters_cont_height_dict[str(id(i["master"]))] = 0

        for i in self._queue:

            if (
                    isinstance(i["frame"], customtkinter.CTkFrame) or
                    isinstance(i["frame"], customtkinter.CTkScrollableFrame)
            ):

                if (
                        isinstance(i["master"], customtkinter.CTk) or
                        isinstance(i["master"], customtkinter.CTkFrame) or
                        isinstance(i["master"], customtkinter.CTkScrollableFrame)
                ):

                    if self.anchor == Anchor.N:

                        if str(id(i["master"])) in masters_pos_y_dict:

                            i["frame"].update()
                            w_width = i["master"].winfo_width()
                            if i["d_width"] is not None:
                                f_width = i["d_width"]
                            else:
                                f_width: int = i["frame"].winfo_width()
                            f_height: int = i["frame"].winfo_height()
                            center_corner_y = masters_pos_y_dict[str(id(i["master"]))]
                            center_corner_x = int((w_width / 2) - (f_width / 2))
                            # print(f'| w_width: {w_width} | f_width: {f_width} | x: {str(center_corner_x)} | y: {str(center_corner_y)} | id: {str(id(i["master"]))}')
                            i["position"] = (center_corner_x, center_corner_y)
                            masters_pos_y_dict[str(id(i["master"]))] += self.separation + f_height

                    if self.anchor == Anchor.S:

                        if str(id(i["master"])) in masters_pos_y_dict:

                            i["frame"].update()
                            w_width = i["master"].winfo_width()
                            w_height = i["master"].winfo_height()
                            f_width: int = i["frame"].winfo_width()
                            f_height: int = i["frame"].winfo_height()
                            center_corner_y = masters_pos_y_dict[str(id(i["master"]))] - f_height - self.separation
                            center_corner_x = (w_width / 2) - (f_width / 2)
                            i["position"] = (center_corner_x, center_corner_y)
                            masters_pos_y_dict[str(id(i["master"]))] = center_corner_y

                            # print(
                            #     f'| res_h = {masters_pos_y_dict[str(id(i["master"]))]} | f_height = {f_height} | w_height = {w_height} | w_width: {w_width} | f_width: {f_width} | x: {str(center_corner_x)} | y: {str(center_corner_y)} | master_id: {str(id(i["master"]))} | id: {str(id(i["frame"]))} | color: {i["frame"].cget("fg_color")}'
                            # )

                    if self.anchor == Anchor.E:

                        if str(id(i["master"])) in masters_pos_y_dict:

                            i["frame"].update()
                            w_width = i["master"].winfo_width()
                            w_height = i["master"].winfo_height()
                            f_width: int = i["frame"].winfo_width()
                            f_height: int = i["frame"].winfo_height()
                            masters_cont_height_dict[str(id(i["master"]))] += f_height + self.separation
                            center_corner_y = (masters_pos_y_dict[str(id(i["master"]))] - f_height - self.separation)
                            center_corner_x = self.separation
                            i["position"] = (center_corner_x, center_corner_y)
                            masters_pos_y_dict[str(id(i["master"]))] = center_corner_y
                            # print(
                            #     f'| res_gen_h: {masters_cont_height_dict[str(id(i["master"]))]} | res_h = {masters_pos_y_dict[str(id(i["master"]))]} | f_height = {f_height} | w_height = {w_height} | w_width: {w_width} | f_width: {f_width} | x: {str(center_corner_x)} | y: {str(center_corner_y)} | master_id: {str(id(i["master"]))} | id: {str(id(i["frame"]))} | color: {i["frame"].cget("fg_color")}'
                            # )

                        pass

                    if self.anchor == Anchor.W:

                        if str(id(i["master"])) in masters_pos_y_dict:

                            i["frame"].update()
                            w_width = i["master"].winfo_width()
                            w_height = i["master"].winfo_height()
                            f_width: int = i["frame"].winfo_width()
                            f_height: int = i["frame"].winfo_height()
                            masters_cont_height_dict[str(id(i["master"]))] += f_height + self.separation
                            center_corner_y = (masters_pos_y_dict[str(id(i["master"]))] - f_height - self.separation)
                            center_corner_x = w_width - f_width - self.separation
                            i["position"] = (center_corner_x, center_corner_y)
                            masters_pos_y_dict[str(id(i["master"]))] = center_corner_y
                            # print(
                            #     f'| res_gen_h: {masters_cont_height_dict[str(id(i["master"]))]} | res_h = {masters_pos_y_dict[str(id(i["master"]))]} | f_height = {f_height} | w_height = {w_height} | w_width: {w_width} | f_width: {f_width} | x: {str(center_corner_x)} | y: {str(center_corner_y)} | master_id: {str(id(i["master"]))} | id: {str(id(i["frame"]))} | color: {i["frame"].cget("fg_color")}'
                            # )

                        pass

                    if self.anchor == Anchor.NE:

                        if str(id(i["master"])) in masters_pos_y_dict:
                            i["frame"].update()
                            w_width = i["master"].winfo_width()

                            if i["d_width"] is not None:
                                f_width = i["d_width"]
                            else:
                                f_width: int = i["frame"].winfo_width()

                            f_height: int = i["frame"].winfo_height()
                            center_corner_y = masters_pos_y_dict[str(id(i["master"]))]
                            center_corner_x = self.separation
                            # print(
                            #     f'| w_width: {w_width} | f_width: {f_width} | x: {str(center_corner_x)} | y: {str(center_corner_y)} | id: {str(id(i["master"]))}')
                            i["position"] = (center_corner_x, center_corner_y)
                            masters_pos_y_dict[str(id(i["master"]))] += center_corner_y + self.separation + f_height

                    if self.anchor == Anchor.SE:

                        if str(id(i["master"])) in masters_pos_y_dict:

                            i["frame"].update()
                            w_width = i["master"].winfo_width()
                            w_height = i["master"].winfo_height()
                            f_width: int = i["frame"].winfo_width()
                            f_height: int = i["frame"].winfo_height()
                            center_corner_y = masters_pos_y_dict[str(id(i["master"]))] - f_height - self.separation
                            center_corner_x = self.separation
                            i["position"] = (center_corner_x, center_corner_y)
                            masters_pos_y_dict[str(id(i["master"]))] = center_corner_y

                            # print(
                            #     f'| res_h = {masters_pos_y_dict[str(id(i["master"]))]} | f_height = {f_height} | w_height = {w_height} | w_width: {w_width} | f_width: {f_width} | x: {str(center_corner_x)} | y: {str(center_corner_y)} | master_id: {str(id(i["master"]))} | id: {str(id(i["frame"]))} | color: {i["frame"].cget("fg_color")}'
                            # )

                    if self.anchor == Anchor.NW:

                        if str(id(i["master"])) in masters_pos_y_dict:
                            i["frame"].update()
                            w_width = i["master"].winfo_width()
                            if i["d_width"] is not None:
                                f_width = i["d_width"]
                            else:
                                f_width: int = i["frame"].winfo_width()
                            f_height: int = i["frame"].winfo_height()
                            center_corner_y = masters_pos_y_dict[str(id(i["master"]))]
                            center_corner_x = w_width - f_width - self.separation
                            # print(
                            #     f'| w_width: {w_width} | f_width: {f_width} | x: {str(center_corner_x)} | y: {str(center_corner_y)} | id: {str(id(i["master"]))}')
                            # i["position"] = (center_corner_x, center_corner_y)
                            masters_pos_y_dict[str(id(i["master"]))] += center_corner_y + self.separation + f_height

                    if self.anchor == Anchor.SW:

                        if str(id(i["master"])) in masters_pos_y_dict:

                            i["frame"].update()
                            w_width = i["master"].winfo_width()
                            w_height = i["master"].winfo_height()
                            f_width: int = i["frame"].winfo_width()
                            f_height: int = i["frame"].winfo_height()
                            center_corner_y = masters_pos_y_dict[str(id(i["master"]))] - f_height - self.separation
                            center_corner_x = w_width - f_width - self.separation
                            i["position"] = (center_corner_x, center_corner_y)
                            masters_pos_y_dict[str(id(i["master"]))] = center_corner_y

                            # print(
                            #     f'| res_h = {masters_pos_y_dict[str(id(i["master"]))]} | f_height = {f_height} | w_height = {w_height} | w_width: {w_width} | f_width: {f_width} | x: {str(center_corner_x)} | y: {str(center_corner_y)} | master_id: {str(id(i["master"]))} | id: {str(id(i["frame"]))} | color: {i["frame"].cget("fg_color")}'
                            # )

            else:

                i["active"] = False

        for i in self._queue:

            if self.anchor == Anchor.E or self.anchor == Anchor.W:
                center_corner_y = i["position"][1] + (masters_cont_height_dict[str(id(i["master"]))] / 2)
                i["position"] = (i["position"][0], center_corner_y)

            pass

    def update(self):
        self.show_by_id()
