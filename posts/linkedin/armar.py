"""LinkedIn: un artículo semanal (carrusel PDF 1080×1350 + texto) que agrupa 2–5 gráficas relacionadas de las dos series,
con liga al video de YouTube de cada gráfica. Primero «Rayos X · corte octubre 2026» (6 semanas), luego «La realidad de la educación» (7).
Uso: python3 armar.py            → salida/ (PDF, PNG de cada lámina, TXT del post) + copia en ~/Downloads/LinkedIn/
     SOLO=3 python3 armar.py     → solo el artículo 3
Nada se publica desde aquí: Ricardo revisa y decide. Ricardo López Reyero · RLR"""
import os, sys, json, glob, datetime, shutil, html, re
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__)); POSTS = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(POSTS, 'estadisticas')); sys.path.insert(0, os.path.join(POSTS, 'rayosx_corte'))
import render, serie as S
sys.argv = ['piezas.py', '2026-10-29']; import piezas as X  # noqa: E402  (carga el corte sin renderizar)

SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M'); VERSION = 'v1'
SALIDA = os.path.join(AQUI, 'salida'); HTMLD = os.path.join(AQUI, 'html'); DESCARGAS = os.path.expanduser('~/Downloads/LinkedIn')
PIEZA = {('R', p['n']): p for p in S.P}; PIEZA.update({('X', p['n']): p for p in X.P})
PIE = {'R': ('', 'Serie · La realidad de la educación'), 'X': ('', f'Serie · Rayos X · corte {X.MES} {X.ANIO}')}
CORTO = {'R': 'LA REALIDAD DE LA EDUCACIÓN', 'X': X.SERIES[4]['corto']}
HASH_SERIE = {'R': S.HASH_SERIE, 'X': '#SerieRayosX'}

# ligas y fechas de YouTube (ya programadas) desde el calendario
cal = json.load(open(sorted(glob.glob(os.path.join(POSTS, 'calendario', 'Calendario series · v2 · *.json')))[-1]))
YT = {('X' if c['serie'].startswith('Rayos') else 'R', c['n']): c for c in cal}

MUESTRA_X = (f"Son {X.N} instituciones privadas en {X.CIU} ciudades que pidieron el diagnóstico entre {X.PERIODO}: es nuestra muestra, no el país. "
             "Y publicamos mediana, no promedio: un colegio de 7,000 alumnos mueve el promedio y miente.")
CTA_X = 'Si quieres saber en qué lugar de estos números está tu institución, el Rayos X de Inscripciones lo dice con tus datos: https://superleads.mx/rayos_x'
CTA_R = 'Cada gráfica tiene su fuente al pie y el documento completo, con metodología, se entrega a solicitud: hola@superleads.mx'
FIRMA = 'Ing. Ricardo López Reyero · Founder Comercial de SuperLeads. Solo hacemos admisiones: por nuestro sistema pasan más de 300,000 prospectos educativos al año.'

