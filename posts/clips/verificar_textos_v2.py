"""Cruza lo leído en Studio (JSON pegado desde el navegador) contra textos_shorts_v2.json y marca el estado.
Uso: python3 verificar_textos_v2.py lectura.json"""
import json, sys, os

AQUI = os.path.dirname(os.path.abspath(__file__))
textos = {r['id']: r for r in json.load(open(os.path.join(AQUI, 'textos_shorts_v2.json')))}
CAT = {r['id']: (r['titulo_publicado'] or r['titulo_actual']) for r in json.load(open('/Users/ricardolopezreyero/SEO/youtube/descripciones.json'))}
CAT['WFCeQA_GgQY'] = 'CRM para escuelas vs Excel: qué revisar antes de pagar'
lectura = json.load(open(sys.argv[1]))
mal = []
for l in lectura:
    t = textos[l['id']]
    okT = t['titulo'].startswith(l['t'][:40]); okD = t['descripcion'].startswith(l['d'][:30])
    okR = CAT[t['largo']].lower()[:25] == (l['rel'] or '').lower()[:25]
    if not (okT and okD and okR): mal.append((l['id'], okT, okD, okR, l))
    else: t['estado'] = 'aplicada y verificada en Studio 2026-10-29 (título, descripción, vídeo relacionado)'
json.dump(list(textos.values()), open(os.path.join(AQUI, 'textos_shorts_v2.json'), 'w'), ensure_ascii=False, indent=1)
print(len(lectura) - len(mal), 'verificados;', len(mal), 'con diferencias'); [print(m) for m in mal]
