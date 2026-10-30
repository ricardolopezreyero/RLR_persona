"""Corte periódico de los Rayos X de Inscripciones → agregados anonimizados por nivel.
Lee la exportación CSV de la app (nunca se sube al repo: trae nombres y contactos) y escribe
cortes/<fecha>/agregados.json + agregados.md con medianas, cuartiles, n y distribuciones por grupo.
Uso: python3 agregar.py <export.csv> <AAAA-MM-DD> [HH:MM]
Reglas (heredadas de Superleads-RayosX/scripts/datos-x/armar.py): fuera pruebas y archivados; una fila por institución
(la más reciente); montos solo en MXN; mediana antes que promedio; filtros de verosimilitud por métrica; n < 5 no se publica.
Ricardo López Reyero · RLR"""
import csv, json, os, re, sys, statistics as st, collections, datetime

csv.field_size_limit(10 ** 9)
AQUI = os.path.dirname(os.path.abspath(__file__))
PRUEBAS = re.compile(r'^(nueva instituci|victor$|boston|prueba|test)', re.I)
SUPERIOR = {'universidad', 'maestria', 'doctorado'}
N_MIN = 5

def num(v):
    try:
        x = float(v); return x if x == x else None
    except (TypeError, ValueError): return None

def lista(v):
    try:
        x = json.loads(v) if isinstance(v, str) and v else v; return x if isinstance(x, list) else []
    except Exception: return []

def cargar(ruta):
    filas = list(csv.DictReader(open(ruta, encoding='utf-8-sig')))
    total = len(filas)
    filas = [f for f in filas if f['status'] == 'submitted' and f['archivado'] != 'si' and f['posible_prueba'] != 'si'
             and not PRUEBAS.search((f['institucion'] or '').strip())]
    por_inst = {}
    for f in sorted(filas, key=lambda x: x['submitted_at']):
        por_inst[f['institution_id'] or f['institucion'].strip().lower()] = f
    return total, list(por_inst.values())

def niveles(f):
    o = set(lista(f['oferta_academica'])); g = {'todos'}
    sup = bool(o & SUPERIOR)
    if sup: g.add('universidad')
    if 'primaria' in o and not sup: g.add('primaria')
    if 'preparatoria' in o and not sup: g.add('preparatoria')
    return g

