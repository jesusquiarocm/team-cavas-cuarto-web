"""Renderiza el video tutorial 'Cómo pedir tu cotización' (1080x1920, 30 fps) como frames -> ffmpeg.

Uso:  python3 render_tutorial.py [--prueba SEGUNDO ...]   (guarda PNG sueltos)
      python3 render_tutorial.py                          (renderiza video_mudo.mp4)
Lee audio/<id>.wav (duración de cada escena) y audio/palabras_tutorial.json (subtítulos).
"""
import json, math, subprocess, sys, wave
from pathlib import Path
from multiprocessing import Pool
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = Path(__file__).resolve().parent
LOGO = AQUI.parent / "SITIO" / "img" / "logo.png"
FFMPEG = "/Users/jesusquiaro/Downloads/EDICIONES TCC/.venv-chatterbox/lib/python3.11/site-packages/imageio_ffmpeg/binaries/ffmpeg-macos-aarch64-v7.1"
COOL = "/Users/jesusquiaro/Library/Containers/com.lemon.lvoverseas/Data/Library/Fonts/Coolvetica Rg.otf"
ARIAL = "/System/Library/Fonts/Supplemental/Arial.ttf"
ARIALB = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

W, H, FPS, SS = 1080, 1920, 30, 2
NAVY, NAVYD, SKY, CYAN = (0, 64, 160), (7, 38, 96), (41, 169, 232), (0, 227, 255)
INK, MUTED, LINE, ICE = (17, 33, 61), (92, 108, 134), (205, 219, 235), (238, 244, 251)
GREEN, GREEND, WHITE = (37, 211, 102), (14, 122, 59), (255, 255, 255)
PAD = 0.7                       # silencio al final de cada escena (s)

_f = {}
def font(path, px):
    k = (path, px)
    if k not in _f:
        _f[k] = ImageFont.truetype(path, int(px * SS))
    return _f[k]
def S(v):
    return int(round(v * SS))

def ease(t):                       # easeInOutCubic
    t = max(0.0, min(1.0, t)); return 4*t*t*t if t < .5 else 1 - (-2*t + 2) ** 3 / 2
def easeout(t):
    t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
def back(t):                       # rebote
    t = max(0.0, min(1.0, t)); c = 1.70158; return 1 + (c+1)*(t-1)**3 + c*(t-1)**2
def clamp(v, a=0.0, b=1.0): return max(a, min(b, v))

def rr(d, box, r, fill=None, outline=None, width=1):
    x0, y0, x1, y1 = box
    d.rounded_rectangle((S(x0), S(y0), S(x1), S(y1)), S(r), fill=fill, outline=outline, width=S(width) if outline else 0)
def tx(d, xy, s, f, fill, anchor="la"):
    d.text((S(xy[0]), S(xy[1])), s, font=f, fill=fill, anchor=anchor)

# --------------------------------------------------------------------------- datos
ESCENAS = [
 dict(id="intro"), dict(id="p1", campo="que"), dict(id="p2", campo="tipo"), dict(id="p3", campo="temp"),
 dict(id="p4", campo="med"), dict(id="p5", campo="ciu"), dict(id="p6", campo="nom"), dict(id="p7", campo="foto"),
 dict(id="p8", campo="enviar"), dict(id="fin"),
]
OPC = {
 "que": ["Fabricar e instalar una cava cuarto", "Comprar equipos o materiales", "Un freezer", "Otro"],
 "tipo": ["Carnicería", "Pescadería / mariscos", "Pollería", "Restaurante", "Heladería", "Panadería", "Abasto / bodega", "Distribuidor / galpón", "Otro"],
 "temp": ["Refrigeración (0 a 5 °C)", "Congelación (−18 °C)", "Ambas", "No estoy seguro"],
}
ELIGE = {"que": 0, "tipo": 0, "temp": 3}
CFG = {
 "que": dict(open=2.0, pick=9.6, hov=[(5.0, 6.5, 0), (6.6, 7.6, 1), (7.7, 8.5, 2), (8.6, 9.3, 3)]),
 "tipo": dict(open=2.4, pick=6.9, hov=[(3.6, 4.6, 0), (4.7, 5.6, 5), (5.8, 6.6, 6)]),
 "temp": dict(open=2.0, pick=12.8, hov=[(3.0, 5.2, 0), (5.4, 8.0, 1), (9.0, 12.6, 3)], tag=(9.0, 12.4)),
}
VALOR = {"med": ["4", "3", "2.5"], "ciu": "Barcelona, Anzoátegui", "nom": "María"}
ETIQ = {"que": "¿Qué necesitas?", "tipo": "¿Para qué negocio es?", "temp": "¿Qué temperatura necesitas?",
        "med": "Medidas aproximadas en metros", "ciu": "¿En qué ciudad o estado?", "nom": "Tu nombre"}
