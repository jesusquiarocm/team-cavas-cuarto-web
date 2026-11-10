// Refrigeración Team: redirecciones 301, página 404 real, cabeceras de caché/seguridad
// y la API que guarda solicitudes del cotizador y clics de contacto en D1 (binding DB, base "tcc-leads").
// Cloudflare ejecuta esto antes de servir los archivos del sitio (run_worker_first).
const APEX = "cavascuartoteam.com";

// ------------------------------------------------------------------ API: /api/lead y /api/clic
const API_H = { "Content-Type": "application/json", "Cache-Control": "no-store", "X-Content-Type-Options": "nosniff" };
const resp = (status, ok = false) => new Response(JSON.stringify({ ok }), { status, headers: API_H });
const limpio = (v, n) => String(v ?? "").replace(/[\u0000-\u001f\u007f]/g, " ").replace(/\s+/g, " ").trim().slice(0, n);

// huella: hash corto de IP + fecha (no se guarda la IP; sirve solo para frenar spam y cambia cada día)
async function huella(req) {
  const ip = req.headers.get("CF-Connecting-IP") || "";
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(ip + "|" + new Date().toISOString().slice(0, 10)));
  return [...new Uint8Array(buf).slice(0, 8)].map(b => b.toString(16).padStart(2, "0")).join("");
}

async function api(req, env, url) {
  if (req.method !== "POST") return resp(405);
  if (req.headers.get("Origin") !== "https://" + APEX) return resp(403);          // solo desde la propia web
  const crudo = await req.text();
  if (crudo.length > 4000) return resp(413);
  let d;
  try { d = JSON.parse(crudo); } catch { return resp(400); }
  if (!d || typeof d !== "object") return resp(400);
  if (!env.DB) return resp(503);
  const h = await huella(req);
  const pais = limpio(req.cf && req.cf.country, 2);
  const pagina = /^\/[a-z0-9\-\/]*$/.test(d.pagina || "") ? String(d.pagina).slice(0, 80) : "/";
  try {
    if (url.pathname === "/api/clic") {
      const tipo = ["whatsapp", "llamada", "cotizador"].includes(d.tipo) ? d.tipo : "whatsapp";
      const { n } = await env.DB.prepare("SELECT COUNT(*) AS n FROM clics WHERE huella = ? AND creado > datetime('now','-10 minutes')").bind(h).first();
      if (n >= 60) return resp(429);
      await env.DB.prepare("INSERT INTO clics (tipo, lugar, pagina, pais, huella) VALUES (?,?,?,?,?)").bind(tipo, limpio(d.lugar, 40), pagina, pais, h).run();
      return resp(200, true);
    }
    // /api/lead: campo trampa "web" (los bots lo llenan) y mínimo de tiempo desde que se cargó la página
    if (limpio(d.web, 50) || (Number(d.ms) || 0) < 1500) return resp(200, true);      // se descarta en silencio
    const campos = { nombre: 60, necesito: 80, negocio: 60, temperatura: 40, largo: 10, ancho: 10, alto: 10, ciudad: 80 };
    const v = {};
    for (const [k, max] of Object.entries(campos)) v[k] = limpio(d[k], max);
    if (!Object.values(v).some(Boolean)) return resp(200, true);                       // formulario vacío: nada que guardar
    const { n } = await env.DB.prepare("SELECT COUNT(*) AS n FROM leads WHERE huella = ? AND creado > datetime('now','-10 minutes')").bind(h).first();
    if (n >= 5) return resp(429);
    await env.DB.prepare("INSERT INTO leads (nombre, necesito, negocio, temperatura, largo, ancho, alto, ciudad, con_foto, pagina, pais, huella) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)")
      .bind(v.nombre, v.necesito, v.negocio, v.temperatura, v.largo, v.ancho, v.alto, v.ciudad, d.foto ? 1 : 0, pagina, pais, h).run();
    return resp(200, true);
  } catch (e) {
    return resp(500);
  }
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);

    // www -> dominio raíz y http -> https, en un solo salto permanente
    if (url.hostname === "www." + APEX || (url.hostname === APEX && url.protocol === "http:")) {
      url.hostname = APEX;
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }

    if (url.pathname === "/api/lead" || url.pathname === "/api/clic") return api(req, env, url);

    // fotos: WebP (más livianas) para los navegadores que lo aceptan
    // las imágenes para compartir (og*.jpg) van siempre en JPG: algunos lectores de enlaces no aceptan WebP
    if (/^\/img\/(gal\/)?(?!og)[^/]+\.jpg$/.test(url.pathname) &&(req.headers.get("Accept") || "").includes("image/webp")) {
      const w = await env.ASSETS.fetch(new Request(url.origin + url.pathname.replace(/\.jpg$/, ".webp"), req));
      if (w.ok) {
        const r = new Response(w.body, w);
        r.headers.set("Content-Type", "image/webp");
        r.headers.set("Vary", "Accept");
        r.headers.set("Cache-Control", "public, max-age=2592000, stale-while-revalidate=86400");
        r.headers.set("X-Content-Type-Options", "nosniff");
        return r;
      }
    }

    let res = await env.ASSETS.fetch(req);

    // las redirecciones automáticas (/index.html, barra final) pasan a ser permanentes
    if (res.status === 307 || res.status === 308) {
      return new Response(null, { status: 301, headers: { Location: res.headers.get("Location") } });
    }

    const p = url.pathname;
    // /404 no debe responder 200
    const status = p === "/404" ? 404 : res.status;
    res = new Response(res.body, { status, statusText: res.statusText, headers: res.headers });
    const h = res.headers;

    if (/^\/img\/(gal\/)?(?!og)[^/]+\.jpg$/.test(p)) h.set("Vary", "Accept");
    if (/^\/(img|video|tutorial)\//.test(p) || p === "/favicon.ico") {
      h.set("Cache-Control", "public, max-age=2592000, stale-while-revalidate=86400");
    } else if (p.startsWith("/fonts/")) {
      h.set("Cache-Control", "public, max-age=31536000, immutable");
    } else if (p.startsWith("/js/")) {
      // las páginas piden /js/x.js?v=<versión>, así que se puede guardar 30 días
      h.set("Cache-Control", url.search ? "public, max-age=2592000, immutable" : "public, max-age=3600");
    }
    if ((h.get("Content-Type") || "").startsWith("text/html")) {
      h.set("Content-Type", "text/html; charset=utf-8");
    }
    h.set("Strict-Transport-Security", "max-age=31536000");
    h.set("X-Content-Type-Options", "nosniff");
    h.set("Referrer-Policy", "strict-origin-when-cross-origin");
    return res;
  },
};
