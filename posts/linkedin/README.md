# LinkedIn · posts (dos por semana) con las gráficas de las dos series

Un **carrusel** (PDF 1080×1350, el formato 4:5 de los documentos de LinkedIn) con 2 a 5 gráficas que cuentan una sola historia, más el **texto del post** y un **primer comentario** con fuentes y videos. Las gráficas son las mismas de las series «Rayos X» y «La realidad de la educación», re-renderizadas para LinkedIn: sin la nota al pie en la lámina, con una portada y una lámina de cierre que lleva **solo una frase de cambio de perspectiva** (Ricardo, 30-oct: «un cierre con una bonita frase elegante», sin más información).

**Estado: los 13 posts PROGRAMADOS en LinkedIn el 30-oct-2026** (son publicaciones del feed con documento, no «artículos» de LinkedIn; esos vendrán después). Pendiente a mano: pegar el `Primer comentario` de cada post el día que salga. Orden: primero las 6 entregas del corte Rayos X (5 a 26-nov-2026), luego los 7 capítulos de La realidad de la educación (3-dic-2026 a 14-ene-2027). Martes y jueves 9:00 GMT-6 cuando los Shorts de cada gráfica ya están públicos; pausa del 24-dic al 6-ene; la serie termina el 14-ene (Ricardo: «aprieta… el 15 de enero estaré terminando»).

| Archivo | Qué es |
|---|---|
| [armar.py](armar.py) | **La fuente de verdad**: los 13 artículos (gráficas, gancho, cuerpo, pregunta, cierre, hashtags), las láminas de portada y cierre, el texto del post y el plan. Reusa `render.py` en modo `linkedin` y toma las ligas de YouTube del calendario. |
| `salida/Artículo NN · slug/` | El PDF del carrusel, `laminas/` (PNG de cada lámina), `Texto del post` y `Primer comentario` (fuentes y video de cada gráfica). |
| `salida/PLAN LinkedIn · vN · fecha.md` y `plan.json` | Fechas, láminas, gráficas y caracteres de cada artículo. |

## Reglas

1. Una historia por artículo: las gráficas se agrupan por tema, no por orden de publicación en YouTube.
2. Primero una serie completa y luego la otra ([[feedback_contenido_siempre_agregar]]). Lo ya programado en otras redes no se mueve.
3. Cada gráfica lleva su video de YouTube (en el texto y en el primer comentario); `armar.py` comprueba que el Short ya esté público antes de la fecha del post.
4. Ningún número que no esté en la pieza original: los textos citan lo que dicen las gráficas (mediana, n, fuente). Montos siempre con MXN/USD.
5. Texto ≤ 3,000 caracteres (límite de LinkedIn). Las ligas externas bajan el alcance: alternativa, pegarlas en el primer comentario.
6. Marca: nombre de Ricardo arriba, SuperLeads solo logo abajo.

## Cómo regenerar

```bash
cd ~/Code/RLR_persona/posts/linkedin
python3 armar.py              # los 13 → salida/ y ~/Downloads/LinkedIn/
SOLO=3 python3 armar.py       # solo el artículo 3 (no toca el plan ni Descargas)
```

## Cómo se programaron

Helpers de BrowserOS neo en linkedin.com: `liRedactar` (abre linkedin.com/sharing/compose, escribe el texto en el editor TipTap línea por línea, abre «Documento», intercepta el input de archivo parcheando `HTMLInputElement.prototype.click`, carga el PDF por CDP `DOM.setFileInputFiles`, pone el título ≤58 y pulsa «Hecho» esperando a que el modal cierre) y `liProgramar` (reloj «Programadas (n)», fecha dd/mm/aaaa, hora, cierra la lista de horas pulsando el título del modal —nunca Escape: abre «guardar borrador»—, comprueba el resumen «Publicando el …», Confirmar y Programar). Datos para los helpers: `datos_li.html` (file://, window.__L; en .gitignore).
