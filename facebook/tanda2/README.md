# Facebook · tanda 2 (lo aprendido en X, llevado al feed)

Los 21 posts de educación de la tanda 2 de X (`posts/tanda2/`), adaptados al feed de la página. Se armaron el 3-nov-2026.

## Qué se trasladó de X y por qué

| En X aprendimos (ver `aprendizajes/X-2026-11-03.md`) | En Facebook queda así |
|---|---|
| La fórmula del IMSS: niega la creencia, da el número, muestra el mecanismo, culpa al sistema y deja una sola salida | Mismos textos, sin recortar: Facebook no limita a 280 caracteres |
| La tarjeta tachada trae guardados | Misma tarjeta, ahora **4:5 (1080×1350)**, el formato que más espacio ocupa en el feed de Facebook |
| Los textos personales («Todo es mi culpa») traen visitas al perfil | Se alternan tarjeta, texto corto y texto largo |
| Una idea por post, con espacio | **Uno al día a las 9:00**, fuera de los Reels de 12:30 y 19:30 |
| La meta es seguidores, no vistas baratas | Cada post cierra con «Escribo de admisiones todos los días. Si tienes un colegio, sigue la página.» |
| Educación a fondo, cero política | Ninguno de los 21 toca política |

Además se cambiaron la bio de la página («Ingeniero. Escribo de admisiones en colegios privados con los datos de 102 Rayos X: lo que el sistema produce y nadie quiere ver.») y la categoría, de «Personal blog» a **Educational Consultant + Education**.

## Calendario

Del 4 al 24 de noviembre, uno diario a las 9:00. El orden abre con la tarjeta del 46 % (la fórmula que más funcionó), deja «22 de febrero de 2022» el 11-nov para que «1,723 días» siga siendo cierto, y cierra el 24-nov con la invitación al Rayos X (liga con `utm_source=facebook`).

| Archivo | Qué es |
|---|---|
| `hacer_fb.py` | Genera `fb_tanda2.json` (texto, fecha, hora, estado) y las tarjetas 4:5 de `tarjetas/` |
| `fb_tanda2.json` | Los 21 posts; `estado` dice cuáles ya están programados en Business Suite |
| `tarjetas/` | Las 7 tarjetas tachadas en 1080×1350 |

## Cómo se programan

En Meta Business Suite (composer), con los helpers de BrowserOS neo `fbFeedA` (abre el composer, desmarca Instagram, sube la tarjeta, escribe el texto) y `fbFeedB` (pone la fecha con el calendario, la hora en los spinbuttons, y confirma «Your post is scheduled»). Los datos se sirven desde una página local con `window.__F`.

Suave con Meta: se programan 7 por día, uno por uno. El 3-nov quedaron los 7 primeros (4 al 10 de noviembre).
