"""Tarjetas 1600×900 de la tanda 2, con el formato del post del IMSS (el que más funcionó:
7,215 vistas, 538 likes, 35 guardados): lo que la gente cree, tachado en rojo; lo que es, en amarillo.
Abajo, la regla de marca del 30-oct: nombre de Ricardo a la izquierda y logo de SuperLeads a la derecha.
HTML → PNG con Chrome sin cabeza."""
import json, os, html, subprocess, datetime, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
LOGO = open(os.path.join(AQUI, '..', 'estadisticas', 'logo_blanco.svg')).read()
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.join(AQUI, 'visuales')
ENTREGA = os.path.expanduser('~/Desktop/HTML/RLR_marca_personal/X tanda 2')

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1600px;height:900px;background:#0D0D0D;color:#F5F5F0;font-family:'Avenir Next','Avenir',sans-serif;
 padding:110px 110px 0 110px;position:relative;overflow:hidden}
.barra{width:80px;height:8px;background:#FFC72C;margin-bottom:26px}
.etq{color:#FFC72C;font-size:28px;font-weight:600;letter-spacing:.5px}
.arriba{font-size:var(--t);font-weight:800;line-height:1.1;margin-top:44px}
.tachado{font-size:var(--t);font-weight:800;line-height:1.15;color:#8A8A85;position:relative;display:inline-block;margin-top:8px}
.tachado:after{content:'';position:absolute;left:-12px;right:-12px;top:52%;height:12px;background:#E5242B;transform:rotate(-1deg)}
.resp{font-size:var(--t);font-weight:800;line-height:1.1;color:#FFC72C;margin-top:10px}
.pie{font-size:34px;color:#8A8A85;margin-top:30px;max-width:1380px;line-height:1.25}
.firma{position:absolute;left:110px;bottom:62px;font-size:31px;font-weight:600}
.logo{position:absolute;right:110px;bottom:58px;width:250px}
.logo svg{width:250px;height:auto}
"""


def tamano(t):
    """Tamaño de letra según la línea más larga (en caracteres) para que nada se salga."""
    largo = max(len(t['arriba']), len(t['tachado']), len(t['respuesta']))
    return 130 if largo <= 18 else 112 if largo <= 23 else 96 if largo <= 28 else 80


def html_tarjeta(t):
    tach = f'<div><span class="tachado">{html.escape(t["tachado"])}</span></div>' if t['tachado'] else ''
    return f"""<!doctype html><meta charset="utf-8"><style>{CSS}</style>
<body style="--t:{tamano(t)}px"><div class="barra"></div><div class="etq">{html.escape(t['etiqueta'])}</div>
<div class="arriba">{html.escape(t['arriba'])}</div>{tach}<div class="resp">{html.escape(t['respuesta'])}</div>
<div class="pie">{html.escape(t['pie'])}</div>
<div class="firma">Ing. Ricardo López Reyero · Torreón</div><div class="logo">{LOGO}</div></body>"""


def main():
    os.makedirs(SALIDA, exist_ok=True)
    os.makedirs(ENTREGA, exist_ok=True)
    posts = json.load(open(os.path.join(AQUI, 'posts_tanda2.json')))
    tmp = tempfile.mkdtemp()
    for p in posts:
        if p['tipo'] != 'tarjeta':
            continue
        t = p['tarjeta']
        f = os.path.join(tmp, f"{p['n']}.html")
        open(f, 'w').write(html_tarjeta(t))
        nombre = f"Post {p['n']:02d} · {t['respuesta'].rstrip('.')} · v1 · {SELLO}.png".replace('/', '-').replace('$', '')
        out = os.path.join(SALIDA, nombre)
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1600,900', f'--screenshot={out}', 'file://' + f], check=True, capture_output=True)
        subprocess.run(['cp', out, ENTREGA])
        p['visual'] = 'visuales/' + nombre
        print(nombre)
    json.dump(posts, open(os.path.join(AQUI, 'posts_tanda2.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
