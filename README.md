# Refrigeración Team Cavas Cuarto (TCC) — sitio web

- `FUENTE/`: generador (`build_web.py`, `home.src.html`, `gen_mapa.py`). Salida en `SITIO/`.
- `SITIO/`: sitio estático publicado en Netlify.
- `TUTORIAL/`: scripts del video tutorial "Cómo cotizar" (el video final está en `SITIO/tutorial/`).

Reconstruir: `cd FUENTE && python3 build_web.py`
Antes de publicar con dominio: `INDEXAR=True` y `BASE` real en `build_web.py`.
