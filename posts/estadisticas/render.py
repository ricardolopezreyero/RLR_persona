"""Render de la serie «Datos» (serie.py) a Shorts verticales 1080×1920 con el diseño SuperLeads:
HTML + SVG por pieza → Chrome sin cabeza por CDP → PNG (cuadro final) y MP4 (las barras crecen, los números cuentan, 8 s).
Uso: python3 render.py [n ...]  (sin argumentos: todas). Variables: SOLO_PNG=1 para saltar el video.
Ricardo López Reyero · RLR"""
import os, re, sys, json, math, time, html, shutil, datetime, subprocess, tempfile, urllib.request
import websocket
from serie import P, SERIES, armar_descripcion

_RLR = 'Ricardo López Reyero'; _k = 'EYE'; _rev = 181218  # ROT13 de RLR y posiciones 18·12·18
AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, 'salida'); HTMLD = os.path.join(AQUI, 'html')
SCRATCH = os.environ.get('SCRATCH', os.path.join(tempfile.gettempdir(), 'rlr_datos'))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
VERSION = os.environ.get('VERSION', 'v1')
FPS, DUR, FIN_ANIM = 30, 8.0, 3.6
COL = {'c1': '#2a78d6', 'c2': '#eb6834', 'c3': '#1baf7a', 'neu': '#c6ccd8'}
TRACK = 'rgba(255,255,255,.07)'; T2 = '#7a9fd4'; T3 = '#4a6aaa'
WC = 920  # ancho útil (1080 − 2×80)
PIE = ('', 'Serie · La realidad de la educación'); LOGO = 'file://' + os.path.join(AQUI, 'logo_blanco.svg')  # parametrizables por serie
LOGO_RLR_N = 'file://' + os.path.join(AQUI, 'rlr_nombre.png')  # la marca de Ricardo, arriba: solo el nombre completo (sin monograma, 29-oct)

# ───────────── formato de números ─────────────
def partes(v, fmt):
    """(prefijo, decimales, sufijo) para el conteo animado."""
    return {'num': ('', 0, ''), 'usd': ('$', 0, ''), 'mxn': ('$', 0, ''), 'pct': ('', 0, '%'),
            'pct1': ('', len(str(v).split('.')[1]) if '.' in str(v) else 0, '%'), 'x': ('', 0, '×')}[fmt]

def texto_valor(v, fmt):
    pre, dec, suf = partes(v, fmt)
    return f"{pre}{v:,.{dec}f}{suf}"

UNIDAD = {'mxn': 'MXN', 'usd': 'USD'}  # la unidad siempre visible, como etiqueta (Ricardo, 29-oct: «estamos en internet»)
def chip_svg(xr, y, txt, size):
    """Etiqueta de unidad en SVG, pegada a la derecha en xr; regresa (svg, ancho)."""
    fs = round(size * .5); cw = round(len(txt) * fs * .72 + fs * .9); h = round(size * .68); yt = y - round(size * .7)
    return (f'<rect x="{xr - cw}" y="{yt}" width="{cw}" height="{h}" rx="{round(h * .22)}" fill="none" stroke="rgba(255,255,255,.7)" stroke-width="1.5"/>'
            f'<text x="{xr - cw / 2:.1f}" y="{yt + h / 2 + fs * .36:.1f}" text-anchor="middle" font-size="{fs}" font-weight="800" letter-spacing="1.5" fill="#fff">{txt}</text>'), cw

def u_html(txt):
    """' MXN' / ' USD' en un texto (ya escapado o HTML) → etiqueta de unidad."""
    return re.sub(r' (MXN|USD)\b', r'<span class="u">\1</span>', txt)

def num_anim(v, fmt, x, y, retardo, size=34, anchor='end', fill='#fff', peso=800, extra=''):
    pre, dec, suf = partes(v, fmt); chip = ''
    if fmt in UNIDAD and anchor == 'end':
        chip, cw = chip_svg(x, y, UNIDAD[fmt], size); x = x - cw - round(size * .3)
    return chip + (f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" font-weight="{peso}" fill="{fill}" class="tab" '
            f'data-a="n" data-n="{v}" data-dec="{dec}" data-pre="{html.escape(pre)}" data-suf="{html.escape(suf)}" data-d="{retardo:.2f}" data-t="1.0" {extra}>{texto_valor(v, fmt)}</text>')

def stat_anim(txt, retardo):
    """Número de un stat: cuenta si es numérico ('1,410,459', '+391%', '89 mil', '~45,000'), si no, texto fijo."""
    chip = ''; mu = re.match(r'^(.*\S) (MXN|USD)$', txt)
    if mu: txt, chip = mu.group(1), f'<span class="u">{mu.group(2)}</span>'
    m = re.match(r'^([~$+−-]*)([\d,]+(?:\.\d+)?)(.*)$', txt)
    if not m: return html.escape(txt) + chip
    pre, n, suf = m.groups(); v = float(n.replace(',', '')); dec = len(n.split('.')[1]) if '.' in n else 0
    return (f'<span data-a="n" data-n="{v}" data-dec="{dec}" data-pre="{html.escape(pre)}" data-suf="{html.escape(suf)}" data-d="{retardo:.2f}" data-t="1.1">{html.escape(txt)}</span>') + chip

