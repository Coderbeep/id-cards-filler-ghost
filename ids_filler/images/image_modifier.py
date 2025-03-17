import textwrap

from ids_filler import *
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import FreeTypeFont
from ids_filler.config import TextType

class ImageModifier:
    @classmethod
    def insert_text(
            cls,
            image: Image.Image,
            text: str,
            text_color: str,
            text_type: TextType,
            text_start_height: int,
            text_start_width: int
    ) -> None:
        lines = textwrap.wrap(text, width=35)
        width, _ = image.size

        initial_size = 400 if text_type != TextType.AFFILIATION else 130
        print(initial_size)
        font = cls._get_font_for_text_type(text_type)
        while True:
            text_width = cls._calculate_text_width(lines, font)
            if text_width > width - 400:
                initial_size -= 10
                font = cls._get_font_for_text_type(text_type, initial_size)
            else:
                break


        cls._insert_text(image, lines, font, text_color, text_start_height, text_start_width)

    @staticmethod
    def _calculate_text_width(lines: list[str], font: FreeTypeFont) -> int:
        return max(font.getbbox(line)[2] for line in lines)
    
    @staticmethod
    def _get_font_for_text_type(text_type: TextType, size: int = 400) -> FreeTypeFont:
        if text_type == TextType.NAME:
            return ImageFont.truetype(font=NAME_FONT_PATH, size=size or 400)
        elif text_type == TextType.SURNAME:
            return ImageFont.truetype(font=SURNAME_FONT_PATH, size=size or 400)
        elif text_type == TextType.AFFILIATION:
            return ImageFont.truetype(font=AFFILIATION_FONT_PATH, size=size or 120)
        else:
            raise ValueError(f"Unknown text type: {text_type}")
    
    @staticmethod
    def _insert_text(
            image: Image.Image,
            lines: list[str],
            font: FreeTypeFont,
            text_color: str,
            text_start_height: int,
            text_start_width: int
    ) -> None:
        draw = ImageDraw.Draw(image)
        image_width, image_height = image.size
        y_text = text_start_height
        for line in lines:
            _, _, line_width, line_height = font.getbbox(line)
            draw.text(
                xy=(text_start_width, y_text),
                text=line,
                font=font,
                fill=text_color
            )
            y_text += line_height
