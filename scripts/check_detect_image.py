from ultralytics import YOLO

# 1. Cargar tu modelo entrenado
# Reemplaza 'ruta/a/tu/mejor_modelo.pt' por la ubicación de tus pesos (suele estar en 'runs/train/exp/weights/best.pt')
model = YOLO("models/best.pt")

# 2. Pasar la imagen que deseas analizar
# Reemplaza 'ruta/a/tu/imagen.jpg' por la imagen que quieres probar
imagen_prueba = "data/demo/cocacola1.jpg"

# 3. Realizar la predicción
# save=True guardará automáticamente la imagen con las cajas delimitadoras (bounding boxes)
results = model.predict(source=imagen_prueba, save=True, conf=0.5)

print("¡Detección completada! Revisa la carpeta generada para ver la imagen procesada.")
