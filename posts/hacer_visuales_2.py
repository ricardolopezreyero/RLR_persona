"""Visuales de los posts 10 al 33 (mismo estilo que hacer_visuales.py: negro, blanco, acento).
Fotos de los artículos cuando la imagen exacta existe; tarjetas y GIF propios cuando no."""
import os, json, glob
from PIL import Image, ImageDraw, ImageFont, ImageOps
from hacer_visuales import (f, lienzo, pie, tarjeta, guardar, envolver, W, H, NEGRO, BLANCO, GRIS, ACENTO, AV, SELLO, AQUI, RAIZ)


def foto(n, patron, titulo, orden, centro=(0.5, 0.5), recortar=True):
    src = glob.glob(os.path.join(RAIZ, 'imagenes', f'{n:02d}_*__{patron}.*'))[0]
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    if recortar:
        im = ImageOps.fit(im, (W, H), centering=centro)
    else:
        im.thumbnail((2000, 2000))
    return guardar(im, orden, titulo)


def gif(nombre, frames, duraciones, w=1200):
    out = f'Post {nombre} · v1 · {SELLO}.gif'
    fr = [i.convert('P', palette=Image.ADAPTIVE, colors=32) for i in frames]
    fr[0].save(os.path.join(AQUI, out), save_all=True, append_images=fr[1:], duration=duraciones, loop=0, optimize=True)
    return out


def p10():  # tabla de PIB de su artículo, tal cual
    return foto(3, 'img1', 'La presidenta y el filtro', 10, recortar=False)


def p11():  # boleta 2.0
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'BOLETA 2.0 · CIUDADANOS CON VOTO', font=f('demi', 30), fill=ACENTO)
    filas = [('Top 1 % de aportadores', '×100'), ('Siguiente 9 %', '×10'), ('Todos los demás', '×1'), ('Quien más ayuda recibe del Estado', '×0.1')]
    y = 230
    for i, (a, b) in enumerate(filas):
        d.rectangle((110, y, W - 110, y + 118), fill=(28, 28, 26) if i % 2 == 0 else (22, 22, 20))
        d.text((150, y + 36), a, font=f('demi', 44), fill=BLANCO)
        d.text((W - 150, y + 22), b, font=f('heavy', 70), fill=ACENTO if i < 2 else GRIS, anchor='ra')
        y += 128
    d.text((110, 760), 'Todos votan. Nadie compra un voto con miedo.', font=f('medium', 36), fill=GRIS)
    pie(d)
    return guardar(im, 11, 'Boleta 2 0 voto por aportacion')


def p13():
    return foto(45, 'img2', 'Pared con mensaje', 13, centro=(0.5, 0.6))


