# Clips de YouTube para X

Prueba del 28-oct-2026 con el video «CRM para escuelas vs Excel: 1.2 millones de impresiones, 3 inscritos» (WFCeQA_GgQY), tramo 1:39–2:15 (36 s).

Formato: vertical 1080×1920. Arriba el gancho fijo («1.2 millones de impresiones. 3 inscritos.»), en medio la lámina de la presentación recortada, abajo la cámara de Ricardo en círculo con aro amarillo y subtítulos grandes por trozos (palabras clave en amarillo), y el @ al pie. Sin liga externa: el video va nativo en X.

Cómo se hizo (`hacer_clip.py`): `yt-dlp` baja el video y los subtítulos automáticos con tiempo por palabra; cada trozo de subtítulo es un PNG (Avenir Next Heavy) que ffmpeg sobrepone con `enable=between(t,a,b)`; la lámina y la cámara se recortan del cuadro original (la cámara es un círculo de 296 px, por eso se ve suave al crecer). Render: ~40 s por clip.

Para otro video solo cambian: id, tramo (INI/FIN), geometría si la cámara está en otro lugar, gancho y palabras de énfasis.

## Shorts de YouTube (28-oct-2026, v1)

Cinco Shorts con el sistema de diseño de SuperLeads (navy profundo `#001240`, verde `#56EF9F`, Plus Jakarta Sans, logo blanco), hechos con `hacer_short.py`:
`palabras.py` saca el tiempo por palabra del VTT automático; un agente por video elige el tramo, el gancho y corrige los subtítulos siguiendo `BRIEF_tramo.md` (resultado en `selecciones/<id>.json`); `hacer_short.py` recorta contenido y cámara (geometría por video en `CONFIG`, fuente 1668×1080) y sobrepone gancho, subtítulos y pie; `entregar.py` nombra los archivos y escribe la guía de publicación (título, descripción, hashtags, tramo). Entrega en `~/Desktop/HTML/RLR_marca_personal/Shorts` y `~/Downloads`.

| # | Video | Tramo | Gancho |
|---|---|---|---|
| 1 | ZP5BSoRFaio · no necesita más publicidad | 2:00–2:46 | El problema no es la publicidad. Es el seguimiento. |
| 2 | 0tRgTomkaAw · 34 % puede pagar | 3:46–4:20 | 34 % puede pagar colegio privado. Solo el 10 % paga. |
| 3 | oqLweG2S0Bk · WhatsApp de noche | 22:18–22:49 | 40 consultas. 4 o 12 inscritos. 2.7 millones. |
| 4 | mDfb_nteAe8 · mapa del proceso | 19:52–20:31 | ¿El alumno o el profesor? Primero admisiones |
| 5 | aZggkBKgqrg · monetizar sin subir colegiatura | 17:08–17:55 | Un teatro de 6 millones. Se pagó en 1 año. |