# ───────────── los artículos: una historia por semana ─────────────
ARTICULOS = [
 dict(serie='X', slug='La mitad del colegio esta vacia', titulo='La mitad del colegio está vacía', piezas=[1, 2, 3],
      portada_sub='102 Rayos X de Inscripciones en 69 ciudades. Primera entrega del corte: quiénes son y cuánta de su capacidad están usando.',
      gancho='La escuela privada mediana en México opera al 46% de su capacidad. No es un colegio en crisis: es la mitad de la muestra.',
      cuerpo=['Entre marzo y octubre de 2026 hicimos 102 Rayos X de Inscripciones con dueños y directores de instituciones privadas en 69 ciudades de México: 35 colegios con primaria, 14 con preparatoria y 42 universidades y posgrados. Esta es la primera entrega del corte.',
              'El dato que abre la serie es la ocupación. La institución mediana usa 46 de cada 100 lugares que construyó. Sumando las 98 que reportaron el dato, son 59,507 lugares vacíos: aulas hechas, maestros contratados, sillas sin alumno. Puesto en pesos, esa capacidad sin usar vale $279.6 millones MXN al año.',
              'Lo que más me llama la atención no es el número sino la normalidad con la que se vive. Nadie abre un colegio para llenarlo a la mitad; se llega ahí un ciclo a la vez, con una familia que no contestó y otra que llegó tarde a la cita. La infraestructura ya está pagada. Lo único que falta es el alumno, y el alumno sí preguntó.'],
      pregunta='¿Qué porcentaje de tu capacidad está ocupado hoy? Si estás abajo del 60%, estás con la mayoría. La pregunta es si quieres quedarte ahí.',
      cierre='El colegio no está medio vacío. <em>Está medio vendido.</em>', hashtags='#Ocupación #EducaciónPrivada'),
 dict(serie='X', slug='El problema esta antes de la cita', titulo='El problema está antes de la cita', piezas=[4, 5, 6],
      portada_sub='Prospectos, conversión y cierre: el embudo de admisiones de la escuela privada mexicana, con datos de 102 Rayos X.',
      gancho='La escuela privada mediana recibe 8 prospectos al día e inscribe al 2.4%. Pero cuando la familia llega a la cita, 40% se inscribe. El problema no está en la cita.',
      cuerpo=['Segunda entrega del corte: el embudo. Cuántas familias preguntan, cuántas se inscriben y en qué punto se pierden las demás.',
              'La institución mediana recibe 8 prospectos al día (15 las universidades). De cada 100 que preguntan, 2.4 se inscriben. Y sin embargo, de las familias que sí llegan a la cita o al recorrido, 40% termina inscribiéndose.',
              'Esas tres cifras juntas dicen algo incómodo: el colegio sabe vender cuando tiene a la familia enfrente. Lo que no sabe es llevarla hasta ahí. Entre el primer mensaje y la cita se evapora la mayor parte de la demanda, y casi nunca por precio: por tiempo de respuesta, por seguimiento, por un «ahorita le contesto» que se volvió nunca.'],
      pregunta='¿Sabes, con número, cuántas de tus consultas llegan a una cita? Ese porcentaje es tu negocio.',
      cierre='La inscripción no se pierde en la cita. <em>Se pierde en el camino a ella.</em>', hashtags='#Conversión #Prospectos'),
 dict(serie='X', slug='Cuanto vale un alumno y cuanto cuesta', titulo='Cuánto vale un alumno y cuánto cuesta', piezas=[7, 8, 9, 10],
      portada_sub='Colegiatura, valor de vida, publicidad y el precio de un punto de conversión. Todo en pesos, mediana de 102 Rayos X.',
      gancho='Un alumno cuesta $1,381 MXN en publicidad y vale $144,000 MXN a lo largo de su permanencia. La publicidad no es el problema: lo que se compra con ella se pierde después.',
      cuerpo=['Tercera entrega del corte: el dinero. Cuánto cobra la escuela privada, cuánto vale cada alumno, cuánto invierte en publicidad y cuánto deja de ganar por cada punto de conversión.',
              'La colegiatura mediana es $3,300 MXN al mes. El valor de vida mediano de un alumno (colegiatura por meses de permanencia) es $144,000 MXN. La institución mediana invierte $8,000 MXN al mes en publicidad; cada prospecto le cuesta $41 MXN y cada alumno inscrito $1,381 MXN.',
              'Con esa relación entre costo y valor, la publicidad educativa es de las inversiones más rentables que existen. El problema no es cuánto se invierte sino cuánto de lo comprado se evapora. Y por eso la última gráfica es la que más importa: subir un solo punto la conversión vale $109,500 MXN al año para la institución mediana. Sin un peso más de anuncios.'],
      pregunta='¿Cuánto vale un punto de conversión en tu colegio? Multiplica tus prospectos del año por 1% y por el valor de vida de un alumno.',
      cierre='La publicidad no es cara. <em>Caro es lo que se pierde después de pagarla.</em>', hashtags='#Colegiatura #ValorDeVida'),
 dict(serie='X', slug='Becas recomendacion y lo demas', titulo='Becas, recomendación y lo demás', piezas=[11, 12, 19],
      portada_sub='Cuánto se beca, cuántos alumnos llegan por recomendación sin que nadie la pida, y qué más cobra el colegio además de la colegiatura.',
      gancho='40% de los alumnos de la escuela privada llega por recomendación. 70% de los colegios no tiene un programa de recomendados. El canal más barato es el que nadie trabaja.',
      cuerpo=['Quinta entrega del corte: las palancas que casi nadie mide. Becas, recomendación y los ingresos además de la colegiatura.',
              '68% de las instituciones da becas y la mediana tiene 40% de alumnos becados: la beca es ya una herramienta comercial, no una excepción. 40% de los alumnos llega por recomendación de otra familia, y aun así 70% de los colegios no tiene un programa para pedirla. Y en monetización, cafetería (69%) y graduaciones (60%) son casi universales; el transporte, apenas 17%.',
              'Las tres gráficas cuentan la misma historia: el colegio ya tiene activos que valen dinero (familias contentas, alumnos becados que llenan lugares, servicios que la familia quiere pagar) y los administra por costumbre, no por diseño. La recomendación es el ejemplo más claro: tus familias quieren recomendarte y nadie les dice cómo.'],
      pregunta='¿Cuántas familias inscribiste el ciclo pasado porque alguien te recomendó? ¿Y a cuántas de ellas les diste las gracias con algo concreto?',
      cierre='Tus mejores vendedoras ya pagan colegiatura. <em>Nadie les ha pedido que vendan.</em>', hashtags='#Becas #Recomendación'),
 dict(serie='X', slug='La maquina de admisiones', titulo='La máquina de admisiones', piezas=[13, 14, 15, 16],
      portada_sub='Herramientas, equipo, plan de compensación y los meses en que se inscribe: cómo está armada la operación comercial del colegio privado.',
      gancho='71% de las escuelas privadas lleva sus admisiones en WhatsApp o Excel. Con 1.1 persona. Sin plan de compensación en casi la mitad. Y todo se decide en dos meses.',
      cuerpo=['Cuarta entrega del corte: la máquina. Con qué herramientas, con cuánta gente, con qué incentivos y en qué meses se inscribe la escuela privada mexicana.',
              '71% de las instituciones lleva las admisiones en WhatsApp o Excel; solo 29% tiene un CRM. El equipo de admisiones del colegio mediano es de 1.1 persona (6 en la universidad mediana). 48% no tiene plan de compensación para ese equipo. Y la inscripción se concentra en julio y agosto.',
              'Es una operación de temporada alta atendida por una persona, con memoria en un teléfono y sin incentivo por inscribir. No es falta de talento: es falta de sistema. El CRM es la memoria comercial del colegio; cuando se va el asesor, se la lleva.'],
      pregunta='Si mañana se va la persona que lleva tus admisiones, ¿qué se queda en el colegio y qué se va con ella?',
      cierre='No es falta de talento. <em>Es falta de sistema.</em>', hashtags='#CRMEducativo #Admisiones'),
 dict(serie='X', slug='Lo que el director cree', titulo='Lo que el director cree', piezas=[17, 18],
      portada_sub='Por qué no se inscriben las familias según quien dirige el colegio, y cómo califica su propio marketing frente a su ocupación real.',
      gancho='62% de los directores culpa al precio cuando una familia no se inscribe. 38% admite falta de seguimiento. 44% califica su marketing de muy bueno; 64% opera abajo del 60% de ocupación.',
      cuerpo=['Sexta y última entrega del corte de octubre: lo que el director cree. Aquí no hay mediciones, hay creencias, y por eso lo decimos así.',
              'Cuando preguntamos por qué no se inscribieron las familias, la causa más mencionada es el precio (62%); la segunda, la falta de seguimiento (38%). La primera no depende de nadie; la segunda está completamente bajo el control del colegio. Y cuando preguntamos por el marketing, 44% lo califica de muy bueno o excelente, mientras 64% de las instituciones opera abajo del 60% de su capacidad.',
              'Con una colegiatura mediana de $3,300 MXN y 13.4 millones de hogares que pueden pagarla, el precio rara vez es el motivo. El silencio, casi siempre. La brecha entre percepción y realidad es, probablemente, la gráfica más importante de todo el corte: no se arregla lo que no se ve.'],
      pregunta='¿Tu colegio mide por qué no se inscriben las familias, o lo supone?',
      cierre='El precio es la excusa que no depende de nadie. <em>El silencio es la causa que depende de ti.</em>', hashtags='#Dirección #Marketing'),
 dict(serie='R', slug='Lo que aprenden', titulo='Lo que aprenden', piezas=[1, 2, 11, 7],
      portada_sub='Nueva serie: la realidad de la educación en México, con fuentes. Capítulo 1: los aprendizajes, de PISA a la secundaria.',
      gancho='México es el lugar 35 de 37 en PISA. 66% de los alumnos de 15 años no alcanza el nivel básico de Matemáticas. 8 de cada 10 de 3° de secundaria no desarrollaron los aprendizajes esperados.',
      cuerpo=['Terminamos el corte de los Rayos X y empieza la segunda serie: la realidad de la educación en México, con las fuentes al pie. Primer capítulo: lo que los alumnos aprenden, o no.',
              'En PISA 2022 México quedó en el lugar 35 de 37 países de la OCDE, 77 puntos abajo del promedio en Matemáticas. 66% de los alumnos de 15 años no alcanza el nivel básico. En 3° de secundaria, 8 de cada 10 no desarrollaron los aprendizajes esperados. Y el país necesita 400,000 maestros de inglés: tiene 80,000.',
              'No son opiniones: son las mediciones oficiales e internacionales que todavía existen. Las pongo juntas porque cada una se discute por separado y así se diluye. Vistas en una sola página, cuentan la historia de la demanda que llega a la escuela privada: familias que ya saben que la pública no les alcanza.'],
      pregunta='Cuando una familia te pregunta «¿y por qué pagar?», ¿tu colegio contesta con esto en una frase?',
      cierre='Cada punto que pierde la escuela pública <em>es una familia buscando a dónde ir.</em>', hashtags='#PISA2022 #EducaciónMéxico'),
 dict(serie='R', slug='Donde aprenden y con que', titulo='Dónde aprenden y con qué', piezas=[3, 4, 8, 9],
      portada_sub='Capítulo 2 de la realidad de la educación: infraestructura, conectividad y el dinero que el país pone por cada alumno.',
      gancho='40% de las escuelas públicas opera sin agua, luz o sanitarios dignos. 65 de cada 100 no tienen computadora ni internet. México es último de la OCDE en gasto por alumno.',
      cuerpo=['Segundo capítulo: el lugar donde se aprende y los recursos con los que se aprende.',
              '40% de las escuelas públicas opera sin agua, luz o sanitarios dignos. 65 de cada 100 no tienen computadoras ni internet. México invierte $2,933 USD al año por alumno de primaria, el último lugar de la OCDE. Y las familias ya pagan 16.2% del gasto educativo público de su bolsillo, frente a 9.9% en el promedio de la OCDE.',
              'La última cifra es la que cambia la conversación: la escuela gratuita no lo es. La familia mexicana ya está pagando por educación; la pregunta es a quién le paga y qué recibe a cambio. Para el colegio privado eso no es una amenaza. Es la definición de su mercado.'],
      pregunta='Si la familia ya paga, ¿qué le ofrece tu colegio que la pública no puede, dicho en una frase?',
      cierre='La escuela gratuita no lo es. <em>La familia ya paga; la pregunta es a quién.</em>', hashtags='#Infraestructura #GastoEducativo'),
 dict(serie='R', slug='Quien ensena y quien mide', titulo='Quién enseña y quién mide', piezas=[5, 6, 10],
      portada_sub='Capítulo 3: el ingreso del maestro, los paros que dejan niños sin clases y la cronología de cómo el país dejó de medir.',
      gancho='El maestro mexicano promedio gana $7,890 MXN al mes, menos que el salario mínimo. En junio de 2026, 1,410,459 niños se quedaron sin clases. Y desde 2019 el país apagó sus termómetros.',
      cuerpo=['Tercer y último capítulo sobre la educación pública: quién enseña, qué pasa cuando no está y quién mide el resultado.',
              'El ingreso mensual promedio de un docente en México es $7,890 MXN, por debajo del salario mínimo (incluye jornadas parciales e informalidad; los docentes formales de tiempo completo rondan los $18,000 MXN, aún abajo del promedio OCDE). El paro de la CNTE de junio de 2026 dejó 1,410,459 niños sin clases según la SEP. Y la cronología 2019, 2025, 2026 muestra cómo México dejó de medir su educación.',
              'Te pago poco, no te formo, no te evalúo: la desmotivación no es un defecto del magisterio, es la respuesta racional a esos incentivos. Y un país que rompe sus termómetros no cura la fiebre; solo deja de verla.'],
      pregunta='¿Qué mide tu colegio cada ciclo que la escuela pública ya no mide?',
      cierre='Un país que rompe sus termómetros no cura la fiebre. <em>Solo deja de verla.</em>', hashtags='#Docentes #CNTE'),
 dict(serie='R', slug='Como elige una familia', titulo='Cómo elige una familia', piezas=[20, 13, 18, 21],
      portada_sub='La boleta invisible, capítulo 1: cuánto tarda la decisión, a qué hora ocurre, qué peso tienen las reseñas y qué tan cerca busca la familia.',
      gancho='Una familia tarda 6 meses en elegir colegio y la mitad de la decisión ocurre sin que el colegio lo sepa. 93% investiga entre las 9 de la noche y la medianoche. El colegio cierra a las 3.',
      cuerpo=['Nueva serie dentro de la serie: la boleta invisible, cómo deciden las familias. Primer capítulo: el proceso de decisión.',
              'La decisión toma 6 meses y pasa por 5 etapas; la mitad ocurre antes de que el colegio se entere. 93% de las familias está conectada entre 9 de la noche y medianoche, cuando el colegio lleva horas cerrado. 71% descarta un colegio con menos de 3 estrellas y el rango que más confianza genera es 4.2 a 4.5. Y 46% de las búsquedas en Google es local: 76% de quienes buscan «cerca de mí» visitan en 24 horas.',
              'La familia decide de noche, con el teléfono, leyendo lo que otras familias dijeron de ti y buscando lo que le queda cerca. El colegio compite en un horario y en un canal que no son los suyos. Quien aparece en ese momento, con una respuesta, se queda con la cita.'],
      pregunta='¿Qué ve una familia de tu colegio a las 10 de la noche, desde su teléfono, antes de escribirte?',
      cierre='La familia decide de noche, con el teléfono. <em>El colegio abre a las ocho.</em>', hashtags='#BoletaInvisible #Familias'),
 dict(serie='R', slug='La velocidad es la estrategia', titulo='La velocidad es la estrategia', piezas=[12, 14, 15, 19],
      portada_sub='La boleta invisible, capítulo 2: qué pasa cuando la familia escribe y nadie contesta, y por qué los minutos deciden la inscripción.',
      gancho='44% de las consultas a colegios jamás recibe respuesta. 78% de las familias le compra al primero que responde. Solo 7% responde en 5 minutos.',
      cuerpo=['Segundo capítulo de la boleta invisible: la velocidad.',
              'En un estudio con 1,000 consultas a colegios, 44% jamás recibió respuesta. 78% de los compradores le compra al primero que responde, y solo 7% de las organizaciones contesta en los primeros 5 minutos. Responder en 5 minutos hace 21 veces más probable calificar al prospecto que hacerlo a los 30. Y en México el canal es uno: WhatsApp se abre 98% de las veces; el correo, 21%.',
              'La publicidad compra interés; solo el proceso lo convierte. No se pierde por falta de demanda, ni de prestigio, ni de anuncios: se pierde por velocidad. Y capturar a una familia que ya escribió cuesta $0 MXN en publicidad. Solo requiere proceso.'],
      pregunta='¿Cuánto tarda hoy tu colegio en contestar el primer WhatsApp de una familia? Mídelo esta semana, con reloj.',
      cierre='No gana el mejor colegio. <em>Gana el primero que contesta.</em>', hashtags='#TiempoDeRespuesta #WhatsApp'),
 dict(serie='R', slug='La matematica del silencio', titulo='La matemática del silencio', piezas=[16, 17],
      portada_sub='La boleta invisible, capítulo 3: cuánto cuesta un WhatsApp sin contestar y qué cambia con las mismas 40 familias cuando se responde en minutos.',
      gancho='Un WhatsApp sin contestar cuesta $450,000 MXN. Las mismas 40 familias: 4 inscripciones respondiendo en horas, 10 respondiendo en minutos.',
      cuerpo=['Tercer capítulo de la boleta invisible: ponerle número al silencio. Son dos modelos con supuestos conservadores de un colegio típico, y así los declaramos.',
              'Colegiatura de $4,500 MXN al mes, seis años de permanencia y la probabilidad de hermano que todo director conoce: alrededor de $450,000 MXN por familia inscrita. Ese es el precio de cada mensaje que se enfrió. Y con las mismas 40 consultas, el colegio que responde en horas inscribe 4; el que responde en minutos, 10. La diferencia son 6 familias: $2.7 millones MXN de valor de vida por temporada.',
              'Es el hallazgo que más sorprende a los directores en nuestros diagnósticos: el crecimiento más barato del colegio no está en conseguir más mensajes. Está en dejar de perder los que ya llegan.'],
      pregunta='¿Cuántas familias se enfriaron en tu colegio el ciclo pasado? Multiplica por $450,000 MXN.',
      cierre='Cada «ahorita le contesto» tiene precio. <em>Y ya lo estás pagando.</em>', hashtags='#ValorDeVida #Seguimiento'),
 dict(serie='R', slug='El mercado que nadie esta atendiendo', titulo='El mercado que nadie está atendiendo', piezas=[22, 23, 24, 25, 26],
      portada_sub='Capítulo final: la educación privada en Latinoamérica y el tamaño real del mercado mexicano, con cinco gráficas.',
      gancho='35% de los hogares mexicanos puede pagar colegio privado. Solo 10% inscribe. En Perú, 10% puede pagar y 26% inscribe.',
      cuerpo=['Cierre de la serie: el mercado. Cinco gráficas sobre cuánto espacio hay para crecer en la educación privada mexicana.',
              'Solo 10% de los alumnos de México está en escuela privada, la penetración más baja de Latinoamérica. 13.4 millones de hogares pueden pagar un colegio privado. Perú, con 10% de hogares que pueden pagar, inscribe al 26%; México, con 35%, inscribe al 10%. El país no tiene 45,000 colegios privados: tiene unos 20,000 planteles con 260 alumnos en promedio. Y los 10 colegios más caros de la Ciudad de México cobran $1,050 USD al mes, lo mismo que los de Lima y Bogotá, en una economía mayor.',
              'En México hay más familias que pueden pagar colegio privado que familias que lo están pagando. Esa brecha es el techo de crecimiento de todo el sector. La lección peruana es brutal y liberadora: cuando una familia cree que la educación de sus hijos lo vale, encuentra cómo pagarla. La pregunta nunca fue si pueden. Es a quién se la pagan.'],
      pregunta='¿Tu colegio compite contra el de enfrente, o contra la opción de no pagar?',
      cierre='La pregunta nunca fue si pueden pagar. <em>Es a quién le pagan.</em>', hashtags='#EducaciónPrivada #Latinoamérica'),
]
HORA = '09:00'
# Ricardo (30-oct): «aprieta un poco más… el 15 de enero estaré terminando». Dos por semana (martes y jueves) mientras los Shorts
# de cada gráfica ya estén públicos; pausa del 24-dic al 6-ene; la serie termina el 14-ene-2027.
FECHAS = {'La mitad del colegio esta vacia': (2026, 11, 5), 'El problema esta antes de la cita': (2026, 11, 10), 'Cuanto vale un alumno y cuanto cuesta': (2026, 11, 12),
          'La maquina de admisiones': (2026, 11, 19), 'Becas recomendacion y lo demas': (2026, 11, 24), 'Lo que el director cree': (2026, 11, 26),
          'Lo que aprenden': (2026, 12, 3), 'Donde aprenden y con que': (2026, 12, 8), 'Quien ensena y quien mide': (2026, 12, 10),
          'Como elige una familia': (2026, 12, 17), 'La velocidad es la estrategia': (2026, 12, 22), 'La matematica del silencio': (2027, 1, 7),
          'El mercado que nadie esta atendiendo': (2027, 1, 14)}
