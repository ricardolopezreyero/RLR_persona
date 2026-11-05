"""LinkedIn · NVIDIA AI Day Mexico City (Expo Santa Fe, 4-nov-2026): tres posts seguidos.

Ricardo subió 68 fotos a Drive («Nvidia IA Day 2026 CDMX») y pidió escoger lo mejor, editar colores, recortar,
acomodar y armar las publicaciones; la diapositiva «Anatomy of an Agent» tiene que salir sí o sí.

- Post 1 · El día: agradecimiento y narración, 10 fotos editadas (4:3, 1600 px).
- Post 2 · Anatomía de un agente: carrusel PDF 1080×1350 con la diapositiva original y su lectura pieza por pieza.
- Post 3 · Dueño de tu inteligencia: 4 fotos de diapositivas (propiedad, costo, camino a producción, límites).

Uso: python3 hacer_nvidia.py <carpeta con las fotos numeradas 00.jpg…67.jpg (orden por hora)>
Escribe todo en salida/ y una copia en ~/Downloads/."""
import os, sys, html, shutil, subprocess, tempfile, datetime
from PIL import Image, ImageOps, ImageEnhance, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
EST = os.path.join(AQUI, '..', '..', 'estadisticas')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
NOMBRE = 'file://' + os.path.abspath(os.path.join(EST, 'rlr_nombre.png'))
LOGO = open(os.path.join(EST, 'logo_blanco.svg')).read()
SELLO = datetime.datetime.now().strftime('%Y-%m-%d %Hh%M')
SALIDA = os.path.join(AQUI, 'salida')
FUENTE = sys.argv[1] if len(sys.argv) > 1 else None

# ---------- fotos ----------
# n: número por hora de toma · nombre de archivo · recorte (izq, arr, der, aba en fracción) · texto alternativo
POST1 = [
    (30, 'nvidia-ai-day-cdmx-ricardo-lopez-reyero-en-el-publico',
     (0, 0.02, 1, 1),
     'Ricardo López Reyero y un acompañante con audífonos en el público del NVIDIA AI Day Mexico City; al fondo, el letrero del evento y cientos de asistentes con audífonos iluminados.'),
    (45, 'nvidia-ai-day-cdmx-tres-conferencias-a-la-vez',
     (0, 0.18, 1, 1),
     'Escenario principal del NVIDIA AI Day Mexico City con tres pantallas y tres conferencias al mismo tiempo; el público escucha cada una con audífonos.'),
    (56, 'nvidia-ai-day-cdmx-audifonos-verdes',
     (0, 0.04, 1, 1),
     'Selfie en el auditorio del NVIDIA AI Day Mexico City: filas de asistentes con audífonos de luz verde para seguir la conferencia que cada quien eligió.'),
    (26, 'nvidia-ai-day-cdmx-expo-santa-fe',
     (0, 0.10, 1, 1),
     'Vista desde lo alto de la Expo Santa Fe durante el NVIDIA AI Day Mexico City: pasillos con stands iluminados en verde y asistentes recorriendo la exposición.'),
    (28, 'nvidia-ai-day-cdmx-panel-principal',
     (0, 0, 1, 0.92),
     'Panel en el escenario principal del NVIDIA AI Day Mexico City frente a una pantalla gigante con la imagen de un centro de datos.'),
    (39, 'nvidia-ai-day-cdmx-anatomy-of-an-agent',
     (0, 0.08, 1, 1),
     'Diapositiva «Anatomy of an Agent» en el NVIDIA AI Day Mexico City: Models, Harness, Knowledge, Tools y Runtime.'),
    (61, 'nvidia-ai-day-cdmx-panel-escalar-la-ia',
     (0, 0.10, 1, 1),
     'Panel «Escala la IA a través de Tecnología, Alianzas y Go-to-Market» en el NVIDIA AI Day Mexico City.'),
    (36, 'nvidia-ai-day-cdmx-anahuac-online',
     (0, 0.05, 1, 1),
     'Stand de Anáhuac Online en el NVIDIA AI Day Mexico City, con su mascota de león y luces verdes.'),
    (34, 'nvidia-ai-day-cdmx-arena-de-robots',
     (0, 0.05, 1, 1),
     'Arena de robots con conos y obstáculos en la zona de exhibición del NVIDIA AI Day Mexico City.'),
    (67, 'nvidia-ai-day-cdmx-llegada-expo-santa-fe',
     (0, 0, 1, 1),
     'Ricardo López Reyero y un acompañante llegando a la Expo Santa Fe para el NVIDIA AI Day Mexico City.'),
]
POST3 = [
    (48, 'nvidia-ai-day-cdmx-no-vas-a-comprar-tu-ia',
     (0.31, 0.30, 0.74, 0.90),
     'Diapositiva en el NVIDIA AI Day Mexico City: «No vas a comprar tu IA. Vas a ser dueño de ella. Y va a correr donde tú decidas».'),
    (42, 'nvidia-ai-day-cdmx-switchyard-un-tercio-del-costo',
     (0.13, 0.27, 0.90, 0.87),
     'Diapositiva «NVIDIA Switchyard Provides Frontier Accuracy at 1/3 Cost»: combinar modelos completa casi las mismas tareas con una fracción del costo.'),
    (62, 'nvidia-ai-day-cdmx-the-production-path',
     (0.18, 0, 0.90, 1),
     'Diapositiva «The Production Path»: seis pasos para llevar un agente a producción, de elegir el flujo a la liberación controlada, con seguridad, confiabilidad y observabilidad en cada etapa.'),
    (55, 'nvidia-ai-day-cdmx-openshell-limites-de-ejecucion',
     (0, 0.08, 1, 0.95),
     'Diapositiva «OpenShell Enforces Runtime Boundaries for AI Agents»: cada acción del agente se monitorea, el agente no puede tocar sus controles y corre bajo una política explícita.'),
]


