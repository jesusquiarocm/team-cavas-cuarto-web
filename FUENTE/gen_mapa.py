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
tonos = ["#3aa6ec", "#2e94e0", "#2584d3", "#3399e3"]
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
    paths.append(f'<path d="{dd}" fill="{tonos[n % 4]}" style="--i:{len(paths)}"><title>{nom}</title></path>')
CIU = [  # nombre, lon, lat, (dx, dy, lado) : posición de la etiqueta respecto al pin; lado s=empieza a la derecha del punto, e=termina a la izquierda, m=centrada
 ("Caracas", -66.90, 10.49, (8, -52, "s")), ("Maracaibo", -71.64, 10.65, (-14, -40, "e")), ("Valencia", -68.00, 10.16, (0, 12, "m")),
 ("Barquisimeto", -69.32, 10.07, (-8, 14, "e")), ("Barcelona", -64.70, 10.13, (8, -48, "s")), ("Mérida", -71.15, 8.59, (-14, -36, "e")),
 ("Maturín", -63.18, 9.75, (10, -22, "s")), ("San Cristóbal", -72.23, 7.77, (-10, 14, "s")), ("Ciudad Guayana", -62.65, 8.30, (10, -22, "s")),
 ("San Fernando de Apure", -67.47, 7.89, (0, 12, "m")), ("Puerto Ayacucho", -67.62, 5.66, (12, -22, "s")), ("Coro", -69.68, 11.40, (-14, -38, "e")),
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
svg = (f'<svg class="vzmap" viewBox="0 0 {ancho} {alto}" role="img" aria-label="Mapa de Venezuela por estados con cavas cuarto instaladas en todo el país">'
       f'<defs><radialGradient id="vzglow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#29A9E8" stop-opacity=".25"/><stop offset="1" stop-color="#29A9E8" stop-opacity="0"/></radialGradient></defs>'
       f'<ellipse cx="{ancho*0.55:.0f}" cy="{alto*0.52:.0f}" rx="{ancho*0.55:.0f}" ry="{alto*0.5:.0f}" fill="url(#vzglow)"/>'
       f'<text class="gl" x="{xy(-69.5,12.3)[0]:.0f}" y="{xy(-69.5,12.3)[1]:.0f}">Mar Caribe</text><text class="gl" x="{xy(-72.9,5.2)[0]:.0f}" y="{xy(-72.9,5.2)[1]:.0f}">Colombia</text>'
       f'<text class="gl" x="{xy(-63.5,3.0)[0]:.0f}" y="{xy(-63.5,3.0)[1]:.0f}">Brasil</text><text class="gl" x="{xy(-60.6,7.5)[0]:.0f}" y="{xy(-60.6,7.5)[1]:.0f}">Guyana</text>'
       f'<g class="vz-st" stroke="#fff" stroke-width="1.6" stroke-linejoin="round">{"".join(paths)}</g>{pins}</svg>')
open('mapa_vzla.svg.html', 'w', encoding='utf-8').write(svg)
print(len(svg)//1024, "KB", ancho, alto)
