"""3 anuncios para la campaña de SEGUIDORES (TEXTO, 42917614, en pausa) dirigidos a gente de admisiones educativas.

Salen de lo que funcionó:
- el texto personal sin imagen («Todo es mi culpa») trajo más visitas al perfil por peso;
- la tarjeta tachada (IMSS) trajo más guardados.
Cierre con invitación a seguir, porque el objetivo es seguidores. Cifras del corte Rayos X oct-2026 y de la serie
«La realidad de la educación». Escribe anuncios_seguidores.json y las tarjetas en anuncios_seguidores/."""
import json, os, subprocess, datetime, tempfile, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from hacer_tarjetas import html_tarjeta, CHROME  # noqa: E402

SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.join(AQUI, 'anuncios_seguidores')

A = [
    dict(nombre='S · 01 · Si trabajas en admisiones (texto)',
         texto="Si trabajas en admisiones, esto es para ti:\n\nNo te faltan prospectos. Te falta un sistema.\n\nDe cada 100 familias que preguntan por un colegio privado, 2 se inscriben. Y hay colegios que inscriben a más de 10 con las mismas 100.\n\nEscribo de admisiones todos los días. Sígueme.",
         fuente='Corte Rayos X oct-2026 (conversión mediana 2.4 %); Rayos X oct-14: 9 % de los colegios convierte más de 10 % (n=57)',
         tarjeta=None),
    dict(nombre='S · 02 · Admisiones no es administrativa (tarjeta)',
         texto="Tu área de admisiones no es administrativa. Es comercial.\n\nEl colegio mediano tiene 1.1 personas en admisiones, y 48 % no tiene plan de compensación para su equipo.\n\nAsí no se llena un colegio. Así se contesta cuando se puede.\n\nEscribo de admisiones todos los días. Sígueme.",
         fuente='Corte Rayos X oct-2026 (series 14 y 15)',
         tarjeta=dict(etiqueta='PARA QUIEN TRABAJA EN ADMISIONES', arriba='Admisiones no es un área', tachado='administrativa.',
                      respuesta='Es el área comercial.', pie='Colegio mediano: 1.1 personas en admisiones · 48 % sin plan de compensación')),
    dict(nombre='S · 03 · Se fue con el que contestó primero (tarjeta)',
         texto="La familia no se fue con la competencia. Se fue con el que contestó primero.\n\n78 % le compra al primero que responde, y solo 7 % de las organizaciones contesta en 5 minutos.\n\nSi trabajas en admisiones, cronometra hoy tu primera respuesta.\n\nSígueme para más.",
         fuente='Serie Realidad #14 (MIT, HBR, Velocify)',
         tarjeta=dict(etiqueta='ADMISIONES · PRIMERA RESPUESTA', arriba='No se fue con la', tachado='competencia.',
                      respuesta='Se fue con el que contestó primero.', pie='78 % le compra al primero que responde · solo 7 % contesta en 5 minutos')),
]


def main():
    os.makedirs(SALIDA, exist_ok=True)
    tmp = tempfile.mkdtemp()
    for k, a in enumerate(A, 1):
        assert len(a['texto']) <= 280, (k, len(a['texto']))
        a['caracteres'] = len(a['texto'])
        a['imagen'] = None
        if a['tarjeta']:
            f = os.path.join(tmp, f'{k}.html')
            open(f, 'w').write(html_tarjeta(a['tarjeta']))
            out = os.path.join(SALIDA, f"Anuncio seguidores {k:02d} · {a['tarjeta']['respuesta'].rstrip('.')} · v1 · {SELLO}.png")
            subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                            '--window-size=1600,900', f'--screenshot={out}', 'file://' + f], check=True, capture_output=True)
            a['imagen'] = out
        print(k, a['caracteres'], a['imagen'] or 'solo texto')
    json.dump(A, open(os.path.join(AQUI, 'anuncios_seguidores.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
