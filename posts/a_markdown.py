"""Pasa los artículos (content_state de X, ya convertidos del blog) a Markdown para el repo RLR_persona.
Un archivo por artículo en RLR_persona/articulos/, imágenes en RLR_persona/articulos/imagenes/."""
import json, os, re, shutil, unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.expanduser('~/Code/RLR_persona')
DEST = os.path.join(REPO, 'articulos')
IMG = os.path.join(DEST, 'imagenes')
# No van al repo público: ensayo ajeno (Paul Graham), documentos internos de SuperLeads y la foto familiar.
EXCLUIR = {51, 59, 60, 62, 92, 95}


def slug(t):
    s = unicodedata.normalize('NFKD', t).encode('ascii', 'ignore').decode()
    s = re.sub(r'[^a-zA-Z0-9]+', '-', s).strip('-').lower()
    return s[:70]


def estilo(texto, rangos):
    """Aplica negritas/cursivas por offsets (en caracteres)."""
    if not rangos:
        return texto
    marcas = {}
    for r in rangos:
        a, z = r['offset'], r['offset'] + r['length']
        m = {'BOLD': '**', 'Bold': '**', 'ITALIC': '_', 'Italic': '_'}.get(r['style'])
        if not m or z <= a:
            continue
        marcas.setdefault(a, []).append(m)
        marcas.setdefault(z, []).insert(0, m)
    out = ''
    for i, ch in enumerate(texto):
        out += ''.join(marcas.get(i, [])) + ch
    out += ''.join(marcas.get(len(texto), []))
    return out


def ligas(texto, ers, mapa):
    """Inserta [texto](url) por entity_ranges LINK, de atrás hacia adelante."""
    for e in sorted(ers, key=lambda e: -e['offset']):
        v = mapa[str(e['key'])]['value']
        if v['type'] != 'LINK':
            continue
        a, z = e['offset'], e['offset'] + e['length']
        texto = texto[:a] + f"[{texto[a:z]}]({v['data']['url']})" + texto[z:]
    return texto


def bloque_md(b, mapa, portada_rel):
    t = b['type']
    if t == 'atomic':
        v = mapa[str(b['entity_ranges'][0]['key'])]['value']
        if v['type'] == 'DIVIDER':
            return '---'
        d = v['data']
        archivo = os.path.basename(d.get('archivo') or '')
        alt = (d.get('alt_original') or d.get('caption') or '').replace('\n', ' ')
        if d.get('clase') == 'video':
            return f'[Video: {archivo}](imagenes/{archivo})'
        pie = f"\n\n_{d['caption']}_" if d.get('caption') else ''
        return f'![{alt}](imagenes/{archivo}){pie}'
    txt = b['text']
    # las ligas primero (cambian offsets), con estilos solo si no hay ligas en el bloque
    if b['entity_ranges']:
        txt = ligas(txt, b['entity_ranges'], mapa)
    else:
        txt = estilo(txt, b['inline_style_ranges'])
    txt = txt.replace('\n', '  \n')
    if t == 'header-one':
        return '## ' + txt
    if t == 'header-two':
        return '### ' + txt
    if t == 'unordered-list-item':
        return '- ' + txt
    if t == 'ordered-list-item':
        return '1. ' + txt
    if t == 'blockquote':
        return '> ' + txt
    return txt


def main():
    arts = json.load(open(os.path.join(AQUI, 'x_articulos.json')))
    fuente = {d['_id']: d for d in json.load(open(os.path.join(AQUI, 'articulos.json')))}
    os.makedirs(IMG, exist_ok=True)
    indice = []
    for x in arts:
        if x['n'] in EXCLUIR:
            continue
        mapa = {e['key']: e for e in x['content_state']['entity_map']}
        src = fuente.get(x['id'], {})
        fecha = (src.get('publishedAt') or src.get('createdAt') or '')[:10]
        portada = x.get('portada')
        partes = [f"# {x['title']}", '']
        partes.append(f"_Ing. Ricardo López Reyero · {fecha} · escrito a mano, sin IA_")
        partes.append('')
        if portada:
            pf = os.path.basename(portada)
            partes.append(f'![Portada](imagenes/{pf})')
            partes.append('')
            copiar(portada, pf)
        for b in x['content_state']['blocks']:
            partes.append(bloque_md(b, mapa, None))
            partes.append('')
            if b['type'] == 'atomic':
                v = mapa[str(b['entity_ranges'][0]['key'])]['value']
                if v['type'] == 'MEDIA':
                    copiar(v['data'].get('archivo'), os.path.basename(v['data'].get('archivo') or ''))
        nombre = f"{x['n']:02d}-{slug(x['title'])}.md"
        open(os.path.join(DEST, nombre), 'w').write(re.sub(r'\n{3,}', '\n\n', '\n'.join(partes)).strip() + '\n')
        indice.append((x['n'], x['title'], nombre, fecha))
    json.dump(indice, open(os.path.join(AQUI, 'indice_md.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(indice), 'artículos en Markdown')


def copiar(ruta, nombre):
    if not ruta or not nombre:
        return
    for carpeta in ('imagenes', 'videos', 'imagenes_x2', 'imagenes_x'):
        cand = os.path.join(AQUI, carpeta, os.path.basename(ruta))
        if os.path.exists(cand):
            dst = os.path.join(IMG, nombre)
            if not os.path.exists(dst):
                shutil.copy(cand, dst)
            return
    if os.path.exists(ruta):
        shutil.copy(ruta, os.path.join(IMG, nombre))


if __name__ == '__main__':
    main()
