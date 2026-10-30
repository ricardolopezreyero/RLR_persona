# Serie «Datos» · estadísticas para YouTube Shorts

Un gráfico y un texto por pieza. Las cifras salen, sin pintura, de los tres documentos de mercado de SuperLeads (julio 2026) y cada pieza conserva su fuente original en pantalla y en la descripción. Diseño: guía de estilos SuperLeads (Plus Jakarta Sans, navy profundo, verde solo sobre oscuro, gráficas con la paleta `--chart-*`, texto siempre en tinta).

**Estado: hechas, sin publicar.** Ricardo revisa y decide fechas.

| Serie | Documento | Piezas |
|---|---|---|
| 1 · La realidad de la educación pública en México | P1-01 | 01–11 |
| 2 · La boleta invisible: cómo eligen colegio las familias | P1-02 | 12–21 |
| 3 · Análisis de la educación privada en Latinoamérica | P1-03 | 22–26 |

## Qué hay aquí

| Archivo | Qué es |
|---|---|
| [serie.py](serie.py) | **La fuente de verdad.** Datos, fuente, gráfico elegido, título, descripción y hashtags de cada pieza. Si algo cambia, cambia aquí y se vuelve a renderizar. |
| [render.py](render.py) | Plantilla HTML + SVG por pieza → Chrome sin cabeza por CDP → PNG (cuadro final) y MP4 de 8 s a 30 fps (las barras crecen, los números cuentan). |
| [entregar.py](entregar.py) | Escribe `indice.json`, `SHORTS_datos_textos.md` y `hoja.jpg`. |
| [salida/](salida/) | Los PNG 1080×1920 y los MP4, nombrados `Dato NN · título · versión · fecha hora`. |
| [html/](html/) | El HTML de cada pieza (se puede abrir en el navegador y llamar `anim(t)` en consola). |
| [SHORTS_datos_textos.md](SHORTS_datos_textos.md) | Título, descripción y hashtags de las 26, listos para pegar en Studio. |
| [hoja.jpg](hoja.jpg) | Hoja de contacto con las 26 piezas. |

## Tipos de gráfico (uno por idea, el que mejor transmite el dato)

`barras` (comparaciones y rankings) · `pares` (dos series por grupo, PISA) · `waffle` (de cada 100 / de cada 10) · `dona` y `donas` (porcentajes solos) · `tiempo` (cronologías y etapas) · `franjas` (24 horas: cuándo investiga la familia vs. cuándo atiende el colegio) · `estrellas` (la escala de reseñas) · `embudo` (40 consultas, dos procesos) · `tarjetas` (México vs. Perú) · `piramide` (niveles socioeconómicos) · `stats` (fila de cifras de apoyo).

## Reglas de la serie

1. Nada se inventa: si el documento trae un rango («~170–190»), la pieza trae el rango. Los modelos ilustrativos (valor de vida, 40 consultas) se declaran como tales en la nota.
2. La fuente va en la pieza (nota al pie) y en la descripción. Metodología completa a solicitud: hola@superleads.mx.
3. Zona segura de Shorts: el contenido termina antes de y = 1600 (`render.py` avisa si se pasa); el tercio inferior queda para el título que pone YouTube.
4. Sin caras ni firmas de personas: lo que se comparte es la información.
5. La descripción cierra con el Rayos X («tiene costo; por ahora lo damos sin costo») y el bloque de autor.

## Cómo regenerar

```bash
cd ~/Code/RLR_persona/posts/estadisticas
python3 serie.py            # valida datos y largos
python3 render.py           # todas (o: python3 render.py 3 12 → solo esas; SOLO_PNG=1 para saltar el video)
python3 entregar.py         # índice, textos y hoja
```

Requiere Google Chrome, ffmpeg, Pillow y `websocket-client` (`pip3 install --user websocket-client`).
