from src.ascii.art_converter import ArtConverter


async def get_ascii_art(font_size, file):
    contents = await file.read()
    font = 72 if font_size > 72 else font_size
    img_art = ArtConverter(contents, font_size=font)
    img_art.draw()
    return img_art.save_image()
