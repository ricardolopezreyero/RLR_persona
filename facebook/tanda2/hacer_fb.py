"""La tanda 2 de X llevada al feed de Facebook (3-nov-2026).

Lo que se traslada de X (ver aprendizajes/X-2026-11-03.md):
- la fórmula del IMSS: niega la creencia, da el número, muestra el mecanismo, culpa al sistema, deja una sola salida;
- la tarjeta tachada, ahora en 4:5 (1080×1350), que es el formato que más ocupa del feed de Facebook;
- textos personales mezclados con tarjetas de datos; educación a fondo, cero política;
- una idea por post: uno al día a las 9:00, fuera de los Reels de 12:30 y 19:30;
- cierre que pide seguir la página, porque la meta en Facebook es la misma que en X: seguidores.
Escribe fb_tanda2.json y las tarjetas en tarjetas/."""
import json, os, sys, html, subprocess, datetime, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
TANDA = os.path.join(AQUI, '..', '..', 'posts', 'tanda2')
sys.path.insert(0, TANDA)
from hacer_tarjetas import CHROME, LOGO  # noqa: E402

SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.join(AQUI, 'tarjetas')
INICIO = datetime.date(2026, 11, 4)
HORA = '09:00'
CIERRE = 'Escribo de admisiones todos los días. Si tienes un colegio, sigue la página.'

# Orden del feed: abre con la fórmula que más funcionó en X (tarjeta tachada), alterna tarjeta, texto y largo,
# deja el #11 en el 11-nov para que «1,723 días» siga siendo cierto, y cierra con la invitación al Rayos X.
ORDEN = [1, 5, 3, 10, 2, 18, 13, 11, 4, 8, 6, 19, 14, 9, 16, 17, 12, 7, 20, 15, 21]

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#0D0D0D;color:#F5F5F0;font-family:'Avenir Next','Avenir',sans-serif;
 padding:0 84px;position:relative;overflow:hidden;display:flex;flex-direction:column;justify-content:center}
.caja{margin-top:-60px}
.barra{width:72px;height:8px;background:#FFC72C;margin-bottom:24px}
.etq{color:#FFC72C;font-size:27px;font-weight:600;letter-spacing:.5px}
.arriba{font-size:var(--t);font-weight:800;line-height:1.08;margin-top:40px}
.tachado{font-size:var(--t);font-weight:800;line-height:1.12;color:#8A8A85;position:relative;display:inline-block;margin-top:8px}
.tachado:after{content:'';position:absolute;left:-10px;right:-10px;top:52%;height:11px;background:#E5242B;transform:rotate(-1deg)}
.resp{font-size:var(--t);font-weight:800;line-height:1.08;color:#FFC72C;margin-top:12px}
.pie{font-size:32px;color:#8A8A85;margin-top:40px;line-height:1.3}
.firma{position:absolute;left:84px;bottom:66px;font-size:29px;font-weight:600}
.logo{position:absolute;right:84px;bottom:60px;width:220px}
.logo svg{width:220px;height:auto}
"""


def tamano(t):
    largo = max(len(t['arriba']), len(t['tachado']), len(t['respuesta']))
    return 104 if largo <= 18 else 92 if largo <= 23 else 84


def html_tarjeta(t):
    tach = f'<div><span class="tachado">{html.escape(t["tachado"])}</span></div>' if t['tachado'] else ''
    return f"""<!doctype html><meta charset="utf-8"><style>{CSS}</style>
<body style="--t:{tamano(t)}px"><div class="caja"><div class="barra"></div><div class="etq">{html.escape(t['etiqueta'])}</div>
<div class="arriba">{html.escape(t['arriba'])}</div>{tach}<div class="resp">{html.escape(t['respuesta'])}</div>
<div class="pie">{html.escape(t['pie'])}</div></div>
<div class="firma">Ing. Ricardo López Reyero · Torreón</div><div class="logo">{LOGO}</div></body>"""


def texto_fb(p):
    t = p['texto'].replace('Si tienes un colegio, sígueme.', 'Si tienes un colegio, sigue la página.')
    t = t.replace('https://superleads.mx/rayos_x', 'https://superleads.mx/rayos_x?utm_source=facebook&utm_medium=organico&utm_campaign=fb-tanda2')
    if 'sigue la página' not in t and p['embudo'] != 'conversion':
        t += '\n\n' + CIERRE
    return t


def main():
    os.makedirs(SALIDA, exist_ok=True)
    posts = {p['n']: p for p in json.load(open(os.path.join(TANDA, 'posts_tanda2.json')))}
    assert sorted(ORDEN) == sorted(posts)
    tmp = tempfile.mkdtemp()
    salida = []
    for k, n in enumerate(ORDEN):
        p = posts[n]
        fecha = INICIO + datetime.timedelta(days=k)
        if n == 11:
            assert fecha == datetime.date(2026, 11, 11)
            assert (fecha - datetime.date(2022, 2, 22)).days == 1723
        imagen = None
        if p.get('tarjeta'):
            f = os.path.join(tmp, f'{n}.html')
            open(f, 'w').write(html_tarjeta(p['tarjeta']))
            imagen = os.path.join(SALIDA, f"FB {k + 1:02d} · post {n:02d} · {p['tarjeta']['respuesta'].rstrip('.')} · v1 · {SELLO}.png".replace('/', '-').replace('$', ''))
            subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                            '--window-size=1080,1350', f'--screenshot={imagen}', 'file://' + f], check=True, capture_output=True)
        salida.append(dict(fb=k + 1, n=n, fecha=fecha.isoformat(), hora=HORA, tipo=p['tipo'], embudo=p['embudo'],
                           texto=texto_fb(p), fuente=p['fuente'],
                           imagen=os.path.relpath(imagen, AQUI) if imagen else None, estado='por programar'))
        print(k + 1, fecha, n, p['tipo'], 'tarjeta' if imagen else '')
    json.dump(salida, open(os.path.join(AQUI, 'fb_tanda2.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
