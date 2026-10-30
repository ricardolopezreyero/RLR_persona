"""Serie «Corte Rayos X»: de cortes/<fecha>/agregados.json a las piezas (gráfico + texto) y su render.
Todos los números de los títulos, gráficas y descripciones se toman del JSON: el siguiente corte es volver a correr
agregar.py y este archivo. Uso: python3 piezas.py <AAAA-MM-DD> [SOLO_PNG=1]
Ricardo López Reyero · RLR"""
import os, sys, json, datetime, glob
from PIL import Image
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, '..', 'estadisticas'))
import render
from serie import RAYOS, AUTOR, HASH_BASE

FECHA = sys.argv[1] if len(sys.argv) > 1 else sorted(os.listdir(os.path.join(AQUI, 'cortes')))[-1]
CARPETA = os.path.join(AQUI, 'cortes', FECHA)
A = json.load(open(os.path.join(CARPETA, 'agregados.json'))); C = A['corte']; G = A['grupos']
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
d = datetime.date.fromisoformat(FECHA); MES, ANIO = MESES[d.month - 1], d.year
desde, hasta = datetime.date.fromisoformat(C['desde']), datetime.date.fromisoformat(C['hasta'])
PERIODO = f"{MESES[desde.month - 1]} y {MESES[hasta.month - 1]} de {hasta.year}" if desde.year == hasta.year else f"{MESES[desde.month - 1]} de {desde.year} y {MESES[hasta.month - 1]} de {hasta.year}"
N, CIU = C['instituciones'], C['ciudades']
NIV = [('primaria', 'Colegios con primaria'), ('preparatoria', 'Con preparatoria'), ('universidad', 'Universidades'), ('todos', 'Todas las instituciones')]
MUESTRA_CORTA = f'Muestra: {N} Rayos X de Inscripciones en {CIU} ciudades, entre {PERIODO}. Instituciones que pidieron el diagnóstico, no el país. Mediana, no promedio.'
MUESTRA = (f"Muestra: {N} Rayos X de Inscripciones finalizados entre {PERIODO} con dueños y directores de {N} instituciones privadas en {CIU} ciudades de México. "
           'Son instituciones que pidieron el diagnóstico, no el país. Mediana, no promedio: un colegio de 7,000 alumnos mueve el promedio y miente.')

def med(g, k): r = G[g]['metricas'].get(k); return r['mediana'] if r else None
def n_(g, k): r = G[g]['metricas'].get(k); return r['n'] if r else 0
def parte(g, k): r = G[g]['partes'].get(k); return r['pct'] if r else None
def lista(g, k): return G[g]['listas'].get(k)
def dist(g, k): return G[g]['distribuciones'].get(k)
def f0(x): return f'{x:,.0f}'
def f1(x): return f'{x:,.1f}'.rstrip('0').rstrip('.')
def mxn(x): return f'${x:,.0f}'
def mil(x): return f'${x / 1000:,.0f} mil' if x < 1_000_000 else f'${x / 1_000_000:,.1f} millones'
def de10(p): return round(p / 10)
def por_nivel(k, color_todos='c3'):
    return [(lab, med(g, k), 'c3' if g == 'todos' else 'c1') for g, lab in NIV if med(g, k) is not None]
def ns(k): return 'n = ' + ' / '.join(f"{n_(g, k)}" for g, lab in NIV if n_(g, k)) + ' (' + ', '.join(lab.lower().replace('todas las instituciones', 'todas') for g, lab in NIV if n_(g, k)) + ')'
def tramo(g, k, i): return dist(g, k)['tramos'][i]['pct']

SERIES = {4: dict(nombre=f'Corte Rayos X · {MES} {ANIO}', corto=f'CORTE RAYOS X · {MES[:3].upper()} {ANIO}', doc=f'exportación de {C["archivo"]} ({C["fecha"]} {C["hora"]})')}
P = []
def pieza(**k):
    k['serie'] = 4; k['n'] = len(P) + 1; k['compacto'] = True; k['nota_larga'] = k['nota']; k['nota'] = k['nota'].replace(MUESTRA, MUESTRA_CORTA); P.append(k)

T = 'todos'; m = lambda k: med(T, k)
oc = dist(T, 'ocupacion'); cv = dist(T, 'conversion'); cc = dist(T, 'cierre_cita')

pieza(slug='La radiografia del corte', eyebrow=f'CORTE {MES.upper()} {ANIO} · QUIÉNES SON',
    h1=f'<em>{N} Rayos X</em> en {CIU} ciudades. Esta es la radiografía.',
    grafica=[dict(tipo='stats', items=[(str(N), 'instituciones privadas diagnosticadas'), (str(CIU), 'ciudades de México'), (f"{m('edad'):.0f} años", 'operando, la institución mediana')]),
             dict(tipo='barras', fmt='num', alto=44, items=[('Colegios con primaria', C['grupos']['primaria'], 'c1'), ('Con preparatoria (sin superior)', C['grupos']['preparatoria'], 'c1'), ('Universidades y posgrados', C['grupos']['universidad'], 'c1')], sub='Instituciones por nivel (una puede contar en primaria y preparatoria)')],
    lectura=f'Rayos X finalizados entre {PERIODO}, en vivo con el dueño o director. Lo que sigue es lo que miden, no lo que creen.',
    nota=f'Fuera pruebas, archivados y repetidos (una fila por institución, la más reciente). Montos en pesos. Ningún dato con menos de 5 instituciones se publica. Corte del {C["fecha"]} a las {C["hora"]}.',
    titulo=f'{N} Rayos X de Inscripciones en {CIU} ciudades: la radiografía de la educación privada en México, corte {MES} {ANIO}',
    parrafos=[f'Entre {PERIODO} hicimos {N} Rayos X de Inscripciones con dueños y directores de instituciones privadas en {CIU} ciudades de México: {C["grupos"]["primaria"]} colegios con primaria, {C["grupos"]["preparatoria"]} con preparatoria y {C["grupos"]["universidad"]} universidades y posgrados. La institución mediana lleva {m("edad"):.0f} años operando.',
              'Esta serie es el corte: ocupación, prospectos, conversión, colegiatura, valor de vida, publicidad, becas, equipo y herramientas, separados por nivel, para que cualquier director sepa si está arriba o abajo de sus pares. Sin nombres. Con n. Mediana, no promedio. Lo repetiremos cada seis meses.'],
    pregunta='¿Tú sabes, con número, en qué lugar de esta radiografía está tu colegio?', hashtags='#RayosX #DatosReales')

