"""Serie «Datos» para YouTube Shorts: un gráfico y un texto por pieza.
Fuente de verdad de la serie: cada cifra sale de los tres documentos de mercado de SuperLeads (julio 2026)
y conserva la fuente original. Nada se inventa; si el documento trae un rango, la pieza trae el rango.
Autor: Ricardo López Reyero (RLR). Render: render.py."""

# RLR
SERIES = {
    1: dict(nombre='La realidad de la educación pública en México', corto='EDUCACIÓN PÚBLICA EN MÉXICO',
            doc='P1-01 · La realidad de la educación pública en México (julio 2026)'),
    2: dict(nombre='La boleta invisible: cómo eligen colegio las familias mexicanas', corto='LA BOLETA INVISIBLE',
            doc='P1-02 · La boleta invisible: cómo deciden las familias (julio 2026)'),
    3: dict(nombre='Análisis de la educación privada en Latinoamérica', corto='EDUCACIÓN PRIVADA EN LATAM',
            doc='P1-03 · Análisis de la educación privada en LATAM (julio 2026)'),
}

RAYOS = ('Rayos X de Inscripciones: en una sesión acomodamos los números de admisiones de tu colegio como tienen que estar '
         'y te llevas un PDF con los más importantes. Tiene costo; por ahora lo damos sin costo. Agenda aquí: https://superleads.mx/rayos_x')
AUTOR = ('Soy el Ing. Ricardo López Reyero, Founder Comercial de SuperLeads. Solo hacemos admisiones: por nuestro sistema pasan '
         'más de 300,000 prospectos educativos al año. Más en https://superleads.mx')
DOCS = 'El documento completo, con sus fuentes y metodología, se entrega a solicitud: hola@superleads.mx'
HASH_BASE = '#Admisiones #ColegiosPrivados'

# Cada pieza: n, serie, slug, eyebrow, h1 (con <em>), grafica (una o lista), lectura, nota, titulo, parrafos, pregunta, hashtags.
# Colores de gráfica (guía SuperLeads §16): c1 azul serie base, c2 naranja «el antes / el problema», c3 verde «la meta», neu sin dato.
P = []

# ───────────────────────── Serie 1 · Educación pública en México ─────────────────────────
P.append(dict(n=1, serie=1, slug='Lugar 35 de 37 en PISA',
    eyebrow='PISA 2022 · MATEMÁTICAS, LECTURA Y CIENCIAS',
    h1='México: lugar <em>35 de 37</em> países de la OCDE.',
    grafica=dict(tipo='pares', fmt='num', series=('Promedio OCDE', 'México'),
                 grupos=[('Matemáticas', 472, 395), ('Lectura', 476, 415), ('Ciencias', 485, 410)]),
    lectura='Tercer peor resultado en Matemáticas y Lectura. El peor de toda la OCDE en Ciencias.',
    nota='Puntaje promedio de estudiantes de 15 años. 20 puntos PISA equivalen aproximadamente a un año escolar. Fuente: OCDE, PISA 2022 Results, Country Note México.',
    titulo='México es el lugar 35 de 37 en PISA: 77 puntos abajo del promedio en Matemáticas',
    parrafos=['Puntaje PISA 2022: México 395 en Matemáticas contra 472 del promedio OCDE. En Lectura 415 contra 476. En Ciencias 410 contra 485, el peor de toda la organización. Veinte puntos PISA equivalen a un año escolar: el alumno mexicano promedio de 15 años va entre tres y cuatro años atrás de sus pares.',
              'Es la última fotografía internacional que existe del aprendizaje en México, porque después el país dejó de medirse. No es un problema de maestros ni de niños: es el resultado que produce el sistema que los seleccionó, los formó y dejó de evaluarlos.'],
    pregunta='¿A qué escuela va la mayoría de los niños de tu ciudad: a la que mide, o a la que dejó de medir?',
    hashtags='#PISA2022 #EducaciónMéxico'))

P.append(dict(n=2, serie=1, slug='2 de cada 3 reprobados en lo basico',
    eyebrow='PISA 2022 · NIVEL BÁSICO DE MATEMÁTICAS',
    h1='<em>2 de cada 3</em> reprobados en lo básico.',
    grafica=dict(tipo='waffle', total=100, lleno=66, cols=10, numero='66%',
                 etiqueta='de los estudiantes mexicanos de 15 años no alcanza el nivel básico de competencia en Matemáticas'),
    lectura='En Lectura, 47% no comprende lo que lee. En excelencia matemática: prácticamente 0%.',
    nota='Fuente: OCDE, PISA 2022; IMCO, «PISA 2022: dos de cada tres estudiantes en México no alcanzan el nivel básico en Matemáticas» (dic 2023).',
    titulo='66% de los alumnos mexicanos de 15 años no alcanza el nivel básico de Matemáticas',
    parrafos=['Dos de cada tres estudiantes mexicanos de 15 años no alcanzan el nivel básico de competencia en Matemáticas. Casi la mitad, 47%, no comprende lo que lee. Y el porcentaje que alcanza la excelencia en Matemáticas es prácticamente cero.',
              'Nivel básico no es sacar diez: es poder usar una regla de tres en la vida diaria. Eso es lo que el sistema le entrega hoy a nueve de cada diez niños del país. Y es la alternativa real contra la que compite todo colegio privado.'],
    pregunta='Si tu colegio tuviera estos números, ¿cuántas familias se quedarían?',
    hashtags='#PISA2022 #EducaciónMéxico'))

P.append(dict(n=3, serie=1, slug='4 de cada 10 escuelas sin agua luz o sanitarios',
    eyebrow='INSTALACIONES · AGUA, LUZ Y SANITARIOS',
    h1='<em>4 de cada 10</em> escuelas públicas operan sin agua, luz o sanitarios dignos.',
    grafica=dict(tipo='barras', fmt='pct', max=50, alto=56,
                 items=[('Escuelas públicas', 40, 'c2'), ('Escuelas privadas', 8, 'c1')]),
    lectura='La desigualdad educativa no empieza en el aula. Empieza en el inmueble.',
    nota='Porcentaje de planteles que operan con al menos una carencia de servicios esenciales. Fuente: Aprender Parejo, México Evalúa / Tec de Monterrey (2024).',
    titulo='40% de las escuelas públicas de México opera sin agua, luz o sanitarios dignos',
    parrafos=['Cuatro de cada diez escuelas públicas en México operan con al menos una carencia de servicios esenciales: agua, luz o sanitarios. En las privadas, 8%. La misma ciudad, los mismos niños, cinco veces la probabilidad de aprender sin baño digno.',
              'La consecuencia la vive el padre de familia el primer día de clases, y la recuerda cada vez que compara instalaciones. No es un argumento de ventas: es la razón por la que una familia que puede pagar, paga.'],
    pregunta='¿Cuándo fue la última vez que entraste a un baño de escuela pública?',
    hashtags='#EducaciónMéxico #EscuelasPúblicas'))