def editar(n, recorte, ancho=1600):
    im = ImageOps.exif_transpose(Image.open(os.path.join(FUENTE, f'{n:02d}.jpg'))).convert('RGB')
    w, h = im.size
    l, t, r, b = recorte
    im = im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))
    im = ImageOps.autocontrast(im, cutoff=0.4)
    im = ImageEnhance.Contrast(im).enhance(1.05)
    im = ImageEnhance.Color(im).enhance(1.06)
    escala = ancho / im.width
    im = im.resize((ancho, round(im.height * escala)), Image.LANCZOS)
    return im.filter(ImageFilter.UnsharpMask(radius=1.4, percent=55, threshold=3))


def anatomia_derecha(ancho=1600):
    """La diapositiva de #39 enderezada (perspectiva) para el carrusel."""
    im = ImageOps.exif_transpose(Image.open(os.path.join(FUENTE, '39.jpg'))).convert('RGB')
    # esquinas de la pantalla en la foto: arriba-izq, abajo-izq, abajo-der, arriba-der
    quad = (72, 122, 37, 563, 780, 610, 745, 247)
    W, H = 1600, 900
    im = im.transform((W, H), Image.QUAD, quad, Image.BICUBIC)
    im = ImageOps.autocontrast(im, cutoff=0.6)
    return im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))


# ---------- carrusel ----------
CSS = """
*{margin:0;padding:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:#001240;color:#fff;font-family:'Plus Jakarta Sans',sans-serif;position:relative;overflow:hidden}
.fondo{position:absolute;inset:0;background:radial-gradient(circle at 85% 8%,rgba(118,185,0,.20),transparent 55%),
 radial-gradient(circle at 0% 100%,rgba(42,137,251,.18),transparent 50%)}
.nombre{position:absolute;left:80px;top:72px;height:44px}
.logo{position:absolute;right:80px;bottom:66px;width:202px}.logo svg{width:202px;height:auto}
.pag{position:absolute;left:80px;bottom:74px;font-size:24px;color:#7C8BB3;letter-spacing:1px}
.caja{position:absolute;left:80px;right:80px;top:200px;bottom:170px;display:flex;flex-direction:column;justify-content:center}
.etq{align-self:flex-start;color:#76B900;font-size:24px;font-weight:700;letter-spacing:1.5px;border:1px solid rgba(118,185,0,.65);
 border-radius:999px;padding:9px 18px}
h1{font-size:104px;font-weight:800;line-height:1.02;letter-spacing:-2px;margin-top:40px}
h2{font-size:64px;font-weight:800;line-height:1.08;letter-spacing:-1px;margin-top:34px}
.sub{font-size:40px;font-weight:600;line-height:1.3;color:#C9D4F2;margin-top:34px}
.verde{color:#76B900}.menta{color:#56EF9F}
.num{font-size:200px;font-weight:800;line-height:.9;color:#76B900;letter-spacing:-6px}
.en{font-size:34px;font-weight:700;color:#7C8BB3;letter-spacing:2px;text-transform:uppercase;margin-top:18px}
.idea{font-size:76px;font-weight:800;line-height:1.05;letter-spacing:-1.5px;margin-top:8px}
ul{list-style:none;margin-top:44px}
li{font-size:36px;line-height:1.32;color:#E8EEFF;padding-left:40px;position:relative;margin-bottom:22px}
li:before{content:'';position:absolute;left:0;top:16px;width:16px;height:16px;border-radius:4px;background:#76B900}
.foto{width:100%;border-radius:18px;border:2px solid rgba(255,255,255,.12);margin-top:40px}
.pie{font-size:28px;color:#9FB0D9;margin-top:26px;line-height:1.35}
.linea{display:flex;justify-content:space-between;margin-top:56px}
.pieza{width:172px;text-align:center}
.pieza b{display:flex;align-items:center;justify-content:center;width:120px;height:120px;margin:0 auto;border-radius:26px;
 background:rgba(118,185,0,.14);border:2px solid #76B900;font-size:50px;font-weight:800;color:#76B900}
.pieza span{display:block;font-size:30px;font-weight:800;margin-top:20px}.pieza i{display:block;font-style:normal;font-size:24px;color:#9FB0D9;margin-top:6px;line-height:1.25}
.pasos{margin-top:40px}
.paso{display:flex;gap:26px;align-items:flex-start;margin-bottom:24px}
.paso b{flex:0 0 66px;height:66px;border-radius:14px;background:#76B900;color:#001240;font-size:30px;font-weight:800;display:flex;align-items:center;justify-content:center}
.paso span{font-size:36px;font-weight:800;line-height:1.15}.paso i{display:block;font-style:normal;font-size:28px;font-weight:500;color:#C9D4F2;margin-top:4px}
.banda{margin-top:18px;padding:20px 26px;border-radius:16px;background:rgba(86,239,159,.10);border:1px solid rgba(86,239,159,.4);font-size:30px;color:#E8EEFF}
"""

