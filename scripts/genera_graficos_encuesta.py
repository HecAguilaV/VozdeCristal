# Gráfico circular (pie)
def svg_circular(conteo, etiquetas, width=220, height=220, colores=None):
    if colores is None:
        colores = ['#ff7f50', '#6ec6ff', '#ffd54f', '#81c784', '#ba68c8', '#ff8a65']
    total = sum(conteo.get(k,0) for k in etiquetas)
    if total == 0:
        return svg_placeholder('Sin respuestas', width, height)
    cx, cy, r = width//2, height//2, 80
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
    svg += '<style>.label{font:12px sans-serif;}</style>\n'
    start = 0
    for i, key in enumerate(etiquetas):
        val = conteo.get(key, 0)
        angle = 2*math.pi*val/total
        x1 = cx + r*math.cos(start)
        y1 = cy + r*math.sin(start)
        x2 = cx + r*math.cos(start+angle)
        y2 = cy + r*math.sin(start+angle)
        large = 1 if angle > math.pi else 0
        color = colores[i % len(colores)]
        svg += f'<path d="M{cx},{cy} L{x1},{y1} A{r},{r} 0 {large},1 {x2},{y2} Z" fill="{color}"/>'
        # Etiqueta
        mid = start + angle/2
        lx = cx + (r+25)*math.cos(mid)
        ly = cy + (r+25)*math.sin(mid)
        percent = f"{(val/total*100):.0f}%" if total else "0%"
        svg += f'<text class="label" x="{lx}" y="{ly}" text-anchor="middle">{key} ({percent})</text>'
        start += angle
    svg += '</svg>'
    return svg
# Si no hay respuestas, función placeholder
def svg_placeholder(text, width=400, height=120):
    return f'''<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">
      <text x="{width//2}" y="{height//2}" font-size="20" text-anchor="middle" fill="#888">{text}</text>
    </svg>'''

