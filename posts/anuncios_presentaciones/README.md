# X Ads · campaña «Presentaciones» (9-nov-2026)

**Ver en vivo:** [el artículo que promueve](https://x.com/ricardolopezrey/status/2119912581720658195) · campaña ID 43000350 en ads.x.com/manager/18ce55ra3kx/campaigns

**Estado: ACTIVA desde el 9-nov-2026 con MX$50/día.** Ricardo pidió una campaña en X llamada «Presentaciones» con unos cuatro posts que lleven gente interesada al artículo «Hay más familias queriendo inscribirse en tu colegio de las que tu proceso alcanza a inscribir». Solo aplica en X.

**Presupuesto:** a la campaña de tráfico 42933062 se le bajaron MX$50/día (de MX$210 a MX$160) y esos MX$50 son los de «Presentaciones». El gasto total por día no cambia: MX$210.

## Configuración

- **Cómo se hizo:** «Copiar campaña» de la 42933062. Conserva el objetivo Tráfico web, se paga por clic en enlace con puja automática, y conserva el público «Dueños de colegio · México · español · 25+». Ese público lleva el interés Education, las palabras clave de admisiones, similares a @Mexicanos1o e @imcomx y retargeting.
- **Anuncios copiados:** los 12 que venían de la otra campaña (T2 y RX) se quitaron del borrador. La 42933062 conserva los suyos.
- **4 anuncios solo de promoción:** generados con `anuncios.py`, que escribe `anuncios.json` y las imágenes en `tarjetas/`. Cada uno lleva:
  - texto de 280 caracteres o menos, con la liga al artículo al final;
  - tarjeta tachada 1.91:1;
  - URL del sitio web, que es el artículo en x.com. La tarjeta muestra «De x.com».
- **UTM:** X pasó la liga con UTM a «Seguimiento de URL» y dejó vacía la URL del sitio web. Hubo que escribir a mano la URL del artículo sin UTM.
- **Aviso de X:** debajo de cada imagen salió «No cumple nuestros estándares estéticos». No fue un error que bloqueara: la revisión dijo «0 problemas» y la campaña se publicó.

| # | Gancho (negación) | Número | Tarjeta |
|---|---|---|---|
| PR 01 | No te faltan familias. Te falta contestarles. | 35 % puede pagar, 10 % está en privada | ~~familias.~~ → Te falta contestarles. |
| PR 02 | No se fueron por el precio. Se fueron por el silencio. | 44 % sin respuesta, 14 h | ~~precio.~~ → Se fueron por el silencio. |
| PR 03 | No es falta de esfuerzo. Es falta de sistema. | 71 % en WhatsApp o Excel, $450,000 MXN | ~~esfuerzo.~~ → Es falta de sistema. |
| PR 04 | El problema no es la demanda. Es el proceso. | 46 % de capacidad, 2.4 de 100 | ~~la demanda.~~ → Es el proceso. |

## Cómo medir

Clics en enlace y CPC por anuncio, comparados con la campaña de tráfico, que va en MX$0.96 por clic. Regla de la base mínima: si un anuncio pasa de 4,000 impresiones con CTR menor a 0.35 %, se apaga.
