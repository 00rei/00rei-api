from io import BytesIO

import pygame as pg
import cv2
import numpy as np


class ArtConverter:
    def __init__(self, content, font_size=32, color_lvl=8):
        pg.init()
        self.content = content
        self.COLOR_LVL = color_lvl
        self.image, self.gray_image = self.get_image()
        self.RES = self.WIDTH, self.HEIGHT = self.image.shape[0], self.image.shape[1]
        self.surface = pg.display.set_mode(self.RES, pg.HIDDEN)

        self.ASCII_CHARS = ' ixzao*#MW&8%B@$'
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        self.font = pg.font.Font(None, font_size)
        self.font.set_bold(True)

        self.CHAR_STEP = int(font_size * 0.6)
        self.PALETTE, self.COLOR_COEFF = self.create_palette()

    def draw_converted_image(self):
        char_indices = self.gray_image // self.ASCII_COEFF
        color_indices = self.image // self.COLOR_COEFF
        for x in range(0, self.WIDTH, self.CHAR_STEP):
            for y in range(0, self.HEIGHT, self.CHAR_STEP):
                char_index = char_indices[x, y]
                if char_index:
                    char = self.ASCII_CHARS[char_index]
                    color = tuple(color_indices[x, y])
                    self.surface.blit(self.PALETTE[char][color], (x, y))

    def create_palette(self):
        colors, color_coeff = np.linspace(0, 255, num=self.COLOR_LVL, dtype=int, retstep=True)
        color_palette = [np.array([r, g, b]) for r in colors for g in colors for b in colors]
        palette = dict.fromkeys(self.ASCII_CHARS, None)
        color_coeff = int(color_coeff)
        for char in palette:
            char_palette = {}
            for color in color_palette:
                color_key = tuple(color // color_coeff)
                char_palette[color_key] = self.font.render(char, False, tuple(color))
            palette[char] = char_palette
        return palette, color_coeff

    def get_image(self):
        raw_img = np.frombuffer(self.content, np.uint8)
        cv2_image = cv2.imdecode(raw_img, cv2.IMREAD_COLOR)
        transposed_image = cv2.transpose(cv2_image)
        image = cv2.cvtColor(transposed_image, cv2.COLOR_RGB2BGR)
        gray_image = cv2.cvtColor(transposed_image, cv2.COLOR_BGR2GRAY)

        return image, gray_image

    def draw(self):
        self.draw_converted_image()

    def save_image(self):
        pygame_image = pg.surfarray.array3d(self.surface)
        cv2_img = cv2.transpose(pygame_image)
        cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_RGB2BGR)
        _, img_encoded = cv2.imencode(".png", cv2_img)
        image_stream = BytesIO(img_encoded.tobytes())
        image_stream.seek(0)

        return image_stream
