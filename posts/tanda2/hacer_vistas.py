"""Vista previa de cada post de la tanda 2 como se ve en X (modo oscuro, ancho de timeline de 600 px):
avatar, nombre con palomita, @, texto completo, imagen y fecha de salida. Una PNG por post en Descargas."""
import json, os, html, subprocess, datetime, tempfile, base64

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.expanduser(f'~/Downloads/X tanda 2 · vista previa · {SELLO}')
AVATAR = os.path.join(AQUI, '..', '..', 'persona', 'avatar', 'x-1.png')
DIAS = ['lun', 'mar', 'mié', 'jue', 'vie', 'sáb', 'dom']
MESES = ['ene', 'feb', 'mar', 'abr', 'may', 'jun', 'jul', 'ago', 'sep', 'oct', 'nov', 'dic']
PALOMITA = ('<svg viewBox="0 0 22 22" width="19" height="19" style="vertical-align:-3px;margin-left:3px"><path fill="#1D9BF0" d="M20.4 11c0-1.3-.8-2.5-2-3 .4-1.3.1-2.7-.8-3.6-.9-.9-2.3-1.2-3.6-.8-.5-1.2-1.7-2-3-2s-2.5.8-3 2c-1.3-.4-2.7-.1-3.6.8-.9.9-1.2 2.3-.8 3.6-1.2.5-2 1.7-2 3s.8 2.5 2 3c-.4 1.3-.1 2.7.8 3.6.9.9 2.3 1.2 3.6.8.5 1.2 1.7 2 3 2s2.5-.8 3-2c1.3.4 2.7.1 3.6-.8.9-.9 1.2-2.3.8-3.6 1.2-.5 2-1.7 2-3zm-10.8 4.4L5.9 11.7l1.3-1.3 2.4 2.4 5.2-5.2 1.3 1.3-6.5 6.5z"/></svg>')

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{background:#000;width:600px;font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;color:#E7E9EA}
.post{display:flex;gap:12px;padding:14px 16px 12px;border-bottom:1px solid #2F3336}
.av{width:40px;height:40px;border-radius:50%;flex:none}
.cab{font-size:15px;line-height:20px;white-space:nowrap}.cab b{font-weight:700}.gris{color:#71767B}
.txt{font-size:15px;line-height:20px;white-space:pre-wrap;margin-top:2px;word-wrap:break-word}
.txt a{color:#1D9BF0;text-decoration:none}
.img{margin-top:12px;width:100%;border-radius:16px;border:1px solid #2F3336;display:block}
.acc{display:flex;justify-content:space-between;margin-top:12px;color:#71767B;font-size:13px;max-width:425px}
.sale{background:#16181C;color:#FFC72C;font-size:13px;padding:8px 16px;border-bottom:1px solid #2F3336}"""


def b64(ruta):
    ext = 'png' if ruta.endswith('.png') else 'jpeg'
    return f'data:image/{ext};base64,' + base64.b64encode(open(ruta, 'rb').read()).decode()


def ligas(t):
    t = html.escape(t)
    import re
    return re.sub(r'(https?://\S+)', lambda m: f'<a>{m.group(1).replace("https://", "")}</a>', t)


def main():
    os.makedirs(SALIDA, exist_ok=True)
    posts = json.load(open(os.path.join(AQUI, 'posts_tanda2.json')))
    av = b64(AVATAR)
    tmp = tempfile.mkdtemp()
    for k, p in enumerate(posts, 1):
        d = datetime.date.fromisoformat(p['fecha'])
        cuando = f"{DIAS[d.weekday()]} {d.day} {MESES[d.month - 1]} · {p['hora']}"
        img = f'<img class="img" src="{b64(os.path.join(AQUI, p["visual"]))}">' if p.get('visual') else ''
        h = f"""<!doctype html><meta charset="utf-8"><style>{CSS}</style><body>
<div class="sale">Sale el {cuando} (Torreón)</div>
<div class="post"><img class="av" src="{av}"><div style="flex:1;min-width:0">
<div class="cab"><b>Ing. Ricardo López Reyero</b>{PALOMITA} <span class="gris">@ricardolopezrey · {d.day} {MESES[d.month - 1]}</span></div>
<div class="txt">{ligas(p['texto'])}</div>{img}
<div class="acc"><span>💬</span><span>🔁</span><span>♡</span><span>📊</span><span>🔖</span></div></div></div></body>"""
        f = os.path.join(tmp, f'{k}.html')
        open(f, 'w').write(h)
        titulo = p['texto'].split('\n')[0].rstrip('.:')[:60].replace('/', '-').replace(':', '').replace('$', '').replace('?', '').replace('¿', '')
        nombre = f"{k:02d} · {p['fecha'][5:]} {p['hora'].replace(':', 'h')} · {titulo} · v1 · {SELLO}.png"
        out = os.path.join(SALIDA, nombre)
        alto = 1400 if img else 900
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=2',
                        f'--window-size=600,{alto}', f'--screenshot={out}', 'file://' + f], check=True, capture_output=True)
        recortar(out)
        print(nombre)
    print(SALIDA)


def recortar(ruta):
    """Quita el negro sobrante de abajo (Chrome toma la ventana completa)."""
    from PIL import Image
    im = Image.open(ruta).convert('RGB')
    w, h = im.size
    px = im.load()
    y = h - 1
    while y > 0 and all(px[x, y] == (0, 0, 0) for x in range(0, w, 7)):
        y -= 1
    im.crop((0, 0, w, min(h, y + 2))).save(ruta)


if __name__ == '__main__':
    main()