P.append(dict(n=4, serie=1, slug='65 de cada 100 escuelas sin computadora ni internet',
    eyebrow='INSTALACIONES · TECNOLOGÍA',
    h1='<em>65 de cada 100</em> escuelas públicas no tienen computadoras ni internet.',
    grafica=[dict(tipo='waffle', total=100, lleno=65, cols=10, numero='65', etiqueta='de cada 100 escuelas públicas operan sin computadoras o sin internet', tam=40, gap=9),
             dict(tipo='stats', items=[('9,034', 'planteles públicos sin agua potable (SEP, 2023–24)'), ('5,112', 'planteles sin servicio eléctrico'), ('89 mil', 'escuelas de básica sin drenaje (Coneval)')])],
    lectura='Entre 2013 y 2024 se gastaron $451,230 millones de pesos en infraestructura educativa. Desde 2019 nadie actualiza el censo que diría en qué se convirtieron.',
    nota='Fuentes: SEP, estadísticas de servicios básicos por plantel (ciclo 2023–2024); Coneval (2021); ASF / INIFED; SNIIFE congelado desde 2019.',
    titulo='65 de cada 100 escuelas públicas no tienen computadoras ni internet',
    parrafos=['En México, 65 de cada 100 escuelas públicas operan sin computadoras o sin internet. 9,034 planteles de educación básica no tienen agua potable. 5,112 no tienen luz. 89 mil no tienen drenaje.',
              'Entre 2013 y 2024 el país gastó $451,230 millones de pesos en infraestructura educativa. Y desde 2019 dejó de actualizarse el censo nacional de infraestructura escolar, así que nadie puede decir oficialmente en qué se convirtió ese dinero. Se gastó el presupuesto y se apagó el medidor.'],
    pregunta='¿Cómo se aprende a programar, a investigar o a escribir un correo en una escuela sin internet?',
    hashtags='#EducaciónMéxico #EscuelasPúblicas'))

P.append(dict(n=5, serie=1, slug='El maestro gana menos que el salario minimo',
    eyebrow='DOCENTES · INGRESO MENSUAL PROMEDIO (ENOE 1T-2025)',
    h1='El maestro promedio gana <em>menos que el salario mínimo</em>.',
    grafica=dict(tipo='barras', fmt='mxn', alto=48,
                 items=[('Salario mínimo 2025', 8400, 'c1'), ('Docente promedio', 7890, 'c2'), ('Docente de preescolar', 6430, 'c2'), ('Docente de preparatoria', 6260, 'c2')]),
    lectura='Te pago poco, no te formo, no te evalúo. La desmotivación no es un defecto del magisterio: es la respuesta racional a esos incentivos.',
    nota='Promedios nacionales ENOE 1T-2025 / Data México; incluyen jornadas parciales (27–28 h/semana) e informalidad. Los docentes formales de tiempo completo (IMCO) promedian ~$18,000, aún por debajo del promedio OCDE para la profesión.',
    titulo='El maestro mexicano promedio gana $7,890 al mes: menos que el salario mínimo',
    parrafos=['Ingreso mensual promedio de un docente en México: $7,890 pesos. El salario mínimo 2025: $8,400. Un maestro de preescolar promedia $6,430; uno de preparatoria, $6,260. Son promedios nacionales de la ENOE que incluyen jornadas parciales; los docentes formales de tiempo completo rondan los $18,000, todavía abajo del promedio OCDE para la profesión.',
              'Desde 2019 nadie verifica la idoneidad de quien está frente a grupo, y la capacitación es esporádica y sin seguimiento. El mensaje del sistema a su maestro es coherente: te pago poco, no te formo, no te evalúo. El docente no es el villano de esta historia. Es su segunda víctima.'],
    pregunta='¿Qué resultado esperarías de cualquier profesión con ese paquete?',
    hashtags='#Docentes #EducaciónMéxico'))

P.append(dict(n=6, serie=1, slug='1.4 millones de ninos sin clases',
    eyebrow='JUNIO 2026 · PARO NACIONAL DE LA CNTE',
    h1='<em>1.4 millones</em> de niños sin clases.',
    grafica=[dict(tipo='stats', items=[('17,471', 'escuelas cerradas en la recta final del ciclo'), ('1,410,459', 'alumnos sin clases (corte al 5 de junio)'), ('88,546', 'docentes en paro en 10 estados')]),
             dict(tipo='barras', fmt='pct1', max=100, alto=56, items=[('Oaxaca: matrícula estatal sin un solo día de clases', 92.13, 'c2')])],
    lectura='Nueve de cada diez niños oaxaqueños sin maestro. No por una guerra. No por una pandemia. Por la negociación anual entre el sindicato y el gobierno.',
    nota='Fuente: SEP, reportes oficiales del paro de la CNTE, corte al 5 de junio de 2026; cobertura de Excélsior, El Universal y El Informador.',
    titulo='1,410,459 niños sin clases: el paro de la CNTE de junio 2026 en cifras de la SEP',
    parrafos=['Corte de la SEP al 5 de junio de 2026: 17,471 escuelas cerradas, 1,410,459 alumnos sin clases y 88,546 docentes en paro en diez estados. En Oaxaca, 92.13% de la matrícula estatal sin un solo día de clases.',
              'No es un evento extraordinario: es un patrón que se repite cada ciclo desde hace décadas. Cada semana perdida en los primeros años es un agujero que rara vez se recupera. Y para la familia la consecuencia es la incertidumbre: no sabe, al inscribir el ciclo, cuántos días de clase recibirá realmente su hijo. La certeza del calendario, algo que ningún colegio privado presume, es uno de los diferenciales más valorados por las familias que cruzan de la pública a la privada.'],
    pregunta='¿Cuántos días de clase recibió tu hijo el ciclo pasado? ¿Lo sabes con número?',
    hashtags='#CNTE #EducaciónMéxico'))