def metricas(f):
    """Solo lo verosímil; cada métrica se calcula por colegio y luego se agrega."""
    m = {}; mxn = f['moneda'] == 'mxn'
    mat, cap = num(f['matricula_actual']), num(f['capacidad_instalada'])
    if mat is not None and cap and mat >= 0 and cap > 0 and mat / cap <= 1.5:
        m['ocupacion'] = mat / cap * 100; m['vacios'] = max(cap - mat, 0); m['matricula'] = mat; m['capacidad'] = cap
    leads, nuevos = num(f['leads_al_anio']), num(f['nuevos_alumnos_ultimo_ciclo'])
    if leads and leads > 0 and nuevos is not None and nuevos >= 0 and nuevos / leads <= 1: m['conversion'] = nuevos / leads * 100
    if nuevos is not None and nuevos > 0: m['nuevos'] = nuevos
    ld = num(f['leads_al_dia'])
    if ld and ld > 0: m['leads_dia'] = ld
    cita = num(f['tasa_conversion_cita_alumno_pct'])
    if cita is not None and 0 < cita <= 100: m['cierre_cita'] = cita
    ret = num(f['meses_promedio_retencion'])
    if ret and ret > 0: m['retencion'] = ret
    if mxn:
        for k, col in [('colegiatura', 'colegiatura_mensual_promedio'), ('inscripcion', 'cuota_inscripcion'), ('ltv', 'ltv'), ('publicidad', 'inversion_publicidad_mensual'),
                       ('cpl', 'cpl'), ('caa', 'caa'), ('extra_1pct', 'ingreso_extra_por_1pct_conversion'), ('capacidad_ociosa', 'oportunidad_capacidad_no_usada')]:
            v = num(f[col])
            if v and v > 0: m[k] = v
        if m.get('colegiatura') and m['colegiatura'] < 300: del m['colegiatura']  # capturas en miles o errores
        if m.get('inscripcion') and m['inscripcion'] < 100: del m['inscripcion']
    roi = num(f['roi_publicidad'])
    if roi and roi > 0: m['roi'] = roi
    if f['usan_becas'] in ('si', 'no'): m['usan_becas'] = f['usan_becas'] == 'si'
    bec, bp = num(f['becados_pct']), num(f['beca_promedio_pct'])
    if bec is not None and 0 < bec <= 100: m['becados'] = bec
    if bp is not None and 0 < bp <= 100: m['beca_promedio'] = bp
    for k in ('pct_recomendados', 'pct_anuncios'):
        v = num(f[k])
        if v is not None and 0 <= v <= 100: m[k] = v
    herr = lista(f['proceso_admision_herramientas'])
    if herr:
        m['herramientas'] = herr; m['con_crm'] = any(h.startswith('crm') or h == 'erp' for h in herr)
        m['solo_whatsapp_excel'] = all(h in ('whatsapp', 'excel', 'messenger') for h in herr)
    staff = [num(f[k]) for k in ('staff_director_admisiones', 'staff_marketing', 'staff_community_manager', 'staff_asesores_admisiones')]
    if any(s is not None for s in staff):
        m['staff'] = sum(s or 0 for s in staff)
        if staff[0] is not None: m['tiene_director_adm'] = staff[0] > 0
        if staff[3] is not None: m['asesores'] = staff[3]
    ag = num(f['staff_agencia_externa'])
    if ag is not None: m['agencia'] = ag > 0
    ev = num(f['eventos_inscripcion_al_anio'])
    if ev is not None and ev >= 0: m['eventos'] = ev
    m['causas'] = lista(f['causas_no_inscripcion']); m['meses'] = lista(f['meses_mayor_inscripcion'])
    for k in ('estado_actual', 'plan_compensacion_asesores', 'nivel_marketing', 'gancho_cierre_admision', 'programa_recomendados', 'formularios_exclusivos_admisiones', 'tecnico_en_equipo'):
        if f[k]: m[k] = f[k]
    rubros = [k for k in ('uniforme_escolar', 'uniforme_deportes', 'asesorias_extra', 'transporte', 'cafeteria', 'libros', 'utiles', 'eventos_pinatas', 'eventos_graduaciones', 'viajes') if num(f.get(f'monetizacion_{k}')) is not None]
    if rubros:
        m['rubros_total'] = len(rubros); m['rubros_activos'] = [k for k in rubros if (num(f[f'monetizacion_{k}']) or 0) >= 1]
    edad = num(f['edad_institucional'])
    if edad and edad > 0:
        m['edad'] = datetime.date.today().year - edad if edad > 1800 else edad
    sedes = num(f['num_sedes'])
    if sedes and sedes > 0: m['sedes'] = sedes
    return m

def resumen(ms, k):
    v = [m[k] for m in ms if m.get(k) is not None]
    if len(v) < N_MIN: return None
    q = st.quantiles(v, n=4)
    return dict(n=len(v), mediana=st.median(v), promedio=st.fmean(v), q1=q[0], q3=q[2], min=min(v), max=max(v), suma=sum(v))

def parte(ms, k):
    v = [m[k] for m in ms if k in m]
    return dict(n=len(v), pct=sum(1 for x in v if x) / len(v) * 100) if len(v) >= N_MIN else None

def distribucion(ms, k, cortes, etiquetas):
    v = [m[k] for m in ms if m.get(k) is not None]
    if len(v) < N_MIN: return None
    cuentas = [0] * len(etiquetas)
    for x in v:
        i = sum(1 for c in cortes if x >= c); cuentas[i] += 1
    return dict(n=len(v), tramos=[dict(etiqueta=e, n=c, pct=c / len(v) * 100) for e, c in zip(etiquetas, cuentas)])

def conteo_lista(ms, k, etiquetas=None):
    con = [m for m in ms if m.get(k)]
    if len(con) < N_MIN: return None
    c = collections.Counter(x for m in con for x in m[k])
    return dict(n=len(con), items=[dict(clave=a, etiqueta=(etiquetas or {}).get(a, a), n=b, pct=b / len(con) * 100) for a, b in c.most_common()])

def conteo_valor(ms, k, etiquetas=None):
    con = [m[k] for m in ms if m.get(k)]
    if len(con) < N_MIN: return None
    c = collections.Counter(con)
    return dict(n=len(con), items=[dict(clave=a, etiqueta=(etiquetas or {}).get(a, a), n=b, pct=b / len(con) * 100) for a, b in c.most_common()])

