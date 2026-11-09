# Artículo · Hay más familias queriendo inscribirse en tu colegio de las que tu proceso alcanza a inscribir (9-nov-2026)

**Ver en vivo:** [X](https://x.com/ricardolopezrey/status/2119912581720658195) · [LinkedIn](https://www.linkedin.com/pulse/hay-m%C3%A1s-familias-queriendo-inscribirse-en-tu-colegio-de-l%C3%B3pez-reyero-promc/)

**Estado: PUBLICADO el 9-nov-2026 en X y en LinkedIn.** Ricardo pidió un artículo en X con su presentación y el video, con la idea central de que en América Latina, y más en México, hay más familias queriendo estudiar en la educación privada de las que los procesos de inscripción alcanzan a captar. Luego pidió lo mismo en LinkedIn.

- **Texto:** `armar.py` es la fuente de verdad: unas 1,000 palabras, 8 subtítulos y 14 láminas. Genera `articulo.md` para leer y `publicar.json` con los segmentos.
- **Láminas:** salen del PDF «CIMEDU 9 · SuperLeads · presentación · v1 · 2026-11-09 15h47», renderizadas a 2400 px en `imagenes/`. Son la 03, 04, 05, 07, 09, 10, 17, 18, 20, 22, 23, 25, 28 y 30.
- **Portadas:** se armaron con la lámina 1. La de X es 5:2 y la de LinkedIn 16:9. Se borró el botón «Pantalla completa» y el bloque «Presenta · RICARDO LOPÉZ REYERO», porque el PDF trae el apellido mal acentuado (**LOPÉZ**). **Hay que corregirlo en la presentación.**
- **Video:** en X va nativo, subido dentro del artículo, después del párrafo que lo presenta. En LinkedIn va como liga a YouTube (youtu.be/op95KKuYzms).

## Decisiones

- **CIMEDU:** no se nombra. El texto dice «la charla que di hace unos días frente a dueños y directores de colegios». No se usaron las láminas 32 y 33, que traen cimedu9.superleads.mx ([[feedback_nada_de_cimedu]]).
- **Cifras con fuente:** todas las cifras salen de las láminas y llevan su fuente al final:
  - Banco Mundial y UNESCO;
  - AMAI;
  - APEIM;
  - corte Rayos X de octubre de 2026;
  - UPCEA 2025.
- **Chile:** en el video Ricardo dice 73 %, pero la lámina y `cimedu9/DATOS.md` dicen 63 %. Va 63 %.
- **«Quieren» contra «pueden»:** el 35 % es de hogares que *pueden* pagar. Que *quieren* lo prueban las familias que escriben y no reciben respuesta: el 44 % sin respuesta y la conversión de 2.4 de cada 100.
- **Sin casos de clientes:** no va la lámina 29, porque Sanford, Pereyra y Tampico siguen marcados «confirmar».
- **Cierre:** «Lunes 9 de noviembre de 2026, 3:55 pm · Torreón, Coahuila, México · 22°.» y la firma con ricardo@superleads.mx, como en los artículos anteriores.

## Texto del feed de LinkedIn

```
Hay más familias queriendo inscribirse en tu colegio de las que tu proceso alcanza a inscribir.

En México, el 35 % de los hogares puede pagar un colegio privado y solo el 10 % de los alumnos está en uno. La institución mediana opera al 46 % de su capacidad y, de cada 100 familias que escriben, se inscriben 2.4.

El problema no es la demanda. Es el proceso.

Escribí este artículo con las láminas de mi charla y el video completo.
```

## Cómo se publicó (helpers nuevos con `evaluateInPage`)

- **X:** primero «create» en x.com/compose/articles. Luego, igual que `xArtInicio`, el título con clic real y la portada con Apply. Después `xArtCuerpo2` por tramos de 6 a 9 segmentos.
  - El video se pega como archivo con el cursor al final del párrafo; queda abajo de ese párrafo.
  - Para publicar se usa `publicarArticulo`, que sigue sirviendo.
- **LinkedIn:** `liArtInicio2` pone título y portada, `liArtCuerpo2` arma el cuerpo por tramos de 10 y `liArtPublicar2` hace «Siguiente», escribe el texto del feed y publica.
- **Datos:** salen de `datos.html`, que se sirve con `python3 -m http.server 8769` en esta carpeta. No se sube al repo.
