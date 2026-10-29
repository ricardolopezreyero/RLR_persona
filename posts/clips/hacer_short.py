"""Short vertical 1080×1920 para YouTube con el sistema de diseño de SuperLeads (navy profundo, verde, Plus Jakarta Sans).
Entrada: v/<id>/video.mp4 (1668×1080, pantalla compartida + cámara abajo a la derecha) y v/<id>/seleccion.json
(tramo, gancho, trozos de subtítulo corregidos, énfasis). Recortes de contenido y cámara por video en CONFIG.
Todo el texto va en PNG (este ffmpeg no trae drawtext ni libass) y se sobrepone con enable=between."""
import os, sys, json, subprocess
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.expanduser('~/Library/Fonts/PlusJakartaSans-{}.ttf')
NAVY_DEEP, NAVY_MID, VERDE, BLANCO, SUB, LABEL = (0, 18, 64), (0, 26, 94), (86, 239, 159), (255, 255, 255), (122, 159, 212), (74, 106, 170)
W, H = 1080, 1920

# geometría en la fuente 1668×1080: (x, y, w, h) del contenido y de la cámara
CONFIG = {
    'ZP5BSoRFaio': {'cont': (50, 115, 1568, 585), 'cam': (1080, 718, 520, 290)},
    '0tRgTomkaAw': {'cont': (196, 196, 1308, 494), 'cam': (1120, 690, 480, 290)},
    'aZggkBKgqrg': {'cont': (300, 240, 1100, 380), 'cam': (1120, 690, 480, 290)},
    'mDfb_nteAe8': {'cont': (330, 240, 1000, 340), 'cam': (1120, 690, 480, 290)},
    'oqLweG2S0Bk': {'cont': (370, 200, 1160, 480), 'cam': (1120, 690, 480, 290)},
}
CONT_XY, CONT_W = (40, 470), 1000
CAM_W, CAM_Y = 800, None  # la cámara va después del contenido; su alto sale de su recorte


def fuente(peso, tam):
    return ImageFont.truetype(FUENTES.format(peso), tam)


def envolver(d, texto, fu, ancho):
    lineas, actual = [], ''
    for w in texto.split(' '):
        prueba = (actual + ' ' + w).strip()
        if d.textlength(prueba, font=fu) > ancho and actual:
            lineas.append(actual); actual = w
        else:
            actual = prueba
    return lineas + [actual]


