"""PDF con los 33 posts (texto, formato, visual y liga al artículo). HTML → Chrome sin cabeza."""
import json, os, html, subprocess, datetime, shutil, base64
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
TMP = os.environ.get('TMPDIR_PDF', os.path.join(AQUI, '_pdf_tmp'))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
NOMBRE = f'Posts X · 33 posts de RLR · v1 · {SELLO}.pdf'


def vista(nombre):
    """PNG embebido (base64) del visual; de un GIF, el último cuadro."""
    if not nombre:
        return ''
    ruta = os.path.join(AQUI, nombre)
    im = Image.open(ruta)
    if nombre.endswith('.gif'):
        im.seek(im.n_frames - 1)
    im = im.convert('RGB')
    im.thumbnail((1200, 1200))
    os.makedirs(TMP, exist_ok=True)
    out = os.path.join(TMP, f'{abs(hash(nombre))}.jpg')
    im.save(out, quality=82)
    return 'data:image/jpeg;base64,' + base64.b64encode(open(out, 'rb').read()).decode()


def main():
    posts = json.load(open(os.path.join(AQUI, 'posts.json')))
    etiqueta = {'texto': 'Solo texto', 'imagen': 'Imagen', 'gif': 'GIF animado'}
    partes = [f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>33 posts de X</title>
<style>
@page {{ size: A4; margin: 14mm 14mm 16mm 14mm; }}
body {{ font-family: 'Avenir Next', 'Helvetica Neue', Arial, sans-serif; color: #0D0D0D; margin: 0; }}
.portada {{ height: 250mm; display: flex; flex-direction: column; justify-content: flex-end; page-break-after: always; }}
.portada .barra {{ width: 28mm; height: 3mm; background: #FFC72C; margin-bottom: 8mm; }}
.portada h1 {{ font-size: 44pt; margin: 0 0 6mm; line-height: 1.05; }}
.portada p {{ font-size: 13pt; color: #555; margin: 2mm 0; }}
.indice {{ page-break-after: always; }}
.indice h2 {{ font-size: 20pt; margin: 0 0 6mm; }}
.indice table {{ width: 100%; border-collapse: collapse; font-size: 9.5pt; }}
.indice td, .indice th {{ padding: 1.6mm 2mm; border-bottom: 0.3pt solid #ddd; text-align: left; vertical-align: top; }}
.indice th {{ color: #888; font-weight: 600; }}
.post {{ page-break-after: always; }}
.post .cab {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 0.6pt solid #0D0D0D; padding-bottom: 2mm; margin-bottom: 4mm; }}
.post .num {{ font-size: 26pt; font-weight: 800; }}
.post .meta {{ font-size: 9.5pt; color: #666; text-align: right; }}
.post .meta b {{ color: #0D0D0D; }}
.etq {{ display: inline-block; font-size: 8.5pt; font-weight: 700; padding: 1mm 2.5mm; border-radius: 2mm; background: #0D0D0D; color: #FFC72C; margin-left: 2mm; }}
.etq.texto {{ background: #eee; color: #333; }}
.cuerpo {{ display: flex; gap: 6mm; }}
.texto {{ flex: 1; font-size: 11.5pt; line-height: 1.45; white-space: pre-wrap; }}
.visual {{ width: 88mm; flex: none; }}
.visual img {{ width: 88mm; border: 0.3pt solid #ccc; }}
.visual .pie {{ font-size: 8pt; color: #777; margin-top: 1.5mm; }}
.liga {{ margin-top: 5mm; font-size: 9.5pt; color: #444; }}
.liga a {{ color: #0D0D0D; }}
.sintexto {{ font-size: 8.5pt; color: #999; margin-top: 2mm; }}
.estado {{ font-size: 8.5pt; color: #999; margin-top: 8mm; }}
</style></head><body>
<div class="portada"><div class="barra"></div><h1>33 posts para X</h1>
<p>Ing. Ricardo López Reyero · @ricardolopezrey</p>
<p>9 ya hechos (en borradores de X, pausados) + 24 nuevos propuestos. Ninguno programado.</p>
<p>Cada post cierra con la liga a su artículo completo en X. {len([p for p in posts if p['formato']=='texto'])} solo texto · {len([p for p in posts if p['formato']=='imagen'])} con imagen · {len([p for p in posts if p['formato']=='gif'])} con GIF.</p>
<p>v1 · {SELLO}</p></div>
<div class="indice"><h2>Índice</h2><table><tr><th>#</th><th>Artículo de origen</th><th>Formato</th><th>Primera línea</th></tr>"""]
    for p in posts:
        partes.append(f"<tr><td>{p['orden']}</td><td>{html.escape(p['titulo'])}</td><td>{etiqueta[p['formato']]}</td><td>{html.escape(p['texto'].split(chr(10))[0][:90])}</td></tr>")
    partes.append('</table></div>')
    for p in posts:
        img = vista(p.get('visual'))
        vis = f'<div class="visual"><img src="{img}"><div class="pie">{html.escape(p["visual"])}{" · se muestra el último cuadro" if p["formato"]=="gif" else ""}</div></div>' if img else ''
        partes.append(f"""<div class="post"><div class="cab"><div><span class="num">Post {p['orden']}</span><span class="etq {p['formato']}">{etiqueta[p['formato']]}</span></div>
<div class="meta">Artículo {p['articulo']:02d} · <b>{html.escape(p['titulo'])}</b></div></div>
<div class="cuerpo"><div class="texto">{html.escape(p['texto'])}</div>{vis}</div>
<div class="liga">Cierra con: <b>Lo escribí completo aquí:</b> <a href="{p['liga']}">{p['liga']}</a> · {len(p['texto_x'])} caracteres con la liga</div>
<div class="estado">{html.escape(p['estado'])}</div></div>""")
    partes.append('</body></html>')
    os.makedirs(TMP, exist_ok=True)
    h = os.path.join(TMP, 'posts.html')
    open(h, 'w').write('\n'.join(partes))
    pdf = os.path.join(AQUI, NOMBRE)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={pdf}', 'file://' + h], check=True, capture_output=True)
    shutil.rmtree(TMP, ignore_errors=True)
    print(pdf)


if __name__ == '__main__':
    main()
