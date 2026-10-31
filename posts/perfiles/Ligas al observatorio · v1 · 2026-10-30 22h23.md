<!-- RLR · Ing. Ricardo López Reyero -->
# Ligas al Observatorio SuperLeads en todo lo programado · 30-oct-2026

Ricardo pidió mencionar observatorio.superleads.mx en todos los posts programados y en los artículos donde valga la pena, para que haya tráfico de ida y vuelta. Esto es lo que se agregó (nada se quitó ni se movió de fecha).

## YouTube (Studio)
- **45 Shorts de las series** (2-nov a 16-dic): segundo párrafo de la descripción = «Dato completo, con tabla, fuente y cita lista: https://observatorio.superleads.mx/dato/<slug>/» (la página de ESE dato).
- **21 Shorts de la tanda 2 + 3 programados de antes + 5 publicados sobre admisiones** (34%, «no tiene problema de demanda», «por qué se pierden las inscripciones», «convertir interés en inscritos», «no necesita más leads»): «Más datos de la educación en México, con fuente: https://observatorio.superleads.mx» (al 34% y a «Mismas 40 consultas» les tocó su dato exacto).
- **Las 2 listas** (Rayos X y La realidad): línea antes de la firma con /rayos-x/ y /realidad/.
- **Correo:** las 45 descripciones decían «metodología a solicitud: hola@superleads.mx»; ahora ricardo@superleads.mx.
- Ojo: YouTube no hace clicables las ligas en descripciones de Shorts; la liga queda visible y copiable (el «vídeo relacionado» sigue siendo el clic).
- Sin tocar: Shorts personales (gratitud, plástico, atardeceres) y videos largos.

## X (programados)
- **45 posts de las series** (17:30, 2-nov a 16-dic): antes de la línea «Serie «…»» va «Dato completo, con tabla, fuente y cita lista: https://observatorio.superleads.mx/dato/<slug>/». Misma fecha, mismo video (verificado en la respuesta de X: texto igual, 1 media).
- **Post de opinión «Crédito productivo para colegios»** (6-nov 13:30): «Más datos de la educación en México, con fuente: https://observatorio.superleads.mx».
- **Los otros 26 posts de opinión** (impuestos, política, libros, ciudad…) se dejaron sin liga: no hablan de educación y la liga les restaría alcance.

## LinkedIn
- **13 posts programados** (5-nov a 14-ene): línea antes del cierre «Todos los datos de la serie, con tabla, fuente y cita lista: https://observatorio.superleads.mx/rayos-x/» (o /realidad/). LinkedIn la acorta a lnkd.in al guardar.
- **Correo:** los 7 de La realidad decían hola@superleads.mx en el cierre; ahora ricardo@superleads.mx.
- **Primer comentario** (se pega a mano el día de cada post): nueva versión v2 en `linkedin/salida/Artículo NN · …/Primer comentario · fuentes, videos y observatorio · v2 · …txt` (+ copia en ~/Downloads/LinkedIn): cada gráfica trae «Dato completo, tabla y cita: <liga del dato>» y al final la liga de la serie. Usar la v2, no la v1.

## Artículos publicados (LinkedIn y X)
- Los 3 artículos llevan, antes de la fecha y la firma, el párrafo «Todos los datos de este artículo, cada uno con su tabla, su fuente y su cita lista, están en el Observatorio SuperLeads: …» (art. 1 → /rayos-x/, art. 2 → /realidad/, art. 3 → home).
- **X:** editar un artículo lo despublica un momento; se volvió a publicar cada uno y conservan su status (2116226266504262059, 2116226732881596903, 2116228044574675363), sus interacciones y el art. 3 sigue fijado.
- **LinkedIn:** «Actualizar» a veces no sube el cambio a la primera; se dio dos veces y se verificó en la página pública.

## Fuentes corregidas en el repo
hola@ → ricardo@ en `estadisticas/serie.py` (DOCS), `rayosx_corte/piezas.py`, calendario JSON, índices y textos SHORTS, y en `linkedin/armar.py` (CTA_R). `linkedin/armar.py` además arma el primer comentario con la liga de cada dato (`OBS`, `slug_obs`).

## Helpers de BrowserOS neo nuevos
- studio.youtube.com: `ligaObservatorio` (inserta una línea como 2.º párrafo si la descripción no la tiene), `correoShort` (hola@ → ricardo@).
- x.com: `lineaObservatorioX` (abre el programado, inserta la línea antes de «Serie «», guarda sin mover fecha; baja la lista para los de diciembre), `xArtLineaObs` (Edit Article → Confirm → inserta antes de la firma; luego `publicarArticulo` con el id de edición).
- linkedin.com: `liLineaObservatorio` (Programadas → n-ésimo → inserta antes del cierre; marca por frase porque LinkedIn acorta la liga), `liArtLinea` (artículo: inserta antes de la firma y «Actualizar»).
