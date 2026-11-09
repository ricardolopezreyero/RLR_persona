"""Artículo «Hay más familias queriendo inscribirse en tu colegio de las que tu proceso alcanza a inscribir» (9-nov-2026).

Fuente de verdad del texto. Se arma con las láminas de la presentación de Ricardo (PDF v1 del 9-nov) y el video de la charla.
Escribe: articulo.md (para leer), publicar.json (segmentos html/img para X y LinkedIn) y datos.html (window.__A para BrowserOS).
Regla del editor de X: nunca dos imágenes seguidas; siempre hay texto entre una y otra."""
import html, json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(AQUI, 'imagenes')
TITULO = 'Hay más familias queriendo inscribirse en tu colegio de las que tu proceso alcanza a inscribir'
RAYOS = 'https://rayosx.superleads.mx/rayos_x'
VIDEO = 'https://youtu.be/op95KKuYzms'
CIERRE = 'Lunes 9 de noviembre de 2026, 3:55 pm · Torreón, Coahuila, México · 22°.'
FIRMA = 'Ing. Ricardo López Reyero · Founder Comercial · SuperLeads · ricardo@superleads.mx'

# ('p', texto) párrafo · ('h', texto) subtítulo · ('img', archivo) lámina · ('ul', [..]) lista
B = [
    ('p', 'Hay una frase que escucho en casi todas mis juntas con dueños y directores de colegios: «ya no hay niños». A veces cambia: «la demanda se acabó», «las familias ya no pueden pagar».'),
    ('p', 'Los datos dicen otra cosa. En América Latina, y sobre todo en México, hay más familias que pueden pagar un colegio privado, y que escriben para pedir informes, de las que la educación privada está logrando inscribir.'),
    ('p', 'El problema no es la demanda. Es el proceso.'),
    ('p', 'Te lo explico con las láminas de la charla que di hace unos días frente a dueños y directores de colegios. Al final te dejo el video completo.'),

    ('h', 'México está al final de la lista'),
    ('img', '03-alumnos-en-escuela-privada-por-pais.jpg'),
    ('p', 'De cada 100 alumnos de primaria en Chile, 63 están en una escuela privada. En Perú, 26. El promedio mundial es 19. En México, 10.'),
    ('p', 'México tiene una de las proporciones de educación privada más bajas de la región.'),
    ('img', '04-mexico-35-pueden-pagar-10-inscritos.jpg'),
    ('p', 'Y no es porque las familias no puedan pagar. El 35 % de los hogares mexicanos tiene el nivel socioeconómico para pagar un colegio privado: son 13.4 millones de hogares. Solo el 10 % de los alumnos está en uno.'),
    ('img', '05-peru-es-al-reves.jpg'),
    ('p', 'Perú es el espejo. Allá solo el 10 % de los hogares podría pagar, y aun así el 26 % de los alumnos está en escuela privada. Las familias peruanas hacen un esfuerzo enorme por la educación privada. Aquí, con mucha más capacidad de pago, se inscriben menos.'),
    ('img', '07-el-problema-no-es-la-demanda.jpg'),
    ('p', 'Hay muchos más alumnos de los que la educación privada está captando. El problema no es la demanda. Está en otro lado.'),

    ('h', 'Los colegios tienen lugares vacíos'),
    ('img', '09-46-por-ciento-de-capacidad.jpg'),
    ('p', 'Lo vemos en los Rayos X de Inscripciones que hacemos con cada institución. En el corte de octubre de 2026, con 102 instituciones en 69 ciudades, la institución mediana opera al 46 % de su capacidad.'),
    ('p', 'Más de la mitad de los lugares está vacía. Y en la educación privada no existe algo más costoso que una silla vacía.'),

    ('h', 'Las familias sí escriben'),
    ('img', '10-conversion-mediana-2-4.jpg'),
    ('p', 'La conversión mediana es de 2.4 %: de cada 100 familias que escriben para pedir informes, se inscriben 2.4.'),
    ('p', 'Las familias sí están llegando. Escriben por WhatsApp, por Messenger, por Instagram; llaman, mandan correos, llenan formularios. Lo que no está llegando es la respuesta.'),
    ('img', '18-44-por-ciento-sin-respuesta.jpg'),
    ('p', 'Un estudio de UPCEA con 1,000 consultas a instituciones educativas encontró que el 44 % nunca recibió respuesta. Y cuando sí contestan, la respuesta promedio tarda 14 horas con 23 minutos.'),
    ('p', 'Catorce horas es una eternidad para una mamá que está decidiendo dónde va a estudiar su hijo. En ese tiempo ya le contestó otro colegio.'),
    ('img', '17-71-por-ciento-whatsapp-excel.jpg'),
    ('p', '¿Por qué pasa? Porque el 71 % de las instituciones lleva sus admisiones en WhatsApp, Excel, Messenger o a mano. El otro 29 % usa un CRM genérico, administrativo o académico. Ninguno fue hecho para admisiones.'),
    ('p', 'Por eso lo digo así: hay más familias queriendo inscribirse en tu colegio que las que tus procesos de inscripción alcanzan a captar.'),

    ('h', 'No es falta de esfuerzo'),
    ('img', '20-no-es-falta-de-esfuerzo.jpg'),
    ('p', 'Conozco a muchos equipos de admisiones. Trabajan muchísimo. Contestan desde su celular en la noche, en fin de semana, en vacaciones.'),
    ('p', 'No es falta de esfuerzo. Es falta de sistema. Y si es falta de sistema, se corrige con la herramienta correcta.'),
    ('p', 'La matemática de las inscripciones es simple: prospectos por tasa de conversión es igual a alumnos. Solo hay dos palancas. Subir cualquiera de las dos sube los alumnos, y mejorar la conversión es la más barata, porque esas familias ya te escribieron.'),

    ('h', 'Por eso creamos a Constanza'),
    ('img', '22-constanza.jpg'),
    ('p', 'Constanza es una inteligencia artificial hecha solo para admisiones. Contesta a cada familia en segundos, a cualquier hora, los 365 días del año. También a las 11 de la noche, que es cuando muchos papás por fin se sientan a buscar colegio.'),
    ('p', 'Y nunca pregunta «¿cuándo puede?». Propone tres horarios concretos, porque así es como una familia sí agenda.'),
    ('img', '23-constanza-todos-los-dias.jpg'),
    ('p', 'Todos los días filtra el spam, recaba la información de cada familia, resuelve sus dudas, da seguimiento por su cuenta y agenda citas con alta probabilidad de inscripción.'),
    ('img', '25-asi-fluye-cada-prospecto.jpg'),
    ('p', 'Así fluye cada prospecto: la familia escribe por el medio que quiera, todo entra por el colegio, Constanza lo atiende uno a uno con la inteligencia artificial de SuperLeads especializada en admisiones, y la respuesta regresa a la familia. Cien familias preguntando a la vez, y ninguna esperando.'),
    ('p', 'La estamos iterando todo el tiempo. Vemos en directo lo que pasa en más de 100 instituciones, aprendemos qué funciona y qué no, y la ajustamos cada día para que genere más citas y de mejor calidad.'),
    ('p', 'Constanza no sustituye a tu equipo. Le quita lo que no le toca para que haga lo que mejor sabe hacer: recibir a la familia y cerrar la inscripción.'),

    ('h', 'Un sistema se instala'),
    ('img', '28-implementacion.jpg'),
    ('p', 'Un software se entrega. Un sistema se instala, se opera y se audita. Por eso implementamos cuatro cosas juntas: tecnología, metodología, ejecución y soporte. Si quitas una, se cae todo.'),
    ('img', '30-admisiones-es-comercial.jpg'),
    ('p', 'Admisiones no es administrativo. Admisiones no es académico. Admisiones es comercial, y tiene un ritmo distinto al de todas las demás áreas del colegio. Por eso necesita su propio sistema.'),

    ('h', 'La oportunidad'),
    ('p', 'México tiene millones de familias que pueden pagar un colegio privado y colegios con la mitad de sus lugares vacíos. Entre unas y otros hay un puente roto: el proceso de inscripción.'),
    ('p', 'Arreglarlo no le quita alumnos a nadie. Hace que lleguen al final las familias que ya querían llegar.'),
    ('p', f'Si quieres ver los números de tu colegio con esta perspectiva, agenda un Rayos X de Inscripciones: {RAYOS}'),
    ('p', f'Aquí está el video completo de la charla, seis minutos: {VIDEO}'),

    ('h', 'Fuentes'),
    ('ul', [
        'Banco Mundial e Instituto de Estadística de la UNESCO: matrícula de primaria en escuela privada, 2022–2024.',
        'AMAI, Regla NSE 2024; Banco Mundial; UNESCO: hogares que pueden pagar un colegio privado en México.',
        'APEIM, Niveles Socioeconómicos 2025: Perú.',
        'Corte Rayos X de Inscripciones de SuperLeads, octubre de 2026: 102 instituciones en 69 ciudades, valores medianos.',
        'UPCEA, Enrollment Process Review: Secret Shopper Analysis, 2025: 1,000 consultas a instituciones educativas.',
    ]),
    ('p', CIERRE),
    ('p', FIRMA),
]