ET = dict(
    herramientas={'whatsapp': 'WhatsApp', 'excel': 'Excel', 'crm_generico': 'CRM genérico', 'messenger': 'Messenger', 'crm_empresarial': 'CRM empresarial', 'crm_academico': 'CRM académico', 'crm_administrativo': 'CRM administrativo', 'erp': 'ERP', 'crm_educativo': 'CRM educativo'},
    causas={'precio': 'Precio', 'sin_seguimiento': 'No les dieron seguimiento', 'cupo_u_horario': 'Cupo u horario', 'se_fue_con_competencia': 'Se fue con la competencia', 'distancia': 'Distancia', 'no_era_quien_decide': 'No era quien decide', 'otro': 'Otro', 'requisitos_documentos': 'Requisitos o documentos'},
    plan={'no_hay': 'No hay plan de compensación', 'comodos': 'Hay plan, están cómodos', 'se_puede_mejorar': 'Hay plan, se puede mejorar'},
    estado={'menor_60': 'Menos de 60% de ocupación', 'entre_60_80': 'Entre 60 y 80%', 'mayor_80': 'Más de 80%', 'lista_espera': 'Con lista de espera'},
    calif={'mal': 'Mal', 'mas_o_menos': 'Más o menos', 'bien': 'Bien', 'muy_bien': 'Muy bien', 'excelente': 'Excelente'},
    rubros={'cafeteria': 'Cafetería', 'uniforme_escolar': 'Uniforme escolar', 'eventos_graduaciones': 'Graduaciones', 'libros': 'Libros', 'uniforme_deportes': 'Uniforme deportivo', 'eventos_pinatas': 'Eventos y piñatas', 'asesorias_extra': 'Asesorías extra', 'viajes': 'Viajes', 'utiles': 'Útiles', 'transporte': 'Transporte'},
    programa={'nada': 'No tiene', 'a': 'Básico', 'aa': 'Bueno', 'aaa': 'Excelente'},
)
MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

def agregar_grupo(ms):
    g = dict(n=len(ms), metricas={}, partes={}, distribuciones={}, listas={})
    for k in ('ocupacion', 'vacios', 'matricula', 'capacidad', 'conversion', 'nuevos', 'leads_dia', 'cierre_cita', 'retencion', 'colegiatura', 'inscripcion', 'ltv',
              'publicidad', 'cpl', 'caa', 'extra_1pct', 'capacidad_ociosa', 'roi', 'becados', 'beca_promedio', 'pct_recomendados', 'pct_anuncios', 'staff', 'asesores', 'eventos', 'rubros_total', 'edad', 'sedes'):
        r = resumen(ms, k)
        if r: g['metricas'][k] = r
    for k in ('usan_becas', 'con_crm', 'solo_whatsapp_excel', 'tiene_director_adm', 'agencia'):
        r = parte(ms, k)
        if r: g['partes'][k] = r
    g['distribuciones']['ocupacion'] = distribucion(ms, 'ocupacion', [60, 80], ['Menos de 60%', '60 a 80%', 'Más de 80%'])
    g['distribuciones']['conversion'] = distribucion(ms, 'conversion', [2, 5, 10], ['Menos de 2%', '2 a 5%', '5 a 10%', 'Más de 10%'])
    g['distribuciones']['cierre_cita'] = distribucion(ms, 'cierre_cita', [25, 50, 75], ['Menos de 25%', '25 a 50%', '50 a 75%', 'Más de 75%'])
    g['listas']['herramientas'] = conteo_lista(ms, 'herramientas', ET['herramientas'])
    g['listas']['causas'] = conteo_lista(ms, 'causas', ET['causas'])
    g['listas']['rubros'] = conteo_lista(ms, 'rubros_activos', ET['rubros'])
    meses = conteo_lista(ms, 'meses')
    if meses: meses['items'] = sorted(meses['items'], key=lambda i: MESES.index(i['clave']) if i['clave'] in MESES else 99)
    g['listas']['meses'] = meses
    g['listas']['plan'] = conteo_valor(ms, 'plan_compensacion_asesores', ET['plan'])
    g['listas']['estado'] = conteo_valor(ms, 'estado_actual', ET['estado'])
    g['listas']['nivel_marketing'] = conteo_valor(ms, 'nivel_marketing', ET['calif'])
    g['listas']['gancho'] = conteo_valor(ms, 'gancho_cierre_admision', ET['calif'])
    g['listas']['programa_recomendados'] = conteo_valor(ms, 'programa_recomendados', ET['programa'])
    g['distribuciones'] = {k: v for k, v in g['distribuciones'].items() if v}; g['listas'] = {k: v for k, v in g['listas'].items() if v}
    return g

GRUPOS = dict(todos='Todas las instituciones', primaria='Colegios con primaria (sin nivel superior)', preparatoria='Instituciones con preparatoria (sin nivel superior)', universidad='Universidades y posgrados')

