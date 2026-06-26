import cv2
from ultralytics import YOLO

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# from src.detect_image import detect_image

# 1. Carga tu modelo entrenado
ruta_modelo = Path("models/best.pt")
model = YOLO(str(ruta_modelo))

# 2. Inicia la cámara web
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error al abrir la cámara web")
    exit()

# 3. Configuración para guardar el video
# Obtenemos las propiedades reales de tu cámara web
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))

# Si la cámara devuelve 0 FPS por error, forzamos un estándar (20-30)
if fps == 0:
    fps = 20

# Definimos el códec y el archivo de salida
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('data/outputs/resultado_yolo.mp4', fourcc, fps, (frame_width, frame_height))

print("Grabando en MP4... Presiona la tecla 'q' para detener y guardar.")

# 4. Bucle de procesamiento
while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Ejecutamos YOLO (aquí puedes ajustar el umbral 'conf')
    #results = model(frame, conf=0.5)[0]  # Añadimos [0] para asegurar el acceso al primer resultado
    results = model(frame, conf=0.5)

    # Dibujamos las cajas de detección
    # El parámetro 'render()' u 'output' en YOLOv8 se obtiene con .plot()
    frame_con_detecciones = results[0].plot()

    # Guardamos el fotograma actual en el archivo de video
    out.write(frame_con_detecciones)

    # Mostramos el video en pantalla
    cv2.imshow("Deteccion y Grabacion YOLO (MP4)", frame_con_detecciones)

    # Detener con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 5. Limpieza de recursos (¡Muy importante para que el video se guarde bien!)
cap.release()
out.release()  # Cierra y consolida el archivo de video
cv2.destroyAllWindows()
print("Video guardado exitosamente como 'data/outputs/resultado_yolo.mp4'")