pieza(slug='Ocupacion mediana', eyebrow='OCUPACIÓN · ALUMNOS ENTRE CAPACIDAD INSTALADA',
    h1=f'La institución mediana opera al <em>{m("ocupacion"):.0f}%</em> de su capacidad.',
    grafica=[dict(tipo='barras', fmt='pct', max=100, alto=40, gap=14, items=[(l, round(v), c) for l, v, c in por_nivel('ocupacion')], sub='Ocupación mediana por nivel'),
             dict(tipo='stats', items=[(f"{tramo(T, 'ocupacion', 0):.0f}%", 'opera abajo del 60% de su capacidad'), (f"{tramo(T, 'ocupacion', 1):.0f}%", 'entre 60 y 80%'), (f"{tramo(T, 'ocupacion', 2):.0f}%", 'arriba del 80%')])],
    lectura=f'{de10(tramo(T, "ocupacion", 0))} de cada 10 instituciones tienen más de la tercera parte de sus lugares vacíos. En un mercado con demanda disponible, eso no es un problema de mercado.',
    nota=f'Ocupación = matrícula actual ÷ capacidad instalada declarada. {MUESTRA} {ns("ocupacion")}.',
    titulo=f'La escuela privada mediana en México opera al {m("ocupacion"):.0f}% de su capacidad ({oc["n"]} Rayos X)',
    parrafos=[f'Ocupación mediana en el corte de {MES} {ANIO}: colegios con primaria {med("primaria", "ocupacion"):.0f}%, con preparatoria {med("preparatoria", "ocupacion"):.0f}%, universidades {med("universidad", "ocupacion"):.0f}%. Todas juntas: {m("ocupacion"):.0f}%. {tramo(T, "ocupacion", 0):.0f}% opera abajo del 60% y solo {tramo(T, "ocupacion", 2):.0f}% arriba del 80%.',
              'Un colegio con lugares disponibles en un mercado con demanda disponible no tiene un problema de mercado. Tiene un problema de proceso. La familia sí llega; lo que decide el ciclo es lo que pasa en las horas siguientes a su primer mensaje.'],
    pregunta='¿Qué porcentaje de tu capacidad está ocupado hoy? Si estás abajo del 60%, estás con la mayoría. La pregunta es si quieres quedarte ahí.', hashtags='#RayosX #Ocupación')

va = G[T]['metricas']['vacios']; co = G[T]['metricas']['capacidad_ociosa']
pieza(slug='Lugares vacios', eyebrow='CAPACIDAD · LUGARES VACÍOS POR INSTITUCIÓN',
    h1=f'<em>{f0(m("vacios"))} lugares vacíos</em> en la institución mediana.',
    grafica=[dict(tipo='barras', fmt='num', alto=40, gap=14, items=[(l, round(v), c) for l, v, c in por_nivel('vacios')], sub='Lugares vacíos (mediana por nivel)'),
             dict(tipo='stats', items=[(f0(va['suma']), f'lugares vacíos sumando las {va["n"]} instituciones con dato'), (mil(m('capacidad_ociosa')), 'al año vale la capacidad sin usar de la institución mediana')])],
    lectura=f'Entre las {co["n"]} instituciones con dato, la capacidad sin usar vale {mil(co["suma"])} de pesos al año. Aulas construidas, maestros contratados, lugares sin alumno.',
    nota=f'Lugares vacíos = capacidad instalada − matrícula. Valor anual = lugares vacíos × colegiatura × meses del ciclo, según el modelo del Rayos X. {MUESTRA}',
    titulo=f'{f0(va["suma"])} lugares vacíos en {va["n"]} escuelas privadas: la capacidad sin usar vale {mil(co["suma"])} al año',
    parrafos=[f'La institución mediana del corte tiene {f0(m("vacios"))} lugares vacíos: {f0(med("primaria", "vacios"))} en colegios con primaria, {f0(med("preparatoria", "vacios"))} en los que tienen preparatoria y {f0(med("universidad", "vacios"))} en universidades. Sumando las {va["n"]} instituciones con dato: {f0(va["suma"])} lugares.',
              f'Puesto en pesos, la capacidad sin usar de la institución mediana vale {mil(m("capacidad_ociosa"))} al año, y entre todas {mil(co["suma"])}. Es infraestructura ya pagada: el aula existe, el maestro existe, el lugar existe. Lo único que falta es el alumno, y el alumno sí preguntó.'],
    pregunta='Multiplica tus lugares vacíos por tu colegiatura por diez meses. Ese es el tamaño de tu oportunidad, y ya está construida.', hashtags='#RayosX #Capacidad')

pieza(slug='Prospectos al dia', eyebrow='PROSPECTOS · FAMILIAS NUEVAS QUE ESCRIBEN CADA DÍA',
    h1=f'<em>{f1(m("leads_dia"))} prospectos al día</em> llegan a la institución mediana.',
    grafica=[dict(tipo='barras', fmt='num', alto=40, gap=14, items=[(l, round(v), c) for l, v, c in por_nivel('leads_dia')], sub='Prospectos nuevos al día (mediana por nivel)'),
             dict(tipo='stats', items=[(f0(med('primaria', 'nuevos')), 'alumnos nuevos al año, colegio con primaria mediano'), (f0(med('universidad', 'nuevos')), 'alumnos nuevos al año, universidad mediana'), (f0(m('nuevos')), 'alumnos nuevos al año, todas')])],
    lectura='La demanda existe y es medible. Lo que casi nadie mide es cuántas de esas familias recibieron respuesta en los primeros cinco minutos.',
    nota=f'Prospectos al día: declarados por el director en el Rayos X (todos los canales). Alumnos nuevos: inscritos del último ciclo. {MUESTRA} {ns("leads_dia")}.',
    titulo=f'Cuántos prospectos recibe al día una escuela privada en México: {f1(m("leads_dia"))} la mediana, {f1(med("universidad", "leads_dia"))} las universidades',
    parrafos=[f'Prospectos nuevos al día en el corte de {MES} {ANIO}: {f1(med("primaria", "leads_dia"))} en colegios con primaria, {f1(med("preparatoria", "leads_dia"))} con preparatoria y {f1(med("universidad", "leads_dia"))} en universidades. La institución mediana recibe {f1(m("leads_dia"))} al día e inscribe {f0(m("nuevos"))} alumnos nuevos al año.',
              'El dato que importa no es cuántos llegan sino cuántos se quedan en el camino. En la mayoría de los Rayos X, nadie en la institución puede decir cuántas familias escribieron el mes pasado y en qué etapa se enfrió cada una. No por negligencia: porque nadie diseñó el proceso para verlo.'],
    pregunta='¿Cuántas familias escribieron a tu colegio esta semana? ¿Y cuántas de ellas recibieron respuesta en minutos?', hashtags='#RayosX #Prospectos')