P.append(dict(n=7, serie=1, slug='Faltan 4 de cada 5 maestros de ingles',
    eyebrow='INGLÉS · MAESTROS NECESARIOS VS. EXISTENTES',
    h1='Faltan <em>4 de cada 5</em> maestros de inglés.',
    grafica=[dict(tipo='barras', fmt='num', alto=52, items=[('Maestros de inglés necesarios', 400000, 'c1'), ('Maestros de inglés existentes', 80000, 'c2')]),
             dict(tipo='stats', items=[('97%', 'de los egresados de secundaria pública no alcanza el nivel de inglés del plan SEP'), ('86%', 'de las escuelas públicas de básica no tiene ni un maestro de inglés'), ('52%', 'de los maestros que sí lo imparten no alcanza el B1 que se espera de sus alumnos')])],
    lectura='El niño de colegio privado toma inglés desde preescolar. El de escuela pública, con 86% de probabilidad, jamás tendrá un maestro del idioma.',
    nota='Fuente: Mexicanos Primero, «Sorry: el aprendizaje del inglés en México» (CIDE / CEES); SEP / SHCP, presupuestos del PRONI 2018–2024. Cobertura nacional estimada: 20%.',
    titulo='México necesita 400,000 maestros de inglés y tiene 80,000',
    parrafos=['México necesita 400,000 maestros de inglés para cubrir la escuela pública y tiene 80,000. 86% de las escuelas de básica no tiene ni uno. 97% de los egresados de secundaria pública no alcanza el nivel que el propio plan de la SEP promete. Y 52% de los maestros que sí dan inglés no llegan al B1 que se le exige a sus alumnos.',
              'El país comparte 3,142 kilómetros de frontera con la economía más grande del mundo, y su motor de crecimiento opera en inglés. Esa sola variable define trayectorias salariales de por vida. Pocas brechas son tan fáciles de explicar a una familia, y tan difíciles de cerrar después.'],
    pregunta='¿Tu colegio dice «bilingüe» en la barda o lo puede demostrar con un examen?',
    hashtags='#Inglés #EducaciónMéxico'))

P.append(dict(n=8, serie=1, slug='Ultimo lugar de la OCDE en gasto por alumno',
    eyebrow='INVERSIÓN · GASTO POR ALUMNO DE PRIMARIA (USD, 2021)',
    h1='<em>Último lugar</em> de la OCDE en gasto por alumno.',
    grafica=dict(tipo='barras', fmt='usd', alto=40, gap=18,
                 items=[('Luxemburgo', 25584, 'c1'), ('Estados Unidos', 15270, 'c1'), ('Promedio OCDE', 11902, 'c1'), ('Lituania', 8716, 'c1'), ('Croacia', 8199, 'c1'), ('México', 2933, 'c2')]),
    lectura='Colombia, Bulgaria, Turquía, Hungría y Rumania, con menor PIB per cápita que México, invierten más por alumno. Y el gasto cayó 10.5% entre 2015 y 2022.',
    nota='Gasto anual por alumno de primaria, USD PPA, 2021. Fuente: OCDE, Education at a Glance 2023–2025; Mexicanos Primero, análisis de Education at a Glance (2025).',
    titulo='México invierte $2,933 USD por alumno de primaria: último lugar de la OCDE',
    parrafos=['Gasto anual por alumno de primaria: Luxemburgo $25,584 USD, Estados Unidos $15,270, promedio OCDE $11,902, Lituania $8,716, Croacia $8,199. México: $2,933. Último lugar. Países con menor PIB per cápita, como Colombia, Bulgaria, Turquía, Hungría y Rumania, invierten más por niño.',
              'Y la tendencia es descendente: el gasto por alumno cayó 10.5% entre 2015 y 2022 mientras el promedio OCDE subía. Detrás de cada sección anterior de esta serie hay una causa común, y es esta. Se recorta lo que construye capacidad: escuelas, maestros, materiales, evaluación.'],
    pregunta='¿Con $2,933 dólares al año, qué esperarías que le entregaran a tu hijo?',
    hashtags='#GastoEducativo #EducaciónMéxico'))

P.append(dict(n=9, serie=1, slug='La escuela gratuita no lo es',
    eyebrow='INVERSIÓN · QUIÉN PAGA LA ESCUELA «GRATUITA»',
    h1='La escuela gratuita <em>no lo es</em>.',
    grafica=[dict(tipo='barras', fmt='pct1', max=20, alto=56, items=[('Familias mexicanas', 16.2, 'c2'), ('Promedio OCDE', 9.9, 'c1')],
                  sub='Parte del gasto educativo en básica y media superior que cubren las familias'),
             dict(tipo='stats', items=[('3.19%', 'del PIB será el gasto educativo en 2026, el nivel más bajo desde 2018'), ('−10.5%', 'cayó el gasto por alumno entre 2015 y 2022')])],
    lectura='Cooperaciones, útiles, mantenimiento de los planteles. La familia mexicana ya paga por la educación pública. Lo que no recibe a cambio es el servicio.',
    nota='Fuente: OCDE, Education at a Glance 2025 (participación del gasto privado de los hogares); CIEP, análisis del Paquete Económico 2026.',
    titulo='Las familias mexicanas pagan 16.2% del gasto educativo público; el promedio OCDE es 9.9%',
    parrafos=['Las familias mexicanas cubren 16.2% del gasto educativo en básica y media superior, vía cooperaciones, útiles y mantenimiento de los planteles. El promedio de la OCDE es 9.9%. Al mismo tiempo, el gasto educativo de 2026 equivale a 3.19% del PIB, el nivel más bajo desde 2018.',
              'La escuela «gratuita» no lo es. La familia mexicana ya paga por la educación pública; lo que no recibe a cambio es el servicio. Cuando esa misma familia compara lo que paga con lo que recibe, la colegiatura de un colegio privado deja de ser un lujo y se vuelve una cuenta.'],
    pregunta='Si ya estás pagando, ¿a quién le quieres pagar?',
    hashtags='#GastoEducativo #EducaciónMéxico'))

P.append(dict(n=10, serie=1, slug='El pais que rompio sus termometros',
    eyebrow='MEDICIÓN · LO QUE EL PAÍS DEJÓ DE MEDIR',
    h1='El país que rompió <em>sus propios termómetros</em>.',
    grafica=dict(tipo='tiempo', items=[
        ('2019', 'Desaparece el INEE, el instituto autónomo de evaluación. Se cancelan PLANEA y la evaluación docente obligatoria. Se congela el censo de infraestructura escolar.'),
        ('2019–25', 'México sale del ERCE, la prueba regional de la UNESCO, y pone en riesgo PISA 2025, al grado de que la OCDE exige públicamente no abandonar la última medición que queda.'),
        ('2025', 'Desaparece Mejoredu, el organismo que sustituyó al INEE, sin publicar los resultados de su última evaluación. El acervo histórico del INEE deja de estar en línea.'),
        ('2026', 'La UNESCO advierte: México implementa un nuevo modelo educativo sin ningún mecanismo nacional para saber si funciona.')]),
    lectura='Ningún sistema serio destruye sus instrumentos de medición cuando los resultados van bien. Se destruyen cuando los resultados son indefendibles.',
    nota='Fuente: UNESCO, Estrategia de País México 2026–2031; OCDE / IMCO / Ibero sobre el riesgo de salida de PISA 2025; desaparición del INEE (2019) y de Mejoredu (2025).',
    titulo='2019, 2025, 2026: la cronología de cómo México dejó de medir su educación',
    parrafos=['2019: desaparece el INEE, se cancelan PLANEA y la evaluación docente obligatoria, se congela el censo de infraestructura escolar. 2019 a 2025: México sale del ERCE de la UNESCO y la OCDE tiene que exigir públicamente que no abandone PISA. 2025: desaparece Mejoredu sin publicar su última evaluación. 2026: la UNESCO advierte que el nuevo modelo educativo opera sin ningún mecanismo nacional para saber si funciona.',
              'Ningún sistema serio destruye sus instrumentos de medición cuando los resultados van bien. La opacidad no es un descuido administrativo: es una política. Y la consecuencia es que hoy el debate educativo del país se da con datos de 2022 hacia atrás.'],
    pregunta='Si en tu colegio dejaran de entregar boletas, ¿pensarías que los niños van mejor?',
    hashtags='#INEE #EducaciónMéxico'))

