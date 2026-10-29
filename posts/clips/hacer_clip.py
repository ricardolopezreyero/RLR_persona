"""Clip vertical 1080×1920 para X a partir de un video de YouTube (grabación de pantalla con cámara en círculo).
Capas: fondo negro, lámina de la presentación arriba, cámara en círculo con aro amarillo, subtítulos grandes por trozos
(PNG por trozo, overlay con enable=between), gancho fijo arriba y @ abajo. Sin drawtext ni libass: todo texto va en PNG."""
import os, sys, json, re, subprocess
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(AQUI, 'src')
sys.path.insert(0, os.path.expanduser('~/Code/RLR_persona/posts'))
from hacer_visuales import f  # Avenir Next por peso

NEGRO, BLANCO, ACENTO, GRIS = (13, 13, 13), (245, 245, 240), (255, 199, 44), (150, 150, 145)
W, H = 1080, 1920
INI, FIN = 98.9, 134.7
# geometría de la fuente (1920×1080): lámina y cámara
LAM = (126, 88, 1444, 936)      # x, y, w, h  (sin la esquina de la cámara)
CAM = (1582, 742, 296, 296)
LAM_W, LAM_H = 920, 596
LAM_XY = (80, 470)
CAM_D = 400
CAM_XY = (340, 1100)
ENFASIS = {'vanidad', 'aulas.', '1.2', 'millones', 'tres', 'equivocada.', 'siguiente', 'paso.', 'mesa.', 'responsable', 'fecha?', 'inscritos.', 'alumnos'}

# 1 · capa fija: fondo con ventanas transparentes para lámina y cámara, gancho y @
fijo = Image.new('RGBA', (W, H), NEGRO + (255,))
d = ImageDraw.Draw(fijo)
# ventana lámina (esquinas redondeadas) y ventana circular de la cámara
mask = Image.new('L', (W, H), 255)
md = ImageDraw.Draw(mask)
md.rounded_rectangle((LAM_XY[0], LAM_XY[1], LAM_XY[0] + LAM_W, LAM_XY[1] + LAM_H), radius=28, fill=0)
md.ellipse((CAM_XY[0], CAM_XY[1], CAM_XY[0] + CAM_D, CAM_XY[1] + CAM_D), fill=0)
fijo.putalpha(mask)
d = ImageDraw.Draw(fijo)
d.ellipse((CAM_XY[0] - 10, CAM_XY[1] - 10, CAM_XY[0] + CAM_D + 10, CAM_XY[1] + CAM_D + 10), outline=ACENTO, width=10)
d.rectangle((60, 92, 140, 100), fill=ACENTO)
d.text((60, 118), 'RICARDO LÓPEZ REYERO · ADMISIONES', font=f('demi', 30), fill=ACENTO)
d.text((60, 166), '1.2 millones', font=f('heavy', 92), fill=BLANCO)
d.text((60, 266), 'de impresiones.', font=f('heavy', 92), fill=BLANCO)
d.text((60, 366), '3 inscritos.', font=f('heavy', 92), fill=ACENTO)
d.text((W // 2, 1860), '@ricardolopezrey', font=f('demi', 34), fill=GRIS, anchor='mm')
fijo.save(os.path.join(AQUI, 'capa_fija.png'))

# 2 · trozos de subtítulo con tiempos de palabra
pal = [(t, w.split()[-1]) for t, w in json.load(open(os.path.join(SRC, 'palabras_seg.json'))) if INI <= t <= FIN]
trozos, cur = [], []
for t, w in pal:
    cur.append((t, w))
    if len(cur) >= 5 or re.search(r'[.?!]$', w) or (w.endswith(',') and len(cur) >= 3):
        trozos.append(cur); cur = []
if cur:
    trozos.append(cur)
os.makedirs(os.path.join(AQUI, 'sub'), exist_ok=True)
entradas = []
for k, tr in enumerate(trozos):
    a = tr[0][0] - INI
    b = (trozos[k + 1][0][0] - INI) if k + 1 < len(trozos) else (FIN - INI)
    im = Image.new('RGBA', (W, 360), (0, 0, 0, 0))
    dd = ImageDraw.Draw(im)
    fu = f('heavy', 74)
    palabras = [w for _, w in tr]
    # dos renglones si no cabe
    lineas, actual = [], ''
    for w in palabras:
        prueba = (actual + ' ' + w).strip()
        if dd.textlength(prueba, font=fu) > W - 120 and actual:
            lineas.append(actual); actual = w
        else:
            actual = prueba
    lineas.append(actual)
    y = 180 - len(lineas) * 45
    for ln in lineas:
        x = (W - dd.textlength(ln, font=fu)) / 2
        for w in ln.split(' '):
            col = ACENTO if w.strip('¿¡').lower() in ENFASIS else BLANCO
            dd.text((x + 3, y + 3), w, font=fu, fill=(0, 0, 0, 180))
            dd.text((x, y), w, font=fu, fill=col)
            x += dd.textlength(w + ' ', font=fu)
        y += 90
    ruta = os.path.join(AQUI, 'sub', f'{k:02d}.png')
    im.save(ruta)
    entradas.append((ruta, round(a, 2), round(b, 2)))

# 3 · ffmpeg
inputs = ['-ss', str(INI), '-to', str(FIN), '-i', os.path.join(SRC, 'video.mp4'), '-i', os.path.join(AQUI, 'capa_fija.png')]
for ruta, _, _ in entradas:
    inputs += ['-i', ruta]
fc = [f'color=c=0x0D0D0D:s={W}x{H}:r=30[bg]',
      f'[0:v]crop={LAM[2]}:{LAM[3]}:{LAM[0]}:{LAM[1]},scale={LAM_W}:{LAM_H}[lam]',
      f'[0:v]crop={CAM[2]}:{CAM[3]}:{CAM[0]}:{CAM[1]},scale={CAM_D}:{CAM_D}[cam]',
      f'[bg][lam]overlay={LAM_XY[0]}:{LAM_XY[1]}:shortest=1[a]',
      f'[a][cam]overlay={CAM_XY[0]}:{CAM_XY[1]}[b]',
      '[b][1:v]overlay=0:0[c]']
prev = 'c'
for k, (_, a, b) in enumerate(entradas):
    fc.append(f"[{prev}][{k + 2}:v]overlay=0:1500:enable='between(t,{a},{b})'[s{k}]")
    prev = f's{k}'
fc.append(f'[{prev}]format=yuv420p[v]')
salida = sys.argv[1]
cmd = ['ffmpeg', '-y', '-v', 'error'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '0:a',
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-r', '30', '-c:a', 'aac', '-b:a', '160k', '-af', f'afade=t=out:st={FIN - INI - 0.6}:d=0.6', '-movflags', '+faststart', salida]
subprocess.run(cmd, check=True)
print(len(entradas), 'trozos ·', salida)
