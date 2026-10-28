"""Lo común a los generadores de capítulo (capitulos/NN-*.py).

Cada capítulo tiene dos archivos que se editan a mano:

  capitulos/NN-titulo.md   el texto (bloques, recuadros, globos)
  capitulos/NN-titulo.py   el generador: qué pacientes y qué figuras lleva

y se rehace entero con:

  python3 docs/libro/capitulos/NN-titulo.py              casos + figuras + PDF
  python3 docs/libro/capitulos/NN-titulo.py --solo-pdf   solo el PDF (texto cambiado)
  python3 docs/libro/capitulos/NN-titulo.py --rearmar    vuelve a armar los casos por cuadro

El generador declara los casos con `demo()` (un paciente de práctica) o
`cuadro()` (un caso nuevo que arma el editor real, ver figuras/armar_casos.sh)
y las figuras con `fig.*`. Un caso por cuadro se rearma solo si cambió su
pedido; si no, se reutiliza el de casos/generados/.
"""
import json
import os
import pathlib
import subprocess
import sys

AQUI = pathlib.Path(__file__).resolve().parent        # docs/libro/herramientas
LIBRO = AQUI.parent                                   # docs/libro
RAIZ = pathlib.Path(os.environ.get('LABSIM', LIBRO.parent / 'LabSim'))   # checkout de LabSim (solo para rearmar casos y figuras)
MATERIAL = LIBRO / 'material'
CASOS = MATERIAL / 'casos'
GENERADOS = CASOS / 'generados'


