# Corte Rayos X · la realidad de la educación privada en México, con datos propios

Serie periódica (cada ~6 meses) hecha a partir de los Rayos X de Inscripciones que SuperLeads hace en vivo con dueños y directores de instituciones privadas. Cada corte produce una tanda de gráficos verticales para YouTube Shorts, separados por nivel (colegios con primaria, con preparatoria, universidades), para que cualquier director tenga un punto de referencia: ¿estoy arriba o abajo de mis pares?

**Primer corte: 29 de octubre de 2026, 18:08** → [cortes/2026-10-29/](cortes/2026-10-29/) · 102 instituciones, 69 ciudades, 19 piezas. Estado: hechas, sin publicar.

## Reglas (no se negocian)

1. **El CSV nunca entra al repo** (trae nombres, correos y teléfonos). Vive en Descargas o en la app; aquí solo entran los agregados. `.gitignore` bloquea `*.csv`.
2. **Sin nombres.** Todo es agregado con su n. Fuera pruebas (`posible_prueba`, nombres de prueba), archivados y repetidos: una fila por institución, la más reciente.
3. **Mediana antes que promedio.** Un colegio de 7,000 alumnos mueve el promedio y miente. Se publican mediana, cuartiles y n.
4. **Montos en pesos.** Las instituciones en dólares quedan fuera de los montos (sí cuentan en lo demás).
5. **n < 5 no se publica** (ni una métrica, ni un grupo).
6. **Lo que el director cree** (causas de no inscripción, calificación de su marketing) se dice como creencia, no como medición.
7. **Es nuestra muestra, no el país:** instituciones que pidieron un diagnóstico. Se dice en cada pieza.
8. Filtros de verosimilitud por métrica (ocupación ≤ 150%, conversión ≤ 100%, colegiatura ≥ $300, etc.) en `agregar.py`.

## Niveles

| Grupo | Definición |
|---|---|
| Colegios con primaria | Ofrecen primaria y no tienen nivel superior |
| Con preparatoria | Ofrecen preparatoria y no tienen nivel superior (un colegio K-12 cuenta aquí y en primaria) |
| Universidades y posgrados | Ofrecen universidad, maestría o doctorado |
| Todas | Toda la muestra (incluye academias, en línea y otros) |

## Cómo se hace un corte nuevo

```bash
cd ~/Code/RLR_persona/posts/rayosx_corte
python3 agregar.py ~/Downloads/Rayos_X_terminados_datos_vN_AAAA-MM-DD_HHMM.csv AAAA-MM-DD HH:MM
python3 piezas.py AAAA-MM-DD          # SOLO_PNG=1 para saltar el video
```

1. Exportar el CSV de Rayos X terminados desde la app (rayosx.superleads.mx).
2. `agregar.py` escribe `cortes/<fecha>/agregados.json` y `agregados.md` (revisar el md: ahí se ve todo lo que se va a publicar).
3. `piezas.py` arma las 19 piezas con los números del JSON (títulos, gráficas, descripciones y hashtags se recalculan solos), las renderiza con el motor de [../estadisticas/render.py](../estadisticas/render.py) y escribe `salida/` (PNG + MP4), `html/`, `indice.json`, `SHORTS_corte_textos.md` y `hoja.jpg`.
4. Revisar la hoja y los textos; Ricardo decide fechas; nada se publica solo.
5. Comparar contra el corte anterior: los `agregados.json` de cada corte quedan en el repo para ver la serie en el tiempo.

## Las 19 piezas del corte

Radiografía del corte · Ocupación · Lugares vacíos · Prospectos al día · Conversión prospecto → inscrito · Cierre en cita · Colegiatura · Valor de vida · Publicidad y costo por alumno · Ingreso extra por +1 punto de conversión · Becas · Recomendación vs. anuncios · Herramientas de admisión · Equipo · Plan de compensación · Meses de mayor inscripción · Por qué no se inscribieron (creencia) · Percepción vs. realidad · Monetización además de la colegiatura.

Fuera por ahora: retorno de la publicidad (no está documentada la fórmula del campo `roi_publicidad` en la app) y eventos de inscripción (mediana 0).