# ───────────── gráficas ─────────────  RLR
def g_barras(g, r0):
    items = g['items']; alto = g.get('alto', 44); gap = g.get('gap', 24); fmt = g['fmt']
    vmax = g.get('max') or max(i[1] for i in items)
    y = 0; out = []
    if g.get('sub'):
        out.append(f'<text x="0" y="22" font-size="24" fill="{T3}">{html.escape(g["sub"])}</text>'); y = 50
    if g.get('ref'): y += 44
    y0 = y
    for i, it in enumerate(items):
        label, v, c = it[0], it[1], it[2]; txt = it[3] if len(it) > 3 else None
        w = v / vmax * WC; d = r0 + i * 0.12
        out.append(f'<text x="0" y="{y + 30}" font-size="30" font-weight="600" fill="#fff">{html.escape(label)}</text>')
        if txt: out.append(f'<text x="{WC}" y="{y + 30}" text-anchor="end" font-size="34" font-weight="800" fill="#fff" class="tab">{html.escape(txt)}</text>')
        else: out.append(num_anim(v, fmt, WC, y + 30, d))
        out.append(f'<rect x="0" y="{y + 46}" width="{WC}" height="{alto}" rx="{alto / 2}" fill="{TRACK}"/>')
        out.append(f'<rect x="0" y="{y + 46}" width="{w:.1f}" height="{alto}" rx="{alto / 2}" fill="{COL[c]}" data-a="w" data-w="{w:.1f}" data-d="{d:.2f}" data-t="1.0"/>')
        y += 46 + alto + gap
    H = y - gap
    if g.get('ref'):
        rv, rl = g['ref']; rx = rv / vmax * WC
        out.append(f'<line x1="{rx:.1f}" y1="{y0 - 14}" x2="{rx:.1f}" y2="{H}" stroke="rgba(255,255,255,.55)" stroke-width="2" stroke-dasharray="8 8"/>')
        out.append(f'<text x="{rx + 14:.1f}" y="{y0 - 22}" font-size="24" font-weight="600" fill="{T2}">{html.escape(rl)}</text>')
    return f'<svg width="{WC}" height="{H}" viewBox="0 0 {WC} {H}">{"".join(out)}</svg>', r0 + len(items) * 0.12 + 1.0

def g_pares(g, r0):
    s1, s2 = g['series']; alto = 38; out = []
    vmax = max(max(a, b) for _, a, b in g['grupos'])
    out.append(f'<circle cx="8" cy="12" r="8" fill="{COL["c1"]}"/><text x="26" y="20" font-size="24" font-weight="600" fill="{T2}">{html.escape(s1)}</text>')
    out.append(f'<circle cx="268" cy="12" r="8" fill="{COL["c2"]}"/><text x="286" y="20" font-size="24" font-weight="600" fill="{T2}">{html.escape(s2)}</text>')
    y = 56
    for i, (lab, a, b) in enumerate(g['grupos']):
        out.append(f'<text x="0" y="{y + 28}" font-size="30" font-weight="700" fill="#fff">{html.escape(lab)}</text>')
        for j, (v, c) in enumerate(((a, 'c1'), (b, 'c2'))):
            yy = y + 44 + j * (alto + 10); w = v / vmax * (WC - 120); d = r0 + i * 0.18 + j * 0.1
            out.append(f'<rect x="0" y="{yy}" width="{WC - 120}" height="{alto}" rx="{alto / 2}" fill="{TRACK}"/>')
            out.append(f'<rect x="0" y="{yy}" width="{w:.1f}" height="{alto}" rx="{alto / 2}" fill="{COL[c]}" data-a="w" data-w="{w:.1f}" data-d="{d:.2f}" data-t="1.0"/>')
            out.append(num_anim(v, g['fmt'], WC, yy + 29, d, size=30))
        y += 44 + 2 * alto + 10 + 34
    H = y - 34
    return f'<svg width="{WC}" height="{H}" viewBox="0 0 {WC} {H}">{"".join(out)}</svg>', r0 + 1.6

