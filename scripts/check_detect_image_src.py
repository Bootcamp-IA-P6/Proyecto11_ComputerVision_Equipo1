import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.detect_image import detect_image


if __name__ == "__main__":

    # Para llamar a la función detect_image que está en src hay que pasarle la imagen en modo path
    # y el modelo (que está en models/best.pt) en modo path
    # y como resultado en el directorio data/outputs devuelve un fichero annoted_pepsi_cocacola1.jpg (annoted_nombre_fichero_imagen.jpg)

    # Como llamar desde terminal a detect_image.py de src -> python -m src.detect_image --image data/demo/pepsi_cocacola1.jpg

    # Para el ejemplo de llamada la imagen pepsi_cocacola1.jpg debe estar en la carpeta data/demo/

    img = Path("data/demo/pepsi_cocacola1.jpg")
    model = Path("models/best.pt")
     
    out = detect_image(img, model)
    print(f"Saved annotated image to {out}")
