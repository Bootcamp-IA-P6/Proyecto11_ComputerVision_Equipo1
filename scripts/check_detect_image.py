from ultralytics import YOLO
import cv2


# Constantes con los parámetros de prueba
# El modelo
MODEL = "models/best.pt"

# Donde dejará la salida y como nombrará el fichero resultado
OUTPUT = "data/outputs/result.jpg"

# Imágenes de prueba que están en data/demo
#IMAGE = "data/demo/cocacola1.jpg"
#IMAGE = "data/demo/pepsi2.jpg"
#IMAGE = "data/demo/pepsi_cocacola2.jpg"
#IMAGE = "data/demo/pepsi_cocacola1.jpg"
IMAGE = "data/demo/pepsi_cocacola3.jpg"

# Función que le pasas el modelo y una imagen e imprime resultados
# Los resultados se pueden ver en la carpeta runs/detect/predict/cocacola1.jpg
def detect_image(model_trained, image_test):
    # 1. Cargar tu modelo entrenado
    model = YOLO(model_trained)

    # 2. Realizar la predicción
    # save=True guardará automáticamente la imagen con las cajas delimitadoras (bounding boxes)
    results = model.predict(source=image_test, save=True, conf=0.5)

    # 3. Imprime los resultados
    for box in results[0].boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0])
        cls = int(box.cls[0])

        print(
            f"{model.names[cls]} "
            f"({conf:.2f}) "
            f"[{x1:.0f}, {y1:.0f}, {x2:.0f}, {y2:.0f}]"
        )


# Función que le pasas el modelo y una imagen y muestra por pantalla la imagen con el resultado
def detect_image_with_results(model_trained, image_test):
    model = YOLO(model_trained)

    results = model.predict(source=image_test, save=True, conf=0.5)

    # Imagen con las detecciones dibujadas
    annotated_img = results[0].plot()

    cv2.imshow("Detección", annotated_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Función que le pasas el modelo, una imagen y la ruta para la imagen resultado
# Los resultados se pueden ver en la carpeta data/outputs/result.jpg
def detect_image_and_save(model_trained, image_test, image_output):
    model = YOLO(model_trained)

    results = model.predict(source=image_test, save=False, conf=0.5)

    # Imagen con las detecciones dibujadas
    annotated_img = results[0].plot()

    cv2.imwrite(image_output, annotated_img)


if __name__ == "__main__":
    #detect_image(MODEL, IMAGE)
    #detect_image_with_results(MODEL, IMAGE)
    detect_image_and_save(MODEL, IMAGE, OUTPUT)