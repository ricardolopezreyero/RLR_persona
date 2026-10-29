"""Portada vertical 1080×1920 por Short (gancho grande + cuadro de la cámara + logo) y publicar.json con título,
descripción y fecha/hora de programación por video."""
import os, json, subprocess
from PIL import Image, ImageDraw, ImageFont
from hacer_short import CONFIG, fuente, NAVY_DEEP, VERDE, BLANCO, SUB, W, H, AQUI

ORDEN = ['ZP5BSoRFaio', '0tRgTomkaAw', 'oqLweG2S0Bk', 'mDfb_nteAe8', 'aZggkBKgqrg']
# hora prime para directores de colegio en México: mediodía entre semana (12:30) y 11:00 el sábado
PROGRAMA = {'ZP5BSoRFaio': ('2026-10-29', '12:30'), '0tRgTomkaAw': ('2026-10-30', '12:30'), 'oqLweG2S0Bk': ('2026-10-31', '11:00'),
            'mDfb_nteAe8': ('2026-11-02', '12:30'), 'aZggkBKgqrg': ('2026-11-03', '12:30')}
# segundo del video fuente donde Ricardo mira a cámara (elegido viendo cuadros)
CARA = {'ZP5BSoRFaio': 123.0, '0tRgTomkaAw': 228.0, 'oqLweG2S0Bk': 1346.0, 'mDfb_nteAe8': 1200.0, 'aZggkBKgqrg': 1050.0}
TIT = json.load(open(os.path.join(AQUI, 'titulos_videos.json')))
os.makedirs(os.path.join(AQUI, 'portadas'), exist_ok=True)
pub = []
for k, vid in enumerate(ORDEN, 1):
    sel = json.load(open(os.path.join(AQUI, 'v', vid, 'seleccion.json')))
    kx, ky, kw, kh = CONFIG[vid]['cam']
    raw = os.path.join(AQUI, 'portadas', f'{vid}_cara.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-ss', str(CARA[vid]), '-i', os.path.join(AQUI, 'v', vid, 'video.mp4'), '-frames:v', '1', '-vf', f'crop={kw}:{kh}:{kx}:{ky}', '-y', raw], check=True)
    cara = Image.open(raw).convert('RGB')
    cw0 = round(cara.width * 0.68); cx0 = (cara.width - cw0) // 2 + 20
    cara = cara.crop((cx0, 0, cx0 + cw0, cara.height))
    # la cara ocupa la mitad inferior: ancho 1080, recorte centrado a 1080×1000
    esc = W / cara.width
    cara = cara.resize((W, round(cara.height * esc)), Image.LANCZOS)
    P = Image.new('RGB', (W, H), NAVY_DEEP)
    P.paste(cara, (0, H - cara.height - 140))
    # degradado navy sobre la parte alta de la cara para que el texto respire
    grad = Image.new('L', (1, 400))
    for y in range(400):
        grad.putpixel((0, y), int(255 * (1 - y / 400) ** 1.4))
    grad = grad.resize((W, 400))
    P.paste(Image.new('RGB', (W, 400), NAVY_DEEP), (0, H - cara.height - 140), grad)
    # franja inferior navy con el logo
    d = ImageDraw.Draw(P)
    d.rectangle((0, H - 140, W, H), fill=NAVY_DEEP)
    logo = Image.open(os.path.join(AQUI, 'marca', 'logo_blanco.png')).convert('RGBA')
    logo = logo.resize((260, round(logo.height * 260 / logo.width)), Image.LANCZOS)
    P.paste(logo, (60, H - 70 - logo.height // 2), logo)
    d.text((W - 60, H - 70), 'Ing. Ricardo López Reyero', font=fuente('Medium', 32), fill=SUB, anchor='rm')
    # gancho
    y = 190
    n = len(sel['gancho'])
    for i, linea in enumerate(sel['gancho']):
        tam = 118
        fu = fuente('ExtraBold', tam)
        while d.textlength(linea, font=fu) > W - 120 and tam > 70:
            tam -= 4; fu = fuente('ExtraBold', tam)
        d.text((60, y), linea, font=fu, fill=VERDE if i == n - 1 else BLANCO)
        y += int(tam * 1.12)
    d.rectangle((60, y + 24, 160, y + 30), fill=VERDE)
    ruta = os.path.join(AQUI, 'portadas', f'{vid}.png')
    P.save(ruta)
    fecha, hora = PROGRAMA[vid]
    titulo = sel['frase'] + ' #Shorts'
    desc = (sel['descripcion'] + f'\n\nVideo completo: https://www.youtube.com/watch?v={vid}\n'
            'Rayos X de Inscripciones (diagnóstico sin costo): https://superleads.mx/rayos_x\n\n'
            'Soy el Ing. Ricardo López Reyero, Founder Comercial de SuperLeads. Solo hacemos admisiones: por nuestro sistema pasan más de 300,000 prospectos educativos al año. Más en https://superleads.mx')
    pub.append({'n': k, 'id': vid, 'archivo': os.path.join(AQUI, 'out', f'{vid}.mp4'), 'portada': ruta, 'titulo': titulo, 'descripcion': desc, 'fecha': fecha, 'hora': hora, 'largo': TIT[vid]})
json.dump(pub, open(os.path.join(AQUI, 'publicar.json'), 'w'), ensure_ascii=False, indent=1)
print('\n'.join(f"{p['n']} {p['fecha']} {p['hora']} · {p['titulo']} ({len(p['titulo'])})" for p in pub))