def a_html(texto):
    t = html.escape(texto)
    for url in (RAYOS, VIDEO, 'ricardo@superleads.mx'):
        e = html.escape(url)
        href = 'mailto:' + url if '@' in url else url
        t = t.replace(e, f'<a href="{href}">{e}</a>')
    return t


def segmentos():
    segs, buf = [], []
    for k, v in B:
        if k == 'img':
            if buf:
                segs.append({'html': ''.join(buf)}); buf = []
            assert segs and 'html' in segs[-1], 'dos imágenes seguidas'
            segs.append({'img': os.path.join(IMG, v)})
        elif k == 'h':
            buf.append(f'<h2>{html.escape(v)}</h2>')
        elif k == 'ul':
            buf.append('<ul>' + ''.join(f'<li>{html.escape(x)}</li>' for x in v) + '</ul>')
        else:
            buf.append(f'<p>{a_html(v)}</p>')
    if buf:
        segs.append({'html': ''.join(buf)})
    return segs


def main():
    segs = segmentos()
    md = [f'# {TITULO}', '', '![portada](portada-linkedin-16x9.jpg)', '']
    for k, v in B:
        md += ([f'## {v}'] if k == 'h' else [f'![](imagenes/{v})'] if k == 'img' else [f'- {x}' for x in v] if k == 'ul' else [v]) + ['']
    open(os.path.join(AQUI, 'articulo.md'), 'w').write('\n'.join(md))
    A = {'titulo': TITULO, 'portada_x': os.path.join(AQUI, 'portada-x-5x2.jpg'),
         'portada_li': os.path.join(AQUI, 'portada-linkedin-16x9.jpg'), 'segs': segs}
    json.dump(A, open(os.path.join(AQUI, 'publicar.json'), 'w'), ensure_ascii=False, indent=1)
    open(os.path.join(AQUI, 'datos.html'), 'w').write('<!doctype html><meta charset="utf-8"><title>datos</title><script>window.__A={0:' + json.dumps(A, ensure_ascii=False) + '};</script>ok')
    palabras = sum(len((v if isinstance(v, str) else ' '.join(v)).split()) for k, v in B if k != 'img')
    print(len(segs), 'segmentos ·', sum(1 for s in segs if 'img' in s), 'imágenes ·', palabras, 'palabras')


if __name__ == '__main__':
    main()
