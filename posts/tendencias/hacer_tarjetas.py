"""Tarjetas 1600×900 de las tendencias semanales. Usa la plantilla de ../tanda2/hacer_tarjetas.py
(formato IMSS: lo que creen tachado en rojo, lo que es en amarillo; nombre a la izquierda, logo a la derecha).
Uso: python3 hacer_tarjetas.py 2026-11-09"""
import json, os, sys, subprocess, tempfile
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'tanda2'))
from hacer_tarjetas import html_tarjeta, CHROME, SELLO

fecha = sys.argv[1]
ruta = os.path.join(AQUI, f'{fecha}.json')
d = json.load(open(ruta))
salida = os.path.join(AQUI, 'visuales', fecha)
os.makedirs(salida, exist_ok=True)
tmp = tempfile.mkdtemp()
for p in d['posts']:
    t = p.get('tarjeta')
    if not t:
        continue
    f = os.path.join(tmp, f"{p['n']}.html")
    open(f, 'w').write(html_tarjeta(t))
    nombre = f"Tendencia {p['n']:02d} · {t['respuesta'].rstrip('.')} · v1 · {SELLO}.png".replace('/', '-').replace('$', '')
    out = os.path.join(salida, nombre)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                    '--window-size=1600,900', f'--screenshot={out}', 'file://' + f], check=True, capture_output=True)
    p['visual'] = f'visuales/{fecha}/{nombre}'
    print(nombre)
json.dump(d, open(ruta, 'w'), ensure_ascii=False, indent=1)