P.append(dict(n=11, serie=1, slug='8 de cada 10 sin los aprendizajes esperados',
    eyebrow='APRENDIZAJES · 3° DE SECUNDARIA, 2024–2025',
    h1='<em>8 de cada 10</em> no desarrollaron los aprendizajes esperados.',
    grafica=dict(tipo='waffle', total=10, lleno=8, cols=5, tam=150, gap=24, numero=None, etiqueta=None),
    lectura='La pandemia añadió un rezago de dos años de escolaridad: el egresado de secundaria sabe hoy lo que antes sabía un alumno de primero.',
    nota='Fuente: Mejoredu, evaluación diagnóstica 2024–2025 (no publicada oficialmente; filtrada a la prensa, oct 2025); Banco Mundial, estimación de pérdida de aprendizajes post-COVID.',
    titulo='8 de cada 10 alumnos de 3° de secundaria no desarrollaron los aprendizajes esperados',
    parrafos=['La última evaluación nacional conocida, Mejoredu ciclo 2024–2025, encontró que 8 de cada 10 estudiantes de tercero de secundaria no desarrollaron los aprendizajes esperados. Nunca se publicó oficialmente: se filtró a la prensa en octubre de 2025, poco antes de que el organismo desapareciera.',
              'El Banco Mundial estima que la pandemia añadió un rezago equivalente a dos años de escolaridad: el egresado promedio de secundaria sabe hoy lo que antes sabía un alumno de primero. Ese es el punto de partida real de la mayoría de los niños del país, y la medida contra la que una familia compara cualquier colegio.'],
    pregunta='¿Qué harías si supieras que tu hijo va dos años atrás y nadie te lo dijo?',
    hashtags='#Mejoredu #EducaciónMéxico'))

# ───────────────────────── Serie 2 · La boleta invisible ─────────────────────────
P.append(dict(n=12, serie=2, slug='44 por ciento de consultas sin respuesta',
    eyebrow='COMPRADOR SECRETO · 1,000 CONSULTAS A COLEGIOS',
    h1='<em>44%</em> de las consultas jamás recibió respuesta.',
    grafica=dict(tipo='dona', pct=44, numero='44%', etiqueta='de las consultas de prospectos a instituciones educativas no recibió respuesta. Ni rápida ni lenta: ninguna.', color='c2'),
    lectura='Promedio de respuesta del sector: 14 horas con 23 minutos. Para entonces, otro colegio ya saludó a la familia por su nombre.',
    nota='Fuente: UPCEA, Enrollment Process Review: Secret Shopper Analysis 2025 (1,000 consultas a instituciones educativas).',
    titulo='44% de las consultas a colegios jamás recibe respuesta (estudio con 1,000 consultas)',
    parrafos=['El estudio de comprador secreto más grande hecho al sector educativo, 1,000 consultas de prospectos, encontró que 44% jamás recibió respuesta. Ni rápida ni lenta: ninguna. Y el promedio de respuesta de las que sí contestaron fue de 14 horas con 23 minutos.',
              'En los diagnósticos a colegios mexicanos vemos el mismo patrón, agravado por el horario: el mensaje del domingo en la noche se contesta, si se contesta, el lunes después de la junta. Para entonces otro colegio ya saludó a la familia por su nombre, le preguntó por su hijo y le ofreció dos horarios de recorrido. La familia no dijo que no. Se quedó en el camino por el silencio.'],
    pregunta='De las últimas 40 familias que escribieron a tu colegio, ¿cuántas recibieron respuesta? Si no conoces el dato, ya conoces el problema.',
    hashtags='#Prospectos #TiempoDeRespuesta'))

P.append(dict(n=13, serie=2, slug='La familia investiga de noche',
    eyebrow='HÁBITOS DIGITALES · ¿CUÁNDO INVESTIGA LA FAMILIA?',
    h1='La familia investiga <em>de noche</em>. El colegio atiende de 7 a 3.',
    grafica=dict(tipo='franjas'),
    lectura='Ese desfase es la primera fuga del embudo, y la más invisible, porque ocurre cuando no hay nadie viendo.',
    nota='Usuarios conectados por franja horaria en México. Fuente: Asociación de Internet MX, Estudios de Hábitos de Usuarios de Internet en México (eds. 14–15). El horario de atención escolar es el típico, ilustrativo.',
    titulo='93% de las familias está conectada entre 9 de la noche y medianoche; el colegio cierra a las 3',
    parrafos=['Los estudios de hábitos digitales en México ubican los picos de conexión fuera del horario laboral: 90% al mediodía, 85% en la tarde y hasta 93% entre las 21:00 y las 24:00. El colegio típico atiende de 7 de la mañana a 3 de la tarde, entre semana.',
              'Domingo, 9:47 de la noche: una mamá acostó a los niños y por fin tiene veinte minutos para lo importante. Busca «colegios privados cerca de mí», lee reseñas, entra a tres sitios y le escribe por WhatsApp a los dos que sobrevivieron. Su colegio fue evaluado esa noche, y nadie en la institución se enteró. Ese desfase de horarios es la primera fuga del embudo.'],
    pregunta='¿Quién le contesta a esa mamá en tu colegio a las 9:47 de la noche de un domingo?',
    hashtags='#Prospectos #WhatsApp'))

P.append(dict(n=14, serie=2, slug='78 compra al primero que responde solo 7 responde en 5 minutos',
    eyebrow='PRIMER CONTACTO · VELOCIDAD DE RESPUESTA',
    h1='<em>78%</em> le compra al primero que responde. Solo <em>7%</em> responde en 5 minutos.',
    grafica=dict(tipo='donas', items=[(78, '78%', 'de los clientes le compra al primero que responde', 'c1'), (7, '7%', 'de las organizaciones responde dentro de los primeros 5 minutos', 'c2')]),
    lectura='El primer mensaje es la primera clase muestra.',
    nota='Fuente: MIT / InsideSales.com, Lead Response Management Study (Oldroyd); Lead Response Management / Drift: solo 7% responde en menos de 5 minutos y 55% tarda más de 5 días.',
    titulo='78% le compra al primero que responde; solo 7% de las organizaciones contesta en 5 minutos',
    parrafos=['78% de los clientes le compra al primero que responde. Solo 7% de las organizaciones responde dentro de los primeros cinco minutos, y 55% tarda más de cinco días. Son dos décadas de investigación comercial (MIT, Harvard Business Review, Velocify) diciendo lo mismo.',
              'La familia no interpreta la respuesta lenta como «están ocupados». La interpreta como «así van a atender a mi hijo cuando ya esté adentro». El primer mensaje es la primera clase muestra. Y en un mercado donde 93% de los que responden lo hacen tarde, contestar en cinco minutos no es una mejora: es la ventaja completa.'],
    pregunta='¿Cuánto tardó tu colegio en contestar el último WhatsApp de informes? Pruébalo hoy con un número que no conozcan.',
    hashtags='#Prospectos #TiempoDeRespuesta'))

