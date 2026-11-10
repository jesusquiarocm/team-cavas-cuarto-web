// Refrigeración Team: redirecciones 301, página 404 real y cabeceras de caché/seguridad.
// Cloudflare ejecuta esto antes de servir los archivos del sitio (run_worker_first).
const APEX = "cavascuartoteam.com";

export default {
  async fetch(req, env) {
    const url = new URL(req.url);

    // www -> dominio raíz y http -> https, en un solo salto permanente
    if (url.hostname === "www." + APEX || (url.hostname === APEX && url.protocol === "http:")) {
      url.hostname = APEX;
      url.protocol = "https:";
      return Response.redirect(url.toString(), 301);
    }

    // fotos: WebP (más livianas) para los navegadores que lo aceptan
    if (/^\/img\/[^/]+\.jpg$/.test(url.pathname) && (req.headers.get("Accept") || "").includes("image/webp")) {
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

    if (/^\/img\/[^/]+\.jpg$/.test(p)) h.set("Vary", "Accept");
    if (/^\/(img|video|tutorial)\//.test(p) || p === "/favicon.ico") {
      h.set("Cache-Control", "public, max-age=2592000, stale-while-revalidate=86400");
    } else if (p.startsWith("/js/")) {
      h.set("Cache-Control", "public, max-age=3600, stale-while-revalidate=86400");
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