def p15():  # 60 impuestos → 1
    nombres = ['ISR', 'IVA', 'IEPS', 'ISN', 'PTU', 'IMSS', 'INFONAVIT', 'FONACOT', 'Tenencia', 'ISAN', 'Nómina', 'Predial', 'ISAI', 'Hospedaje', 'Derechos', 'Aprovechamientos',
               'Importación', 'Exportación', 'Cedular', 'Loterías', 'Minería', 'Hidrocarburos', 'Espectro', 'Agua', 'Refrendo', 'Placas', 'Verificación', 'Alcoholes', 'Tabaco', 'Bebidas',
               'Gasolina', 'Telecom', 'Juegos', 'Diésel', 'Carbono', 'Plaguicidas', 'Comida chatarra', 'Alimentos', 'Servicios digitales', 'Plataformas', 'Rifas', 'Espectáculos',
               'Anuncios', 'Licencias', 'Construcción', 'Fraccionamientos', 'Panteones', 'Mercados', 'Rastro', 'Estacionamiento', 'Registro', 'Catastro', 'Notarial', 'Vehicular',
               'Ambiental', 'Residuos', 'Turismo', 'Extracción', 'Cuotas', 'Multas']
    frames, dur = [], []
    cols, filas = 6, 10
    for paso in range(0, 70, 3):
        im, d = lienzo()
        d.rectangle((110, 110, 190, 118), fill=ACENTO)
        d.text((110, 138), 'COBRANZA EXPRESS DE IMPUESTOS', font=f('demi', 30), fill=ACENTO)
        vivos = max(0, 60 - paso)
        d.text((W - 110, 118), f'{vivos} impuestos', font=f('heavy', 54), fill=BLANCO if vivos else ACENTO, anchor='ra')
        for i, nombre in enumerate(nombres[:vivos]):
            c, r = i % cols, i // cols
            x, y = 110 + c * 232, 215 + r * 56
            d.text((x, y), nombre, font=f('medium', 26), fill=GRIS)
        pie(d)
        frames.append(im); dur.append(70)
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'COBRANZA EXPRESS DE IMPUESTOS', font=f('demi', 30), fill=ACENTO)
    d.text((110, 270), '1 impuesto.', font=f('heavy', 150), fill=ACENTO)
    d.text((110, 470), '1–2 % por transacción, retenido por el banco al instante.', font=f('heavy', 48), fill=BLANCO)
    d.text((110, 545), 'Sin declaración. Sin contador. Sin evasión.', font=f('medium', 40), fill=GRIS)
    pie(d)
    for _ in range(3):
        frames.append(im); dur.append(1000)
    dur[-1] = 3000
    return gif('15 · 60 impuestos a 1', frames, dur)


def p17():
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'ORGANIGRAMA GOBIERNO 2.0 · 552 PUESTOS CON KPI', font=f('demi', 30), fill=ACENTO)
    d.text((110, 210), 'El presidente se mide con 3 números.', font=f('heavy', 62), fill=BLANCO)
    cajas = [('Muertes', '= 0'), ('PIB', 'por persona'), ('kWh', 'por persona')]
    for i, (a, b) in enumerate(cajas):
        x = 110 + i * 460
        d.rectangle((x, 330, x + 420, 600), fill=(28, 28, 26))
        d.rectangle((x, 330, x + 420, 338), fill=ACENTO)
        d.text((x + 36, 380), a, font=f('heavy', 76), fill=ACENTO)
        d.text((x + 36, 480), b, font=f('demi', 44), fill=BLANCO)
    d.text((110, 660), 'Co-presidente: un solo indicador, felicidad ciudadana.', font=f('medium', 38), fill=GRIS)
    d.text((110, 715), 'Seis años. Tres indicadores. Cualquiera lo puede evaluar.', font=f('medium', 38), fill=GRIS)
    pie(d)
    return guardar(im, 17, 'Presidente 3 indicadores')


def p18():
    return foto(30, 'img1', 'Escribiendo la constitucion de 2 hojas', 18, centro=(0.5, 0.55))


def p19():
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'SELECCIÓN DE FUNCIONARIOS 2.0', font=f('demi', 30), fill=ACENTO)
    d.text((110, 240), 'Hoy:', font=f('demi', 44), fill=GRIS)
    d.text((110, 290), 'por sus palabras.', font=f('heavy', 96), fill=GRIS)
    d.text((110, 470), 'Propuesta:', font=f('demi', 44), fill=ACENTO)
    d.text((110, 520), 'por sus resultados.', font=f('heavy', 96), fill=BLANCO)
    d.text((110, 690), 'Los 3 alcaldes con más crecimiento van a la boleta de gobernador; los 3 gobernadores, a la de presidente.', font=f('medium', 30), fill=GRIS)
    pie(d)
    return guardar(im, 19, 'Por resultados no por palabras')