pieza(slug='Conversion prospecto a inscrito', eyebrow='CONVERSIÓN · DE PROSPECTO A INSCRITO',
    h1=f'De cada 100 familias que escriben, se inscriben <em>{f1(m("conversion"))}</em>.',
    grafica=[dict(tipo='barras', fmt='pct1', max=max(v for _, v, _ in por_nivel('conversion')) * 1.15, alto=40, gap=14, items=[(l, round(v, 1), c) for l, v, c in por_nivel('conversion')], sub='Conversión prospecto → inscrito (mediana por nivel)'),
             dict(tipo='stats', items=[(f"{tramo(T, 'conversion', 0):.0f}%", 'convierte menos del 2%'), (f"{tramo(T, 'conversion', 1):.0f}%", 'entre 2 y 5%'), (f"{tramo(T, 'conversion', 2):.0f}%", 'entre 5 y 10%'), (f"{tramo(T, 'conversion', 3):.0f}%", 'más del 10%')])],
    lectura=f'{tramo(T, "conversion", 0) + tramo(T, "conversion", 1):.0f}% de las instituciones convierte menos del 5% de sus prospectos. El sistema de referencia convierte 14.4%.',
    nota=f'Conversión = alumnos nuevos del último ciclo ÷ prospectos al año; solo valores verosímiles (≤ 100%). Embudo de referencia SuperLeads: 100% → 80% contactados → 60% cita → 60% asistencia → 50% inscrito = 14.4%. {MUESTRA} {ns("conversion")}.',
    titulo=f'Conversión real de las escuelas privadas en México: {f1(m("conversion"))}% de los prospectos se inscribe (mediana de {cv["n"]} Rayos X)',
    parrafos=[f'Conversión mediana de prospecto a inscrito, corte {MES} {ANIO}: colegios con primaria {f1(med("primaria", "conversion"))}%, con preparatoria {f1(med("preparatoria", "conversion"))}%, universidades {f1(med("universidad", "conversion"))}%. Todas: {f1(m("conversion"))}%. {tramo(T, "conversion", 0):.0f}% convierte menos del 2% y solo {tramo(T, "conversion", 3):.0f}% pasa del 10%.',
              'El embudo de referencia de un sistema de inscripciones es 100 prospectos → 80 contactados → 60 con cita → 60% asiste → 50% se inscribe: 14.4 de cada 100. La distancia entre la mediana y ese número no es demanda ni publicidad: es el tramo silencioso entre el primer mensaje y la firma.'],
    pregunta='Divide tus alumnos nuevos entre tus prospectos del año. ¿Qué número te sale? ¿Lo sabías antes de hacer la cuenta?', hashtags='#RayosX #Conversión')

pieza(slug='Cierre en cita', eyebrow='CIERRE · DE LA CITA A LA INSCRIPCIÓN',
    h1=f'Cuando la familia va a la cita, <em>{de10(m("cierre_cita"))} de cada 10</em> se inscriben.',
    grafica=[dict(tipo='barras', fmt='pct', max=100, alto=40, gap=14, items=[(l, round(v), c) for l, v, c in por_nivel('cierre_cita')], sub='Cierre en cita (mediana por nivel)'),
             dict(tipo='stats', items=[(f"{tramo(T, 'cierre_cita', 0):.0f}%", 'cierra menos del 25% de sus citas'), (f"{tramo(T, 'cierre_cita', 2) + tramo(T, 'cierre_cita', 3):.0f}%", 'cierra más de la mitad')])],
    lectura=f'El cierre en cita es {m("cierre_cita"):.0f}%; la conversión total es {f1(m("conversion"))}%. La familia no se pierde en la visita. Se pierde antes de llegar a ella.',
    nota=f'Cierre en cita = inscritos ÷ familias que asistieron a cita, según el director. {MUESTRA} {ns("cierre_cita")}.',
    titulo=f'{m("cierre_cita"):.0f}% de las familias que van a la cita se inscriben; el problema del colegio privado está antes de la cita',
    parrafos=[f'Cierre en cita mediano del corte {MES} {ANIO}: colegios con primaria {med("primaria", "cierre_cita"):.0f}%, con preparatoria {med("preparatoria", "cierre_cita"):.0f}%, universidades {med("universidad", "cierre_cita"):.0f}%. Cuando la familia cruza el portón, {de10(m("cierre_cita"))} de cada 10 firman.',
              f'Compáralo con la conversión total de {f1(m("conversion"))}%. La familia no viene a conocer, viene a confirmar; la visita ya la ganó la institución. Lo que se pierde es el tramo anterior: el WhatsApp sin contestar, la cita que nadie propuso, el seguimiento que no existió. Ahí está el embudo, y ahí no hay nadie viendo.'],
    pregunta='¿Cuántas de tus citas del mes pasado terminaron en inscripción? ¿Y cuántos prospectos nunca llegaron a cita?', hashtags='#RayosX #Admisión')

