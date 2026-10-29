"""Variantes de foto de perfil para X a partir del avatar oficial (avatar-rlr-400.jpg).
Mismo lenguaje visual de los posts: negro, blanco roto, amarillo y rojo para negar/sellar.
Genera 4 variantes 1200×1200, una propuesta de portada 1500×500 y una hoja de comparación."""
import os, sys, datetime
from PIL import Image, ImageDraw, ImageOps, ImageEnhance, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', 'posts'))
from hacer_visuales import f  # noqa: E402  (fuente Avenir Next por peso)

NEGRO, BLANCO, ACENTO, ROJO = (13, 13, 13), (245, 245, 240), (255, 199, 44), (229, 36, 43)
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.expanduser('~/Desktop/HTML/RLR_marca_personal')
os.makedirs(SALIDA, exist_ok=True)
N = 1200

base = Image.open(os.path.join(AQUI, 'avatar-rlr-400.jpg')).convert('RGB').resize((N, N), Image.LANCZOS)
gris = ImageOps.autocontrast(ImageEnhance.Contrast(base.convert('L')).enhance(1.35), cutoff=1)


def sello(im, texto, xy, angulo=-12, color=ROJO, tam=150, grosor=16):
    fu = f('heavy', tam)
    tmp = Image.new('RGBA', (N * 2, 600), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    w = d.textlength(texto, font=fu)
    x0, y0 = N - w / 2 - 50, 300 - tam * 0.78
    d.rounded_rectangle((x0, y0, x0 + w + 100, y0 + tam * 1.56), radius=28, outline=color, width=grosor)
    d.text((N, 300), texto, font=fu, fill=color, anchor='mm')
    tmp = tmp.rotate(angulo, resample=Image.BICUBIC, expand=True)
    im.paste(tmp, (int(xy[0] - tmp.width / 2), int(xy[1] - tmp.height / 2)), tmp)


def banda(im, texto, color=ROJO, texto_color=BLANCO, alto=190):
    """Banda inclinada en la parte baja con una palabra: se lee incluso en círculo chico."""
    tmp = Image.new('RGBA', (N * 2, N * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    y = N + 330
    d.rectangle((0, y, N * 2, y + alto), fill=color)
    d.text((N, y + alto / 2), texto, font=f('heavy', 118), fill=texto_color, anchor='mm')
    tmp = tmp.rotate(-8, resample=Image.BICUBIC)
    im.paste(tmp, (-N // 2, -N // 2), tmp)


# 1 · Duotono amarillo: la cara en negro y amarillo, sin texto. Gráfico, nada de foto bonita.
v1 = ImageOps.colorize(gris, black=NEGRO, white=ACENTO, mid=(190, 140, 25))

# 2 · Duotono + sello INCÓMODO
v2 = v1.copy()
sello(v2, 'INCÓMODO', (N * 0.5, N * 0.74), angulo=-10, tam=128, grosor=14)

# 3 · Alto contraste en blanco y negro con banda roja SIN FILTRO
pos = gris.point(lambda p: 0 if p < 95 else (120 if p < 170 else 255))
v3 = ImageOps.colorize(pos, black=NEGRO, white=BLANCO).convert('RGB')
banda(v3, 'SIN FILTRO')

# 4 · Negativo sobre negro: la cara en blanco "quemado", borde amarillo grueso
neg = ImageOps.invert(gris)
neg = ImageOps.autocontrast(neg, cutoff=2)
v4 = ImageOps.colorize(neg, black=NEGRO, white=BLANCO).convert('RGB')
d = ImageDraw.Draw(v4)
d.ellipse((0, 0, N - 1, N - 1), outline=ACENTO, width=46)

VARIANTES = [('1 duotono amarillo', v1), ('2 duotono con sello INCÓMODO', v2), ('3 blanco y negro SIN FILTRO', v3), ('4 negativo con aro amarillo', v4)]
for nombre, im in VARIANTES:
    im.convert('RGB').save(os.path.join(SALIDA, f'Avatar X · {nombre} · v1 · {SELLO}.png'))
    im.convert('RGB').save(os.path.join(AQUI, f'x-{nombre.split()[0]}.png'))

# Portada 1500×500 con una frase bandera
P = Image.new('RGB', (1500, 500), NEGRO)
d = ImageDraw.Draw(P)
d.rectangle((70, 90, 150, 98), fill=ACENTO)
d.text((70, 128), 'El sistema con el que', font=f('heavy', 96), fill=BLANCO)
d.text((70, 232), 'operamos produce', font=f('heavy', 96), fill=BLANCO)
d.text((70, 336), 'el resultado.', font=f('heavy', 96), fill=ACENTO)
d.text((1430, 440), 'Ing. Ricardo López Reyero · Torreón', font=f('demi', 30), fill=(140, 140, 135), anchor='rs')
P.save(os.path.join(SALIDA, f'Portada X · frase bandera · v1 · {SELLO}.png'))
P.save(os.path.join(AQUI, 'x-portada.png'))

# Hoja de comparación: cada variante en círculo grande y chico sobre fondo X (negro)
H = Image.new('RGB', (2400, 1500), (0, 0, 0))
d = ImageDraw.Draw(H)
d.text((60, 50), 'Foto de perfil para X · 4 variantes · así se ven en círculo (grande y en el feed)', font=f('demi', 44), fill=BLANCO)
for k, (nombre, im) in enumerate(VARIANTES):
    x = 60 + k * 590
    for tam, y in ((420, 150), (96, 640), (48, 780)):
        c = im.convert('RGB').resize((tam, tam), Image.LANCZOS)
        m = Image.new('L', (tam * 4, tam * 4), 0)
        ImageDraw.Draw(m).ellipse((0, 0, tam * 4 - 1, tam * 4 - 1), fill=255)
        H.paste(c, (x, y), m.resize((tam, tam), Image.LANCZOS))
        if tam < 400:
            d.text((x + tam + 24, y + tam / 2), 'Ricardo López Reyero', font=f('bold', 30 if tam > 60 else 22), fill=BLANCO, anchor='lm')
    d.text((x, 880), nombre.upper(), font=f('demi', 30), fill=ACENTO)
H.paste(P.resize((1125, 375), Image.LANCZOS), (60, 1000))
d.text((1260, 1010), 'Portada 1500×500 (propuesta)', font=f('demi', 30), fill=ACENTO)
H.save(os.path.join(SALIDA, f'Avatar X · comparación · v1 · {SELLO}.png'))
print(SALIDA)
