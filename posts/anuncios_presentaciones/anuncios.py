"""Campaña de X Ads «Presentaciones» (9-nov-2026): 4 anuncios que llevan al artículo
«Hay más familias queriendo inscribirse en tu colegio de las que tu proceso alcanza a inscribir».

Base mínima de X (aprendizajes/X-Ads-2026-11-06.md): la negación de algo que el director sí cree arriba, la causa real,
un número que duela y la tarjeta tachada; la invitación al artículo al final, nunca de gancho.
Cada texto ≤280 caracteres contando la liga como 23. Escribe anuncios.json, datos.html y las tarjetas en tarjetas/."""
import json, os, re, subprocess, tempfile, sys, datetime
sys.path.insert(0, os.path.expanduser('~/Code/RLR_persona/posts/tanda2'))
from anuncios_trafico import tarjeta, CHROME

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, 'tarjetas')
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
ARTICULO = 'https://x.com/ricardolopezrey/status/2119912581720658195'
ETQ = 'ARTÍCULO · 14 LÁMINAS'

# (texto sin liga, arriba, tachado, respuesta, pie)
A = [
    ("No te faltan familias. Te falta contestarles.\n\nEn México, 35 % de los hogares puede pagar un colegio privado y solo 10 % de los alumnos está en uno.\n\nLo explico lámina por lámina en este artículo:",
     'No te faltan', 'familias.', 'Te falta contestarles.',
     '35 % de los hogares puede pagar · solo 10 % de los alumnos está en privada'),
    ("No se fueron por el precio. Se fueron por el silencio.\n\n44 % de las consultas a instituciones educativas nunca recibe respuesta. La que sí llega tarda 14 horas.\n\nLos datos y las láminas, en este artículo:",
     'No se fueron por el', 'precio.', 'Se fueron por el silencio.',
     '44 % nunca recibe respuesta · la respuesta promedio tarda 14 h 23 min'),
    ("No es falta de esfuerzo. Es falta de sistema.\n\n71 % de los colegios lleva sus admisiones en WhatsApp, Excel o a mano. Cada familia que se pierde ahí vale hasta $450,000 MXN.\n\nLo escribí completo aquí:",
     'No es falta de', 'esfuerzo.', 'Es falta de sistema.',
     '71 % en WhatsApp, Excel o a mano · cada familia vale hasta $450,000 MXN'),
    ("El problema no es la demanda. Es el proceso.\n\nLa institución mediana opera al 46 % de su capacidad, y de cada 100 familias que escriben se inscriben 2.4.\n\nEl artículo completo, con las láminas de mi charla:",
     'El problema no es', 'la demanda.', 'Es el proceso.',
     'Colegios al 46 % de su capacidad · 2.4 de cada 100 familias se inscriben'),
]


def main():
    os.makedirs(SALIDA, exist_ok=True)
    tmp = tempfile.mkdtemp(); out = []
    for i, (t, arriba, tach, resp, pie) in enumerate(A, 1):
        url = f'{ARTICULO}?utm_source=x&utm_medium=paid&utm_campaign=presentaciones&utm_content=pr-{i:02d}'
        texto = f'{t}\n{ARTICULO}'
        n = len(re.sub(r'https?://\S+', 'x' * 23, texto))
        assert n <= 280, (i, n)
        f = os.path.join(tmp, f'{i}.html'); open(f, 'w').write(tarjeta(ETQ, arriba, tach, resp, pie))
        img = os.path.join(SALIDA, f'Presentaciones {i:02d} · {resp.rstrip(".")} · v1 · {SELLO}.png')
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1600,838', f'--screenshot={img}', 'file://' + f], check=True, capture_output=True)
        out.append({'n': i, 'nombre': f'PR · {i:02d} · {t.split(chr(10))[0][:45]}', 'texto': texto, 'caracteres': n,
                    'url': url, 'imagen': img})
    json.dump(out, open(os.path.join(AQUI, 'anuncios.json'), 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(AQUI, 'datos.html'), 'w').write('<!doctype html><meta charset="utf-8"><title>datos</title><script>window.__A=' + json.dumps(out, ensure_ascii=False) + ';</script>ok')
    print([a['caracteres'] for a in out])


if __name__ == '__main__':
    main()