pieza(slug='Colegiatura mediana', eyebrow='PRECIO · COLEGIATURA MENSUAL',
    h1=f'La colegiatura mediana es <em>{mxn(m("colegiatura"))}</em> al mes.',
    grafica=[dict(tipo='barras', fmt='mxn', alto=40, gap=14, items=[(l, round(v), c) for l, v, c in por_nivel('colegiatura')], sub='Colegiatura mensual (mediana por nivel, MXN)'),
             dict(tipo='stats', items=[(mxn(G[T]['metricas']['colegiatura']['q1']), 'cuartil 1: una de cada cuatro cobra menos'), (mxn(G[T]['metricas']['colegiatura']['q3']), 'cuartil 3: una de cada cuatro cobra más'), (mxn(m('inscripcion')), f'cuota de inscripción mediana (n = {n_(T, "inscripcion")})')])],
    lectura=f'La mitad de las instituciones cobra entre {mxn(G[T]["metricas"]["colegiatura"]["q1"])} y {mxn(G[T]["metricas"]["colegiatura"]["q3"])}. A 10% del ingreso familiar por hijo, ese rango lo sostienen millones de hogares.',
    nota=f'Colegiatura mensual promedio declarada; solo instituciones en pesos. {MUESTRA} {ns("colegiatura")}.',
    titulo=f'Cuánto cobra una escuela privada en México: colegiatura mediana de {mxn(m("colegiatura"))} al mes ({n_(T, "colegiatura")} Rayos X)',
    parrafos=[f'Colegiatura mensual mediana del corte {MES} {ANIO}: colegios con primaria {mxn(med("primaria", "colegiatura"))}, con preparatoria {mxn(med("preparatoria", "colegiatura"))}, universidades {mxn(med("universidad", "colegiatura"))}. Todas: {mxn(m("colegiatura"))}. La mitad cobra entre {mxn(G[T]["metricas"]["colegiatura"]["q1"])} y {mxn(G[T]["metricas"]["colegiatura"]["q3"])}; la cuota de inscripción mediana es {mxn(m("inscripcion"))}.',
              'Con la regla de que una colegiatura sana ronda el 10% del ingreso familiar por hijo, ese rango está al alcance de los 13.4 millones de hogares de los niveles A/B, C+ y C. El precio no es el techo del mercado. Es la excusa más cómoda para no mirar el proceso.'],
    pregunta='¿Tu colegiatura está arriba o abajo de la mediana de tu nivel? ¿Y tu proceso de admisión está a la altura de lo que cobras?', hashtags='#RayosX #Colegiaturas')

pieza(slug='Valor de vida de un alumno', eyebrow='VALOR DE VIDA · LO QUE VALE UNA INSCRIPCIÓN',
    h1=f'Un alumno vale <em>{mil(m("ltv"))}</em> de pesos a lo largo de su permanencia.',
    grafica=[dict(tipo='barras', fmt='mxn', alto=40, gap=14, items=[(l, round(v), c) for l, v, c in por_nivel('ltv')], sub='Valor de vida de un alumno (mediana por nivel, MXN)'),
             dict(tipo='stats', items=[(f"{med('primaria', 'retencion'):.0f} meses", 'permanece un alumno en el colegio con primaria mediano'), (f"{med('universidad', 'retencion'):.0f} meses", 'en la universidad mediana'), (f"{m('retencion'):.0f} meses", 'todas las instituciones')])],
    lectura='Cada «ahorita le contesto» que se volvió nunca tiene este precio. Y capturar a una familia que ya escribió cuesta $0 en publicidad.',
    nota=f'Valor de vida = colegiatura mensual × meses de permanencia promedio, según el modelo del Rayos X; solo instituciones en pesos. {MUESTRA} {ns("ltv")}.',
    titulo=f'Cuánto vale un alumno para una escuela privada: {mxn(m("ltv"))} de valor de vida (mediana de {n_(T, "ltv")} Rayos X)',
    parrafos=[f'Valor de vida mediano de un alumno en el corte {MES} {ANIO}: {mxn(med("primaria", "ltv"))} en colegios con primaria ({med("primaria", "retencion"):.0f} meses de permanencia), {mxn(med("preparatoria", "ltv"))} con preparatoria, {mxn(med("universidad", "ltv"))} en universidades ({med("universidad", "retencion"):.0f} meses). Todas: {mxn(m("ltv"))}.',
              'Ese es el precio de cada familia que se enfrió en el camino. No se pierde por falta de demanda ni de prestigio: se pierde por velocidad y por seguimiento. Y a diferencia de la publicidad, el proceso que la captura se paga una vez y convierte todas las temporadas.'],
    pregunta='¿Cuántas familias se enfriaron en tu colegio el ciclo pasado? Multiplica por el valor de vida de tu nivel.', hashtags='#RayosX #ValorDeVida')

pieza(slug='Inversion en publicidad', eyebrow='PUBLICIDAD · INVERSIÓN MENSUAL Y COSTO POR ALUMNO',
    h1=f'La institución mediana invierte <em>{mxn(m("publicidad"))}</em> al mes en publicidad.',
    grafica=[dict(tipo='barras', fmt='mxn', alto=40, gap=14, items=[(l, round(v), c) for l, v, c in por_nivel('publicidad')], sub='Inversión mensual en publicidad (mediana por nivel, MXN)'),
             dict(tipo='stats', items=[(mxn(m('cpl')), 'cuesta cada prospecto (mediana)'), (mxn(m('caa')), 'cuesta adquirir un alumno (mediana)'), (mxn(med('universidad', 'caa')), 'cuesta un alumno en la universidad mediana')])],
    lectura=f'Un alumno cuesta {mxn(m("caa"))} y vale {mxn(m("ltv"))}. La publicidad no es el problema: lo que se compra con ella se pierde después, sin que nadie lo vea.',
    nota=f'Costo por prospecto = inversión ÷ prospectos; costo de adquisición = inversión ÷ alumnos nuevos, según el Rayos X; solo instituciones en pesos. {MUESTRA} {ns("publicidad")}.',
    titulo=f'Cuánto invierte en publicidad una escuela privada en México: {mxn(m("publicidad"))} al mes y {mxn(m("caa"))} por alumno (mediana)',
    parrafos=[f'Inversión mensual en publicidad mediana, corte {MES} {ANIO}: colegios con primaria {mxn(med("primaria", "publicidad"))}, con preparatoria {mxn(med("preparatoria", "publicidad"))}, universidades {mxn(med("universidad", "publicidad"))}. Cada prospecto cuesta {mxn(m("cpl"))} y cada alumno inscrito {mxn(m("caa"))} (mediana).',
              f'Con un valor de vida mediano de {mxn(m("ltv"))}, la publicidad educativa es de las inversiones más rentables que existen. El problema no es cuánto se invierte sino cuánto de lo comprado se evapora: cada prospecto que no recibe respuesta ya costó {mxn(m("cpl"))} y se fue gratis con el colegio de enfrente.'],
    pregunta='Antes de subir el presupuesto de anuncios: ¿cuántos de tus prospectos del mes pasado recibieron seguimiento?', hashtags='#RayosX #Publicidad')

