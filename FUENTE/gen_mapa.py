"""Genera el SVG del mapa de Venezuela (estados reales, geoBoundaries CC BY 4.0) con pines, mini cava y nombres."""
import json, math
SC = 62            # px por grado
LON0, LAT1 = -73.6, 12.45
def xy(lo, la): return ((lo - LON0) * SC + 20, (LAT1 - la) * SC + 20)
def dp(pts, tol):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dmax, idx = 0, 0
    dx, dy = b[0]-a[0], b[1]-a[1]; L = math.hypot(dx, dy) or 1e-9
    for i in range(1, len(pts)-1):
        d = abs(dy*pts[i][0] - dx*pts[i][1] + b[0]*a[1] - b[1]*a[0]) / L
        if d > dmax: dmax, idx = d, i
    if dmax > tol: return dp(pts[:idx+1], tol)[:-1] + dp(pts[idx:], tol)
    return [a, b]
d = json.load(open('ven_adm1.geojson'))
paths, nombres = [], []
tonos = ["#2584d3", "#1f78c8", "#2a8ad9", "#1d70bf"]          # estados donde han trabajado
claros = ["#bfe0f7", "#b3d9f5", "#c7e5f8", "#b9dcf6"]          # resto del país
# confirmados por el cliente (publicación de Instagram del 1 ene 2025 y obras publicadas)
SERVIDOS = {"Bolívar", "Monagas", "Sucre", "Distrito Capital", "Miranda", "Zulia", "Carabobo", "Aragua", "Mérida",
            "Trujillo", "Lara", "Anzoátegui", "Nueva Esparta", "La Guaira"}
for n, f in enumerate(d['features']):
    nom = f['properties']['shapeName']
    if nom.startswith('Dependencias'): continue
    g = f['geometry']; polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']]
    dd = ""
    for p in polys:
        for ring in p[:1]:
            pts = [xy(*c[:2]) for c in ring]
            m = len(pts) // 2
            pts = dp(pts[:m + 1], 0.9)[:-1] + dp(pts[m:], 0.9)
            if len(pts) < 4: continue
            dd += "M" + "L".join(f"{x:.0f},{y:.0f}" for x, y in pts) + "Z"
    paths.append(f'<path d="{dd}" fill="{(tonos if nom in SERVIDOS else claros)[n % 4]}" style="--i:{len(paths)}"><title>{nom}</title></path>')
CIU = [  # obras publicadas, sede y un pin por cada estado de SERVIDOS (en su ciudad principal)
 # nombre, lon, lat, (dx, dy, lado): s=etiqueta a la derecha, e=a la izquierda, m=centrada
 ("Caracas, Miranda y La Guaira", -66.90, 10.52, (0, -74, "m")), ("Tocuyito", -68.10, 10.10, (-6, 12, "e")),
 ("Barcelona · sede", -64.70, 10.13, (0, 12, "m")), ("Cumaná", -64.18, 10.45, (8, -52, "s")),
 ("Zulia", -71.64, 10.65, (-14, -40, "e")), ("Lara", -69.32, 10.07, (-14, -40, "e")),
 ("Trujillo", -70.60, 9.32, (-14, -40, "e")), ("Mérida", -71.15, 8.59, (-14, 12, "e")),
 ("Aragua", -67.60, 10.25, (0, 12, "m")), ("Nueva Esparta", -63.90, 11.00, (8, -70, "s")),
 ("Monagas", -63.18, 9.75, (12, -14, "s")), ("Bolívar", -62.65, 8.30, (12, -14, "s")),
]
pins = ""
CAVA = ('<rect x="0" y="0" width="26" height="20" rx="3" fill="#fff" stroke="#06224d" stroke-width="1.6"/><rect x="15" y="4" width="8" height="16" rx="1.5" fill="#29A9E8"/>'
        '<rect x="2" y="2.5" width="12" height="3" rx="1" fill="#06224d"/><g stroke="#0040A0" stroke-width="1.3" stroke-linecap="round"><path d="M7.5 8v9M4 10l7 5M4 15l7-5"/></g>')
for i, (nom, lo, la, (dx, dy, an)) in enumerate(CIU):
    x, y = xy(lo, la); w = len(nom) * 7.6 + 54
    lx = dx if an == "s" else dx - w if an == "e" else -w / 2
    pins += (f'<g class="pn" style="--d:{0.8+i*0.32:.2f}s" transform="translate({x:.0f} {y:.0f})">'
             f'<circle class="rip" r="10"/><circle class="rip r2" r="10"/>'
             f'<g class="pk"><path d="M0 0c-4-8.8-13.4-14.4-13.4-25a13.4 13.4 0 0 1 26.8 0c0 10.6-9.4 16.2-13.4 25z" fill="#06224d"/><circle cy="-25" r="5.8" fill="#00E3FF"/></g>'
             f'<g transform="translate({lx:.0f} {dy})"><g class="lb"><rect width="{w:.0f}" height="34" rx="17" fill="#fff" stroke="#cfe0f3" stroke-width="1.5"/>'
             f'<g transform="translate(10 7)">{CAVA}</g><text x="42" y="22.5">{nom}</text></g></g></g>')
ancho, alto = int((73.6 - 59.7) * SC + 40), int((12.45 - 0.55) * SC + 40)
svg = (f'<svg class="vzmap" viewBox="0 0 {ancho} {alto}" role="img" aria-label="Mapa de Venezuela con los estados donde Refrigeración Team ha instalado cavas cuarto">'
       f'<defs><radialGradient id="vzglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#29A9E8" stop-opacity=".25"/><stop offset="1" stop-color="#29A9E8" stop-opacity="0"/></radialGradient></defs>'
       f'<ellipse cx="{ancho*0.55:.0f}" cy="{alto*0.52:.0f}" rx="{ancho*0.55:.0f}" ry="{alto*0.5:.0f}" fill="url(#vzglow)"/>'
       f'<text class="gl" x="{xy(-69.5,12.3)[0]:.0f}" y="{xy(-69.5,12.3)[1]:.0f}">Mar Caribe</text><text class="gl" x="{xy(-72.9,5.2)[0]:.0f}" y="{xy(-72.9,5.2)[1]:.0f}">Colombia</text>'
       f'<text class="gl" x="{xy(-63.5,3.0)[0]:.0f}" y="{xy(-63.5,3.0)[1]:.0f}">Brasil</text><text class="gl" x="{xy(-60.6,7.5)[0]:.0f}" y="{xy(-60.6,7.5)[1]:.0f}">Guyana</text>'
       f'<g class="vz-st" stroke="#fff" stroke-width="1.6" stroke-linejoin="round">{"".join(paths)}</g>{pins}</svg>')
open('mapa_vzla.svg.html', 'w', encoding='utf-8').write(svg)
print(len(svg)//1024, "KB", ancho, alto)
