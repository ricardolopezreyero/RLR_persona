"""Piezas visuales de los 9 posts de X (estilo personal: negro, blanco y un acento)."""
import os, datetime, glob
from PIL import Image, ImageDraw, ImageFont, ImageOps

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
W, H = 1600, 900
NEGRO, BLANCO, GRIS, ACENTO = (13, 13, 13), (245, 245, 240), (140, 140, 135), (255, 199, 44)
AV = '/System/Library/Fonts/Supplemental/Avenir Next.ttc'
MONO = '/System/Library/Fonts/SFNSMono.ttf'
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')


def f(peso, tam):
    return ImageFont.truetype(AV, tam, index={'heavy': 8, 'bold': 0, 'demi': 2, 'medium': 5, 'regular': 7, 'italic': 4}[peso])


def envolver(d, texto, fuente, ancho):
    lineas = []
    for parrafo in texto.split('\n'):
        actual = ''
        for p in parrafo.split(' '):
            prueba = (actual + ' ' + p).strip()
            if d.textlength(prueba, font=fuente) <= ancho:
                actual = prueba
            else:
                lineas.append(actual)
                actual = p
        lineas.append(actual)
    return lineas


def lienzo():
    im = Image.new('RGB', (W, H), NEGRO)
    return im, ImageDraw.Draw(im)


def pie(d, oscuro=True):
    d.text((110, H - 92), 'Ing. Ricardo López Reyero · Torreón', font=f('demi', 30), fill=BLANCO if oscuro else NEGRO)
    d.text((W - 110, H - 92), '@ricardolopezrey', font=f('medium', 30), fill=GRIS, anchor='ra')


def tarjeta(etiqueta, frase, remate=None, tam=84):
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), etiqueta.upper(), font=f('demi', 30), fill=ACENTO)
    fuente = f('heavy', tam)
    lineas = envolver(d, frase, fuente, W - 220)
    y = 230
    for l in lineas:
        d.text((110, y), l, font=fuente, fill=BLANCO)
        y += int(tam * 1.18)
    if remate:
        d.text((110, y + 28), remate, font=f('medium', 38), fill=GRIS)
    pie(d)
    return im


def guardar(im, n, titulo, ext='png', **kw):
    nombre = f'Post {n} · {titulo} · v1 · {SELLO}.{ext}'
    im.save(os.path.join(AQUI, nombre), **kw)
    return nombre


def post_democracia():
    # su propia infografía, tal cual
    src = glob.glob(os.path.join(RAIZ, 'imagenes', '01_*__img1.*'))[0]
    return guardar(ImageOps.exif_transpose(Image.open(src)).convert('RGB'), 1, 'El fin de la democracia')


def post_presidentes():
    return guardar(tarjeta('Selección presidencial 2.0',
                           'Candidatos a presidente: los 6 gobernadores que más subieron el ingreso por persona en su estado.',
                           'Medido cada año. Público. Sin campañas, sin opiniones.', 78), 2, 'Presidentes seleccionados')


def post_sueldos():
    return guardar(tarjeta('Gobierno 2.0', 'Un Player A no deja la iniciativa privada por amor al arte.',
                           'Lo mejor se paga. Con bonos atados a resultados.', 96), 3, 'Sueldos competitivos en gobierno')


def post_impuestos():
    im, d = lienzo()
    d.text((110, 138), 'COBRANZA DE IMPUESTOS 2.0', font=f('demi', 30), fill=ACENTO)
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 220), 'No son impuestos.', font=f('heavy', 84), fill=BLANCO)
    d.text((110, 320), 'Son aportaciones.', font=f('heavy', 84), fill=ACENTO)
    d.text((110, 450), 'Y quien aporta es un donador,\nno un sospechoso.', font=f('medium', 44), fill=GRIS, spacing=14)
    # recibo
    x0, y0, x1, y1 = 1010, 120, 1490, 780
    d.rectangle((x0 + 10, y0 + 10, x1 + 10, y1 + 10), fill=(40, 40, 38))
    d.rectangle((x0, y0, x1, y1), fill=(250, 248, 240))
    m = ImageFont.truetype(MONO, 25)
    mb = ImageFont.truetype(MONO, 30)
    filas = [('RECIBO DE APORTACIÓN', mb), ('', m), ('Ciudadano:      Tú', m), ('Folio:          000001', m), ('', m),
             ('Tu aportación construyó:', m), ('  · la calle de hoy', m), ('  · la luz de tu casa', m), ('  · el agua de la llave', m),
             ('  · la seguridad', m), ('', m), ('- - - - - - - - - - - - -', m), ('', m), ('GRACIAS POR CONSTRUIR', mb), ('TU CIUDAD.', mb)]
    y = y0 + 40
    for t, fu in filas:
        d.text((x0 + 36, y), t, font=fu, fill=NEGRO)
        y += 38
    pie(d)
    return guardar(im, 4, 'Impuestos son aportaciones')


def post_carceles():
    return guardar(tarjeta('Presos y cárceles 2.0', 'Las cárceles deberían tener las bibliotecas más grandes de la ciudad.',
                           'Emociones todos los días. Un oficio. Y libros.', 92), 5, 'Carceles con bibliotecas')


