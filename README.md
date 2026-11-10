# Refrigeración Team Cavas Cuarto (TCC) — sitio web

Publicado en https://cavascuartoteam.com (dominio, DNS y alojamiento en Cloudflare).

- `FUENTE/`: generador del sitio (`build_web.py`, `home.src.html`, `sitio.js`, `gen_mapa.py`, `hacer_galeria.py`). Salida en `SITIO/`.
- `SITIO/`: sitio estático servido por Cloudflare Workers (assets). `worker.js` hace las redirecciones 301 (www/http → https://cavascuartoteam.com), caché, cabeceras de seguridad y entrega WebP a los navegadores que lo aceptan (las imágenes para compartir `og*.jpg` van siempre en JPG). Configuración en `wrangler.jsonc`; `.assetsignore` evita publicar archivos internos.
- `TUTORIAL/`: scripts del video tutorial "Cómo cotizar" (el video final está en `SITIO/tutorial/`).

## Actualizar el sitio
1. Fotos nuevas de la galería: `python3 FUENTE/hacer_galeria.py`
2. Mapa: `cd FUENTE && python3 gen_mapa.py`
3. Generar: `python3 FUENTE/build_web.py` (también crea el sitemap, robots.txt y una imagen para compartir por página: `SITIO/img/og-<página>.jpg`)
4. Publicar: `cd SITIO && npx wrangler deploy`

Supabase todavía no se usa: el cotizador arma el mensaje y abre WhatsApp, sin guardar datos.
