import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.detect_image import detect_image


if __name__ == "__main__":

    img = Path("data/demo/cocacola1.jpg")
    model = Path("models/best.pt")
     
    out = detect_image(img, model)
    print(f"Saved annotated image to {out}")