def p21():  # toma de protesta: pantalla negra, letras blancas
    lineas = [('Gracias.', 900), ('Gracias. Gracias.', 900), ('Gracias. Gracias. Gracias.', 1400), ('Hoy tenemos un México frustrado.', 1100), ('Hoy tenemos un México ansioso.', 1100),
              ('Hoy tenemos un México enojado.', 1300), ('Sabemos que la política no funcionó.', 1500), ('De político a empresario.', 1200), ('De caer bien a seguir un indicador.', 1400),
              ('Por 6 años, dos números:', 1200), ('Muertos.   PIB por persona.', 1800), ('Gobierno 2.0', 2600)]
    frames, dur = [], []
    for i, (t, ms) in enumerate(lineas):
        im = Image.new('RGB', (1200, 675), (0, 0, 0))
        d = ImageDraw.Draw(im)
        tam = 96 if i == len(lineas) - 1 else 54
        fu = f('heavy' if i == len(lineas) - 1 else 'medium', tam)
        ls = envolver(d, t, fu, 1040)
        y = 337 - len(ls) * tam * 0.6
        for l in ls:
            d.text((600, y), l, font=fu, fill=ACENTO if i == len(lineas) - 1 else (245, 245, 240), anchor='ma')
            y += tam * 1.2
        d.text((600, 630), 'TOMA DE PROTESTA · MÉXICO · AÑO DESCONOCIDO', font=f('demi', 18), fill=(90, 90, 88), anchor='ma')
        frames.append(im); dur.append(ms)
    return gif('21 · Toma de protesta pantalla negra', frames, dur)


def p22():
    return guardar(tarjeta('Energía por ciudadano', 'El país más avanzado es el que más energía consume por persona.',
                           'KPI del gobierno: kWh por ciudadano, subiendo cada año.', 86), 22, 'kWh por ciudadano')


def p23():
    return foto(41, 'img1', 'Semaforos sincronizados', 23, centro=(0.5, 0.35))


def p24():
    return foto(26, 'img1', 'Avenida con miles de arboles', 24)


def p25():
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'CRÉDITO AL TRABAJO FORMAL', font=f('demi', 30), fill=ACENTO)
    d.text((100, 170), '54.8%', font=ImageFont.truetype(AV, 300, index=8), fill=ACENTO)
    d.text((110, 530), 'de México trabaja en la informalidad (ENOE, 2T 2025).', font=f('heavy', 50), fill=BLANCO)
    d.text((110, 610), 'Propuesta: pagarle al que se formaliza, automático y sin trámites.', font=f('medium', 38), fill=GRIS)
    d.text((110, 665), 'Un indicador: ingreso disponible del 40 % más pobre.', font=f('medium', 38), fill=GRIS)
    pie(d)
    return guardar(im, 25, 'Credito al trabajo formal 54 8')


def p27():
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'HAY 3 TIPOS DE SOCIOS', font=f('demi', 30), fill=ACENTO)
    cajas = [('1', 'Operadores', 'Crean valor y hacen\ncrecer la empresa.', BLANCO), ('2', 'Capitalistas', 'Ponen dinero y recomiendan\nel producto todos los días.', BLANCO),
             ('3', 'Bultos de cemento', 'Ven crecer la empresa\nsin mover un dedo.', ACENTO)]
    for i, (num, a, b, col) in enumerate(cajas):
        x = 110 + i * 460
        d.rectangle((x, 230, x + 420, 640), fill=(28, 28, 26))
        d.text((x + 36, 250), num, font=f('heavy', 120), fill=(60, 60, 58))
        d.text((x + 36, 400), a, font=f('heavy', 44 if i < 2 else 40), fill=col)
        d.text((x + 36, 470), b, font=f('medium', 28), fill=GRIS, spacing=8)
    d.text((110, 700), 'Quédatelos de amigos, no de socios. Un bulto pesa.', font=f('medium', 38), fill=GRIS)
    pie(d)
    return guardar(im, 27, 'Tres tipos de socios')


