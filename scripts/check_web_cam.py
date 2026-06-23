# import libraries
from ultralytics import YOLO
import cv2

# 1. Carga tu modelo entrenado (reemplaza con la ruta a tu archivo .pt)
ruta_modelo = "../models/best.pt"
model = YOLO(ruta_modelo)

# 2. Inicia la cámara web (0 suele ser la cámara integrada, 1 para una externa)
cap = cv2.VideoCapture(0)

# Verifica si la cámara abrió correctamente
if not cap.isOpened():
    print("Error al abrir la cámara web")
    exit()

print("Presiona la tecla 'q' para salir de la ventana de video.")

# 3. Bucle para procesar el video en tiempo real
while True:
    # Lee un fotograma (frame) de la cámara
    ret, frame = cap.read()
    if not ret:
        break

    # Realiza la predicción en el fotograma
    # conf=0.5 establece un umbral de confianza del 50%
    results = model(frame, conf=0.5)

    # Dibuja los resultados sobre el fotograma
    frame_con_detecciones = results[0].plot()

    # Muestra el fotograma resultante en una ventana
    cv2.imshow("Deteccion YOLO en tiempo real", frame_con_detecciones)

    # Cierra el programa si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera la cámara y cierra todas las ventanas
cap.release()
cv2.destroyAllWindows()