class fig:
    """Las figuras que sabe hacer el motor (figuras/motor/), con sus opciones."""

    @staticmethod
    def audiograma(estudio=True, ldl=True, sin_enmascarar=False, clinico=False, combinado=False):
        """estudio: ósea solo donde la aérea es anormal; sin_enmascarar: la curva sombra;
        clinico: la forma de la hoja del tomo II (frecuencias arriba, ósea completa, LDL:);
        combinado: los dos oídos en una sola grilla, como se hace una audiometría."""
        f = {'tipo': 'audiograma', 'estudio': estudio, 'ldl': ldl, 'sin_enmascarar': sin_enmascarar,
             'clinico': clinico}
        if combinado:
            f['combinado'] = True
        return f

    @staticmethod
    def acumetria():
        return {'tipo': 'acumetria'}

    @staticmethod
    def logo(enmascarado=True):
        return {'tipo': 'logoaudiometria', 'enmascarado': enmascarado}

    @staticmethod
    def timpanograma(sonda=226):
        return {'tipo': 'timpanograma', 'sonda': sonda}

    @staticmethod
    def reflejos():
        return {'tipo': 'reflejos'}

    @staticmethod
    def impedancia(sonda=226):
        """Hoja de impedanciometría de los casos del tomo II (motor/impedancia_hoja.py):
        un timpanograma con las dos curvas, sus datos, los reflejos por sonda,
        el decay del reflejo y la función tubaria."""
        return {'tipo': 'impedancia', 'sonda': sonda}

    @staticmethod
    def teoae():
        return {'tipo': 'teoae'}

    @staticmethod
    def dpoae():
        return {'tipo': 'dpoae'}

    @staticmethod
    def abr(niveles=(80, 60, 40), estimulo=None, marcar=('I', 'III', 'V'),
            transductor='insercion', polaridad='alternada', tasa=21.1, promediaciones=None,
            ventana=None, enmascaramiento=None):
        """transductor: insercion/copa/oseo; polaridad: alternada/condensacion/
        rarefaccion; tasa en estímulos/s; ventana en ms (12 si no se da: el burst
        grave y el lactante piden 15 a 20); enmascaramiento: dB del ruido en el
        oído contrario (el MKG del panel). Lo que no cambia no entra al JSON,
        así los casos ya armados no se rehacen."""
        f = {'tipo': 'abr', 'niveles': list(niveles), 'marcar': list(marcar)}
        if estimulo:
            f['estimulo'] = estimulo
        if transductor != 'insercion':
            f['transductor'] = transductor
        if polaridad != 'alternada':
            f['polaridad'] = polaridad
        if tasa != 21.1:
            f['tasa'] = tasa
        if promediaciones:
            f['promediaciones'] = promediaciones     # cerca del umbral, para que la V se vea
        if ventana:
            f['ms_max'] = float(ventana)
        if enmascaramiento:
            f['enmascaramiento'] = float(enmascaramiento)
        return f

    @staticmethod
    def cortical(prueba='MLR', niveles=(70,), estimulo=None, canales=None, marcar=True,
                 promediaciones=None, ventana=None, oidos=None):
        """Latencia media o tardía en la ventana del ABR: prueba MLR, CAEP, P300
        o MMN. El caso necesita cuadro central (cuadro(..., central='tpac')).
        canales: los que se dibujan (por defecto C3/Cz/C4 en el MLR, Cz en el
        CAEP, Pz en la P300 y Fz en la MMN)."""
        f = {'tipo': 'cortical', 'prueba': prueba, 'niveles': list(niveles)}
        if estimulo:
            f['estimulo'] = estimulo
        if canales:
            f['canales'] = list(canales)
        if not marcar:
            f['marcar'] = False
        if promediaciones:
            f['promediaciones'] = promediaciones
        if ventana:
            f['ms_max'] = float(ventana)
        if oidos:
            f['oidos'] = list(oidos)
        return f

    @staticmethod
    def campo_libre(ganancia=None):
        """Campo libre calculado del caso (oído mejor). ganancia: {Hz: dB} de
        ganancia funcional para dibujar también la curva con audífono."""
        f = {'tipo': 'campo_libre'}
        if ganancia:
            f['ganancia'] = {str(k): v for k, v in ganancia.items()}
        return f

    @staticmethod
    def ecochg(nivel=90):
        return {'tipo': 'ecochg', 'nivel': nivel}

    @staticmethod
    def vemp(subtipo='cvemp'):
        return {'tipo': 'vemp', 'subtipo': subtipo}

    @staticmethod
    def vemps():
        """cVEMP y oVEMP lado a lado, en una sola figura ancha."""
        return {'tipo': 'vemp', 'subtipo': 'ambos'}

    @staticmethod
    def audiologo():
        """Audiograma de los dos oídos en un gráfico, con la logoaudiometría en
        datos al lado (SDT, SRT, UMD con los tres mejores intentos)."""
        return {'tipo': 'audiologo'}

    @staticmethod
    def nistagmo(con_fijacion=None, sin_fijacion=None):
        """Hoja del campo clínico (hexágonos). Cada mirada (izquierda, arriba,
        centro, abajo, derecha): VFL en °/s, negativa = bate a la izquierda, o
        {'dir': 'arriba'|'abajo'|'izquierda'|'derecha', 'vfl': n}."""
        return {'tipo': 'nistagmo', 'con_fijacion': con_fijacion or {}, 'sin_fijacion': sin_fijacion or {}}

    @staticmethod
    def audiosupra(sin_enmascarar=False):
        """Hoja auditiva de los casos vestibulares (motor/audio_supra.py):
        audiograma clínico con el Fowler y, al lado, logoaudiometría y
        supraliminares en una tabla OD | OI."""
        return {'tipo': 'audiosupra', 'sin_enmascarar': sin_enmascarar}

    @staticmethod
    def supraliminares():
        """Supraliminares del caso en LabSim: escalera de Fowler donde el caso
        la tiene, y SISI, Carhart, Metz y decay del reflejo de cada oído con
        pérdida sensorioneural."""
        return {'tipo': 'supraliminares'}

    @staticmethod
    def vhit(der=1.0, izq=1.0, sacadas_der=None, sacadas_izq=None):
        """vHIT del canal lateral (motor/vestibular.vhit): ganancia de cada lado y
        sacadas None|'covert'|'overt'|'ambas'."""
        return {'tipo': 'vhit', 'der': {'ganancia': der, 'sacadas': sacadas_der},
                'izq': {'ganancia': izq, 'sacadas': sacadas_izq}}

    @staticmethod
    def vng(*paneles):
        """VNG de una maniobra: un panel por posición, {'titulo', 'seg', 'h', 'v'};
        'h' y 'v' son el componente horizontal y el vertical, {'dir': +1|-1
        (derecha o arriba = +1), 'lat': s, 'pico': °/s, 'dur': s,
        'tipo': 'paroxistico'|'persistente'}, o None si no hay."""
        return {'tipo': 'vng', 'paneles': list(paneles)}

    @staticmethod
    def mariposa(od44, od30, oi44, oi30):
        """Calórica bitermal: VFL máxima de cada irrigación (°/s)."""
        return {'tipo': 'mariposa', 'OD44': od44, 'OD30': od30, 'OI44': oi44, 'OI30': oi30}


def _figuras(figuras):
    """La lista de figuras del caso, con una sola hoja de impedanciometría: el
    timpanograma y los reflejos van juntos en ella (él, 2026-10-20)."""
    out, vistos = [], set()
    for f in figuras:
        # una sola hoja de impedancia; y una sola de cada emisión, que en el
        # tomo II van siempre las dos juntas (él, 2026-10-20)
        if f.get('tipo') in ('impedancia', 'teoae', 'dpoae'):
            if f['tipo'] in vistos:
                continue
            vistos.add(f['tipo'])
        out.append(f)
    return out


def demo(numero, figuras, nombre=None):
    """Un paciente de práctica (docs/manual/capturas/casos_demo.json)."""
    return {'nombre': nombre or f'p{numero}', 'caso': f'demo:{numero}', 'figuras': _figuras(figuras)}


