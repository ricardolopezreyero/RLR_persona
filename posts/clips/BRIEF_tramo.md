# Brief: elegir el tramo de un video para un Short de YouTube

Trabajas sobre UNA carpeta `v/<id>/` que contiene:
- `transcripcion.txt`: transcripción automática de YouTube, una línea cada ~12 s con el minuto:segundo de inicio (mm:ss).
- `palabras.json`: lista `[[segundos, palabra], ...]` con el tiempo exacto de cada palabra (misma transcripción).

El autor es el Ing. Ricardo López Reyero (SuperLeads, admisiones para colegios y universidades privados). Habla de tú a tú con directores y dueños de colegios. El Short debe tener gancho desde el primer segundo y cerrar con una idea completa.

## Qué elegir
1. **Un solo tramo continuo de 25 a 50 segundos** (nunca más de 58 s). Debe:
   - Empezar en una afirmación fuerte o un dato concreto (no en «entonces», «bueno», «aquí», ni a media frase).
   - Ser autocontenido: quien no vio el video lo entiende completo.
   - Terminar en una conclusión o remate, no en una enumeración a medias.
   - Preferir datos, contrastes y frases que incomoden («las métricas de vanidad no llenan aulas»), evitando tramos donde vende SuperLeads o presenta el índice del video.
   - Evitar tramos donde Ricardo titubea mucho o repite («este… este…»); la transcripción automática lo delata.
2. `ini` y `fin` deben ser tiempos exactos tomados de `palabras.json`: `ini` = tiempo de la primera palabra menos 0.25 s; `fin` = tiempo de la última palabra + 0.9 s (o el tiempo de la palabra siguiente si está más cerca).
3. **Gancho** (texto fijo arriba del video): 2 o 3 renglones muy cortos (máximo 18 caracteres por renglón), con el dato o la afirmación. El último renglón es el remate y se pinta de verde. Ejemplo: `["1.2 millones", "de impresiones.", "3 inscritos."]`. Sin signos de exclamación, sin mayúsculas sostenidas.
4. **Subtítulos corregidos**: toma las palabras del tramo desde `palabras.json` y entrégalas agrupadas en trozos de 2 a 5 palabras (una idea o respiración por trozo), con el texto CORREGIDO: ortografía, acentos, puntuación, números como cifras («1.2 millones», «34 %»), y nombres propios bien escritos. No cambies lo que dice ni lo resumas: solo corrige. Si la transcripción automática inventó una palabra claramente errónea, pon la correcta según el contexto. Quita muletillas sueltas («este», «eh», «o sea» repetido) cuando se puedan quitar sin dejar hueco raro; si las quitas, el trozo cubre igual ese tiempo.
   - Cada trozo: `{"ini": <seg de su primera palabra>, "fin": <seg de la primera palabra del siguiente trozo, o fin del tramo>, "texto": "..."}`.
   - Marca en `enfasis` de 4 a 8 palabras o cifras del tramo que deban ir en verde (las que cargan el golpe: cifras, «no», «vanidad», «inscritos»...). Tal cual aparecen en los trozos.
5. `frase`: la idea del tramo en una línea, para el título del Short (máximo 60 caracteres, sin mayúsculas sostenidas).
6. `descripcion`: 2 renglones para la descripción del Short + 3 hashtags (#Admisiones #ColegiosPrivados y uno del tema).
7. `cuadros`: 2 tiempos (segundos) dentro del tramo donde la pantalla compartida muestre algo que valga la pena ver (lámina, gráfica, cifra).

## Entrega
Escribe `v/<id>/seleccion.json` con exactamente estas llaves:
```json
{"id": "...", "ini": 98.9, "fin": 134.7, "gancho": ["...", "...", "..."], "enfasis": ["...", "..."],
 "trozos": [{"ini": 99.0, "fin": 101.8, "texto": "Las métricas de vanidad"}, ...],
 "frase": "...", "descripcion": "...", "cuadros": [110, 125], "por_que": "una línea de por qué este tramo"}
```
Antes de escribirlo, verifica: que `ini` < primer trozo, que los trozos sean continuos (fin de uno = ini del siguiente), que el último `fin` ≤ `fin` del tramo, que la duración esté entre 25 y 58 s, y que el texto unido de los trozos se lea como español correcto en voz alta. Reporta en tu respuesta final solo: id, duración, gancho, frase y por qué.
