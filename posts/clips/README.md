# Clips de YouTube para X

Prueba del 28-oct-2026 con el video «CRM para escuelas vs Excel: 1.2 millones de impresiones, 3 inscritos» (WFCeQA_GgQY), tramo 1:39–2:15 (36 s).

Formato: vertical 1080×1920. Arriba el gancho fijo («1.2 millones de impresiones. 3 inscritos.»), en medio la lámina de la presentación recortada, abajo la cámara de Ricardo en círculo con aro amarillo y subtítulos grandes por trozos (palabras clave en amarillo), y el @ al pie. Sin liga externa: el video va nativo en X.

Cómo se hizo (`hacer_clip.py`): `yt-dlp` baja el video y los subtítulos automáticos con tiempo por palabra; cada trozo de subtítulo es un PNG (Avenir Next Heavy) que ffmpeg sobrepone con `enable=between(t,a,b)`; la lámina y la cámara se recortan del cuadro original (la cámara es un círculo de 296 px, por eso se ve suave al crecer). Render: ~40 s por clip.

Para otro video solo cambian: id, tramo (INI/FIN), geometría si la cámara está en otro lugar, gancho y palabras de énfasis.
