"""Visuales v2 de los 33 posts: más atrevidos. Tipografía gigante que llena el cuadro, palabras tachadas en rojo,
sellos inclinados, y una sola idea por imagen. Mismo negro/blanco/amarillo + rojo para negar."""
import os, json, glob
from PIL import Image, ImageDraw, ImageFont, ImageOps
from hacer_visuales import f, pie, envolver, W, H, NEGRO, BLANCO, GRIS, ACENTO, AV, SELLO, AQUI, RAIZ

ROJO = (229, 36, 43)
SELLO_V = SELLO


def lienzo(color=NEGRO):
    im = Image.new('RGB', (W, H), color)
    return im, ImageDraw.Draw(im)


def ajustar(d, texto, peso, maximo, ancho, minimo=40):
    """Tamaño de fuente más grande con el que el texto cabe en `ancho`."""
    t = maximo
    while t > minimo and d.textlength(texto, font=f(peso, t)) > ancho:
        t -= 4
    return f(peso, t), t


def tachar(d, x, y, texto, fuente, color=ROJO, grosor=None):
    w = d.textlength(texto, font=fuente)
    h = fuente.size
    g = grosor or max(8, h // 11)
    d.line((x - 10, y + h * 0.62, x + w + 10, y + h * 0.48), fill=color, width=g)


def sello(im, texto, xy, angulo=-12, color=ROJO, tam=44):
    """Sello inclinado tipo tinta: marco + texto, pegado en xy (centro)."""
    fu = f('heavy', tam)
    tmp = Image.new('RGBA', (1200, 300), (0, 0, 0, 0))
    d = ImageDraw.Draw(tmp)
    w = d.textlength(texto, font=fu)
    x0, y0 = 600 - w / 2 - 30, 150 - tam * 0.75
    d.rounded_rectangle((x0, y0, x0 + w + 60, y0 + tam * 1.5), radius=12, outline=color, width=8)
    d.text((600, 150), texto, font=fu, fill=color, anchor='mm')
    tmp = tmp.rotate(angulo, resample=Image.BICUBIC, expand=True)
    im.paste(tmp, (int(xy[0] - tmp.width / 2), int(xy[1] - tmp.height / 2)), tmp)


def golpe(orden, nombre, etiqueta, lineas, remate=None, sello_txt=None, sello_xy=None, maximo=170, y0=215, fondo=NEGRO, pie_claro=True):
    """lineas: [(texto, color, tachado)] en tipografía gigante, una debajo de otra."""
    im, d = lienzo(fondo)
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), etiqueta.upper(), font=f('demi', 30), fill=ACENTO)
    y = y0
    for texto, color, tach in lineas:
        fu, t = ajustar(d, texto, 'heavy', maximo, W - 220)
        d.text((110, y), texto, font=fu, fill=color)
        if tach:
            tachar(d, 110, y, texto, fu)
        y += int(t * 1.08)
    if remate:
        tam = 40
        while tam > 26 and y + 30 + len(envolver(d, remate, f('medium', tam), W - 220)) * (tam + 18) > H - 140:
            tam -= 2
        for l in envolver(d, remate, f('medium', tam), W - 220):
            y += 14
            d.text((110, y + 16), l, font=f('medium', tam), fill=GRIS)
            y += tam + 4
    pie(d, pie_claro)
    if sello_txt:
        sello(im, sello_txt, sello_xy or (W - 380, 190))
    return guardar(im, orden, nombre)


def guardar(im, n, titulo, ext='png', **kw):
    nombre = f'Post {n} · {titulo} · v2 · {SELLO_V}.{ext}'
    im.save(os.path.join(AQUI, nombre), **kw)
    return nombre


def foto(n, patron, titulo, orden, centro=(0.5, 0.5), banda=None, sello_txt=None):
    """Foto del artículo, con una banda negra abajo y texto gigante opcional."""
    src = glob.glob(os.path.join(RAIZ, 'imagenes', f'{n:02d}_*__{patron}.*'))[0]
    im = ImageOps.fit(ImageOps.exif_transpose(Image.open(src)).convert('RGB'), (W, H), centering=centro)
    if banda:
        capa = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        cd = ImageDraw.Draw(capa)
        cd.rectangle((0, H - 300, W, H), fill=(13, 13, 13, 225))
        im = Image.alpha_composite(im.convert('RGBA'), capa).convert('RGB')
        d = ImageDraw.Draw(im)
        fu, t = ajustar(d, banda, 'heavy', 96, W - 220)
        d.text((110, H - 270), banda, font=fu, fill=ACENTO)
        pie(d)
    if sello_txt:
        sello(im, sello_txt, (W - 380, 190))
    return guardar(im, orden, titulo)