# posiciones (espacio del formulario, px): (y de la etiqueta)
POS = {"que": 190, "tipo": 390, "temp": 590, "med": 790, "ciu": 1000, "nom": 1200, "foto": 1400, "enviar": 1500}
ALTO_FORM = 1680
CARD = (60, 330, 1020, 1470)     # x0,y0,x1,y1
CW, CH = CARD[2] - CARD[0], CARD[3] - CARD[1]

def cargar_tiempos():
    dur, t0 = {}, 0.0
    ini = {}
    for e in ESCENAS:
        with wave.open(str(AQUI / "audio" / f"{e['id']}.wav")) as w:
            d = w.getnframes() / w.getframerate()
        e["voz"] = d; e["dur"] = d + PAD; e["t0"] = t0; t0 += e["dur"]
    return t0

def scroll_de(campo):
    if campo is None: return 0
    y = POS[campo]
    obj = y - 170 if campo != "enviar" else y - 520
    return clamp(obj, 0, ALTO_FORM - CH + 40)

# --------------------------------------------------------------------------- piezas
def fondo():
    im = Image.new("RGB", (S(W), S(H)), NAVYD)
    px = Image.new("RGB", (1, 256))
    for y in range(256):
        k = y / 255
        px.putpixel((0, y), tuple(int(NAVY[i] * (1 - k) * .9 + NAVYD[i] * k + (8 if i == 2 else 0)) for i in range(3)))
    im = px.resize((S(W), S(H)), Image.BILINEAR)
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.ellipse((S(-300), S(-300), S(500), S(500)), fill=(41, 169, 232, 40))
    d.ellipse((S(600), S(1300), S(1500), S(2200)), fill=(0, 227, 255, 28))
    ov = ov.filter(ImageFilter.GaussianBlur(S(60)))
    im.paste(ov, (0, 0), ov)
    return im
BG = None

def sombra(im, box, r, alpha=90, blur=30, dy=18):
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    x0, y0, x1, y1 = box
    d.rounded_rectangle((S(x0), S(y0 + dy), S(x1), S(y1 + dy)), S(r), fill=(0, 10, 40, alpha))
    ov = ov.filter(ImageFilter.GaussianBlur(S(blur))); im.paste(ov, (0, 0), ov)

def anillo(d, box, r, t, color=CYAN):
    """aro cian que late alrededor de un campo"""
    k = (math.sin(t * 6.0) + 1) / 2
    x0, y0, x1, y1 = box
    for i, (g, a) in enumerate(((12 + 6 * k, 70), (6, 255))):
        rr(d, (x0 - g, y0 - g, x1 + g, y1 + g), r + g, outline=color + (a,), width=6 if i else 10)

def toque(d, xy, t):
    """círculo de toque con ondas (t: segundos desde el toque; <0 = aún no)"""
    x, y = xy
    if t < 0 or t > 1.2: return
    for k, ret in enumerate((0, .18)):
        u = clamp((t - ret) / .8)
        if u <= 0 or u >= 1: continue
        r = 40 + 80 * easeout(u)
        d.ellipse((S(x - r), S(y - r), S(x + r), S(y + r)), outline=(255, 255, 255, int(220 * (1 - u))), width=S(8))
    u = clamp(t / .15); r = 34 * (1 - .25 * math.sin(math.pi * clamp(t / .35)))
    d.ellipse((S(x - r), S(y - r), S(x + r), S(y + r)), fill=(255, 255, 255, int(235 * u * (1 - clamp((t - .5) / .7)))))

def dedo(d, xy, a=255):
    """puntero: círculo translúcido con el dedo (simplificado)"""
    x, y = xy
    d.ellipse((S(x - 38), S(y - 38), S(x + 38), S(y + 38)), fill=(0, 64, 160, int(110 * a / 255)), outline=(255, 255, 255, a), width=S(6))
    d.ellipse((S(x - 12), S(y - 12), S(x + 12), S(y + 12)), fill=(255, 255, 255, a))

def etiqueta_toca(d, xy, texto, t, lado="izq"):
    f = font(COOL, 40)
    w = d.textlength(texto, font=f) / SS + 56
    x, y = xy
    k = back(clamp(t / .35)); y += 10 * math.sin(t * 5)
    if k <= 0: return
    x0 = x - w if lado == "izq" else x
    box = (x0, y - 40 * k, x0 + w, y + 40 * k)
    rr(d, box, 40, fill=CYAN + (255,))
    tx(d, ((box[0] + box[2]) / 2, y), texto, f, NAVYD, "mm")