P.append(dict(n=15, serie=2, slug='21 veces mas probable en 5 minutos',
    eyebrow='PRIMER CONTACTO · PROBABILIDAD DE CALIFICAR AL PROSPECTO',
    h1='Responder en 5 minutos: <em>21 veces</em> más probable calificar al prospecto.',
    grafica=[dict(tipo='barras', fmt='x', max=21, alto=56, items=[('Respuesta en menos de 5 minutos', 21, 'c3'), ('Respuesta a los 30 minutos', 1, 'c2')]),
             dict(tipo='stats', items=[('60×', 'más probable contactarlo respondiendo en 1 hora que en 24 horas'), ('+391%', 'de conversión al responder en el primer minuto')])],
    lectura='No es una ventana de horas. Es una ventana de minutos, y se cierra sola.',
    nota='Fuente: MIT / InsideSales.com (Dr. James Oldroyd), Lead Response Management Study; Harvard Business Review, «The Short Life of Online Sales Leads» (2.24 M leads); Velocify.',
    titulo='Responder en 5 minutos hace 21 veces más probable calificar al prospecto que a los 30 minutos',
    parrafos=['Responder a un prospecto en menos de cinco minutos hace 21 veces más probable calificarlo que responder a los 30 minutos. Contactarlo en la primera hora es 60 veces más probable que en 24 horas. Y responder en el primer minuto sube la conversión 391%.',
              'Cuando una mamá escribe «quisiera informes», no está mandando un recado: está abriendo una ventana de decisión. Y esa ventana tiene una vida medida con precisión por dos décadas de investigación: se cierra en minutos. El colegio que entiende esto no necesita más mensajes. Necesita dejar de perder los que ya llegan.'],
    pregunta='¿Tu proceso de admisión está diseñado para minutos o para «mañana le marco»?',
    hashtags='#Prospectos #TiempoDeRespuesta'))

P.append(dict(n=16, serie=2, slug='Un WhatsApp sin contestar cuesta 450 mil pesos',
    eyebrow='LA MATEMÁTICA DEL SILENCIO · VALOR DE VIDA DE UNA FAMILIA',
    h1='Un WhatsApp sin contestar cuesta <em>$450 mil</em> pesos.',
    grafica=dict(tipo='barras', fmt='mxn', alto=52,
                 items=[('Colegiatura anual (11 meses + inscripción)', 54000, 'c1'), ('Permanencia esperada (6 años)', 324000, 'c1'), ('Con probabilidad de hermano (×1.4)', 450000, 'c3')]),
    lectura='$0 cuesta en publicidad capturar a una familia que ya escribió. Solo requiere proceso.',
    nota='Modelo con supuestos conservadores de un colegio típico: colegiatura de $4,500 MXN mensuales, permanencia promedio de 6 años, factor de hermanos ×1.4. Cada institución puede recalcularlo con sus propias cifras.',
    titulo='Cuánto cuesta un WhatsApp sin contestar: $450,000 pesos por familia',
    parrafos=['Pongámosle número al silencio, con cifras conservadoras de un colegio típico: colegiatura de $4,500 al mes son $54,000 al año con inscripción. Seis años de permanencia: $324,000. Con la probabilidad de hermano que todo director conoce, ×1.4: alrededor de $450,000 pesos por familia inscrita.',
              'Ese es el precio de cada «ahorita le contesto» que se volvió nunca. No se pierde por falta de demanda, ni de publicidad, ni de prestigio: se pierde por velocidad. Y capturar a una familia que ya escribió cuesta $0 en anuncios. Solo requiere proceso.'],
    pregunta='¿Cuántas familias se enfriaron en tu colegio el ciclo pasado? Multiplica por $450,000.',
    hashtags='#ValorDeVida #Prospectos'))

P.append(dict(n=17, serie=2, slug='Mismas 40 familias 6 inscripciones de diferencia',
    eyebrow='LA MATEMÁTICA DEL SILENCIO · 40 CONSULTAS POR TEMPORADA',
    h1='Mismas 40 familias. <em>6 inscripciones</em> de diferencia.',
    grafica=dict(tipo='embudo', total=40, izq=dict(titulo='Responde en horas, sin seguimiento', lleno=4, cifra='4 a 5', color='c2'),
                 der=dict(titulo='Responde en minutos, seguimiento al día siguiente', lleno=10, cifra='10 a 12', color='c3')),
    lectura='La publicidad compra interés. Solo el proceso lo convierte. 6 familias son $2.7 millones de pesos de valor de vida por temporada.',
    nota='Patrón observado en los diagnósticos Rayos X de SuperLeads en colegios mexicanos; cifras de un colegio típico, ilustrativas. Valor de vida por familia: ≈ $450,000 MXN.',
    titulo='Las mismas 40 familias: 4 inscripciones respondiendo en horas, 10 respondiendo en minutos',
    parrafos=['Un colegio que recibe 40 consultas reales por temporada y responde como el promedio del sector, horas después y sin seguimiento asignado, convierte típicamente 4 o 5. El mismo colegio respondiendo en minutos, con seguimiento al día siguiente y propuesta concreta tras el recorrido, convierte 10 a 12.',
              'La diferencia, 6 familias, son $2.7 millones de pesos de valor de vida por temporada, perdidos no por falta de demanda sino por velocidad. Es el hallazgo que más sorprende a los directores en nuestros diagnósticos: el crecimiento más barato del colegio no está en conseguir más mensajes. Está en dejar de perder los que ya llegan.'],
    pregunta='Antes de invertir un peso más en anuncios: ¿cuántas de tus últimas 40 consultas recibieron respuesta en menos de 5 minutos?',
    hashtags='#Embudo #Prospectos'))

