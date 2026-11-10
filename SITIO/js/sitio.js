const NEGOCIO = "Refrigeración Team";

// video de fondo del hero: solo en pantallas grandes, sin ahorro de datos, y después de cargar la página
(function(){
  const v = document.querySelector(".hero-bg"); if (!v) return;
  const c = navigator.connection || {};
  if (matchMedia("(max-width:860px)").matches || matchMedia("(prefers-reduced-motion:reduce)").matches || c.saveData || /2g/.test(c.effectiveType || "")) return;
  const go = () => {
    v.src = v.dataset.src;
    v.addEventListener("playing", () => v.classList.add("on"), {once:true});
    v.play().catch(() => {});
    new IntersectionObserver(es => es.forEach(e => e.isIntersecting ? v.play().catch(() => {}) : v.pause())).observe(v.parentElement);
  };
  const idle = window.requestIdleCallback || (f => setTimeout(f, 1200));
  if (document.readyState === "complete") idle(go); else addEventListener("load", () => idle(go));
})();

// cotizador -> mensaje de WhatsApp
const fq = document.getElementById("f");
if (fq) fq.addEventListener("submit", e => {
  e.preventDefault();
  const v = id => document.getElementById(id).value.trim();
  const med = [v("l"), v("a"), v("h")];
  const l = ["Hola " + NEGOCIO + ", quiero cotizar una cava cuarto."];
  if (v("nom"))  l.push("Nombre: " + v("nom"));
  if (v("que"))  l.push("Necesito: " + v("que"));
  if (v("tipo")) l.push("Negocio: " + v("tipo"));
  if (v("temp")) l.push("Temperatura: " + v("temp"));
  if (med.some(Boolean)) l.push("Medidas aprox. (largo x ancho x alto, m): " + med.map(x => x || "?").join(" x "));
  else l.push("Medidas: aún no las sé, necesito orientación.");
  if (v("ciu"))  l.push("Ubicación: " + v("ciu"));
  if (document.getElementById("foto").checked) l.push("Te enviaré una foto del espacio por aquí.");
  track("cotizador", "cotizador");
  // guardamos la solicitud (sin esperar la respuesta: WhatsApp se abre igual aunque falle)
  beacon("/api/lead", {nombre: v("nom"), necesito: v("que"), negocio: v("tipo"), temperatura: v("temp"), largo: v("l"), ancho: v("a"), alto: v("h"),
    ciudad: v("ciu"), foto: document.getElementById("foto").checked, web: v("web"), ms: Math.round(performance.now()), pagina: location.pathname});
  window.open(wa(l.join("\n")), "_blank", "noopener");
});

// galería ampliada: data-full trae la foto grande; con flechas se pasa a la siguiente
const lb = document.getElementById("lb");
if (lb) {
  const lbi = lb.querySelector("img"), cap = lb.querySelector(".lb-c");
  let fotos = [], i = 0;
  const muestra = n => {
    i = (n + fotos.length) % fotos.length; const im = fotos[i];
    lbi.src = im.dataset.full || im.currentSrc || im.src; lbi.alt = im.alt;
    if (cap) cap.textContent = (i + 1) + " / " + fotos.length;
    const sig = fotos[(i + 1) % fotos.length]; if (sig.dataset.full) new Image().src = sig.dataset.full;
  };
  ["rail","equipo","galeria","fotos"].forEach(id => { const el = document.getElementById(id); if (el) el.addEventListener("click", e => {
    const im = e.target.closest("img"); if (!im) return;
    fotos = [...el.querySelectorAll("img")]; lb.classList.toggle("solo", fotos.length < 2);
    muestra(fotos.indexOf(im)); lb.classList.add("on");
  }); });
  const cierra = () => { lb.classList.remove("on"); lbi.removeAttribute("src"); };
  lb.addEventListener("click", e => {
    if (e.target.closest(".lb-p")) muestra(i - 1); else if (e.target.closest(".lb-n")) muestra(i + 1);
    else if (e.target !== lbi || window.innerWidth < 700) cierra();
  });
  document.addEventListener("keydown", e => {
    if (!lb.classList.contains("on")) return;
    if (e.key === "Escape") cierra(); else if (e.key === "ArrowLeft") muestra(i - 1); else if (e.key === "ArrowRight") muestra(i + 1);
  });
  let x0 = null;   // deslizar con el dedo
  lb.addEventListener("touchstart", e => { x0 = e.touches[0].clientX; }, {passive: true});
  lb.addEventListener("touchend", e => { if (x0 === null) return; const dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 50) { e.preventDefault(); muestra(dx < 0 ? i + 1 : i - 1); } });
}