# --------------------------------------------------------------------------- formulario
def dibuja_campo_select(d, y, campo, valor, activo):
    tx(d, (46, y), ETIQ[campo], font(ARIALB, 34), INK)
    box = (46, y + 52, CW - 46, y + 162)
    rr(d, box, 24, fill=(255, 255, 255, 255), outline=LINE + (255,), width=3)
    if valor:
        tx(d, (78, y + 107), valor, font(ARIAL, 38), INK, "lm")
    else:
        tx(d, (78, y + 107), "Selecciona…", font(ARIAL, 38), (120, 135, 160), "lm")
    # chevron
    cx, cy = CW - 92, y + 107
    d.line([(S(cx - 12), S(cy - 6)), (S(cx), S(cy + 8)), (S(cx + 12), S(cy - 6))], fill=INK, width=S(5), joint="curve")
    return box

def dibuja_input(d, box, texto, ph, activo, cursor):
    rr(d, box, 22, fill=(255, 255, 255, 255), outline=LINE + (255,), width=3)
    if texto:
        tx(d, (box[0] + 24, (box[1] + box[3]) / 2), texto + ("|" if cursor else ""), font(ARIAL, 40), INK, "lm")
    else:
        tx(d, (box[0] + 24, (box[1] + box[3]) / 2), ph + ("" if not cursor else ""), font(ARIAL, 38), (120, 135, 160), "lm")
        if cursor: tx(d, (box[0] + 24, (box[1] + box[3]) / 2), "|", font(ARIAL, 40), INK, "lm")

def estado(i, t):
    """qué hay escrito/elegido en el formulario en la escena i, tiempo t -> dict valores + animaciones"""
    e = ESCENAS[i]; c = e.get("campo"); st = dict(sel={}, med=["", "", ""], ciu="", nom="", foto=False, abierto=None,
                                                  opc_hover=None, activo=None, wa=0, tap=None)
    # valores finales de escenas anteriores
    for j in range(1, i):
        k = ESCENAS[j].get("campo")
        if k in ELIGE: st["sel"][k] = OPC[k][ELIGE[k]]
        elif k == "med": st["med"] = list(VALOR["med"])
        elif k == "ciu": st["ciu"] = VALOR["ciu"]
        elif k == "nom": st["nom"] = VALOR["nom"]
        elif k == "foto": st["foto"] = True
    st["activo"] = c
    dur = e["dur"]
    if c in ELIGE:
        cfg = CFG[c]; t_open, t_pick = cfg["open"], cfg["pick"]
        st["t_open"], st["t_pick"], st["cfg"] = t_open, t_pick, cfg
        if t_open < t < t_pick + .5: st["abierto"] = c; st["abre_t"] = t - t_open
        if t > t_pick + .35: st["sel"][c] = OPC[c][ELIGE[c]]
        hv = None
        for (a0, a1, n) in cfg["hov"]:
            if a0 <= t < a1: hv = n
        if hv is None and t > t_pick - .5: hv = ELIGE[c]
        st["opc_hover"] = hv
    elif c == "med":
        for n in range(3):
            a = [3.3, 4.2, 5.0][n]
            v = VALOR["med"][n]; k = clamp((t - a) / .6)
            st["med"][n] = v[:int(len(v) * k + .0001)] if t > a else ""
        st["med_n"] = 0 if t < 4.1 else 1 if t < 4.9 else 2
    elif c == "ciu":
        k = clamp((t - 2.0) / 2.2); v = VALOR["ciu"]; st["ciu"] = v[:int(len(v) * k)]
    elif c == "nom":
        k = clamp((t - 2.0) / 1.0); v = VALOR["nom"]; st["nom"] = v[:int(len(v) * k)]
    elif c == "foto":
        st["foto"] = t > 2.5
    elif c == "enviar":
        st["wa"] = 0
    return st