ARTICULOS.sort(key=lambda a: FECHAS[a['slug']])
for i, a in enumerate(ARTICULOS): a['n'] = i + 1; a['fecha'] = datetime.date(*FECHAS[a['slug']])

# ───────────── láminas: portada y cierre ─────────────
CSS_EXTRA = """
.port{position:absolute;top:200px;left:80px;right:80px}
.port h1{font-size:88px;line-height:1.02;letter-spacing:-3px;margin:0 0 40px;font-weight:800}
.port .sub{font-size:33px;line-height:1.38;color:var(--t2);font-weight:500}
.port .tag{display:inline-block;margin-top:56px;padding:14px 22px;border:1.5px solid rgba(255,255,255,.35);border-radius:14px;font-size:21px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#fff}
.desliza{position:absolute;left:80px;bottom:190px;font-size:24px;font-weight:700;letter-spacing:3px;text-transform:uppercase;color:var(--green)}
.fin{position:absolute;top:0;bottom:0;left:80px;right:80px;display:flex;flex-direction:column;justify-content:center;padding-bottom:40px}
.fin .raya{width:72px;height:6px;border-radius:3px;background:var(--green);margin-bottom:44px}
.fin h2{font-size:78px;line-height:1.08;letter-spacing:-2.6px;margin:0;font-weight:800}
.fin h2 em{font-style:italic;color:var(--green)}
.fin .cta{font-size:27px;line-height:1.4;color:#fff;font-weight:600;margin-bottom:12px}
.fin .cta b{color:var(--green);font-weight:800}
.fin .fuentes{margin-top:34px;border-top:.5px solid rgba(255,255,255,.18);padding-top:22px}
.fin .fuentes .t{font-size:17px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--t3);margin-bottom:12px}
.fin .fuentes p{margin:0 0 10px;font-size:inherit;line-height:1.4;color:var(--t3)}
"""
def cabeza(serie):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{render.CSS}{render.CSS_LI}{CSS_EXTRA}</style></head><body data-author="RLR">'
            f'<div class="fondo"><div class="g1"></div><div class="g2"></div></div>'
            f'<header><div class="marca"><img class="nombre" src="{render.LOGO_RLR_N}" alt="Ricardo López Reyero"></div><div class="serie">{html.escape(CORTO[serie])}</div></header>')
