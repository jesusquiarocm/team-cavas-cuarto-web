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
  track("cotizador");
  window.open(wa(l.join("\n")), "_blank", "noopener");
});

// galería ampliada
const lb = document.getElementById("lb");
if (lb) {
  const lbi = lb.querySelector("img");
  ["rail","equipo","galeria"].forEach(id => { const el = document.getElementById(id); if (el) el.addEventListener("click", e => {
    const im = e.target.closest("img"); if (!im) return;
    lbi.src = im.currentSrc || im.src; lbi.alt = im.alt; lb.classList.add("on");
  }); });
  lb.addEventListener("click", () => lb.classList.remove("on"));
  document.addEventListener("keydown", e => { if (e.key === "Escape") lb.classList.remove("on"); });
}


(function(){var tv=document.getElementById("tv");if(!tv)return;var v=tv.querySelector("video");
function abre(){tv.classList.add("on");if(!v.src){v.src=v.dataset.src}try{v.play()}catch(e){}try{window.track&&track("tutorial")}catch(e){}}
function cierra(){tv.classList.remove("on");v.pause()}
document.querySelectorAll("[data-tutorial]").forEach(function(b){b.addEventListener("click",abre)});
tv.addEventListener("click",function(e){if(e.target===tv||e.target.tagName==="BUTTON")cierra()});
document.addEventListener("keydown",function(e){if(e.key==="Escape")cierra()})})();

(function(){var m=document.getElementById("cobertura");if(!m)return;
if(!("IntersectionObserver"in window)){m.classList.add("go");return}
new IntersectionObserver(function(es,o){es.forEach(function(e){if(e.isIntersecting){m.classList.add("go");o.disconnect()}})},{threshold:.3}).observe(m)})();
