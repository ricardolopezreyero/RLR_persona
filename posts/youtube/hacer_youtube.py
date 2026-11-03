"""Publicaciones de comunidad de YouTube (3–20 nov 2026) rehechas con lo aprendido en X.

Sustituyen, en el mismo lugar y a la misma hora, las 18 publicaciones de imagen que estaban programadas
(frases suaves tipo «el seguimiento también es una forma de decir aquí nos importas»). Los videos y Shorts no se tocan.

Lo que se trae de X (aprendizajes/X-2026-11-03.md):
- la fórmula del IMSS: niega la creencia, da el número, muestra el mecanismo, culpa al sistema, deja una sola salida;
- la tarjeta tachada; educación a fondo, cero política; fuente en cada dato.
Lo que es propio de YouTube:
- tarjeta cuadrada 1080×1080 en la paleta de SuperLeads (navy, verde, Plus Jakarta Sans), con el nombre de Ricardo arriba
  y el logo de SuperLeads abajo, como el resto de las piezas del canal;
- texto completo, con la fuente escrita y una pregunta al final: en YouTube las publicaciones viven de los comentarios;
- 5–7 nov: CIMEDU (Congreso Internacional de Marketing Educativo, Anáhuac Norte), con mucha gente de colegios entrando
  desde la Ciudad de México. Esos días el texto abre con el congreso y la hora pasa a 7:30, antes de las primeras charlas.
Escribe publicaciones_youtube.json y las tarjetas en tarjetas/."""
import json, os, html, subprocess, datetime, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
EST = os.path.join(AQUI, '..', 'estadisticas')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
NOMBRE = 'file://' + os.path.join(EST, 'rlr_nombre.png')
LOGO = open(os.path.join(EST, 'logo_blanco.svg')).read()
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.join(AQUI, 'tarjetas')
TANDA = {p['n']: p for p in json.load(open(os.path.join(AQUI, '..', 'tanda2', 'posts_tanda2.json')))}

SUSCRIBE = 'Cada día publico un dato de admisiones con su fuente. Si diriges un colegio, suscríbete.'
TAGS = '#admisiones #colegiosprivados #educación'
TAGS_CIMEDU = '#CIMEDU2026 #marketingeducativo #admisiones'
CIMEDU_LIGA = 'Si vas a CIMEDU: fechas, sede y hoteles en https://cimedu.superleads.mx'
OBS = 'Todos los datos, con fuente: https://observatorio.superleads.mx'

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1080px;background:#001240;color:#fff;font-family:'Plus Jakarta Sans',sans-serif;
 position:relative;overflow:hidden;padding:0 80px}
.fondo{position:absolute;inset:0;background:radial-gradient(circle at 85% 10%,rgba(42,137,251,.22),transparent 55%)}
.nombre{position:absolute;left:80px;top:72px;height:44px}
.caja{position:absolute;left:80px;right:80px;top:52%;transform:translateY(-50%)}
.etq{display:inline-block;color:#56EF9F;font-size:26px;font-weight:700;letter-spacing:1.5px;border:.5px solid rgba(86,239,159,.6);
 border-radius:999px;padding:9px 18px}
