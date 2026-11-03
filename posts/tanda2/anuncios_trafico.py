"""Campaña de tráfico a superleads.mx con los 21 posts de la tanda 2 (aprobada por Ricardo el 2-nov-2026, MX$100/día).

Un anuncio solo-promoción por post: texto corto (X limita a 280 caracteres), tarjeta 1.91:1 (formato de liga
de X) con el diseño tachado y la liga a superleads.mx con UTM para saber qué post trae visitas.
Escribe anuncios_trafico.json y las imágenes en anuncios/."""
import json, os, html, subprocess, datetime, tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
LOGO = open(os.path.join(AQUI, '..', 'estadisticas', 'logo_blanco.svg')).read()
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.join(AQUI, 'anuncios')
TITULO = 'SuperLeads · admisiones para colegios privados'

# n del post en posts_tanda2.json → (texto del anuncio, tarjeta: etiqueta, arriba, tachado, respuesta, pie)
A = {
    1: ("Tu colegio no está vacío. Está mal atendido.\n\nLa escuela privada mediana opera al 46 %. Y 44 de cada 100 consultas a colegios nunca reciben respuesta.\n\nNo faltan familias. Falta quien les conteste.",
        None),
    2: ("Si tu colegio está al 46 %, es tu culpa.\n\nY es la mejor noticia: si fuera culpa de la economía, no podrías hacer nada. Si es tuya, lo arreglas el lunes.\n\nLa culpa total es la libertad total. También para un director.",
        ('PARA DUEÑOS DE COLEGIO', 'Si tu colegio está al 46 %,', '', 'es tu culpa.', 'Y es la mejor noticia: lo arreglas el lunes.')),
    3: ("Hicimos 102 Rayos X con dueños de escuelas privadas en 69 ciudades:\n\n· Operan al 46 %\n· 40 % de quienes van a la cita se inscribe\n· Un alumno vale $144,000 MXN\n· 70 % no tiene programa de recomendados\n\nNo es el mercado. Es el sistema.",
        ('102 RAYOS X · 69 CIUDADES', 'Lo que nadie te dice', '', 'de la escuela privada.', 'Ocupación 46 % · cierre en cita 40 % · un alumno vale $144,000 MXN')),
    4: ("Tu colegio no necesita más publicidad. Necesita contestar.\n\nEl colegio mediano paga $1,381 MXN por alumno inscrito: es su gasto más rentable. Lo que falla es el camino: solo 2.4 % de los prospectos termina inscrito.",
        None),
    5: ("Opinión impopular: con menos de 900 alumnos no hay pretexto para no tener lista de espera.\n\n13.4 millones de hogares en México pueden pagar un colegio privado. Tu ciudad tiene las familias.\n\nLa lista de espera no se anuncia. Se construye.",
        ('OPINIÓN IMPOPULAR', 'Con menos de 900 alumnos,', 'lista de espera imposible.', 'No hay pretexto.', '13.4 millones de hogares en México pueden pagar colegio privado.')),
    6: ("El colegio cierra a las 3 de la tarde. Las familias deciden a las 11 de la noche.\n\n93 % está conectada entre las 9 y la medianoche, y 78 % le compra al primero que responde.\n\n¿Quién contesta en tu colegio a las 11 pm?",
        ('EL HORARIO QUE NADIE ATIENDE', 'El colegio cierra a las 3.', '', 'La familia decide a las 11 pm.', '93 % conectada de 9 a 12 de la noche · 78 % le compra al primero que responde')),
    7: ("El problema de la educación en México no es el maestro.\n\nEl docente promedio gana $7,890 MXN al mes y México invierte $2,933 USD por alumno: último lugar de la OCDE.\n\nNo es la persona. Es el sistema que la puso ahí.",
        None),
    8: ("Pregunta para dueños de colegio: ¿cuánto vale un alumno?\n\nSi dijiste «una colegiatura», dijiste mal. El alumno mediano vale $144,000 MXN en toda su estancia.\n\nEse es el tamaño de cada WhatsApp que se queda en visto.",
        ('PREGUNTA PARA DUEÑOS DE COLEGIO', '¿Cuánto vale un alumno?', 'Una colegiatura.', '$144,000 MXN.', 'Valor de vida mediano de un alumno · 97 Rayos X')),
    9: ("Perú: 10 % de los hogares puede pagar colegio privado y 26 % de los alumnos está en uno.\n\nMéxico: 35 % puede pagarlo y solo 10 % está en uno.\n\nNo falta dinero. Falta que cada colegio explique por qué vale la pena.",
        ('MÉXICO VS. PERÚ', '35 % puede pagarlo.', '', 'Solo 10 % lo hace.', 'Perú: 10 % puede pagar colegio privado y 26 % inscribe.')),
    10: ("Un WhatsApp sin contestar no cuesta nada. Eso creen casi todos.\n\nColegiatura de $4,500 MXN, 6 años de permanencia y un hermano: unos $450,000 MXN por familia.\n\nEse es el precio de cada «ahorita le contesto».",
         None),
    11: ("El 22 de febrero de 2022 me pregunté a qué nicho dedicarme con la máxima rentabilidad y longevidad. Salió educación.\n\nUn colegio lleno no es solo un negocio lleno: es una ciudad con más gente preparada.\n\nPor eso escribo de esto todos los días.",
         ('POR QUÉ EDUCACIÓN', 'Un colegio lleno', '', 'es una ciudad más preparada.', 'Escribo de esto todos los días desde el 22 de febrero de 2022.')),
    12: ("68 % de las escuelas privadas da becas y la mediana tiene 40 % de alumnos becados.\n\nUna beca con estrategia atrae al alumno que quieres. Sin estrategia, es un descuento que nadie te pidió.\n\n¿Tu beca atrae o solo retiene por miedo?",
         ('BECAS', 'Una beca sin estrategia', 'es generosidad.', 'Es un descuento.', '68 % da becas · la mediana tiene 40 % de alumnos becados')),
    13: ("No se fueron por el precio. Se fueron por el silencio.\n\n62 % de los directores culpa al precio. Pero 40 % de las familias que llegan a la cita se inscribe, al mismo precio.\n\nEl precio es la explicación cómoda.",
         None),
    14: ("Tu colegio no compite contra el colegio de enfrente.\n\nCompite contra la escuela pública gratuita, donde están 9 de cada 10 niños del país. Y contra el WhatsApp que nadie contestó.\n\nEse es tu mercado.",
         ('TU MERCADO', 'Tu competencia no es', 'el colegio de enfrente.', 'Es la pública y el silencio.', '9 de cada 10 alumnos en México estudian en la escuela pública.')),
    15: ("40 % de los alumnos de la escuela privada llega por recomendación.\n\nY 70 % de los colegios no tiene ningún programa de recomendados.\n\nTus familias quieren recomendarte. Nadie les dice cómo.",
         ('RECOMENDADOS', 'El canal más barato', '', 'no cuesta un peso.', '40 % llega por recomendación · 70 % no tiene programa')),
    16: ("No es un problema de los niños.\n\nEn PISA, México quedó 35 de 37 y 2 de cada 3 alumnos de 15 años no alcanzan el nivel básico de matemáticas.\n\nEs el sistema que los forma. Si cambias el proceso, cambias los resultados.",
         None),
    17: ("Si estuvieras viendo tu colegio en la pantalla de un cine, ¿qué te estaría gritando la audiencia?\n\nYo creo que algo así:\n\n«¡Contesta ese mensaje!»",
         ('LA PELÍCULA DE TU COLEGIO', 'Si vieras tu colegio en un cine,', '', '«¡Contesta ese mensaje!»', '¿Qué te gritaría la audiencia?')),
    18: ("Las 3 preguntas que le hago a todo dueño de colegio:\n\n1. ¿Cuántos lugares vacíos tienes?\n2. ¿Cuántas familias preguntan al día?\n3. ¿Cuántas se inscriben?\n\nSi no las sabes sin abrir un Excel, ese es el primer problema.",
         ('RAYOS X DE INSCRIPCIONES', '3 preguntas', '', 'para todo dueño de colegio.', 'Lugares vacíos · familias al día · familias inscritas')),
    19: ("De cada 100 familias que preguntan por un colegio privado, 2 se inscriben.\n\nCon las mismas 100, subir un punto vale $109,500 MXN al año para el colegio mediano.\n\nMás publicidad es lo último. Primero, el proceso.",
         None),
    20: ("Hay 3 tipos de colegios:\n\n1. Los que esperan inscripciones.\n2. Los que las compran.\n3. Los que las construyen.\n\nLos primeros culpan al año. Los segundos, al anuncio. Los terceros tienen lista de espera.",
         ('3 TIPOS DE COLEGIOS', 'Esperan, compran', '', 'o construyen.', 'Solo los que construyen tienen lista de espera.')),
    21: ("Hicimos 102 Rayos X de Inscripciones con dueños y directores en 69 ciudades.\n\nEn una sesión acomodamos los números de tu colegio como tienen que estar y te llevas un PDF. Por ahora, sin costo.",
         ('RAYOS X DE INSCRIPCIONES', 'Tu colegio,', '', 'en números.', '102 diagnósticos en 69 ciudades · por ahora sin costo')),
}

