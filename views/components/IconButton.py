import customtkinter
import tkinter
from typing import Union, Tuple, Callable, Optional, Any
import importlib.resources as pkg_resources
from PIL import Image
from customtkinter import CTkFont
import cairosvg
import io


class IconButton:
    def __init__(self,
                 master: Any,
                 width: int = 140,
                 height: int = 28,
                 corner_radius: Optional[int] = None,
                 button_border_width: Optional[int] = 1,
                 border_spacing: int = 2,

                 bg_color: Union[str, Tuple[str, str]] = "transparent",
                 fg_color: Optional[Union[str, Tuple[str, str]]] = None,
                 button_hover_color: Optional[Union[str, Tuple[str, str]]] = 'gray',
                 button_border_color: Optional[Union[str, Tuple[str, str]]] = 'white',
                 text_color: Optional[Union[str, Tuple[str, str]]] = ('black', 'white'),
                 text_color_disabled: Optional[Union[str, Tuple[str, str]]] = None,

                 background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                 round_width_to_even_numbers: bool = True,
                 round_height_to_even_numbers: bool = True,

                 text: str = "---",
                 font: Optional[Union[tuple, CTkFont]] = None,
                 text_variable: Union[tkinter.Variable, None] = None,
                 image_path: Optional[str] = 'bs-box',  # use bs-icon-name to use bootstrap icons
                 state: str = "normal",
                 hover: bool = True,
                 command: Union[Callable[[], Any], None] = None,
                 compound: str = "left",
                 anchor: str = "center",
                 button_x_padding: Optional[int] = 5,
                 button_y_padding: Optional[int] = 5,
                 button_height: Optional[int] = 32,
                 button_width: Optional[int] = 32,
                 icon_frame_height: Optional[int] = 32,
                 icon_frame_width: Optional[int] = 32,
                 icon_frame_x_padding: Optional[int] = 0,
                 icon_frame_y_padding: Optional[int] = 0,
                 icon_side: Optional[str] = 'left',  # left - right
                 icon_x_padding: Optional[int] = 5,
                 icon_y_padding: Optional[int] = 5,
                 icon_size: Optional[tuple[int, int]] = (32, 32),
                 icon_color: Optional[Union[tuple[int, int, int], None]] = None,
                 icon_dark_color: Optional[Union[tuple[int, int, int], None]] = None,
                 button_frame_x_padding: Optional[int] = 5,
                 button_frame_y_padding: Optional[int] = 5,
                 button_corner_radius: Optional[int] = 5,
                 button_fg_color: Optional[Union[str, Tuple[str, str]]] = 'transparent',
                 button_bg_color: Optional[Union[str, Tuple[str, str]]] = 'transparent',
                 button_frame_color: Optional[Union[str, Tuple[str, str]]] = 'transparent',
                 icon_frame_fg_color: Optional[Union[str, Tuple[str, str]]] = 'transparent'
                 ):

        self._image = None

        if image_path != '':
            if image_path[:2] == 'bs':
                path_cut = image_path.split('bs-', 1)
                img_name = path_cut[1] if len(path_cut) > 1 else image_path

                icon_package = f"Views.components.bootstrap.icons"
                icon_file = f"{img_name}.svg"

                with pkg_resources.open_binary(icon_package, icon_file) as svg_file:

                    png_data = cairosvg.svg2png(file_obj=svg_file, output_width=icon_size[0], output_height=icon_size[1])
                    image = Image.open(io.BytesIO(png_data))
                    image_black = Image.open(io.BytesIO(png_data))

                    if icon_color is not None:
                        image = self.change_black_to_white(image, icon_color)
                        if icon_dark_color is not None:
                            image_black = self.change_black_to_white(image, icon_dark_color)

                    image = image.resize(icon_size, Image.Resampling.LANCZOS)
                    image_black = image_black.resize(icon_size, Image.Resampling.LANCZOS)

                    self._image = customtkinter.CTkImage(light_image=image, dark_image=image_black, size=icon_size)
            else:

                if image_path.lower().endswith('.svg'):
                    with open(image_path, 'rb') as svg_file:
                        png_data = cairosvg.svg2png(file_obj=svg_file, output_width=icon_size[0],
                                                    output_height=icon_size[1])
                        image = Image.open(io.BytesIO(png_data))
                        image_black = Image.open(io.BytesIO(png_data))
                else:
                    image = Image.open(image_path)
                    image_black = Image.open(image_path)

                if icon_color is not None:
                    image = self.change_black_to_white(image, icon_color)
                    if icon_dark_color is not None:
                        image_black = self.change_black_to_white(image, icon_dark_color)
                image = image.resize(icon_size, Image.Resampling.LANCZOS)
                image_black = image_black.resize(icon_size, Image.Resampling.LANCZOS)
                self._image = customtkinter.CTkImage(light_image=image, dark_image=image_black, size=icon_size)

                pass

        self.general_frame = customtkinter.CTkFrame(master, width=width, height=height,
                                                    corner_radius=corner_radius,
                                                    fg_color=fg_color,
                                                    bg_color=bg_color
                                                    )

        self.icon_frame = customtkinter.CTkFrame(self.general_frame,
                                                 height=icon_frame_height,
                                                 width=icon_frame_width,
                                                 fg_color=icon_frame_fg_color
                                                 )

        if self._image is not None:
            self.label = customtkinter.CTkLabel(self.icon_frame, image=self._image, text='',
                                                width=icon_frame_width,
                                                height=icon_frame_height,
                                                fg_color=icon_frame_fg_color)
            self.label.pack(padx=icon_x_padding, pady=icon_y_padding)

        self.general_button_frame = customtkinter.CTkFrame(self.general_frame, button_corner_radius,
                                                           fg_color=button_frame_color)
        self.general_button_frame.pack(padx=button_frame_x_padding, pady=button_frame_y_padding, fill='both',
                                       side=(tkinter.RIGHT if icon_side == 'left' else tkinter.LEFT),
                                       expand=True
                                       )

        self.general_button = customtkinter.CTkButton(self.general_button_frame,
                                                      width=button_width, height=button_height,
                                                      corner_radius=button_corner_radius,
                                                      border_width=button_border_width,
                                                      border_spacing=border_spacing,
                                                      bg_color=button_bg_color,
                                                      fg_color=button_fg_color,
                                                      hover_color=button_hover_color,
                                                      border_color=button_border_color,
                                                      text_color=text_color,
                                                      text_color_disabled=text_color_disabled,
                                                      background_corner_colors=background_corner_colors,
                                                      round_width_to_even_numbers=round_width_to_even_numbers,
                                                      round_height_to_even_numbers=round_height_to_even_numbers,
                                                      text=text,
                                                      font=font,
                                                      textvariable=text_variable,
                                                      state=state,
                                                      hover=hover,
                                                      command=command,
                                                      compound=compound,
                                                      anchor=anchor
                                                      )

        self.general_button.pack(padx=button_x_padding, pady=button_y_padding, fill='both', expand=True)

        if icon_side != tkinter.RIGHT and icon_side != tkinter.LEFT:
            raise AttributeError(icon_side + ' is not a possible side, use: [left, right]')
        else:
            self.icon_frame.pack(padx=icon_frame_x_padding, pady=icon_frame_y_padding, side=icon_side, fill='both', expand=False)
        pass

    def pack(self, **kwargs):
        self.general_frame.pack(**kwargs)
        pass

    def place(self, **kwargs):
        self.place(**kwargs)

    @staticmethod
    def change_black_to_white(image, color):
        image = image.convert("RGBA")

        white_image = Image.new("RGBA", image.size, (255, 255, 255, 0))

        img_pixels = image.load()
        white_pixels = white_image.load()

        threshold = 50

        for y in range(image.height):
            for x in range(image.width):
                r, g, b, a = img_pixels[x, y]
                if r < threshold and g < threshold and b < threshold:
                    white_pixels[x, y] = (color[0], color[1], color[2], a)
                else:
                    white_pixels[x, y] = img_pixels[x, y]

        return white_image
