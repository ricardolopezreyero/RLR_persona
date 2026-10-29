# Brief v2: los mejores tramos de un video para Shorts premium

Trabajas sobre UNA carpeta `v/<id>/` con `transcripcion.txt` (una línea cada ~12 s, mm:ss al inicio) y `palabras.json` (`[[segundos, palabra], ...]`, tiempo exacto de cada palabra).

Autor: Ing. Ricardo López Reyero, Founder Comercial de SuperLeads (admisiones para colegios y universidades privados). Habla de tú a tú con directores y dueños de colegios. Objetivo de estos Shorts: que la gente se quede viendo porque la idea es interesante y está completa, no por volumen. Sacar la mejor versión de él: claro, directo, con datos, sin arrogancia.

## Qué entregar
Hasta **3 tramos** del video, los mejores, ordenados de mejor a peor. Si el video solo da para 1 o 2 buenos, entrega esos; si no da para ninguno (relleno, índice, venta, titubeos), entrega lista vacía y explica por qué. Prefiere tramos que:
- Empiezan en una afirmación fuerte, una pregunta que incomoda o un dato concreto (nunca en «entonces», «bueno», «aquí», ni a media frase).
- Son autocontenidos: quien no vio el video lo entiende completo.
- Terminan en un remate o conclusión (no en enumeración a medias).
- Tienen cifras, contrastes, historias de un colegio real (sin nombres propios de colegios si no son clientes públicos), o una frase que un director recordaría.
- Duran **entre 25 y 75 segundos**. No cortes una idea para cumplir un número; si la idea completa dura 70 s, va de 70. Si dura más de 90 s, busca otra o un subtramo que cierre bien.
- Evitan venta explícita de SuperLeads, índices del video, saludos, despedidas, y zonas con muchos titubeos (la transcripción automática los delata: «este… este», repeticiones).
- Dos tramos del mismo video no deben solaparse ni repetir la misma idea.

## Formato por tramo
`ini` = tiempo de la primera palabra − 0.25 s; `fin` = tiempo de la última palabra + 0.9 s (o el tiempo de la palabra siguiente si está más cerca). Tiempos exactos de `palabras.json`.

- `gancho`: 2 o 3 renglones muy cortos (máximo 18 caracteres cada uno) con el dato o la afirmación; el último renglón es el remate y va en verde. Sin signos de exclamación, sin mayúsculas sostenidas, sin promesas.
- `trozos`: las palabras del tramo agrupadas en trozos de 2 a 5 palabras (una respiración por trozo), texto CORREGIDO: ortografía, acentos, puntuación, cifras como cifras («1.2 millones», «34 %»). No cambies lo que dice ni resumas. Quita muletillas sueltas («este», «eh», «o sea» repetido) si no deja hueco raro; el trozo cubre igual ese tiempo. Cada trozo: `{"ini", "fin" (= ini del siguiente o fin del tramo), "texto"}`, continuos.
- `enfasis`: 4 a 8 palabras o cifras del tramo que van en verde, tal cual aparecen en los trozos.
- `frase`: la idea en una línea para el título del Short (≤ 60 caracteres, sin mayúsculas sostenidas).
- `descripcion`: 2 renglones + 3 hashtags (#Admisiones #ColegiosPrivados y uno del tema).
- `cara`: un segundo dentro del tramo donde Ricardo mira a cámara con gesto tranquilo (para la portada).
- `tema`: 2 o 3 palabras (p. ej. «seguimiento», «colegiatura», «referidos») para no repetir temas entre videos.
- `por_que`: una línea.

## Entrega
Escribe `v/<id>/tramos.json`:
```json
{"id": "...", "tramos": [{"ini": 98.9, "fin": 134.7, "gancho": [...], "enfasis": [...], "trozos": [...], "frase": "...", "descripcion": "...", "cara": 110, "tema": "...", "por_que": "..."}], "sin_tramos_por": null}
```
Valida con python3 -I antes de escribir: ini < primer trozo, trozos continuos, último fin ≤ fin, duración 25–90 s, texto unido legible en voz alta. En tu respuesta final reporta solo: id, número de tramos, y por tramo duración + gancho + frase.