CSS = """*{margin:0;padding:0;box-sizing:border-box}
body{width:1600px;height:838px;background:#0D0D0D;color:#F5F5F0;font-family:'Avenir Next',sans-serif;padding:80px 100px 0;position:relative;overflow:hidden}
.barra{width:80px;height:8px;background:#FFC72C;margin-bottom:22px}
.etq{color:#FFC72C;font-size:27px;font-weight:600}
.arriba{font-size:var(--t);font-weight:800;line-height:1.1;margin-top:34px}
.tachado{font-size:var(--t);font-weight:800;line-height:1.15;color:#8A8A85;position:relative;display:inline-block;margin-top:6px}
.tachado:after{content:'';position:absolute;left:-12px;right:-12px;top:52%;height:11px;background:#E5242B;transform:rotate(-1deg)}
.resp{font-size:var(--t);font-weight:800;line-height:1.1;color:#FFC72C;margin-top:8px}
.pie{font-size:31px;color:#8A8A85;margin-top:26px;line-height:1.25;max-width:1400px}
.firma{position:absolute;left:100px;bottom:52px;font-size:29px;font-weight:600}
.logo{position:absolute;right:100px;bottom:48px;width:240px}.logo svg{width:240px;height:auto}"""


def tamano(arriba, tach, resp):
    largo = max(len(arriba), len(tach), len(resp))
    return 112 if largo <= 18 else 100 if largo <= 23 else 86 if largo <= 28 else 74