pieza(slug='Ingreso extra por un punto de conversion', eyebrow='LA CUENTA · +1 PUNTO DE CONVERSIÓN',
    h1=f'Subir <em>un punto</em> la conversión vale {mil(m("extra_1pct"))} al año para la institución mediana.',
    grafica=dict(tipo='barras', fmt='mxn', alto=44, gap=16, items=[(l, round(v), c) for l, v, c in por_nivel('extra_1pct')], sub='Ingreso anual extra por cada +1% de conversión (mediana por nivel, MXN)'),
    lectura=f'De {f1(m("conversion"))}% a {f1(m("conversion") + 1)}%: el mismo número de familias interesadas, más alumnos inscritos. Eso es lo que hace un sistema; la publicidad no puede comprarlo.',
    nota=f'Ingreso extra = prospectos al año × 1% × colegiatura × meses de permanencia, según el modelo del Rayos X; solo instituciones en pesos. {MUESTRA} {ns("extra_1pct")}.',
    titulo=f'Cuánto vale subir un punto la conversión de un colegio privado: {mxn(m("extra_1pct"))} al año (mediana de {n_(T, "extra_1pct")} Rayos X)',
    parrafos=[f'Un punto porcentual más de conversión vale, en ingreso anual, {mxn(med("primaria", "extra_1pct"))} para el colegio con primaria mediano, {mxn(med("preparatoria", "extra_1pct"))} para el que tiene preparatoria y {mxn(med("universidad", "extra_1pct"))} para la universidad mediana. Todas: {mxn(m("extra_1pct"))}.',
              f'La conversión mediana es {f1(m("conversion"))}%. Un sistema de inscripciones no cambia cuántas familias llegan, eso lo hace la publicidad; cambia cuántas se quedan. Y de {f1(m("conversion"))}% a 14.4% hay más de diez puntos de distancia. Haz la multiplicación con tu número.'],
    pregunta='Toma tus prospectos del año, multiplica por 1%, por tu colegiatura y por tus meses de permanencia. ¿Cuánto vale un punto en tu colegio?', hashtags='#RayosX #Conversión')

be = por_nivel('becados')
pieza(slug='Becas', eyebrow='BECAS · CUÁNTOS ALUMNOS Y CUÁNTO DESCUENTO',
    h1=f'<em>{parte(T, "usan_becas"):.0f}%</em> da becas. La mediana tiene {m("becados"):.0f}% de alumnos becados.',
    grafica=[dict(tipo='barras', fmt='pct', max=100, alto=40, gap=14, items=[(l, round(v), c) for l, v, c in be], sub='Alumnos becados (mediana por nivel, entre las que dan becas)'),
             dict(tipo='stats', items=[(f"{m('beca_promedio'):.0f}%", 'beca promedio (mediana)'), (f"{parte('universidad', 'usan_becas'):.0f}%", 'de las universidades da becas'), (f"{parte('primaria', 'usan_becas'):.0f}%", 'de los colegios con primaria')])],
    lectura='La beca es la forma más cara de resolver un problema de proceso: se descuenta la colegiatura de todos para no perder a los que ya querían inscribirse.',
    nota=f'Porcentaje de becados y beca promedio declarados por el director. {MUESTRA} becados {ns("becados")}; usan becas n = {G[T]["partes"]["usan_becas"]["n"]}.',
    titulo=f'Becas en la escuela privada mexicana: {parte(T, "usan_becas"):.0f}% las da y la institución mediana tiene {m("becados"):.0f}% de alumnos becados',
    parrafos=[f'En el corte {MES} {ANIO}, {parte(T, "usan_becas"):.0f}% de las instituciones da becas: {parte("universidad", "usan_becas"):.0f}% de las universidades y {parte("primaria", "usan_becas"):.0f}% de los colegios con primaria. Entre las que dan, la mediana tiene {m("becados"):.0f}% de los alumnos becados con una beca promedio de {m("beca_promedio"):.0f}%.',
              f'Léelo junto a la ocupación mediana de {m("ocupacion"):.0f}%. Una beca no llena un colegio: baja el ingreso por alumno para compensar un proceso que no convierte. Es la forma más cara de resolver un problema que se resuelve con velocidad de respuesta y seguimiento.'],
    pregunta='¿Qué porcentaje de tu matrícula está becado? ¿Y cuántas de esas becas se dieron para «no perder» a una familia que ya quería inscribirse?', hashtags='#RayosX #Becas')

pieza(slug='Recomendacion contra anuncios', eyebrow='ORIGEN · POR DÓNDE LLEGAN LOS ALUMNOS',
    h1=f'<em>{m("pct_recomendados"):.0f}%</em> llega por recomendación. {lista(T, "programa_recomendados")["items"][0]["pct"]:.0f}% no tiene programa.',
    grafica=[dict(tipo='pares', fmt='pct', series=('Por recomendación', 'Por anuncios'), grupos=[(lab, round(med(g, 'pct_recomendados')), round(med(g, 'pct_anuncios'))) for g, lab in NIV if g != 'todos' and med(g, 'pct_recomendados') is not None]),
             dict(tipo='stats', items=[(f"{lista(T, 'programa_recomendados')['items'][0]['pct']:.0f}%", f"no tiene programa de recomendados (n = {lista(T, 'programa_recomendados')['n']})")])],
    lectura='El canal que más alumnos trae es el único que casi nadie opera. Se deja a la suerte lo que debería ser un sistema.',
    nota=f'Porcentaje de alumnos que llegan por recomendación y por anuncios, declarado por el director (mediana por nivel). {MUESTRA} {ns("pct_recomendados")}.',
    titulo=f'{m("pct_recomendados"):.0f}% de los alumnos de una escuela privada llega por recomendación y {lista(T, "programa_recomendados")["items"][0]["pct"]:.0f}% de los colegios no tiene programa de recomendados',
    parrafos=[f'Origen de los alumnos, mediana del corte {MES} {ANIO}: en colegios con primaria {med("primaria", "pct_recomendados"):.0f}% llega por recomendación y {med("primaria", "pct_anuncios"):.0f}% por anuncios; en universidades {med("universidad", "pct_recomendados"):.0f}% y {med("universidad", "pct_anuncios"):.0f}%. Y {lista(T, "programa_recomendados")["items"][0]["pct"]:.0f}% de las instituciones no tiene ningún programa de recomendados.',
              'La recomendación es el canal más barato y el que trae a la familia más parecida a las que ya tienes. Dejarlo a la suerte es regalar la mitad del embudo. Un programa de recomendados no es un descuento: es pedirlo en el momento correcto, a la familia correcta, con un proceso que lo registra.'],
    pregunta='¿Cuántos alumnos te trajo la recomendación el ciclo pasado? ¿Y cuántos te traería si la pidieras a todas las familias contentas?', hashtags='#RayosX #Recomendación')