def p29():  # contador de videollamadas 0 → 300 y versión V41
    frames, dur = [], []
    pasos = 40
    fn = ImageFont.truetype(AV, 230, index=8)
    for i in range(pasos + 16):
        t = min(1, i / pasos)
        val = round(300 * (1 - (1 - t) ** 3))
        im = Image.new('RGB', (1200, 675), NEGRO)
        d = ImageDraw.Draw(im)
        d.rectangle((80, 80, 140, 86), fill=ACENTO)
        d.text((80, 104), 'DE $0 A $1M USD ARR', font=f('demi', 26), fill=ACENTO)
        d.text((80, 170), f'{val}', font=fn, fill=ACENTO if t >= 1 else BLANCO)
        d.text((86, 440), 'videollamadas de venta 1:1, hechas por el founder', font=f('heavy', 44), fill=BLANCO)
        d.text((86, 510), 'Versión 41 del producto. Las primeras llamadas, un desastre.', font=f('medium', 30), fill=GRIS)
        d.text((80, 605), 'Ing. Ricardo López Reyero · @ricardolopezrey', font=f('demi', 24), fill=GRIS)
        frames.append(im); dur.append(45 if i < pasos else 120)
    dur[-1] = 2500
    return gif('29 · 300 videollamadas', frames, dur)


def p31():
    im, d = lienzo()
    d.rectangle((110, 110, 190, 118), fill=ACENTO)
    d.text((110, 138), 'LEER POR ENCONTRAR LA FRASE QUE LO CAMBIA TODO', font=f('demi', 30), fill=ACENTO)
    d.text((110, 210), '150 libros.', font=f('heavy', 110), fill=BLANCO)
    d.text((110, 345), 'Una frase.', font=f('heavy', 110), fill=ACENTO)
    libros = ['Autobiografía de un yogui · Yogananda', 'Thinking in Systems · Meadows', 'The Road Less Stupid · Cunningham', 'Meditaciones · Marco Aurelio']
    y = 510
    for l in libros:
        d.text((110, y), '· ' + l, font=f('medium', 34), fill=GRIS)
        y += 48
    pie(d)
    return guardar(im, 31, '150 libros una frase')


def p32():  # meses → minutos
    frames, dur = [], []
    etapas = [('Meses.', GRIS, 1200), ('Semanas.', GRIS, 700), ('Días.', GRIS, 600), ('Horas.', BLANCO, 600), ('Minutos.', ACENTO, 2800)]
    for i, (t, col, ms) in enumerate(etapas):
        im = Image.new('RGB', (1200, 675), NEGRO)
        d = ImageDraw.Draw(im)
        d.rectangle((80, 80, 140, 86), fill=ACENTO)
        d.text((80, 104), 'LOS SUPERPODERES QUE DA LA IA', font=f('demi', 26), fill=ACENTO)
        d.text((80, 170), 'Lo que me tardaba', font=f('medium', 40), fill=GRIS)
        d.text((80, 230), t, font=f('heavy', 180), fill=col)
        if i == len(etapas) - 1:
            d.text((80, 470), '100X el impacto. No 10 % mejor.', font=f('heavy', 48), fill=BLANCO)
        d.text((80, 605), 'Ing. Ricardo López Reyero · @ricardolopezrey', font=f('demi', 24), fill=GRIS)
        frames.append(im); dur.append(ms)
    return gif('32 · De meses a minutos', frames, dur)


def p33():
    return foto(50, 'img1', 'Donde escribo', 33, centro=(0.4, 0.5))


HECHOS = {10: p10, 11: p11, 13: p13, 15: p15, 17: p17, 18: p18, 19: p19, 21: p21, 22: p22, 23: p23, 24: p24, 25: p25, 27: p27, 29: p29, 31: p31, 32: p32, 33: p33}

if __name__ == '__main__':
    posts = json.load(open(os.path.join(AQUI, 'posts.json')))
    por = {p['orden']: p for p in posts}
    for orden, fn in HECHOS.items():
        nombre = fn()
        por[orden]['visual'] = nombre
        print(orden, nombre)
    json.dump(posts, open(os.path.join(AQUI, 'posts.json'), 'w'), ensure_ascii=False, indent=1)
