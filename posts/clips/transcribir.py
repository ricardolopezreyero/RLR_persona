"""whisper-cli local → palabras.json [[t, palabra], ...] y transcripcion.txt (una línea cada ~12 s). Uso: python3 transcribir.py <id> [...]"""
import json, os, subprocess, sys
M = os.path.expanduser('~/Library/Application Support/Screen Studio/models/ggml-medium.bin')
def ts(s):
    h, m, r = s.replace(',', '.').split(':'); return int(h) * 3600 + int(m) * 60 + float(r)
for vid in sys.argv[1:]:
    d = f'v/{vid}'
    if os.path.exists(f'{d}/palabras.json') and os.path.getsize(f'{d}/palabras.json') > 100: print(vid, 'ya'); continue
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{d}/video.mp4', '-ar', '16000', '-ac', '1', f'{d}/audio.wav'], check=True)
    subprocess.run(['whisper-cli', '-m', M, '-l', 'es', '-f', f'{d}/audio.wav', '-ml', '1', '-oj', '-of', f'{d}/whisper', '-np'], check=True, capture_output=True)
    segs = json.load(open(f'{d}/whisper.json'))['transcription']
    words = []
    for s in segs:
        tok = s['text']
        if not tok.strip(): continue
        t0 = ts(s['timestamps']['from'])
        if tok.startswith(' ') or not words or words[-1][1][-1] in '.,;:?!':
            words.append([round(t0, 2), tok.strip()])
        else:
            words[-1][1] += tok.strip()
    # pegar signos sueltos a la palabra anterior
    out = []
    for t, w in words:
        if out and w in ('.', ',', '?', '!', ';', ':', '%'): out[-1][1] += w
        else: out.append([t, w])
    json.dump(out, open(f'{d}/palabras.json', 'w'), ensure_ascii=False)
    lineas, cur, t0 = [], [], None
    for t, w in out:
        if t0 is None: t0 = t
        cur.append(w)
        if t - t0 >= 12: lineas.append(f'{int(t0//60):02d}:{int(t0%60):02d} ' + ' '.join(cur)); cur, t0 = [], None
    if cur: lineas.append(f'{int(t0//60):02d}:{int(t0%60):02d} ' + ' '.join(cur))
    open(f'{d}/transcripcion.txt', 'w').write('\n'.join(lineas))
    os.remove(f'{d}/audio.wav')
    print(vid, len(out), 'palabras')