def g_waffle(g, r0):
    total, lleno, cols = g['total'], g['lleno'], g['cols']; tam = g.get('tam', 46); gap = g.get('gap', 10)
    filas = math.ceil(total / cols); Wg = cols * tam + (cols - 1) * gap; Hg = filas * tam + (filas - 1) * gap
    rx = 8 if tam < 80 else 24; out = []
    for i in range(total):
        x = (i % cols) * (tam + gap); y = (i // cols) * (tam + gap)
        if i < lleno:
            out.append(f'<rect x="{x}" y="{y}" width="{tam}" height="{tam}" rx="{rx}" fill="{COL["c2"]}" data-a="o" data-d="{r0 + i * (1.4 / max(lleno, 1)):.3f}" data-t="0.3"/>')
        else:
            out.append(f'<rect x="{x}" y="{y}" width="{tam}" height="{tam}" rx="{rx}" fill="rgba(255,255,255,.08)" stroke="rgba(255,255,255,.18)" stroke-width=".5"/>')
    svg = f'<svg width="{Wg}" height="{Hg}" viewBox="0 0 {Wg} {Hg}">{"".join(out)}</svg>'
    if g.get('numero'):
        return (f'<div class="waffle"><div>{svg}</div><div class="wnum"><div class="n" data-a="oy" data-d="{r0 + .4:.2f}" data-t=".8">{g["numero"]}</div>'
                f'<div class="l" data-a="o" data-d="{r0 + .8:.2f}">{html.escape(g["etiqueta"])}</div></div></div>'), r0 + 1.6
    return f'<div class="waffle">{svg}</div>', r0 + 1.6

def g_dona(g, r0):
    R, S = 190, 48; C = 2 * math.pi * R; f = g['pct'] / 100
    svg = (f'<svg width="440" height="440" viewBox="0 0 440 440"><circle cx="220" cy="220" r="{R}" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="{S}"/>'
           f'<circle cx="220" cy="220" r="{R}" fill="none" stroke="{COL[g.get("color", "c2")]}" stroke-width="{S}" stroke-linecap="round" transform="rotate(-90 220 220)" '
           f'stroke-dasharray="{C:.1f}" stroke-dashoffset="{C:.1f}" data-a="r" data-c="{C:.1f}" data-f="{f}" data-d="{r0:.2f}" data-t="1.4"/>'
           f'<text x="220" y="258" text-anchor="middle" font-size="112" font-weight="800" fill="#fff" class="tab" data-a="n" data-n="{g["pct"]}" data-dec="0" data-pre="" data-suf="%" data-d="{r0:.2f}" data-t="1.4">{g["numero"]}</text></svg>')
    return f'<div class="dona">{svg}<div class="l" data-a="oy" data-d="{r0 + .6:.2f}">{html.escape(g["etiqueta"])}</div></div>', r0 + 1.6

def g_donas(g, r0):
    R, S = 128, 34; C = 2 * math.pi * R; cols = []
    for i, (pct, num, lab, c) in enumerate(g['items']):
        d = r0 + i * 0.25
        svg = (f'<svg width="300" height="300" viewBox="0 0 300 300"><circle cx="150" cy="150" r="{R}" fill="none" stroke="rgba(255,255,255,.08)" stroke-width="{S}"/>'
               f'<circle cx="150" cy="150" r="{R}" fill="none" stroke="{COL[c]}" stroke-width="{S}" stroke-linecap="round" transform="rotate(-90 150 150)" '
               f'stroke-dasharray="{C:.1f}" stroke-dashoffset="{C:.1f}" data-a="r" data-c="{C:.1f}" data-f="{pct / 100}" data-d="{d:.2f}" data-t="1.4"/>'
               f'<text x="150" y="176" text-anchor="middle" font-size="76" font-weight="800" fill="#fff" class="tab" data-a="n" data-n="{pct}" data-dec="0" data-pre="" data-suf="%" data-d="{d:.2f}" data-t="1.4">{num}</text></svg>')
        cols.append(f'<div class="dcol">{svg}<div class="l" data-a="oy" data-d="{d + .6:.2f}">{html.escape(lab)}</div></div>')
    return f'<div class="donas">{"".join(cols)}</div>', r0 + 1.8

def g_stats(g, r0):
    cells = ''.join(f'<div class="cell"><div class="n" data-a="oy" data-d="{r0 + i * .15:.2f}">{stat_anim(n, r0 + i * .15)}</div><div class="l">{html.escape(l)}</div></div>'
                    for i, (n, l) in enumerate(g['items']))
    return f'<div class="stats" style="grid-template-columns:repeat({len(g["items"])},1fr)">{cells}</div>', r0 + 1.2

def g_tiempo(g, r0):
    res = g.get('resaltar'); rows = []
    for i, (a, t) in enumerate(g['items']):
        cls = ' hi' if (res is None or i in res) else ''
        rows.append(f'<div class="tr{cls}" data-a="oy" data-d="{r0 + i * .22:.2f}" data-t=".7"><div class="ty">{html.escape(a)}</div><div class="tx">{html.escape(t)}</div></div>')
    return f'<div class="tl">{"".join(rows)}</div>', r0 + len(g['items']) * .22 + .7

def g_franjas(g, r0):
    X = lambda h: h / 24 * WC; out = []; alto = 64
    out.append(f'<text x="0" y="22" font-size="26" font-weight="600" fill="{T2}">Familias conectadas a internet</text>')
    for i, (a, b, pct) in enumerate([(12, 14, 90), (16, 19, 85), (21, 24, 93)]):
        x, w = X(a), X(b) - X(a); d = r0 + i * .15
        out.append(f'<rect x="{x:.1f}" y="38" width="{w:.1f}" height="{alto}" rx="10" fill="{COL["c1"]}" data-a="w" data-w="{w:.1f}" data-d="{d:.2f}" data-t=".9"/>')
        out.append(f'<text x="{x + w / 2:.1f}" y="80" text-anchor="middle" font-size="27" font-weight="800" fill="#fff" class="tab">{pct}%</text>')
        out.append(f'<text x="{x + w / 2:.1f}" y="130" text-anchor="middle" font-size="22" fill="{T3}">{a}–{b} h</text>')
    out.append(f'<text x="0" y="186" font-size="26" font-weight="600" fill="{T2}">Horario de atención del colegio</text>')
    x, w = X(7), X(15) - X(7)
    out.append(f'<rect x="{x:.1f}" y="202" width="{w:.1f}" height="{alto}" rx="10" fill="{COL["c2"]}" data-a="w" data-w="{w:.1f}" data-d="{r0 + .6:.2f}" data-t=".9"/>')
    out.append(f'<text x="{x + w / 2:.1f}" y="244" text-anchor="middle" font-size="27" font-weight="800" fill="#fff">7:00 – 15:00</text>')
    for h in range(0, 25, 3):
        out.append(f'<line x1="{X(h):.1f}" y1="282" x2="{X(h):.1f}" y2="296" stroke="rgba(255,255,255,.3)" stroke-width="2"/>')
        anc = 'start' if h == 0 else 'end' if h == 24 else 'middle'
        out.append(f'<text x="{X(h):.1f}" y="326" text-anchor="{anc}" font-size="22" fill="{T3}" class="tab">{h}:00</text>')
    out.append(f'<line x1="0" y1="282" x2="{WC}" y2="282" stroke="rgba(255,255,255,.3)" stroke-width="1"/>')
    return f'<svg width="{WC}" height="336" viewBox="0 0 {WC} 336">{"".join(out)}</svg>', r0 + 1.8

def g_estrellas(g, r0):
    X = lambda v: (v - 1) / 4 * WC; out = []; y, h = 150, 56
    out.append(f'<rect x="0" y="{y}" width="{WC}" height="{h}" rx="{h / 2}" fill="rgba(255,255,255,.08)"/>')
    w1 = X(3); out.append(f'<rect x="0" y="{y}" width="{w1:.1f}" height="{h}" rx="{h / 2}" fill="{COL["c2"]}" data-a="w" data-w="{w1:.1f}" data-d="{r0:.2f}" data-t="1.0"/>')
    x2, w2 = X(4.2), X(4.5) - X(4.2); out.append(f'<rect x="{x2:.1f}" y="{y}" width="{w2:.1f}" height="{h}" fill="{COL["c3"]}" data-a="w" data-w="{w2:.1f}" data-d="{r0 + .5:.2f}" data-t=".8"/>')
    out.append(f'<circle cx="{WC - 28}" cy="{y + h / 2}" r="22" fill="{COL["c2"]}" stroke="#001240" stroke-width="6" data-a="o" data-d="{r0 + 1.0:.2f}" data-t=".5"/>')
    for v in range(1, 6):
        anc = 'start' if v == 1 else 'end' if v == 5 else 'middle'
        out.append(f'<text x="{X(v):.1f}" y="{y + h + 46}" text-anchor="{anc}" font-size="30" font-weight="700" fill="#fff">{v} ★</text>')
    # anotaciones arriba
    out.append(f'<g data-a="oy" data-d="{r0 + .3:.2f}"><text x="{w1 / 2:.1f}" y="44" text-anchor="middle" font-size="40" font-weight="800" fill="#fff" class="tab">71%</text>'
               f'<text x="{w1 / 2:.1f}" y="82" text-anchor="middle" font-size="24" fill="{T2}">descarta un negocio con menos de 3 estrellas</text>'
               f'<line x1="{w1 / 2:.1f}" y1="98" x2="{w1 / 2:.1f}" y2="{y - 12}" stroke="rgba(255,255,255,.35)" stroke-width="2"/></g>')
    xm = x2 + w2 / 2
    out.append(f'<g data-a="oy" data-d="{r0 + .9:.2f}"><text x="{WC}" y="44" text-anchor="end" font-size="40" font-weight="800" fill="#fff" class="tab">4.2 – 4.5</text>'
               f'<text x="{WC}" y="82" text-anchor="end" font-size="24" fill="{T2}">el rango que más confianza genera</text>'
               f'<line x1="{xm:.1f}" y1="98" x2="{xm:.1f}" y2="{y - 12}" stroke="rgba(255,255,255,.35)" stroke-width="2"/></g>')
    out.append(f'<text x="{WC}" y="{y + h + 112}" text-anchor="end" font-size="24" fill="{T2}" data-a="o" data-d="{r0 + 1.3:.2f}"><tspan font-weight="800" fill="#fff">5.0 perfecto: 46% desconfía.</tspan> Lo asocia con reseñas compradas.</text>')
    H = y + h + 130
    return f'<svg width="{WC}" height="{H}" viewBox="0 0 {WC} {H}">{"".join(out)}</svg>', r0 + 2.0

def g_embudo(g, r0):
    cols = []; total = g['total']; nc, pitch, r = 8, 52, 19
    for k, lado in enumerate((g['izq'], g['der'])):
        dots = []
        for i in range(total):
            cx = (i % nc) * pitch + pitch / 2; cy = (i // nc) * pitch + pitch / 2
            if i < lado['lleno']:
                dots.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{COL[lado["color"]]}" data-a="o" data-d="{r0 + .3 + i * .08:.2f}" data-t=".3"/>')
            else:
                dots.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="rgba(255,255,255,.1)" stroke="rgba(255,255,255,.2)" stroke-width=".5"/>')
        W, H = nc * pitch, math.ceil(total / nc) * pitch
        cols.append(f'<div class="ecol"><div class="et">{html.escape(lado["titulo"])}</div><svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{"".join(dots)}</svg>'
                    f'<div class="en" data-a="oy" data-d="{r0 + 1.3:.2f}">{html.escape(lado["cifra"])}</div><div class="el">inscripciones de {total} consultas</div></div>')
    return f'<div class="embudo">{"".join(cols)}</div>', r0 + 2.0

def g_tarjetas(g, r0):
    cards = []
    for k, (tit, stats, remate) in enumerate(g['items']):
        rows = ''
        for j, (v, num, lab, c) in enumerate(stats):
            d = r0 + k * .2 + j * .3; w = v / 100 * 376
            rows += (f'<div class="trow"><div class="tn tab" data-a="n" data-n="{v}" data-dec="0" data-pre="" data-suf="%" data-d="{d:.2f}" data-t="1.1">{num}</div><div class="tlab">{html.escape(lab)}</div>'
                     f'<svg width="376" height="14" viewBox="0 0 376 14"><rect x="0" y="0" width="376" height="14" rx="7" fill="{TRACK}"/><rect x="0" y="0" width="{w:.1f}" height="14" rx="7" fill="{COL[c]}" data-a="w" data-w="{w:.1f}" data-d="{d:.2f}" data-t="1.1"/></svg></div>')
        cards.append(f'<div class="card"><div class="ct">{html.escape(tit)}</div>{rows}<div class="cr" data-a="o" data-d="{r0 + 1.4:.2f}">{html.escape(remate)}</div></div>')
    return f'<div class="tarjetas">{"".join(cards)}</div>', r0 + 2.0

def g_piramide(g, r0):
    items = g['items']; vmax = max(i[1] for i in items); rh, X0, WMAX = 70, 170, 430; out = []
    top = sum(1 for i in items if i[4]); y = 48
    out.append(f'<rect x="0" y="{y - 10}" width="{WC}" height="{top * rh + 4}" rx="14" fill="rgba(86,239,159,.06)" stroke="rgba(86,239,159,.35)" stroke-width=".5"/>')
    out.append(f'<text x="{WC}" y="30" text-anchor="end" font-size="24" font-weight="700" fill="#56EF9F" letter-spacing="1">{html.escape(g["corchete"])}</text>')
    for i, (lab, pct, hog, ing, hi) in enumerate(items):
        yy = y + i * rh; w = pct / vmax * WMAX; d = r0 + i * .1
        out.append(f'<text x="{X0 - 24}" y="{yy + 30}" text-anchor="end" font-size="28" font-weight="800" fill="#fff">{html.escape(lab)}</text>')
        out.append(f'<text x="{X0 - 24}" y="{yy + 56}" text-anchor="end" font-size="21" fill="{T3}" class="tab">{pct}%</text>')
        out.append(f'<rect x="{X0}" y="{yy + 8}" width="{w:.1f}" height="{rh - 20}" rx="10" fill="{COL["c1"] if hi else "rgba(255,255,255,.16)"}" data-a="w" data-w="{w:.1f}" data-d="{d:.2f}" data-t="1.0"/>')
        out.append(f'<text x="{X0 + w + 16:.1f}" y="{yy + 42}" font-size="28" font-weight="800" fill="#fff" class="tab" data-a="o" data-d="{d + .5:.2f}">{hog}</text>')
        if ing: out.append(f'<text x="{WC}" y="{yy + 42}" text-anchor="end" font-size="22" fill="{T2}" class="tab">{html.escape(ing)}</text>')
    H = y + len(items) * rh
    return f'<svg width="{WC}" height="{H}" viewBox="0 0 {WC} {H}">{"".join(out)}</svg>', r0 + 1.8

def g_columnas(g, r0):
    """Columnas verticales (meses): etiqueta abajo, valor arriba, la más alta en c2 si g['resaltar']."""
    items = g['items']; vmax = g.get('max') or max(v for _, v in items); H = g.get('alto', 420); n = len(items)
    gap = 14; w = (WC - gap * (n - 1)) / n; base = H - 44; out = []
    for i, (lab, v) in enumerate(items):
        h = v / vmax * (base - 50); x = i * (w + gap); y = base - h; c = COL['c2'] if (g.get('resaltar') and v >= g['resaltar']) else COL['c1']
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="8" fill="{c}" data-a="h" data-h="{h:.1f}" data-y0="{y:.1f}" data-d="{r0 + i * .07:.2f}" data-t=".9"/>')
        out.append(num_anim(v, g['fmt'], x + w / 2, y - 12, r0 + i * .07, size=24, anchor='middle'))
        out.append(f'<text x="{x + w / 2:.1f}" y="{H - 10}" text-anchor="middle" font-size="22" font-weight="600" fill="{T2}">{html.escape(lab)}</text>')
    out.append(f'<line x1="0" y1="{base}" x2="{WC}" y2="{base}" stroke="rgba(255,255,255,.25)" stroke-width="1"/>')
    return f'<svg width="{WC}" height="{H}" viewBox="0 0 {WC} {H}">{"".join(out)}</svg>', r0 + n * .07 + .9

GRAF = dict(columnas=g_columnas, barras=g_barras, pares=g_pares, waffle=g_waffle, dona=g_dona, donas=g_donas, stats=g_stats, tiempo=g_tiempo,
            franjas=g_franjas, estrellas=g_estrellas, embudo=g_embudo, tarjetas=g_tarjetas, piramide=g_piramide)

CSS = """
:root{--green:#56EF9F;--navy-deep:#001240;--t2:#7a9fd4;--t3:#4a6aaa}
*{box-sizing:border-box}
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:var(--navy-deep);color:#fff;font-family:"Plus Jakarta Sans",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
.fondo{position:absolute;inset:0;overflow:hidden;pointer-events:none}
.g1{position:absolute;top:-240px;right:-280px;width:960px;height:960px;border-radius:50%;background:rgba(42,137,251,.11);filter:blur(150px)}
.g2{position:absolute;bottom:-320px;left:-280px;width:900px;height:900px;border-radius:50%;background:rgba(86,239,159,.07);filter:blur(150px)}
header{position:absolute;top:78px;left:80px;right:80px;display:flex;justify-content:space-between;align-items:center}
.marca{display:flex;align-items:center} .marca .nombre{height:78px;width:auto;display:block}
.serie{font-size:17px;font-weight:700;letter-spacing:2px;color:var(--t3);text-transform:uppercase;text-align:right;max-width:300px;line-height:1.35}
main{position:absolute;top:292px;left:80px;right:80px}
.eyebrow{display:flex;align-items:center;gap:12px;margin-bottom:26px}
.eyebrow::before{content:"";width:12px;height:12px;border-radius:50%;background:var(--green);flex:none}
.eyebrow span{font-size:22px;font-weight:700;letter-spacing:2.4px;text-transform:uppercase;color:var(--green)}
h1{margin:0;font-weight:800;line-height:1.04;font-size:var(--h1);letter-spacing:var(--ls)}
h1 em{font-style:italic;color:var(--green)}
.u{display:inline-block;font-style:normal;font-size:.44em;font-weight:800;letter-spacing:1.5px;line-height:1;padding:.24em .46em .2em;border:1.5px solid currentColor;border-radius:.36em;margin-left:.3em;vertical-align:middle;position:relative;top:-.1em;opacity:.92}
.grafica{margin-top:var(--gap)} .grafica>*+*{margin-top:34px}
.lectura{margin-top:var(--gap);font-size:33px;line-height:1.38;font-weight:500;color:var(--t2)}
.nota{margin-top:28px;font-size:22px;line-height:1.4;color:var(--t3)}
main.compacto .lectura{font-size:30px;margin-top:30px} main.compacto .nota{font-size:21px;margin-top:22px} main.compacto .grafica>*+*{margin-top:26px}
footer{position:absolute;left:80px;right:80px;bottom:132px;border-top:.5px solid rgba(255,255,255,.14);padding-top:26px;display:flex;justify-content:space-between;align-items:center;font-size:21px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--t3)}
footer img{width:202px;height:auto;display:block}
svg{display:block;overflow:visible} svg text{font-family:"Plus Jakarta Sans"} .tab{font-variant-numeric:tabular-nums}
.waffle{display:flex;align-items:center;gap:48px} .wnum .n{font-size:168px;font-weight:800;letter-spacing:-7px;line-height:1} .wnum .l{margin-top:16px;font-size:27px;line-height:1.35;color:var(--t2)}
.dona{display:flex;align-items:center;gap:44px} .dona .l{font-size:30px;line-height:1.38;color:var(--t2)}
.donas{display:flex;gap:40px} .dcol{flex:1;display:flex;flex-direction:column;align-items:center;text-align:center} .dcol .l{margin-top:14px;font-size:25px;line-height:1.35;color:var(--t2)}
.stats{display:grid;gap:1px;background:rgba(255,255,255,.14);border:.5px solid rgba(255,255,255,.14);border-radius:16px;overflow:hidden}
.stats .cell{background:var(--navy-deep);padding:26px 20px 24px} .stats .n{white-space:nowrap} .stats .u{font-size:.36em;margin-left:.22em} .lectura .u{font-size:.58em;top:-.06em} .stats .n{font-size:52px;font-weight:800;letter-spacing:-1.5px;line-height:1;font-variant-numeric:tabular-nums} .stats .l{margin-top:10px;font-size:21px;line-height:1.35;color:var(--t3)}
.tl{display:flex;flex-direction:column;gap:22px} .tr{display:grid;grid-template-columns:168px 1fr;gap:18px;position:relative;padding-left:0}
.ty{font-size:38px;font-weight:800;color:var(--green);letter-spacing:-1px;line-height:1.1} .tx{font-size:26px;line-height:1.34;color:var(--t2);border-left:.5px solid rgba(255,255,255,.2);padding-left:22px} .tr.hi .tx{color:#fff}
.embudo{display:flex;gap:40px} .ecol{flex:1;display:flex;flex-direction:column;align-items:flex-start} .et{font-size:22px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:var(--t2);margin-bottom:18px;min-height:60px;line-height:1.3}
.en{margin-top:18px;font-size:72px;font-weight:800;letter-spacing:-2px;line-height:1} .el{margin-top:6px;font-size:22px;color:var(--t3)}
.tarjetas{display:flex;gap:32px} .card{flex:1;border:.5px solid rgba(255,255,255,.16);background:rgba(255,255,255,.03);border-radius:20px;padding:30px 32px 26px}
.ct{font-size:22px;font-weight:700;letter-spacing:2.4px;color:var(--green);margin-bottom:14px} .trow{margin-top:18px} .tn{font-size:92px;font-weight:800;letter-spacing:-4px;line-height:1} .tlab{font-size:22px;color:var(--t2);margin:6px 0 10px}
.cr{margin-top:24px;font-size:22px;font-style:italic;color:var(--t3);line-height:1.35}
"""

JS = """
/* RLR */ const _RLR='Ricardo López Reyero', _k='EYE', _rev=181218;
const E=t=>{t=Math.min(Math.max(t,0),1);return 1-Math.pow(1-t,3)};
const fmtN=(v,dec,pre,suf)=>pre+v.toFixed(dec).replace(/\\B(?=(\\d{3})+(?!\\d))/g,',')+suf;
window.anim=function(t){document.querySelectorAll('[data-a]').forEach(el=>{const D=el.dataset,p=E((t-(+D.d||0))/(+D.t||.8));switch(D.a){
case 'w':el.setAttribute('width',Math.max(0,+D.w*p));break;
case 'o':el.style.opacity=p;break;
case 'oy':el.style.opacity=p;el.style.transform='translateY('+((1-p)*22)+'px)';break;
case 'n':el.textContent=fmtN(+D.n*p,+D.dec||0,D.pre||'',D.suf||'');break;
case 'r':el.setAttribute('stroke-dashoffset',+D.c*(1-(+D.f)*p));break;
case 'h':el.setAttribute('height',Math.max(0,+D.h*p));el.setAttribute('y',+D.y0+(+D.h)*(1-p));break;}})};
window.anim(0);
"""

def tam_h1(h1):
    n = len(re.sub('<[^>]+>', '', h1))
    return 94 if n <= 36 else 84 if n <= 50 else 74 if n <= 66 else 66 if n <= 84 else 58

def pagina(p):
    s = SERIES[p['serie']]; total = sum(1 for q in P if q['serie'] == p['serie']); k = sum(1 for q in P if q['serie'] == p['serie'] and q['n'] <= p['n'])
    gs = p['grafica'] if isinstance(p['grafica'], list) else [p['grafica']]
    r = 0.5; bloques = []
    for g in gs:
        h, r = GRAF[g['tipo']](g, r); bloques.append(h)
    fin = r
    t = tam_h1(p['h1']); gap = 52 if t >= 74 else 44
    if p.get('compacto'): gap = 34
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{html.escape(p['slug'])}</title>
<meta name="author" content="{_RLR}"><meta name="build" content="eye"><meta name="rev" content="{_rev}">
<!-- RLR · serie Datos · pieza {p['n']:02d} -->
<style>{CSS}</style></head><body data-author="RLR">
<div class="fondo"><div class="g1"></div><div class="g2"></div></div>
<header><div class="marca"><img class="nombre" src="{LOGO_RLR_N}" alt="Ricardo López Reyero"></div><div class="serie">{html.escape(s['corto'])}<br>{k:02d} / {total:02d}</div></header>
<main style="--h1:{t}px;--ls:{-t * 0.035:.1f}px;--gap:{gap}px" class="{'compacto' if p.get('compacto') else ''}">
<div class="eyebrow"><span>{html.escape(p['eyebrow'])}</span></div>
<h1 data-a="oy" data-d="0" data-t=".8">{u_html(p['h1'])}</h1>
<div class="grafica">{''.join(bloques)}</div>
<div class="lectura" data-a="oy" data-d="{fin - .4:.2f}" data-t=".8">{u_html(html.escape(p['lectura']))}</div>
<div class="nota" data-a="o" data-d="{fin:.2f}" data-t=".7">{html.escape(p['nota'])}</div>
</main>
<footer><img src="{LOGO}" alt="SuperLeads"><span>{html.escape(PIE[1])}</span></footer>
<script>{JS}</script>
<!-- {_RLR} · {_rev} --></body></html>"""

# ───────────── Chrome por CDP ─────────────  RLR
class Chrome:
    def __init__(self, port=9333):
        self.dir = tempfile.mkdtemp(prefix='rlr_chrome_')
        self.p = subprocess.Popen([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--no-first-run', '--force-device-scale-factor=1',
                                   f'--remote-debugging-port={port}', '--window-size=1080,1920', f'--user-data-dir={self.dir}', 'about:blank'],
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(80):
            try:
                tabs = json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json')); break
            except Exception: time.sleep(.25)
        tab = next(t for t in tabs if t['type'] == 'page')
        self.ws = websocket.create_connection(tab['webSocketDebuggerUrl'], max_size=None, suppress_origin=True); self.i = 0
        self.send('Page.enable'); self.send('Runtime.enable')
        self.send('Emulation.setDeviceMetricsOverride', width=1080, height=1920, deviceScaleFactor=1, mobile=False)

    def send(self, method, **params):
        self.i += 1; self.ws.send(json.dumps(dict(id=self.i, method=method, params=params)))
        while True:
            m = json.loads(self.ws.recv())
            if m.get('id') == self.i:
                if 'error' in m: raise RuntimeError(m['error'])
                return m.get('result', {})

    def abrir(self, url):
        self.send('Page.navigate', url=url)
        while True:
            m = json.loads(self.ws.recv())
            if m.get('method') == 'Page.loadEventFired': break
        self.eval('document.fonts.ready.then(()=>1)', wait=True); time.sleep(.15)

    def eval(self, js, wait=False):
        return self.send('Runtime.evaluate', expression=js, awaitPromise=wait, returnByValue=True).get('result', {}).get('value')

    def foto(self, ruta, fmt='png', calidad=92):
        kw = dict(format=fmt); kw.update(dict(quality=calidad) if fmt == 'jpeg' else {})
        open(ruta, 'wb').write(__import__('base64').b64decode(self.send('Page.captureScreenshot', **kw)['data']))

    def cerrar(self):
        try: self.ws.close()
        except Exception: pass
        self.p.terminate(); shutil.rmtree(self.dir, ignore_errors=True)

def render(p, ch, solo_png=False):
    os.makedirs(HTMLD, exist_ok=True); os.makedirs(SALIDA, exist_ok=True)
    ruta_html = os.path.join(HTMLD, f'{p["n"]:02d}.html'); open(ruta_html, 'w').write(pagina(p))
    ch.abrir('file://' + ruta_html)
    base = f'Dato {p["n"]:02d} · {p["slug"]} · {VERSION} · {SELLO}'
    fondo = ch.eval("document.querySelector('main').getBoundingClientRect().bottom")
    ch.eval('anim(99)'); ch.foto(os.path.join(SALIDA, base + '.png'))
    if not solo_png:
        fr = os.path.join(SCRATCH, 'frames', f'{p["n"]:02d}'); shutil.rmtree(fr, ignore_errors=True); os.makedirs(fr)
        nf = int(FIN_ANIM * FPS); total = int(DUR * FPS)
        for i in range(nf):
            ch.eval(f'anim({i / FPS:.4f})'); ch.foto(os.path.join(fr, f'f_{i:04d}.jpg'), 'jpeg')
        for i in range(nf, total): os.link(os.path.join(fr, f'f_{nf - 1:04d}.jpg'), os.path.join(fr, f'f_{i:04d}.jpg'))
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(fr, 'f_%04d.jpg'), '-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo',
                        '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS), '-c:a', 'aac', '-b:a', '64k', '-shortest',
                        '-movflags', '+faststart', os.path.join(SALIDA, base + '.mp4')], check=True)
    return base, fondo

if __name__ == '__main__':
    pedidos = [int(a) for a in sys.argv[1:]] or [p['n'] for p in P]
    solo_png = os.environ.get('SOLO_PNG') == '1'
    ch = Chrome(); idx = {}
    try:
        for p in P:
            if p['n'] not in pedidos: continue
            base, fondo = render(p, ch, solo_png)
            aviso = '  ⚠ se pasa de 1600' if fondo > 1600 else ''
            print(f'{p["n"]:02d} fondo={fondo:.0f}{aviso} · {base}'); idx[p['n']] = dict(archivo=base, fondo=round(fondo))
    finally:
        ch.cerrar()
    os.makedirs(SCRATCH, exist_ok=True); json.dump(idx, open(os.path.join(SCRATCH, 'ultimo_render.json'), 'w'), ensure_ascii=False, indent=1)
# Ricardo López Reyero · EYE · 181218