P.append(dict(n=18, serie=2, slug='71 no consideraria un colegio con menos de 3 estrellas',
    eyebrow='RESEÑAS · LA BOLETA QUE ESCRIBEN OTROS PADRES',
    h1='<em>71%</em> no consideraría un colegio con menos de 3 estrellas.',
    grafica=dict(tipo='estrellas'),
    lectura='88% de los consumidores es más propenso a elegir un negocio que responde a todas sus reseñas. La respuesta a una queja no es para el papá que se quejó: es para las cien familias que la leerán.',
    nota='Fuente: BrightLocal, Local Consumer Review Survey 2024–2026 (83% usa Google para leer reseñas; 71% descarta menos de 3 estrellas; 88% prefiere negocios que responden); Northwestern University / Spiegel Research Center (rango 4.2–4.5; desconfianza del 46% hacia el 5.0 perfecto).',
    titulo='71% descarta un colegio con menos de 3 estrellas; el rango que más confianza genera es 4.2 a 4.5',
    parrafos=['Google concentra la conversación: 83% de los consumidores lo usa para leer reseñas. 71% no consideraría un negocio con menos de 3 estrellas. El rango que genera más confianza es 4.2 a 4.5, y 46% desconfía de un 5.0 perfecto porque lo asocia con reseñas compradas. 88% es más propenso a elegir un negocio que responde a todas sus reseñas.',
              'La recomendación de boca en boca siempre decidió inscripciones. Lo que cambió es su formato: hoy está escrita, es pública, tiene estrellas y la lee cada familia que evalúa. El director revisa la boleta de sus alumnos cada bimestre. La boleta del colegio la revisan las familias todos los días.'],
    pregunta='¿Cada cuánto revisas la boleta de tu colegio? ¿Tu última reseña negativa tiene respuesta?',
    hashtags='#Reseñas #GoogleMaps'))

P.append(dict(n=19, serie=2, slug='WhatsApp se abre 98 de 100 veces el correo 21',
    eyebrow='CANALES · TASA DE APERTURA',
    h1='WhatsApp se abre <em>98 de cada 100</em> veces. El correo, 21.',
    grafica=[dict(tipo='barras', fmt='pct', max=100, alto=56, items=[('WhatsApp', 98, 'c1'), ('Correo electrónico', 21, 'c2')], sub='Tasa de apertura de mensajes'),
             dict(tipo='stats', items=[('93%', 'de penetración de WhatsApp en México'), ('9 de 10', 'usuarios prefieren el chat antes que una llamada')])],
    lectura='Cuando una mamá escribe «quisiera informes», no está mandando un recado: está abriendo una ventana de decisión.',
    nota='Fuente: YCloud / Aunoa (tasa de apertura de WhatsApp ~98% vs. email ~21%); Blip / Aurora Inbox / Infobip (penetración de WhatsApp en México 93%; 71% de los negocios mexicanos vende por WhatsApp).',
    titulo='WhatsApp se abre 98% de las veces y el correo 21%: México es territorio WhatsApp',
    parrafos=['México es territorio WhatsApp: 93% de penetración, tasas de apertura de 98% contra 21% del correo, y 9 de cada 10 usuarios prefieren el chat antes que una llamada. El canal por el que llega la familia ya está decidido; lo único que decide el colegio es qué pasa cuando llega.',
              'Y lo que pasa, en la mayoría de los colegios, es que el WhatsApp de informes lo atiende la misma persona que contesta el teléfono, organiza el festival y apoya en caja. El mensaje más importante del año llega al canal menos atendido de la institución.'],
    pregunta='¿Quién tiene el WhatsApp de informes de tu colegio en este momento? ¿Y el domingo?',
    hashtags='#WhatsApp #Prospectos'))

P.append(dict(n=20, serie=2, slug='6 meses de decision 5 etapas',
    eyebrow='EL MAPA · CÓMO ELIGE COLEGIO UNA FAMILIA',
    h1='<em>6 meses</em> de decisión. La mitad ocurre antes de que el colegio sepa que la familia existe.',
    grafica=dict(tipo='tiempo', resaltar=[1, 2], items=[
        ('Mes 1–2', 'Algo rompe el statu quo: un cambio de casa, un mal ciclo, la entrada a kínder o secundaria. La familia decide buscar.'),
        ('Mes 2–4', 'Google, Maps y reseñas, de noche. De ~8 opciones quedan 3 o 4. Aquí se descartan más colegios que en cualquier otra etapa, sin que ninguno se entere.'),
        ('Mes 4–5', 'El WhatsApp que define la terna. El que contesta primero y mejor pasa al frente; el que tarda 2 días sale de la lista.'),
        ('Mes 5–6', 'El recorrido. La familia no viene a conocer: viene a confirmar. Evalúa cómo la reciben y si sale con propuesta y fecha.'),
        ('Mes 6', 'La decisión: económica al final, emocional siempre. Gana el colegio que generó más confianza.')]),
    lectura='87% investiga en línea antes de contactar a una sola institución. 78% de las inscripciones se concentra en dos ventanas al año.',
    nota='Fuente: Shortway, Marketing para escuelas privadas, Guía 2026 (6 meses; 87% investiga en línea); SEO Top México (78% en dos ventanas); Spinoza Estudio; Mercadotecnia Educativa.',
    titulo='6 meses para elegir colegio: la mitad de la decisión ocurre sin que el colegio lo sepa',
    parrafos=['Las familias investigan en promedio seis meses antes de elegir colegio, y 87% investiga en línea antes de contactar a una sola institución. Cinco etapas: el detonante, la investigación silenciosa en Google y Maps, el WhatsApp que define la terna, la visita que confirma y la decisión final.',
              'Lee de nuevo las etapas dos y tres: la mitad de la decisión ocurre antes de que el colegio sepa que la familia existe. La decisión ya no se toma en la sala de juntas ni en el recorrido. Se toma antes, en lugares que el colegio no ve, pero que sí puede ganar.'],
    pregunta='¿En qué etapa se entera tu colegio de que una familia lo está evaluando?',
    hashtags='#Embudo #Admisión'))

P.append(dict(n=21, serie=2, slug='76 visita en 24 horas',
    eyebrow='BÚSQUEDA LOCAL · GOOGLE MAPS ES LA NUEVA FACHADA',
    h1='<em>76%</em> de quienes buscan «cerca de mí» visitan un lugar en 24 horas.',
    grafica=[dict(tipo='donas', items=[(46, '46%', 'de todas las búsquedas en Google tiene intención local', 'c1'), (76, '76%', 'de quienes buscan «cerca de mí» visitan un lugar en las siguientes 24 horas', 'c3')]),
             dict(tipo='stats', items=[('3', 'resultados muestra el «map pack» de Google: estar ahí multiplica llamadas y visitas contra el resto')])],
    lectura='Durante décadas la primera impresión fue la barda y el portón. Hoy es un rectángulo en un mapa: foto, calificación, número de reseñas y horario.',
    nota='Fuente: Think with Google / SEMrush (intención local; búsquedas «cerca de mí» que derivan en visita en 24 h; dominio del map pack); Spinoza Estudio (Google Maps como primer punto de contacto).',
    titulo='46% de las búsquedas en Google es local y 76% de quienes buscan «cerca de mí» visitan en 24 horas',
    parrafos=['46% de todas las búsquedas en Google tiene intención local. 76% de quienes buscan «cerca de mí» visitan un lugar en las siguientes 24 horas. Y el «map pack» muestra tres resultados: estar ahí multiplica llamadas y visitas contra todo el resto.',
              'Durante décadas la primera impresión de un colegio fue su barda, su portón, su recepción. Hoy es un rectángulo en un mapa: foto de portada, calificación, número de reseñas y horario. Para las escuelas, el perfil de Google Maps es muchas veces el primer punto de contacto con los padres, y casi nadie en la institución lo administra.'],
    pregunta='Busca «colegios privados en tu zona» ahora mismo. ¿Tu colegio aparece? ¿Con fotos de este año?',
    hashtags='#GoogleMaps #SEOLocal'))

