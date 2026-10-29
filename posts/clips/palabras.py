"""Saca palabras con tiempo del VTT automático de YouTube → palabras.json [[t, palabra], ...] y transcripcion.txt por minuto."""
import re, json, sys
d = sys.argv[1]
t = open(f'{d}/video.es.vtt', encoding='utf-8').read()
def seg(s):
    h, m, r = s.split(':'); return int(h) * 3600 + int(m) * 60 + float(r)
words = []
for blk in re.split(r'\n\n+', t):
    lines = blk.strip().split('\n')
    if len(lines) < 2 or '-->' not in lines[0]: continue
    ini = seg(lines[0].split(' --> ')[0].strip())
    body = ' '.join(lines[1:])
    if '<c>' not in body: continue
    parts = re.split(r'<(\d\d:\d\d:\d\d\.\d+)>', body)
    toks = [(ini, re.sub(r'<[^>]+>', '', parts[0]).strip())]
    for i in range(1, len(parts), 2):
        toks.append((seg(parts[i]), re.sub(r'<[^>]+>', '', parts[i + 1]).strip()))
    for ts, w in toks:
        w = w.split()[-1] if w else ''
        if w and (not words or words[-1] != (ts, w)): words.append((round(ts, 2), w))
json.dump(words, open(f'{d}/palabras.json', 'w'), ensure_ascii=False)
# transcripción legible: una línea cada ~12 s
lineas, cur, t0 = [], [], None
for ts, w in words:
    if t0 is None: t0 = ts
    cur.append(w)
    if ts - t0 >= 12:
        lineas.append(f'{int(t0//60):02d}:{int(t0%60):02d} ' + ' '.join(cur)); cur, t0 = [], None
if cur: lineas.append(f'{int(t0//60):02d}:{int(t0%60):02d} ' + ' '.join(cur))
open(f'{d}/transcripcion.txt', 'w').write('\n'.join(lineas))
print(d, len(words), 'palabras')