PIEZAS = [
    ('01', 'Models', 'Conocimiento concentrado.',
     ['Ya existen y son muchos: Claude, Gemini, GPT, Llama, Mistral, Nemotron.',
      'No hay que casarse con uno: se combinan.',
      'NVIDIA mostró que mezclar modelos da precisión de frontera a una tercera parte del costo.']),
    ('02', 'Harness', 'Los límites.',
     ['Contexto, estado, herramientas y evaluación.',
      'Orquesta el ciclo: piensa, actúa, revisa y vuelve a intentar.',
      'Sandbox y política: qué puede hacer y qué no.']),
    ('03', 'Knowledge', 'Lo que sabe tu organización.',
     ['Tus datos, los ordenados y los que viven en documentos.',
      'Con ellos el agente busca, analiza y predice.',
      'Un modelo sin tu conocimiento es un genio que no conoce tu negocio.']),
    ('04', 'Tools', 'Las manos.',
     ['Lo que el agente puede hacer en el mundo: consultar, escribir, ejecutar.',
      'Cada herramienta es un permiso.',
      'Pocas herramientas y reglas de aprobación claras: así se empieza.']),
    ('05', 'Runtime', 'Cuando está corriendo.',
     ['Cada acción del agente se monitorea.',
      'El agente no puede tocar sus propios controles.',
      'Corre bajo una política explícita y los datos se quedan dentro de tu frontera.']),
]

PASOS = [
    ('01', 'Flujo y valor', 'Elige el flujo y define qué es éxito.'),
    ('02', 'Datos y permisos', 'Datos al día, accesos y origen cuidados.'),
    ('03', 'Agente y acciones', 'Limita herramientas y fija reglas de aprobación.'),
    ('04', 'Evaluación', 'Verifica resultados, precisión y repetibilidad.'),
    ('05', 'Carga y recuperación', 'Demanda real: latencia, costo y recuperación.'),
    ('06', 'Liberación controlada', 'Pocos usuarios primero; mide, mejora y crece.'),
]


def pagina(cuerpo, i, total):
    return f"""<!doctype html><meta charset="utf-8"><style>{CSS}</style><body><div class="fondo"></div>
<img class="nombre" src="{NOMBRE}"><div class="caja">{cuerpo}</div>
<div class="pag">{i} / {total}</div><div class="logo">{LOGO}</div></body>"""