# ───────────────────────── Serie 3 · Educación privada en Latinoamérica ─────────────────────────
P.append(dict(n=22, serie=3, slug='Mexico la penetracion privada mas baja de la region',
    eyebrow='EL TAMAÑO REAL DEL MERCADO · MATRÍCULA PRIMARIA EN PRIVADA',
    h1='La penetración privada <em>más baja</em> de la región.', compacto=True,
    grafica=dict(tipo='barras', fmt='pct', max=63, alto=32, gap=10, ref=(19, 'Promedio mundial · 19%'),
                 items=[('Chile', 63, 'c1'), ('Perú', 26, 'c1'), ('Colombia', 19, 'c1'), ('Brasil', 18, 'c1'), ('Guatemala', 12, 'c1'), ('El Salvador', 12, 'c1'), ('México', 10, 'c2'), ('Estados Unidos', 9, 'neu')]),
    lectura='Perú, con una economía cuatro veces menor, inscribe en privada a una proporción 2.6 veces mayor de sus alumnos.',
    nota='Porcentaje de matrícula primaria en instituciones privadas. Fuente: Banco Mundial (SE.PRM.PRIV.ZS) / Instituto de Estadística de la UNESCO, 2022–2024.',
    titulo='Solo 10% de los alumnos de México está en escuela privada: la penetración más baja de Latinoamérica',
    parrafos=['Matrícula primaria en privada: Chile 63%, Perú 26%, Colombia 19%, Brasil 18%, Guatemala y El Salvador 12%. México: 10%. Por debajo del promedio mundial de 19%, por debajo de Guatemala, al mismo nivel que Estados Unidos, donde la escuela pública compite con presupuestos de otro planeta.',
              'Cuando un directivo mexicano dice «hay demasiados colegios», los datos responden otra cosa: hay demasiado pocas familias en la privada para el tamaño de su economía. La educación privada en México no es un mercado saturado. Es un mercado subdesarrollado. Y un mercado subdesarrollado es, por definición, un mercado por capturar.'],
    pregunta='¿Tu colegio compite contra el de enfrente, o contra la opción de no pagar?',
    hashtags='#EducaciónPrivada #Latinoamérica'))

P.append(dict(n=23, serie=3, slug='35 puede pagar solo 10 inscribe',
    eyebrow='PODER DE PAGO · HOGARES POR NSE (AMAI 2024)',
    h1='<em>35%</em> de los hogares puede pagar colegio privado. Solo <em>10%</em> inscribe.',
    grafica=dict(tipo='piramide', items=[
        ('A/B', 5.6, '2.1M', '~$120,000+/mes', True), ('C+', 13.1, '5.0M', '~$48,000/mes', True), ('C', 16.7, '6.3M', '~$28,000/mes', True),
        ('C−', 16.4, '6.2M', '~$21,000/mes', False), ('D+', 17.6, '6.7M', '~$15,000/mes', False), ('D', 22.4, '8.5M', '~$10,500/mes', False), ('E', 8.2, '3.1M', '', False)],
        corchete='13.4 millones de hogares · 35.4%'),
    lectura='En México hay más familias que pueden pagar colegio privado que familias que lo están pagando. Esa brecha es el techo de crecimiento de todo el sector.',
    nota='Hogares e ingreso familiar mensual estimado por nivel. Regla NSE AMAI 2024 sobre ~38 millones de hogares (ENIGH, INEGI). Una colegiatura sana ≈ 10% del ingreso familiar por hijo.',
    titulo='13.4 millones de hogares pueden pagar colegio privado y solo 10% de la matrícula está en privada',
    parrafos=['La Regla NSE de la AMAI clasifica los ~38 millones de hogares del país en siete niveles. Los tres superiores son el territorio natural del colegio privado: A/B, 2.1 millones de hogares con más de $120,000 al mes; C+, 5 millones con ~$48,000; C, 6.3 millones con ~$28,000. Sumados: 13.4 millones de hogares, 35% del país, que pueden sostener colegiaturas de $2,800 a más de $12,000 mensuales.',
              'Y sin embargo, solo 10% de la matrícula nacional está en privada. Léelo de nuevo: hay más familias que pueden pagar que familias que están pagando. Cada familia que cruza de la pública a la privada no es un alumno que le quitaste al colegio de enfrente: es mercado nuevo, que no existía para nadie.'],
    pregunta='«Es que la gente no puede pagar.» ¿Seguro? ¿O es que nadie le ha dado una razón para pagarte a ti?',
    hashtags='#EducaciónPrivada #NSE'))

P.append(dict(n=24, serie=3, slug='Peru 10 puede pagar 26 inscribe',
    eyebrow='LA PRUEBA PERUANA · ¿ES CUESTIÓN DE DINERO?',
    h1='Perú: <em>10%</em> puede pagar, <em>26%</em> inscribe.',
    grafica=dict(tipo='tarjetas', items=[
        ('MÉXICO', [(35, '35%', 'de los hogares puede pagar', 'c1'), (10, '10%', 'de la matrícula está en privada', 'c2')], 'Mercado angosto en uso, ancho en potencial.'),
        ('PERÚ', [(10, '10%', 'de los hogares puede pagar', 'c1'), (26, '26%', 'de la matrícula está en privada', 'c3')], 'La convicción supera al ingreso.')]),
    lectura='Cuando una familia cree que la educación de sus hijos lo vale, encuentra cómo pagarla. La pregunta nunca fue si pueden. Es a quién se la pagan.',
    nota='Fuente: APEIM, Niveles Socioeconómicos 2025 (niveles A y B: 10.4% de los hogares peruanos); Banco Mundial / UIS (matrícula primaria privada). México: AMAI 2024 y Banco Mundial.',
    titulo='Perú: 10% de los hogares puede pagar y 26% inscribe en privada. México: 35% puede, 10% inscribe',
    parrafos=['En Perú, los niveles A y B suman apenas 10.4% de los hogares, con ingresos muy inferiores a sus equivalentes mexicanos. Y aun así, 26% de los alumnos peruanos está en escuela privada, porque familias de nivel C, e incluso D, pagan pensiones de S/300 a S/600 por una razón que no aparece en ninguna encuesta de ingreso: decidieron que la pública no era opción para sus hijos, y ajustaron todo lo demás.',
              'México: 35% puede pagar, 10% inscribe. La lección peruana es brutal y liberadora a la vez: cuando una familia cree que la educación de sus hijos lo vale, encuentra cómo pagarla. La pregunta nunca fue si pueden. Es a quién se la pagan, y por qué a ti o por qué a otro.'],
    pregunta='Si una familia de ingreso medio te pregunta «¿y por qué pagar?», ¿tu colegio tiene la respuesta en una frase?',
    hashtags='#EducaciónPrivada #Perú'))

