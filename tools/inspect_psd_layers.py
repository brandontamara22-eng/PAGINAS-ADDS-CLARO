from pathlib import Path

from PIL import Image, ImageDraw
from psd_tools import PSDImage


PSD_PATH = Path(r"C:\Users\Brandon\Downloads\BANNER PAGINA.psd")
OUT_DIR = Path("tmp/psd-layers")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    psd = PSDImage.open(PSD_PATH)
    cards = []

    for index, layer in enumerate(psd):
        image = layer.composite()
        if image is None:
            continue
        image.save(OUT_DIR / f"{index:02d}.png")
        preview = image.copy()
        preview.thumbnail((360, 210), Image.Resampling.LANCZOS)
        card = Image.new("RGB", (390, 270), "#ededed")
        x = (card.width - preview.width) // 2
        y = 34 + (210 - preview.height) // 2
        if preview.mode == "RGBA":
            card.paste(preview, (x, y), preview)
        else:
            card.paste(preview, (x, y))
        draw = ImageDraw.Draw(card)
        draw.text((12, 10), f"{index}: {layer.name}", fill="#111111")
        draw.text((12, 248), f"bbox={tuple(layer.bbox)}", fill="#333333")
        cards.append(card)

    cols = 3
    rows = (len(cards) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 390, rows * 270), "white")
    for index, card in enumerate(cards):
        sheet.paste(card, ((index % cols) * 390, (index // cols) * 270))
    sheet.save(OUT_DIR / "contact-sheet.jpg", quality=92)


if __name__ == "__main__":
    main()
