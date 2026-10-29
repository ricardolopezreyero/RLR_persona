"""Detecta el encuadre de cada video: dónde está la cámara de Ricardo y qué zona de pantalla compartida mostrar.
Método: 10 cuadros repartidos en el video; la varianza temporal por píxel es alta donde hay cámara (él se mueve) y baja
en la lámina. Si la zona de alta varianza cubre casi todo el cuadro, el video es «solo cámara» (a cuadro completo).
Escribe v/<id>/encuadre.json = {"tipo": "pantalla_camara"|"solo_camara", "w", "h", "cam": [x,y,w,h], "cont": [x,y,w,h]}
y una imagen v/<id>/encuadre.jpg con los rectángulos para revisar."""
import os, sys, json, subprocess
import numpy as np
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))


def dur_wh(ruta):
    o = subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height:format=duration', '-of', 'json', ruta], capture_output=True, text=True).stdout
    j = json.loads(o)
    return float(j['format']['duration']), j['streams'][0]['width'], j['streams'][0]['height']


def cuadro(ruta, t):
    out = subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(t), '-i', ruta, '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'], capture_output=True).stdout
    from io import BytesIO
    return np.asarray(Image.open(BytesIO(out)).convert('L'), dtype=np.float32)


def bbox(mask):
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max() - xs.min() + 1), int(ys.max() - ys.min() + 1)


def main(vid):
    carpeta = os.path.join(AQUI, 'v', vid)
    ruta = os.path.join(carpeta, 'video.mp4')
    dur, W, H = dur_wh(ruta)
    ts = [dur * k for k in (0.15, 0.3, 0.45, 0.6, 0.75, 0.9)]
    pares = [(cuadro(ruta, t), cuadro(ruta, t + 0.7)) for t in ts]
    frames = np.stack([a for a, _ in pares])
    # movimiento a corto plazo: la cámara cambia en 0.7 s, la lámina casi nunca
    var = np.median(np.stack([np.abs(a - b) for a, b in pares]), axis=0)
    # suavizar en bloques de 8 px
    b = 8
    vb = var[:H // b * b, :W // b * b].reshape(H // b, b, W // b, b).mean(axis=(1, 3))
    vb[int(vb.shape[0] * 0.88):, :] = 0  # fuera la franja de subtítulos quemados
    alta = vb > max(3.0, float(np.percentile(vb, 85)))
    frac = alta.mean()
    tipo = 'solo_camara' if frac > 0.45 else 'pantalla_camara'
    cam = None
    if tipo == 'pantalla_camara':
        # región de alta varianza más grande: crecer desde la celda de máxima varianza
        from collections import deque
        best = None
        vis = np.zeros_like(alta, dtype=bool)
        for y in range(alta.shape[0]):
            for x in range(alta.shape[1]):
                if alta[y, x] and not vis[y, x]:
                    q = deque([(y, x)]); vis[y, x] = True; cells = []
                    while q:
                        cy, cx = q.popleft(); cells.append((cy, cx))
                        for ny, nx in ((cy + 1, cx), (cy - 1, cx), (cy, cx + 1), (cy, cx - 1)):
                            if 0 <= ny < alta.shape[0] and 0 <= nx < alta.shape[1] and alta[ny, nx] and not vis[ny, nx]:
                                vis[ny, nx] = True; q.append((ny, nx))
                    if best is None or len(cells) > len(best):
                        best = cells
        m = np.zeros_like(alta);
        for cy, cx in best: m[cy, cx] = True
        x, y, w, h = bbox(m)
        cx, cy = (x + w / 2) * b, (y + h / 2) * b
        cw, chh = round(W * 0.288), round(H * 0.268)   # 480×290 en 1668×1080
        x0 = int(min(max(cx - cw / 2, 0), W - cw)); y0 = int(min(max(cy - chh * 0.6, 0), H * 0.93 - chh))
        cam = [x0, y0, cw, chh]
        # contenido: la franja superior completa por encima de la cámara, sin bordes negros
        f = frames.mean(axis=0)
        cols = np.where(f.mean(axis=0) > 18)[0]; rows = np.where(f.mean(axis=1) > 18)[0]
        x0, x1 = int(cols.min()), int(cols.max()); y0 = int(rows.min())
        # saltar la barra del navegador/herramientas: filas superiores que NO cambian entre cuadros lejanos
        rv = frames.std(axis=0).mean(axis=1)
        lim = int(H * 0.28)
        for yy in range(y0, lim):
            if rv[yy] > 2.5:
                y0 = max(y0, yy - 4); break
        else:
            y0 = max(y0, int(H * 0.17))
        y1 = max(y0 + 200, cam[1] - 10)
        cont = [x0 + 20, y0 + 20, x1 - x0 - 40, y1 - y0 - 20]
    else:
        cont = None
    enc = {'tipo': tipo, 'w': W, 'h': H, 'dur': round(dur, 1), 'cam': cam, 'cont': cont, 'frac_var': round(float(frac), 3)}
    json.dump(enc, open(os.path.join(carpeta, 'encuadre.json'), 'w'))
    im = Image.fromarray(frames[2].astype(np.uint8)).convert('RGB')
    d = ImageDraw.Draw(im)
    if cam: d.rectangle((cam[0], cam[1], cam[0] + cam[2], cam[1] + cam[3]), outline=(86, 239, 159), width=6)
    if cont: d.rectangle((cont[0], cont[1], cont[0] + cont[2], cont[1] + cont[3]), outline=(255, 199, 44), width=6)
    im.resize((W // 2, H // 2)).save(os.path.join(carpeta, 'encuadre.jpg'))
    print(vid, enc)


if __name__ == '__main__':
    for v in sys.argv[1:]:
        try:
            main(v)
        except Exception as e:
            print(v, 'ERROR', e)
