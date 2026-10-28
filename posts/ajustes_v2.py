"""Retro de Ricardo del 28-oct-2026 sobre los 33 posts:
3 más simple, 10 fuerte sin odio, 13 sin «mi ley», 14 con Salinas/Téllez/Loret, 26 sin su esposa,
el 4 (0.3 %) se retira y entra uno nuevo del artículo 54."""
import json, os

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
PUB = json.load(open(os.path.join(RAIZ, 'publicados_x.json')))
ARTS = {x['n']: x['title'] for x in json.load(open(os.path.join(RAIZ, 'x_articulos.json')))}

CAMBIOS = {
    3: "El IMSS no está quebrado.\n\nTorreón le aporta unos $5 mil millones al año. Dividido entre camas, el IMSS tiene casi el mismo dinero por cama que el mejor hospital privado de la región.\n\nEntonces, ¿por qué uno se siente de primer mundo y el otro de guerra?\n\nPorque parte de tu cuota no compra consultas ni medicinas: paga pensiones de un régimen de 1966.\n\nNo es falta de dinero. Es cómo está armado. @Tu_IMSS",
    10: "Claudia Sheinbaum tiene todo lo que su movimiento pidió durante 20 años: mayoría absoluta, el Congreso, los estados.\n\nResultado hasta hoy: +0.8 % de PIB en 2025 y los mismos muertos de siempre.\n\nNo es que sea mala persona. Es que el filtro que la puso ahí no busca al mejor para gobernar: busca al más leal a quien lo eligió.\n\nCon todo el poder y estos resultados, ya no es ella: es el sistema.",
    13: "Rayar una pared ajena no es arte. Es un insulto a quien la pagó.\n\nImagina una ley así: 5 años de servicio comunitario pintando todo lo vandalizado de la ciudad. Si te gusta pintar, pinta para todos.\n\nAsí me imagino las paredes de Torreón: con un mensaje que valga la pena leer.\n\n«Eres mucho más listo de lo que crees, confía.»\n\nEsa es la diferencia entre rayar y aportar.",
    14: "Nadie quiere decir esto:\n\nMéxico está como está por el nivel de conciencia promedio de quien vota. Una población que piensa desde la escasez elige líderes que gobiernan desde la escasez.\n\nNo es culpa del ciudadano ni del político. Es el sistema de selección, que premia hablar bonito en vez de dar resultados.\n\nLos recursos están. El talento está. La geografía está. Falta poner a las personas correctas en los puestos correctos.\n\n@RicardoBSalinas, @LillyTellez, @CarlosLoret: ustedes también lo ven. ¿Qué proponen para cambiar el sistema, no solo a quien lo ocupa?",
    26: "Vi de cerca a un colegio recorrer 15 bancos buscando crédito para crecer. Ninguno le prestó.\n\nLos bancos no le prestan a colegios: si no pagan, embargar una escuela con toda su comunidad se ve mal. Y el mercado les parece chico.\n\nEse grupo pasó de 300 a 3,300 alumnos. Sin ellos.\n\nLa SEP no apoya a la escuela privada, el banco no presta y el gobierno cobra. Y aun así esa gente forma a los líderes del México que viene.\n\nEl dinero debería fluir hacia quien construye el futuro, no alejarse de él.",
}

NUEVO_4 = {'orden': 4, 'articulo': 54, 'titulo': ARTS[54], 'formato': 'texto', 'visual': None,
           'texto': "Si estuvieras viendo tu vida en la pantalla de un cine, ¿qué te estaría gritando la audiencia que hicieras?\n\nNo vayas al sótano. Dale el beso. Aplica a ese trabajo. Escribe el libro. Márcale a esa persona.\n\nEsa voz que grita desde las butacas eres tú mismo, viendo con claridad lo que ya sabes que tienes que hacer.\n\nYo la escuché a los 39 y empecé a escribir. ¿Qué te está gritando a ti?",
           'liga': f"https://x.com/ricardolopezrey/status/{PUB['54']}", 'estado': 'propuesto 28-oct-2026: sin crear en X'}


def main():
    posts = json.load(open(os.path.join(AQUI, 'posts.json')))
    retirados = [p for p in posts if p['orden'] == 4]
    for r in retirados:
        r['estado'] = 'RETIRADO 28-oct-2026 (resta más de lo que da); sigue en borradores de X hasta que Ricardo lo borre'
    json.dump(retirados, open(os.path.join(AQUI, 'posts_retirados.json'), 'w'), ensure_ascii=False, indent=1)
    posts = [p for p in posts if p['orden'] != 4]
    posts.append(NUEVO_4)
    posts.sort(key=lambda p: p['orden'])
    for p in posts:
        if p['orden'] in CAMBIOS:
            p['texto'] = CAMBIOS[p['orden']]
            p['estado'] = p['estado'].split(';')[0] + '; texto ajustado 28-oct-2026 con retro de Ricardo' + (' (en X sigue el texto viejo)' if p['orden'] <= 9 else '')
        p['texto_x'] = p['texto'] + '\n\nLo escribí completo aquí: ' + p['liga']
    json.dump(posts, open(os.path.join(AQUI, 'posts.json'), 'w'), ensure_ascii=False, indent=1)
    print(len(posts), [p['orden'] for p in posts if 'ajustado' in p['estado'] or p['orden'] == 4])


if __name__ == '__main__':
    main()
