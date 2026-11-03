# YouTube · publicaciones de comunidad (3–20 nov 2026)

**Ver en vivo:** [youtube.com/@RicardoLopezReyero/posts](https://www.youtube.com/@RicardoLopezReyero/posts)

El 3-nov-2026 Ricardo pidió llevar a YouTube lo aprendido en X, solo en las publicaciones de texto o imagen (los videos y Shorts no se tocan), hechas para YouTube.

> **Regla (3-nov-2026):** nada de CIMEDU ni de ningún congreso o evento generalista de admisiones: ni texto, ni hashtag, ni liga, ni horario pensado para el evento. Ricardo habla desde sus datos, no desde la agenda de otros.

## Qué cambió

Había 18 publicaciones de imagen programadas del 3 al 20 de noviembre a las 9:00, con frases suaves («El seguimiento también es una forma de decirle a una familia: aquí nos importas»). Se sustituyeron por 18 publicaciones nuevas, en las mismas fechas:

- **Fórmula del IMSS** (niega la creencia, da el número, muestra el mecanismo, culpa al sistema, deja una salida) y tarjeta tachada.
- **Tarjeta cuadrada 1080×1080** en la paleta de SuperLeads (navy, verde, Plus Jakarta Sans), nombre de Ricardo arriba y logo de SuperLeads abajo. Tres plantillas: tachado, lista y cita.
- **Texto completo** con la fuente escrita, una pregunta al final para los comentarios, invitación a suscribirse y hashtags.
- Todas salen a las **9:00**. Una primera versión del 4 al 7-nov se montó en un congreso del sector; el mismo 3-nov se quitó de las cuatro (texto y hora) por la regla de arriba.
- El 11-nov va «22 de febrero de 2022» para que «1,723 días» sea cierto ese día. El 20-nov cierra con la invitación al Rayos X (liga con `utm_source=youtube`).

**Nada se borró.** Studio no deja cambiar la imagen de una publicación ya programada, así que las nuevas se crearon desde el compositor del canal y las 18 viejas se movieron, en el mismo orden y a la misma hora, del **21 de noviembre al 8 de diciembre** (`publicaciones_viejas_movidas.json` guarda su texto, fecha anterior y fecha nueva).

## Archivos

| Archivo | Qué es |
|---|---|
| `hacer_youtube.py` | Fuente de verdad: fecha, hora, tarjeta y texto de las 18; genera `publicaciones_youtube.json` y `tarjetas/` |
| `publicaciones_youtube.json` | Las 18 nuevas, con estado |
| `publicaciones_viejas_movidas.json` | Las 18 anteriores: id de Studio, texto, fecha original y fecha nueva |
| `ids_studio.json` | Id de Studio de cada publicación vieja por fecha original |
| `tarjetas/` | Las 18 tarjetas 1080×1080 |

## Cómo se programan (BrowserOS neo)

- **Nueva:** `ytPostA(browser, page, I)` abre `youtube.com/channel/<id>/posts`, «Añadir una imagen» → «selecciónalas desde tu ordenador» (parche de `HTMLInputElement.click` + `DOM.setFileInputFiles`), escribe el texto; `ytPostB` abre «Menú de acciones» → «Programar publicación», escribe la fecha («Nov 5, 2026»), elige la hora en la lista (ojo: «AM/PM» trae un espacio angosto ` `) y pulsa «Programar». **Nunca «Publicar»**: publica en ese momento.
- **Mover una vieja:** `studioMoverPost(browser, page, postId, '21 nov 2026')` en `studio.youtube.com/post/<id>/edit` → «Editar estado de visibilidad» → fecha → «Hecho» → «Guardar» («Cambios guardados»).
