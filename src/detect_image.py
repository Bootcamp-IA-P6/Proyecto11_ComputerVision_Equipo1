import argparse
from pathlib import Path

from src.config import get_settings


def detect_image(image_path: Path, weights_path: Path, output_path: Path | None = None) -> Path:
    from ultralytics import YOLO

    settings = get_settings()
    model = YOLO(str(weights_path))
    results = model.predict(
        source=str(image_path),
        conf=settings.confidence_threshold,
        save=False,
    )
    result = results[0]
    annotated = result.plot()
    out = output_path or settings.outputs_dir / f"annotated_{image_path.name}"
    out.parent.mkdir(parents=True, exist_ok=True)

    import cv2

    cv2.imwrite(str(out), annotated)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect Coca-Cola and Pepsi logos in an image.")
    parser.add_argument("--image", type=Path, required=True)
    parser.add_argument("--weights", type=Path, default=None)
    parser.add_argument("--output", type=Path, default=None)
    args = parser.parse_args()

    settings = get_settings()
    settings.ensure_dirs()
    weights = args.weights or settings.model_path
    out = detect_image(args.image, weights, args.output)
    print(f"Saved annotated image to {out}")


if __name__ == "__main__":
    main()
