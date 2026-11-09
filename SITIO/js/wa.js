// Refrigeración Team: WhatsApp, medición de clics y avisos
// Imágenes: sin carga diferida en el carrusel y reintento si alguna falla
(function(){
  document.querySelectorAll('#rail img, #equipo img').forEach(function(i){ i.loading='eager'; });
  function fix(i){
    var n=+(i.dataset.r||0);
    if(n>=3) return;
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

const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }), {threshold:.12});
document.querySelectorAll(".rv").forEach(el => io.observe(el));
const yr = document.getElementById("yr"); if (yr) yr.textContent = new Date().getFullYear();