he = lista(T, 'herramientas')
pieza(slug='Herramientas de admision', eyebrow='HERRAMIENTAS · CON QUÉ SE LLEVA LA ADMISIÓN',
    h1=f'<em>{parte(T, "solo_whatsapp_excel"):.0f}%</em> lleva las admisiones en WhatsApp, Excel o Messenger.',
    grafica=[dict(tipo='barras', fmt='pct', max=100, alto=36, gap=12, items=[(i['etiqueta'], round(i['pct']), 'c2' if i['clave'] in ('whatsapp', 'excel', 'messenger') else 'c1') for i in he['items'][:5]], sub=f'Instituciones que usan cada herramienta (n = {he["n"]}, pueden usar varias)'),
             dict(tipo='stats', items=[(f"{parte('primaria', 'con_crm'):.0f}%", 'de los colegios con primaria tiene CRM o ERP'), (f"{parte('universidad', 'con_crm'):.0f}%", 'de las universidades'), (f"{parte(T, 'con_crm'):.0f}%", 'todas')])],
    lectura='Sin sistema, cada prospecto vive en el teléfono de una persona. Cuando esa persona se va, se va el embudo completo.',
    nota=f'Herramientas con las que la institución lleva su proceso de admisión, declaradas en el Rayos X. CRM = cualquier CRM o ERP. {MUESTRA}',
    titulo=f'{parte(T, "solo_whatsapp_excel"):.0f}% de las escuelas privadas lleva las admisiones en WhatsApp o Excel; solo {parte(T, "con_crm"):.0f}% tiene un CRM',
    parrafos=[f'Con qué se lleva la admisión en el corte {MES} {ANIO}: WhatsApp {he["items"][0]["pct"]:.0f}%, Excel {next(i["pct"] for i in he["items"] if i["clave"] == "excel"):.0f}%. {parte(T, "solo_whatsapp_excel"):.0f}% de las instituciones no usa nada más que WhatsApp, Excel o Messenger. Tiene CRM o ERP {parte("primaria", "con_crm"):.0f}% de los colegios con primaria y {parte("universidad", "con_crm"):.0f}% de las universidades.',
              'No es un problema de tecnología: es que sin sistema nadie puede responder cuántas familias preguntaron, en qué etapa se perdió cada una y por qué. Cada prospecto vive en el celular de una persona, y con ella se va. Un sistema de inscripciones empieza por eso: que cada familia quede trazada desde el primer mensaje hasta la firma, sin depender de la memoria de nadie.'],
    pregunta='Si tu mejor asesor renunciara mañana, ¿cuántas conversaciones de familias se irían con él?', hashtags='#RayosX #CRM')

pieza(slug='Equipo de admisiones', eyebrow='EQUIPO · PERSONAS EN ADMISIONES Y MARKETING',
    h1=f'El colegio con primaria mediano tiene <em>{f1(med("primaria", "staff"))} persona</em> en admisiones y marketing.',
    grafica=[dict(tipo='barras', fmt='num', alto=40, gap=14, items=[(l, round(v, 1), c, f1(v)) for l, v, c in por_nivel('staff')], sub='Personas en admisiones y marketing (mediana por nivel, tiempos completos equivalentes)'),
             dict(tipo='stats', items=[(f"{parte('primaria', 'tiene_director_adm'):.0f}%", 'de los colegios con primaria tiene director de admisiones'), (f"{parte('universidad', 'tiene_director_adm'):.0f}%", 'de las universidades'), (f"{parte(T, 'agencia'):.0f}%", 'de todas tiene agencia externa')])],
    lectura='La persona que da el recorrido es la misma que contesta el teléfono, organiza el festival y apoya en caja. El mensaje más importante del año llega al puesto menos atendido.',
    nota=f'Suma de director de admisiones, marketing, community manager y asesores (fracciones = medio tiempo). {MUESTRA} {ns("staff")}.',
    titulo=f'Cuánta gente tiene una escuela privada en admisiones: {f1(med("primaria", "staff"))} persona en el colegio mediano, {f1(med("universidad", "staff"))} en la universidad mediana',
    parrafos=[f'Personas en admisiones y marketing, mediana del corte {MES} {ANIO}: {f1(med("primaria", "staff"))} en colegios con primaria, {f1(med("preparatoria", "staff"))} con preparatoria y {f1(med("universidad", "staff"))} en universidades. Solo {parte("primaria", "tiene_director_adm"):.0f}% de los colegios con primaria tiene director de admisiones; {parte(T, "agencia"):.0f}% de las instituciones contrata agencia externa.',
              f'Con {f1(med("primaria", "staff"))} persona que además hace otras cosas, es imposible contestar en cinco minutos un domingo a las nueve de la noche. No es falta de esfuerzo: es que los esfuerzos sueltos no se acumulan y los sistemas sí. Un sistema contesta, agenda y da seguimiento aunque la única persona esté en el festival.'],
    pregunta='¿Quién atiende el WhatsApp de informes de tu colegio? ¿Y qué más hace esa persona?', hashtags='#RayosX #Admisiones')

pl = lista(T, 'plan'); pl_no = next(i for i in pl['items'] if i['clave'] == 'no_hay')
pieza(slug='Plan de compensacion', eyebrow='INCENTIVOS · PLAN DE COMPENSACIÓN DE LOS ASESORES',
    h1=f'<em>{pl_no["pct"]:.0f}%</em> de las instituciones no tiene plan de compensación para quien inscribe.',
    grafica=dict(tipo='barras', fmt='pct', max=100, alto=44, gap=16, items=[(i['etiqueta'], round(i['pct']), 'c2' if i['clave'] == 'no_hay' else 'c1') for i in pl['items']] + [(f'Sin plan · colegios con primaria', round(next(i['pct'] for i in lista('primaria', 'plan')['items'] if i['clave'] == 'no_hay')), 'c2'), (f'Sin plan · universidades', round(next(i['pct'] for i in lista('universidad', 'plan')['items'] if i['clave'] == 'no_hay')), 'c2')], sub=f'Plan de compensación del equipo de admisiones (n = {pl["n"]})'),
    lectura='A la persona que inscribe se le paga lo mismo inscriba 5 o 50. Después nos sorprende que conteste el lunes.',
    nota=f'Declarado por el director en el Rayos X: no hay plan / hay plan y están cómodos / hay plan y se puede mejorar. {MUESTRA}',
    titulo=f'{pl_no["pct"]:.0f}% de las escuelas privadas no tiene plan de compensación para su equipo de admisiones',
    parrafos=[f'En el corte {MES} {ANIO}, {pl_no["pct"]:.0f}% de las instituciones no tiene plan de compensación para quien inscribe: {next(i["pct"] for i in lista("primaria", "plan")["items"] if i["clave"] == "no_hay"):.0f}% de los colegios con primaria y {next(i["pct"] for i in lista("universidad", "plan")["items"] if i["clave"] == "no_hay"):.0f}% de las universidades. {next(i["pct"] for i in pl["items"] if i["clave"] == "comodos"):.0f}% tiene plan y está cómodo; {next(i["pct"] for i in pl["items"] if i["clave"] == "se_puede_mejorar"):.0f}% cree que se puede mejorar.',
              'Los sistemas producen el resultado para el que fueron diseñados. Si a quien inscribe se le paga igual inscriba cinco o cincuenta, el sistema está diseñado para que conteste el lunes. Alinear intereses no es un gasto: es la diferencia entre un asesor que persigue familias y uno que las espera.'],
    pregunta='¿Qué gana tu asesor de admisiones cuando inscribe una familia más? Si la respuesta es «nada», ya sabes por qué contesta tarde.', hashtags='#RayosX #Equipo')

