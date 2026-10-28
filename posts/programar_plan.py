"""Calendario de los 33 (3 al día: 8:00, 13:30, 20:30 Torreón, del 29-oct al 8-nov-2026) y etiquetas nuevas.
Deja en posts.json: cuando (ISO local), slot y texto_x final."""
import json, os, datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
HORAS = [(8, 0), (13, 30), (20, 30)]
INICIO = datetime.date(2026, 10, 29)
# orden de salida: abre fuerte, alterna política / negocio / vida, GIFs repartidos
SECUENCIA = [1, 33, 2, 3, 30, 11, 5, 31, 12, 14, 4, 6, 15, 27, 10, 7, 29, 16, 8, 32, 13, 9, 28, 17, 23, 26, 18, 24, 25, 19, 22, 20, 21]
# etiquetas verificadas en x.com el 28-oct-2026 (cuenta real, seguidores) que se agregan al final del texto
ETIQUETAS = {
    10: "@Claudiashein, con todo el poder, ¿qué cambia en 2026?",
    12: "@OHarfuch, ¿cuántos muertos son aceptables? Yo digo cero.",
    18: "@Mx_Diputados, ¿se animan a resumirla en 2 hojas?",
    20: "@SRE_mx, ¿alguien ya pensó el año 5?",
    22: "@CFEmx, ¿cuántos kWh por mexicano este año?",
    25: "@STPS_mx, ¿cuánto cuesta no hacerlo?",
    26: "@SEP_mx, ¿cuántos colegios privados cerraron este año por falta de crédito?",
    32: "Gracias, @AnthropicAI y @OpenAI.",
}
DIAS = ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom']


def main():
    posts = json.load(open(os.path.join(AQUI, 'posts.json')))
    por = {p['orden']: p for p in posts}
    assert sorted(SECUENCIA) == list(range(1, 34))
    for i, orden in enumerate(SECUENCIA):
        dia = INICIO + datetime.timedelta(days=i // 3)
        h, m = HORAS[i % 3]
        p = por[orden]
        p['slot'] = i + 1
        p['cuando'] = f'{dia.isoformat()}T{h:02d}:{m:02d}'
        p['cuando_texto'] = f'{DIAS[dia.weekday()]} {dia.day} {["ene","feb","mar","abr","may","jun","jul","ago","sep","oct","nov","dic"][dia.month-1]} · {h:02d}:{m:02d}'
        if orden in ETIQUETAS and ETIQUETAS[orden] not in p['texto']:
            if orden == 32:
                p['texto'] = p['texto'].replace('Gracias a todos los humanos que la construyeron.', 'Gracias a todos los humanos que la construyeron. ' + ETIQUETAS[orden])
            else:
                p['texto'] = p['texto'] + '\n\n' + ETIQUETAS[orden]
        p['texto_x'] = p['texto'] + '\n\nLo escribí completo aquí: ' + p['liga']
    posts.sort(key=lambda p: p['slot'])
    json.dump(posts, open(os.path.join(AQUI, 'posts.json'), 'w'), ensure_ascii=False, indent=1)
    for p in posts:
        print(f"{p['slot']:02d} {p['cuando']} post {p['orden']:02d} {p['formato']:6s} {len(p['texto_x'])} {p['titulo'][:40]}")


if __name__ == '__main__':
    main()
