from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


SOURCE_PATH = Path("tools/banner-300mbps-fuente.webp")
WIDE_PATH = Path("img/banner-fibra-300mbps-wide")
MOBILE_PATH = Path("img/banner-fibra-300mbps-mobile")
WIDE_SIZE = (2200, 780)
# Proporción del banner + franja inferior que el CSS móvil desvanece con su máscara.
MOBILE_SIZE = (1080, 740)
MOBILE_TOP = 20


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    scale = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - size[0]) // 2
    top = (resized.height - size[1]) // 2
    return resized.crop((left, top, left + size[0], top + size[1]))


def blurred_backdrop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    # Fondo rojo para rellenar los bordes: degradado vertical con el color de la
    # franja izquierda del banner (solo estadio rojo). La mediana por ventana
    # descarta los rayos de luz blancos para que no aparezcan como bandas.
    strip = image.crop((0, 0, 90, image.height)).resize((1, size[1]), Image.Resampling.BOX)
    rows = [strip.getpixel((0, y)) for y in range(size[1])]
    half = size[1] // 5
    column = Image.new("RGB", (1, size[1]))
    for y in range(size[1]):
        window = rows[max(0, y - half):y + half + 1]
        column.putpixel((0, y), tuple(sorted(c[i] for c in window)[len(window) // 2] for i in range(3)))
    backdrop = column.resize(size, Image.Resampling.BILINEAR).filter(ImageFilter.GaussianBlur(30))
    return ImageEnhance.Brightness(backdrop).enhance(0.95)


def fade_mask(size: tuple[int, int], fade_left: int, fade_right: int) -> Image.Image:
    mask = Image.new("L", size, 255)
    pixels = mask.load()
    for x in range(size[0]):
        alpha = 255
        if x < fade_left:
            alpha = round(255 * x / fade_left)
        elif x >= size[0] - fade_right:
            alpha = round(255 * (size[0] - 1 - x) / fade_right)
        if alpha < 255:
            for y in range(size[1]):
                pixels[x, y] = alpha
    return mask


def save(image: Image.Image, base: Path) -> None:
    rgb = image.convert("RGB")
    rgb.save(base.with_suffix(".webp"), "WEBP", quality=86, method=6)
    rgb.save(base.with_suffix(".png"), "PNG", optimize=True)


def build_wide(source: Image.Image) -> None:
    # Escritorio: el banner se coloca a la izquierda-centro y la derecha queda
    # libre para el formulario "Te llamamos gratis".
    canvas = blurred_backdrop(source, WIDE_SIZE)
    height = WIDE_SIZE[1]
    width = round(source.width * height / source.height)
    banner = source.resize((width, height), Image.Resampling.LANCZOS)
    x = 180
    canvas.paste(banner, (x, 0), fade_mask(banner.size, 120, 220))
    save(canvas, WIDE_PATH)


def build_mobile(source: Image.Image) -> None:
    # Móvil: el banner completo a lo ancho, casi arriba del todo.
    canvas = blurred_backdrop(source, MOBILE_SIZE)
    width = MOBILE_SIZE[0]
    height = round(source.height * width / source.width)
    banner = source.resize((width, height), Image.Resampling.LANCZOS)
    mask = fade_mask(banner.size[::-1], MOBILE_TOP, 60).transpose(Image.Transpose.TRANSPOSE)
    canvas.paste(banner, (0, MOBILE_TOP), mask)
    save(canvas, MOBILE_PATH)


def main() -> None:
    source = Image.open(SOURCE_PATH).convert("RGB")
    build_wide(source)
    build_mobile(source)


if __name__ == "__main__":
    main()
