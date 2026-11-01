"""Plan de Reels para la página de Facebook (arranque 1-nov-2026, primera pieza ese mismo día).

Dos carriles, una pieza diaria cada uno, sin mezclar series:
  · 12:30  los 26 Shorts ya probados en YouTube (el del 34 % sale primero: es el que más vistas tiene).
  · 19:30  serie «Rayos X» completa (19) y después «La realidad de la educación» (26), en orden.
El texto sale de las descripciones de YouTube, recortado para Facebook: gancho, cuerpo, pregunta,
invitación a seguir la página y hashtags. Sin ligas (en un Reel no se pueden pulsar) ni bloque de venta:
el único objetivo de la página es ganar seguidores.
Escribe facebook/reels_plan.json y facebook/REELS_plan.md."""
import json, os, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
POSTS = os.path.join(AQUI, '..', 'posts')
SHORTS1 = os.path.expanduser('~/Desktop/HTML/RLR_marca_personal/Shorts')
SEGUIR = 'Sígueme: cada día publico datos y casos reales de la educación privada en México.'
FUERA = ('Video completo', 'Sigue con', 'Para profundizar', 'Rayos X de Inscripciones:', 'Soy el Ing.', 'Serie «', 'http')


def texto_fb(titulo, descripcion, serie=None):
    pars = [p.strip() for p in descripcion.split('\n\n') if p.strip()]
    tags = next((p for p in reversed(pars) if p.startswith('#')), '')
    cuerpo = []
    for p in pars[1:]:
        if p.startswith('#') or p.startswith(FUERA):
            continue
        if p.startswith('Fuente') and len(p) > 220:
            p = p[:p.find('.', 120) + 1] if p.find('.', 120) > 0 else p[:220]
        cuerpo.append(p)
    bloques = [titulo.replace('#Shorts', '').strip(), *cuerpo]
    if serie:
        bloques.append(serie)
    bloques += [SEGUIR, tags]
    return '\n\n'.join(b for b in bloques if b)


def carril_shorts():
    textos = {t['fecha']: t for t in json.load(open(os.path.join(POSTS, 'clips', 'textos_shorts_v2.json')))}
    t2 = json.load(open(os.path.join(POSTS, 'clips', 'programacion_tanda2.json')))
    primeros = sorted(f for f in os.listdir(SHORTS1) if f.startswith('Short ') and f.endswith('.mp4'))
    largos = [x['id'] for x in json.load(open(os.path.join(POSTS, 'clips', 'publicados_youtube_2026-10-28.json')))]
    piezas = []
    for archivo, fecha, largo in zip(primeros, ['2026-10-29', '2026-10-30', '2026-10-31', '2026-11-02', '2026-11-03'], largos):
        t = textos[fecha]
        piezas.append({'archivo': os.path.join(SHORTS1, archivo), 'portada': os.path.join(SHORTS1, 'portadas', largo + '.png'), 'titulo': t['titulo'], 'youtube': t['id'], 'texto': texto_fb(t['titulo'], t['descripcion'])})
    for x in t2:
        t = textos[x['fecha']]
        piezas.append({'archivo': x['archivo'], 'portada': x['portada'], 'titulo': t['titulo'], 'youtube': t['id'], 'texto': texto_fb(t['titulo'], t['descripcion'])})
    piezas.insert(0, piezas.pop(1))  # el 34 % primero
    return piezas


def carril_series():
    cal = json.load(open(os.path.join(POSTS, 'calendario', 'Calendario series · v2 · 2026-10-29 21h40.json')))
    piezas = []
    for c in cal:
        serie_linea = next((p.split('. ')[0] + '.' for p in c['descripcion'].split('\n\n') if p.startswith('Serie «')), '')
        piezas.append({'archivo': c['mp4'], 'portada': c['png'], 'titulo': c['titulo'], 'serie': c['serie'], 'texto': texto_fb(c['titulo'], c['descripcion'], serie_linea)})
    return piezas


def main():
    hoy = datetime.date(2026, 11, 1)
    plan = []
    for k, p in enumerate(carril_shorts()):
        plan.append({**p, 'carril': 'Shorts', 'fecha': str(hoy + datetime.timedelta(days=k)), 'hora': '12:30'})
    for k, p in enumerate(carril_series()):
        plan.append({**p, 'carril': 'Series', 'fecha': str(hoy + datetime.timedelta(days=k)), 'hora': '19:30'})
    plan.sort(key=lambda x: (x['fecha'], x['hora']))
    for p in plan:
        assert os.path.exists(p['archivo']), p['archivo']
        assert os.path.exists(p['portada']), p['portada']
        p['titulo_fb'] = p['titulo'].replace('#Shorts', '').strip()
        p['estado'] = 'pendiente'
    json.dump(plan, open(os.path.join(AQUI, 'reels_plan.json'), 'w'), ensure_ascii=False, indent=1)
    with open(os.path.join(AQUI, 'REELS_plan.md'), 'w') as f:
        f.write('# Reels de Facebook · calendario\n\nGenerado por `plan_reels.py`. Hora de Torreón (GMT-6).\n\n| Fecha | Hora | Carril | Reel |\n|---|---|---|---|\n')
        for p in plan:
            f.write(f"| {p['fecha']} | {p['hora']} | {p['carril']} | {p['titulo'].replace('#Shorts', '').strip()} |\n")
    print(len(plan), plan[0]['fecha'], plan[-1]['fecha'])
    print(plan[0]['texto'])
    print('---')
    print([p for p in plan if p['carril'] == 'Series'][0]['texto'])


if __name__ == '__main__':
    main()
