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

## Solicitudes y clics (D1 de Cloudflare)
- El cotizador y los botones de WhatsApp/llamada guardan sus datos en la base **D1 `tcc-leads`** (misma cuenta de Cloudflare, plan gratuito, sin pausas). WhatsApp se abre igual aunque el guardado falle.
- API en `SITIO/worker.js`: `POST /api/lead` y `POST /api/clic` (solo desde cavascuartoteam.com; campo trampa, tiempo mínimo, validación y límite de 5 solicitudes / 60 clics cada 10 min por visitante). No se guarda la IP: solo un hash que cambia cada día.
- Esquema en `FUENTE/schema.sql` (aplicar con `cd SITIO && npx wrangler d1 execute tcc-leads --remote --file ../FUENTE/schema.sql`).
- Ver lo guardado: `python3 FUENTE/ver_leads.py [días]` o el panel de Cloudflare → Workers & Pages → D1 → tcc-leads.
- Supabase no hace falta (su plan gratuito permite 2 proyectos activos y ya están ocupados).
