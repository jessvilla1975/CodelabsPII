import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"  
import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from mtcnn.mtcnn import MTCNN
from time import time

# Ruta relativa a la carpeta del script (codelab2)
img_path = Path(__file__).parent / "foto3.jpg"
img = cv2.imread(str(img_path))
if img is None:
    raise FileNotFoundError(f"No se encontró la imagen. Coloca 'foto2.png' en: {img_path.parent}")
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

detector = MTCNN()   # puedes ajustar min_face_size
t0 = time()
res = detector.detect_faces(img_rgb)
t1 = time()

tiempo_deteccion_ms = (t1 - t0) * 1000
lineas_reporte = [
    f"Imagen: {img_path.name}",
    f"Detected: {len(res)} rostro(s) • tiempo: {tiempo_deteccion_ms:.1f} ms",
    "",
]
print(lineas_reporte[1])
for r in res:
    linea = f"  conf={r['confidence']:.6f} box={r['box']} keypoints={list(r['keypoints'].keys())}"
    lineas_reporte.append(linea)
    print(r['confidence'], r['box'], r['keypoints'].keys())

# Filtrado por confianza mínima
detector = MTCNN()  # su NMS interno filtra solapes
# Prueba filtrado por confianza mínima
thr = 0.90
filtrados = [r for r in res if r['confidence'] >= thr]
lineas_reporte.extend(["", f"Con thr={thr} quedan {len(filtrados)} rostros"])
print(f"Con thr={thr} quedan {len(filtrados)} rostros")


def iou(a, b):
    # a,b en formato [x,y,w,h]
    ax1, ay1, aw, ah = a; ax2, ay2 = ax1+aw, ay1+ah
    bx1, by1, bw, bh = b; bx2, by2 = bx1+bw, by1+bh
    ix1, iy1 = max(ax1,bx1), max(ay1,by1)
    ix2, iy2 = min(ax2,bx2), min(ay2,by2)
    inter = max(0, ix2-ix1)*max(0, iy2-iy1)
    union = aw*ah + bw*bh - inter
    return inter/union if union>0 else 0.0

gt_box = [59, 69, 54, 58]

# Si tienes una caja "ground truth" gt_box, compara:
iou_val = iou(res[0]['box'], gt_box) if res else 0.0
lineas_reporte.extend(["", f"IoU(primer_rostro, gt_box): {iou_val}"])

# Guardar reporte en .txt (misma carpeta que el script)
reporte_path = Path(__file__).parent / "reporte_rostros.txt"
with open(reporte_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lineas_reporte))
print(f"\nReporte guardado en: {reporte_path}")

print(iou_val)

# Visualización
vis = img_rgb.copy()
for r in res:
    x, y, w, h = r['box']
    cv2.rectangle(vis, (x,y), (x+w, y+h), (0,255,0), 2)
    for name, (px,py) in r['keypoints'].items():
        cv2.circle(vis, (px,py), 2, (255,0,0), -1)
plt.imshow(vis)
plt.axis('off')
plt.show()