def pie(serie): return f'<footer><img src="{render.LOGO}" alt="SuperLeads"><span>{html.escape(PIE[serie][1])}</span></footer></body></html>'

def lamina_portada(a):
    n_x = sum(1 for b in ARTICULOS if b['serie'] == a['serie']); k = sum(1 for b in ARTICULOS if b['serie'] == a['serie'] and b['n'] <= a['n'])
    return (cabeza(a['serie']) + f'<div class="port"><div class="eyebrow"><span>Entrega {k} de {n_x} · {len(a["piezas"])} gráficas</span></div>'
            f'<h1>{html.escape(a["titulo"])}</h1><div class="sub">{html.escape(a["portada_sub"])}</div>'
            f'<div class="tag">{"Mediana, no promedio · " + str(X.N) + " Rayos X" if a["serie"] == "X" else "Con fuentes al pie"}</div></div>'
            f'<div class="desliza">Desliza →</div>' + pie(a['serie']))

def lamina_cierre(a):
    """Solo la frase de cierre: un cambio de perspectiva, elegante, sin más información (Ricardo, 30-oct). Fuentes y ligas van al primer comentario."""
    return cabeza(a['serie']) + f'<div class="fin"><div class="raya"></div><h2>{a["cierre"]}</h2></div>' + pie(a['serie'])

