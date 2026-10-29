"""Tanda 2 de los Shorts tras la revisión de Ricardo (etiquetas de Finder sobre la tanda 1):
rojas = se descartan; amarilla = audio normalizado; azules = edición corregida. Los verdes se copian intactos
(mismo archivo y nombre v1); los corregidos salen como v2. Escribe la guía con la tabla de descartados.
Uso: python3 entregar_tanda2.py"""
import os, json, shutil, datetime, subprocess, re
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
REV = json.load(open(os.path.join(AQUI, 'revision_tanda1.json')))
ROJAS, V2 = set(REV['rojas']), {int(k): v for k, v in REV['v2'].items()}
ORIGEN = os.path.expanduser('~/Desktop/HTML/RLR_marca_personal/Shorts 33')
DEST = os.path.expanduser('~/Desktop/HTML/RLR_marca_personal/Shorts 33 · tanda 2')
DESC = os.path.expanduser('~/Downloads/Shorts 33 · tanda 2')
for d in (DEST, DESC, os.path.join(DEST, 'portadas'), os.path.join(DESC, 'portadas')): os.makedirs(d, exist_ok=True)
CAT = {r['id']: (r['titulo_publicado'] or r['titulo_actual']) for r in json.load(open('/Users/ricardolopezreyero/SEO/youtube/descripciones.json'))}
sel = json.load(open(os.path.join(AQUI, 'seleccion33.json')))
previos = {int(f[6:8]): f for f in os.listdir(ORIGEN) if f.startswith('Short ') and f.endswith('.mp4')}
previas_por = {int(f[8:10]): f for f in os.listdir(os.path.join(ORIGEN, 'portadas')) if f.startswith('Portada ')}
md = [f'# Shorts de YouTube · tanda 2 · {SELLO}', '',
      f'Revisión de Ricardo sobre la tanda 1 (v1 · 2026-10-29 00h07): {len(ROJAS)} rojos descartados, 1 amarillo con audio corregido, '
      f'3 azules con la edición corregida, {33 - len(ROJAS) - len(V2)} verdes sin tocar.',
      'Los verdes conservan su archivo y nombre v1 (son bit a bit los mismos). Los corregidos van como v2.',
      'Nada subido ni programado: esperan tu OK. Archivos en Desktop/HTML/RLR_marca_personal/Shorts 33 · tanda 2 y en Descargas.', '',
      '## Qué cambió en los v2', '']
for n, v in sorted(V2.items()): md.append(f'- **Short {n:02d}**: {v}')
md += ['', '## Descartados (rojos), no se publican', '', '| # | Título | Video de origen |', '|---|---|---|']
for n, (vid, k) in enumerate(sel, 1):
    if n in ROJAS:
        tr = json.load(open(os.path.join(AQUI, 'v', vid, 'tramos.json')))['tramos'][k]
        md.append(f'| {n} | {tr["frase"]} | {CAT.get(vid, vid)[:50]} |')
md += ['', f'## Los {33 - len(ROJAS)} que siguen', '', '| # | Versión | Título sugerido | Seg | Tema | Video de origen |', '|---|---|---|---|---|---|']
fichas, hoja = [], []
for n, (vid, k) in enumerate(sel, 1):
    if n in ROJAS: continue
    tr = json.load(open(os.path.join(AQUI, 'v', vid, 'tramos.json')))['tramos'][k]
    corto = re.sub(r'[^\w áéíóúñÁÉÍÓÚÑ%.,¿?]', '', tr['frase'])[:48].strip()
    if n in V2:
        src = os.path.join(AQUI, 'out33', f'{n:02d}.mp4'); por = os.path.join(AQUI, 'out33', f'{n:02d}_portada.png')
        nombre = f'Short {n:02d} · {corto} · v2 · {SELLO}.mp4'; npor = f'Portada {n:02d} · {corto} · v2 · {SELLO}.png'; ver = 'v2'
    else:
        nombre = previos[n]; npor = previas_por[n]; ver = 'v1'
        src = os.path.join(ORIGEN, nombre); por = os.path.join(ORIGEN, 'portadas', npor)
    for d in (DEST, DESC):
        shutil.copy(src, os.path.join(d, nombre)); shutil.copy(por, os.path.join(d, 'portadas', npor))
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    m, s = divmod(int(tr['ini']), 60); m2, s2 = divmod(int(tr['fin']), 60)
    md.append(f'| {n} | {ver} | {tr["frase"]} | {dur:.0f} | {tr.get("tema", "")} | {CAT.get(vid, vid)[:50]} ({m}:{s:02d}) |')
    fichas += [f'## {n}. {tr["frase"]}', '',
               f'Archivo: `{nombre}` · portada: `portadas/{npor}` · {dur:.0f} s · del video «{CAT.get(vid, vid)}» (https://www.youtube.com/watch?v={vid}), minuto {m}:{s:02d}–{m2}:{s2:02d}', '',
               f'**Gancho en pantalla:** {" / ".join(tr["gancho"])}', '', f'**Título del Short:** {tr["frase"]} #Shorts', '', '**Descripción:**', '', tr['descripcion'], '',
               f'**Por qué este tramo:** {tr.get("por_que", "")}', '', '**Subtítulos (texto completo):** ' + ' '.join(t['texto'] for t in tr['trozos']), '']
    hoja.append((n, por))
md += [''] + fichas
for d in (DEST, DESC):
    open(os.path.join(d, f'Shorts 33 · guía de publicación · tanda 2 · {SELLO}.md'), 'w').write('\n'.join(md))
cols, tw, th = 7, 270, 480
filas = (len(hoja) + cols - 1) // cols
H = Image.new('RGB', (cols * (tw + 10) + 10, filas * (th + 10) + 10), (0, 18, 64))
for i, (n, p) in enumerate(hoja):
    H.paste(Image.open(p).convert('RGB').resize((tw, th)), (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
for d in (DEST, DESC):
    H.save(os.path.join(d, f'Shorts 33 · hoja de portadas · tanda 2 · {SELLO}.jpg'), quality=88)
print(DEST, len(hoja), 'shorts;', len(ROJAS), 'descartados')