def tarjeta(etq, arriba, tach, resp, pie):
    t = f'<div><span class="tachado">{html.escape(tach)}</span></div>' if tach else ''
    return (f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><body style="--t:{tamano(arriba, tach, resp)}px">'
            f'<div class="barra"></div><div class="etq">{html.escape(etq)}</div><div class="arriba">{html.escape(arriba)}</div>{t}'
            f'<div class="resp">{html.escape(resp)}</div><div class="pie">{html.escape(pie)}</div>'
            f'<div class="firma">Ing. Ricardo López Reyero · Torreón</div><div class="logo">{LOGO}</div></body>')


def main():
    os.makedirs(SALIDA, exist_ok=True)
    posts = {p['n']: p for p in json.load(open(os.path.join(AQUI, 'posts_tanda2.json')))}
    tmp = tempfile.mkdtemp()
    out = []
    for n in range(1, 22):
        texto, spec = A[n]
        assert len(texto) <= 280, (n, len(texto))
        if spec is None:
            t = posts[n]['tarjeta']
            spec = (t['etiqueta'], t['arriba'], t['tachado'], t['respuesta'], t['pie'])
        f = os.path.join(tmp, f'{n}.html')
        open(f, 'w').write(tarjeta(*spec))
        img = os.path.join(SALIDA, f'Anuncio {n:02d} · {spec[3].rstrip(".»").lstrip("«")[:40]} · v1 · {SELLO}.png'.replace('$', '').replace('/', '-'))
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1600,838', f'--screenshot={img}', 'file://' + f], check=True, capture_output=True)
        url = 'https://superleads.mx/rayos_x' if n == 21 else 'https://superleads.mx/'
        url += f'?utm_source=x&utm_medium=paid&utm_campaign=x-trafico-tanda2&utm_content=post-{n:02d}'
        out.append({'n': n, 'nombre': f'T2 · {n:02d} · {texto.split(chr(10))[0][:45]}', 'texto': texto, 'caracteres': len(texto),
                    'url': url, 'titulo': TITULO, 'imagen': img})
    json.dump(out, open(os.path.join(AQUI, 'anuncios_trafico.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(out), max(a['caracteres'] for a in out))


if __name__ == '__main__':
    main()
