"""Color de las 4 fotos del stand (9-nov-2026). Mismo grado para las cuatro: balance de blancos suave,
curva en S con sombras levantadas, vibrancia, un toque cálido y nitidez. La 4 se recorta para quitar la marca «HONOR 200 Pro».
Orden del carrusel (pedido de Ricardo): la de él con clientes (sin selfie), la de más gente, y luego de más a menos."""
import os, numpy as np
from PIL import Image, ImageFilter, ImageOps
SRC = '/private/tmp/claude-501/-Users-ricardolopezreyero/dfb20a09-f148-4061-aed0-5a4a56730342/images'
AQUI = os.path.dirname(os.path.abspath(__file__))
ORDEN = [  # (origen, nombre)
    ('34.jpg', '01-ricardo-con-clientes-de-superleads.jpg'),
    ('33.jpg', '02-clientes-y-equipo-superleads-en-el-stand.jpg'),
    ('31.jpg', '03-ricardo-con-clientes-en-el-pasillo.jpg'),
    ('32.jpg', '04-equipo-superleads-y-cliente-en-el-stand.jpg'),
]

def grado(im):
    a = np.asarray(im.convert('RGB')).astype(np.float32) / 255
    # balance de blancos: mundo gris al 45 %
    m = a.reshape(-1, 3).mean(0); g = m.mean()
    a = a * (1 + 0.45 * (g / m - 1))
    # curva: levanta sombras y da contraste en medios
    a = np.clip(a, 0, 1)
    a = a + 0.06 * (1 - a) * (1 - a) * a * 4          # sombras arriba
    a = a + 0.10 * np.sin(np.pi * (a - 0.5)) * 0.5    # S suave
    a = np.clip(a, 0, 1)
    # vibrancia: sube más lo poco saturado
    mx = a.max(2, keepdims=True); mn = a.min(2, keepdims=True); s = (mx - mn) / (mx + 1e-6)
    luma = (a * [0.299, 0.587, 0.114]).sum(2, keepdims=True)
    k = 1 + 0.38 * (1 - s)
    a = luma + (a - luma) * k
    # cálido leve
    a = a * [1.025, 1.0, 0.97]
    a = np.clip(a, 0, 1)
    out = Image.fromarray((a * 255 + 0.5).astype(np.uint8))
    return out.filter(ImageFilter.UnsharpMask(radius=1.6, percent=55, threshold=2))

for src, nombre in ORDEN:
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, src)))
    if src == '34.jpg':  # quita «HONOR 200 Pro» (abajo a la izquierda) manteniendo 4:3
        w, h = im.size; nh = h - 96; nw = int(nh * 4 / 3); x0 = (w - nw) // 2
        im = im.crop((x0, 0, x0 + nw, nh))
    grado(im).save(os.path.join(AQUI, nombre), quality=92, optimize=True)  # sin EXIF
    print(nombre, im.size)
