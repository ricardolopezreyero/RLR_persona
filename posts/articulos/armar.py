"""Tres artículos largos para LinkedIn (formato «artículo», no post), escritos por Ricardo, citables, con las gráficas de las
dos series re-renderizadas en formato horizontal 1600×900: título arriba del gráfico; abajo el nombre de Ricardo a la
izquierda y SuperLeads a la derecha. Nada se publica desde aquí.
Uso: python3 armar.py          → salida/Artículo N · slug/ (texto .md y .txt, imagenes/) + copia en ~/Downloads/LinkedIn Artículos/
Ricardo López Reyero · RLR"""
import os, sys, json, glob, datetime, shutil, html, re

AQUI = os.path.dirname(os.path.abspath(__file__)); POSTS = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(POSTS, 'estadisticas')); sys.path.insert(0, os.path.join(POSTS, 'rayosx_corte'))
import render, serie as S
sys.argv = ['piezas.py', '2026-10-29']; import piezas as X  # noqa: E402

SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M'); VERSION = 'v1'
SALIDA = os.path.join(AQUI, 'salida'); HTMLD = os.path.join(AQUI, 'html'); DESCARGAS = os.path.expanduser('~/Downloads/LinkedIn Artículos')
PIEZA = {('R', p['n']): p for p in S.P}; PIEZA.update({('X', p['n']): p for p in X.P})
FIRMA = 'Viernes 30 de octubre de 2026, 9:24 am · Torreón, Coahuila, México · 19°.'
FIRMA_NOMBRE = ['Ing. Ricardo López Reyero', 'Founder Comercial · SuperLeads', 'ricardo@superleads.mx']
CORREO = 'ricardo@superleads.mx'
AUTOR = 'Ricardo López Reyero'