def formulario(i, t, sc0, sc1):
    """capa del formulario (tamaño de la tarjeta) con scroll interpolado."""
    st = estado(i, t)
    e = ESCENAS[i]; dur = e["dur"]
    k = ease(t / 0.9)
    sc = sc0 + (sc1 - sc0) * k
    im = Image.new("RGBA", (S(CW), S(CH)), (255, 255, 255, 255))
    d = ImageDraw.Draw(im, "RGBA")
    oy = -sc
    # contenido desplazable: se dibuja en una capa alta y se recorta
    cap = Image.new("RGBA", (S(CW), S(ALTO_FORM + CH)), (255, 255, 255, 255)); dd = ImageDraw.Draw(cap, "RGBA")
    tx(dd, (46, 50), "Pide tu cotización", font(COOL, 58), INK)
    tx(dd, (46, 118), "Menos de un minuto. Con lo que sepas es suficiente.", font(ARIAL, 28), MUTED)
    cajas = {}
    for campo in ("que", "tipo", "temp"):
        cajas[campo] = dibuja_campo_select(dd, POS[campo], campo, st["sel"].get(campo), st["activo"] == campo)
    # medidas
    y = POS["med"]
    tx(dd, (46, y), "Medidas aproximadas en metros", font(ARIALB, 34), INK)
    tx(dd, (46 + 540, y + 4), "(si las sabes)", font(ARIAL, 30), MUTED)
    bw = (CW - 92 - 40) / 3
    mb = []
    for n, nombre in enumerate(("Largo", "Ancho", "Alto")):
        b = (46 + n * (bw + 20), y + 52, 46 + n * (bw + 20) + bw, y + 162); mb.append(b)
        cur = st["activo"] == "med" and st.get("med_n") == n and int(t * 2.5) % 2 == 0 and t > 2
        dibuja_input(dd, b, st["med"][n], nombre, False, cur)
    cajas["med"] = (46, y + 52, CW - 46, y + 162)
    # ciudad / nombre
    for campo, ph in (("ciu", "Ej: Barcelona, Anzoátegui"), ("nom", "¿Cómo te llamas?")):
        y = POS[campo]
        tx(dd, (46, y), ETIQ[campo], font(ARIALB, 34), INK)
        b = (46, y + 52, CW - 46, y + 162); cajas[campo] = b
        cur = st["activo"] == campo and t > 1.8 and int(t * 2.5) % 2 == 0 and len(st[campo]) < len(VALOR[campo])
        dibuja_input(dd, b, st[campo], ph, False, cur or (st["activo"] == campo and t > 1.8 and st[campo] != "" and int(t * 2.5) % 2 == 0))
    # casilla foto
    y = POS["foto"]
    cb = (46, y + 6, 46 + 64, y + 70)
    rr(dd, cb, 14, fill=(255, 255, 255, 255), outline=LINE + (255,) if not st["foto"] else NAVY + (255,), width=4)
    if st["foto"]:
        rr(dd, cb, 14, fill=NAVY + (255,))
        ck = clamp((t - 2.5) / .3) if st["activo"] == "foto" else 1.0
        pts = [(cb[0] + 14, cb[1] + 34), (cb[0] + 28, cb[1] + 48), (cb[0] + 52, cb[1] + 18)]
        dd.line([(S(p[0]), S(p[1])) for p in pts[:2 if ck < .5 else 3]], fill=WHITE, width=S(8), joint="curve")
    tx(dd, (140, y + 38), "Te enviaré una foto del espacio por WhatsApp", font(ARIAL, 31), INK, "lm")
    cajas["foto"] = cb
    # botón
    y = POS["enviar"]
    bb = (46, y, CW - 46, y + 130); cajas["enviar"] = bb
    pulsa = 1 + .02 * math.sin(t * 6) if st["activo"] == "enviar" else 1
    rr(dd, bb, 40, fill=GREEN + (255,))
    tx(dd, ((bb[0] + bb[2]) / 2 + 30, y + 65), "Enviar por WhatsApp", font(ARIALB, 44), (4, 54, 26), "mm")
    wi = (bb[0] + bb[2]) / 2 - 250
    dd.ellipse((S(wi - 22), S(y + 43), S(wi + 22), S(y + 87)), outline=(4, 54, 26), width=S(5))
    # --- overlays de escena sobre la capa (anillo, lista desplegable)
    ov = Image.new("RGBA", cap.size, (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    c = e.get("campo")
    if c and t > .9:
        box = cajas[c] if c != "med" else mb[st.get("med_n", 0)]
        if c == "foto": box = (cb[0] - 8, cb[1] - 8, 46 + 64 + 8 + 760, cb[3] + 8)
        anillo(od, box, 24, t)
    abierto = st["abierto"]
    if abierto:
        ko = back(clamp(st["abre_t"] / .4))
        b = cajas[abierto]; opts = OPC[abierto]
        vis = opts
        ih = 92; lh = ih * len(vis)
        top = b[3] + 10
        panel = (b[0], top, b[2], top + lh * clamp(ko, 0, 1))
        sh = Image.new("RGBA", cap.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
        sd.rounded_rectangle((S(panel[0]), S(panel[1] + 10), S(panel[2]), S(panel[3] + 10)), S(20), fill=(0, 20, 60, 90))
        sh = sh.filter(ImageFilter.GaussianBlur(S(14))); ov.alpha_composite(sh)
        od = ImageDraw.Draw(ov)
        rr(od, panel, 20, fill=WHITE + (255,), outline=LINE + (255,), width=3)
        if ko > .6:
            for n, o in enumerate(vis):
                iy = top + n * ih
                hov = st["opc_hover"] == n
                if hov: rr(od, (b[0] + 8, iy + 6, b[2] - 8, iy + ih - 6), 16, fill=(213, 238, 252, 255), outline=SKY + (255,), width=3)
                tx(od, (b[0] + 36, iy + ih / 2), o, font(ARIALB if hov else ARIAL, 36), INK, "lm")
                if abierto == "temp" and n == 3 and hov:
                    pass
    cap.alpha_composite(ov)
    # recorte con scroll
    vista = cap.crop((0, S(sc), S(CW), S(sc + CH)))
    im.paste(vista, (0, 0))
    if sc > 5:      # desvanecido blanco arriba para que no se vean textos cortados
        fade = Image.new("RGBA", im.size, (0, 0, 0, 0)); fd = ImageDraw.Draw(fade)
        for yy in range(70):
            fd.rectangle((0, S(yy), im.width, S(yy + 1)), fill=(255, 255, 255, int(255 * (1 - yy / 70) ** 1.4)))
        im.alpha_composite(fade)
    # coordenadas de pantalla para toques
    def pant(x, y): return (CARD[0] + x, CARD[1] + y - sc)
    info = dict(st=st, cajas=cajas, mb=mb, pant=pant, sc=sc, cb=cb)
    return im, info

def mensaje_wa():
    return ["Hola, quiero cotizar.", "Necesito: Fabricar e instalar una cava cuarto", "Negocio: Carnicería", "Temperatura: No estoy seguro",
            "Medidas: 4 x 3 x 2.5 m", "Ciudad: Barcelona, Anzoátegui", "Nombre: María"]

def pantalla_wa(t):
    """simulación de WhatsApp en la tarjeta (t = segundos desde que se abre). Devuelve imagen RGBA tamaño tarjeta."""
    im = Image.new("RGBA", (S(CW), S(CH)), (236, 229, 221, 255)); d = ImageDraw.Draw(im, "RGBA")
    rr(d, (0, 0, CW, 130), 0, fill=(7, 94, 84, 255))
    d.ellipse((S(34), S(26), S(110), S(102)), fill=WHITE)
    tx(d, (72, 64), "TCC", font(COOL, 30), NAVY, "mm")
    tx(d, (134, 52), "Refrigeración Team", font(ARIALB, 36), WHITE, "lm")
    tx(d, (134, 94), "en línea", font(ARIAL, 26), (200, 230, 225), "lm")
    lineas = mensaje_wa()
    enviado = clamp((t - 3.4) / .5)
    f = font(ARIAL, 31)
    bw, lh = 800, 46
    bh = lh * len(lineas) + 56
    if enviado <= 0:
        # mensaje listo en el cuadro de texto abajo
        rr(d, (24, CH - 100 - bh - 10, CW - 24, CH - 110), 24, fill=WHITE + (255,), outline=(190, 200, 205, 255), width=3)
        for n, l in enumerate(lineas):
            tx(d, (50, CH - 100 - bh + 24 + n * lh), l, f, INK)
        tx(d, (CW - 330, CH - 150), "", f, INK)
        # barra inferior con botón enviar
        rr(d, (0, CH - 100, CW, CH), 0, fill=(240, 240, 240, 255))
        rr(d, (24, CH - 84, CW - 150, CH - 18), 34, fill=WHITE + (255,))
        tx(d, (50, CH - 51), "Mensaje", font(ARIAL, 30), (150, 160, 170), "lm")
        cx, cy = CW - 80, CH - 51
        d.ellipse((S(cx - 48), S(cy - 48), S(cx + 48), S(cy + 48)), fill=(0, 168, 132, 255))
        d.polygon([(S(cx - 16), S(cy - 22)), (S(cx + 24), S(cy)), (S(cx - 16), S(cy + 22)), (S(cx - 8), S(cy))], fill=WHITE)
        if t > 0.5:
            anillo(d, (cx - 52, cy - 52, cx + 52, cy + 52), 52, t)
    else:
        # burbuja enviada
        x1 = CW - 40; x0 = x1 - bw
        y1 = 160 + bh
        rr(d, (x0, 160, x1, y1), 26, fill=(220, 248, 198, 255))
        for n, l in enumerate(lineas):
            tx(d, (x0 + 28, 186 + n * lh), l, f, INK)
        tx(d, (x1 - 26, y1 - 16), "✓✓", font(ARIALB, 28), (52, 160, 220), "rm")
        rr(d, (0, CH - 100, CW, CH), 0, fill=(240, 240, 240, 255))
        rr(d, (24, CH - 84, CW - 150, CH - 18), 34, fill=WHITE + (255,))
        tx(d, (50, CH - 51), "Mensaje", font(ARIAL, 30), (150, 160, 170), "lm")
    return im

def pantalla_fin(t):
    im = Image.new("RGBA", (S(CW), S(CH)), (255, 255, 255, 255)); d = ImageDraw.Draw(im, "RGBA")
    k = back(clamp(t / .6))
    cx, cy, r = CW / 2, 250, 150 * k
    d.ellipse((S(cx - r), S(cy - r), S(cx + r), S(cy + r)), fill=GREEN + (255,))
    ck = clamp((t - .4) / .5)
    pts = [(cx - 70, cy + 5), (cx - 20, cy + 55), (cx + 80, cy - 55)]
    if ck > 0:
        seg = pts[:2] if ck < .5 else pts
        d.line([(S(p[0]), S(p[1])) for p in seg], fill=WHITE, width=S(26), joint="curve")
    tx(d, (cx, 520), "¡Listo!", font(COOL, 120), INK, "mm")
    tx(d, (cx, 640), "Te respondemos lo antes posible", font(ARIAL, 38), MUTED, "mm")
    u = easeout(clamp((t - 3.4) / .6))
    if u > 0:
        rr(d, (80, 740, CW - 80, 920), 40, fill=ICE + (255,))
        tx(d, (cx, 790), "¿Prefieres hablar directo?", font(ARIAL, 34), MUTED, "mm")
        tx(d, (cx, 868), "0412 1856429", font(COOL, 90), NAVY, "mm")
    return im

# --------------------------------------------------------------------------- encabezado y subtítulos
def cabecera(im, i, t):
    d = ImageDraw.Draw(im, "RGBA")
    # logo + título
    lg = Image.open(LOGO).convert("RGBA"); lg.thumbnail((S(130), S(130)))
    rr(d, (50, 50, 50 + lg.width / SS + 20, 50 + lg.height / SS + 20), 28, fill=WHITE + (255,))
    im.paste(lg, (S(60), S(60)), lg)
    tx(d, (50 + lg.width / SS + 50, 90), "Cómo pedir tu cotización", font(COOL, 50), WHITE, "lm")
    tx(d, (50 + lg.width / SS + 50, 140), "Refrigeración Team Cavas Cuarto", font(ARIAL, 28), (170, 200, 240), "lm")
    # paso
    e = ESCENAS[i]
    if e["id"].startswith("p"):
        n = int(e["id"][1:])
        pop = back(clamp(t / .4))
        w = 330 * pop
        rr(d, (540 - w / 2, 200, 540 + w / 2, 200 + 96 * clamp(pop)), 48, fill=CYAN + (255,))
        if pop > .5: tx(d, (540, 248), f"PASO {n} de 8", font(COOL, 58), NAVYD, "mm")
        # puntos
        for k in range(8):
            x = 540 + (k - 3.5) * 44
            col = CYAN + (255,) if k < n else (255, 255, 255, 70)
            d.ellipse((S(x - 11), S(312 - 11 - 0), S(x + 11), S(312 + 11 - 0)), fill=col)
    elif e["id"] == "intro":
        pop = back(clamp((t - .4) / .5)); w = 640 * pop
        rr(d, (540 - w / 2, 200, 540 + w / 2, 200 + 96 * clamp(pop)), 48, fill=CYAN + (255,))
        if pop > .6: tx(d, (540, 248), "TUTORIAL · PASO A PASO", font(COOL, 48), NAVYD, "mm")

def subtitulo(im, t_abs, palabras):
    d = ImageDraw.Draw(im, "RGBA")
    # frase activa: grupos de palabras
    act = None
    for g in palabras:
        if g[0] - 0.05 <= t_abs <= g[1] + 0.25: act = g; break
    if not act: return
    f = font(COOL, 64)
    lineas = act[2]
    ancho = max(d.textlength(l, font=f) / SS for l in lineas) + 80
    alto = 86 * len(lineas) + 40
    y0 = 1560
    sombra(im, (540 - ancho / 2, y0, 540 + ancho / 2, y0 + alto), 44, alpha=70, blur=16, dy=10)
    d = ImageDraw.Draw(im, "RGBA")
    rr(d, (540 - ancho / 2, y0, 540 + ancho / 2, y0 + alto), 44, fill=(4, 20, 60, 235))
    for n, l in enumerate(lineas):
        tx(d, (540, y0 + 20 + 43 + n * 86), l, f, WHITE, "mm")

# --------------------------------------------------------------------------- frame
PALABRAS = []
def escena_en(t):
    for i, e in enumerate(ESCENAS):
        if e["t0"] <= t < e["t0"] + e["dur"]: return i
    return len(ESCENAS) - 1

def frame(t_abs):
    global BG
    if BG is None: BG = fondo()
    i = escena_en(t_abs); e = ESCENAS[i]; t = t_abs - e["t0"]; c = e.get("campo")
    im = BG.copy()
    cabecera(im, i, t)
    sombra(im, CARD, 44)
    # scroll previo -> nuevo
    prev = scroll_de(ESCENAS[i - 1].get("campo")) if i > 1 else 0
    cur = scroll_de(c) if c else 0
    if e["id"] == "intro": cur = prev = 0
    if e["id"] == "fin": cur = prev = scroll_de("enviar")
    wa_t = None
    if e["id"] == "p8":
        t_tap = 4.2; wa_t = t - (t_tap + .9)
    carta, info = formulario(i, t, prev, cur)
    if e["id"] == "intro":
        zi = ease(t / 1.2)
    if e["id"] == "p8" and wa_t is not None and wa_t > 0:
        slide = ease(clamp(wa_t / .6))
        wa = pantalla_wa(wa_t)
        carta.paste(wa, (int(S(CW) * (1 - slide)), 0))
    if e["id"] == "fin":
        carta = pantalla_fin(t)
    # máscara redondeada
    m = Image.new("L", carta.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, carta.width - 1, carta.height - 1), S(44), fill=255)
    im.paste(carta, (S(CARD[0]), S(CARD[1])), m)
    d = ImageDraw.Draw(im, "RGBA")
    # --- toques y etiquetas (coordenadas de pantalla)
    st = info["st"]; pant = info["pant"]; cj = info["cajas"]
    if c in ELIGE:
        b = cj[c]; p = pant((b[0] + b[2]) / 2 - 80, (b[1] + b[3]) / 2)
        cfg = st["cfg"]; t_open, t_pick = cfg["open"], cfg["pick"]
        if .9 < t < t_open - .4: etiqueta_toca(d, (880, p[1] - 100), "Toca aquí", t - .9, "izq")
        if t_open - .7 < t < t_open + .6: toque(d, p, t - (t_open - .4))
        q = pant(b[0] + 360, b[3] + 10 + ELIGE[c] * 92 + 46)
        if t_open + .8 < t < t_pick + .5:
            u = ease(clamp((t - (t_pick - 1.0)) / .8))
            dedo(d, (p[0] + (q[0] - p[0]) * u, p[1] + (q[1] - p[1]) * u + 30 * (1 - u) * (1 if t < t_pick - 1.0 else 0)))
        toque(d, q, t - t_pick)
        if "tag" in cfg and cfg["tag"][0] < t < cfg["tag"][1]:
            q3 = pant(b[2] - 60, b[3] + 10 + 3 * 92 + 46)
            etiqueta_toca(d, (q3[0] - 120, q3[1] + 80), "¿No sabes? Elige esta", t - cfg["tag"][0], "izq")
    elif c == "med":
        for n in range(3):
            a = 2.0 + n * 1.5
            if a - .6 < t < a + .5:
                b = info["mb"][n]; p = pant((b[0] + b[2]) / 2, (b[1] + b[3]) / 2); toque(d, p, t - (a - .6));
        b = info["mb"][0]
        if .9 < t < 2.8: etiqueta_toca(d, (880, pant(0, b[1])[1] - 80), "Toca aquí", t - .9)
        if t > 6.2:
            u = back(clamp((t - 6.2) / .4)); w = 760
            rr(d, (540 - w / 2, 1400, 540 + w / 2, 1400 + 70 * u), 35, fill=CYAN + (255,))
            if u > .6: tx(d, (540, 1415), "Si no las sabes, déjalas en blanco", font(COOL, 38), NAVYD, "mm")
    elif c in ("ciu", "nom"):
        b = cj[c]
        if .9 < t < 2.2: etiqueta_toca(d, (880, pant(0, b[1])[1] - 80), "Toca aquí", t - .9)
        if 1.5 < t < 2.4: toque(d, pant((b[0] + b[2]) / 2 - 100, (b[1] + b[3]) / 2), t - 1.5)
    elif c == "foto":
        b = info["cb"]
        if .9 < t < 2.2: etiqueta_toca(d, (880, pant(0, b[1])[1] - 80), "Toca aquí", t - .9)
        if 2.0 < t < 3.4: toque(d, pant((b[0] + b[2]) / 2, (b[1] + b[3]) / 2), t - 2.3)
        if t > 5.0:
            u = back(clamp((t - 5.0) / .4)); w = 560
            rr(d, (540 - w / 2, 1380, 540 + w / 2, 1380 + 70 * u), 35, fill=CYAN + (255,))
            if u > .6: tx(d, (540, 1415), "Es opcional", font(COOL, 40), NAVYD, "mm")
    elif c == "enviar":
        b = cj["enviar"]
        p = pant((b[0] + b[2]) / 2, (b[1] + b[3]) / 2)
        if wa_t is not None and wa_t < 0:
            if t > 1.0 and t < 3.7: etiqueta_toca(d, (880, p[1] + 110), "Toca aquí", t - 1.0)
            if 3.6 < t < 5.0: toque(d, p, t - 4.2)
        if wa_t is not None and wa_t > 0 and wa_t < 5.0:
            # WhatsApp: botón enviar abajo derecha de la tarjeta
            cx, cy = CARD[0] + CW - 80, CARD[1] + CH - 51
            if 0.8 < wa_t < 3.1: etiqueta_toca(d, (cx + 40, CARD[1] + CH - 100 - 46 * 7 - 56 - 70), "Toca enviar", wa_t - 1.2, "izq")
            if 2.9 < wa_t < 4.2: toque(d, (cx, cy), wa_t - 3.4)
    # subtítulos
    subtitulo(im, t_abs, PALABRAS)
    return im.convert("RGB").resize((W, H), Image.LANCZOS)

def init():
    cargar_tiempos(); prepara_palabras()

def trabajo(f):
    return frame(f / FPS).tobytes()

def prepara_palabras():
    p = AQUI / "audio" / "palabras_tutorial.json"
    global PALABRAS
    if not p.exists(): PALABRAS = []; return
    ws0 = json.loads(p.read_text()); ws = []
    for w in ws0:
        if w["w"].startswith("-") and ws and ws[-1]["w"][-1:].isdigit():
            ws[-1] = dict(w=ws[-1]["w"] + w["w"][1:], s=ws[-1]["s"], e=w["e"])
        else:
            ws.append(dict(w))
    import re as _re
    for w in ws:
        m = _re.fullmatch(r"(\d{4})(\d{7})([.,]?)", w["w"])
        if m: w["w"] = f"{m.group(1)} {m.group(2)}{m.group(3)}"
    grupos, act = [], []
    for w in ws:
        act.append(w)
        fin = w["w"].endswith((".", "!", "?", ":"))
        if len(act) >= 5 or fin or (len(act) >= 3 and w["w"].endswith(",")):
            grupos.append(act); act = []
    if act: grupos.append(act)
    out = []
    for g in grupos:
        txt = [x["w"] for x in g]
        if len(txt) > 3:
            m = (len(txt) + 1) // 2; lineas = [" ".join(txt[:m]), " ".join(txt[m:])]
        else:
            lineas = [" ".join(txt)]
        out.append((g[0]["s"], g[-1]["e"], lineas))
    PALABRAS = out

if __name__ == "__main__":
    total = cargar_tiempos(); prepara_palabras()
    print("duración total", round(total, 1), "s", [(e["id"], round(e["t0"], 1), round(e["dur"], 1)) for e in ESCENAS])
    if len(sys.argv) > 1 and sys.argv[1] == "--prueba":
        for s in sys.argv[2:]:
            frame(float(s)).save(AQUI / f"prueba_{float(s):06.2f}.png")
        sys.exit()
    n = int(total * FPS)
    cmd = [FFMPEG, "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "medium", str(AQUI / "video_mudo.mp4")]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    with Pool(8, initializer=init) as pool:
        for k, b in enumerate(pool.imap(trabajo, range(n), chunksize=6)):
            pr.stdin.write(b)
            if k % 150 == 0: print("frame", k, "/", n, flush=True)
    pr.stdin.close(); pr.wait()
    print("OK video_mudo.mp4")
