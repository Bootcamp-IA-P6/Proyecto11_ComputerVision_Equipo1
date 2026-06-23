from pathlib import Path
from ultralytics import YOLO
import cv2


def count_brands_in_video(
    video_path: Path,
    weights_path: Path,
    confidence: float = 0.5,
):
    model = YOLO(str(weights_path))

    cap = cv2.VideoCapture(str(video_path))

    counts = {
        "cocacola": 0,
        "pepsi": 0,
    }

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        results = model.predict(
            source=frame,
            conf=confidence,
            verbose=False
        )

        result = results[0]

        for box in result.boxes:
            class_id = int(box.cls[0])
            class_name = model.names[class_id]

            if class_name in counts:
                counts[class_name] += 1

    cap.release()

    return counts

if __name__ == "__main__":

    counts = count_brands_in_video(
        #Path("data/demo/cocacola1-hd_1920_1080_30fps.mp4"),  #{'cocacola': 0, 'pepsi': 0}
        #Path("data/demo/pepsi_cocacola-hd_1920_1080_30fps.mp4"), #{'cocacola': 0, 'pepsi': 0}
        #Path("data/demo/cocacola2-hd_1920_1080_30fps.mp4"), #{'cocacola': 0, 'pepsi': 0}
        #Path("data/demo/cocacola3-2192786305-640_adpp_is.mp4"), #{'cocacola': 0, 'pepsi': 0} 2 min
        #Path("data/demo/cocacola4-1401761579-640_adpp_is.mp4"), #{'cocacola': 0, 'pepsi': 0} 3 min 10 sg
        Path("data/demo/pepsi1-hd_1920_1080_30fps.mp4"), #{'cocacola': 0, 'pepsi': 0} 2 min 48 sg
        Path("models/best.pt")
    )

    print(counts)