.arriba{font-size:var(--t);font-weight:800;line-height:1.08;margin-top:40px;letter-spacing:-1px}
.tachado{font-size:var(--t);font-weight:800;line-height:1.1;color:#7C8BB3;position:relative;display:inline-block;margin-top:6px;letter-spacing:-1px}
.tachado:after{content:'';position:absolute;left:-8px;right:-8px;top:54%;height:10px;background:#FF4D5E;transform:rotate(-1.2deg);border-radius:4px}
.resp{font-size:var(--t);font-weight:800;line-height:1.08;color:#56EF9F;margin-top:10px;letter-spacing:-1px}
.titulo{font-size:72px;font-weight:800;line-height:1.1;margin-top:36px;letter-spacing:-1px}
ol{list-style:none;margin-top:34px}
li{display:flex;gap:22px;align-items:flex-start;font-size:36px;font-weight:600;line-height:1.3;margin-bottom:18px;color:#E8EEFF}
li b{flex:0 0 46px;height:46px;border-radius:50%;background:#56EF9F;color:#001240;font-size:24px;font-weight:800;
 display:flex;align-items:center;justify-content:center;margin-top:-2px}
.cita{font-size:62px;font-weight:700;line-height:1.2;margin-top:40px;color:#E8EEFF}
.pie{position:absolute;left:80px;right:330px;bottom:72px;font-size:26px;line-height:1.35;color:#9FB0D9}
.logo{position:absolute;right:80px;bottom:66px;width:202px}
.logo svg{width:202px;height:auto}
"""


def tamano(t):
    largo = max(len(t.get('arriba', '')), len(t.get('tachado', '')), len(t.get('respuesta', '')))
    return 102 if largo <= 18 else 98 if largo <= 24 else 86 if largo <= 30 else 74


def html_tarjeta(t):
    e = html.escape
    if t['tipo'] == 'tachado':
        tach = f'<div><span class="tachado">{e(t["tachado"])}</span></div>' if t.get('tachado') else ''
        cuerpo = (f'<div class="arriba">{e(t["arriba"])}</div>{tach}<div class="resp">{e(t["respuesta"])}</div>')
    elif t['tipo'] == 'lista':
        items = ''.join(f'<li><b>{i}</b><span>{e(x)}</span></li>' for i, x in enumerate(t['items'], 1))
        cuerpo = f'<div class="titulo">{e(t["titulo"])}</div><ol>{items}</ol>'
    else:  # cita
        cuerpo = f'<div class="cita">«{e(t["cita"])}»</div><div class="resp" style="--t:66px">{e(t["respuesta"])}</div>'
    return f"""<!doctype html><meta charset="utf-8"><style>{CSS}</style>
<body style="--t:{tamano(t)}px"><div class="fondo"></div><img class="nombre" src="{NOMBRE}">
<div class="caja"><span class="etq">{e(t['etiqueta'])}</span>{cuerpo}</div>
<div class="pie">{e(t['pie'])}</div><div class="logo">{LOGO}</div></body>"""


def T(n):
    return TANDA[n]['texto']


# fecha, hora, origen, tarjeta, texto. El texto de X va completo; se le agregan apertura (CIMEDU), fuente, pregunta y cierre.
P = [
    dict(fecha='2026-11-03', hora='09:00', origen='X tanda 2 · post 01',
         tarjeta=dict(tipo='tachado', **{k: TANDA[1]['tarjeta'][k] for k in ('etiqueta', 'arriba', 'tachado', 'respuesta', 'pie')}),
         texto=T(1) + '\n\nFuente: 98 Rayos X de Inscripciones con dueños y directores de colegios privados (corte octubre 2026) y el estudio de comprador secreto de 1,000 consultas al sector.\n\n' + OBS),
    dict(fecha='2026-11-04', hora='09:00', origen='X tanda 2 · post 04 · víspera de CIMEDU',
         tarjeta=dict(tipo='tachado', **{k: TANDA[4]['tarjeta'][k] for k in ('etiqueta', 'arriba', 'tachado', 'respuesta', 'pie')}),
         texto='Mañana empieza CIMEDU, el Congreso Internacional de Marketing Educativo. Van a ser tres días hablando de cómo atraer más familias. Antes de llegar, un dato incómodo:\n\n'
               + T(4) + '\n\nFuente: corte de 102 Rayos X de Inscripciones, octubre 2026.\n\n' + CIMEDU_LIGA, cimedu=True),
    dict(fecha='2026-11-05', hora='07:30', origen='X tanda 2 · post 13 · CIMEDU día 1',
         tarjeta=dict(tipo='tachado', **{k: TANDA[13]['tarjeta'][k] for k in ('etiqueta', 'arriba', 'tachado', 'respuesta', 'pie')}),
         texto='Hoy arranca CIMEDU. Se va a hablar mucho de cómo traer familias nuevas. Yo empezaría por otra pregunta: ¿por qué se van las que ya llegaron?\n\n'
               + T(13) + '\n\nFuente: corte de 102 Rayos X de Inscripciones, octubre 2026.\n\nCuéntame en los comentarios: ¿precio o seguimiento?', cimedu=True),
    dict(fecha='2026-11-06', hora='07:30', origen='X tanda 2 · post 10 · CIMEDU día 2',
         tarjeta=dict(tipo='tachado', **{k: TANDA[10]['tarjeta'][k] for k in ('etiqueta', 'arriba', 'tachado', 'respuesta', 'pie')}),
         texto='Segundo día de CIMEDU. Si hoy alguien te vende una herramienta para conseguir más prospectos, haz primero esta cuenta:\n\n'
               + T(10) + '\n\n¿Cuántos «ahorita le contesto» tiene hoy el WhatsApp de tu colegio?', cimedu=True),
    dict(fecha='2026-11-07', hora='07:30', origen='X tanda 2 · post 19 · CIMEDU día 3',
         tarjeta=dict(tipo='tachado', etiqueta='102 RAYOS X · CONVERSIÓN', arriba='De cada 100 familias que preguntan,', tachado='',
                      respuesta='2 se inscriben.', pie=TANDA[19]['tarjeta']['pie']),
         texto='Último día de CIMEDU. Si te llevas una sola idea del congreso a tu colegio, que sea esta:\n\n'
               + T(19) + '\n\nFuente: corte de 102 Rayos X de Inscripciones, octubre 2026.\n\n¿Sabes cuál es la conversión de tu colegio? Escríbela en los comentarios, aunque sea aproximada.', cimedu=True),
    dict(fecha='2026-11-08', hora='09:00', origen='Anuncio de seguidores S·02 de X',
         tarjeta=dict(tipo='tachado', etiqueta='PARA QUIEN DIRIGE UN COLEGIO', arriba='Admisiones no es un área', tachado='administrativa.',
                      respuesta='Es el área comercial.', pie='Colegio mediano: 1.1 personas en admisiones · 48 % sin plan de compensación'),
         texto='Tu área de admisiones no es administrativa. Es comercial.\n\nEl colegio mediano tiene 1.1 personas en admisiones, y 48 % no tiene plan de compensación para su equipo.\n\nAsí no se llena un colegio. Así se contesta cuando se puede.\n\nUna escuela le pide a admisiones lo que le pediría a un equipo comercial, pero le paga y la mide como a una oficina de trámites.\n\nFuente: corte de 102 Rayos X de Inscripciones, octubre 2026.\n\n¿Cuántas personas tiene admisiones en tu colegio, y cómo se les paga?'),
    dict(fecha='2026-11-09', hora='09:00', origen='Anuncio de seguidores S·03 de X',
         tarjeta=dict(tipo='tachado', etiqueta='ADMISIONES · PRIMERA RESPUESTA', arriba='No se fue con la', tachado='competencia.',
                      respuesta='Se fue con el que contestó primero.', pie='78 % le compra al primero que responde · solo 7 % contesta en 5 minutos'),
         texto='La familia no se fue con la competencia. Se fue con el que contestó primero.\n\n78 % le compra al primero que responde, y solo 7 % de las organizaciones contesta en 5 minutos.\n\nNo perdiste contra un colegio mejor. Perdiste contra un colegio más rápido.\n\nFuente: estudios de MIT, Harvard Business Review y Velocify sobre tiempo de respuesta (serie «La realidad de la educación»).\n\nHaz la prueba hoy: escríbele a tu propio colegio como si fueras una familia y cronometra la respuesta.'),
    dict(fecha='2026-11-10', hora='09:00', origen='X tanda 2 · post 03',
         tarjeta=dict(tipo='lista', etiqueta='102 RAYOS X · 69 CIUDADES', titulo='5 cosas que nadie me había dicho',
                      items=['La escuela mediana opera al 46 %.', '40 % de las familias que van a la cita se inscribe.',
                             'Un alumno vale $144,000 MXN en toda su estancia.', '70 % no tiene programa de recomendados.',
                             '62 % culpa al precio. Solo 38 % admite que no dio seguimiento.'],
                      pie='Corte Rayos X de Inscripciones · octubre 2026'),
         texto=T(3) + '\n\nFuente: corte de 102 Rayos X de Inscripciones, octubre 2026.\n\n¿Cuál de las cinco se parece más a tu colegio?'),
    dict(fecha='2026-11-11', hora='09:00', origen='X tanda 2 · post 11 (personal)',
         tarjeta=dict(tipo='cita', etiqueta='22 DE FEBRERO DE 2022 · 50 MINUTOS',
                      cita='¿A qué nicho me enfoco que tenga la máxima rentabilidad y la máxima longevidad?',
                      respuesta='Salió educación. 1,723 días después, sigo aquí.', pie='Un colegio lleno es una ciudad con más gente preparada.'),
         texto=T(11).replace('Si tienes un colegio, sígueme.', 'Si tienes un colegio, suscríbete.')),
    dict(fecha='2026-11-12', hora='09:00', origen='X tanda 2 · post 18',
         tarjeta=dict(tipo='lista', etiqueta='RAYOS X DE INSCRIPCIONES', titulo='Las 3 preguntas que le hago a todo dueño de colegio',
                      items=['¿Cuántos lugares vacíos tienes hoy?', '¿Cuántas familias te preguntan al día?', '¿Cuántas de esas terminan inscritas?'],
                      pie='Si no las contestas sin abrir un Excel, ese es el primer problema.'),
         texto=T(18) + '\n\nContesta las tres en los comentarios. Sin nombre del colegio, solo los números.'),
    dict(fecha='2026-11-13', hora='09:00', origen='X tanda 2 · post 06',
         tarjeta=dict(tipo='tachado', etiqueta='LA REALIDAD DE LA EDUCACIÓN', arriba='Las familias no deciden', tachado='a las 11 de la mañana.',
                      respuesta='Deciden a las 11 de la noche.', pie='93 % conectada entre 9 y 12 de la noche · 78 % le compra al primero que responde'),
         texto=T(6) + '\n\nFuente: serie «La realidad de la educación», capítulos 13 y 14.'),
    dict(fecha='2026-11-14', hora='09:00', origen='X tanda 2 · post 02 («Todo es mi culpa»)',
         tarjeta=dict(tipo='tachado', etiqueta='LA FRASE QUE MÁS ME HA SERVIDO', arriba='Si tu colegio está al 46 %, no es', tachado='el mercado.',
                      respuesta='Es tu culpa. Y es la mejor noticia.', pie='La culpa total es la libertad total.'),
         texto=T(2) + '\n\n46 % es la ocupación del colegio mediano en el corte de 102 Rayos X de Inscripciones (octubre 2026).\n\n¿De quién es la culpa en tu colegio?'),
    dict(fecha='2026-11-15', hora='09:00', origen='X tanda 2 · post 12',
         tarjeta=dict(tipo='tachado', etiqueta='BECAS', arriba='Una beca sin estrategia no es', tachado='una beca.',
                      respuesta='Es un descuento que nadie te pidió.', pie='68 % de las escuelas privadas da becas · la mediana tiene 40 % de alumnos becados'),
         texto=T(12) + '\n\nFuente: corte de 102 Rayos X de Inscripciones, octubre 2026.'),
    dict(fecha='2026-11-16', hora='09:00', origen='X tanda 2 · post 15',
         tarjeta=dict(tipo='tachado', etiqueta='RECOMENDACIÓN', arriba='Tus familias no te recomiendan porque', tachado='no quieren.',
                      respuesta='Nadie les dice cómo.', pie='40 % de los alumnos llega por recomendación · 70 % de los colegios no tiene programa'),
         texto=T(15) + '\n\nFuente: corte de 102 Rayos X de Inscripciones, octubre 2026.'),
    dict(fecha='2026-11-17', hora='09:00', origen='X tanda 2 · post 07',
         tarjeta=dict(tipo='tachado', **{k: TANDA[7]['tarjeta'][k] for k in ('etiqueta', 'arriba', 'tachado', 'respuesta', 'pie')}),
         texto=T(7) + '\n\nFuente: ENOE (INEGI) y OCDE, en la serie «La realidad de la educación».\n\n' + OBS),
    dict(fecha='2026-11-18', hora='09:00', origen='X tanda 2 · post 16',
         tarjeta=dict(tipo='tachado', **{k: TANDA[16]['tarjeta'][k] for k in ('etiqueta', 'arriba', 'tachado', 'respuesta', 'pie')}),
         texto=T(16) + '\n\nFuente: OCDE, PISA 2022, e IMCO.\n\n' + OBS),
    dict(fecha='2026-11-19', hora='09:00', origen='X tanda 2 · post 09',
         tarjeta=dict(tipo='tachado', etiqueta='PERÚ VS. MÉXICO', arriba='En México no falta', tachado='dinero.',
                      respuesta='Falta explicar por qué vale la pena.', pie='Perú: 10 % puede pagar privada y 26 % está en una · México: 35 % puede y 10 % está'),
         texto=T(9) + '\n\nFuente: serie «La realidad de la educación», capítulo 24.\n\n' + OBS),
    dict(fecha='2026-11-20', hora='09:00', origen='X tanda 2 · post 21 (invitación al Rayos X)',
         tarjeta=dict(tipo='lista', etiqueta='RAYOS X DE INSCRIPCIONES', titulo='102 radiografías en 69 ciudades. Una sesión para tu colegio.',
                      items=['Ocupación', 'Prospectos', 'Conversión', 'Valor de un alumno'],
                      pie='Te llevas un PDF con tus números más importantes.'),
         texto=T(21).replace('https://superleads.mx/rayos_x', 'https://superleads.mx/rayos_x?utm_source=youtube&utm_medium=comunidad&utm_campaign=yt-posts-nov')),
]


def texto_final(p):
    t = p['texto']
    if 'superleads.mx/rayos_x' not in t:
        t += '\n\n' + SUSCRIBE
    return t + '\n\n' + (TAGS_CIMEDU if p.get('cimedu') else TAGS)


def main():
    os.makedirs(SALIDA, exist_ok=True)
    tmp = tempfile.mkdtemp()
    out = []
    for k, p in enumerate(P, 1):
        f = os.path.join(tmp, f'{k}.html')
        open(f, 'w').write(html_tarjeta(p['tarjeta']))
        tit = p['tarjeta'].get('respuesta') or p['tarjeta'].get('titulo')
        img = os.path.join(SALIDA, f"YT {k:02d} · {p['fecha'][5:]} · {tit.rstrip('.')} · v1 · {SELLO}.png".replace('/', '-').replace('$', ''))
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1080,1080', f'--screenshot={img}', 'file://' + f], check=True, capture_output=True)
        txt = texto_final(p)
        assert len(txt) <= 5000, (k, len(txt))
        out.append(dict(yt=k, fecha=p['fecha'], hora=p['hora'], origen=p['origen'], texto=txt,
                        imagen=os.path.relpath(img, AQUI), archivo=img, estado='por aplicar'))
        print(k, p['fecha'], p['hora'], len(txt), os.path.basename(img))
    json.dump(out, open(os.path.join(AQUI, 'publicaciones_youtube.json'), 'w'), ensure_ascii=False, indent=1)


if __name__ == '__main__':
    main()
