"""Portada de la página de Facebook: la misma frase bandera de X y YouTube.
Facebook recorta distinto en computadora (820×312, recorta arriba y abajo) y en celular (640×360,
recorta los lados), así que el lienzo es 1640×924 y el texto va centrado en la franja que ambos ven."""
import os, sys, datetime
from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', '..', 'posts'))
from hacer_visuales import f  # noqa: E402

NEGRO, BLANCO, ACENTO = (13, 13, 13), (245, 245, 240), (255, 199, 44)
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.expanduser('~/Desktop/HTML/RLR_marca_personal')
os.makedirs(SALIDA, exist_ok=True)

W, H = 1640, 924
P = Image.new('RGB', (W, H), NEGRO)
d = ImageDraw.Draw(P)
cx, tam, paso = W // 2, 92, 104
y0 = H // 2 - paso * 1.5 + 8
d.rectangle((cx - 40, y0 - 44, cx + 40, y0 - 36), fill=ACENTO)
d.text((cx, y0), 'El sistema con el que', font=f('heavy', tam), fill=BLANCO, anchor='ma')
d.text((cx, y0 + paso), 'operamos produce', font=f('heavy', tam), fill=BLANCO, anchor='ma')
d.text((cx, y0 + paso * 2), 'el resultado.', font=f('heavy', tam), fill=ACENTO, anchor='ma')
P.save(os.path.join(AQUI, 'fb-portada.png'))
P.save(os.path.join(SALIDA, f'Portada Facebook · frase bandera · v1 · {SELLO}.png'))
print(os.path.join(AQUI, 'fb-portada.png'))
