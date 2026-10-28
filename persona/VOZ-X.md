# Cómo escribe Ricardo en X

Guía operativa para producir posts a escala (la meta es ~10,000 posts al año) sin que dejen de sonar a él. Antes de esto, leer [ESENCIA.md](ESENCIA.md).

## La fuente es el artículo, no la ocurrencia

Cada post nace de uno de sus artículos ([articulos/](../articulos/)). El artículo ya tiene la tesis, la cuenta y la frase; el post la condensa y manda al lector al artículo completo publicado en X. Un artículo da para 5 a 20 posts distintos (una tesis, una cifra, una escena, una frase, una pregunta, un contraste, una lista). Así se llega a miles sin inventar nada.

## Anatomía de un post que sí suena a él

1. **Primera línea = golpe.** La conclusión o la cifra, nunca el contexto. «Política 100 % vivos.» «Todo es mi culpa.» «El IMSS no está quebrado.»
2. **Dos a cuatro párrafos cortos** con el porqué: una idea, un número, una conclusión. Renglón en blanco entre párrafos. La cuenta completa se queda en el artículo; si el post necesita que el lector haga la cuenta, está mal (el IMSS de la primera versión «estaba sumamente complejo»).
3. **El giro de sistema:** «no es la persona, es el filtro», «no es el piso, es la arquitectura».
4. **Cierre con pregunta que el lector se hace en voz alta, o con una frase de una línea.** «¿Prefieres la ilusión de igualdad o un gobierno alineado con quien lo paga?» «Un bulto pesa.»
5. **Última línea fija:** `Lo escribí completo aquí: https://x.com/ricardolopezrey/status/<id>` (los ids están en [posts/publicados_x.json](../posts/publicados_x.json)).

Largo que ha funcionado: 350 a 600 caracteres con la liga (la cuenta tiene posts largos). Los de SuperLeads de 200 caracteres con dato y n no jalaron en X; los personales y contundentes, sí.

## Lo que lo hace controversial sin volverlo tóxico

- Dice lo que nadie quiere decir y lo sostiene con una cuenta o con una propuesta concreta. La provocación sin propuesta no es él.
- Los golpes van al sistema, al proceso o al rol («la presidenta», «el SAT», «los bancos»), y cuando van a una persona, siempre sigue «no es culpa de ella, es el filtro». Fuerte sí; insulto no («estúpida» se queda en el artículo, no en el post).
- Nombra y etiqueta a figuras públicas sin miedo (Sheinbaum, Salinas Pliego, Lilly Téllez, Loret) y les hace una pregunta directa. Nunca a particulares.
- Las propuestas se imaginan: «imagina una ley que…», «propongo», «¿y si…?». Nunca «mi ley».
- Nunca insulta a un lector, a un maestro, a un trabajador. Puede llamar «bulto de cemento» a un socio porque es una categoría, no un nombre.
- Habla de sus errores y de su proceso con naturalidad (las 300 videollamadas, los 39 años sin escribir): eso le da permiso para ser duro con lo demás. No habla de su esposa ni de su hija en los posts, ni de en qué percentil de ingreso está.

## Etiquetas (@)

Solo cuentas reales y verificadas a mano antes de usarlas (el 28-oct-2026 @SHCP_mx resultó parodia). Las que ya se usaron y son correctas: @Claudiashein, @Tu_IMSS, @SATMX, @SSPCMexico, @INEMexico, @mrikelme (alcalde de Torreón), @manolojim (gobernador de Coahuila), @elonmusk, @X, @GobiernoMX, @RicardoBSalinas, @LillyTellez, @CarlosLoret. Normalmente una etiqueta por post, al final, con una pregunta directa; varias cuando el post es una pregunta a un grupo (como el de nivel de conciencia). Nunca etiquetar a particulares.

## Visuales

Un post de cada tres va sin imagen. Cuando lleva, tiene que explicar algo que el texto no dice solo:

- **Foto o gráfico del propio artículo** cuando existe (la tabla de PIB, la avenida con árboles, el semáforo, su escritorio). Es lo que más suena a él.
- **Tarjeta** 1600×900: fondo negro #0D0D0D, texto blanco #F5F5F0, acento amarillo #FFC72C, Avenir Next, barra corta de acento arriba, etiqueta en mayúsculas, firma «Ing. Ricardo López Reyero · Torreón» y «@ricardolopezrey». Sin logo de SuperLeads. Nunca caras ajenas.
- **GIF** 1200×675 para contadores (1,171 días, 300 videollamadas), listas que se desvanecen (60 impuestos → 1), o pantallas que cambian (toma de protesta). Último cuadro largo (2.5–3 s) con el mensaje final.

El código que los genera está en [posts/hacer_visuales.py](../posts/hacer_visuales.py) y [posts/hacer_visuales_2.py](../posts/hacer_visuales_2.py).

## Proceso para una tanda nueva

1. Elegir artículos (o ángulos nuevos de artículos ya usados) y anotar la tesis en una línea.
2. Escribir el post con la anatomía de arriba. Leerlo en voz alta: ¿suena a un ingeniero de Torreón que ya hizo la cuenta y no pide permiso? Si suena a opinólogo o a consultor, reescribir.
3. Verificar cada cifra contra el artículo. No inventar números nuevos; si el artículo no lo trae, el post tampoco.
4. Decidir visual (ninguno / del artículo / tarjeta / GIF) y variar entre posts seguidos.
5. Verificar etiquetas en x.com antes de usarlas.
6. Guardar en [posts/posts.json](../posts/posts.json) con orden, artículo, formato, texto, liga, visual y estado.
7. Ricardo revisa. Nada se publica ni se programa sin su visto bueno. Las fechas las decide él.

## Cadencia (desde el 28-oct-2026)

Ricardo pidió intensidad: «más intenso de lo que yo lo haría». Quedó en 3 posts al día, 8:00, 13:30 y 20:30 hora de Torreón (mañana, comida y noche, los tres picos de lectura en México), sin descansar fines de semana. Los 33 primeros salen del jue 29-oct al dom 8-nov-2026. El orden alterna política / negocio / vida, abre con lo más personal (1,171 días; 88 artículos 0 % IA) y reparte los GIF uno por día como máximo. La siguiente tanda se prepara antes de que termine la anterior para que el perfil nunca tenga un día vacío.

## Lo aprendido operando X (28-oct-2026)

- Publicar borradores o artículos por API dispara el error 226 («parece automatizado»): todo se crea desde el editor de X. No se evade.
- Un post programado no admite comentario (hilo) hasta que sale; por eso la liga va dentro del texto.
- Para pausar programados: abrir el post → Schedule post → Clear → cerrar → Save. Quedan en Borradores sin fecha.
- Las menciones abren un menú de sugerencias que se come el Enter; cerrar el menú antes de seguir.
- Un artículo publicado en X crea un post en el perfil; el id de ese post es la liga que usamos.
- Programar 33 posts desde el editor toma ~15 s por post con los helpers de BrowserOS (escribirPost, ponerMedia, programarPost). Al reabrir un borrador viejo hay que esperar a que cargue su texto antes de borrarlo, si no el texto nuevo se pega encima del viejo.
- Etiquetas que resultaron parodia o inexistentes: @SHCP_mx (parodia), @Buen_GobiernoMX y @TorreonGob (no existen). Reales y verificadas: @OHarfuch, @SRE_mx, @CFEmx, @STPS_mx, @SEP_mx, @Mx_Diputados, @AnthropicAI, @OpenAI.