# ───────────── la lámina de artículo: 1600×900, título arriba, nombre y SuperLeads abajo ─────────────
CSS_ART = """
html,body{width:1600px;height:900px}
header{display:none}
main.art{position:absolute;top:58px;left:90px;right:90px;transform:none}
main.art .eyebrow{margin-bottom:16px} main.art .eyebrow span{font-size:21px}
main.art h1{font-size:56px;line-height:1.08;letter-spacing:-1.8px;margin:0;max-width:1400px}
main.art .grafica{position:relative;left:50%;margin-top:26px;display:inline-flex;gap:44px;align-items:flex-start;transform-origin:50% 0;transform:translateX(-50%)}
main.art .grafica>*{width:920px;flex:none} main.art .grafica>*+*{margin-top:0}
main.art .grafica.col{flex-direction:column;gap:30px}
.nota.art{position:absolute;left:90px;right:90px;bottom:118px;margin:0;font-size:18px;line-height:1.35;color:var(--t3)}
footer.art{position:absolute;left:90px;right:90px;bottom:38px;border-top:.5px solid rgba(255,255,255,.14);padding-top:22px;display:flex;justify-content:space-between;align-items:center}
footer.art .nombre{height:44px;width:auto;display:block} footer.art .sl{width:168px;height:auto;display:block}
"""
JS_FIT = """
function medir(){const g=document.getElementById('g');const n=document.querySelector('.nota.art');g.style.transform='translateX(-50%)';const top=g.getBoundingClientRect().top;
const availH=n.getBoundingClientRect().top-18-top;const availW=1420;const rs=[...g.children].map(c=>c.getBoundingClientRect());
const w=Math.max(...rs.map(r=>r.right))-Math.min(...rs.map(r=>r.left)),h=Math.max(...rs.map(r=>r.bottom))-top;return Math.min(1.5,availH/h,availW/w);}
function fit(){const g=document.getElementById('g');g.classList.remove('col');const sFila=medir();let s=sFila;
if(g.children.length>1){g.classList.add('col');const sCol=medir();if(sCol>sFila*1.08){s=sCol;}else{g.classList.remove('col');s=medir();}}
g.style.transform='translateX(-50%) scale('+s.toFixed(4)+')';return s;}
"""
def lamina_articulo(p):
    gs = p['grafica'] if isinstance(p['grafica'], list) else [p['grafica']]
    r = 0.5; bloques = []
    for g in gs:
        h, r = render.GRAF[g['tipo']](g, r); bloques.append(h)
    nota = p.get('nota')
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{html.escape(p['slug'])}</title>
<style>{render.CSS}{CSS_ART}</style></head><body data-author="RLR">
<div class="fondo"><div class="g1"></div><div class="g2"></div></div>
<main class="art"><div class="eyebrow"><span>{html.escape(p['eyebrow'])}</span></div>
<h1>{render.u_html(p['h1'])}</h1>
<div class="grafica" id="g">{''.join(bloques)}</div></main>
<div class="nota art">{html.escape(nota)}</div>
<footer class="art"><img class="nombre" src="{render.LOGO_RLR_N}" alt="{AUTOR}"><img class="sl" src="{render.LOGO}" alt="SuperLeads"></footer>
<script>{render.JS}{JS_FIT}</script></body></html>"""

CSS_PORTADA = """
html,body{width:var(--w);height:var(--h)}
header{display:none}
.port{position:absolute;left:96px;right:96px;top:0;bottom:120px;display:flex;flex-direction:column;justify-content:center}
.port .eyebrow{margin-bottom:22px} .port .eyebrow span{font-size:calc(var(--fs) * .29)}
.port h1{font-size:var(--fs);line-height:1.04;letter-spacing:-2.4px;margin:0;font-weight:800;max-width:calc(var(--w) - 192px)}
.port h1 em{font-style:italic;color:var(--green)}
.port .sub{margin-top:26px;font-size:28px;line-height:1.38;color:var(--t2);max-width:1250px;font-weight:500}
footer.art{position:absolute;left:96px;right:96px;bottom:40px;border-top:.5px solid rgba(255,255,255,.14);padding-top:22px;display:flex;justify-content:space-between;align-items:center}
footer.art .nombre{height:46px;width:auto;display:block} footer.art .sl{width:176px;height:auto;display:block}
"""
def lamina_portada_art(a, ancho, alto, con_sub=True):
    fs = 76 if alto >= 900 else 104
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{render.CSS}{CSS_PORTADA}</style></head>'
            f'<body data-author="RLR" style="--w:{ancho}px;--h:{alto}px;--fs:{fs}px"><div class="fondo"><div class="g1"></div><div class="g2"></div></div>'
            f'<div class="port"><div class="eyebrow"><span>Artículo {a["n"]} de 3 · {html.escape(a["eyebrow"])}</span></div><h1>{a["titulo_html"]}</h1>'
            + (f'<div class="sub">{html.escape(a["subtitulo"])}</div>' if con_sub else '') +
            f'</div><footer class="art"><img class="nombre" src="{render.LOGO_RLR_N}" alt="{AUTOR}"><img class="sl" src="{render.LOGO}" alt="SuperLeads"></footer></body></html>')

# ───────────── los tres artículos ─────────────
# Cada artículo es una lista de bloques: ('h2', texto) · ('p', párrafo) · ('fig', 'X2') · ('cita', frase) · ('lista', [..])
A1 = dict(n=1, eyebrow='Corte Rayos X · octubre 2026', titulo_html='Cómo está el mercado educativo privado en México: <em>conclusiones del corte Rayos X</em>', slug='Como esta el mercado educativo privado en Mexico · corte Rayos X octubre 2026',
 titulo='Cómo está el mercado educativo privado en México: conclusiones del corte Rayos X de octubre de 2026',
 subtitulo='102 instituciones, 69 ciudades, ocho meses de diagnósticos. Lo que miden los dueños de colegios, no lo que creen.',
 bloques=[
 ('p', 'Entre marzo y octubre de 2026 me senté, con mi equipo, frente a 102 dueños y directores de instituciones educativas privadas en 69 ciudades de México. Con cada uno hicimos lo mismo: un Rayos X de Inscripciones. Una sesión para acomodar los números de admisiones de su institución como tienen que estar: capacidad, matrícula, prospectos, citas, inscritos, colegiatura, permanencia, publicidad, equipo.'),
 ('p', 'Este artículo es el primer corte de esos números. Lo publico porque creo que el sector necesita un punto de referencia que hoy no existe: cuando un director quiere saber si su colegio va bien o va mal, no tiene con quién compararse. Compara con el ciclo pasado y con lo que escucha en el pasillo. Aquí tiene algo mejor: la mediana de 102 instituciones que se midieron con la misma regla.'),
 ('p', 'Dos advertencias antes de empezar, porque me importa que esto sea citable. La primera: es nuestra muestra, no el país. Son instituciones que pidieron un diagnóstico, 35 colegios con primaria, 14 con preparatoria y 42 universidades y posgrados, más academias y escuelas en línea. La segunda: publico medianas, no promedios. Un colegio de 7,000 alumnos mueve el promedio y miente. La mediana dice dónde está el colegio típico, y eso es lo que te sirve para ubicarte.'),
 ('fig', 'X1'),
 ('h2', '1. La mitad del colegio está vacía'),
 ('p', 'El primer dato es el que más me cuesta decir en voz alta: la institución privada mediana en México opera al 46 % de su capacidad instalada. No es un colegio en crisis. Es la mitad de la muestra. De cada 100 lugares que construyó, usa 46.'),
 ('fig', 'X2'),
 ('p', 'Por nivel, la foto cambia poco. Los colegios con primaria operan al 60 % en la mediana, los que tienen preparatoria al 52 % y las universidades al 41 %. Seis de cada diez instituciones de la muestra están abajo del 60 % de ocupación; solo 13 % está arriba del 80 %.'),
 ('p', 'Puesto en lugares, la institución mediana tiene 267 sillas vacías. Sumando las 98 instituciones que reportaron el dato, son 59,507 lugares sin alumno. Y puesto en pesos, la capacidad sin usar de la institución mediana vale $794,625 MXN al año; entre todas, $279.6 millones MXN al año. Es infraestructura ya pagada: el aula existe, el maestro existe, el lugar existe. Lo único que falta es el alumno.'),
 ('fig', 'X3'),
 ('p', 'Lo que más me llama la atención no es el número, sino la normalidad con la que se vive. Nadie abre un colegio para llenarlo a la mitad. Se llega ahí un ciclo a la vez, con una familia que no contestó y otra que llegó tarde a la cita. Y como el deterioro es lento, nadie lo ve como emergencia.'),
 ('h2', '2. El embudo: dónde se pierde la inscripción'),
 ('p', 'La institución mediana recibe 8 prospectos nuevos al día. El colegio con primaria recibe 3, el de preparatoria 5 y la universidad 15. No es poca demanda: son entre 60 y 400 familias al mes que levantan la mano.'),
 ('fig', 'X4'),
 ('p', 'De cada 100 familias que preguntan, 2.4 se inscriben. Esa es la conversión mediana de prospecto a inscrito. Cuatro de cada diez instituciones convierten menos del 2 %. Solo 9 % convierte más del 10 %.'),
 ('fig', 'X5'),
 ('p', 'Y aquí viene el dato que cambia el diagnóstico. De las familias que sí llegan a la cita o al recorrido, 40 % se inscribe. Es decir: cuando el colegio tiene a la familia enfrente, vende. Lo que no sabe hacer es llevarla hasta ahí.'),
 ('fig', 'X6'),
 ('p', 'Esas tres cifras juntas dicen algo incómodo y muy útil. El problema del colegio privado mexicano no está en la cita. Está antes de la cita: en el tiempo de respuesta al primer mensaje, en el seguimiento del segundo día, en el «ahorita le contesto» que se volvió nunca. Entre el primer WhatsApp y el recorrido se evapora la mayor parte de la demanda, y casi nunca por precio.'),
 ('h2', '3. El dinero: cuánto vale un alumno y cuánto cuesta'),
 ('p', 'La colegiatura mensual mediana es de $3,300 MXN. La mitad de las instituciones cobra entre $2,150 y $5,000 MXN al mes. Los colegios con primaria cobran $3,825 MXN en la mediana, los de preparatoria $4,000 MXN y las universidades $2,994 MXN. La cuota de inscripción mediana es de $3,750 MXN.'),
 ('fig', 'X7'),
 ('p', 'Un alumno permanece 48 meses en la institución mediana: 60 meses en el colegio con primaria, 60 en preparatoria, 36 en la universidad. Colegiatura por meses de permanencia da el valor de vida: $144,000 MXN por alumno en la mediana general, y $222,670 MXN en el colegio con primaria. Cada familia que se inscribe vale eso. Cada familia que se enfría, también.'),
 ('fig', 'X8'),
 ('p', 'Del otro lado está el costo. La institución mediana invierte $8,000 MXN al mes en publicidad: $3,250 MXN el colegio con primaria, $6,083 MXN el de preparatoria, $14,000 MXN la universidad. Cada prospecto le cuesta $41 MXN y cada alumno inscrito, $1,381 MXN.'),
 ('fig', 'X9'),
 ('p', 'Léelo junto: un alumno cuesta $1,381 MXN y vale $144,000 MXN. La publicidad educativa es de las inversiones más rentables que conozco. El problema nunca ha sido cuánto se invierte, sino cuánto de lo que se compra con esa inversión se evapora después, sin que nadie lo vea.'),
 ('p', 'Por eso la cifra que más repito en cada Rayos X es esta: subir un solo punto porcentual la conversión vale $109,500 MXN al año para la institución mediana. $39,420 MXN para el colegio con primaria mediano, $101,324 MXN para el de preparatoria y $158,629 MXN para la universidad mediana. Sin un peso más de anuncios. Es el mismo número de familias interesadas, atendidas mejor.'),
 ('fig', 'X10'),
 ('h2', '4. Cómo está armada la operación de admisiones'),
 ('p', 'Aquí está la explicación de casi todo lo anterior. 71 % de las instituciones lleva sus admisiones en WhatsApp o en Excel. Solo 29 % tiene un CRM. En los colegios con primaria, el 88 % trabaja con WhatsApp y Excel y apenas 12 % tiene CRM.'),
 ('fig', 'X13'),
 ('p', 'El equipo de admisiones y marketing de la institución mediana es de 3 personas; en el colegio con primaria, 1.1 persona. La mediana de asesores de admisiones dedicados es 1; en el colegio con primaria, cero. Solo 55 % de las instituciones tiene alguien con el cargo de director de admisiones, y 24 % trabaja con una agencia externa.'),
 ('p', '48 % de las instituciones no tiene un plan de compensación para su equipo de admisiones. En colegios con primaria, 61 %. Es decir: la persona que decide si la familia se inscribe o no, casi nunca tiene un incentivo ligado a inscribir.'),
 ('p', 'Y todo eso ocurre en una temporada muy corta. Julio y agosto concentran la inscripción para la mitad de las instituciones, y febrero para cuatro de cada diez. Una operación de temporada alta, atendida por una persona, con la memoria en un teléfono y sin incentivo. No es falta de talento. Es falta de sistema.'),
 ('h2', '5. Las palancas que casi nadie trabaja'),
 ('p', '68 % de las instituciones da becas y la mediana tiene 40 % de alumnos becados, con una beca promedio de 25 %. La beca dejó de ser una excepción: es una herramienta comercial, y conviene administrarla como tal.'),
 ('p', '40 % de los alumnos llega por recomendación de otra familia; 50 % llega por anuncios. Y sin embargo, 70 % de las instituciones no tiene un programa de recomendados. El canal más barato y más confiable del colegio es el que nadie trabaja.'),
 ('fig', 'X12'),
 ('p', 'En ingresos además de la colegiatura, la cafetería (69 %) y las graduaciones (60 %) son casi universales; uniformes y libros los cobra 57 %; el transporte, 17 %. Lo que ya tienes vale más que lo que falta por comprar.'),
 ('h2', '6. Lo que el director cree'),
 ('p', 'En el Rayos X también preguntamos qué cree el director. Lo digo así, «cree», porque aquí no hay mediciones: hay percepciones, y conviene no confundirlas.'),
 ('p', 'Cuando preguntamos por qué no se inscribieron las familias que no se inscribieron, la causa más mencionada es el precio (62 %). La segunda, la falta de seguimiento (38 %). Después, con 17 % cada una, el cupo u horario, la competencia y la distancia. Fíjate en el orden: la primera causa no depende de nadie; la segunda está completamente bajo el control del colegio.'),
 ('fig', 'X17'),
 ('p', 'Y cuando preguntamos cómo califica su marketing, 44 % lo califica de muy bueno o excelente. Al mismo tiempo, 64 % de las instituciones opera abajo del 60 % de su capacidad. Esa distancia entre percepción y realidad es, probablemente, la gráfica más importante de todo el corte. No se arregla lo que no se ve.'),
 ('fig', 'X18'),
 ('h2', 'Conclusiones del corte'),
 ('lista', ['La institución privada mediana en México opera al 46 % de su capacidad. Hay demanda disponible, hay lugares disponibles y hay infraestructura pagada. Lo que falta no es mercado: es proceso.',
            'El colegio sabe cerrar: 40 % de las familias que llegan a la cita se inscribe. Pero solo 2.4 % de las que preguntan llega a inscribirse. La inscripción se pierde entre el primer mensaje y la cita, no en la cita.',
            'Un alumno cuesta $1,381 MXN en publicidad y vale $144,000 MXN. La publicidad no es el problema. Lo que se compra con ella se pierde después, en el seguimiento.',
            'Un punto de conversión vale $109,500 MXN al año para la institución mediana. Es el crecimiento más barato que existe: las familias ya llegaron.',
            'Siete de cada diez instituciones operan sus admisiones en WhatsApp y Excel, con una persona y sin plan de compensación. El resultado no es casualidad: es el sistema que se tiene.',
            'El director culpa al precio. Los datos culpan al silencio. Con una colegiatura mediana de $3,300 MXN y 13.4 millones de hogares mexicanos que pueden pagarla, el precio rara vez es el motivo.']),
 ('h2', 'Para qué sirve esto'),
 ('p', 'Sirve para que te ubiques. Toma tu ocupación, tu conversión, tu cierre en cita, tu costo por alumno y tu valor de vida, y ponlos junto a estas medianas. Si estás arriba, ya tienes un sistema y este corte te confirma el tamaño de lo que estás capturando. Si estás abajo, no estás solo: estás con la mayoría, y la buena noticia es que ninguna de estas cifras depende del mercado. Todas dependen del proceso.'),
 ('p', 'Estos números salen de los Rayos X de Inscripciones que hacemos en SuperLeads. Es una sesión de trabajo con el dueño o el director en la que ordenamos los números de su institución exactamente como aparecen aquí, con sus datos, y salen con un PDF con lo más importante. Volveremos a publicar el corte cada seis meses, con los datos acumulados, para que el sector tenga por fin una referencia que no sea el pasillo.'),
 ('p', 'La próxima edición es en abril de 2027. Si quieres que tu institución esté en ella, el Rayos X es el camino: superleads.mx/rayos_x. Y si quieres comentar estos números conmigo, escríbeme directo: ricardo@superleads.mx.'),
 ('h2', 'Nota metodológica'),
 ('p', 'Corte del 29 de octubre de 2026 a las 18:08. 110 Rayos X exportados; fuera pruebas, archivados y repetidos (una fila por institución, la más reciente): 102 instituciones en 69 ciudades, finalizados entre el 6 de marzo y el 28 de octubre de 2026. Montos en pesos mexicanos; las instituciones en dólares quedan fuera de los montos. Ningún dato con menos de cinco instituciones se publica. Medianas, con cuartiles y n por métrica, disponibles a solicitud: ricardo@superleads.mx.'),
 ])

A2 = dict(n=2, eyebrow='La realidad de la educación', titulo_html='La educación pública en México: <em>lo que dicen los datos</em>', slug='La educacion publica en Mexico · lo que dicen los datos',
 titulo='La educación pública en México: lo que dicen los datos',
 subtitulo='Aprendizajes, planteles, maestros, días de clase e inversión. Las cifras oficiales e internacionales que todavía existen, puestas en una sola página.',
 bloques=[
 ('p', 'Nueve de cada diez niños mexicanos estudian en una escuela pública. Yo trabajo todos los días con colegios privados, y aun así, o precisamente por eso, llevo años leyendo todo lo que se publica sobre la escuela pública. La razón es simple: casi ninguna familia llega a un colegio privado preguntando por el colegio privado. Llega preguntando «¿qué pasa si no?». Qué pasa si mi hijo se queda en la escuela que le toca.'),
 ('p', 'Este artículo responde esa pregunta con datos. No con percepciones ni con anécdotas: con las cifras de la OCDE, el Coneval, la Auditoría Superior de la Federación, la UNESCO, el INEGI y la propia SEP. No es un ataque a los maestros, que como verás son tan víctimas del sistema como los alumnos. Es la lectura de la realidad con la que conviene operar, sea cual sea el lado del mostrador en el que estés.'),
 ('p', 'Y es, también, un documento que se está volviendo difícil de armar. Buena parte de esta información ya no se produce: el país desmanteló sus instrumentos de medición educativa, y lo que no se mide tiende a desaparecer del debate. Por eso lo escribo hoy, con las últimas cifras que existen.'),
 ('h2', '1. Lo que aprenden, y lo que no'),
 ('p', 'La última fotografía internacional del aprendizaje en México es PISA 2022, de la OCDE. La última, porque después el país dejó de medirse. El retrato es este: México quedó en el lugar 35 de 37 países de la OCDE. Tercer peor resultado en Matemáticas y Lectura; el peor de toda la OCDE en Ciencias.'),
 ('fig', 'R1'),
 ('p', 'En Matemáticas, el alumno mexicano de 15 años obtuvo 395 puntos contra 472 del promedio OCDE: 77 puntos abajo. Veinte puntos PISA equivalen, aproximadamente, a un año escolar. En Lectura, 415 contra 476. En Ciencias, 410 contra 485.'),
 ('p', '66 % de los alumnos mexicanos de 15 años no alcanza el nivel básico de competencia en Matemáticas. 47 % no comprende lo que lee al nivel mínimo. 1 % alcanza niveles de excelencia en Lectura; en Matemáticas, prácticamente 0 %.'),
 ('fig', 'R2'),
 ('p', 'El Banco Mundial estima que la pandemia añadió un rezago equivalente a dos años de escolaridad: el egresado promedio de secundaria sabe hoy lo que antes sabía un alumno de primero. Y la última evaluación nacional conocida, la de Mejoredu para el ciclo 2024-2025, filtrada a la prensa, encontró que 8 de cada 10 estudiantes de tercero de secundaria no desarrollaron los aprendizajes esperados.'),
 ('fig', 'R11'),
 ('h2', '2. El plantel: aprender sin agua, sin luz, sin internet'),
 ('p', 'La desigualdad educativa mexicana no empieza en el aula. Empieza en el inmueble. Según el estudio Aprender Parejo de México Evalúa y el Tec de Monterrey, 40 % de las escuelas públicas opera con al menos una carencia de servicios básicos: agua, luz o sanitarios dignos. En las privadas, 8 %.'),
 ('fig', 'R3'),
 ('p', 'Las cifras oficiales lo confirman pieza por pieza. 9,034 planteles públicos de educación básica no tienen acceso a agua potable y 5,112 no tienen servicio eléctrico, según la SEP para el ciclo 2023-2024. 89 mil escuelas de básica no tienen drenaje, según el Coneval. 61 % de las primarias supera los 25 años de vida útil estructural, según la Auditoría Superior de la Federación. 31 % de los planteles diagnosticados por el INIFED presentaba daño estructural.'),
 ('p', 'Y 65 de cada 100 escuelas públicas operan sin computadoras ni internet. En un país cuya economía se mueve con el T-MEC, el nearshoring y el turismo, dos de cada tres escuelas públicas no tienen una computadora conectada.'),
 ('fig', 'R4'),
 ('p', 'Lo notable no es la falta de dinero. Entre 2013 y 2024 se gastaron $451,230 millones MXN en infraestructura educativa. Pero desde 2019 dejó de actualizarse el censo nacional de infraestructura escolar, así que nadie puede decir, oficialmente, en qué se convirtió ese dinero. Se gastó el presupuesto y se apagó el medidor.'),
 ('h2', '3. Quién está frente al grupo'),
 ('p', 'Aquí conviene decirlo con claridad: el docente mexicano no es el villano de esta historia. Es su segunda víctima. Los datos del INEGI, en la ENOE del primer trimestre de 2025, sobre los cerca de dos millones de docentes del país, dicen que el ingreso mensual promedio de un maestro es de $7,890 MXN. El salario mínimo de 2025 es de $8,400 MXN. Un maestro de preescolar promedia $6,430 MXN; uno de preparatoria, $6,260 MXN.'),
 ('fig', 'R5'),
 ('p', 'Son promedios nacionales que incluyen jornadas parciales e informalidad. Las mediciones de docentes formales de tiempo completo, como las del IMCO, elevan el promedio a unos $18,000 MXN, todavía por debajo del promedio OCDE para la profesión. La OCDE añade el cuadro estructural: México combina una de las cargas frente a grupo más altas del organismo con uno de los salarios base más bajos.'),
 ('p', 'A eso se suman dos decisiones de política. La capacitación docente es esporádica y sin seguimiento. Y desde 2019, con la cancelación de la evaluación docente obligatoria, no existe ningún mecanismo nacional que verifique las competencias de quien está frente a un grupo. El mensaje del sistema a su maestro es coherente y devastador: te pago poco, no te formo, no te evalúo. La desmotivación no es un defecto del magisterio. Es la respuesta racional a esos incentivos.'),
 ('h2', '4. El calendario que no se cumple'),
 ('p', 'En junio de 2026 ocurrió la interrupción educativa de mayor cobertura geográfica en décadas. El paro nacional de la CNTE, iniciado el 1 de junio, dejó, en cifras de la propia SEP con corte al 5 de junio, 17,471 escuelas cerradas en la recta final del ciclo, 1,410,459 alumnos sin clases y 88,546 docentes en paro en diez estados. En Oaxaca, 92.13 % de la matrícula estatal se quedó sin un solo día de clases.'),
 ('fig', 'R6'),
 ('p', 'No es un evento extraordinario. Es un patrón que se repite cada ciclo desde hace décadas, con distinta intensidad por estado, y sus efectos son acumulativos: cada semana perdida en los primeros años de escolaridad es un agujero que rara vez se recupera, y golpea más a las familias sin acceso a clases particulares, computadora o internet.'),
 ('p', 'Para la familia, la consecuencia práctica es la incertidumbre: no sabe, al inscribir el ciclo, cuántos días de clase recibirá realmente su hijo. La certeza del calendario, algo tan elemental que ningún colegio privado lo presume, es uno de los diferenciales más valorados por las familias que cruzan de la pública a la privada.'),
 ('h2', '5. El inglés: una materia que se aprueba sin aprenderse'),
 ('p', 'El diagnóstico más completo sobre el inglés en la escuela pública, el estudio Sorry de Mexicanos Primero, sigue sin ser refutado, y la evidencia posterior indica deterioro. 97 % de los egresados de secundaria pública no alcanza el nivel de inglés del propio plan de la SEP. 86 % de las escuelas públicas de básica no tiene siquiera un maestro de inglés. 52 % de los maestros que sí lo imparten no alcanza el nivel B1 que se espera de sus alumnos.'),
 ('fig', 'R7'),
 ('p', 'México necesita 400,000 maestros de inglés y tiene 80,000. La matrícula pública atendida con inglés cayó 43 %, de 9.2 a 5.2 millones de alumnos, y el presupuesto del Programa Nacional de Inglés se redujo 27 % real entre 2018 y 2024. En primaria pública, el inglés ni siquiera es obligatorio. El niño de colegio privado toma inglés desde preescolar. El de escuela pública, con 86 % de probabilidad, jamás tendrá un maestro del idioma.'),
 ('h2', '6. Cuánto invierte el Estado en cada niño'),
 ('p', 'Detrás de cada sección anterior hay una causa común, y la OCDE la mide cada año en Education at a Glance. México ocupa el último lugar de la OCDE en gasto por alumno de primaria: $2,933 USD al año. Luxemburgo invierte $25,584 USD; Estados Unidos, $15,270 USD; el promedio OCDE es $11,902 USD. Países con menor PIB per cápita que México, como Colombia, Bulgaria, Turquía, Hungría y Rumania, invierten más por niño.'),
 ('fig', 'R8'),
 ('p', 'Y la tendencia es descendente. El gasto por alumno cayó 10.5 % entre 2015 y 2022 mientras el promedio OCDE subía. El gasto educativo de 2026 equivale a 3.19 % del PIB, el nivel más bajo desde 2018. La composición también cambió: cerca de 180 mil millones de pesos anuales se destinan a becas universales que, según los especialistas, no han mejorado cobertura, permanencia ni aprendizaje, mientras se recorta lo que construye capacidad: escuelas, maestros, materiales, evaluación.'),
 ('p', 'Un dato cierra el círculo: la escuela «gratuita» no lo es. Las familias mexicanas cubren 16.2 % del gasto educativo en básica y media superior, con cooperaciones, útiles y mantenimiento de los planteles. El promedio OCDE es 9.9 %. La familia mexicana ya paga por la educación pública. Lo que no recibe a cambio es el servicio.'),
 ('fig', 'R9'),
 ('h2', '7. El país que rompió sus termómetros'),
 ('p', 'Si algunas cifras de este artículo te parecieron viejas, no es descuido mío. Es el hallazgo central: México desmanteló sistemáticamente sus instrumentos de medición educativa. La cronología, verificada por la UNESCO en su Estrategia de País 2026-2031, es esta.'),
 ('fig', 'R10'),
 ('p', 'En 2019 desaparece el INEE, el instituto autónomo de evaluación. Se cancelan las pruebas censales nacionales (PLANEA) y la evaluación docente obligatoria. Se congela el censo de infraestructura escolar. Entre 2019 y 2025 México sale del ERCE, la prueba regional de la UNESCO, y pone en riesgo su participación en PISA 2025, al grado de que la OCDE pide públicamente no abandonar la última medición que queda. En 2025 desaparece Mejoredu, el organismo que sustituyó al INEE, sin publicar los resultados de su última evaluación diagnóstica. En 2026 la UNESCO advierte que México implementa un nuevo modelo educativo, la Nueva Escuela Mexicana, sin ningún mecanismo nacional para saber si funciona.'),
 ('p', 'Ningún sistema serio destruye sus instrumentos de medición cuando los resultados van bien. Se destruyen cuando los resultados son indefendibles. La opacidad no es un descuido administrativo. Es una política. Y la consecuencia para todos es que el debate público sobre educación se da con datos de 2022 hacia atrás.'),
 ('h2', 'Lo que esto significa'),
 ('p', 'Súmalo y obtienes la trayectoria del niño promedio en la escuela pública: un plantel que en 4 de cada 10 casos carece de servicios básicos; un maestro que gana menos que el salario mínimo, sin formación ni evaluación; semanas de clases perdidas cada ciclo; 86 % de probabilidad de no tener jamás un maestro de inglés; y a los 15 años, 66 % de probabilidad de no dominar las matemáticas básicas.'),
 ('p', 'Quiero ser claro en algo. Yo quisiera que la escuela pública funcionara. Es la única salida real para un país de 130 millones de personas, y ojalá en algún futuro funcione. Pero hoy, con los pies en la tierra, no está funcionando, y la familia que decide dónde inscribir a su hijo lo sabe antes que cualquier informe. Por eso, mientras la pública se arregla, la educación privada no es un lujo ni una competencia desleal: es esencial para este país. Cada familia que encuentra un buen colegio privado es un niño que sale de esta estadística.'),
 ('p', 'Si diriges un colegio privado, este artículo es tu argumentario, con fuentes y sin adjetivos. La conversación de admisión más poderosa no es «somos mejores que el colegio X». Es «esto es lo que tu hijo recibe aquí, y esto es lo que el sistema le garantiza si no». La familia que cruza de la pública a la privada no está comparando colegios. Está comprando certeza. Y la primera prueba de certeza que le das no es tu instalación ni tu modelo educativo: es cómo la atiendes en las primeras 24 horas desde que mostró interés. En SuperLeads nos dedicamos exactamente a ese tramo, y es lo que escribiré en el siguiente artículo. Si quieres los datos de este texto para tu propio argumentario, escríbeme: ricardo@superleads.mx.'),
 ('h2', 'Fuentes'),
 ('p', 'OCDE, PISA 2022 Results y Country Note México; IMCO, «PISA 2022: dos de cada tres estudiantes en México no alcanzan el nivel básico en Matemáticas» (2023) y Compara Carreras (2025); Banco Mundial, estimaciones de pérdida de aprendizajes post-COVID; Mejoredu / El Universal, evaluación diagnóstica 2024-2025; México Evalúa / Tec de Monterrey, Aprender Parejo (2024); Coneval, Información Estratégica para el Regreso a Clases (2021); SEP, estadísticas de servicios básicos por plantel, ciclo 2023-2024, y reportes oficiales del paro de la CNTE con corte al 5 de junio de 2026; ASF e INIFED, antigüedad y daño estructural de planteles; INEGI, ENOE 1T-2025; Data México, salarios por nivel educativo; Mexicanos Primero, Sorry: el aprendizaje del inglés en México y análisis de Education at a Glance (2025); SEP / SHCP, presupuestos del Programa Nacional de Inglés 2018-2024; OCDE, Education at a Glance 2023-2025; CIEP, Paquete Económico 2026; UNESCO, Estrategia de País México 2026-2031. Metodología y fuentes completas a solicitud: ricardo@superleads.mx.'),
 ])

A3 = dict(n=3, eyebrow='La gran oportunidad', titulo_html='Por qué los dueños de colegios en México <em>tienen que ser más ambiciosos</em>', slug='La gran oportunidad de los duenos de colegios en Mexico',
 titulo='La gran oportunidad: por qué los dueños de colegios en México tienen que ser más ambiciosos',
 subtitulo='13.4 millones de hogares pueden pagar un colegio privado y solo 10 % de los alumnos está en uno. El mercado ya hizo su parte. Lo que falta está dentro de cada institución.',
 bloques=[
 ('p', 'Escribí dos artículos antes que este. En el primero conté cómo está el mercado educativo privado en México con los números de 102 Rayos X de Inscripciones: la institución mediana opera al 46 % de su capacidad. En el segundo conté cómo está la educación pública con las cifras oficiales e internacionales que todavía existen: 66 % de los alumnos de 15 años no alcanza el nivel básico de matemáticas. Este tercer artículo junta los dos, y llega a una conclusión que me parece la más importante de las tres.'),
 ('p', 'Los dueños y directores de colegios en México tienen frente a ellos una de las oportunidades más grandes que he visto en cualquier industria. Y tienen, al mismo tiempo, una responsabilidad enorme: deben ser más ambiciosos. Deben querer crecer mucho más sus colegios, porque cada alumno que inscriben es un bien real para el país. Lo que les falta no es mercado ni vocación. Es saber venderse. Voy a explicarlo con datos.'),
 ('h2', '1. El tamaño real del mercado'),
 ('p', 'Hay una pregunta que casi ningún directivo se ha hecho con datos en la mano, y es la primera que vale la pena responder. No es «¿cuánta competencia tengo?». Es «¿qué tan penetrada está la educación privada en mi país?».'),
 ('fig', 'R22'),
 ('p', 'Solo 10 % de los alumnos de México está en una escuela privada. Es la penetración más baja de Latinoamérica, según el Banco Mundial y el Instituto de Estadística de la UNESCO. Chile tiene 63 %. Perú, 26 %. Colombia, 19 %. Brasil, 18 %. Guatemala y El Salvador, 12 %. El promedio mundial es 19 %. México, la segunda economía de la región, con 38 millones de hogares y una de las clases medias urbanas más grandes del continente, está al nivel de Estados Unidos, donde la escuela pública compite con presupuestos de otro planeta.'),
 ('p', 'Cuando un directivo mexicano dice «hay demasiados colegios», los datos responden otra cosa: en México hay demasiado pocas familias en la privada para el tamaño de su economía. La educación privada en México no es un mercado saturado. Es un mercado subdesarrollado. Y un mercado subdesarrollado es, por definición, un mercado por capturar.'),
 ('h2', '2. «Es que la gente no puede pagar»'),
 ('p', 'A esa primera conclusión siempre le sigue la misma objeción. Es una explicación cómoda, porque exime a todos de responsabilidad. También es falsa, y la pirámide socioeconómica lo demuestra.'),
 ('fig', 'R23'),
 ('p', 'La Regla NSE de la AMAI, el estándar con el que toda la industria de consumo en México segmenta a sus clientes, clasifica los cerca de 38 millones de hogares del país en siete niveles. Los tres superiores son el territorio natural del colegio privado: A/B, 5.6 % de los hogares, unos 2.1 millones de familias con ingresos superiores a $120,000 MXN al mes; C+, 13.1 %, unos 5 millones con alrededor de $48,000 MXN; y C, 16.7 %, unos 6.3 millones con cerca de $28,000 MXN.'),
 ('p', 'Sumados: 13.4 millones de hogares, 35 % del país. Aplicando la regla más aceptada del sector, que una colegiatura sana representa alrededor del 10 % del ingreso familiar por hijo, esos hogares pueden sostener colegiaturas de $2,800 a más de $12,000 MXN mensuales. Exactamente el rango en el que opera la inmensa mayoría de los colegios privados del país. Y sin embargo, solo 10 % de la matrícula está en privada.'),
 ('p', 'Léelo de nuevo: en México hay más familias que pueden pagar colegio privado que familias que lo están pagando. Esa brecha es el techo de crecimiento de todo el sector, y está lejísimos.'),
 ('h2', '3. La prueba peruana'),
 ('p', 'Perú desmiente la objeción del dinero con elegancia. Allá, los niveles A y B suman apenas 10.4 % de los hogares, con ingresos muy inferiores a sus equivalentes mexicanos. Y aun así, 26 % de los alumnos peruanos está en privada, porque familias de nivel C, e incluso de nivel D, pagan pensiones de 300 a 600 soles por una razón que no aparece en ninguna encuesta de ingreso: decidieron que la educación pública no era opción para sus hijos, y ajustaron todo lo demás.'),
 ('fig', 'R24'),
 ('p', 'México: 35 % puede pagar, 10 % inscribe. Perú: 10 % puede pagar, 26 % inscribe. La lección peruana es brutal y liberadora a la vez. Cuando una familia cree que la educación de sus hijos lo vale, encuentra cómo pagarla. La pregunta nunca fue si pueden. La pregunta es a quién se la pagan, y por qué a ti o por qué a otro.'),
 ('h2', '4. Un sector más grande y más profesional de lo que parece'),
 ('p', 'Las estadísticas oficiales hablan de 45,000 escuelas privadas de educación básica. El dato está inflado por una razón técnica que cualquier dueño conoce: cada nivel de un plantel genera su propia clave de centro de trabajo, así que un colegio con kínder, primaria y secundaria aparece tres veces. Corrigiendo ese efecto, el universo real es de unos 20,000 planteles privados que atienden a unos 5.2 millones de alumnos. Eso da 260 alumnos por colegio, el segundo promedio más alto de la región.'),
 ('fig', 'R25'),
 ('p', 'No es una escuelita de supervivencia. Es una operación de 260 familias, con facturación anual de varios millones de pesos, nómina docente profesional y dos o tres niveles educativos funcionando en paralelo. Y esa última frase esconde la complejidad que define al sector: dos o tres niveles significan dos o tres procesos de captación simultáneos, que en la mayoría de los colegios atiende la misma persona que además contesta el teléfono y organiza el festival.'),
 ('p', 'En el extremo alto, el premio se mide con precisión. Los diez colegios más caros de la Ciudad de México cobran $1,050 USD al mes en promedio. Lo mismo que los de Lima y Bogotá, en una economía mayor, y lejos de São Paulo ($1,850 USD) o Washington DC ($4,800 USD). Ni siquiera el segmento premium mexicano ha alcanzado el precio que su mercado podría sostener. Tiene margen en volumen y en precio: un lujo que muy pocas industrias pueden presumir.'),
 ('fig', 'R26'),
 ('p', 'Y la demografía empuja a favor. Querétaro recibe cada año miles de familias de clase media alta que migran desde la Ciudad de México. Mérida es el imán de la seguridad. Cancún y la Riviera Maya tienen la demografía más joven del país. La periferia industrial de Monterrey, con el nearshoring, recibe familias con ingreso formal y urgencia de decidir colegio en semanas. En todas esas plazas llegan las familias más fáciles de inscribir de todo el mercado: no están evaluando si cambiarse de colegio, necesitan uno ya.'),
 ('h2', '5. Entonces, ¿por qué los colegios no están llenos?'),
 ('p', 'Con ese contexto, todos los colegios privados de México deberían estar llenos. Y la institución mediana de nuestro corte de octubre opera al 46 % de su capacidad. Las dos cosas no pueden ser ciertas si el problema fuera el mercado. Una de las dos explicaciones está equivocada, y los datos dicen cuál.'),
 ('fig', 'X2'),
 ('p', 'Un colegio con lugares disponibles en un mercado con demanda disponible no tiene un problema de mercado. Tiene un problema de proceso. Y el problema de proceso tiene una anatomía que he visto repetirse en cientos de diagnósticos con variaciones mínimas. Las familias sí llegan: 8 prospectos al día en la institución mediana. Lo que decide el ciclo escolar es lo que pasa en las horas y días siguientes.'),
 ('p', 'Los datos de comportamiento de las familias son contundentes. En un estudio con 1,000 consultas a instituciones educativas, 44 % jamás recibió respuesta. 78 % de las familias le compra al primero que responde, y solo 7 % de las organizaciones contesta en los primeros cinco minutos. Responder en cinco minutos hace 21 veces más probable calificar al prospecto que hacerlo a los treinta.'),
 ('fig', 'R12'),
 ('fig', 'R14'),
 ('p', 'Y la familia investiga cuando el colegio está cerrado: 93 % está conectada entre las 9 de la noche y la medianoche, y 71 % descarta un colegio con menos de 3 estrellas en Google. La decisión toma seis meses y la mitad ocurre sin que el colegio se entere. El colegio compite en un horario y en un canal que no son los suyos, y quien aparece con una respuesta se queda con la cita.'),
 ('fig', 'R15'),
 ('p', 'Ponle número. Con una colegiatura de $4,500 MXN, seis años de permanencia y la probabilidad de hermano que todo director conoce, cada familia inscrita vale alrededor de $450,000 MXN. Con las mismas 40 consultas, el colegio que responde en horas inscribe 4; el que responde en minutos, 10. La diferencia son 6 familias: $2.7 millones MXN de valor de vida por temporada. No se pierden por falta de demanda, ni de prestigio, ni de publicidad. Se pierden por velocidad.'),
 ('fig', 'R17'),
 ('p', 'La inscripción perdida casi nunca es una familia que dijo que no. Es una familia que dijo que sí con su interés, y se quedó en el camino por el silencio.'),
 ('h2', '6. La responsabilidad'),
 ('p', 'Aquí quiero cambiar de tono, porque este artículo no es un reproche. Los dueños de colegio que conozco trabajan muchísimo. Invierten en publicidad, renuevan la página, abren redes, capacitan a su gente. Y hacen algo que pocas industrias hacen: reinvierten. No conozco mejor dinero que el que le queda al dueño de un colegio, porque casi todo regresa a la escuela. Están picados, mejorando el laboratorio, el inglés, la cancha, la capacitación. Es gente apasionada por educar.'),
 ('p', 'Por eso es correcto y es sano que su modelo de negocio opere al máximo. Un colegio rentable es un colegio que puede reinvertir, pagar mejor a sus maestros y sostener la calidad que promete. Y si el sistema de inscripciones no opera al máximo, automáticamente el activo y la rentabilidad del colegio tampoco. La matrícula no es una meta que se persigue cada agosto: es un activo que se compone. Las familias bien inscritas permanecen más años, las que permanecen recomiendan, y cada ciclo construye sobre el anterior.'),
 ('p', 'La educación pública, hoy, no está funcionando. Ojalá en algún futuro funcione, y lo digo con sinceridad. Pero con los pies en la tierra, cada niño que entra a un buen colegio privado sale de la estadística del 66 %, del 86 % sin maestro de inglés, de los paros de junio. Eso es lo que hace un dueño de colegio cuando llena un salón. Por eso digo que tienen que ser más ambiciosos: no por ellos, por el país. Y lo mejor de todo es que pueden crecer enormemente sin moverle un alumno a nadie. Con 13.4 millones de hogares que pueden pagar y 10 % de penetración, cada familia que cruza de la pública a la privada es mercado nuevo, que no existía para nadie. El colegio que aprende a convertir a esas familias no está peleando el pastel. Está horneando uno más grande.'),
 ('h2', '7. Cómo se hace: modelo, sistema, escala'),
 ('p', 'Lo que necesitan los colegios no es más vocación ni más esfuerzo. Es saber venderse, y venderse bien es un sistema, no una temporada. El orden que he visto funcionar es siempre el mismo.'),
 ('lista', ['Primero se revisa el modelo de negocio. Capacidad, matrícula, colegiatura, permanencia, valor de vida de un alumno, costo por alumno nuevo. Son diez números, y la mayoría de los colegios no los tiene a la mano. Sin ellos, cualquier decisión comercial es una corazonada.',
            'Luego se parametriza el sistema de inscripciones. Cada etapa del embudo con un responsable, un tiempo máximo de respuesta y una conversión medida. Cada prospecto trazado desde el primer mensaje hasta la firma, sin depender de la memoria de nadie. El cuello de botella se ve en un tablero, no se descubre en agosto.',
            'Y con eso se escala. El mismo número de familias interesadas produce más alumnos inscritos. El sistema no cambia cuántas familias llegan, eso lo hace la publicidad. Cambia cuántas se quedan, y eso ningún presupuesto de publicidad lo puede comprar.']),
 ('p', 'En el corte de octubre, subir un solo punto la conversión vale $109,500 MXN al año para la institución mediana. Es el crecimiento más barato que existe, porque las familias ya llegaron. Y la brecha entre lo que el director cree y lo que mide (44 % califica su marketing de muy bueno mientras 64 % opera abajo del 60 % de ocupación) es la primera cosa que se cierra cuando los números están sobre la mesa.'),
 ('fig', 'X10'),
 ('fig', 'X18'),
 ('h2', 'Cierre'),
 ('p', 'El mercado ya hizo su parte. Las familias existen, el poder de pago existe, la demografía empuja y la oferta tiene espacio. La parte que falta no ocurre en el mercado: ocurre dentro de cada institución, en el tramo silencioso entre el primer «buenas tardes, quisiera informes» y la firma de la inscripción.'),
 ('p', 'La vida es más fácil cuando tienes tecnología, metodología, soporte y estrategia implementados en tu institución educativa. No porque te quiten trabajo, sino porque dejan de depender de la memoria, del teléfono de una persona y de la suerte de la temporada. A eso me dedico en SuperLeads, y es lo que hacemos en cada Rayos X de Inscripciones: en una sesión, poner los números del colegio como tienen que estar y ver, por fin, dónde está la fuga, qué la provoca y qué corregir primero.'),
 ('p', 'Si diriges un colegio, te pido una sola cosa después de leer esto: sé más ambicioso. El país te necesita lleno. Y si quieres platicarlo conmigo, escríbeme: ricardo@superleads.mx.'),
 ('h2', 'Fuentes'),
 ('p', 'Banco Mundial, matrícula primaria privada (indicador SE.PRM.PRIV.ZS); UNESCO UIS, matrícula por tipo de sostenimiento; AMAI, Regla NSE 2024; INEGI, ENIGH; APEIM, Niveles Socioeconómicos 2025 (Perú); SEP / SIGED, catálogo de centros de trabajo y RVOE; Minedu Perú, INEP Brasil, Mineduc Chile, MEN Colombia, NCES; rankings de colegiaturas 2025-2026 de CDMX, Lima, Bogotá, Santiago, São Paulo, Guatemala y Washington DC; IMCO, Índice de Competitividad Urbana 2026; CONAPO, ONU-Habitat; UPCEA, Enrollment Process Review: Secret Shopper Analysis 2025 (1,000 consultas a instituciones educativas); MIT / InsideSales.com, Lead Response Management Study (James Oldroyd); Harvard Business Review, «The Short Life of Online Sales Leads»; Asociación de Internet MX, Estudio de Hábitos de Usuarios de Internet en México; BrightLocal, Local Consumer Review Survey 2024-2026; Northwestern University / Spiegel Research Center; Shortway, Marketing para escuelas privadas, Guía 2026; Think with Google / SEMrush; SuperLeads, corte Rayos X de Inscripciones del 29 de octubre de 2026 (102 instituciones, 69 ciudades). Estimaciones de planteles físicos y promedios por colegio elaboradas por SuperLeads a partir de censos oficiales. Metodología completa a solicitud: ricardo@superleads.mx.'),
 ])
ARTICULOS = [A1, A2, A3]

# ───────────── salida ─────────────
def md_y_txt(a, figs):
    """figs: {clave: (ruta relativa de la imagen, pie de figura)}"""
    md = [f'# {a["titulo"]}', '', f'*{a["subtitulo"]}*', '', f'Por {AUTOR}', '']; txt = [a['titulo'], '', a['subtitulo'], '', f'Por {AUTOR}', '']
    k = 0
    for tipo, c in a['bloques']:
        if tipo == 'h2': md += [f'## {c}', '']; txt += [c.upper(), '']
        elif tipo == 'p': md += [c, '']; txt += [c, '']
        elif tipo == 'cita': md += [f'> {c}', '']; txt += [f'«{c}»', '']
        elif tipo == 'lista':
            md += [f'{i + 1}. {x}' for i, x in enumerate(c)] + ['']; txt += [f'{i + 1}. {x}' for i, x in enumerate(c)] + ['']
        elif tipo == 'fig':
            k += 1; ruta, pie = figs[c]
            md += [f'![{pie}]({ruta})', '', f'*Figura {k}. {pie}*', '']; txt += [f'[IMAGEN {k:02d} · {os.path.basename(ruta)}]', f'Figura {k}. {pie}', '']
    md += ['---', '', FIRMA, ''] + [f'**{FIRMA_NOMBRE[0]}**  '] + [f'{x}  ' for x in FIRMA_NOMBRE[1:]] + ['']; txt += ['', FIRMA, ''] + FIRMA_NOMBRE
    return '\n'.join(md), '\n'.join(txt)

if __name__ == '__main__':
    os.makedirs(SALIDA, exist_ok=True); os.makedirs(HTMLD, exist_ok=True); os.makedirs(DESCARGAS, exist_ok=True)
    render.FORMATO = 'articulo'
    ch = render.Chrome(alto=900, ancho=1600, dpr=2); resumen = []  # 2× para Retina: PNG de 3200×1800
    try:
        for a in ARTICULOS:
            carpeta = os.path.join(SALIDA, f'Artículo {a["n"]} · {a["slug"]}'); shutil.rmtree(carpeta, ignore_errors=True); os.makedirs(os.path.join(carpeta, 'imagenes'))
            figs = {}; k = 0; avisos = []
            for tipo, c in a['bloques']:
                if tipo != 'fig' or c in figs: continue
                k += 1; p = PIEZA[(c[0], int(c[1:]))]
                ruta_html = os.path.join(HTMLD, f'A{a["n"]}_{c}.html'); open(ruta_html, 'w').write(lamina_articulo(p)); ch.abrir('file://' + ruta_html)
                escala = ch.eval('anim(99); fit()')
                nombre = f'{k:02d} · {p["slug"]}.png'; ch.foto(os.path.join(carpeta, 'imagenes', nombre))
                if escala and escala < .7: avisos.append(f'{c} escala {escala:.2f}')
                fuente = 'SuperLeads, corte Rayos X de Inscripciones del 29 de octubre de 2026 (102 instituciones privadas en 69 ciudades de México; mediana, no promedio).' if c[0] == 'X' else (p.get('nota') or '')
                pie = re.sub('<[^>]+>', '', p['h1']).replace(' .', '.') + ' Fuente: ' + fuente
                figs[c] = (f'imagenes/{nombre}', pie)
            for nombre, (w, h_, sub) in {'portada 16x9': (1600, 900, True), 'portada 5x2 X': (2000, 800, False)}.items():
                ch.send('Emulation.setDeviceMetricsOverride', width=w, height=h_, deviceScaleFactor=2 if w == 1600 else 1.5, mobile=False)
                rp = os.path.join(HTMLD, f'A{a["n"]}_{nombre[:7].strip()}.html'); open(rp, 'w').write(lamina_portada_art(a, w, h_, sub)); ch.abrir('file://' + rp)
                ch.foto(os.path.join(carpeta, f'{nombre}.png'))
            ch.send('Emulation.setDeviceMetricsOverride', width=1600, height=900, deviceScaleFactor=2, mobile=False)
            pub = dict(n=a['n'], titulo=a['titulo'], subtitulo=a['subtitulo'], portada=os.path.join(carpeta, 'portada 16x9.png'), portada_x=os.path.join(carpeta, 'portada 5x2 X.png'),
                       bloques=[[t, (os.path.join(carpeta, figs[c][0]) if t == 'fig' else c), (figs[c][1] if t == 'fig' else None)] for t, c in a['bloques']],
                       cierre=[FIRMA] + FIRMA_NOMBRE)
            json.dump(pub, open(os.path.join(carpeta, 'publicar.json'), 'w'), ensure_ascii=False, indent=1)
            md, txt = md_y_txt(a, figs)
            base = f'Artículo {a["n"]} · {a["slug"]} · {VERSION} · {SELLO}'
            open(os.path.join(carpeta, base + '.md'), 'w').write(md); open(os.path.join(carpeta, base + '.txt'), 'w').write(txt)
            palabras = len(re.findall(r'\w+', ' '.join(c if isinstance(c, str) else ' '.join(c) for t, c in a['bloques'] if t != 'fig')))
            resumen.append(dict(n=a['n'], titulo=a['titulo'], palabras=palabras, figuras=k, carpeta=os.path.basename(carpeta), avisos=avisos))
            print(f'{a["n"]} · {palabras} palabras · {k} figuras · {a["titulo"]}' + (f'  ⚠ {avisos}' if avisos else ''))
    finally: ch.cerrar()
    guia = [f'# LinkedIn · tres artículos · {VERSION} · {SELLO}', '', 'Formato «artículo» de LinkedIn (no post). Sin publicar: Ricardo revisa.', '',
            '| # | Artículo | Palabras | Figuras |', '|---|---|---|---|'] + [f"| {r['n']} | {r['titulo']} | {r['palabras']} | {r['figuras']} |" for r in resumen] + ['',
            'Cada carpeta trae el texto en Markdown (con las imágenes en su lugar) y en TXT (con marcas [IMAGEN NN] donde va cada una), y la carpeta `imagenes/` con las gráficas en 1600×900: título arriba, nombre de Ricardo abajo a la izquierda y SuperLeads abajo a la derecha.', '',
            'Para armarlo en LinkedIn: Escribir artículo → pegar el TXT → en cada marca [IMAGEN NN] insertar la imagen correspondiente y poner la «Figura N» como pie. La imagen 01 de cada artículo sirve de portada.', '',
            f'Firma al final de cada artículo: {FIRMA} / ' + ' · '.join(FIRMA_NOMBRE), '']
    open(os.path.join(SALIDA, f'GUÍA tres artículos · {VERSION} · {SELLO}.md'), 'w').write('\n'.join(guia)); json.dump(resumen, open(os.path.join(SALIDA, 'resumen.json'), 'w'), ensure_ascii=False, indent=1)
    for f in glob.glob(os.path.join(DESCARGAS, '*')): shutil.rmtree(f) if os.path.isdir(f) else os.remove(f)
    for f in glob.glob(os.path.join(SALIDA, '*')): (shutil.copytree if os.path.isdir(f) else shutil.copy)(f, os.path.join(DESCARGAS, os.path.basename(f)))
    print(len(resumen), 'artículos →', DESCARGAS)
# Ricardo López Reyero · EYE · 181218