def main(ruta, fecha, hora='18:08'):
    total, filas = cargar(ruta)
    datos = [(f, niveles(f), metricas(f)) for f in filas]
    ciudades = {re.sub(r'\s+', ' ', (f['inst_ciudad'] or '').strip().lower()) for f in filas if (f['inst_ciudad'] or '').strip()}
    out = dict(corte=dict(fecha=fecha, hora=hora, archivo=os.path.basename(ruta), filas_exportadas=total, instituciones=len(filas), ciudades=len(ciudades),
                          desde=min(f['fecha_hoy'] for f in filas), hasta=max(f['fecha_hoy'] for f in filas), generado=datetime.datetime.now().isoformat(timespec='minutes'),
                          grupos={k: sum(1 for _, g, _ in datos if k in g) for k in GRUPOS}, nombres_grupos=GRUPOS), grupos={})
    for k in GRUPOS:
        out['grupos'][k] = agregar_grupo([m for _, g, m in datos if k in g])
    carpeta = os.path.join(AQUI, 'cortes', fecha); os.makedirs(carpeta, exist_ok=True)
    json.dump(out, open(os.path.join(carpeta, 'agregados.json'), 'w'), ensure_ascii=False, indent=1)
    escribir_md(out, os.path.join(carpeta, 'agregados.md'))
    c = out['corte']; print(f"{c['instituciones']} instituciones ({c['filas_exportadas']} filas), {c['ciudades']} ciudades, {c['desde']} → {c['hasta']}; grupos {c['grupos']}")

NOMBRES = dict(ocupacion='Ocupación (alumnos ÷ capacidad)', vacios='Lugares vacíos', matricula='Matrícula', capacidad='Capacidad instalada', conversion='Conversión prospecto → inscrito', nuevos='Alumnos nuevos el último ciclo',
               leads_dia='Prospectos nuevos al día', cierre_cita='Cierre en cita (cita → inscrito)', retencion='Permanencia (meses)', colegiatura='Colegiatura mensual (MXN)', inscripcion='Cuota de inscripción (MXN)', ltv='Valor de vida de un alumno (MXN)',
               publicidad='Inversión mensual en publicidad (MXN)', cpl='Costo por prospecto (MXN)', caa='Costo de adquirir un alumno (MXN)', extra_1pct='Ingreso extra por +1% de conversión (MXN/año)', capacidad_ociosa='Valor anual de la capacidad sin usar (MXN)',
               roi='Retorno de la publicidad (veces)', becados='Alumnos becados (%)', beca_promedio='Beca promedio (%)', pct_recomendados='Llegan por recomendación (%)', pct_anuncios='Llegan por anuncios (%)', staff='Personas en admisiones y marketing',
               asesores='Asesores de admisiones', eventos='Eventos de inscripción al año', rubros_total='Rubros de monetización medidos', edad='Años operando', sedes='Sedes')

def escribir_md(out, ruta):
    c = out['corte']; L = [f"# Corte Rayos X · {c['fecha']} {c['hora']}", '',
                           f"{c['instituciones']} instituciones en {c['ciudades']} ciudades, Rayos X finalizados entre {c['desde']} y {c['hasta']} ({c['filas_exportadas']} filas exportadas; fuera pruebas, archivados y repetidos). "
                           'Sin nombres: solo agregados con su n. Mediana antes que promedio. Montos en MXN. Grupos con n < 5 no se publican.', '']
    for k, g in out['grupos'].items():
        L += [f"## {GRUPOS[k]} · n = {g['n']}", '', '| Dato | Mediana | Q1 – Q3 | Promedio | n |', '|---|---|---|---|---|']
        for mk, r in g['metricas'].items():
            L.append(f"| {NOMBRES[mk]} | {r['mediana']:,.1f} | {r['q1']:,.1f} – {r['q3']:,.1f} | {r['promedio']:,.1f} | {r['n']} |")
        L.append('')
        for pk, r in g['partes'].items(): L.append(f"- {pk}: {r['pct']:.0f}% (n = {r['n']})")
        for dk, d in g['distribuciones'].items(): L.append(f"- {dk} (n = {d['n']}): " + ' · '.join(f"{t['etiqueta']} {t['pct']:.0f}%" for t in d['tramos']))
        for lk, d in g['listas'].items(): L.append(f"- {lk} (n = {d['n']}): " + ' · '.join(f"{i['etiqueta']} {i['pct']:.0f}%" for i in d['items'][:8]))
        L.append('')
    open(ruta, 'w').write('\n'.join(L))

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], *(sys.argv[3:4]))
# Ricardo López Reyero · EYE · 181218
