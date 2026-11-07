"""Cuatro anuncios nuevos para agendar un Rayos X (6-nov-2026), escritos con lo que enseñaron los 21 de tráfico.

Lo aprendido del 2 al 6-nov (aprendizajes/X-Ads-2026-11-06.md): gana la negación de una creencia en la primera
línea con la causa real en la segunda («No es el precio. Es el silencio.»), un solo número en MXN, el tema del
WhatsApp que nadie contestó y la tarjeta tachada. Pierden las listas, las preguntas como gancho, la historia
personal, la venta directa y el «es tu culpa».

Cada anuncio: ≤280 caracteres, tarjeta 1.91:1 tachada, liga a rayosx.superleads.mx/rayos_x con UTM propio.
Escribe anuncios_rayosx.json y las imágenes en anuncios_rayosx/."""
import json, os, subprocess, datetime, tempfile
from anuncios_trafico import tarjeta, CHROME

AQUI = os.path.dirname(os.path.abspath(__file__))
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.join(AQUI, 'anuncios_rayosx')
TITULO = 'Rayos X de Inscripciones · SuperLeads'
LIGA = 'https://rayosx.superleads.mx/rayos_x'

# (texto, etiqueta, arriba, tachado, respuesta, pie)
A = [
    ("No se fueron por el precio. Se fueron por el silencio.\n\n62 % de los directores culpa al precio. Pero 40 % de las familias que llegan a la cita se inscribe, al mismo precio.\n\nUn Rayos X de Inscripciones te dice en 10 minutos dónde se van las tuyas. Por ahora, sin costo.",
     'RAYOS X DE INSCRIPCIONES', 'No se fueron por el', 'precio.', 'Se fueron por el silencio.',
     '62 % culpa al precio · 40 % de quien llega a la cita se inscribe · Tu Rayos X, por ahora sin costo'),
    ("Un WhatsApp sin contestar no cuesta nada. Cuesta $450,000 MXN.\n\nColegiatura de $4,500 MXN, 6 años y un hermano: eso vale cada familia que escribió y nadie atendió.\n\nEn un Rayos X contamos cuántas se te fueron este mes. Por ahora, sin costo.",
     'RAYOS X DE INSCRIPCIONES', 'Un WhatsApp sin contestar', 'no cuesta nada.', 'Cuesta $450,000 MXN.',
     'Colegiatura $4,500 MXN × 6 años + un hermano · Tu Rayos X, por ahora sin costo'),
    ("El problema no es el precio ni la publicidad. Es el proceso.\n\nDe cada 100 familias que preguntan, 2 se inscriben. Subir un solo punto vale $109,500 MXN al año.\n\nUn Rayos X de Inscripciones te muestra tus 3 números en una sesión. Por ahora, sin costo.",
     'RAYOS X DE INSCRIPCIONES', 'De cada 100 familias,', 'faltan más familias.', '2 se inscriben.',
     'Un punto más de conversión vale $109,500 MXN al año · Tu Rayos X, por ahora sin costo'),
    ("Tu colegio no compite contra el de enfrente. Compite contra el silencio.\n\n78 % de las familias le compra al primero que responde. Solo 7 % contesta en 5 minutos.\n\n¿Quién contesta en tu colegio a las 11 de la noche? Un Rayos X te lo dice. Por ahora, sin costo.",
     'RAYOS X DE INSCRIPCIONES', 'Tu competencia no es', 'el colegio de enfrente.', 'Es el silencio.',
     '78 % le compra al primero que responde · solo 7 % contesta en 5 min · Tu Rayos X, por ahora sin costo'),
]


def main():
    os.makedirs(SALIDA, exist_ok=True)
    tmp = tempfile.mkdtemp()
    out = []
    for i, (texto, etq, arriba, tach, resp, pie) in enumerate(A, 1):
        assert len(texto) <= 280, (i, len(texto))
        f = os.path.join(tmp, f'{i}.html')
        open(f, 'w').write(tarjeta(etq, arriba, tach, resp, pie))
        img = os.path.join(SALIDA, f'Rayos X {i:02d} · {resp.rstrip(".")[:40]} · v1 · {SELLO}.png'.replace('$', '').replace('/', '-'))
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1600,838', f'--screenshot={img}', 'file://' + f], check=True, capture_output=True)
        out.append({'n': i, 'nombre': f'RX · {i:02d} · {texto.split(chr(10))[0][:45]}', 'texto': texto, 'caracteres': len(texto),
                    'url': f'{LIGA}?utm_source=x&utm_medium=paid&utm_campaign=x-trafico-rayosx&utm_content=rx-{i:02d}',
                    'titulo': TITULO, 'imagen': img})
    json.dump(out, open(os.path.join(AQUI, 'anuncios_rayosx.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(out), max(a['caracteres'] for a in out))


if __name__ == '__main__':
    main()
