from ultralytics import YOLO
import cv2

MODEL = "models/best.pt"

#IMAGE = "data/demo/cocacola1.jpg"
#IMAGE = "data/demo/pepsi2.jpg"
#IMAGE = "data/demo/pepsi_cocacola2.jpg"
#IMAGE = "data/demo/pepsi_cocacola1.jpg"
IMAGE = "data/demo/pepsi_cocacola3.jpg"

def detect_image(model_trained, image_test):
    # 1. Cargar tu modelo entrenado
    # Reemplaza 'ruta/a/tu/mejor_modelo.pt' por la ubicación de tus pesos (suele estar en 'runs/train/exp/weights/best.pt')
    #model = YOLO("models/best.pt")
    model = YOLO(model_trained)

    # 2. Pasar la imagen que deseas analizar
    # Reemplaza 'ruta/a/tu/imagen.jpg' por la imagen que quieres probar
    #imagen_prueba = "data/demo/cocacola1.jpg"
    #imagen_prueba = image_test

    # 3. Realizar la predicción
    # save=True guardará automáticamente la imagen con las cajas delimitadoras (bounding boxes)
    #results = model.predict(source=imagen_prueba, save=True, conf=0.5)
    results = model.predict(source=image_test, save=True, conf=0.5)

    # Los resultados se pueden ver en la carpeta runs/detect/predict/cocacola1.jpg
    #print("¡Detección completada! Revisa la carpeta generada para ver la imagen procesada.")
    #print(results[0])

    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls = int(box.cls[0])

        print(
            f"{model.names[cls]} "
            f"({conf:.2f}) "
            f"[{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]"
        )



def detect_image_with_results(model_trained, image_test):
    model = YOLO(model_trained)

    results = model.predict(source=image_test, save=True, conf=0.5)

    # Imagen con las detecciones dibujadas
    annotated_img = results[0].plot()

    cv2.imshow("Detección", annotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    detect_image(MODEL, IMAGE)
    #detect_image_with_results(MODEL, IMAGE)