ms = lista(T, 'meses'); mes_max = max(i['pct'] for i in ms['items']); top = [i['clave'] for i in ms['items'] if i['pct'] >= mes_max - 1]
pieza(slug='Meses de mayor inscripcion', eyebrow='TEMPORADAS · MESES DE MAYOR INSCRIPCIÓN',
    h1=f'<em>{" y ".join(top)}</em>: los meses en que se llena el colegio.',
    grafica=dict(tipo='columnas', fmt='pct', alto=400, resaltar=mes_max - 1, items=[(i['clave'][:3], round(i['pct'])) for i in ms['items']]),
    lectura='La temporada dura semanas; la decisión de la familia empezó seis meses antes. Quien arranca campaña en julio llega a cobrar lo que otros sembraron en febrero.',
    nota=f'Porcentaje de instituciones que señalan cada mes entre sus meses de mayor inscripción (pueden señalar varios). n = {ms["n"]}. {MUESTRA}',
    titulo=f'En qué meses se inscriben más alumnos en las escuelas privadas de México: {", ".join(top)} ({ms["n"]} Rayos X)',
    parrafos=[f'Meses de mayor inscripción señalados por las instituciones del corte {MES} {ANIO}: ' + ', '.join(f"{i['clave']} {i['pct']:.0f}%" for i in sorted(ms['items'], key=lambda i: -i['pct'])[:5]) + '. Hay dos temporadas claras: la de verano y la de inicio de año.',
              'La familia investiga seis meses antes de inscribir. Para cuando llega la temporada, ya evaluó, descartó y armó su terna. La campaña que arranca cuando empieza la temporada compite por las familias que quedaron; la que trabaja todo el año cosecha las que se decidieron antes.'],
    pregunta='Si tu temporada fuerte es julio, ¿qué hizo tu colegio por esas familias en febrero?', hashtags='#RayosX #Temporadas')

ca = lista(T, 'causas'); ca_precio = next(i['pct'] for i in ca['items'] if i['clave'] == 'precio'); ca_seg = next(i['pct'] for i in ca['items'] if i['clave'] == 'sin_seguimiento')
pieza(slug='Por que no se inscribieron', eyebrow='LO QUE CREE EL DIRECTOR · POR QUÉ NO SE INSCRIBIERON',
    h1=f'<em>{de10(ca_precio)} de cada 10</em> directores culpan al precio. {de10(ca_seg)} de cada 10 admiten que no hubo seguimiento.',
    grafica=dict(tipo='barras', fmt='pct', max=100, alto=40, gap=14, items=[(i['etiqueta'], round(i['pct']), 'c2' if i['clave'] == 'sin_seguimiento' else 'c1') for i in ca['items'][:6]], sub=f'Causas de no inscripción según el director (n = {ca["n"]}, varias por institución)'),
    lectura='El precio es la explicación cómoda: exime a todos. El seguimiento es la incómoda: está bajo el control del colegio.',
    nota=f'Lo que el director cree que pasó con las familias que fueron a cita y no se inscribieron; es creencia, no medición. {MUESTRA}',
    titulo=f'Por qué no se inscriben las familias según los directores: {ca_precio:.0f}% dice que el precio, {ca_seg:.0f}% admite falta de seguimiento',
    parrafos=[f'Cuando preguntamos a los directores por qué no se inscribieron las familias que sí fueron a cita, {ca_precio:.0f}% responde que el precio y {ca_seg:.0f}% admite que no les dieron seguimiento. Le siguen cupo u horario, la competencia y la distancia.',
              f'Es lo que el director cree, no lo que se midió. Y la creencia tiene un patrón: la causa más mencionada es la que no depende de nadie. La segunda es la única que está completamente bajo el control del colegio. Con una colegiatura mediana de {mxn(m("colegiatura"))} y 13.4 millones de hogares que pueden pagarla, el precio rara vez es el motivo. El silencio, casi siempre.'],
    pregunta='De las últimas 10 familias que no se inscribieron, ¿a cuántas les llamaste para preguntar por qué?', hashtags='#RayosX #Seguimiento')

nm = lista(T, 'nivel_marketing'); nm_bien = sum(i['pct'] for i in nm['items'] if i['clave'] in ('muy_bien', 'excelente'))
pieza(slug='Percepcion contra realidad', eyebrow='PERCEPCIÓN · CÓMO CALIFICA EL DIRECTOR SU MARKETING',
    h1=f'<em>{nm_bien:.0f}%</em> califica su marketing como muy bueno o excelente. <em>{tramo(T, "ocupacion", 0):.0f}%</em> opera abajo del 60%.',
    grafica=dict(tipo='donas', items=[(round(nm_bien), f'{nm_bien:.0f}%', f'califica su marketing como «muy bien» o «excelente» (n = {nm["n"]})', 'c1'), (round(tramo(T, 'ocupacion', 0)), f'{tramo(T, "ocupacion", 0):.0f}%', f'opera abajo del 60% de su capacidad (n = {oc["n"]})', 'c2')]),
    lectura=f'La conversión mediana es {f1(m("conversion"))}%. El marketing trae a la familia; lo que la pierde ocurre después, y eso nadie lo está calificando.',
    nota=f'Autoevaluación del director (mal / más o menos / bien / muy bien / excelente) contra la ocupación medida. {MUESTRA}',
    titulo=f'{nm_bien:.0f}% de los directores califica su marketing de muy bueno o excelente; {tramo(T, "ocupacion", 0):.0f}% de sus escuelas opera abajo del 60%',
    parrafos=[f'En el corte {MES} {ANIO}, {nm_bien:.0f}% de los directores califica el marketing de su institución como muy bueno o excelente. Al mismo tiempo, {tramo(T, "ocupacion", 0):.0f}% opera abajo del 60% de su capacidad y la conversión mediana de prospecto a inscrito es {f1(m("conversion"))}%.',
              'Las dos cosas pueden ser ciertas: el marketing puede estar bien y el colegio vacío. Porque el marketing llena el ciclo de prospectos y el sistema llena el colegio. Lo que casi nadie califica es el tramo entre el primer mensaje y la firma, y ahí es donde se pierde la familia que el marketing ya trajo.'],
    pregunta='Si tu marketing está bien y tu colegio no está lleno, ¿qué parte del proceso no estás mirando?', hashtags='#RayosX #Marketing')