# ---------- los 33 ----------

def v1():   # GIF 1,171 se queda
    return None


def v2():   # su infografía, se queda
    return None


def v3():
    return golpe(3, 'IMSS no esta quebrado', 'El error de 1943 · IMSS',
                 [('El IMSS no está', BLANCO, False), ('QUEBRADO.', GRIS, True), ('Está mal armado.', ACENTO, False)],
                 'Parte de tu cuota no compra consultas ni medicinas: paga pensiones de 1966.', maximo=136)


def v5():
    return golpe(5, 'Impuestos tachado aportaciones', 'Cobranza de impuestos 2.0',
                 [('IMPUESTOS', GRIS, True), ('APORTACIONES.', ACENTO, False)],
                 'Quien aporta es un donador, no un sospechoso. Gracias a eso existe la calle de hoy.', sello_txt='GRACIAS')


def v6():
    im, d = lienzo()
    for x in range(0, W, 120):  # barrotes
        d.rectangle((x, 0, x + 26, H), fill=(26, 26, 24))
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'PRESOS Y CÁRCELES 2.0', font=f('demi', 30), fill=ACENTO)
    fu, t = ajustar(d, 'La biblioteca más grande', 'heavy', 120, W - 220)
    d.text((110, 230), 'La biblioteca más grande', font=fu, fill=BLANCO)
    d.text((110, 230 + int(t * 1.08)), 'de la ciudad', font=fu, fill=BLANCO)
    d.text((110, 230 + int(t * 2.16)), 'va en la cárcel.', font=fu, fill=ACENTO)
    d.text((110, 700), 'Emociones todos los días. Un oficio. Y libros.', font=f('medium', 40), fill=GRIS)
    pie(d)
    return guardar(im, 6, 'Biblioteca en la carcel')


def v7():   # pavimento con foto, se queda
    return None


def v8():
    return golpe(8, 'Se acaban las campanas', 'Selección presidencial 2.0',
                 [('Se acaban las', BLANCO, False), ('CAMPAÑAS.', GRIS, True)],
                 'Candidatos: los 6 gobernadores que más subieron el ingreso por persona. Medido cada año, público.', sello_txt='SIN OPINIONES')


def v9():
    return golpe(9, 'Gobierno barato gobierno lento', 'Sueldos en el gobierno',
                 [('Gobierno barato', GRIS, False), ('= gobierno lento.', ACENTO, False)],
                 'Un Player A no deja la iniciativa privada por amor al arte. Lo mejor se paga.', maximo=130)


def v10():
    src = glob.glob(os.path.join(RAIZ, 'imagenes', '03_*__img1.*'))[0]
    tabla = Image.open(src).convert('RGB')
    tabla.thumbnail((700, 560))
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'LA PRESIDENTA Y EL FILTRO', font=f('demi', 30), fill=ACENTO)
    d.text((110, 215), 'Todo el', font=f('heavy', 120), fill=BLANCO)
    d.text((110, 340), 'poder.', font=f('heavy', 120), fill=BLANCO)
    d.text((110, 500), '+0.8 %', font=f('heavy', 150), fill=ROJO)
    d.text((110, 670), 'de PIB en 2025.', font=f('medium', 44), fill=GRIS)
    d.text((110, 725), 'No es ella. Es el sistema que la puso ahí.', font=f('medium', 36), fill=GRIS)
    im.paste(tabla, (W - 110 - tabla.width, 200))
    d.rectangle((W - 110 - tabla.width, 200, W - 110, 200 + tabla.height), outline=(60, 60, 58), width=2)
    pie(d)
    return guardar(im, 10, 'Todo el poder 0 8 por ciento')


