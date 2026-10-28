"""Guarda un corte de métricas de X (JSON por stdin o archivo) y regenera el CSV y el resumen.
Uso: python3 guardar.py corte.json   |   cat corte.json | python3 guardar.py
Cada corte: {fecha, seguidores, siguiendo, posts:[{id, fecha, texto, articulo, vistas, likes, reposts, respuestas, guardados}]}"""
import json, os, sys, csv, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
JSONL = os.path.join(AQUI, 'cortes.jsonl')
CSV = os.path.join(AQUI, 'metricas.csv')
RESUMEN = os.path.join(AQUI, 'README.md')
POSTS = os.path.join(os.path.dirname(AQUI), 'posts', 'posts.json')


def num(s):
    if isinstance(s, (int, float)):
        return int(s)
    s = (s or '').strip().split(' ')[0].replace(',', '')
    mult = 1
    if s.endswith('K'):
        mult, s = 1000, s[:-1]
    if s.endswith('M'):
        mult, s = 1000000, s[:-1]
    try:
        return int(float(s) * mult)
    except ValueError:
        return 0


def main():
    fuente = open(sys.argv[1]) if len(sys.argv) > 1 else sys.stdin
    corte = json.load(fuente)
    corte['fecha_local'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    corte['seguidores_n'] = num(corte.get('seguidores'))
    # los artículos salen sin texto en el perfil: se les pone su título por id
    pub = os.path.join(os.path.dirname(AQUI), 'posts', 'publicados_x.json')
    arts = os.path.join(os.path.dirname(AQUI), 'articulos', 'README.md')
    if os.path.exists(pub) and os.path.exists(arts):
        titulos = {}
        for l in open(arts):
            if l.startswith('| ') and '](' in l:
                n, t = l.split('|')[1].strip(), l.split('[')[1].split(']')[0]
                titulos[n] = t
        por_id = {v: titulos.get(k.zfill(2), '') for k, v in json.load(open(pub)).items()}
        for p in corte['posts']:
            if not p.get('texto') and p['id'] in por_id:
                p['texto'] = 'Artículo: ' + por_id[p['id']]
                p['articulo'] = True
    with open(JSONL, 'a') as f:
        f.write(json.dumps(corte, ensure_ascii=False) + '\n')
    cortes = [json.loads(l) for l in open(JSONL) if l.strip()]
    # CSV largo: una fila por post por corte
    with open(CSV, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['corte', 'seguidores', 'post_id', 'fecha_post', 'es_articulo', 'vistas', 'likes', 'reposts', 'respuestas', 'guardados', 'texto'])
        for c in cortes:
            for p in c['posts']:
                w.writerow([c['fecha_local'], c['seguidores_n'], p['id'], (p.get('fecha') or '')[:16], int(bool(p.get('articulo'))), p['vistas'], p['likes'], p['reposts'], p['respuestas'], p['guardados'], p['texto']])
    # resumen: último corte, posts programados (no artículos) ordenados por vistas, y delta vs corte anterior
    ult, ant = cortes[-1], (cortes[-2] if len(cortes) > 1 else None)
    prev = {p['id']: p for p in ant['posts']} if ant else {}
    plan = {}
    if os.path.exists(POSTS):
        for x in json.load(open(POSTS)):
            plan[x['texto'].split('\n')[0][:40]] = x
    filas = []
    for p in ult['posts']:
        if p.get('articulo'):
            continue
        q = prev.get(p['id'], {})
        d = lambda k: f"{p[k]} (+{p[k]-q[k]})" if q else str(p[k])
        slot = next((f"#{x['orden']} slot {x['slot']}" for k, x in plan.items() if p['texto'].startswith(k[:30])), '')
        filas.append((p['vistas'], f"| {(p.get('fecha') or '')[:10]} | {slot} | {p['texto'][:50]} | {d('vistas')} | {d('likes')} | {d('reposts')} | {d('respuestas')} | {d('guardados')} |"))
    filas.sort(reverse=True)
    arts = [p for p in ult['posts'] if p.get('articulo')]
    lines = ['# Métricas de X · @ricardolopezrey', '', f"Último corte: {ult['fecha_local']} (hora de la Mac). Seguidores: **{ult.get('seguidores')}** (siguiendo {ult.get('siguiendo')}). Cortes guardados: {len(cortes)}. Datos crudos en [cortes.jsonl](cortes.jsonl) y [metricas.csv](metricas.csv).", '',
             '## Posts (no artículos), por vistas · entre paréntesis el cambio desde el corte anterior', '', '| Publicado | Post | Texto | Vistas | Likes | Reposts | Respuestas | Guardados |', '|---|---|---|---|---|---|---|---|']
    lines += [f for _, f in filas]
    if arts:
        lines += ['', f"## Artículos ({len(arts)} vistos en el perfil)", '', f"Vistas sumadas: {sum(a['vistas'] for a in arts)} · likes: {sum(a['likes'] for a in arts)} · guardados: {sum(a['guardados'] for a in arts)} · respuestas: {sum(a['respuestas'] for a in arts)}"]
    lines += ['', '## Seguidores por corte', '', '| Corte | Seguidores |', '|---|---|'] + [f"| {c['fecha_local']} | {c.get('seguidores')} |" for c in cortes[-30:]]
    open(RESUMEN, 'w').write('\n'.join(lines) + '\n')
    print(f"corte {len(cortes)} guardado: {len(ult['posts'])} posts, seguidores {ult.get('seguidores')}")


if __name__ == '__main__':
    main()
