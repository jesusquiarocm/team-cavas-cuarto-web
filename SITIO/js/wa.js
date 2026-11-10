// Refrigeración Team: WhatsApp, medición de clics y avisos
// Imágenes: reintento si alguna falla al cargar
(function(){
  function fix(i){
    var n=+(i.dataset.r||0);
    var a=i.getAttribute('src');
    if(n>=3 || !a || a.indexOf('/img/')!==0 && a.indexOf('/img/')<0) return;
    i.dataset.r=n+1;
    var u=i.currentSrc||i.src; u=u.split('?')[0];
    setTimeout(function(){ i.src=u+'?r='+Date.now(); }, 600*(n+1));
  }
  document.addEventListener('error', function(e){ if(e.target && e.target.tagName==='IMG') fix(e.target); }, true);
  window.addEventListener('load', function(){
    document.querySelectorAll('img').forEach(function(i){ if(i.complete && i.naturalWidth===0) fix(i); });
  });
})();
const WHATSAPP = "584121856429";   // país + número, sin + ni espacios
const wa = t => "https://wa.me/" + WHATSAPP + "?text=" + encodeURIComponent(t + "\n\n(web: " + location.pathname + ")");
function track(lugar){
  try{
    window.dataLayer = window.dataLayer || [];
    dataLayer.push({event:"whatsapp_click", lugar});
    if (window.gtag) gtag("event","whatsapp_click",{lugar});
    if (window.fbq) fbq("track","Contact",{lugar});
  }catch(e){}
}
document.querySelectorAll("[data-wa]").forEach(a => {
  a.href = wa(a.dataset.wa); a.target = "_blank"; a.rel = "noopener";
  a.addEventListener("click", () => track(a.dataset.lugar || (a.className.split(" ").pop() || "enlace")));
});
document.querySelectorAll('a[href^="tel:"]').forEach(a => a.addEventListener("click", () => track((a.dataset.lugar || "llamada"))));

// aviso flotante tras unos segundos (una vez por visita)
try{
  if (!sessionStorage.getItem("nudge")) setTimeout(() => {
    const n = document.createElement("div"); n.className = "nudge";
    n.innerHTML = '<button aria-label="Cerrar">×</button>¿Quieres cotizar tu cava cuarto?<small>Escríbenos por WhatsApp, te respondemos con gusto.</small>';
    document.body.appendChild(n); requestAnimationFrame(() => n.classList.add("on"));
    const cerrar = () => { n.classList.remove("on"); try{sessionStorage.setItem("nudge","1")}catch(e){} };
    n.querySelector("button").addEventListener("click", e => { e.stopPropagation(); cerrar(); });
    n.addEventListener("click", () => { track("aviso"); window.open(wa("Hola, quiero cotizar una cava cuarto."), "_blank", "noopener"); cerrar(); });
    setTimeout(cerrar, 14000);
  }, 8000);
}catch(e){}

// menú en el celular
const hd = document.querySelector("header"), mb = document.querySelector(".menu-btn");
if (hd && mb) {
  const set = on => { hd.classList.toggle("open", on); mb.setAttribute("aria-expanded", on); mb.setAttribute("aria-label", on ? "Cerrar menú" : "Abrir menú"); };
  mb.addEventListener("click", () => set(!hd.classList.contains("open")));
  hd.querySelectorAll("nav a").forEach(a => a.addEventListener("click", () => set(false)));
  document.addEventListener("keydown", e => { if (e.key === "Escape") set(false); });
}
// submenús: se abren al pasar el mouse (escritorio) o con la flecha (celular y teclado)
const cierraSub = (salvo) => document.querySelectorAll(".dd.open").forEach(d => { if (d !== salvo) { d.classList.remove("open"); d.querySelector(".dd-t").setAttribute("aria-expanded", false); } });
document.querySelectorAll(".dd-t").forEach(b => b.addEventListener("click", e => {
  e.stopPropagation();
  const li = b.parentElement, on = !li.classList.contains("open");
  cierraSub(li); li.classList.toggle("open", on); b.setAttribute("aria-expanded", on);
}));
document.addEventListener("click", e => { if (!e.target.closest(".dd")) cierraSub(); });
document.addEventListener("keydown", e => { if (e.key === "Escape") cierraSub(); });

const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }), {threshold:.12});
document.querySelectorAll(".rv").forEach(el => io.observe(el));
const yr = document.getElementById("yr"); if (yr) yr.textContent = new Date().getFullYear();
