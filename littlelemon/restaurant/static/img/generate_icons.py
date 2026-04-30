"""Generate placeholder PWA icons (icon-192.png, icon-512.png).

Run:  python restaurant/static/img/generate_icons.py
Replace these with proper branded icons before publishing the APK.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def make_icon(size: int, out_path: Path) -> None:
    img = Image.new('RGB', (size, size), color=(61, 90, 79))  # Little Lemon green
    draw = ImageDraw.Draw(img)

    # Lemon-ish circle
    pad = size // 8
    draw.ellipse(
        [(pad, pad), (size - pad, size - pad)],
        fill=(245, 200, 66),
        outline=(255, 255, 255),
        width=max(2, size // 64),
    )

    # "LL" letters in the center
    try:
        font = ImageFont.truetype("arial.ttf", size // 3)
    except Exception:
        font = ImageFont.load_default()

    text = "LL"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(
        ((size - tw) / 2 - bbox[0], (size - th) / 2 - bbox[1]),
        text,
        fill=(61, 90, 79),
        font=font,
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, 'PNG')
    print(f"Wrote {out_path} ({size}x{size})")


if __name__ == '__main__':
    here = Path(__file__).parent
    make_icon(192, here / 'icon-192.png')
    make_icon(512, here / 'icon-512.png')