def cuadro(nombre, figuras, od='normal', oi='normal', grado_od=None, grado_oi=None,
           edad=40, sexo='hombre', semilla=None, edad_horas=None, edad_meses=None,
           anamnesis=None, historia=None, antecedentes=(), medicamentos='', cirugias='',
           central=None):
    """Un caso nuevo por cuadro (claves de CaseProfile::SCENARIOS) y grado.

    Un recién nacido o lactante va con edad_horas= o edad_meses= (la edad en
    años queda en 0, como lo carga el editor)."""
    pedido = {'cuadro': {'OD': od, 'OI': oi}, 'edad': edad, 'sexo': sexo}
    if edad_horas is not None or edad_meses is not None:
        pedido['edad'] = 0
        pedido['edad_valor'] = edad_horas if edad_horas is not None else edad_meses
        pedido['edad_unidad'] = 'horas' if edad_horas is not None else 'meses'
    grado = {k: v for k, v in (('OD', grado_od), ('OI', grado_oi)) if v}
    if grado:
        pedido['grado'] = grado
    if semilla is not None:
        pedido['semilla'] = semilla
    if central:
        pedido['central'] = central   # cuadro de la vía central (CaseProfile::CENTRAL_SCENARIOS)
    # La anamnesis va AL CASO (no solo al libro): queda en la ficha y en el
    # paciente de LabSim, que responde en el chat con esa misma historia.
    # historia: lista de (días hacia atrás, texto) -> líneas '{{-N}} texto'.
    if anamnesis or historia or antecedentes or medicamentos or cirugias:
        pedido['anamnesis'] = {
            'otros': ' '.join((anamnesis or '').split()),
            'historia': '\n'.join(f'{{{{-{d}}}}} {txt}' for d, txt in (historia or [])),
            'hist': list(antecedentes), 'medicamentos': medicamentos, 'cirugias': cirugias,
        }
    return {'nombre': nombre, 'caso': pedido, 'figuras': _figuras(figuras)}


def python_figuras():
    """El python de hacer_figuras.py, que necesita PySide6 y pyqtgraph (el ABR).
    LIBRO_PY_FIGURAS manda; si no, el venv del libro
    (~/.local/share/labsim/libro-venv: python del sistema + pyqtgraph), o el
    env micromamba labsim si existe. El env labsim desapareció el 2026-10-16."""
    if os.environ.get('LIBRO_PY_FIGURAS'):
        return [os.environ['LIBRO_PY_FIGURAS']]
    venv = pathlib.Path.home() / '.local' / 'share' / 'labsim' / 'libro-venv' / 'bin' / 'python'
    if venv.exists():
        return [str(venv)]
    if (pathlib.Path(os.environ.get('MAMBA_ROOT_PREFIX', pathlib.Path.home() / 'micromamba')) / 'envs' / 'labsim').exists():
        return ['micromamba', 'run', '-n', 'labsim', 'python']
    return [sys.executable]


class Capitulo:
    def __init__(self, numero):
        self.numero = numero
        self.prefijo = f'cap{numero:02d}_' if isinstance(numero, int) else f'{str(numero).lower()}_'

    def nombre(self, c):
        return self.prefijo + c['nombre']

    def generar(self, casos, argv=None):
        argv = sys.argv[1:] if argv is None else argv
        nombres = []
        rearmar = []
        for c in casos:
            n = self.nombre(c)
            nombres.append(n)
            spec = {'caso': c['caso'], 'figuras': c['figuras']}
            (CASOS / f'{n}.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
            if isinstance(c['caso'], dict):
                gen = GENERADOS / f'{n}.json'
                previo = json.loads(gen.read_text(encoding='utf-8')).get('pedido') if gen.exists() else None
                if '--rearmar' in argv or previo != c['caso']:
                    rearmar.append(n)
        if '--solo-pdf' not in argv:
            if rearmar:
                print('Armando casos:', ', '.join(rearmar))
                subprocess.run([str(MATERIAL / 'figuras' / 'armar_casos.sh'), *rearmar], check=True, cwd=RAIZ)
            # sin casos no hay figuras: hacer_figuras.py sin nombres rehace las de todo el libro
            if nombres and '--sin-figuras' not in argv:
                print('Figuras:', ', '.join(nombres))
                subprocess.run([*python_figuras(), str(MATERIAL / 'figuras' / 'hacer_figuras.py'),
                                *nombres], check=True, cwd=RAIZ, env=dict(os.environ, QT_QPA_PLATFORM='offscreen'))
        # solo el capítulo: el libro entero se arma aparte (hacer_libro.py --completo)
        subprocess.run([sys.executable, str(AQUI / 'hacer_libro.py'), str(self.numero)], check=True, cwd=RAIZ)
