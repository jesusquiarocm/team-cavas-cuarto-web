# Comprime las fotos de cavas para la página /galeria/.
# Toma las fotos de "VÍDEOS Y FOTOS DE CAVAS", quita repetidas y las que no van,
# y deja en SITIO/img/gal/ dos tamaños de cada una (miniatura y grande), en JPG y WebP.
# Uso: python3 FUENTE/hacer_galeria.py   (después correr build_web.py)
import hashlib, json, re
from pathlib import Path
from PIL import Image, ImageOps

AQUI = Path(__file__).resolve().parent
ORIGEN = AQUI.parent.parent / "VÍDEOS Y FOTOS DE CAVAS"
DESTINO = AQUI.parent / "SITIO" / "img" / "gal"
LISTA = AQUI / "galeria.json"

MINI = (420, 560)   # miniatura 3:4 recortada al centro
GRANDE = 1600       # lado largo de la foto ampliada
# fotos que no van (por nombre de archivo): máquinas que no son cavas, texto encima,
# carne colgada, tableros sueltos y tomas casi iguales a otra que ya está
QUITAR = {
    "WhatsApp Image 2026-05-23 at 16.49.21.jpeg", "WhatsApp Image 2026-05-23 at 16.49.22.jpeg",
    "WhatsApp Image 2026-03-26 at 5.11.34 PM.jpeg", "WhatsApp Image 2026-03-29 at 9.51.27 AM.jpeg",
    "WhatsApp Image 2026-03-29 at 9.51.28 AM.jpeg", "WhatsApp Image 2026-04-09 at 9.34.32 PM (1).jpeg",
    "WhatsApp Image 2026-04-09 at 9.34.32 PM.jpeg", "WhatsApp Image 2026-04-09 at 9.34.33 PM (1).jpeg",
    "WhatsApp Image 2026-04-09 at 9.34.33 PM (2).jpeg", "WhatsApp Image 2026-04-09 at 9.34.33 PM (3).jpeg",
    "WhatsApp Image 2026-04-09 at 9.34.33 PM.jpeg", "WhatsApp Image 2026-04-11 at 3.50.54 PM (2).jpeg",
    "WhatsApp Image 2026-04-28 at 7.08.13 AM (2).jpeg", "WhatsApp Image 2026-05-19 at 9.34.33 PM (4).jpeg",
    "WhatsApp Image 2026-07-10 at 21.32.24 (1).jpeg", "WhatsApp Image 2026-07-18 at 12.01.00.jpeg",
    "WhatsApp Image 2026-07-21 at 18.34.05 copia.jpeg", "WhatsApp Image 2026-07-21 at 18.34.06.jpeg",
    "WhatsApp Image 2026-09-07 at 18.33.55.jpeg",
}

def ahash(im):
    g = im.convert("L").resize((16, 16))
    px = list(g.getdata()); m = sum(px) / len(px)
    return int("".join("1" if p > m else "0" for p in px), 2)

def fecha(nombre):
    m = re.search(r"(\d{4})-(\d+)-(\d+) at ([\d.]+)", nombre)
    return tuple(int(x) for x in m.groups()[:3]) + (m.group(4),) if m else (0, 0, 0, nombre)

def candidatas():
    """Fotos únicas (sin copias exactas ni tomas casi idénticas), en orden de archivo."""
    fs = sorted(p for p in ORIGEN.rglob("*") if p.suffix.lower() in (".jpg", ".jpeg"))
    vistos, quedan = set(), []
    for p in fs:
        md = hashlib.md5(p.read_bytes()).hexdigest()
        if md in vistos: continue
        vistos.add(md)
        im = ImageOps.exif_transpose(Image.open(p)); h = ahash(im)
        for i, (h2, p2, area) in enumerate(quedan):
            if bin(h ^ h2).count("1") <= 12:
                if im.width * im.height > area: quedan[i] = (h, p, im.width * im.height)
                break
        else:
            quedan.append((h, p, im.width * im.height))
    return [p for _, p, _ in quedan]

def guardar(im, base):
    im.save(base.with_suffix(".jpg"), quality=72, optimize=True, progressive=True)
    im.save(base.with_suffix(".webp"), "WEBP", quality=70, method=6)

if __name__ == "__main__":
    import sys
    fotos = candidatas()
    if "--lista" in sys.argv:   # imprime el índice de cada foto, para elegir cuáles quitar
        for i, p in enumerate(fotos): print(i, p.name)
        raise SystemExit
    fotos = [p for p in fotos if p.name not in QUITAR]
    fotos.sort(key=lambda p: fecha(p.name), reverse=True)   # las más recientes primero
    DESTINO.mkdir(parents=True, exist_ok=True)
    for f in DESTINO.iterdir(): f.unlink()
    lista = []
    for n, p in enumerate(fotos, 1):
        im = ImageOps.exif_transpose(Image.open(p)).convert("RGB")   # sin datos EXIF ni GPS
        base = DESTINO / f"cava-{n:03d}"
        g = im.copy(); g.thumbnail((GRANDE, GRANDE), Image.LANCZOS); guardar(g, base)
        guardar(ImageOps.fit(im, MINI, Image.LANCZOS), DESTINO / f"cava-{n:03d}-mini")
        lista.append({"n": f"cava-{n:03d}", "w": g.width, "h": g.height, "vertical": g.height > g.width})
    LISTA.write_text(json.dumps(lista, indent=0))
    peso = lambda pat: sum(f.stat().st_size for f in DESTINO.glob(pat)) / 1024
    print(f"{len(lista)} fotos | miniaturas webp {peso('*-mini.webp'):.0f} KB | grandes webp {peso('cava-???.webp'):.0f} KB "
          f"| originales {sum(p.stat().st_size for p in fotos) / 1024:.0f} KB")
