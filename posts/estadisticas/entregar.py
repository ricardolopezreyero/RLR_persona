"""Después de render.py: escribe el índice (indice.json), el documento de textos para YouTube (SHORTS_datos_textos.md)
y la hoja de contacto (hoja.jpg). Uso: python3 entregar.py"""
import os, json, glob, datetime
from PIL import Image
from serie import P, SERIES, armar_descripcion, HASH_BASE, HASH_SERIE

AQUI = os.path.dirname(os.path.abspath(__file__)); SALIDA = os.path.join(AQUI, 'salida')
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
idx = []
for p in P:
    png = sorted(glob.glob(os.path.join(SALIDA, f'Dato {p["n"]:02d} · *.png')))[-1]
    mp4s = sorted(glob.glob(os.path.join(SALIDA, f'Dato {p["n"]:02d} · *.mp4')))
    idx.append(dict(n=p['n'], serie=p['serie'], slug=p['slug'], titulo=p['titulo'], descripcion=armar_descripcion(p),
                    hashtags=f"{HASH_BASE} {HASH_SERIE} {p['hashtags']}", png=os.path.basename(png), mp4=os.path.basename(mp4s[-1]) if mp4s else None,
                    fuente=p['nota'], estado='hecho, sin publicar'))
json.dump(idx, open(os.path.join(AQUI, 'indice.json'), 'w'), ensure_ascii=False, indent=1)

md = [f'# Serie «Datos» · textos para YouTube Shorts · {SELLO}', '',
      f'{len(P)} piezas en tres series, a partir de los tres documentos de mercado de SuperLeads (julio 2026). Cada pieza: un gráfico vertical 1080×1920 (PNG) y su video de 8 s (MP4), '
      'más título, descripción y hashtags listos para Studio. Ninguna está publicada ni programada. Archivos en `salida/`.', '']
for k, s in SERIES.items():
    md += [f'## Serie {k} · {s["nombre"]}', '', f'Documento de origen: {s["doc"]}', '', '| # | Título | Archivo |', '|---|---|---|']
    md += [f'| {r["n"]:02d} | {r["titulo"]} | `{r["png"]}` |' for r in idx if r['serie'] == k]
    md.append('')
md += ['---', '']
for r in idx:
    md += [f'## {r["n"]:02d} · {r["titulo"]}', '', f'Archivo: `{r["png"]}`' + (f' · video: `{r["mp4"]}`' if r['mp4'] else ''), '',
           '**Título:**', '', r['titulo'], '', '**Descripción:**', '', '```', r['descripcion'], '```', '']
open(os.path.join(AQUI, 'SHORTS_datos_textos.md'), 'w').write('\n'.join(md))

tw, th, cols = 270, 480, 7
filas = (len(idx) + cols - 1) // cols
H = Image.new('RGB', (cols * (tw + 10) + 10, filas * (th + 10) + 10), (0, 18, 64))
for i, r in enumerate(idx):
    H.paste(Image.open(os.path.join(SALIDA, r['png'])).convert('RGB').resize((tw, th)), (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
H.save(os.path.join(AQUI, 'hoja.jpg'), quality=86)
print(len(idx), 'piezas;', sum(1 for r in idx if r['mp4']), 'con video')
# RLR