def carrusel(foto_anatomia):
    e = html.escape
    pags = [
        f'<span class="etq">NVIDIA AI DAY · CIUDAD DE MÉXICO</span><h1>Anatomía de<br>un <span class="verde">agente</span></h1>'
        f'<div class="sub">La IA ya no es la pregunta. La pregunta es qué construyes con lo que ya existe.</div>',
        f'<span class="etq">LA DIAPOSITIVA QUE ME LLEVÉ</span><h2>Cinco piezas.<br>Ni una más.</h2>'
        f'<img class="foto" src="file://{foto_anatomia}"><div class="pie">«Anatomy of an Agent» · NVIDIA AI Day Mexico City, 4 de noviembre de 2026.</div>',
        '<span class="etq">EL MAPA</span><h2>Un agente no es un modelo.<br><span class="verde">Es un sistema.</span></h2><div class="linea">'
        + ''.join(f'<div class="pieza"><b>{n}</b><span>{en}</span><i>{e(idea.rstrip("."))}</i></div>' for n, en, idea, _ in PIEZAS)
        + '</div>',
    ]
    for n, en, idea, puntos in PIEZAS:
        pags.append(f'<div class="num">{n}</div><div class="en">{en}</div><div class="idea">{e(idea)}</div>'
                    '<ul>' + ''.join(f'<li>{e(p)}</li>' for p in puntos) + '</ul>')
    pags.append('<span class="etq">THE PRODUCTION PATH</span><h2>De la demo a producción, en seis pasos.</h2><div class="pasos">'
                + ''.join(f'<div class="paso"><b>{n}</b><div><span>{e(t)}</span><i>{e(d)}</i></div></div>' for n, t, d in PASOS)
                + '</div><div class="banda">En cada paso: seguridad, confiabilidad y observabilidad.</div>')
    pags.append('<span class="etq">LO QUE ME LLEVO</span><h1 style="font-size:88px">La IA ya<br>quedó atrás.</h1>'
                '<div class="sub">Lo que sigue es qué haces con lo que ya existe: <span class="menta">agentes con límites, con tu conocimiento y bajo tu control.</span></div>'
                '<div class="sub" style="font-size:34px;color:#9FB0D9">Gracias, NVIDIA.</div>')
    return pags


def render(paginas, carpeta):
    pngs = []
    with tempfile.TemporaryDirectory() as tmp:
        for i, cuerpo in enumerate(paginas, 1):
            h = os.path.join(tmp, f'{i:02d}.html')
            open(h, 'w', encoding='utf-8').write(pagina(cuerpo, i, len(paginas)))
            png = os.path.join(carpeta, f'Lámina {i:02d}.png')
            subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--allow-file-access-from-files',
                            '--force-device-scale-factor=1', '--window-size=1080,1350', f'--screenshot={png}', 'file://' + h],
                           check=True, capture_output=True)
            pngs.append(png)
    return pngs


