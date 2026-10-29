"""Entrega de los 33 Shorts: copia out33/NN.mp4 + NN_portada.png con nombre (número + frase + versión + fecha) a
Desktop/HTML/RLR_marca_personal/Shorts 33/ y a ~/Downloads/Shorts 33/, arma la hoja de revisión y escribe la guía
(título, descripción, hashtags, gancho, video y minuto de origen, subtítulos). Uso: python3 entregar33.py v1"""
import os, sys, json, shutil, datetime, subprocess, re
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
V = sys.argv[1] if len(sys.argv) > 1 else 'v1'
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
DEST = os.path.expanduser('~/Desktop/HTML/RLR_marca_personal/Shorts 33')
DESC = os.path.expanduser('~/Downloads/Shorts 33')
for d in (DEST, DESC, os.path.join(DEST, 'portadas'), os.path.join(DESC, 'portadas')): os.makedirs(d, exist_ok=True)
CAT = {r['id']: (r['titulo_publicado'] or r['titulo_actual']) for r in json.load(open('/Users/ricardolopezreyero/SEO/youtube/descripciones.json'))}
sel = json.load(open(os.path.join(AQUI, 'seleccion33.json')))
md = [f'# Shorts de YouTube · 33 clips premium · {V} · {SELLO}', '',
      'Vertical 1080×1920, 30 fps, H.264 + AAC, portada vertical por Short. Diseño SuperLeads (navy profundo, verde, Plus Jakarta Sans).',
      'Nada subido ni programado: esperan tu OK. Los archivos van en Desktop/HTML/RLR_marca_personal/Shorts 33 y en Descargas/Shorts 33.', '',
      '| # | Título sugerido | Seg | Tema | Video de origen |', '|---|---|---|---|---|']
fichas = []
hoja = []
for n, (vid, k) in enumerate(sel, 1):
    tr = json.load(open(os.path.join(AQUI, 'v', vid, 'tramos.json')))['tramos'][k]
    src = os.path.join(AQUI, 'out33', f'{n:02d}.mp4'); por = os.path.join(AQUI, 'out33', f'{n:02d}_portada.png')
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    corto = re.sub(r'[^\w áéíóúñÁÉÍÓÚÑ%.,¿?]', '', tr['frase'])[:48].strip()
    nombre = f'Short {n:02d} · {corto} · {V} · {SELLO}.mp4'
    npor = f'Portada {n:02d} · {corto} · {V} · {SELLO}.png'
    for d in (DEST, DESC):
        shutil.copy(src, os.path.join(d, nombre)); shutil.copy(por, os.path.join(d, 'portadas', npor))
    m, s = divmod(int(tr['ini']), 60); m2, s2 = divmod(int(tr['fin']), 60)
    md.append(f'| {n} | {tr["frase"]} | {dur:.0f} | {tr.get("tema", "")} | {CAT.get(vid, vid)[:50]} ({m}:{s:02d}) |')
    fichas += [f'## {n}. {tr["frase"]}', '',
               f'Archivo: `{nombre}` · portada: `portadas/{npor}` · {dur:.0f} s · del video «{CAT.get(vid, vid)}» (https://www.youtube.com/watch?v={vid}), minuto {m}:{s:02d}–{m2}:{s2:02d}', '',
               f'**Gancho en pantalla:** {" / ".join(tr["gancho"])}', '', f'**Título del Short:** {tr["frase"]} #Shorts', '', '**Descripción:**', '', tr['descripcion'], '',
               f'**Por qué este tramo:** {tr.get("por_que", "")}', '', '**Subtítulos (texto completo):** ' + ' '.join(t['texto'] for t in tr['trozos']), '']
    hoja.append(por)
md += [''] + fichas
for d in (DEST, DESC):
    open(os.path.join(d, f'Shorts 33 · guía de publicación · {V} · {SELLO}.md'), 'w').write('\n'.join(md))
# hoja de portadas (7 columnas)
cols, tw, th = 7, 270, 480
filas = (len(hoja) + cols - 1) // cols
H = Image.new('RGB', (cols * (tw + 10) + 10, filas * (th + 10) + 10), (0, 18, 64))
for i, p in enumerate(hoja):
    H.paste(Image.open(p).convert('RGB').resize((tw, th)), (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
for d in (DEST, DESC):
    H.save(os.path.join(d, f'Shorts 33 · hoja de portadas · {V} · {SELLO}.jpg'), quality=88)
print(DEST, len(sel))