def v11():
    im, d = lienzo((245, 243, 236))
    d.rectangle((110, 110, 190, 118), fill=NEGRO)
    d.text((110, 138), 'BOLETA 2.0 · CIUDADANOS CON VOTO', font=f('demi', 30), fill=NEGRO)
    filas = [('Top 1 % de aportadores', '×100', NEGRO), ('Siguiente 9 %', '×10', NEGRO), ('Todos los demás', '×1', (120, 120, 115)), ('Quien más ayuda recibe del Estado', '×0.1', (120, 120, 115))]
    y = 225
    for a, b, col in filas:
        d.rectangle((110, y + 30, 150, y + 70), outline=NEGRO, width=5)
        if b == '×100':
            d.line((118, y + 50, 130, y + 64), fill=NEGRO, width=7); d.line((130, y + 64, 146, y + 36), fill=NEGRO, width=7)
        d.text((180, y + 22), a, font=f('demi', 46), fill=col)
        d.text((W - 110, y + 8), b, font=f('heavy', 74), fill=col, anchor='ra')
        y += 118
    d.text((110, 730), 'Todos votan. Nadie compra un voto con miedo.', font=f('medium', 36), fill=(90, 90, 86))
    pie(d, oscuro=False)
    sello(im, 'PROPUESTA INCÓMODA', (W - 460, 150), angulo=-8)
    return guardar(im, 11, 'Boleta 2 0 propuesta incomoda')


def v12():
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'POLÍTICA 100 % VIVOS', font=f('demi', 30), fill=ACENTO)
    d.text((90, 150), '0', font=ImageFont.truetype(AV, 520, index=8), fill=ACENTO)
    d.text((470, 330), 'muertos.', font=f('heavy', 120), fill=BLANCO)
    d.text((470, 470), 'No «menos». Cero.', font=f('medium', 44), fill=GRIS)
    d.rectangle((0, 640, W, 740), fill=ROJO)
    d.text((W / 2, 690), 'Si matas a una persona: prisión hasta tu muerte biológica.', font=f('heavy', 40), fill=BLANCO, anchor='mm')
    pie(d)
    return guardar(im, 12, 'Cero muertos')


def v13():
    return foto(45, 'img2', 'Pared con mensaje', 13, centro=(0.5, 0.6), banda='Imagina una ley: 5 años pintando lo que rayaste.')


def v14():
    return golpe(14, 'Mexico esta como esta por quien vota', 'México sin dirección',
                 [('México está', BLANCO, False), ('como está', BLANCO, False), ('por quien vota.', ACENTO, False)],
                 'Escasez elige escasez. No es el ciudadano ni el político: es el sistema de selección.', sello_txt='NADIE QUIERE DECIRLO', sello_xy=(W - 460, 170), maximo=130)


def v15():   # GIF se queda
    return None


def v16():
    return golpe(16, 'Sistematiza la corrupcion', 'La corrupción se acaba al sistematizar',
                 [('No acabes con la', GRIS, False), ('CORRUPCIÓN.', GRIS, True), ('Sistematízala.', ACENTO, False)],
                 'Spotify no prohibió la piratería: la volvió lenta. Lo legal ganó por eficiencia.', maximo=140)


def v17():
    return golpe(17, 'Presidente 3 numeros', 'Organigrama Gobierno 2.0 · 552 puestos con KPI',
                 [('El presidente', BLANCO, False), ('se mide con', BLANCO, False), ('3 números.', ACENTO, False)],
                 'Muertes = 0 · PIB por persona · kWh por persona. Seis años. Nada más.', maximo=130)


def v18():
    return foto(30, 'img1', 'Constitucion de 2 hojas', 18, centro=(0.5, 0.55), banda='Si no cabe en 2 hojas, no es un pacto. Es un laberinto.')


def v19():
    return golpe(19, 'Palabras tachado resultados', 'Selección de funcionarios 2.0',
                 [('Hoy: por sus', GRIS, False), ('PALABRAS.', GRIS, True), ('Por sus resultados.', ACENTO, False)],
                 'Sin partidos. Sin INE. Números públicos cada año.', maximo=140)


def v20():
    return golpe(20, 'America un solo nombre', 'Un continente, un nombre',
                 [('AMÉRICA.', ACENTO, False)],
                 'No con fuerza. Con resultados. Primero México funciona; luego cada país entra por lo que más necesita.', sello_txt='EJERCICIO, NO POLÍTICA', maximo=230, y0=240)


def v21():   # GIF se queda
    return None