def post_imss():
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'EL ERROR DE 1943 · IMSS', font=f('demi', 30), fill=ACENTO)
    d.text((110, 210), 'Torreón aporta al IMSS ~$5,000 millones al año.', font=f('heavy', 58), fill=BLANCO)
    d.text((110, 290), '~$500 millones no compran ni una consulta.', font=f('heavy', 58), fill=ACENTO)
    bx0, bx1, by0, by1 = 110, W - 110, 440, 560
    corte = bx0 + (bx1 - bx0) * 0.9
    d.rectangle((bx0, by0, corte, by1), fill=(70, 70, 66))
    d.rectangle((corte + 6, by0, bx1, by1), fill=ACENTO)
    d.text((bx0 + 30, by0 + 38), 'Atención médica  ~$4,500 M', font=f('demi', 38), fill=BLANCO)
    d.text((bx1, by1 + 24), '~$500 M (10%) · pensiones del régimen 1966\nde exempleados del propio IMSS', font=f('demi', 32), fill=ACENTO, anchor='ra', align='right', spacing=10)
    d.text((110, 700), 'No es falta de dinero ni solo robo. Es la arquitectura.', font=f('medium', 38), fill=GRIS)
    d.text((110, 750), 'Cálculo propio con cuotas de La Laguna · artículo «El error de 1943»', font=f('regular', 26), fill=(95, 95, 92))
    pie(d)
    return guardar(im, 6, 'IMSS el error de 1943')


def post_redes_gif():
    w, h = 1200, 675
    frames = []
    fn = ImageFont.truetype(AV, 230, index=8)
    total = 1171
    pasos = 46
    for i in range(pasos + 24):
        t = min(1, i / pasos)
        val = round(total * (1 - (1 - t) ** 3))
        im = Image.new('RGB', (w, h), NEGRO)
        d = ImageDraw.Draw(im)
        d.rectangle((80, 80, 140, 86), fill=ACENTO)
        d.text((80, 104), '0 REDES SOCIALES', font=f('demi', 26), fill=ACENTO)
        d.text((80, 170), f'{val:,}', font=fn, fill=ACENTO if t >= 1 else BLANCO)
        d.text((86, 440), 'días sin redes sociales', font=f('heavy', 58), fill=BLANCO)
        d.text((86, 520), '20.01.2023  —  05.04.2026', font=f('medium', 34), fill=GRIS)
        d.text((80, h - 70), 'Ing. Ricardo López Reyero · @ricardolopezrey', font=f('demi', 24), fill=GRIS)
        frames.append(im.convert('P', palette=Image.ADAPTIVE, colors=32))
    duraciones = [45] * pasos + [120] * 23 + [2500]
    nombre = f'Post 7 · 1171 dias sin redes · v1 · {SELLO}.gif'
    frames[0].save(os.path.join(AQUI, nombre), save_all=True, append_images=frames[1:], duration=duraciones, loop=0, optimize=True)
    return nombre


def post_uno_por_ciento():
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'ESTAR EN EL 1% MÁS RICO', font=f('demi', 30), fill=ACENTO)
    d.text((100, 170), '0.3%', font=ImageFont.truetype(AV, 330, index=8), fill=ACENTO)
    d.text((110, 560), 'Ganar $250,000 al mes en México te pone ahí.', font=f('heavy', 56), fill=BLANCO)
    d.text((110, 640), 'Y aun así discutíamos por dinero.', font=f('medium', 44), fill=GRIS)
    pie(d)
    return guardar(im, 8, 'El 0.3 por ciento')


def post_pavimento():
    src = glob.glob(os.path.join(RAIZ, 'imagenes', '08_*__img1.*'))[0]
    base = ImageOps.fit(ImageOps.exif_transpose(Image.open(src)).convert('RGB'), (W, H), centering=(0.5, 0.45))
    sombra = Image.new('L', (W, H))
    sd = ImageDraw.Draw(sombra)
    for y in range(H):
        sd.line((0, y, W, y), fill=int(242 * min(1, max(0, (y - 360) / 200))))
    im = Image.composite(Image.new('RGB', (W, H), NEGRO), base, sombra)
    d = ImageDraw.Draw(im)
    d.rectangle((110, 520, 190, 528), fill=ACENTO)
    d.text((110, 545), 'TORREÓN · EL PAVIMENTO IDEAL', font=f('demi', 30), fill=ACENTO)
    d.text((110, 595), 'Concreto hidráulico claro.', font=f('heavy', 78), fill=BLANCO)
    d.text((110, 690), 'Menos calor. Menos ruido. Décadas de vida.', font=f('medium', 42), fill=(220, 220, 215))
    pie(d)
    return guardar(im, 9, 'Pavimento ideal Torreon')


if __name__ == '__main__':
    for fn in (post_democracia, post_presidentes, post_sueldos, post_impuestos, post_carceles, post_imss,
               post_redes_gif, post_uno_por_ciento, post_pavimento):
        print(fn())
