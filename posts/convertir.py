"""Convierte el HTML de los blogs de SuperLeads al content_state de los artículos de X.
Sale x_articulos.json: título, portada, bloques y mapa de entidades por artículo."""
import json, re, os, html
from html.parser import HTMLParser

AQUI = os.path.dirname(os.path.abspath(__file__))
BLOQUES = {'p', 'div', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'blockquote', 'figure', 'figcaption', 'ul', 'ol', 'section', 'article', 'pre', 'table', 'tr'}
VACIOS = {'br', 'img', 'hr', 'source', 'input', 'meta', 'link', 'wbr'}


class Nodo:
    def __init__(self, tag, attrs, padre=None):
        self.tag, self.attrs, self.padre, self.hijos = tag, dict(attrs), padre, []


class Arbol(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = Nodo('raiz', [])
        self.act = self.raiz

    def handle_starttag(self, tag, attrs):
        n = Nodo(tag, attrs, self.act)
        self.act.hijos.append(n)
        if tag not in VACIOS:
            self.act = n

    def handle_startendtag(self, tag, attrs):
        self.act.hijos.append(Nodo(tag, attrs, self.act))

    def handle_endtag(self, tag):
        n = self.act
        while n is not self.raiz and n.tag != tag:
            n = n.padre
        if n is not self.raiz:
            self.act = n.padre

    def handle_data(self, data):
        self.act.hijos.append(data)


class Conversor:
    def __init__(self, niveles):
        # los dos niveles de encabezado más altos que use el artículo → Heading y Subheading de X
        self.mapa_h = {}
        for i, nv in enumerate(sorted(niveles)):
            self.mapa_h[nv] = 'header-one' if i == 0 else 'header-two'
        self.bloques, self.entidades = [], []
        self.audios = []
        self._nuevo()

    def _nuevo(self):
        self.txt, self.estilos, self.ligas = '', [], []

    def _cerrar(self, tipo):
        if self.txt.strip():
            self.bloques.append({'tipo': tipo, 'texto': self.txt, 'estilos': self.estilos, 'ligas': self.ligas})
        self._nuevo()

    def _atomico(self, entidad):
        self.entidades.append(entidad)
        self.bloques.append({'tipo': 'atomic', 'texto': ' ', 'estilos': [], 'ligas': [], 'entidad': len(self.entidades) - 1})

    def inline(self, n, estilos, liga):
        if isinstance(n, str):
            s = re.sub(r'[ \t\r\n\f]+', ' ', n.replace(' ', ' '))
            if not s:
                return
            ini = len(self.txt)
            self.txt += s
            fin = len(self.txt)
            for e in estilos:
                self.estilos.append((ini, fin, e))
            if liga:
                self.ligas.append((ini, fin, liga))
            return
        tag = n.tag
        if tag == 'br':
            self.txt += '\n'
            return
        st = list(estilos)
        css = n.attrs.get('style', '') or ''
        if tag in ('strong', 'b') or re.search(r'font-weight:\s*(bold|[6-9]00)', css):
            st.append('Bold')
        if tag in ('em', 'i') or re.search(r'font-style:\s*italic', css):
            st.append('Italic')
        if tag in ('s', 'strike', 'del') or 'line-through' in css:
            st.append('Strikethrough')
        if tag == 'a' and n.attrs.get('href'):
            liga = n.attrs['href']
        for h in n.hijos:
            self.inline(h, st, liga)

    def es_bloque(self, n):
        return not isinstance(n, str) and (n.tag in BLOQUES or n.tag in ('img', 'hr', 'video', 'audio', 'iframe'))

    def contiene_bloque(self, n):
        if isinstance(n, str):
            return False
        return any(self.es_bloque(h) or self.contiene_bloque(h) for h in n.hijos)

    def bloque(self, n, tipo):
        """Recorre n; el texto suelto se junta en bloques del tipo dado."""
        for h in n.hijos:
            if isinstance(h, str) or not (self.es_bloque(h) or self.contiene_bloque(h)):
                self.inline(h, [], None)
                continue
            tag = h.tag
            if tag == 'img':
                self._cerrar(tipo)
                self._atomico({'tipo': 'img', 'src': h.attrs.get('src'), 'alt': (h.attrs.get('alt') or '').strip()})
            elif tag == 'hr':
                self._cerrar(tipo)
                self._atomico({'tipo': 'hr'})
            elif tag == 'video':
                self._cerrar(tipo)
                src = h.attrs.get('src') or next((s.attrs.get('src') for s in h.hijos if not isinstance(s, str) and s.tag == 'source'), None)
                self._atomico({'tipo': 'video', 'src': src})
            elif tag == 'audio':
                self._cerrar(tipo)
                src = h.attrs.get('src') or next((s.attrs.get('src') for s in h.hijos if not isinstance(s, str) and s.tag == 'source'), None)
                self.audios.append(src)
            elif tag in ('ul', 'ol'):
                self._cerrar(tipo)
                lt = 'unordered-list-item' if tag == 'ul' else 'ordered-list-item'
                for li in h.hijos:
                    if isinstance(li, str):
                        continue
                    if li.tag == 'li':
                        self.item(li, lt)
                    else:
                        self.bloque(li, lt)
                        self._cerrar(lt)
            elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
                self._cerrar(tipo)
                t = self.mapa_h.get(int(tag[1]), 'header-two')
                self.bloque(h, t)
                self._cerrar(t)
            elif tag == 'blockquote':
                self._cerrar(tipo)
                self.bloque(h, 'blockquote')
                self._cerrar('blockquote')
            elif tag == 'figcaption':
                self._cerrar(tipo)
                previo = self.bloques[-1] if self.bloques else None
                if previo and previo['tipo'] == 'atomic' and self.entidades[previo['entidad']]['tipo'] == 'img':
                    # el pie va dentro de la imagen, como lo maneja X
                    self.inline(h, [], None)
                    pie = re.sub(r'\s+', ' ', self.txt).strip()
                    self._nuevo()
                    if pie:
                        self.entidades[previo['entidad']]['pie'] = pie
                else:
                    self.inline(h, ['Italic'], None)
                    self._cerrar('unstyled')
            elif tag == 'li':
                self._cerrar(tipo)
                self.item(h, tipo if 'list' in tipo else 'unordered-list-item')
            else:  # p, div, figure, etc.
                self._cerrar(tipo)
                self.bloque(h, tipo)
                self._cerrar(tipo)
        return

    def item(self, li, lt):
        """Un <li>: sus párrafos internos se juntan en un solo renglón con saltos."""
        self._cerrar(lt)
        primero = True
        for h in li.hijos:
            if not isinstance(h, str) and h.tag in ('ul', 'ol'):
                self._cerrar(lt)
                sub = Nodo('x', [])
                sub.hijos = [h]
                self.bloque(sub, lt)
                continue
            if not isinstance(h, str) and h.tag in ('p', 'div'):
                if not primero and self.txt.strip():
                    self.txt += '\n'
                if self.contiene_bloque(h):
                    self.bloque(h, lt)
                else:
                    for x in h.hijos:
                        self.inline(x, [], None)
                primero = False
            elif not isinstance(h, str) and self.es_bloque(h):
                sub = Nodo('x', [])
                sub.hijos = [h]
                self.bloque(sub, lt)
            else:
                self.inline(h, [], None)
        self._cerrar(lt)


def limpiar(b):
    """Quita espacios sobrantes al inicio/fin de cada renglón y recorre estilos y ligas."""
    t = b['texto']
    keep = [True] * len(t)
    # espacios alrededor de saltos y en los extremos
    for m in re.finditer(r' *\n *', t):
        for i in range(m.start(), m.end()):
            keep[i] = t[i] == '\n'
    i = 0
    while i < len(t) and t[i] in ' \n':
        keep[i] = False
        i += 1
    i = len(t) - 1
    while i >= 0 and t[i] in ' \n':
        keep[i] = False
        i -= 1
    nuevo_idx, s = [], ''
    for i, ch in enumerate(t):
        nuevo_idx.append(len(s))
        if keep[i]:
            s += ch
    nuevo_idx.append(len(s))

    def mover(a, z):
        return nuevo_idx[a], nuevo_idx[z]

    def rangos(lista):
        out = []
        for a, z, v in lista:
            a2, z2 = mover(a, z)
            if z2 > a2:
                out.append((a2, z2, v))
        return out
    return s, rangos(b['estilos']), rangos(b['ligas'])


def fusionar(rangos):
    """Une rangos contiguos del mismo valor."""
    por = {}
    for a, z, v in sorted(rangos, key=lambda r: (str(r[2]), r[0])):
        l = por.setdefault(v, [])
        if l and a <= l[-1][1]:
            l[-1][1] = max(l[-1][1], z)
        else:
            l.append([a, z])
    return [(a, z, v) for v, l in por.items() for a, z in l]


def a_x(conv):
    bloques, mapa = [], []
    for i, b in enumerate(conv.bloques):
        if b['tipo'] == 'atomic':
            e = conv.entidades[b['entidad']]
            key = len(mapa)
            if e['tipo'] == 'hr':
                mapa.append({'key': str(key), 'value': {'data': {}, 'type': 'DIVIDER', 'mutability': 'Immutable'}})
            else:
                datos = {'archivo': e['src'], 'clase': e['tipo'], 'alt_original': e.get('alt', '')}
                if e.get('pie'):
                    datos['caption'] = e['pie']
                mapa.append({'key': str(key), 'value': {'data': datos, 'type': 'MEDIA', 'mutability': 'Immutable'}})
            bloques.append({'data': {}, 'text': ' ', 'key': f'b{i:04d}', 'type': 'atomic',
                            'entity_ranges': [{'key': key, 'offset': 0, 'length': 1}], 'inline_style_ranges': []})
            continue
        s, est, lig = limpiar(b)
        if not s.strip():
            continue

        # X cuenta posiciones por carácter (un emoji = 1), no en UTF-16
        def off(a):
            return a
        isr = [{'offset': off(a), 'length': off(z) - off(a), 'style': v} for a, z, v in fusionar(est)]
        ers = []
        for a, z, url in fusionar(lig):
            key = len(mapa)
            mapa.append({'key': str(key), 'value': {'data': {'url': url}, 'type': 'LINK', 'mutability': 'Mutable'}})
            ers.append({'key': key, 'offset': off(a), 'length': off(z) - off(a)})
        bloques.append({'data': {}, 'text': s, 'key': f'b{i:04d}', 'type': b['tipo'],
                        'entity_ranges': ers, 'inline_style_ranges': isr})
    return {'blocks': bloques, 'entity_map': mapa}


def main():
    data = json.load(open(os.path.join(AQUI, 'articulos.json')))
    manifest = json.load(open(os.path.join(AQUI, 'manifest.json')))
    salida = []
    for i, d in enumerate(data):
        h = d.get('rawHTML') or ''
        if not h.strip():
            continue
        a = Arbol()
        a.feed(h)
        niveles = {int(x) for x in re.findall(r'<h([1-6])', h)}
        c = Conversor(niveles)
        c.bloque(a.raiz, 'unstyled')
        c._cerrar('unstyled')
        cs = a_x(c)
        m = manifest[d['_id']]
        por_src = {x['src']: x['file'] for x in m['internas']}
        for e in cs['entity_map']:
            v = e['value']
            if v['type'] == 'MEDIA':
                src = v['data']['archivo']
                v['data']['archivo'] = por_src.get(src, src)
        salida.append({'n': i + 1, 'id': d['_id'], 'title': d['title'].strip(), 'status': d['status'],
                       'portada': m['portada'], 'content_state': cs, 'audios': c.audios})
    json.dump(salida, open(os.path.join(AQUI, 'x_articulos.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(salida), 'artículos convertidos')


if __name__ == '__main__':
    main()