def primer_comentario(a):
    """Lo que salió de la lámina de cierre: las fuentes y el video de cada gráfica, para pegar como primer comentario."""
    s = a['serie']; L = ['Fuentes y método de las gráficas de este carrusel, y el video de cada una:', '']
    for i, n in enumerate(a['piezas']):
        p = PIEZA[(s, n)]; nota = p.get('nota_larga', p['nota'])
        L += [f"{i + 1}. {p['titulo']}", f"   Fuente: {nota}", f"   Video: {YT[(s, n)]['youtube_liga']}", '']
    L.append(CTA_X if s == 'X' else CTA_R)
    return '\n'.join(L)

# ───────────── texto del post ─────────────
def texto_post(a):
    s = a['serie']; lineas = [a['gancho'], ''] + sum([[p, ''] for p in a['cuerpo']], [])
    if s == 'X': lineas += [MUESTRA_X, '']
    lineas += [a['pregunta'], '', 'Las gráficas de este carrusel, con su video de 8 segundos en YouTube:']
    for i, n in enumerate(a['piezas']):
        lineas.append(f"{i + 1}. {PIEZA[(s, n)]['titulo']} → {YT[(s, n)]['youtube_liga']}")
    lineas += ['', CTA_X if s == 'X' else CTA_R, '', FIRMA, '', f"{S.HASH_BASE} {HASH_SERIE[s]} {a['hashtags']} #LinkedInEducación"]
    return '\n'.join(lineas)