def main(vid, salida):
    carpeta = os.path.join(AQUI, 'v', vid)
    sel = json.load(open(os.path.join(carpeta, 'seleccion.json')))
    cfg = CONFIG[vid]
    cx, cy, cw, ch = cfg['cont']
    cont_h = round(CONT_W * ch / cw)
    kx, ky, kw, kh = cfg['cam']
    cam_h = round(CAM_W * kh / kw)
    cam_xy = ((W - CAM_W) // 2, CONT_XY[1] + cont_h + 40)
    y_sub = cam_xy[1] + cam_h + 30            # inicio de la zona de subtítulos
    INI, FIN = sel['ini'], sel['fin']

    # capa fija: fondo navy con ventanas (bordes redondeados), gancho, línea verde, logo y pie
    fijo = Image.new('RGBA', (W, H), NAVY_DEEP + (255,))
    mask = Image.new('L', (W, H), 255)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((CONT_XY[0], CONT_XY[1], CONT_XY[0] + CONT_W, CONT_XY[1] + cont_h), radius=24, fill=0)
    md.rounded_rectangle((cam_xy[0], cam_xy[1], cam_xy[0] + CAM_W, cam_xy[1] + cam_h), radius=24, fill=0)
    fijo.putalpha(mask)
    d = ImageDraw.Draw(fijo)
    # borde de medio tono alrededor de las ventanas
    d.rounded_rectangle((CONT_XY[0] - 1, CONT_XY[1] - 1, CONT_XY[0] + CONT_W + 1, CONT_XY[1] + cont_h + 1), radius=25, outline=(40, 70, 140, 255), width=2)
    d.rounded_rectangle((cam_xy[0] - 1, cam_xy[1] - 1, cam_xy[0] + CAM_W + 1, cam_xy[1] + cam_h + 1), radius=25, outline=(40, 70, 140, 255), width=2)
    # gancho
    y = 110
    n = len(sel['gancho'])
    tam = 96 if n <= 3 else 84
    for k, linea in enumerate(sel['gancho']):
        col = VERDE if k == n - 1 else BLANCO
        fu = fuente('ExtraBold', tam)
        while d.textlength(linea, font=fu) > W - 120 and tam > 56:
            tam -= 4; fu = fuente('ExtraBold', tam)
        d.text((60, y), linea, font=fu, fill=col)
        y += int(tam * 1.12)
    d.rectangle((60, y + 18, 140, y + 22), fill=VERDE)
    # logo y pie
    logo = Image.open(os.path.join(AQUI, 'marca', 'logo_blanco.png')).convert('RGBA')
    lw = 240; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    fijo.alpha_composite(logo, (60, H - 90 - logo.height // 2))
    d = ImageDraw.Draw(fijo)
    d.text((W - 60, H - 90), 'Ing. Ricardo López Reyero', font=fuente('Medium', 30), fill=SUB, anchor='rm')
    ruta_fijo = os.path.join(carpeta, 'capa_fija.png')
    fijo.save(ruta_fijo)

    # subtítulos por trozo (PNG transparente de 1080 × alto de zona)
    alto_sub = H - 150 - y_sub
    enf = {e.lower().strip('.,;:¿?¡!') for e in sel['enfasis']}
    os.makedirs(os.path.join(carpeta, 'sub'), exist_ok=True)
    entradas = []
    for k, tr in enumerate(sel['trozos']):
        im = Image.new('RGBA', (W, alto_sub), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        tam = 72
        fu = fuente('ExtraBold', tam)
        lineas = envolver(dd, tr['texto'], fu, W - 140)
        while len(lineas) > 2 and tam > 54:
            tam -= 4; fu = fuente('ExtraBold', tam); lineas = envolver(dd, tr['texto'], fu, W - 140)
        yy = (alto_sub - len(lineas) * int(tam * 1.25)) // 2
        for ln in lineas:
            x = (W - dd.textlength(ln, font=fu)) / 2
            for w in ln.split(' '):
                col = VERDE if w.lower().strip('.,;:¿?¡!') in enf else BLANCO
                dd.text((x + 2, yy + 3), w, font=fu, fill=(0, 10, 40, 160))
                dd.text((x, yy), w, font=fu, fill=col)
                x += dd.textlength(w + ' ', font=fu)
            yy += int(tam * 1.25)
        ruta = os.path.join(carpeta, 'sub', f'{k:02d}.png')
        im.save(ruta)
        entradas.append((ruta, round(tr['ini'] - INI, 2), round(tr['fin'] - INI, 2)))

    inputs = ['-ss', str(INI), '-to', str(FIN), '-i', os.path.join(carpeta, 'video.mp4'), '-i', ruta_fijo]
    for ruta, _, _ in entradas:
        inputs += ['-i', ruta]
    fc = [f'color=c=0x001240:s={W}x{H}:r=30[bg]',
          f'[0:v]crop={cw}:{ch}:{cx}:{cy},scale={CONT_W}:{cont_h}:flags=lanczos[cont]',
          f'[0:v]crop={kw}:{kh}:{kx}:{ky},scale={CAM_W}:{cam_h}:flags=lanczos[cam]',
          f'[bg][cont]overlay={CONT_XY[0]}:{CONT_XY[1]}:shortest=1[a]',
          f'[a][cam]overlay={cam_xy[0]}:{cam_xy[1]}[b]',
          '[b][1:v]overlay=0:0[c]']
    prev = 'c'
    for k, (_, a, b) in enumerate(entradas):
        fc.append(f"[{prev}][{k + 2}:v]overlay=0:{y_sub}:enable='between(t,{a},{b})'[s{k}]")
        prev = f's{k}'
    fc.append(f'[{prev}]fade=t=in:st=0:d=0.3,fade=t=out:st={FIN - INI - 0.5}:d=0.5,format=yuv420p[v]')
    dur = FIN - INI
    cmd = ['ffmpeg', '-y', '-v', 'error'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '0:a',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-r', '30', '-c:a', 'aac', '-b:a', '192k',
           '-af', f'afade=t=in:st=0:d=0.2,afade=t=out:st={dur - 0.6}:d=0.6', '-movflags', '+faststart', salida]
    subprocess.run(cmd, check=True)
    print(vid, f'{dur:.1f}s', len(entradas), 'trozos ·', salida)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
