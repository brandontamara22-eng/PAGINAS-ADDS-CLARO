from pathlib import Path

from PIL import Image, ImageEnhance
from psd_tools import PSDImage


PSD_PATH = Path(r"C:\Users\Brandon\Downloads\BANNER PAGINA.psd")
OUTPUT_PATH = Path("img/banner-fibra-liga1-mobile.png")
CANVAS_SIZE = (1080, 1080)


def resize_to_width(image: Image.Image, width: int) -> Image.Image:
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def paste_layer(canvas: Image.Image, image: Image.Image, xy: tuple[int, int], width: int) -> None:
    prepared = resize_to_width(image.convert("RGBA"), width)
    canvas.alpha_composite(prepared, xy)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def main() -> None:
    psd = PSDImage.open(PSD_PATH)
    layers = [layer.composite().convert("RGBA") for layer in psd]

    background = cover(layers[0], CANVAS_SIZE).convert("RGBA")
    background = ImageEnhance.Color(background).enhance(1.04)
    canvas = background.copy()

    # La composición móvil usa las capas originales y conserva su proporción.
    paste_layer(canvas, layers[4], (44, 38), 510)   # Distribuidor autorizado
    paste_layer(canvas, layers[7], (876, 30), 158)  # Claro Hogar
    paste_layer(canvas, layers[3], (42, 138), 820)  # Internet Fibra Óptica
    paste_layer(canvas, layers[5], (626, 190), 438) # Jugadores
    paste_layer(canvas, layers[2], (44, 474), 472)  # 1000 Mbps
    paste_layer(canvas, layers[1], (500, 492), 366) # S/55
    paste_layer(canvas, layers[8], (155, 772), 570) # Liga 1 Max
    paste_layer(canvas, layers[6], (345, 936), 270) # 0 costo instalación

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(OUTPUT_PATH, "PNG", optimize=True)


if __name__ == "__main__":
    main()
