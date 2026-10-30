# Tres artículos de LinkedIn (formato «artículo», no post)

Escritos en primera persona por Ricardo para que se puedan citar: 1) cómo está el mercado educativo privado en México según el corte Rayos X de octubre de 2026; 2) la educación pública en México con las cifras oficiales e internacionales que todavía existen; 3) la gran oportunidad y la responsabilidad de los dueños de colegios (los dos anteriores digeridos, con la mención suave de SuperLeads al final).

**Estado: escritos y armados, sin publicar.** Ricardo los revisa en `~/Downloads/LinkedIn Artículos/`.

| Archivo | Qué es |
|---|---|
| [armar.py](armar.py) | **La fuente de verdad**: el texto completo de los tres artículos (bloques: párrafos, subtítulos, listas y figuras) y la lámina de artículo. Reusa los datos de `posts/estadisticas/serie.py` y `posts/rayosx_corte/piezas.py`; ningún número sale de otro lado. |
| `salida/Artículo N · slug/` | `.md` (texto con las imágenes en su lugar), `.txt` (texto con marcas `[IMAGEN NN]` para pegar en el editor de LinkedIn) e `imagenes/` (gráficas 1600×900). |
| `salida/GUÍA tres artículos · …md` | Palabras y figuras por artículo y cómo armarlo en LinkedIn. |

## Formato de las gráficas para artículo

Lienzo horizontal 1600×900 (se ve completo en el cuerpo del artículo de LinkedIn). **Título arriba del gráfico** (eyebrow + titular), el gráfico centrado y escalado para caber, la fuente en letra pequeña y, **abajo, el nombre de Ricardo a la izquierda y el logo de SuperLeads a la derecha** (Ricardo, 30-oct: «cambia la dinámica… el título en la parte de arriba del gráfico; mi logotipo y el de SuperLeads en la parte de abajo: primero mi nombre y luego el de SuperLeads a la derecha»). Sin header, sin numeración de serie.

## Reglas de los textos

1. Es Ricardo escribiendo, de tú al lector; una idea por párrafo, lenguaje llano, cada párrafo da sentido al anterior.
2. Nada se inventa: todas las cifras salen de las piezas de las series (y, por tanto, de los documentos P1-01, P1-02, P1-03 y del corte Rayos X) con su fuente; el artículo 2 y 3 cierran con la lista de fuentes.
3. SuperLeads se menciona al final, como parte del artículo, nunca como anuncio. La frase de Ricardo «La vida es más fácil cuando tienes tecnología, metodología, soporte y estrategia implementados en tu institución educativa» va en el artículo 3.
4. Cierre de cada artículo: `Viernes 30 de octubre de 2026, 9:24 am · Torreón, Coahuila, México · 19°.` y la firma `Ing. Ricardo López Reyero · Founder Comercial · SuperLeads · ricardo@superleads.mx` (la fecha en que se escribieron; si se publican después, se deja igual).
5. El contacto en todo lo de Ricardo es **ricardo@superleads.mx**, nunca hola@superleads.mx: «literal es para que me escriban».
6. Imágenes a 2× (3200×1800) para pantallas Retina; en las gráficas de dos bloques el script prueba fila y columna y se queda con la disposición que cabe más grande.
7. Montos siempre con MXN o USD.

## Cómo regenerar

```bash
cd ~/Code/RLR_persona/posts/articulos
python3 armar.py      # los tres → salida/ y ~/Downloads/LinkedIn Artículos/
```
