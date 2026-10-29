"""Short vertical 1080×1920 (diseño SuperLeads) a partir de v/<id>/video.mp4 + encuadre.json + un tramo (dict).
Generaliza hacer_short.py: el recorte de contenido y cámara sale de encuadre.json (en píxeles de la fuente real),
la cámara se afila un poco si viene de 720p, y hay dos composiciones: pantalla_camara (lámina + cámara) y
solo_camara (cámara a cuadro completo). Uso: main(vid, tramo, salida)."""
import os, sys, json, subprocess
from PIL import Image, ImageDraw
from hacer_short import fuente, envolver, NAVY_DEEP, VERDE, BLANCO, SUB, LABEL, AQUI

W, H = 1080, 1920
CONT_XY, CONT_W = (40, 470), 1000
CAM_W = 800


def main(vid, tr, salida, portada=None):
    carpeta = os.path.join(AQUI, 'v', vid)
    enc = json.load(open(os.path.join(carpeta, 'encuadre.json')))
    INI, FIN = tr['ini'], tr['fin']
    dur = FIN - INI
    tr = dict(tr); tr['gancho'] = [g[:1].upper() + g[1:] for g in tr['gancho']]
    solo = enc['tipo'] == 'solo_camara' or not enc.get('cont')
    enc = dict(enc)
    for campo in ('cam', 'cont', 'forma'):  # un tramo puede traer su propio encuadre (la burbuja se mueve por lámina)
        if tr.get(campo): enc[campo] = tr[campo]
    kx, ky, kw, kh = enc['cam'] if enc.get('cam') else (0, 0, enc['w'], enc['h'])
    if solo:
        # cámara vertical: recorte 9:16 centrado en la cara
        ch = enc['h']; cw = round(ch * 9 / 16); cx = kx + kw / 2
        kx, ky, kw, kh = int(min(max(cx - cw / 2, 0), enc['w'] - cw)), 0, cw, ch
        cam_w, cam_h = W, H
        cam_xy = (0, 0)
        cont_h = 0
    else:
        cx, cy, cw, ch = enc['cont']
        cont_h = round(CONT_W * ch / cw)
        circ = enc.get('forma') == 'circulo'
        cam_w = 620 if circ else CAM_W; cam_h = round(cam_w * kh / kw)
        cont_h = min(cont_h, 600, 1030 - cam_h)  # que quepan contenido + cámara + 230 px de subtítulos
        ch = round(cont_h * cw / CONT_W)  # recorte de contenido proporcional (parte alta)
        cam_xy = ((W - cam_w) // 2, CONT_XY[1] + cont_h + 40)
    afilar = ',unsharp=5:5:0.6:5:5:0.0' if enc['w'] < 1500 else ''

    # capa fija
    fijo = Image.new('RGBA', (W, H), NAVY_DEEP + (255,))
    mask = Image.new('L', (W, H), 255)
    md = ImageDraw.Draw(mask)
    if not solo:
        md.rounded_rectangle((CONT_XY[0], CONT_XY[1], CONT_XY[0] + CONT_W, CONT_XY[1] + cont_h), radius=24, fill=0)
        if circ: md.ellipse((cam_xy[0], cam_xy[1], cam_xy[0] + cam_w, cam_xy[1] + cam_h), fill=0)
        else: md.rounded_rectangle((cam_xy[0], cam_xy[1], cam_xy[0] + cam_w, cam_xy[1] + cam_h), radius=24, fill=0)
    else:
        md.rectangle((0, 0, W, H), fill=0)
    fijo.putalpha(mask)
    d = ImageDraw.Draw(fijo)
    if not solo:
        d.rounded_rectangle((CONT_XY[0] - 1, CONT_XY[1] - 1, CONT_XY[0] + CONT_W + 1, CONT_XY[1] + cont_h + 1), radius=25, outline=(40, 70, 140, 255), width=2)
        if circ: d.ellipse((cam_xy[0] - 4, cam_xy[1] - 4, cam_xy[0] + cam_w + 4, cam_xy[1] + cam_h + 4), outline=(86, 239, 159, 255), width=5)
        else: d.rounded_rectangle((cam_xy[0] - 1, cam_xy[1] - 1, cam_xy[0] + cam_w + 1, cam_xy[1] + cam_h + 1), radius=25, outline=(40, 70, 140, 255), width=2)
    else:
        # banda superior e inferior semitransparentes para que el gancho y los subtítulos respiren
        d.rectangle((0, 0, W, 520), fill=NAVY_DEEP + (200,))
        d.rectangle((0, H - 560, W, H), fill=NAVY_DEEP + (210,))
    y = 110
    n = len(tr['gancho'])
    tam = 96 if n <= 3 else 84
    for k, linea in enumerate(tr['gancho']):
        fu = fuente('ExtraBold', tam)
        while d.textlength(linea, font=fu) > W - 120 and tam > 56:
            tam -= 4; fu = fuente('ExtraBold', tam)
        d.text((60, y), linea, font=fu, fill=VERDE if k == n - 1 else BLANCO)
        y += int(tam * 1.12)
    d.rectangle((60, y + 18, 140, y + 22), fill=VERDE)
    logo = Image.open(os.path.join(AQUI, 'marca', 'logo_blanco.png')).convert('RGBA')
    lw = 240; logo = logo.resize((lw, round(logo.height * lw / logo.width)), Image.LANCZOS)
    fijo.alpha_composite(logo, (60, H - 90 - logo.height // 2))
    d = ImageDraw.Draw(fijo)
    d.text((W - 60, H - 90), 'Ing. Ricardo López Reyero', font=fuente('Medium', 30), fill=SUB, anchor='rm')
    tag = f'{vid}_{int(INI)}'
    ruta_fijo = os.path.join(carpeta, f'fijo_{tag}.png'); fijo.save(ruta_fijo)

    # subtítulos
    y_sub = (cam_xy[1] + cam_h + 30) if not solo else H - 540
    alto_sub = H - 150 - y_sub
    enf = {e.lower().strip('.,;:¿?¡!') for e in tr['enfasis']}
    sdir = os.path.join(carpeta, f'sub_{tag}'); os.makedirs(sdir, exist_ok=True)
    entradas = []
    for k, t in enumerate(tr['trozos']):
        im = Image.new('RGBA', (W, alto_sub), (0, 0, 0, 0)); dd = ImageDraw.Draw(im)
        tam = 72; fu = fuente('ExtraBold', tam); lineas = envolver(dd, t['texto'], fu, W - 140)
        while len(lineas) > 2 and tam > 54:
            tam -= 4; fu = fuente('ExtraBold', tam); lineas = envolver(dd, t['texto'], fu, W - 140)
        yy = (alto_sub - len(lineas) * int(tam * 1.25)) // 2
        for ln in lineas:
            x = (W - dd.textlength(ln, font=fu)) / 2
            for w in ln.split(' '):
                col = VERDE if w.lower().strip('.,;:¿?¡!') in enf else BLANCO
                dd.text((x + 2, yy + 3), w, font=fu, fill=(0, 10, 40, 160)); dd.text((x, yy), w, font=fu, fill=col)
                x += dd.textlength(w + ' ', font=fu)
            yy += int(tam * 1.25)
        ruta = os.path.join(sdir, f'{k:02d}.png'); im.save(ruta)
        entradas.append((ruta, round(t['ini'] - INI, 2), round(t['fin'] - INI, 2)))

    inputs = ['-ss', str(INI), '-to', str(FIN), '-i', os.path.join(carpeta, 'video.mp4'), '-i', ruta_fijo]
    for ruta, _, _ in entradas: inputs += ['-i', ruta]
    fc = [f'color=c=0x001240:s={W}x{H}:r=30[bg]']
    if not solo:
        fc += [f'[0:v]split=2[v1][v2]',
               f'[v1]crop={cw}:{ch}:{cx}:{cy},scale={CONT_W}:{cont_h}:flags=lanczos[cont]',
               f'[v2]crop={kw}:{kh}:{kx}:{ky},scale={cam_w}:{cam_h}:flags=lanczos{afilar}[cam]',
               f'[bg][cont]overlay={CONT_XY[0]}:{CONT_XY[1]}:shortest=1[a]',
               f'[a][cam]overlay={cam_xy[0]}:{cam_xy[1]}[b]']
    else:
        fc += [f'[0:v]crop={kw}:{kh}:{kx}:{ky},scale={W}:{H}:flags=lanczos{afilar}[cam]',
               f'[bg][cam]overlay=0:0:shortest=1[b]']
    fc.append('[b][1:v]overlay=0:0[c]')
    prev = 'c'
    for k, (_, a, b) in enumerate(entradas):
        fc.append(f"[{prev}][{k + 2}:v]overlay=0:{y_sub}:enable='between(t,{a},{b})'[s{k}]"); prev = f's{k}'
    fc.append(f'[{prev}]fade=t=in:st=0:d=0.3,fade=t=out:st={dur - 0.5}:d=0.5,format=yuv420p[v]')
    cmd = ['ffmpeg', '-y', '-v', 'error'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '0:a',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-r', '30', '-c:a', 'aac', '-b:a', '192k',
           '-af', f'afade=t=in:st=0:d=0.2,afade=t=out:st={dur - 0.6}:d=0.6', '-movflags', '+faststart', salida]
    subprocess.run(cmd, check=True)

    # portada vertical (gancho + cara)
    if portada:
        raw = os.path.join(carpeta, f'cara_{tag}.png')
        subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(tr.get('cara', INI + 3)), '-i', os.path.join(carpeta, 'video.mp4'), '-frames:v', '1', '-vf', f'crop={kw}:{kh}:{kx}:{ky}', '-y', raw], check=True)
        cara = Image.open(raw).convert('RGB')
        if not solo:
            cw0 = round(cara.width * 0.68); cx0 = (cara.width - cw0) // 2 + 20
            cara = cara.crop((cx0, 0, cx0 + cw0, cara.height))
        cara = cara.resize((W, round(cara.height * W / cara.width)), Image.LANCZOS)
        if solo: cara = cara.crop((0, 0, W, H))
        P = Image.new('RGB', (W, H), NAVY_DEEP)
        P.paste(cara, (0, H - cara.height - 140) if not solo else (0, 0))
        grad = Image.new('L', (1, 400))
        for yy in range(400): grad.putpixel((0, yy), int(255 * (1 - yy / 400) ** 1.4))
        top = (H - cara.height - 140) if not solo else 0
        P.paste(Image.new('RGB', (W, 400), NAVY_DEEP), (0, top), grad.resize((W, 400)))
        dp = ImageDraw.Draw(P)
        dp.rectangle((0, H - 140, W, H), fill=NAVY_DEEP)
        lg = Image.open(os.path.join(AQUI, 'marca', 'logo_blanco.png')).convert('RGBA'); lg = lg.resize((260, round(lg.height * 260 / lg.width)), Image.LANCZOS)
        P.paste(lg, (60, H - 70 - lg.height // 2), lg)
        dp.text((W - 60, H - 70), 'Ing. Ricardo López Reyero', font=fuente('Medium', 32), fill=SUB, anchor='rm')
        y = 190
        for i, linea in enumerate(tr['gancho']):
            tam = 118; fu = fuente('ExtraBold', tam)
            while dp.textlength(linea, font=fu) > W - 120 and tam > 70: tam -= 4; fu = fuente('ExtraBold', tam)
            dp.text((60, y), linea, font=fu, fill=VERDE if i == n - 1 else BLANCO); y += int(tam * 1.12)
        dp.rectangle((60, y + 24, 160, y + 30), fill=VERDE)
        P.save(portada)
    return dur


if __name__ == '__main__':
    vid, k, salida = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    tr = json.load(open(os.path.join(AQUI, 'v', vid, 'tramos.json')))['tramos'][k]
    print(vid, k, f'{main(vid, tr, salida, salida.replace(".mp4", "_portada.png")):.1f}s')
