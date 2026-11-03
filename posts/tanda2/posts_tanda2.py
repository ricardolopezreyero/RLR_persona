"""Tanda 2 de X · 21 posts (semana 9–15 nov 2026) con la guía VOZ-X v3.

Formato: 8:00 tarjeta (el formato del IMSS: lo que creen, tachado; lo que es, en amarillo),
13:30 solo texto (una idea, su filosofía aplicada al colegio), 20:30 post largo que se guarda.
17:30 sigue la serie de datos ya programada. Cada cifra sale de posts/estadisticas (serie
«La realidad de la educación», con fuente) o del corte Rayos X de oct-2026 (posts/rayosx_corte).
Escribe posts_tanda2.json."""
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))

POSTS = [
    # ── Lunes 9 ────────────────────────────────────────────────────────────
    dict(fecha='2026-11-09', hora='08:00', tipo='tarjeta', embudo='alcance',
         tarjeta=dict(etiqueta='102 RAYOS X · OCTUBRE 2026', arriba='Tu colegio no está', tachado='vacío.',
                      respuesta='Está mal atendido.', pie='Mediana: 46 % de ocupación. 44 de cada 100 consultas nunca reciben respuesta.'),
         texto="""Tu colegio no está vacío.

La escuela privada mediana opera al 46 % de su capacidad. Lo medí en 98 Rayos X con dueños y directores.

Y en el estudio más grande de comprador secreto al sector, 44 de cada 100 consultas jamás recibieron respuesta. Ni tarde: nunca.

No faltan familias. Falta quien les conteste.

¿Cuántos mensajes de este fin de semana siguen sin respuesta en el WhatsApp de tu colegio?""",
         fuente='Corte Rayos X oct-2026 (n=98); serie Realidad #12 (1,000 consultas)'),
    dict(fecha='2026-11-09', hora='13:30', tipo='texto', embudo='alcance',
         texto="""Si tu colegio está al 46 %, es tu culpa.

Y es la mejor noticia que te pueden dar.

Si fuera culpa del gobierno, de la economía o de que nacen menos niños, no podrías hacer nada.

Si es tuya, lo arreglas el lunes.

La culpa total es la libertad total. También para un director.""",
         fuente='Frase bandera «Todo es mi culpa»; corte Rayos X (46 %)'),
    dict(fecha='2026-11-09', hora='20:30', tipo='largo', embudo='confianza',
         texto="""Hicimos 102 Rayos X de Inscripciones con dueños y directores de escuelas privadas en 69 ciudades de México.

5 cosas que nadie me había dicho:

1. La escuela mediana opera al 46 %. Más de la mitad de sus sillas están vacías.
2. 40 % de las familias que van a la cita se inscribe. El problema no está en la cita: está antes.
3. Un alumno vale $144,000 MXN en toda su estancia. Casi todos lo tratan como un mensaje más de WhatsApp.
4. 40 % de los alumnos llega por recomendación y 70 % de los colegios no tiene programa de recomendados.
5. 62 % de los directores culpa al precio. Solo 38 % admite que no dio seguimiento.

El colegio no tiene un problema de mercado. Tiene un problema de sistema.

Guárdalo para tu próxima junta de consejo.""",
         fuente='Corte Rayos X oct-2026 (series 1, 2, 6, 8, 12, 17)'),

    # ── Martes 10 ──────────────────────────────────────────────────────────
    dict(fecha='2026-11-10', hora='08:00', tipo='tarjeta', embudo='alcance',
         tarjeta=dict(etiqueta='ADMISIONES · LO QUE NADIE MIDE', arriba='Tu colegio no necesita más', tachado='publicidad.',
                      respuesta='Necesita contestar.', pie='$1,381 MXN por alumno inscrito. Y solo 2.4 % de los prospectos se inscribe.'),
         texto="""Tu colegio no necesita más publicidad.

El colegio mediano invierte $8,000 MXN al mes en anuncios y paga $1,381 MXN por cada alumno que inscribe. Es el gasto más rentable que tiene.

El problema no es lo que entra. Es lo que se enfría en el camino: solo 2.4 % de los prospectos termina inscrito.

Antes de subirle al anuncio, ¿quién le contesta a los que ya llegaron?""",
         fuente='Corte Rayos X oct-2026 (series 5 y 9)'),
    dict(fecha='2026-11-10', hora='13:30', tipo='texto', embudo='alcance',
         texto="""Opinión impopular entre directores:

Con menos de 900 alumnos no hay pretexto para no tener lista de espera.

13.4 millones de hogares en México pueden pagar un colegio privado. Tu ciudad tiene las familias.

La lista de espera no se anuncia. Se construye, mensaje por mensaje.""",
         fuente='Short 14 (tanda 2); serie Realidad #23 (13.4 millones)'),
    dict(fecha='2026-11-10', hora='20:30', tipo='largo', embudo='confianza',
         texto="""El colegio cierra a las 3 de la tarde.

Las familias deciden a las 11 de la noche.

93 % de las familias mexicanas está conectada entre las 9 y la medianoche. Una mamá acuesta a los niños, busca «colegios cerca de mí», lee reseñas y le escribe a dos.

Esa noche tu colegio fue evaluado. Y nadie en la institución se enteró.

78 % le compra al primero que responde. Solo 7 % de las organizaciones contesta en 5 minutos.

No es un problema de horario. Es un problema de sistema.

¿Quién contesta en tu colegio a las 11 de la noche?""",
         fuente='Serie Realidad #13 y #14'),

    # ── Miércoles 11 ───────────────────────────────────────────────────────
    dict(fecha='2026-11-11', hora='08:00', tipo='tarjeta', embudo='alcance',
         tarjeta=dict(etiqueta='LA REALIDAD DE LA EDUCACIÓN', arriba='El problema no es el', tachado='maestro.',
                      respuesta='Es el sistema que le paga.', pie='Docente promedio: $7,890 MXN al mes. México: último lugar OCDE en gasto por alumno.'),
         texto="""El problema de la educación en México no es el maestro.

El docente promedio gana $7,890 MXN al mes, según la ENOE. México invierte $2,933 USD al año por alumno de primaria: último lugar de la OCDE.

El mensaje del sistema a su maestro es coherente: te pago poco, no te formo, no te evalúo.

No le pidas resultados de primer mundo a un sistema que paga como último lugar.

No es la persona. Es el sistema que la puso ahí.""",
         fuente='Serie Realidad #5 (ENOE) y #8 (OCDE)'),
    dict(fecha='2026-11-11', hora='13:30', tipo='texto', embudo='alcance',
         texto="""Pregunta para dueños de colegio:

¿Cuánto vale un alumno?

Si contestaste «una colegiatura», contestaste mal.

El alumno mediano vale $144,000 MXN en toda su estancia.

Ese es el tamaño de cada WhatsApp que se queda en visto.""",
         fuente='Corte Rayos X oct-2026 (serie 8, n=97)'),
    dict(fecha='2026-11-11', hora='20:30', tipo='largo', embudo='confianza',
         texto="""Perú: 10 % de los hogares puede pagar un colegio privado. 26 % de los alumnos está en uno.

México: 35 % puede pagarlo. Solo 10 % está en uno.

Familias peruanas con mucho menos ingreso pagan colegio porque decidieron que la pública no era opción para sus hijos, y ajustaron todo lo demás.

En México no falta dinero. Falta que alguien le explique a la familia por qué vale la pena.

Eso no lo hace el gobierno. Lo hace cada colegio, una familia a la vez.

¿Tu colegio vende colegiaturas o vende futuro?""",
         fuente='Serie Realidad #24'),

    # ── Jueves 12 ──────────────────────────────────────────────────────────
    dict(fecha='2026-11-12', hora='08:00', tipo='tarjeta', embudo='alcance',
         tarjeta=dict(etiqueta='EL PRECIO DEL SILENCIO', arriba='Un WhatsApp sin contestar', tachado='no cuesta nada.',
                      respuesta='Cuesta $450,000 MXN.', pie='Colegiatura de $4,500 × 12 meses × 6 años × 1.4 por hermanos.'),
         texto="""Un WhatsApp sin contestar no cuesta nada.

Eso creen casi todos.

Hagamos la cuenta con un colegio típico: colegiatura de $4,500 MXN, 6 años de permanencia y la probabilidad de un hermano. Son unos $450,000 MXN por familia.

Ese es el precio de cada «ahorita le contesto» que se volvió nunca.

Recuperar a una familia que ya escribió cuesta $0 en anuncios. Solo cuesta proceso.""",
         fuente='Serie Realidad #16'),
    dict(fecha='2026-11-12', hora='13:30', tipo='texto', embudo='confianza',
         texto="""El 22 de febrero de 2022 me senté 50 minutos con una sola pregunta:

¿A qué nicho me enfoco que tenga la máxima rentabilidad y la máxima longevidad?

Salió educación.

1,724 días después sigo aquí. Un colegio lleno no es solo un negocio lleno: es una ciudad con más gente preparada.

Por eso escribo de esto todos los días. Si tienes un colegio, sígueme.""",
         fuente='ESENCIA (22-feb-2022, 50 minutos); días calculados al 12-nov-2026'),
    dict(fecha='2026-11-12', hora='20:30', tipo='largo', embudo='confianza',
         texto="""Becas: 68 % de las escuelas privadas las da, y la institución mediana tiene 40 % de alumnos becados.

Una beca con estrategia atrae al alumno que quieres.

Una beca sin estrategia es un descuento que nadie te pidió, a una familia que ya te había elegido.

Antes de dar la siguiente, tres preguntas:
1. ¿Qué alumno quiero atraer con ella?
2. ¿Qué tiene que pasar para mantenerla?
3. ¿Cuánto vale ese alumno en toda su estancia?

Si no tienes las tres respuestas, no es beca. Es miedo a perder la inscripción.""",
         fuente='Corte Rayos X oct-2026 (serie 11)'),

    # ── Viernes 13 ─────────────────────────────────────────────────────────
    dict(fecha='2026-11-13', hora='08:00', tipo='tarjeta', embudo='alcance',
         tarjeta=dict(etiqueta='POR QUÉ NO SE INSCRIBEN', arriba='No se fueron por el', tachado='precio.',
                      respuesta='Se fueron por el silencio.', pie='62 % de los directores culpa al precio. 38 % admite que no dio seguimiento.'),
         texto="""No se fueron por el precio.

En los Rayos X, 62 % de los directores culpa al precio de las familias que no se inscribieron. Solo 38 % admite que nadie les dio seguimiento.

Pero de las familias que sí llegan a la cita, 40 % se inscribe. Al mismo precio.

El precio es la explicación cómoda. El seguimiento es la incómoda.

¿Cuál de las dos está más cerca de tu colegio?""",
         fuente='Corte Rayos X oct-2026 (series 6 y 17)'),
    dict(fecha='2026-11-13', hora='13:30', tipo='texto', embudo='alcance',
         texto="""Tu colegio no compite contra el colegio de enfrente.

Compite contra la escuela pública gratuita, donde están 9 de cada 10 niños del país.

Y contra el WhatsApp que nadie contestó.

Ese es tu mercado. No el vecino.""",
         fuente='Serie Realidad #22 (10 % en privada)'),
    dict(fecha='2026-11-13', hora='20:30', tipo='largo', embudo='confianza',
         texto="""El canal más barato para llenar un colegio no cuesta un peso.

40 % de los alumnos de la escuela privada mediana llega por recomendación de otra familia.

Y 70 % de los colegios no tiene ningún programa de recomendados. Ni una invitación, ni un agradecimiento, ni una pregunta.

Tus familias quieren recomendarte. Nadie les dice cómo.

Un programa de recomendados no es un descuento: es pedir, agradecer y medir. Tres cosas.

¿Cuándo fue la última vez que tu colegio le pidió a una familia feliz que invitara a otra?""",
         fuente='Corte Rayos X oct-2026 (serie 12); Short 28'),

    # ── Sábado 14 ──────────────────────────────────────────────────────────
    dict(fecha='2026-11-14', hora='08:00', tipo='tarjeta', embudo='alcance',
         tarjeta=dict(etiqueta='PISA 2022 · MATEMÁTICAS', arriba='No es un problema de los', tachado='niños.',
                      respuesta='Es del sistema que los forma.', pie='México: lugar 35 de 37. 66 % no alcanza el nivel básico.'),
         texto="""No es un problema de los niños.

En PISA, México quedó en el lugar 35 de 37. Dos de cada tres alumnos de 15 años no alcanzan el nivel básico de Matemáticas. Nivel básico es poder usar una regla de tres en la vida diaria.

Veinte puntos PISA equivalen a un año escolar. El alumno mexicano promedio va de tres a cuatro años atrás.

No son los niños. Es el sistema que los selecciona, los forma y los mide.

Si cambias el proceso, cambias los resultados.""",
         fuente='Serie Realidad #1 y #2 (OCDE PISA 2022; IMCO)'),
    dict(fecha='2026-11-14', hora='13:30', tipo='texto', embudo='alcance',
         texto="""Si estuvieras viendo tu colegio en la pantalla de un cine, ¿qué te estaría gritando la audiencia que hicieras?

Yo creo que algo así:

«¡Contesta ese mensaje!»""",
         fuente='Frase bandera (la película de tu vida)'),
    dict(fecha='2026-11-14', hora='20:30', tipo='largo', embudo='confianza',
         texto="""Las 3 preguntas que le hago a todo dueño de colegio en un Rayos X:

1. ¿Cuántos lugares vacíos tienes hoy?
2. ¿Cuántas familias te preguntan al día?
3. ¿Cuántas de esas terminan inscritas?

Con esos tres números sé dónde está el problema en 10 minutos.

Si no los sabes sin abrir un Excel, ese es el primer problema.

Lo que no se mide no se mejora. Y lo que no se mejora, se vacía.""",
         fuente='Proceso del Rayos X de Inscripciones'),

    # ── Domingo 15 ─────────────────────────────────────────────────────────
    dict(fecha='2026-11-15', hora='08:00', tipo='tarjeta', embudo='alcance',
         tarjeta=dict(etiqueta='92 RAYOS X · CONVERSIÓN', arriba='De cada 100 familias que preguntan,', tachado='',
                      respuesta='2 se inscriben.', pie='Pasar de 2.4 % a 3.4 % vale $109,500 MXN al año en el colegio mediano.'),
         texto="""De cada 100 familias que preguntan por un colegio privado, 2 se inscriben.

Y casi todos los directores creen que necesitan más familias.

Con las mismas 100, subir un solo punto, de 2.4 % a 3.4 %, vale $109,500 MXN al año para el colegio mediano.

Más publicidad es lo último. Primero, el proceso.""",
         fuente='Corte Rayos X oct-2026 (series 5 y 10)'),
    dict(fecha='2026-11-15', hora='13:30', tipo='texto', embudo='alcance',
         texto="""Hay 3 tipos de colegios:

1. Los que esperan inscripciones.
2. Los que las compran.
3. Los que las construyen.

Los primeros culpan al año. Los segundos, al anuncio.

Los terceros tienen lista de espera.""",
         fuente='Estructura de «3 tipos de socios» aplicada a colegios'),
    dict(fecha='2026-11-15', hora='20:30', tipo='largo', embudo='conversion',
         texto="""Llevamos 102 Rayos X de Inscripciones con dueños y directores en 69 ciudades.

En una sesión acomodamos los números de admisiones de tu colegio como tienen que estar: ocupación, prospectos, conversión, valor de un alumno. Te llevas un PDF con los más importantes.

Tiene costo. Por ahora lo damos sin costo.

Si tienes un colegio y quieres ver tu radiografía: https://superleads.mx/rayos_x""",
         fuente='Rayos X de Inscripciones (único post de venta de la semana)'),
]


def main():
    for k, p in enumerate(POSTS, 1):
        p['n'] = k
        p['caracteres'] = len(p['texto'])
        p['estado'] = 'propuesto · falta visto bueno de Ricardo'
    json.dump(POSTS, open(os.path.join(AQUI, 'posts_tanda2.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(POSTS), 'posts ·', max(p['caracteres'] for p in POSTS), 'caracteres máx')


if __name__ == '__main__':
    main()