(function(){var tv=document.getElementById("tv");if(!tv)return;var v=tv.querySelector("video");
function abre(){tv.classList.add("on");if(!v.src){v.src=v.dataset.src}try{v.play()}catch(e){}try{window.track&&track("tutorial")}catch(e){}}
function cierra(){tv.classList.remove("on");v.pause()}
document.querySelectorAll("[data-tutorial]").forEach(function(b){b.addEventListener("click",abre)});
tv.addEventListener("click",function(e){if(e.target===tv||e.target.tagName==="BUTTON")cierra()});
document.addEventListener("keydown",function(e){if(e.key==="Escape")cierra()})})();

// temperaturas: al aparecer, el fondo pasa de celeste a azul oscuro mientras cuentan los grados y caen copos desde arriba
(function(){
  const s = document.getElementById("temperaturas");
  if (!s || !("IntersectionObserver" in window) || matchMedia("(prefers-reduced-motion:reduce)").matches) return;
  const nums = [...s.querySelectorAll(".temp .big")].map(el => {
    const m = el.textContent.match(/^(.*?)([−-]?)(\d+)(\s*°C)$/);
    return m && {el, pre: m[1], neg: m[2], fin: +m[3], suf: m[4]};
  }).filter(Boolean);
  const pinta = (n, v) => { n.el.textContent = n.pre + (v ? n.neg : "") + v + n.suf; };
  s.classList.add("t-anim"); nums.forEach(n => pinta(n, 0));
  const DUR = 2800;
  const nieva = () => {
    const c = document.createElement("div"); c.className = "copos"; c.setAttribute("aria-hidden", "true");
    const h = s.offsetHeight + 40, cant = innerWidth < 700 ? 16 : 30;
    for (let k = 0; k < cant; k++) {
      const f = document.createElement("span"); f.className = "copo";
      const t = 6 + Math.random() * 10;   // tamaño en px
      f.style.cssText = `left:${Math.random() * 100}%;--s:${t}px;--o:${(.35 + t / 30).toFixed(2)};--h:${h}px;` +
        `--x:${Math.round(Math.random() * 80 - 40)}px;--d:${(12 + Math.random() * 10).toFixed(1)}s;--w:${(k / cant * 6 + Math.random() * .6).toFixed(1)}s`;
      c.appendChild(f);
    }
    s.prepend(c);
  };
  const empieza = () => {
    s.classList.add("frio");
    const t0 = performance.now();
    const paso = t => {
      const p = Math.min(1, (t - t0) / DUR), e = p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;   // mismo ritmo que el fondo
      nums.forEach(n => pinta(n, Math.round(n.fin * e)));
      if (p < 1) requestAnimationFrame(paso);
    };
    requestAnimationFrame(paso);
    nieva();   // los copos empiezan a caer de a poco desde arriba, junto con el frío
  };
  let hecho = false;
  new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting && !hecho && e.intersectionRatio >= .3) { hecho = true; empieza(); }
    s.classList.toggle("quieto", !e.isIntersecting);   // los copos se pausan fuera de pantalla
  }), {threshold: [0, .3]}).observe(s);
})();

(function(){var m=document.getElementById("cobertura");if(!m)return;
if(!("IntersectionObserver"in window)){m.classList.add("go");return}
new IntersectionObserver(function(es,o){es.forEach(function(e){if(e.isIntersecting){m.classList.add("go");o.disconnect()}})},{threshold:.3}).observe(m)})();