P.append(dict(n=25, serie=3, slug='La SEP no cuenta colegios cuenta RVOEs',
    eyebrow='UNIVERSO DE COLEGIOS · ALUMNOS POR COLEGIO PRIVADO',
    h1='La SEP no cuenta colegios. Cuenta <em>RVOEs</em>.', compacto=True,
    grafica=[dict(tipo='barras', fmt='num', max=310, alto=32, gap=10,
                  items=[('Chile', 310, 'c1'), ('México', 260, 'c2'), ('Brasil', 225, 'c1'), ('Colombia', 180, 'c1'), ('Perú', 180, 'c1', '~170–190')], sub='Alumnos promedio por colegio privado'),
             dict(tipo='stats', items=[('~45,000', 'RVOEs reporta la estadística oficial'), ('~20,000', 'planteles privados reales, ~5.2 M alumnos')])],
    lectura='Un colegio con kínder, primaria y secundaria aparece tres veces en la estadística. El promedio real: 260 familias por colegio, con dos o tres embudos de captación a la vez.',
    nota='Estimaciones de SuperLeads sobre censos oficiales: SEP / SIGED, Minedu / ENAHO, MEN-DUE, INEP, Mineduc Chile. Cada nivel educativo de un plantel genera su propia Clave de Centro de Trabajo.',
    titulo='México no tiene 45,000 colegios privados: tiene ~20,000 planteles con 260 alumnos en promedio',
    parrafos=['Las estadísticas oficiales reportan alrededor de 45,000 escuelas privadas de básica en México. El dato está inflado por una razón técnica que cualquier dueño conoce: cada nivel genera su propia Clave de Centro de Trabajo, así que un colegio con kínder, primaria y secundaria aparece tres veces. Corrigiendo, el universo real es de ~20,000 planteles con ~5.2 millones de alumnos: 260 por colegio, el segundo promedio más grande de la región.',
              'No es una escuelita de supervivencia: es una operación de 260 familias con nómina profesional y dos o tres niveles funcionando en paralelo. Y esa última frase esconde lo que casi nadie nombra: dos o tres niveles son dos o tres procesos de captación simultáneos, que en la mayoría de los colegios atiende la misma persona que contesta el teléfono y apoya en caja.'],
    pregunta='¿Cuántos embudos de admisión tiene tu colegio? ¿Y cuántas personas los atienden?',
    hashtags='#EducaciónPrivada #RVOE'))

P.append(dict(n=26, serie=3, slug='La elite de CDMX cobra lo mismo que Lima',
    eyebrow='COLEGIATURA MENSUAL · 10 COLEGIOS MÁS CAROS (USD)',
    h1='La élite de CDMX cobra <em>lo mismo que Lima</em>.', compacto=True,
    grafica=dict(tipo='barras', fmt='usd', max=4800, alto=32, gap=10,
                 items=[('Washington DC', 4800, 'c1'), ('São Paulo', 1850, 'c1'), ('Ciudad de México', 1050, 'c2'), ('Lima', 1000, 'c1'), ('Bogotá', 1000, 'c1'), ('Santiago', 850, 'c1'), ('Cd. de Guatemala', 650, 'c1')]),
    lectura='En una economía mayor, ni el segmento premium mexicano ha alcanzado el precio que su mercado podría sostener. En Lima, las cuotas de ingreso llegan a $18,500 USD por familia.',
    nota='USD mensuales, promedio estimado de los 10 colegios más caros de cada capital (São Paulo para Brasil), 2025–2026; no incluye cuotas de inscripción. Fuentes: rankings de colegiaturas por ciudad (El CEO / Mexico Industry; Infobae Perú; La República; The Clinic; Exame; tuitions publicadas de Washington DC).',
    titulo='Los 10 colegios más caros de CDMX cobran $1,050 USD al mes: lo mismo que Lima y Bogotá',
    parrafos=['Colegiatura mensual promedio de los diez colegios más caros de cada capital: Washington DC $4,800 USD, São Paulo $1,850, Ciudad de México $1,050, Lima $1,000, Bogotá $1,000, Santiago $850, Guatemala $650. La élite educativa mexicana cobra prácticamente lo mismo que la de Lima y Bogotá, en una economía mayor y lejos del techo regional.',
              'Dicho de otro modo: ni siquiera el segmento premium mexicano ha alcanzado el precio que su mercado podría sostener. Tiene margen en volumen y en precio, un lujo que muy pocas industrias pueden presumir. Y un detalle del modelo peruano: los colegios de élite de Lima cobran cuotas de ingreso de hasta $18,500 USD por familia. Por eso ninguno se permite perder a una familia por un WhatsApp sin contestar.'],
    pregunta='¿Cuánto vale una inscripción completa en tu colegio? ¿Y tu proceso está a la altura de esa cifra?',
    hashtags='#EducaciónPrivada #Colegiaturas'))


def armar_descripcion(p):
    """Descripción de YouTube: búsqueda y tesis en la línea 1, el dato en su voz, pregunta, fuente, serie, Rayos X, autor, hashtags."""
    s = SERIES[p['serie']]
    partes = [p['titulo'] + '.', '', '\n\n'.join(p['parrafos']), '', p['pregunta'], '',
              'Fuente: ' + p['nota'], '',
              f"Pieza {p['n']:02d} de la serie «{s['nombre']}», a partir del documento de mercado {s['doc']}. {DOCS}", '',
              RAYOS, '', AUTOR, '', f"{HASH_BASE} {p['hashtags']}"]
    return '\n'.join(partes)


if __name__ == '__main__':
    import json
    for p in P:
        assert len(p['titulo']) <= 100, (p['n'], len(p['titulo'])); assert len(p['eyebrow']) <= 58, (p['n'], p['eyebrow'])
    print(len(P), 'piezas;', {k: sum(1 for p in P if p['serie'] == k) for k in SERIES})
    for p in P:
        print(f"{p['n']:02d} · {len(p['titulo']):3d} · {len(armar_descripcion(p)):4d} · {p['titulo']}")
# Ricardo López Reyero · 181218
