"""PDF de revisión de la tanda 2: qué funcionó, la fórmula y los 21 posts por día con su tarjeta.
HTML → Chrome sin cabeza. Entrega en Desktop/HTML/RLR_marca_personal/X tanda 2 y en Descargas."""
import json, os, html, subprocess, datetime, base64, tempfile, shutil
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
NOMBRE = f'X tanda 2 · 21 posts de educación · v1 · {SELLO}.pdf'
ENTREGA = os.path.expanduser('~/Desktop/HTML/RLR_marca_personal/X tanda 2')
DIAS = {'2026-11-09': 'Lunes 9 nov', '2026-11-10': 'Martes 10 nov', '2026-11-11': 'Miércoles 11 nov', '2026-11-12': 'Jueves 12 nov',
        '2026-11-13': 'Viernes 13 nov', '2026-11-14': 'Sábado 14 nov', '2026-11-15': 'Domingo 15 nov'}
TIPO = {'tarjeta': 'Tarjeta tachada', 'texto': 'Solo texto', 'largo': 'Post largo para guardar'}
EMBUDO = {'alcance': 'Alcance', 'confianza': 'Confianza', 'conversion': 'Conversión'}

POLITICOS = [
    ('Mar 3 nov · 20:30', 'No acabes con la corrupción. Sistematízala.'),
    ('Mié 4 nov · 08:00', 'Propuesta: se acaban las campañas.'),
    ('Jue 5 nov · 08:00', 'Queremos al mejor talento en el gobierno… pagando como si no importara.'),
    ('Jue 5 nov · 20:30', 'Diseñé el gobierno de México desde cero: 552 puestos.'),
    ('Vie 6 nov · 20:30', 'La Constitución la escribieron abogados de otro siglo.'),
    ('Sáb 7 nov · 20:30', 'Hoy: los seleccionamos por sus palabras. Propuesta: por sus resultados.'),
    ('Dom 8 nov · 13:30', 'Ejercicio de estrategia, no de política: ¿y si México uniera al continente?'),
    ('Dom 8 nov · 20:30', 'Así imagino la toma de protesta del primer presidente de Gobierno 2.0.'),
]

CSS = """
@page{size:Letter;margin:16mm 15mm}
body{font-family:'Avenir Next',sans-serif;color:#111;font-size:11.5pt;line-height:1.45}
h1{font-size:24pt;margin:0 0 4px}h2{font-size:15pt;margin:22px 0 8px;border-bottom:3px solid #FFC72C;padding-bottom:4px}
.sub{color:#666;margin-bottom:14px}
table{border-collapse:collapse;width:100%;font-size:10pt;margin:6px 0 10px}td,th{border:1px solid #ddd;padding:6px 7px;vertical-align:top;text-align:left}th{background:#f3f3f3}
.post{border:1px solid #ddd;border-radius:8px;padding:12px 14px;margin:10px 0;page-break-inside:avoid}
.meta{font-size:9.5pt;color:#555;margin-bottom:6px}.meta b{color:#111}
.chip{display:inline-block;background:#111;color:#FFC72C;border-radius:4px;padding:1px 7px;font-size:9pt;margin-right:6px}
.texto{white-space:pre-wrap}
img{width:100%;border-radius:6px;margin-top:8px}
.fuente{font-size:8.5pt;color:#888;margin-top:6px}
.dia{page-break-before:always}
ol li{margin-bottom:3px}
"""


def img64(ruta):
    im = Image.open(ruta).convert('RGB')
    im.thumbnail((1200, 1200))
    tmp = tempfile.mktemp(suffix='.jpg')
    im.save(tmp, quality=80)
    return 'data:image/jpeg;base64,' + base64.b64encode(open(tmp, 'rb').read()).decode()