# Gráfico de barras
def svg_barras(conteo, etiquetas, width=400, height=160, colores=None):
    if colores is None:
        colores = ['#ff7f50', '#6ec6ff', '#ffd54f', '#81c784', '#ba68c8', '#ff8a65']
    max_val = max(conteo.values()) if conteo else 1
    n = len(etiquetas)
    bar_width = min(50, (width-40)//n-10) if n > 0 else 40
    gap = (width - 2*20 - n*bar_width) // (n-1) if n > 1 else 0
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
    svg += '<style>.label{font:12px sans-serif;}</style>\n'
    for i, key in enumerate(etiquetas):
        valor = conteo.get(key, 0)
        x = 20 + i * (bar_width + gap)
        y = height-40 - (valor / max_val) * 80 if max_val else height-40
        h = (valor / max_val) * 80 if max_val else 0
        color = colores[i % len(colores)]
        svg += f'<rect x="{x}" y="{y}" width="{bar_width}" height="{h}" fill="{color}" rx="6"/>'
        # Etiqueta rotada para el eje X
        svg += f'<g transform="translate({x+bar_width/2},{height-10}) rotate(-35)"><text class="label" text-anchor="end">{key}</text></g>'
        svg += f'<text class="label" x="{x+bar_width/2}" y="{y-5}" text-anchor="middle">{valor}</text>'
    svg += '</svg>'
    return svg
import requests
import csv
from io import StringIO
import math
import os
import json

# Configuración
SHEET_ID = '1xZ6qSFg_YPNtlQcKapjXvwqbDTyBFZxp39BcFx1BzII'
CSV_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv'
IMG_DIR = 'public/assets/img/'
JSON_OUT = 'public/assets/encuesta_data.json'


# Nombres de archivos de salida alineados a la nueva narrativa
ARCHIVOS = {
    'p1_barras': 'encuesta_p1_barras.svg',  # Percepción de seguridad
    'p2_circular': 'encuesta_p2_circular.svg',  # Disposición a usar la pulsera
    'p3_barras': 'encuesta_p3_barras.svg',  # Valoración de autonomía
    'p4_barras': 'encuesta_p4_barras.svg',  # Confianza en IA ética
    'p5_barras': 'encuesta_p5_barras.svg',  # Prioridad de apoyo pedagógico
}

# Preguntas (índices de columna, comenzando en 0, AJUSTAR según la estructura final de la encuesta)
PREGUNTAS = {
    'p1': 1,  # ¿Siente usted que tiene información suficiente sobre lo que ocurre con su hijo/a cuando está bajo el cuidado de terceros?
    'p2': 2,  # En el proceso de aprender lateralidad... ¿qué tan útil considera que los accesorios pedagógicos incorporen sensores de seguridad?
    'p3': 3,  # ¿Es fundamental para usted que un dispositivo de seguridad no grabe audio ni video?
    'p4': 4,  # ¿Estaría de acuerdo con que los centros de salud o establecimientos educacionales entreguen este "Kit"?
    'p5': 5,  # ¿Cuál es su mayor temor respecto a la seguridad de su hijo/a en entornos donde usted no está presente?
}

# Colores para gráficos
COLORES = ['#ff7f50', '#6ec6ff', '#ffd54f', '#81c784', '#ba68c8', '#ff8a65']

# Lee datos de Google Sheets
try:
    resp = requests.get(CSV_URL)
    resp.encoding = 'utf-8'
    csvfile = StringIO(resp.text)
    rows = list(csv.reader(csvfile))
    if not rows or not any(rows[0]):
        raise ValueError('No se pudo leer datos válidos del Sheet.')
except Exception as e:
    rows = []

if len(rows) <= 1:
    # No hay respuestas
    for clave, archivo in ARCHIVOS.items():
        with open(os.path.join(IMG_DIR, archivo), 'w') as f:
            f.write(svg_placeholder('Sin respuestas'))
    # Exportar JSON vacío
    data_json = {
        "p1": {"labels": [], "values": []},
        "p2": {"labels": [], "values": []},
        "p3": {"labels": [], "values": []},
        "p4": {"labels": [], "values": []},
        "p5": {"labels": [], "values": []}
    }
else:
    headers = rows[0]
    datos = rows[1:]

    # Pregunta 1: Información suficiente sobre el hijo/a
    p1_vals = [row[PREGUNTAS['p1']] for row in datos if len(row) > PREGUNTAS['p1'] and row[PREGUNTAS['p1']]]
    p1_etiquetas = sorted(set(p1_vals))
    p1_conteo = {k: p1_vals.count(k) for k in p1_etiquetas}
    with open(os.path.join(IMG_DIR, ARCHIVOS['p1_barras']), 'w') as f:
        f.write(svg_barras(p1_conteo, p1_etiquetas))

    # Pregunta 2: Utilidad de accesorios pedagógicos con sensores
    p2_vals = [row[PREGUNTAS['p2']] for row in datos if len(row) > PREGUNTAS['p2'] and row[PREGUNTAS['p2']]]
    p2_etiquetas = sorted(set(p2_vals))
    p2_conteo = {k: p2_vals.count(k) for k in p2_etiquetas}
    with open(os.path.join(IMG_DIR, ARCHIVOS['p2_circular']), 'w') as f:
        f.write(svg_circular(p2_conteo, p2_etiquetas))

    # Pregunta 3: Privacidad total (Sí/No)
    p3_vals = [row[PREGUNTAS['p3']] for row in datos if len(row) > PREGUNTAS['p3'] and row[PREGUNTAS['p3']]]
    p3_etiquetas = sorted(set(p3_vals))
    p3_conteo = {k: p3_vals.count(k) for k in p3_etiquetas}
    with open(os.path.join(IMG_DIR, ARCHIVOS['p3_barras']), 'w') as f:
        f.write(svg_barras(p3_conteo, p3_etiquetas))

    # Pregunta 4: Entrega gratuita del kit (Sí/No)
    p4_vals = [row[PREGUNTAS['p4']] for row in datos if len(row) > PREGUNTAS['p4'] and row[PREGUNTAS['p4']]]
    p4_etiquetas = sorted(set(p4_vals))
    p4_conteo = {k: p4_vals.count(k) for k in p4_etiquetas}
    with open(os.path.join(IMG_DIR, ARCHIVOS['p4_barras']), 'w') as f:
        f.write(svg_barras(p4_conteo, p4_etiquetas))

    # Pregunta 5: Mayor temor respecto a la seguridad
    p5_vals = [row[PREGUNTAS['p5']] for row in datos if len(row) > PREGUNTAS['p5'] and row[PREGUNTAS['p5']]]
    # Para temores múltiples separados por coma, separamos y contamos cada uno
    p5_items = []
    for val in p5_vals:
        p5_items.extend([v.strip() for v in val.split(',') if v.strip()])
    p5_etiquetas = sorted(set(p5_items))
    p5_conteo = {k: p5_items.count(k) for k in p5_etiquetas}
    with open(os.path.join(IMG_DIR, ARCHIVOS['p5_barras']), 'w') as f:
        f.write(svg_barras(p5_conteo, p5_etiquetas))

    # Exportar datos a JSON para el dashboard
    data_json = {
        "p1": {"labels": p1_etiquetas, "values": [p1_conteo[k] for k in p1_etiquetas]},
        "p2": {"labels": p2_etiquetas, "values": [p2_conteo[k] for k in p2_etiquetas]},
        "p3": {"labels": p3_etiquetas, "values": [p3_conteo[k] for k in p3_etiquetas]},
        "p4": {"labels": p4_etiquetas, "values": [p4_conteo[k] for k in p4_etiquetas]},
        "p5": {"labels": p5_etiquetas, "values": [p5_conteo[k] for k in p5_etiquetas]}
    }


# Guardar JSON para el dashboard (fuera de cualquier función)
if 'data_json' in locals():
    with open(JSON_OUT, 'w', encoding='utf-8') as jf:
        json.dump(data_json, jf, ensure_ascii=False, indent=2)

# Gráfico circular (pie)
def svg_circular(conteo, etiquetas, width=220, height=220, colores=COLORES):
    total = sum(conteo.get(k,0) for k in etiquetas)
    if total == 0:
        return svg_placeholder('Sin respuestas', width, height)
    cx, cy, r = width//2, height//2, 80
    svg = f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">\n'
    svg += '<style>.label{font:12px sans-serif;}</style>\n'
    start = 0
    for i, key in enumerate(etiquetas):
        val = conteo.get(key, 0)
        angle = 2*math.pi*val/total
        x1 = cx + r*math.cos(start)
        y1 = cy + r*math.sin(start)
        x2 = cx + r*math.cos(start+angle)
        y2 = cy + r*math.sin(start+angle)
        large = 1 if angle > math.pi else 0
        color = colores[i % len(colores)]
        svg += f'<path d="M{cx},{cy} L{x1},{y1} A{r},{r} 0 {large},1 {x2},{y2} Z" fill="{color}"/>'
        # Etiqueta
        mid = start + angle/2
        lx = cx + (r+25)*math.cos(mid)
        ly = cy + (r+25)*math.sin(mid)
        percent = f"{(val/total*100):.0f}%" if total else "0%"
        svg += f'<text class="label" x="{lx}" y="{ly}" text-anchor="middle">{key} ({percent})</text>'
        start += angle
    svg += '</svg>'
    return svg

# Procesa y genera gráficos
if len(rows) <= 1:
    # No hay respuestas
    for clave, archivo in ARCHIVOS.items():
        with open(os.path.join(IMG_DIR, archivo), 'w') as f:
            f.write(svg_placeholder('Sin respuestas'))
else:
    headers = rows[0]
    datos = rows[1:]


    # Pregunta 1: Información suficiente sobre el hijo/a
    p1_vals = [row[PREGUNTAS['p1']] for row in datos if len(row) > PREGUNTAS['p1'] and row[PREGUNTAS['p1']]]
    p1_etiquetas = sorted(set(p1_vals))
    p1_conteo = {k: p1_vals.count(k) for k in p1_etiquetas}
    with open(os.path.join(IMG_DIR, ARCHIVOS['p1_barras']), 'w') as f:
        f.write(svg_barras(p1_conteo, p1_etiquetas))

    # Pregunta 2: Utilidad de accesorios pedagógicos con sensores
    p2_vals = [row[PREGUNTAS['p2']] for row in datos if len(row) > PREGUNTAS['p2'] and row[PREGUNTAS['p2']]]
    p2_etiquetas = sorted(set(p2_vals))
    p2_conteo = {k: p2_vals.count(k) for k in p2_etiquetas}
    with open(os.path.join(IMG_DIR, ARCHIVOS['p2_circular']), 'w') as f:
        f.write(svg_circular(p2_conteo, p2_etiquetas))

    # Pregunta 3: Privacidad total (Sí/No)
    p3_vals = [row[PREGUNTAS['p3']] for row in datos if len(row) > PREGUNTAS['p3'] and row[PREGUNTAS['p3']]]
    p3_etiquetas = sorted(set(p3_vals))
    p3_conteo = {k: p3_vals.count(k) for k in p3_etiquetas}
    with open(os.path.join(IMG_DIR, ARCHIVOS['p3_barras']), 'w') as f:
        f.write(svg_barras(p3_conteo, p3_etiquetas))

    # Pregunta 4: Entrega gratuita del kit (Sí/No)
    p4_vals = [row[PREGUNTAS['p4']] for row in datos if len(row) > PREGUNTAS['p4'] and row[PREGUNTAS['p4']]]
    p4_etiquetas = sorted(set(p4_vals))
    p4_conteo = {k: p4_vals.count(k) for k in p4_etiquetas}
    with open(os.path.join(IMG_DIR, ARCHIVOS['p4_barras']), 'w') as f:
        f.write(svg_barras(p4_conteo, p4_etiquetas))

    # Pregunta 5: Mayor temor respecto a la seguridad
    p5_vals = [row[PREGUNTAS['p5']] for row in datos if len(row) > PREGUNTAS['p5'] and row[PREGUNTAS['p5']]]
    # Para temores múltiples separados por coma, separamos y contamos cada uno
    p5_items = []
    for val in p5_vals:
        p5_items.extend([v.strip() for v in val.split(',') if v.strip()])
    p5_etiquetas = sorted(set(p5_items))
    p5_conteo = {k: p5_items.count(k) for k in p5_etiquetas}
    with open(os.path.join(IMG_DIR, ARCHIVOS['p5_barras']), 'w') as f:
        f.write(svg_barras(p5_conteo, p5_etiquetas))

print('¡Gráficos generados!')
