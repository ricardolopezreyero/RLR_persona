"""Anuncios de la campaña de SEGUIDORES de la página de Facebook (objetivo único: que sigan la página).

Salen de lo que funcionó en X (aprendizajes/X-2026-11-03.md): la tarjeta tachada del IMSS y los anuncios de
seguidores para gente de admisiones (posts/tanda2/anuncios_seguidores.py). Tarjetas en 4:5 para el feed.
Escribe anuncios_seguidores.json y las tarjetas en anuncios_seguidores/."""
import json, os, sys, subprocess, datetime, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, 'tanda2'))
sys.path.insert(0, os.path.join(AQUI, '..', 'posts', 'tanda2'))
from hacer_fb import html_tarjeta  # noqa: E402
from hacer_tarjetas import CHROME  # noqa: E402

SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.join(AQUI, 'anuncios_seguidores')
TANDA = {p['n']: p for p in json.load(open(os.path.join(AQUI, '..', 'posts', 'tanda2', 'posts_tanda2.json')))}
CIERRE = 'Si tienes o diriges un colegio, sigue la página: escribo de admisiones todos los días.'

A = [
    dict(nombre='FB S·01 · Admisiones no es administrativa',
         texto="Tu área de admisiones no es administrativa. Es comercial.\n\nEl colegio mediano tiene 1.1 personas en admisiones, y 48 % no tiene plan de compensación para su equipo.\n\nAsí no se llena un colegio. Así se contesta cuando se puede.\n\n" + CIERRE,
         titulo='Admisiones es el área comercial',
         tarjeta=dict(etiqueta='PARA QUIEN DIRIGE UN COLEGIO', arriba='Admisiones no es un área', tachado='administrativa.',
                      respuesta='Es el área comercial.', pie='Colegio mediano: 1.1 personas en admisiones · 48 % sin plan de compensación')),
    dict(nombre='FB S·02 · Se fue con el que contestó primero',
         texto="La familia no se fue con la competencia. Se fue con el que contestó primero.\n\n78 % le compra al primero que responde, y solo 7 % de las organizaciones contesta en 5 minutos.\n\nCronometra hoy la primera respuesta de tu colegio.\n\n" + CIERRE,
         titulo='Se fue con el que contestó primero',
         tarjeta=dict(etiqueta='ADMISIONES · PRIMERA RESPUESTA', arriba='No se fue con la', tachado='competencia.',
                      respuesta='Se fue con el que contestó primero.', pie='78 % le compra al primero que responde · solo 7 % contesta en 5 minutos')),
]
# Tres tarjetas de la tanda 2 que siguen la fórmula del IMSS: 46 % de ocupación, el WhatsApp de $450,000 MXN y el precio.
for n, titulo in ((1, 'Tu colegio no está vacío'), (10, 'Un WhatsApp sin contestar cuesta'), (13, 'No se fueron por el precio')):
    p = TANDA[n]
    A.append(dict(nombre=f'FB S·{len(A) + 1:02d} · post {n:02d} · {titulo}', texto=p['texto'] + '\n\n' + CIERRE,
                  titulo=titulo, tarjeta=p['tarjeta']))


def main():
    os.makedirs(SALIDA, exist_ok=True)
    tmp = tempfile.mkdtemp()
    for k, a in enumerate(A, 1):
        f = os.path.join(tmp, f'{k}.html')
        open(f, 'w').write(html_tarjeta(a['tarjeta']))
        out = os.path.join(SALIDA, f"Anuncio FB seguidores {k:02d} · {a['tarjeta']['respuesta'].rstrip('.')} · v1 · {SELLO}.png".replace('/', '-').replace('$', ''))
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1080,1350', f'--screenshot={out}', 'file://' + f], check=True, capture_output=True)
        a['imagen'] = out
        a['caracteres'] = len(a['texto'])
        print(k, a['nombre'], a['caracteres'])
    json.dump(A, open(os.path.join(AQUI, 'anuncios_seguidores.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
