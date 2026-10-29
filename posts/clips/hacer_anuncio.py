"""Anuncio horizontal 1920×1080 para YouTube (in-stream) a partir del mismo tramo y subtítulos de los Shorts.
Cámara grande a la izquierda, gancho fijo a la derecha desde el primer cuadro (antes de los 5 s de «omitir»),
subtítulos abajo y cierre de 2.5 s con el Rayos X. Diseño SuperLeads (navy, verde, Plus Jakarta Sans)."""
import os, sys, json, subprocess
from PIL import Image, ImageDraw
from hacer_short import CONFIG, fuente, envolver, NAVY_DEEP, VERDE, BLANCO, SUB, LABEL, AQUI

W, H = 1920, 1080
CAM_XY, CAM_W = (70, 150), 960
CIERRE = 2.5


def main(vid, salida):
    carpeta = os.path.join(AQUI, 'v', vid)
    sel = json.load(open(os.path.join(carpeta, 'seleccion.json')))
    kx, ky, kw, kh = CONFIG[vid]['cam']
    cam_h = round(CAM_W * kh / kw)
    INI, FIN = sel['ini'], sel['fin']
    dur = FIN - INI

    # capa fija: fondo con ventana de cámara, gancho a la derecha, logo y pie
    fijo = Image.new('RGBA', (W, H), NAVY_DEEP + (255,))
    mask = Image.new('L', (W, H), 255)
    ImageDraw.Draw(mask).rounded_rectangle((CAM_XY[0], CAM_XY[1], CAM_XY[0] + CAM_W, CAM_XY[1] + cam_h), radius=26, fill=0)
    fijo.putalpha(mask)
    d = ImageDraw.Draw(fijo)
    d.rounded_rectangle((CAM_XY[0] - 1, CAM_XY[1] - 1, CAM_XY[0] + CAM_W + 1, CAM_XY[1] + cam_h + 1), radius=27, outline=(40, 70, 140, 255), width=2)
    x0 = CAM_XY[0] + CAM_W + 70
    ancho = W - x0 - 70
    d.rectangle((x0, 150, x0 + 80, 156), fill=VERDE)
    y = 190
    n = len(sel['gancho'])
    for k, linea in enumerate(sel['gancho']):
        tam = 84
        fu = fuente('ExtraBold', tam)
        while d.textlength(linea, font=fu) > ancho and tam > 48:
            tam -= 4; fu = fuente('ExtraBold', tam)
        d.text((x0, y), linea, font=fu, fill=VERDE if k == n - 1 else BLANCO)
        y += int(tam * 1.15)
    d.text((x0, y + 24), 'Ing. Ricardo López Reyero', font=fuente('SemiBold', 30), fill=SUB)
    d.text((x0, y + 64), 'Founder Comercial · SuperLeads', font=fuente('Medium', 26), fill=LABEL)
    logo = Image.open(os.path.join(AQUI, 'marca', 'logo_blanco.png')).convert('RGBA')
    logo = logo.resize((220, round(logo.height * 220 / logo.width)), Image.LANCZOS)
    fijo.alpha_composite(logo, (W - 70 - logo.width, H - 60 - logo.height))
    ruta_fijo = os.path.join(carpeta, 'capa_fija_h.png')
    fijo.save(ruta_fijo)

    # subtítulos: banda inferior bajo la cámara, centrados en todo el ancho
    y_sub = CAM_XY[1] + cam_h + 24
    alto_sub = H - 70 - y_sub
    enf = {e.lower().strip('.,;:¿?¡!') for e in sel['enfasis']}
    os.makedirs(os.path.join(carpeta, 'sub_h'), exist_ok=True)
    entradas = []
    for k, tr in enumerate(sel['trozos']):
        im = Image.new('RGBA', (W, alto_sub), (0, 0, 0, 0))
        dd = ImageDraw.Draw(im)
        tam = 60
        fu = fuente('ExtraBold', tam)
        lineas = envolver(dd, tr['texto'], fu, W - 400)
        while len(lineas) > 2 and tam > 44:
            tam -= 4; fu = fuente('ExtraBold', tam); lineas = envolver(dd, tr['texto'], fu, W - 400)
        yy = (alto_sub - len(lineas) * int(tam * 1.25)) // 2
        for ln in lineas:
            x = (W - dd.textlength(ln, font=fu)) / 2
            for w in ln.split(' '):
                col = VERDE if w.lower().strip('.,;:¿?¡!') in enf else BLANCO
                dd.text((x + 2, yy + 3), w, font=fu, fill=(0, 10, 40, 160))
                dd.text((x, yy), w, font=fu, fill=col)
                x += dd.textlength(w + ' ', font=fu)
            yy += int(tam * 1.25)
        ruta = os.path.join(carpeta, 'sub_h', f'{k:02d}.png')
        im.save(ruta)
        entradas.append((ruta, round(tr['ini'] - INI, 2), round(tr['fin'] - INI, 2)))

    # cierre
    C = Image.new('RGB', (W, H), NAVY_DEEP)
    dc = ImageDraw.Draw(C)
    dc.rectangle((160, 300, 240, 306), fill=VERDE)
    dc.text((160, 340), 'Rayos X de Inscripciones', font=fuente('ExtraBold', 96), fill=BLANCO)
    dc.text((160, 470), 'En 60 minutos te decimos dónde pierde alumnos tu colegio.', font=fuente('SemiBold', 46), fill=SUB)
    dc.text((160, 560), 'Diagnóstico sin costo · superleads.mx/rayos_x', font=fuente('ExtraBold', 54), fill=VERDE)
    C.paste(logo.resize((320, round(logo.height * 320 / logo.width)), Image.LANCZOS), (160, H - 80 - round(logo.height * 320 / logo.width)), logo.resize((320, round(logo.height * 320 / logo.width)), Image.LANCZOS))
    ruta_cierre = os.path.join(carpeta, 'cierre_h.png')
    C.save(ruta_cierre)

    inputs = ['-ss', str(INI), '-to', str(FIN), '-i', os.path.join(carpeta, 'video.mp4'), '-i', ruta_fijo]
    for ruta, _, _ in entradas:
        inputs += ['-i', ruta]
    n_in = 2 + len(entradas)
    inputs += ['-loop', '1', '-t', str(CIERRE), '-i', ruta_cierre]
    fc = [f'color=c=0x001240:s={W}x{H}:r=30[bg]',
          f'[0:v]crop={kw}:{kh}:{kx}:{ky},scale={CAM_W}:{cam_h}:flags=lanczos[cam]',
          f'[bg][cam]overlay={CAM_XY[0]}:{CAM_XY[1]}:shortest=1[a]',
          '[a][1:v]overlay=0:0[c]']
    prev = 'c'
    for k, (_, a, b) in enumerate(entradas):
        fc.append(f"[{prev}][{k + 2}:v]overlay=0:{y_sub}:enable='between(t,{a},{b})'[s{k}]")
        prev = f's{k}'
    fc.append(f'[{prev}]fade=t=in:st=0:d=0.3,fade=t=out:st={dur - 0.4}:d=0.4,format=yuv420p,setsar=1[cuerpo]')
    fc.append(f'[{n_in}:v]scale={W}:{H},fade=t=in:st=0:d=0.3,fade=t=out:st={CIERRE - 0.5}:d=0.5,format=yuv420p,setsar=1,fps=30[cierre]')
    fc.append('anullsrc=r=48000:cl=stereo[sil]')
    fc.append(f'[sil]atrim=0:{CIERRE}[silc]')
    fc.append(f'[0:a]afade=t=in:st=0:d=0.2,afade=t=out:st={dur - 0.6}:d=0.6,aformat=sample_rates=48000:channel_layouts=stereo[ac]')
    fc.append('[cuerpo][ac][cierre][silc]concat=n=2:v=1:a=1[v][a]')
    cmd = ['ffmpeg', '-y', '-v', 'error'] + inputs + ['-filter_complex', ';'.join(fc), '-map', '[v]', '-map', '[a]',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', '18', '-r', '30', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', salida]
    subprocess.run(cmd, check=True)
    print(vid, f'{dur + CIERRE:.1f}s', len(entradas), 'trozos ·', salida)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
