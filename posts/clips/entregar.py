"""Copia los Shorts con nombre (título + versión + fecha) a Desktop/HTML/RLR_marca_personal/Shorts y ~/Downloads,
y escribe SHORTS.md con título, descripción, hashtags y tramo de cada uno. Uso: python3 entregar.py <vN>"""
import os, sys, json, shutil, datetime, subprocess, re

AQUI = os.path.dirname(os.path.abspath(__file__))
V = sys.argv[1]
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
DEST = os.path.expanduser('~/Desktop/HTML/RLR_marca_personal/Shorts')
DESC = os.path.expanduser('~/Downloads')
os.makedirs(DEST, exist_ok=True)
TITULOS = json.load(open(os.path.join(AQUI, 'titulos_videos.json')))
ORDEN = ['ZP5BSoRFaio', '0tRgTomkaAw', 'oqLweG2S0Bk', 'mDfb_nteAe8', 'aZggkBKgqrg']
md = ['# Shorts de YouTube · 5 clips · ' + SELLO, '', 'Vertical 1080×1920, 30 fps, H.264 + AAC. Diseño SuperLeads (navy profundo, verde, Plus Jakarta Sans). Nada subido: Ricardo los sube desde Studio.', '']
for k, vid in enumerate(ORDEN, 1):
    src = os.path.join(AQUI, 'out', f'{vid}.mp4')
    if not os.path.exists(src):
        md.append(f'## {k}. (pendiente) {vid}'); continue
    sel = json.load(open(os.path.join(AQUI, 'v', vid, 'seleccion.json')))
    dur = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', src], capture_output=True, text=True).stdout)
    corto = re.sub(r'[^\w áéíóúñÁÉÍÓÚÑ%.,¿?]', '', sel['frase'])[:48].strip()
    nombre = f'Short {k} · {corto} · {V} · {SELLO}.mp4'
    shutil.copy(src, os.path.join(DEST, nombre)); shutil.copy(src, os.path.join(DESC, nombre))
    m, s = divmod(int(sel['ini']), 60); m2, s2 = divmod(int(sel['fin']), 60)
    md += [f'## {k}. {sel["frase"]}', '', f'Archivo: `{nombre}` · {dur:.0f} s · del video «{TITULOS[vid]}» (https://www.youtube.com/watch?v={vid}), minuto {m}:{s:02d}–{m2}:{s2:02d}', '',
           f'**Gancho en pantalla:** {" / ".join(sel["gancho"])}', '', f'**Título sugerido del Short:** {sel["frase"]} #Shorts', '', '**Descripción:**', '', sel['descripcion'], '',
           f'**Por qué este tramo:** {sel["por_que"]}', '', '**Subtítulos (texto completo):** ' + ' '.join(t['texto'] for t in sel['trozos']), '']
open(os.path.join(DEST, f'Shorts · guía de publicación · {V} · {SELLO}.md'), 'w').write('\n'.join(md))
print(DEST)
