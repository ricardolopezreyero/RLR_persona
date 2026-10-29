"""Junta todos los v/*/tramos.json en candidatos.json (lista plana con id, k, dur, tema, gancho, frase) y, si se le pasa
una selección (seleccion33.json = [[id, k], ...] en orden), renderiza cada uno a out33/NN.mp4 + portada, y arma la hoja
de revisión y la guía. Uso: python3 ensamblar.py candidatos | python3 ensamblar.py render [desde] [hasta]"""
import os, sys, json, glob, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hacer_short2

TIT = json.load(open('titulos_videos.json')) if os.path.exists('titulos_videos.json') else {}
CAT = {r['id']: (r['titulo_publicado'] or r['titulo_actual']) for r in json.load(open('/Users/ricardolopezreyero/SEO/youtube/descripciones.json'))}


def candidatos():
    out = []
    for f in sorted(glob.glob('v/*/tramos.json')):
        vid = os.path.basename(os.path.dirname(f))
        j = json.load(open(f))
        for k, t in enumerate(j.get('tramos', [])):
            out.append({'id': vid, 'k': k, 'dur': round(t['fin'] - t['ini'], 1), 'tema': t.get('tema'), 'gancho': ' / '.join(t['gancho']), 'frase': t['frase'], 'video': CAT.get(vid, vid)[:60]})
    json.dump(out, open('candidatos.json', 'w'), ensure_ascii=False, indent=1)
    for c in out:
        print(f"{c['id']} #{c['k']} {c['dur']:>5}s · {c['tema']:<22} · {c['gancho']} · {c['frase']}")
    print(len(out), 'candidatos de', len(set(c['id'] for c in out)), 'videos')


def render(desde=0, hasta=None):
    sel = json.load(open('seleccion33.json'))
    os.makedirs('out33', exist_ok=True)
    for n, (vid, k) in enumerate(sel, 1):
        if n < desde or (hasta and n > hasta):
            continue
        tr = json.load(open(f'v/{vid}/tramos.json'))['tramos'][k]
        salida = f'out33/{n:02d}.mp4'
        if os.path.exists(salida):
            continue
        cand = f'out33/cand_{vid}_{k}.mp4'
        if os.path.exists(cand) and os.path.exists(cand.replace('.mp4', '_portada.png')):
            import shutil
            shutil.copy(cand, salida); shutil.copy(cand.replace('.mp4', '_portada.png'), f'out33/{n:02d}_portada.png')
            print(n, vid, k, 'copiado del candidato'); continue
        d = hacer_short2.main(vid, tr, salida, f'out33/{n:02d}_portada.png')
        print(n, vid, k, f'{d:.1f}s')


def render_cands():
    """Renderiza todo candidato que no exista aún como out33/cand_<id>_<k>.mp4 (+ portada)."""
    os.makedirs('out33', exist_ok=True)
    for f in sorted(glob.glob('v/*/tramos.json')):
        vid = os.path.basename(os.path.dirname(f))
        for k, tr in enumerate(json.load(open(f)).get('tramos', [])):
            salida = f'out33/cand_{vid}_{k}.mp4'
            if os.path.exists(salida):
                continue
            try:
                d = hacer_short2.main(vid, tr, salida, salida.replace('.mp4', '_portada.png'))
                print('ok', vid, k, f'{d:.1f}s', flush=True)
            except Exception as e:
                print('ERROR', vid, k, e, flush=True)


def portadas():
    sel = json.load(open('seleccion33.json'))
    for n, (vid, k) in enumerate(sel, 1):
        tr = json.load(open(f'v/{vid}/tramos.json'))['tramos'][k]
        hacer_short2.main(vid, tr, f'out33/{n:02d}.mp4', f'out33/{n:02d}_portada.png', solo_portada=True)
        print(n, vid, k, flush=True)


if __name__ == '__main__':
    if sys.argv[1] == 'portadas':
        portadas()
    elif sys.argv[1] == 'cands':
        render_cands()
    elif sys.argv[1] == 'candidatos':
        candidatos()
    else:
        render(int(sys.argv[2]) if len(sys.argv) > 2 else 0, int(sys.argv[3]) if len(sys.argv) > 3 else None)