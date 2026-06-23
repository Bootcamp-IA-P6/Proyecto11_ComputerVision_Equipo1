from pathlib import Path
from ultralytics import YOLO
import cv2


def count_unique_brands(
    video_path: Path,
    weights_path: Path,
    confidence: float = 0.5,
):
    model = YOLO(str(weights_path))

    cap = cv2.VideoCapture(str(video_path))

    cocacola_ids = set()
    pepsi_ids = set()

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        results = model.track(
            frame,
            conf=confidence,
            persist=True,
            verbose=False
        )

        result = results[0]

        if result.boxes.id is None:
            continue

        for box in result.boxes:

            track_id = int(box.id[0])
            class_id = int(box.cls[0])

            class_name = model.names[class_id]

            if class_name == "cocacola":
                cocacola_ids.add(track_id)

            elif class_name == "pepsi":
                pepsi_ids.add(track_id)

    cap.release()

    return {
        "cocacola": len(cocacola_ids),
        "pepsi": len(pepsi_ids),
    }

if __name__ == "__main__":

        #Path("data/demo/cocacola1-hd_1920_1080_30fps.mp4"),  #{'cocacola': 0, 'pepsi': 0} 1 min 31 sg
        #Path("data/demo/pepsi_cocacola-hd_1920_1080_30fps.mp4"), #{'cocacola': 0, 'pepsi': 0} 2 min 41 sg
        #Path("data/demo/cocacola2-hd_1920_1080_30fps.mp4"), #
        #Path("data/demo/cocacola3-2192786305-640_adpp_is.mp4"), #
        #Path("data/demo/cocacola4-1401761579-640_adpp_is.mp4"), #
        #Path("data/demo/pepsi1-hd_1920_1080_30fps.mp4"), #

    result = count_unique_brands(
        Path("data/demo/cocacola2-hd_1920_1080_30fps.mp4"),
        Path("models/best.pt"),
        0.5
    )

    print(result)