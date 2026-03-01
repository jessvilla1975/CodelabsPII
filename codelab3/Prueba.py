import cv2
import dlib
import time
import numpy as np

# Asegurar versión de NumPy correcta
print(f"Usando NumPy versión: {np.__version__}")

# Inicializar detector
detector = dlib.get_frontal_face_detector()

# Abrir video
cap = cv2.VideoCapture('video2.mp4')

if not cap.isOpened():
    print("ERROR: No se puede abrir el video 'video2.mp4'")
    exit()

print(" Video abierto correctamente. Presiona 'q' para salir...")

prev = time.time()
frames = 0

ANCHO_DESEADO = 640  
ALTO_DESEADO = 640   

while True:
    ok, frame = cap.read()
    if not ok:
        print("Video terminado")
        break
    
    # Guardar el frame original para procesamiento
    frame_original = frame.copy()
    
    # Convertir a RGB para detección
    rgb_frame = cv2.cvtColor(frame_original, cv2.COLOR_BGR2RGB)
    
    # Detectar caras
    rects = detector(rgb_frame, 0)
    
    # Dibujar rectángulos en el frame original
    for r in rects:
        x, y, w, h = r.left(), r.top(), r.width(), r.height()
        cv2.rectangle(frame_original, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Calcular y mostrar FPS
    frames += 1
    if frames % 10 == 0:
        now = time.time()
        fps = 10 / (now - prev)
        prev = now
        cv2.putText(frame_original, f"FPS: {fps:.1f}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    frame_pequeno = cv2.resize(frame_original, (ANCHO_DESEADO, ALTO_DESEADO))
    
    # Mostrar la ventana con el frame redimensionado
    cv2.imshow('Detección Facial', frame_pequeno)
    
    # Salir con 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()
print(" Programa terminado")