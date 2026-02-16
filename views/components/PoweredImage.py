import customtkinter
import tkinter
from typing import Union, Tuple, Callable, Optional, Any
import importlib.resources as pkg_resources
from PIL import Image, ImageTk, ImageFilter, ImageSequence
from customtkinter import CTkFont
from customtkinter import CTkImage
import cairosvg
import io


class PoweredImage:

    def __init__(self,
                 master: Any,
                 image_path: Optional[str] = 'bs-box',
                 size: Tuple[int, int] = (200, 200),
                 color: Optional[Union[tuple[int, int, int], None]] = None,
                 rotation: Optional[float] = 0,
                 rotation_expansion: Optional[bool] = True,
                 image_filter: Optional[str] = ''
                 ):

        self.general_label = customtkinter.CTkLabel(master, text='')

        if image_path != '':
            if image_path[:2] == 'bs':
                path_cut = image_path.split('bs-', 1)
                img_name = path_cut[1] if len(path_cut) > 1 else image_path

                icon_package = f"Views.components.bootstrap.icons"
                icon_file = f"{img_name}.svg"

                with pkg_resources.open_binary(icon_package, icon_file) as svg_file:

                    png_data = cairosvg.svg2png(file_obj=svg_file, output_width=size[0], output_height=size[1])
                    image = Image.open(io.BytesIO(png_data))

                    if color is not None:
                        image = self.change_black_to_white(image, color)

                    image = image.resize(size, Image.Resampling.LANCZOS)
                    image = image.rotate(rotation, expand=rotation_expansion)
                    if image_filter != '':
                        image = self.apply_filter(image, image_filter)

                    self._image = customtkinter.CTkImage(light_image=image, size=size)

                    self.general_label.configure(image=self._image)
            else:
                if image_path.lower().endswith('.svg'):
                    with open(image_path, 'rb') as svg_file:
                        png_data = cairosvg.svg2png(file_obj=svg_file, output_width=size[0],
                                                    output_height=size[1])
                        image = Image.open(io.BytesIO(png_data))
                        self._image = customtkinter.CTkImage(light_image=image, size=size)

                        self.general_label.configure(image=self._image)
                else:
                    image = Image.open(image_path)

                    if image_path.lower().endswith('.gif'):
                        frames = [ImageTk.PhotoImage(frame.copy()) for frame in ImageSequence.Iterator(image)]

                        def update(ind):
                            frame = frames[ind]
                            ind = (ind + 1) % len(frames)
                            self.general_label.configure(image=frame)
                            self.general_label.after(100, update, ind)

                        update(0)
                    else:
                        if color is not None:
                            image = self.change_black_to_white(image, color)
                        image = image.resize(size, Image.Resampling.LANCZOS)
                        self._image = customtkinter.CTkImage(light_image=image, size=size)
                        self.general_label.configure(image=self._image)
                        pass

        pass

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

    def pack(self, **kwargs):
        self.general_label.pack(**kwargs)

    def place(self, **kwargs):
        self.general_label.place(**kwargs)

    @staticmethod
    def apply_filter(image, image_filter: str):

        if image_filter != '':
            if image_filter == 'blur':
                image = image.filter(ImageFilter.BLUR)
            elif image_filter == 'contour':
                image = image.filter(ImageFilter.CONTOUR)
            elif image_filter == 'detail':
                image = image.filter(ImageFilter.DETAIL)
            elif image_filter == 'edge_enhance':
                image = image.filter(ImageFilter.EDGE_ENHANCE)
            elif image_filter == 'edge_enhance_more':
                image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
            elif image_filter == 'emboss':
                image = image.filter(ImageFilter.EMBOSS)
            elif image_filter == 'find_edges':
                image = image.filter(ImageFilter.FIND_EDGES)
            elif image_filter == 'sharpen':
                image = image.filter(ImageFilter.SHARPEN)
            elif image_filter == 'smooth':
                image = image.filter(ImageFilter.SMOOTH)
            elif image_filter == 'smooth_more':
                image = image.filter(ImageFilter.SMOOTH_MORE)

            return image

        pass