# ---------- textos ----------
# Las menciones se escriben con @ en LinkedIn y se eligen de la lista: @NVIDIA (linkedin.com/company/nvidia)
# y @Jensen Huang (linkedin.com/in/jenhsunhuang, «Founder and CEO, NVIDIA»).
TEXTOS = {
    'Post 1 · El día': """Hoy fui al NVIDIA AI Day en la Expo Santa Fe y salí con otra cabeza.

Primero, el formato. Tres conferencias al mismo tiempo, en el mismo escenario, y cada quien con audífonos escuchando la que eligió. Nunca me había tocado y me encantó: cientos de personas en silencio, cada una en su propia charla, con luces verdes en la cabeza.

Segundo, el fondo. Lo que más escuché fue esto: hablar de inteligencia artificial ya quedó en el pasado. La conversación ahora es qué haces con lo que ya existe. Y lo que ya existe se llama agentes.

Me llevo tres ideas:

1. Un agente no es un modelo. Es un sistema de cinco piezas: modelo, arnés, conocimiento, herramientas y ejecución.
2. No vas a comprar tu IA. Vas a ser dueño de ella, y va a correr donde tú decidas.
3. De la demo a producción hay un camino, y empieza con pocos usuarios, límites claros y medición en cada paso.

Encontré conocimiento premium que no habría encontrado en otro lado. Como startupero, esto me cambió la perspectiva de los próximos cinco años. Y cuando cambia la perspectiva, cambia todo.

Aquí vi a una compañía intentando que América Latina use la inteligencia artificial de forma consciente y sabia. Un evento de este tamaño no se hace solo, y lo abrieron con ganas de compartir lo que saben.

Me considero un geek, y hoy fue un gran día para mí. Así se hacen los eventos. Mis respetos a los organizadores y a todo el equipo.

Gracias, @NVIDIA. Gracias, @Jensen Huang.

En los próximos días comparto lo que más me sirvió, empezando por la diapositiva que me traje a casa: la anatomía de un agente.

#NVIDIA #InteligenciaArtificial #AgentesDeIA #AIDay""",
    'Post 2 · Anatomía de un agente': """La diapositiva que más me llevé del NVIDIA AI Day fue la más sencilla: «Anatomy of an Agent».

Cinco piezas. Ni una más.

1. Modelo: conocimiento concentrado. Ya existen y son muchos, y se pueden combinar.
2. Arnés (harness): los límites. Contexto, estado, evaluación y política: lo que convierte a un modelo en un trabajador confiable.
3. Conocimiento: lo que sabe tu organización. Sin esto, el agente es un genio que no conoce tu negocio.
4. Herramientas: las manos. Cada herramienta es un permiso.
5. Ejecución (runtime): cuando está corriendo. Cada acción monitoreada, bajo una política explícita y con tus datos dentro de tu frontera.

Lo que me movió: casi todos seguimos discutiendo cuál modelo es mejor, y quizá sea la pieza que menos te diferencia. Lo que hace que un agente sirva en tu organización son las otras cuatro: los límites, tu conocimiento, las herramientas correctas y el control mientras corre.

En el carrusel está la diapositiva original, mi lectura de cada pieza y los seis pasos que NVIDIA propone para llevar un agente de la demo a producción.

¿Cuál de las cinco piezas le falta hoy a tu organización?

Gracias, @NVIDIA, por explicarlo así de claro.

#AgentesDeIA #InteligenciaArtificial #NVIDIA""",
    'Post 3 · Dueño de tu inteligencia': """«No vas a comprar tu IA. Vas a ser dueño de ella. Y va a correr donde tú decidas.»

Esa frase, de una de las charlas del NVIDIA AI Day, resume el cambio que vi en todo el evento.

Cuatro ideas que me traje para quien dirige una organización en México:

1. Ser dueño, no inquilino. Ahí mismo contaron cómo la IBERO ya es dueña de su inteligencia. Una universidad mexicana, no una tecnológica de Silicon Valley.

2. Combinar modelos cuesta menos. NVIDIA presentó que mezclar modelos logra precisión de frontera a una tercera parte del costo. Ya no se trata de pagar el modelo más caro para todo.

3. A producción se llega por pasos. Elegir el flujo y definir qué es éxito, cuidar datos y permisos, limitar acciones, evaluar, probar con demanda real y liberar primero con pocos usuarios.

4. Los límites no frenan: protegen. Cada acción monitoreada, el agente sin acceso a sus propios controles y los datos dentro de tu frontera.

Trabajo con colegios y universidades todos los días. Lo que vi de la IBERO me confirma algo: la educación privada en México no tiene que esperar a que la IA llegue. Puede ser dueña de la suya.

Gracias otra vez, @NVIDIA. Así se ayuda a un país a usar bien la inteligencia artificial.

#InteligenciaArtificial #Educación #AgentesDeIA #NVIDIA""",
}


def main():
    if os.path.isdir(SALIDA):
        shutil.rmtree(SALIDA)
    p1 = os.path.join(SALIDA, 'Post 1 · El día'); p2 = os.path.join(SALIDA, 'Post 2 · Anatomía de un agente'); p3 = os.path.join(SALIDA, 'Post 3 · Dueño de tu inteligencia')
    for c in (p1, os.path.join(p2, 'láminas'), p3):
        os.makedirs(c)
    for carpeta, fotos in ((p1, POST1), (p3, POST3)):
        alt = []
        for i, (n, nombre, rec, a) in enumerate(fotos, 1):
            editar(n, rec).save(os.path.join(carpeta, f'{i:02d} · {nombre}.jpg'), 'JPEG', quality=90, optimize=True)
            alt.append(f'{i:02d} · {nombre}.jpg\n{a}\n')
        open(os.path.join(carpeta, 'Textos alternativos.txt'), 'w', encoding='utf-8').write('\n'.join(alt))
    fa = os.path.join(p2, 'láminas', 'anatomy-of-an-agent-enderezada.jpg')
    anatomia_derecha().save(fa, 'JPEG', quality=92)
    pngs = render(carrusel(fa), os.path.join(p2, 'láminas'))
    ims = [Image.open(p).convert('RGB') for p in pngs]
    pdf = os.path.join(p2, f'Anatomía de un agente · NVIDIA AI Day · v1 · {SELLO}.pdf')
    ims[0].save(pdf, save_all=True, append_images=ims[1:], resolution=144)
    for carpeta, texto in TEXTOS.items():
        assert len(texto) <= 3000, (carpeta, len(texto))
        open(os.path.join(SALIDA, carpeta, 'Texto del post.txt'), 'w', encoding='utf-8').write(texto + '\n')
        print(carpeta, len(texto), 'caracteres')
    print(SALIDA)


if __name__ == '__main__':
    main()