def v22():
    return golpe(22, 'Ahorrar tachado usar mas', 'Energía por ciudadano',
                 [('AHORRAR', GRIS, True), ('energía.', GRIS, False), ('Usar más.', ACENTO, False)],
                 'El país más avanzado es el que más energía consume por persona. KPI: kWh por ciudadano.', maximo=136)


def v23():
    return foto(41, 'img1', 'Semaforos 1666 dias', 23, centro=(0.5, 0.35), banda='1,666 días laborales perdidos. Cada día. Por no sincronizar.')


def v24():
    return foto(26, 'img1', 'Semaforo mas arbol', 24, banda='Regla: semáforo + árbol. Miles, no cientos.')


def v25():
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'CRÉDITO AL TRABAJO FORMAL', font=f('demi', 30), fill=ACENTO)
    d.text((100, 150), '54.8%', font=ImageFont.truetype(AV, 330, index=8), fill=ROJO)
    d.text((110, 540), 'de México trabaja sin contrato, sin IMSS, sin nada.', font=f('heavy', 52), fill=BLANCO)
    d.text((110, 625), 'Propuesta: pagarle al que se formaliza. Automático. Cero trámites.', font=f('medium', 38), fill=GRIS)
    pie(d)
    sello(im, 'ENOE 2T 2025', (W - 330, 170), angulo=-8, tam=34)
    return guardar(im, 25, '54 8 informal')


def v26():
    return golpe(26, '15 bancos 0 prestamos', 'Crédito productivo para colegios',
                 [('15 bancos.', GRIS, False), ('0 préstamos.', ROJO, False), ('3,300 alumnos.', ACENTO, False)],
                 'Los bancos no le prestan a colegios. Y esa gente forma a los líderes del México que viene.', maximo=140)


def v27():
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'HAY 3 TIPOS DE SOCIOS', font=f('demi', 30), fill=ACENTO)
    d.text((110, 215), 'Operadores.', font=f('heavy', 96), fill=BLANCO)
    d.text((110, 325), 'Capitalistas.', font=f('heavy', 96), fill=BLANCO)
    d.text((110, 435), 'Bultos de cemento.', font=f('heavy', 96), fill=ACENTO)
    # el bulto
    bx, by = 1180, 560
    d.polygon([(bx, by), (bx + 300, by), (bx + 320, by + 200), (bx - 20, by + 200)], fill=(70, 70, 66))
    d.rectangle((bx + 20, by - 30, bx + 280, by), fill=(90, 90, 86))
    d.text((bx + 150, by + 100), 'BULTO', font=f('heavy', 60), fill=NEGRO, anchor='mm')
    d.text((110, 620), 'Quédatelos de amigos, no de socios.', font=f('medium', 44), fill=GRIS)
    d.text((110, 680), 'Un bulto pesa.', font=f('heavy', 44), fill=BLANCO)
    pie(d)
    return guardar(im, 27, 'Bultos de cemento')


def v29():   # GIF se queda
    return None


def v31():
    return golpe(31, '150 libros una frase', 'Leer por encontrar la frase que lo cambia todo',
                 [('150 LIBROS.', GRIS, True), ('1 frase.', ACENTO, False)],
                 'Lo que importa es cuántas frases pegaron tan duro que cambiaron la perspectiva.', maximo=190)


def v32():   # GIF se queda
    return None


def v33():
    return foto(50, 'img1', 'Donde escribo', 33, centro=(0.4, 0.5), banda='88 artículos. 0 % IA.')


HECHOS = {3: v3, 5: v5, 6: v6, 8: v8, 9: v9, 10: v10, 11: v11, 12: v12, 13: v13, 14: v14, 16: v16, 17: v17, 18: v18, 19: v19, 20: v20,
          22: v22, 23: v23, 24: v24, 25: v25, 26: v26, 27: v27, 31: v31, 33: v33}

if __name__ == '__main__':
    posts = json.load(open(os.path.join(AQUI, 'posts.json')))
    por = {p['orden']: p for p in posts}
    for orden, fn in HECHOS.items():
        nombre = fn()
        if nombre:
            por[orden]['visual'] = nombre
            if por[orden]['formato'] == 'texto':
                por[orden]['formato'] = 'imagen'
            print(orden, nombre)
    json.dump(posts, open(os.path.join(AQUI, 'posts.json'), 'w'), ensure_ascii=False, indent=1)