def main():
    posts = json.load(open(os.path.join(AQUI, 'posts_tanda2.json')))
    h = [f'<!doctype html><meta charset="utf-8"><style>{CSS}</style>']
    h.append('<h1>X · tanda 2: educación a fondo</h1><div class="sub">21 posts para el lunes 9 al domingo 15 de noviembre de 2026 · '
             'tu voz con la fórmula del post del IMSS · nada se programa sin tu visto bueno</div>')
    h.append("""<h2>Lo que funcionó en los primeros 5 días</h2><table><tr><th>Post</th><th>Resultado</th><th>Por qué</th></tr>
<tr><td><b>«El IMSS no está quebrado.»</b> (tarjeta con la palabra tachada)</td><td>7,215 vistas · <b>538 likes</b> · 209 reposts · <b>35 guardados</b></td><td>Niega lo que todos creen, pone un número, revela el mecanismo y cierra con una frase</td></tr>
<tr><td><b>«Todo es mi culpa.»</b> (solo texto)</td><td><b>39 visitas a tu perfil</b> con MX$48 de anuncio: la mejor de las 9 campañas</td><td>Eres tú, sin datos. La gente quiere saber quién lo escribió</td></tr>
<tr><td>Artículos de datos (La gran oportunidad, Educación pública, Mercado privado)</td><td>1,300 a 2,800 lecturas</td><td>El dato serio da confianza, pero despega con anuncio</td></tr></table>
<h2>La fórmula (sale del IMSS)</h2><ol><li><b>Niega lo que todos creen:</b> «Tu colegio no está vacío.»</li><li><b>El número que lo prueba</b>, sencillo y con fuente.</li>
<li><b>El mecanismo oculto:</b> por qué pasa.</li><li><b>El giro de sistema:</b> «No es la persona. Es el sistema.»</li><li><b>Una sola salida:</b> pregunta, frase de una línea o una invitación.</li></ol>
<h2>Lo que cambia con el algoritmo de X</h2><ul>
<li><b>Cero política.</b> Silenciados y reportes hunden la cuenta, y X ya detuvo un anuncio por «contenido político». La educación pública se trata como sistema, con datos.</li>
<li><b>Una idea por post</b>, para que X sepa a qué nicho empujarlo: educación privada en México.</li>
<li><b>Las primeras 48 horas se trabajan:</b> contestar comentarios en la primera hora y, al día siguiente, citar el que más jaló.</li>
<li><b>4 al día, con 3 horas o más entre uno y otro:</b> 8:00 tarjeta (alcance) · 13:30 texto (alcance) · 17:30 serie de datos (ya programada) · 20:30 largo para guardar (confianza). Un solo post de venta a la semana.</li>
<li><b>Cada 7 días, 5 posts de tendencias</b> sobre lo que se esté moviendo en educación en México, con tu ángulo y tus datos.</li></ul>""")
    h.append('<h2>Aún programados con tema político (salen del 3 al 8 de noviembre)</h2><table><tr><th>Cuándo</th><th>Post</th></tr>'
             + ''.join(f'<tr><td>{c}</td><td>{html.escape(t)}</td></tr>' for c, t in POLITICOS)
             + '</table><div class="sub">Propuesta: pasarlos a borradores (no se borran) y poner en esos mismos horarios los primeros posts de esta tanda. '
               'El primero sale mañana martes a las 20:30.</div>')
    dia = None
    for p in posts:
        if p['fecha'] != dia:
            dia = p['fecha']
            h.append(f'<h2 class="dia">{DIAS[dia]}</h2>')
        vis = f'<img src="{img64(os.path.join(AQUI, p["visual"]))}">' if p.get('visual') else ''
        h.append(f'<div class="post"><div class="meta"><span class="chip">{p["hora"]}</span><b>{TIPO[p["tipo"]]}</b> · {EMBUDO[p["embudo"]]} · '
                 f'{p["caracteres"]} caracteres</div><div class="texto">{html.escape(p["texto"])}</div>{vis}'
                 f'<div class="fuente">Fuente: {html.escape(p["fuente"])}</div></div>')
    tmp = tempfile.mkdtemp()
    f = os.path.join(tmp, 'r.html')
    open(f, 'w').write(''.join(h))
    os.makedirs(ENTREGA, exist_ok=True)
    out = os.path.join(ENTREGA, NOMBRE)
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={out}', 'file://' + f],
                   check=True, capture_output=True)
    shutil.copy(out, os.path.expanduser('~/Downloads/'))
    print(out)


if __name__ == '__main__':
    main()