ru = lista(T, 'rubros')
pieza(slug='Monetizacion ademas de la colegiatura', eyebrow='MONETIZACIÓN · QUÉ COBRAN ADEMÁS DE LA COLEGIATURA',
    h1=f'<em>{ru["items"][0]["pct"]:.0f}%</em> cobra {ru["items"][0]["etiqueta"].lower()}. Solo {next(i["pct"] for i in ru["items"] if i["clave"] == "transporte"):.0f}%, transporte.',
    grafica=dict(tipo='barras', fmt='pct', max=100, alto=34, gap=10, items=[(i['etiqueta'], round(i['pct']), 'c1') for i in ru['items'][:8]], sub=f'Instituciones que cobran cada rubro (n = {ru["n"]}, los 8 más frecuentes)'),
    lectura='Cada rubro que no se cobra es ingreso que la familia ya está gastando en otro lado. La colegiatura es el piso del ingreso por alumno, no el techo.',
    nota=f'Diez rubros medidos en el Rayos X: uniformes, asesorías, transporte, cafetería, libros, útiles, eventos, graduaciones y viajes. {MUESTRA}',
    titulo=f'Qué cobran las escuelas privadas además de la colegiatura: {ru["items"][0]["etiqueta"].lower()} {ru["items"][0]["pct"]:.0f}%, {ru["items"][1]["etiqueta"].lower()} {ru["items"][1]["pct"]:.0f}%, transporte {next(i["pct"] for i in ru["items"] if i["clave"] == "transporte"):.0f}%',
    parrafos=['Rubros que cobran las instituciones del corte además de la colegiatura: ' + ', '.join(f"{i['etiqueta'].lower()} {i['pct']:.0f}%" for i in ru['items']) + '.',
              'La familia ya gasta en uniformes, libros, transporte y comida; la pregunta es si se lo compra al colegio o a alguien más. Cada rubro bien operado sube el ingreso por alumno sin tocar la colegiatura, y financia el proceso de admisión que llena los lugares vacíos.'],
    pregunta='De estos diez rubros, ¿cuántos cobra tu colegio? ¿Y cuántos podría cobrar el próximo ciclo?', hashtags='#RayosX #Ingresos')

def armar_descripcion(p):
    return '\n'.join([p['titulo'] + '.', '', '\n\n'.join(p['parrafos']), '', p['pregunta'], '', 'Fuente y método: ' + p['nota_larga'], '',
                      f"Pieza {p['n']:02d} de la serie «{SERIES[4]['nombre']}», el corte semestral de los Rayos X de Inscripciones de SuperLeads. Datos agregados y anonimizados; metodología a solicitud: hola@superleads.mx", '',
                      RAYOS, '', AUTOR, '', f"{HASH_BASE} {p['hashtags']}"])

if __name__ == '__main__':
    solo_png = os.environ.get('SOLO_PNG') == '1'
    for p in P: assert len(p['titulo']) <= 140, (p['n'], len(p['titulo'])); assert len(p['eyebrow']) <= 58, (p['n'], p['eyebrow'])
    render.P, render.SERIES = P, SERIES; render.SALIDA = os.path.join(CARPETA, 'salida'); render.HTMLD = os.path.join(CARPETA, 'html')
    render.PIE = ('', f'Corte Rayos X · {MES} {ANIO}'); render.LOGO = 'file://' + os.path.abspath(os.path.join(AQUI, '..', 'estadisticas', 'logo_blanco.svg'))
    for f in glob.glob(os.path.join(render.SALIDA, '*')): os.remove(f)
    ch = render.Chrome(); idx = []
    try:
        for p in P:
            base, fondo = render.render(p, ch, solo_png); print(f'{p["n"]:02d} fondo={fondo:.0f}{"  ⚠ se pasa de 1600" if fondo > 1600 else ""} · {base}')
            idx.append(dict(n=p['n'], slug=p['slug'], titulo=p['titulo'], descripcion=armar_descripcion(p), hashtags=f"{HASH_BASE} {p['hashtags']}", png=base + '.png', mp4=None if solo_png else base + '.mp4', fuente=p['nota'], estado='hecho, sin publicar'))
    finally: ch.cerrar()
    json.dump(idx, open(os.path.join(CARPETA, 'indice.json'), 'w'), ensure_ascii=False, indent=1)
    md = [f"# {SERIES[4]['nombre']} · textos para YouTube Shorts · {datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')}", '', MUESTRA, '', '| # | Título | Archivo |', '|---|---|---|'] + [f"| {r['n']:02d} | {r['titulo']} | `{r['png']}` |" for r in idx] + ['', '---', '']
    for r in idx: md += [f"## {r['n']:02d} · {r['titulo']}", '', f"Archivo: `{r['png']}`" + (f" · video: `{r['mp4']}`" if r['mp4'] else ''), '', '**Título:**', '', r['titulo'], '', '**Descripción:**', '', '```', r['descripcion'], '```', '']
    open(os.path.join(CARPETA, 'SHORTS_corte_textos.md'), 'w').write('\n'.join(md))
    tw, th, cols = 270, 480, 7; filas = (len(idx) + cols - 1) // cols
    H = Image.new('RGB', (cols * (tw + 10) + 10, filas * (th + 10) + 10), (0, 18, 64))
    for i, r in enumerate(idx): H.paste(Image.open(os.path.join(render.SALIDA, r['png'])).convert('RGB').resize((tw, th)), (10 + (i % cols) * (tw + 10), 10 + (i // cols) * (th + 10)))
    H.save(os.path.join(CARPETA, 'hoja.jpg'), quality=86); print(len(idx), 'piezas')
# Ricardo López Reyero · EYE · 181218
