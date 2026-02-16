from typing import Union, Tuple, Optional, Any

import customtkinter


class DynamicSearchItem:
    text = ''
    component = None
    pack_props = None

    def __init__(self,
                 text,
                 component: customtkinter.CTkFrame):
        self.text = text
        self.component = component

        pass

    def set_pack_properties(self, **kwargs):
        self.pack_props = kwargs

    def get_pack_props(self):
        return self.pack_props