def fecha_larga(d): return d.strftime('%d-%b-%Y').replace('Nov', 'nov').replace('Dec', 'dic').replace('Jan', 'ene')

# ───────────── armar ─────────────
if __name__ == '__main__':
    solo = os.environ.get('SOLO'); solo = int(solo) if solo else None
    os.makedirs(SALIDA, exist_ok=True); os.makedirs(HTMLD, exist_ok=True); os.makedirs(DESCARGAS, exist_ok=True)
    render.FORMATO = 'linkedin'; render.SERIES = {**S.SERIES, **X.SERIES}; render.P = S.P + X.P
    ch = render.Chrome(alto=1350); plan = []
    try:
        for a in ARTICULOS:
            if solo and a['n'] != solo: continue
            s = a['serie']; render.PIE = PIE[s]
            # la liga de YouTube de cada gráfica debe estar pública antes del post
            ult = max(datetime.date.fromisoformat(YT[(s, n)]['fecha']) for n in a['piezas']); assert ult < a['fecha'], (a['n'], ult, a['fecha'])
            txt = texto_post(a); assert len(txt) <= 3000, (a['n'], len(txt))
            base = f'Artículo {a["n"]:02d} · {a["slug"]} · {VERSION} · {SELLO}'
            carpeta = os.path.join(SALIDA, f'Artículo {a["n"]:02d} · {a["slug"]}'); shutil.rmtree(carpeta, ignore_errors=True); os.makedirs(os.path.join(carpeta, 'laminas'))
            laminas = [('portada', lamina_portada(a))] + [(f'grafica {i + 1}', render.pagina(PIEZA[(s, n)])) for i, n in enumerate(a['piezas'])] + [('cierre', lamina_cierre(a))]
            pngs = []; avisos = []
            for j, (nombre, h) in enumerate(laminas):
                ruta = os.path.join(HTMLD, f'A{a["n"]:02d}_{j + 1:02d}.html'); open(ruta, 'w').write(h); ch.abrir('file://' + ruta)
                if nombre.startswith('grafica'):
                    ch.eval('anim(99)'); fondo = ch.eval("document.querySelector('main').getBoundingClientRect().bottom")
                    if fondo > 1225: avisos.append(f'{nombre} fondo={fondo:.0f}')
                else:
                    fondo = ch.eval("(document.querySelector('.port,.fin h2')||{getBoundingClientRect:()=>({bottom:0})}).getBoundingClientRect().bottom")
                    if fondo > 1225: avisos.append(f'{nombre} fondo={fondo:.0f}')
                png = os.path.join(carpeta, 'laminas', f'{j + 1:02d} · {nombre}.png'); ch.foto(png); pngs.append(png)
            ims = [Image.open(p).convert('RGB') for p in pngs]
            pdf = os.path.join(carpeta, base + '.pdf'); ims[0].save(pdf, 'PDF', save_all=True, append_images=ims[1:], resolution=96, quality=92)
            open(os.path.join(carpeta, f'Texto del post · {VERSION} · {SELLO}.txt'), 'w').write(txt)
            open(os.path.join(carpeta, f'Primer comentario · fuentes y videos · {VERSION} · {SELLO}.txt'), 'w').write(primer_comentario(a))
            plan.append(dict(n=a['n'], serie=s, titulo=a['titulo'], fecha=a['fecha'].isoformat(), hora=HORA, laminas=len(laminas), piezas=[f"{s}{n:02d}" for n in a['piezas']],
                             videos=[YT[(s, n)]['youtube_liga'] for n in a['piezas']], pdf=os.path.basename(pdf), caracteres=len(txt), estado='planeado, sin publicar', avisos=avisos))
            print(f'{a["n"]:02d} {a["fecha"]} · {len(laminas)} láminas · {len(txt)} caracteres · {a["titulo"]}' + (f'  ⚠ {avisos}' if avisos else ''))
    finally: ch.cerrar()
    if not solo:
        json.dump(plan, open(os.path.join(SALIDA, 'plan.json'), 'w'), ensure_ascii=False, indent=1)
        md = [f'# LinkedIn · plan semanal · {VERSION} · {SELLO}', '',
              f'Un carrusel (PDF 1080×1350: portada, gráficas y una frase de cierre) y un texto, martes y jueves a las {HORA} (GMT-6) mientras los Shorts de cada gráfica ya estén públicos; pausa del 24-dic al 6-ene; termina el 14-ene-2027. '
              'Primero las 6 entregas del corte Rayos X, luego los 7 capítulos de La realidad de la educación. Cada gráfica lleva la liga a su Short de YouTube, '
              'que ya estará publicado antes de la fecha del post (se verifica al armar). **Nada está publicado: Ricardo revisa y decide.**', '',
              'Nota de LinkedIn: las ligas externas en el cuerpo bajan el alcance; si prefieres, el texto va sin ligas y la lista de videos se pega en el primer comentario.', '',
              '| # | Fecha | Serie | Artículo | Láminas | Gráficas | Caracteres |', '|---|---|---|---|---|---|---|']
        for p in plan:
            md.append(f"| {p['n']:02d} | {p['fecha']} {p['hora']} | {'Rayos X' if p['serie'] == 'X' else 'Realidad'} | {p['titulo']} | {p['laminas']} | {', '.join(p['piezas'])} | {p['caracteres']} |")
        md += ['', 'Las fuentes y la liga al video de cada gráfica van en `Primer comentario`, para pegar debajo del post; la lámina de cierre lleva solo la frase.', '',
               'Carpeta de cada artículo: el PDF del carrusel, `laminas/` (PNG de cada lámina), `Texto del post` y `Primer comentario` (fuentes y video de cada gráfica, para pegar debajo del post).', '']
        open(os.path.join(SALIDA, f'PLAN LinkedIn · {VERSION} · {SELLO}.md'), 'w').write('\n'.join(md))
        # copia a Descargas/LinkedIn (se reemplaza completa)
        for f in glob.glob(os.path.join(DESCARGAS, '*')): shutil.rmtree(f) if os.path.isdir(f) else os.remove(f)
        for f in glob.glob(os.path.join(SALIDA, '*')): (shutil.copytree if os.path.isdir(f) else shutil.copy)(f, os.path.join(DESCARGAS, os.path.basename(f)))
        print(len(plan), 'artículos →', DESCARGAS)
# Ricardo López Reyero · EYE · 181218
