"""Muestra las solicitudes del cotizador y el resumen de clics guardados en la base D1 "tcc-leads" (Cloudflare).

Uso:  python3 FUENTE/ver_leads.py [dias]      (por defecto, los últimos 30 días)
Las horas están en UTC (Venezuela = UTC−4).
"""
import json
import os
import subprocess
import sys
from pathlib import Path

SITIO = Path(__file__).resolve().parent.parent / "SITIO"
ENV = dict(os.environ, PATH=str(Path.home() / ".local/node/bin") + ":" + os.environ.get("PATH", ""))
DIAS = int(sys.argv[1]) if len(sys.argv) > 1 else 30


def q(sql):
    r = subprocess.run(["npx", "--yes", "wrangler", "d1", "execute", "tcc-leads", "--remote", "--json", "--command", sql],
                       cwd=SITIO, env=ENV, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)[0]["results"]
    except Exception:
        sys.exit("No se pudo leer la base:\n" + (r.stderr or r.stdout)[-600:])


leads = q(f"SELECT creado, nombre, necesito, negocio, temperatura, largo, ancho, alto, ciudad, con_foto, pagina "
          f"FROM leads WHERE creado >= datetime('now','-{DIAS} days') ORDER BY id DESC LIMIT 100")
print(f"== Solicitudes del cotizador (últimos {DIAS} días): {len(leads)} ==")
for x in leads:
    med = "x".join(m for m in (x["largo"], x["ancho"], x["alto"]) if m) or "sin medidas"
    print(f"{x['creado']} UTC · {x['nombre'] or 'sin nombre'} · {x['ciudad'] or '—'} · {x['negocio'] or '—'} · {x['necesito'] or '—'} · "
          f"{x['temperatura'] or '—'} · {med} m{' · enviará foto' if x['con_foto'] else ''}")

print(f"\n== Clics de contacto (últimos {DIAS} días) ==")
tot = q(f"SELECT tipo, COUNT(*) AS n FROM clics WHERE creado >= datetime('now','-{DIAS} days') GROUP BY tipo ORDER BY n DESC")
print(", ".join(f"{t['tipo']}: {t['n']}" for t in tot) or "ninguno todavía")
for fila in q(f"SELECT lugar, COUNT(*) AS n FROM clics WHERE creado >= datetime('now','-{DIAS} days') GROUP BY lugar ORDER BY n DESC LIMIT 8"):
    print(f"  botón «{fila['lugar']}»: {fila['n']}")
print("Páginas desde donde más contactan:")
for fila in q(f"SELECT pagina, COUNT(*) AS n FROM clics WHERE creado >= datetime('now','-{DIAS} days') GROUP BY pagina ORDER BY n DESC LIMIT 8"):
    print(f"  {fila['pagina']}: {fila['n']}")
