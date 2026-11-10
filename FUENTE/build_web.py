#!/usr/bin/env python3
"""Genera el sitio de Refrigeración Team en ../SITIO a partir de home.src.html.

Uso:  python3 build_web.py
Al publicar con dominio real: INDEXAR = True y BASE = "https://tudominio.com", correr de nuevo.
"""
import html, json, re, datetime, hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

INDEXAR=True
BASE="https://cavascuartoteam.com"
WHATSAPP = "584121856429"
HOY = datetime.date.today().isoformat()
GA_ID = ""      # ej. "G-XXXXXXXXXX" (Google Analytics 4); vacío = sin analítica
PIXEL_ID = ""   # ej. "1234567890" (Meta Pixel); vacío = sin píxel
TOPBAR = '<div class="topbar">Cotización gratis por WhatsApp · <a href="tel:+584121856429" data-lugar="topbar-llamar">0412 1856429</a></div>'

AQUI = Path(__file__).parent
SITIO = AQUI.parent / "SITIO"

ICON_COMPRESOR = '<svg viewBox="0 0 120 120" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="24" y="48" width="72" height="42" rx="10"/><path d="M40 48V34h16v14M72 48V28h14v20"/><circle cx="60" cy="69" r="12"/><path d="M60 61v16M52 69h16M34 90v8M86 90v8"/></svg>'
ICON_LUCES = '<svg viewBox="0 0 120 120" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M60 20a24 24 0 0 0-12 45v9h24v-9a24 24 0 0 0-12-45z"/><path d="M50 84h20M54 94h12"/><circle cx="92" cy="34" r="0"/><path d="M18 36l8 4M102 36l-8 4M60 6v6"/></svg>'
ICON_FREEZER = '<svg viewBox="0 0 120 120" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="18" y="54" width="84" height="44" rx="8"/><path d="M18 66h84M26 54l8-14h52l8 14M52 82h16"/><path d="M60 14v18M52 20l8 8 8-8M46 36l28 0" /></svg>'

# ---------------------------------------------------------------- páginas
PAGES = [
 dict(slug="cavas-cuarto-carniceria", nombre="Carnicerías", img="c88", imgalt="Cava cuarto de carnicería con reses colgadas",
  title="Cava cuarto para carnicería en Venezuela | Refrigeración Team",
  desc="Fabricamos e instalamos cavas cuarto para carnicerías en toda Venezuela: refrigeración para cortes frescos y congelación para almacenar. Cotiza por WhatsApp.",
  h1="Cava cuarto para carnicería, hecha a tu medida",
  intro="Tu carne necesita frío constante desde que llega hasta que se vende. Diseñamos, fabricamos e instalamos la cava cuarto de tu carnicería según el espacio que tienes y el volumen que manejas.",
  ben=[("Cortes frescos, siempre en su punto","Una cava de refrigeración mantiene la carne entre 0 y 5 °C para que el producto llegue bien al mostrador."),
       ("Espacio para colgar y almacenar","Pensamos la distribución según cómo trabajas: reses, cortes en bandejas o cajas."),
       ("Menos pérdidas, más ganancia","Con el frío estable, el producto dura más y reduces lo que se daña.")],
  temp=("Refrigeración o congelación","Para vender en pocos días, lo habitual es la refrigeración (0 a 5 °C). Para guardar por más tiempo, la congelación (−18 °C). Si manejas ambas, podemos hacer dos cavas o una combinada."),
  items=["Reses y medias reses","Cortes frescos","Embutidos","Pollo","Carne congelada"],
  faq=[("¿Qué temperatura necesita una cava para carnicería?","Para carne fresca, entre 0 y 5 °C. Para almacenar por más tiempo, unos −18 °C. Te orientamos según lo que vendes."),
       ("¿Puedo colgar la carne dentro de la cava?","Sí. La estructura interior se diseña según cómo trabajes: ganchos, rieles, estantes o bandejas."),
       ("¿Hacen la cava del tamaño de mi local?","Sí, cada cava se fabrica a la medida de tu espacio. Cuéntanos las medidas por WhatsApp.")],
  wa="Hola, tengo una carnicería y quiero cotizar una cava cuarto.", rel=["cuarto-de-refrigeracion","cuarto-de-congelacion","cuartos-frios-pescaderia"]),

 dict(slug="cuartos-frios-pescaderia", nombre="Pescaderías", img="c85", imgalt="Procesamiento de pescado en una planta con cuarto frío",
  title="Cuarto frío para pescadería y mariscos en Venezuela | Refrigeración Team",
  desc="Cuartos fríos para pescaderías, mariscos y procesadoras en Venezuela. Diseño, fabricación e instalación a tu medida. Cotiza por WhatsApp.",
  h1="Cuarto frío para pescadería y mariscos",
  intro="El pescado y los mariscos no perdonan los cambios de temperatura. Fabricamos e instalamos el cuarto frío de tu pescadería a la medida de tu local, con el frío que tu producto necesita.",
  ben=[("Frío constante todo el día","El equipo se dimensiona para tu volumen, para que la temperatura no suba cuando abres la puerta."),
       ("Paneles fáciles de limpiar","Las superficies lisas de los paneles ayudan a mantener el orden y la higiene."),
       ("Refrigeración y congelación","Puedes tener producto del día y producto para almacenar, cada uno a su temperatura.")],
  temp=("Qué temperatura elegir","Para producto fresco que se vende rápido, refrigeración (0 a 5 °C). Para almacenar mariscos y pescado por más tiempo, congelación (−18 °C)."),
  items=["Pescado fresco","Mariscos","Producto congelado","Hielo y cavas de transporte"],
  faq=[("¿Sirve la misma cava para pescado fresco y congelado?","Cada temperatura necesita su propio equipo. Podemos hacer una cava para cada una o una cava combinada con dos zonas."),
       ("¿Instalan en zonas costeras o lejos de la ciudad?","Sí, trabajamos en toda Venezuela. Escríbenos tu ubicación por WhatsApp."),
       ("¿Qué necesito para cotizar?","Las medidas aproximadas del espacio y cuánto producto vas a guardar. Si no las sabes, te ayudamos.")],
  wa="Hola, tengo una pescadería y quiero cotizar un cuarto frío.", rel=["cuarto-de-congelacion","cavas-cuarto-carniceria","cava-cuarto-restaurante"]),

 dict(slug="cava-cuarto-polleria", nombre="Pollerías", img="c84", imgalt="Cava cuarto con pollo almacenado en bolsas",
  title="Cava cuarto para pollería y frigorífico en Venezuela | Refrigeración Team",
  desc="Cavas cuarto para pollerías y frigoríficos en Venezuela: más capacidad de almacenaje con frío estable. Fabricación e instalación. Cotiza por WhatsApp.",
  h1="Cava cuarto para pollería y frigorífico",
  intro="Si manejas pollo en volumen, necesitas espacio y frío que no falle. Hacemos la cava cuarto de tu pollería o frigorífico del tamaño que tu operación pide.",
  ben=[("Más capacidad de almacenaje","Aprovechamos el espacio para que guardes más producto ordenado."),
       ("Frío que no se interrumpe","Equipo dimensionado para tu carga, con control de temperatura."),
       ("Hecha para el trabajo diario","Puertas y estructura pensadas para el movimiento constante de mercancía.")],
  temp=("Refrigeración o congelación","Para el pollo que se vende en pocos días, refrigeración (0 a 5 °C). Para almacenar por más tiempo, congelación (−18 °C)."),
  items=["Pollo entero","Piezas y cortes","Producto empacado","Mercancía en cajas o bolsas"],
  faq=[("¿Qué tamaño de cava necesito para mi pollería?","Depende de cuánto producto manejas y cada cuánto lo recibes. Cuéntanos tu volumen y te recomendamos."),
       ("¿Pueden agrandar una cava existente?","Escríbenos con fotos y medidas de tu cava actual y evaluamos las opciones."),
       ("¿Hacen la instalación completa?","Sí: armamos la cava, montamos el equipo de frío y la dejamos funcionando.")],
  wa="Hola, tengo una pollería y quiero cotizar una cava cuarto.", rel=["cuarto-de-congelacion","cuartos-frios-galpones-distribuidores","cavas-cuarto-carniceria"]),

 dict(slug="cava-cuarto-restaurante", nombre="Restaurantes", img="c43", imgalt="Cava cuarto instalada dentro de un local",
  title="Cava cuarto para restaurante en Venezuela | Refrigeración Team",
  desc="Cava cuarto para restaurantes y cocinas en Venezuela: ingredientes frescos y ordenados. Diseño, fabricación e instalación. Cotiza por WhatsApp.",
  h1="Cava cuarto para restaurante",
  intro="Una cocina que funciona bien empieza por una buena cava. Diseñamos la cava cuarto de tu restaurante para el espacio que tienes, con frío estable y todo en su lugar.",
  ben=[("Ingredientes frescos","Mantén carnes, lácteos y verduras a la temperatura correcta."),
       ("Orden en la cocina","Zonas separadas para cada tipo de producto, con estantes a tu medida."),
       ("Se adapta a tu local","Fabricamos a la medida, incluso en espacios donde una nevera ya no da abasto.")],
  temp=("Qué temperatura necesitas","La mayoría de las cocinas usan refrigeración (0 a 5 °C) para producto fresco y, si congelan, una zona o cava aparte a −18 °C."),
  items=["Carnes y pollo","Lácteos","Verduras y frutas","Bebidas","Preparaciones"],
  faq=[("¿Una cava reemplaza mis neveras?","Para volumen, una cava cuarto da más espacio y orden que varias neveras. Cuéntanos tu caso y lo evaluamos."),
       ("¿Se puede instalar dentro de un local ya construido?","Sí, la armamos en el sitio a la medida del espacio disponible."),
       ("¿Cuánto tarda la instalación?","Depende del tamaño y del proyecto. Te damos el tiempo estimado en la cotización.")],
  wa="Hola, tengo un restaurante y quiero cotizar una cava cuarto.", rel=["cuarto-de-refrigeracion","cava-cuarto-panaderia","como-elegir-una-cava-cuarto"]),

 dict(slug="cava-cuarto-heladeria", nombre="Heladerías", img="c20", imgalt="Dos cavas con panel de control de temperatura",
  title="Cava cuarto para heladería en Venezuela | Refrigeración Team",
  desc="Cuarto de congelación para heladerías en Venezuela: almacena helado y materia prima a la temperatura correcta. Fabricación e instalación. Cotiza por WhatsApp.",
  h1="Cava cuarto para heladería",
  intro="El helado exige temperaturas muy bajas y estables. Hacemos cuartos de congelación a la medida para almacenar tu producto y tus insumos sin sorpresas.",
  ben=[("Temperatura muy baja y estable","Cuartos de congelación con control de temperatura."),
       ("Espacio para tu producción","Almacena más helado y materia prima en un solo lugar."),
       ("A la medida de tu local","Se adapta al espacio que tienes, grande o pequeño.")],
  temp=("Cuarto de congelación","Para helado y producto congelado, la referencia es la congelación (−18 °C). El equipo se dimensiona según tu volumen."),
  items=["Helado","Materia prima congelada","Frutas congeladas","Producto terminado"],
  faq=[("¿Qué temperatura necesita una heladería?","Para almacenar helado, congelación a unos −18 °C. Te orientamos según tu producto."),
       ("¿Pueden hacer una cava pequeña?","Sí, fabricamos a la medida, desde espacios pequeños hasta galpones."),
       ("¿Instalan fuera de mi ciudad?","Sí, atendemos en toda Venezuela.")],
  wa="Hola, tengo una heladería y quiero cotizar un cuarto de congelación.", rel=["cuarto-de-congelacion","cava-cuarto-restaurante","como-elegir-una-cava-cuarto"]),

 dict(slug="cava-cuarto-panaderia", nombre="Panaderías", img="c40", imgalt="Cava cuarto instalada en un galpón",
  title="Cava cuarto para panadería y pastelería en Venezuela | Refrigeración Team",
  desc="Cavas cuarto para panaderías y pastelerías en Venezuela: conserva lácteos, rellenos y producto terminado. Fabricación e instalación. Cotiza por WhatsApp.",
  h1="Cava cuarto para panadería y pastelería",
  intro="Rellenos, lácteos, cremas y producto terminado necesitan frío para durar. Fabricamos e instalamos la cava cuarto de tu panadería o pastelería a la medida de tu espacio.",
  ben=[("Insumos en buen estado","Conserva lácteos, rellenos y cremas a la temperatura adecuada."),
       ("Ordena tu producción","Un espacio dedicado para cada insumo y cada preparación."),
       ("Se adapta a tu local","Medidas a tu espacio, con puerta y estantes pensados para tu trabajo.")],
  temp=("Qué temperatura necesitas","Para lácteos, rellenos y preparaciones, refrigeración (0 a 5 °C). Si almacenas producto congelado, una zona a −18 °C."),
  items=["Lácteos","Cremas y rellenos","Frutas","Producto terminado"],
  faq=[("¿Sirve una cava para panadería y pastelería a la vez?","Sí. Se diseña según los productos que manejas y la temperatura de cada uno."),
       ("¿Cuánto espacio necesito?","Depende de tu producción. Cuéntanos tus medidas disponibles y te recomendamos un tamaño."),
       ("¿Incluye el equipo de frío?","Sí, instalamos la cava con su sistema de frío y control de temperatura.")],
  wa="Hola, tengo una panadería y quiero cotizar una cava cuarto.", rel=["cuarto-de-refrigeracion","cava-cuarto-restaurante","cava-cuarto-abasto-bodega"]),

 dict(slug="cava-cuarto-abasto-bodega", nombre="Abastos y bodegas", img="c36", imgalt="Cámaras frías exteriores de doble puerta",
  title="Cava cuarto para abasto, bodega y bebidas en Venezuela | Refrigeración Team",
  desc="Cavas cuarto para abastos, bodegas y venta de bebidas en Venezuela: más mercancía fría, más ventas. Fabricación e instalación. Cotiza por WhatsApp.",
  h1="Cava cuarto para abasto, bodega y bebidas",
  intro="Mercancía fría es mercancía que se vende. Hacemos la cava cuarto de tu abasto o bodega de bebidas para que tengas más producto frío disponible, sin llenar el local de neveras.",
  ben=[("Más producto frío","Almacena cajas de bebidas, lácteos y charcutería en un solo lugar."),
       ("Atiende más rápido","Reposición ordenada y a mano, sin salir a otro depósito."),
       ("Una sola solución","En vez de varias neveras, una cava a tu medida con frío estable.")],
  temp=("Qué temperatura necesitas","Bebidas, lácteos y charcutería funcionan con refrigeración (0 a 5 °C). Si vendes congelados, una zona o cava a −18 °C."),
  items=["Bebidas y refrescos","Cervezas","Lácteos","Charcutería","Congelados"],
  faq=[("¿Pueden hacer una cava con puerta para clientes?","Cuéntanos cómo atiendes y evaluamos la mejor configuración para tu local."),
       ("¿Es mejor una cava que varias neveras?","Para volumen, una cava da más espacio y orden. Te ayudamos a evaluarlo según tu caso."),
       ("¿Cómo pido la cotización?","Escríbenos por WhatsApp con las medidas aproximadas y lo que vas a guardar.")],
  wa="Hola, tengo un abasto y quiero cotizar una cava cuarto.", rel=["cuarto-de-refrigeracion","cuartos-frios-galpones-distribuidores","cava-cuarto-restaurante"]),

 dict(slug="cuartos-frios-galpones-distribuidores", nombre="Galpones y distribuidores", img="c86", imgalt="Cava industrial de gran tamaño dentro de un galpón",
  title="Cuartos fríos industriales para galpones y distribuidores | Refrigeración Team",
  desc="Cuartos fríos de gran tamaño para galpones, distribuidores y mayoristas en Venezuela. Diseño, fabricación e instalación. Cotiza por WhatsApp.",
  h1="Cuartos fríos para galpones y distribuidores",
  intro="Cuando mueves mucha mercancía necesitas una cava pensada para eso: puertas amplias, equipos para carga alta y espacio para recibir, guardar y despachar. Fabricamos cuartos fríos de gran tamaño a la medida de tu galpón.",
  ben=[("Puertas amplias","Puertas dimensionadas para el paso de paletas y montacargas."),
       ("Equipo para mucha carga","Evaporadores y condensadoras dimensionados para tu volumen."),
       ("Flujo ordenado","Pensamos el espacio para que recibas, guardes y despaches sin estorbos.")],
  temp=("Refrigeración, congelación o ambas","Según tu mercancía definimos las zonas: refrigeración (0 a 5 °C), congelación (−18 °C) o una combinación."),
  items=["Mercancía en paletas","Alimentos refrigerados","Alimentos congelados","Bebidas"],
  faq=[("¿Hacen cavas de gran tamaño?","Sí, fabricamos desde cavas pequeñas hasta cuartos fríos industriales dentro de un galpón."),
       ("¿Pueden trabajar en mi galpón sin parar la operación?","Cuéntanos cómo opera tu galpón y planificamos la instalación."),
       ("¿Atienden fuera de la ciudad?","Sí, instalamos en toda Venezuela.")],
  wa="Hola, tengo un galpón y quiero cotizar un cuarto frío de gran tamaño.", rel=["cuarto-de-congelacion","cuarto-de-refrigeracion","como-elegir-una-cava-cuarto"]),

 dict(slug="cuarto-de-refrigeracion", nombre="Refrigeración", img="c11", imgalt="Cava cuarto de refrigeración con cortina de aire",
  title="Cuarto de refrigeración (0 a 5 °C) a medida en Venezuela | Refrigeración Team",
  desc="Fabricamos e instalamos cuartos de refrigeración de 0 a 5 °C para alimentos y bebidas en toda Venezuela. Cotiza por WhatsApp.",
  h1="Cuarto de refrigeración de 0 a 5 °C",
  intro="Un cuarto de refrigeración mantiene tus productos frescos sin congelarlos. Lo diseñamos y fabricamos a tu medida, con equipo de frío y control de temperatura incluidos.",
  ben=[("Productos frescos","Ideal para alimentos y bebidas que se venden en pocos días."),
       ("A tu medida","Del tamaño exacto de tu espacio, con puerta y estantes a tu gusto."),
       ("Instalación completa","Armamos la cava, montamos el equipo y la dejamos trabajando.")],
  temp=("De 0 a 5 °C","Es el rango de la refrigeración. Se usa para productos frescos que no deben congelarse."),
  items=["Lácteos","Verduras y frutas","Bebidas","Carnes frescas","Preparaciones"],
  faq=[("¿Qué se guarda en un cuarto de refrigeración?","Productos frescos: lácteos, frutas, verduras, bebidas y carnes que se venden pronto."),
       ("¿En qué se diferencia de un cuarto de congelación?","El de refrigeración trabaja entre 0 y 5 °C y no congela. El de congelación llega a unos −18 °C."),
       ("¿Se puede convertir después a congelación?","Depende del equipo y del aislamiento. Consúltanos antes para diseñarla bien desde el inicio.")],
  wa="Hola, quiero cotizar un cuarto de refrigeración (0 a 5 °C).", rel=["cuarto-de-congelacion","como-elegir-una-cava-cuarto","cava-cuarto-restaurante"]),

 dict(slug="cuarto-de-congelacion", nombre="Congelación", img="c25", imgalt="Cava con puerta corrediza dentro de un galpón",
  title="Cuarto de congelación (−18 °C) a medida en Venezuela | Refrigeración Team",
  desc="Fabricamos e instalamos cuartos de congelación de −18 °C para carnes, mariscos y helados en toda Venezuela. Cotiza por WhatsApp.",
  h1="Cuarto de congelación de −18 °C",
  intro="Para guardar producto por más tiempo necesitas congelación. Fabricamos cuartos de congelación a tu medida, con aislamiento y equipo dimensionado para la carga.",
  ben=[("Conserva por más tiempo","Almacena carnes, mariscos y helados con temperatura estable."),
       ("Aislamiento que cuenta","Paneles aislantes y puertas hechas para mantener el frío adentro."),
       ("Control de temperatura","Instalamos el control para que sepas siempre cómo está tu cava.")],
  temp=("Unos −18 °C","Es la temperatura típica de congelación para almacenamiento. El equipo se dimensiona según el tamaño de la cava y lo que guardas."),
  items=["Carnes","Pescados y mariscos","Pollo","Helados","Producto congelado"],
  faq=[("¿Qué temperatura tiene un cuarto de congelación?","Unos −18 °C, que es la referencia para conservar producto congelado."),
       ("¿Qué se guarda en un cuarto de congelación?","Carnes, mariscos, pollo, helados y cualquier producto que se almacene congelado."),
       ("¿Cuánto cuesta?","Depende del tamaño y del equipo. Escríbenos tus medidas por WhatsApp y te cotizamos.")],
  wa="Hola, quiero cotizar un cuarto de congelación (−18 °C).", rel=["cuarto-de-refrigeracion","cava-cuarto-heladeria","cavas-cuarto-carniceria"]),

 dict(slug="como-elegir-una-cava-cuarto", nombre="Guía", img="real-exterior", imgalt="Cava cuarto con cortina de aire y paneles de control", guia=True,
  title="Cómo elegir una cava cuarto: temperatura, tamaño y equipo | Refrigeración Team",
  desc="Guía para elegir tu cava cuarto: qué temperatura necesitas, cómo calcular el tamaño y qué debe incluir. Respuestas claras de fabricantes. Cotiza por WhatsApp.",
  h1="Cómo elegir tu cava cuarto",
  intro="Antes de pedir una cotización conviene tener claras cuatro cosas. Con esta guía llegas a la conversación sabiendo qué necesitas.",
  ben=[("1. Qué vas a guardar","Define si es producto fresco, congelado o ambos. De eso depende la temperatura: refrigeración de 0 a 5 °C o congelación de unos −18 °C."),
       ("2. Cuánto espacio tienes","Mide el largo, el ancho y el alto del lugar donde va la cava. Si no estás seguro, una foto del espacio ayuda mucho."),
       ("3. Cuánto producto manejas","El volumen y la frecuencia con que entra y sale mercancía definen el tamaño y la potencia del equipo."),
       ("4. Cómo la vas a usar","Si entra gente o montacargas, cuántas veces abres la puerta y si necesitas estantes o ganchos. Eso define la puerta y el interior.")],
  temp=("Qué debe incluir una cava cuarto","Paneles aislantes, puerta con buen sellado, evaporador, condensadora y un control de temperatura. En Refrigeración Team incluimos todo el sistema."),
  items=["Paneles aislantes","Puerta","Evaporador","Condensadora","Control de temperatura"],
  faq=[("¿Cómo sé qué tamaño de cava necesito?","Parte del espacio disponible y del volumen de producto. Cuéntanos ambos por WhatsApp y te recomendamos."),
       ("¿Qué pasa si no sé las medidas?","No hay problema. Una foto del lugar y una idea de lo que quieres guardar bastan para orientarte."),
       ("¿Cuánto tarda en estar lista?","Depende del tamaño y del proyecto. Te damos el tiempo estimado con la cotización.")],
  wa="Hola, quiero ayuda para elegir mi cava cuarto.", rel=["cuarto-de-refrigeracion","cuarto-de-congelacion","cuartos-frios-galpones-distribuidores"]),
]
PAGES += [
 dict(slug="equipos-y-materiales-para-cavas-cuarto", nombre="Equipos y materiales", img="eq-condensadora-unidad", imgalt="Unidad condensadora para cava cuarto",
  title="", desc="Unidades condensadoras Copeland, Bitzer, Danfoss, difusores Elgin, RGC, compresores e insumos para cavas cuarto. Cotiza por WhatsApp.",
  h1="Equipos y materiales para cavas cuarto",
  intro="Además de fabricar e instalar cavas cuarto, te vendemos todo el material para la tuya: unidades condensadoras, compresores, difusores, controles, luces, cerraduras e insumos. Cuéntanos qué necesitas y te cotizamos.",
  ben_eyebrow="Qué vendemos", ben_h2="Todo para tu cava cuarto",
  ben=[("Unidades condensadoras","La parte del sistema que trabaja afuera y expulsa el calor. Te ayudamos a elegir la potencia según el tamaño de tu cava y la temperatura que necesitas. Marcas: Copeland, Tecumseh, Bitzer, Frascold, Danfoss, Invotech y otras."),
       ("Compresores","El corazón del sistema de frío: hace circular el refrigerante. Consulta por el compresor que necesita tu cava."),
       ("Difusores y evaporadores","Los ventiladores que reparten el frío dentro de la cava para que enfríe todo el espacio de forma pareja. Marcas: Elgin, RGC, Freeze, Mipal, Degar y otras."),
       ("Controles y tableros","Control de temperatura y tableros eléctricos para que tu cava trabaje con precisión y puedas vigilarla."),
       ("Luces, cerraduras e insumos","Iluminación para el interior, cerraduras, manijas y otros insumos que necesita tu cava cuarto."),
       ("Asesoría para elegir","Si no sabes qué equipo necesitas, cuéntanos el tamaño de tu cava y qué guardas, y te orientamos.")],
  temp=("¿No sabes qué equipo necesitas?","Escríbenos con el tamaño de tu cava (o una foto) y la temperatura que buscas, y te recomendamos el equipo adecuado. Te confirmamos disponibilidad por WhatsApp."),
  items=["Unidades condensadoras","Compresores","Difusores","Evaporadores","Controles de temperatura","Tableros","Luces","Cerraduras","Freezers"],
  faq=[("¿Venden equipos solos, sin la cava?","Cuéntanos por WhatsApp qué necesitas y te confirmamos disponibilidad y cotización."),
       ("¿Qué marcas venden?","Unidades condensadoras: Copeland, Tecumseh, Bitzer, Frascold, Danfoss, Invotech y otras. Difusores: Elgin, RGC, Freeze, Mipal, Degar y otras. Consulta por WhatsApp la disponibilidad."),
       ("¿Me ayudan a elegir el equipo correcto?","Sí. Parte del tamaño de tu cava y de la temperatura que necesitas (refrigeración de 0 a 5 °C o congelación de unos −18 °C) para recomendarte el equipo."),
       ("¿Qué es una unidad condensadora?","Es el equipo que trabaja afuera de la cava y expulsa el calor del sistema. Va conectado al evaporador (difusor) que está adentro."),
       ("¿Envían a todo el país?","Atendemos en toda Venezuela. Escríbenos tu ubicación por WhatsApp.")],
  wa="Hola, quiero cotizar equipos y materiales para cavas cuarto.", rel=["cuarto-de-refrigeracion","cuarto-de-congelacion","freezers-comerciales"]),
 dict(slug="freezers-comerciales", nombre="Freezers", img="eq-freezers", imgalt="Freezer horizontal y nevera vertical para negocios",
  title="", desc="Venta de freezers comerciales para negocios en Venezuela, además de cavas cuarto. Pregunta por modelos disponibles y cotiza por WhatsApp.",
  h1="Freezers para tu negocio",
  ben_eyebrow="Freezers", ben_h2="Un freezer para cada negocio",
  intro="Además de cavas cuarto, vendemos freezers para negocios. Cuéntanos qué vas a guardar y cuánto espacio necesitas, y te cotizamos el que mejor te sirva.",
  ben=[("Para negocios pequeños","Si tu producto no necesita una cava cuarto, un freezer puede ser la solución más simple."),
       ("Complemento de tu cava","Ideal para tener producto congelado a mano en el punto de venta."),
       ("Te asesoramos","Cuéntanos tu caso y te ayudamos a elegir entre un freezer o una cava cuarto.")],
  temp=("¿Freezer o cava cuarto?","Un freezer sirve para volúmenes pequeños y medianos. Si manejas más producto, necesitas caminar dentro o vender al mayor, una cava cuarto te da más espacio y orden."),
  items=["Carnes","Pollo","Pescados y mariscos","Helados","Producto congelado"],
  faq=[("¿Qué modelos de freezer venden?","Escríbenos por WhatsApp y te confirmamos los modelos disponibles y sus características."),
       ("¿Cuándo conviene una cava cuarto en vez de un freezer?","Cuando manejas mucho volumen, necesitas entrar a organizar el producto o tienes varios productos que guardar a distinta temperatura."),
       ("¿Envían a todo el país?","Atendemos en toda Venezuela. Escríbenos tu ubicación.")],
  wa="Hola, quiero cotizar un freezer.", rel=["equipos-y-materiales-para-cavas-cuarto","cuarto-de-congelacion","como-elegir-una-cava-cuarto"]),
]
for _p in PAGES: _p.setdefault("title", "")

TITULOS = {"cavas-cuarto-carniceria":"Cava Cuarto para Carnicería","cuartos-frios-pescaderia":"Cuarto Frío para Pescadería",
 "cava-cuarto-polleria":"Cava Cuarto para Pollería","cava-cuarto-restaurante":"Cava Cuarto para Restaurante",
 "cava-cuarto-heladeria":"Cava Cuarto para Heladería","cava-cuarto-panaderia":"Cava Cuarto para Panadería",
 "cava-cuarto-abasto-bodega":"Cava Cuarto para Abasto y Bodega","cuartos-frios-galpones-distribuidores":"Cuartos Fríos para Galpones",
 "cuarto-de-refrigeracion":"Cuarto de Refrigeración 0 a 5 °C","cuarto-de-congelacion":"Cuarto de Congelación −18 °C",
 "como-elegir-una-cava-cuarto":"Cómo Elegir una Cava Cuarto",
 "equipos-y-materiales-para-cavas-cuarto":"Equipos y Materiales para Cavas Cuarto","freezers-comerciales":"Freezers Comerciales"}
for _p in PAGES: _p["title"] = TITULOS[_p["slug"]] + " | Refrigeración Team"
BYSLUG = {p["slug"]: p for p in PAGES}

# --------------------------------------------------------------- utilidades
esc = html.escape
def wa_url(t):
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(t)}"

def robots_meta():
    return '<meta name="robots" content="index, follow, max-image-preview:large">' if INDEXAR else \
           '<!-- PROTOTIPO: noindex hasta publicar con dominio real -->\n<meta name="robots" content="noindex, nofollow">'

def add_dims(s):
    """Agrega width/height a las <img> locales para evitar saltos de diseño."""
    def f(m):
        tag = m.group(0)
        if "width=" in tag: return tag
        src = re.search(r'src="/(img/[^"]+)"', tag)
        if not src: return tag
        p = SITIO / src.group(1)
        if not p.exists(): return tag
        w, h = Image.open(p).size
        return tag.replace("<img ", f'<img width="{w}" height="{h}" ', 1)
    return re.sub(r"<img [^>]*>", f, s)

def analytics():
    o = ""
    if GA_ID:
        o += f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>\n<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>\n'
    if PIXEL_ID:
        o += ("<script>!function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};"
              "if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src='https://connect.facebook.net/en_US/fbevents.js';"
              f"s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script');fbq('init','{PIXEL_ID}');fbq('track','PageView');</script>\n")
    return o

WAJS = r'''// Refrigeración Team: WhatsApp, medición de clics y avisos
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
const WHATSAPP = "%s";   // país + número, sin + ni espacios
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
''' % WHATSAPP

SECTORES = ["cavas-cuarto-carniceria", "cuartos-frios-pescaderia", "cava-cuarto-polleria", "cava-cuarto-restaurante",
            "cava-cuarto-heladeria", "cava-cuarto-panaderia", "cava-cuarto-abasto-bodega", "cuartos-frios-galpones-distribuidores"]
TILE_SUB = {"cavas-cuarto-carniceria": "Cortes frescos y almacenaje", "cuartos-frios-pescaderia": "Frío constante todo el día",
            "cava-cuarto-polleria": "Más capacidad de almacenaje", "cava-cuarto-restaurante": "Ingredientes frescos y ordenados",
            "cava-cuarto-heladeria": "Congelación estable", "cava-cuarto-panaderia": "Lácteos, cremas y rellenos",
            "cava-cuarto-abasto-bodega": "Bebidas y charcutería frías", "cuartos-frios-galpones-distribuidores": "Cavas de gran tamaño"}
EQUIPOS = "/equipos-y-materiales-para-cavas-cuarto/"

# menú principal: (texto, url, submenú)
def menu_items():
    return [
        ("Cavas cuarto", "/cavas-cuarto/", [("Fabricación e instalación", "/cavas-cuarto/"),
            ("Cuarto de refrigeración (0 a 5 °C)", "/cuarto-de-refrigeracion/"), ("Cuarto de congelación (−18 °C)", "/cuarto-de-congelacion/"),
            ("Cómo elegir tu cava", "/como-elegir-una-cava-cuarto/")]),
        ("Para tu negocio", "/sectores/", [("Todos los negocios", "/sectores/")] + [(BYSLUG[s]["nombre"], f"/{s}/") for s in SECTORES]),
        ("Equipos", EQUIPOS, [("Equipos y materiales", EQUIPOS), ("Freezers comerciales", "/freezers-comerciales/")]),
        ("Proyectos", "/proyectos/", None),
        ("Nosotros", "/nosotros/", [("Quiénes somos", "/nosotros/"), ("Cobertura", "/cobertura/"),
            ("Preguntas frecuentes", "/preguntas-frecuentes/"), ("Contacto", "/contacto/")]),
    ]

def nav_html(path):
    cur = lambda u: ' aria-current="page"' if u == path else ""
    o = ['      <ul id="menu">']
    for t, u, sub in menu_items():
        if sub:
            subs = "".join('<li><a href="%s"%s>%s</a></li>' % (su, cur(su), esc(st)) for st, su in sub)
            o.append(f'        <li class="dd"><a href="{u}"{cur(u)}>{esc(t)}</a><button class="dd-t" type="button" aria-expanded="false" aria-label="Ver opciones de {esc(t)}"></button>'
                     f'<ul class="submenu">{subs}</ul></li>')
        else:
            o.append(f'        <li><a href="{u}"{cur(u)}>{esc(t)}</a></li>')
    o.append(f'        <li><a class="nav-cta" href="/cotizar/"{cur("/cotizar/")}>Cotizar</a></li>')
    o.append('      </ul>')
    return "\n".join(o)

def foot_cols():
    cols = [("Cavas cuarto", [("Fabricación e instalación", "/cavas-cuarto/"), ("Cuarto de refrigeración", "/cuarto-de-refrigeracion/"),
                ("Cuarto de congelación", "/cuarto-de-congelacion/"), ("Cómo elegir tu cava", "/como-elegir-una-cava-cuarto/"),
                ("Equipos y materiales", EQUIPOS), ("Freezers", "/freezers-comerciales/")]),
            ("Para tu negocio", [(BYSLUG[s]["nombre"], f"/{s}/") for s in SECTORES]),
            ("Empresa", [("Proyectos", "/proyectos/"), ("Nosotros", "/nosotros/"), ("Cobertura", "/cobertura/"),
                ("Preguntas frecuentes", "/preguntas-frecuentes/"), ("Contacto", "/contacto/"), ("Cotizar", "/cotizar/")])]
    lis = lambda items: "".join('<li><a href="%s">%s</a></li>' % (u, esc(t)) for t, u in items)
    return "\n      ".join('<div><p class="fh">%s</p><ul>%s</ul></div>' % (esc(h), lis(items)) for h, items in cols)

# ------------------------------------------------------------ imagen social
def make_og():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), "#06224d")
    ph = Image.open(SITIO / "img/real-exterior.jpg").convert("RGB")
    r = H / ph.height; ph = ph.resize((int(ph.width * r), H))
    im.paste(ph, (W - ph.width, 0))
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for x in range(0, 760):
        d.line([(x, 0), (x, H)], fill=(6, 34, 77, int(255 * max(0, 1 - max(0, x - 520) / 240))))
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    d = ImageDraw.Draw(im)
    def font(sz, bold=True):
        for f in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"):
            try: return ImageFont.truetype(f, sz)
            except Exception: pass
        return ImageFont.load_default()
    logo = Image.open(AQUI / "logo_original.png").convert("RGBA"); logo.thumbnail((170, 170))
    chip = Image.new("RGBA", (logo.width + 24, logo.height + 24), (255, 255, 255, 255)); chip.paste(logo, (12, 12), logo)
    im.paste(chip, (60, 60), chip)
    y = 270
    for ln in ("Cavas cuarto", "a tu medida"):
        d.text((60, y), ln, font=font(58), fill="white"); y += 70
    d.text((60, y + 10), "Fabricación e instalación en toda Venezuela", font=font(30), fill="#00E3FF")
    d.rounded_rectangle((60, 540, 470, 596), 28, fill="#25D366")
    d.text((90, 553), "Cotiza por WhatsApp", font=font(30), fill="#04361a")
    im.save(SITIO / "img/og.jpg", quality=85, optimize=True)

# ---------------------------------------------------------- plantilla común
home = (AQUI / "home.src.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", home, re.S).group(1)
HEADER_T = re.search(r"<header>.*?</header>", home, re.S).group(0)
def header(path): return HEADER_T.replace("{{NAV}}", nav_html(path))
FOOTER = re.search(r"<footer>.*?</footer>", home, re.S).group(0).replace("{{FOOTCOLS}}", foot_cols())
LB = '<div id="lb" role="dialog" aria-modal="true" aria-label="Foto ampliada"><button aria-label="Cerrar">×</button><img alt=""></div>'

FAB = re.search(r'<a class="fab".*?</a>', home, re.S).group(0)
SYMBOL = re.search(r'<svg width="0".*?</svg>', home, re.S).group(0)
MBAR = re.search(r'<div class="mbar">.*?</div>', home, re.S).group(0)
FONTS = re.search(r'<link rel="preconnect" href="https://fonts.googleapis.com">.*?display=swap" rel="stylesheet">', home, re.S).group(0)

EXTRA_CSS = """
.crumbs{font-size:.85rem;color:#9fc0e6;margin-bottom:18px}.crumbs a{color:#cfe0f5;text-decoration:none}.crumbs a:hover{color:#fff}
.phero{background:radial-gradient(1000px 420px at 90% -10%,rgba(41,169,232,.4),transparent 60%),linear-gradient(160deg,var(--navy-dk),#0a3a8a 70%,var(--navy));color:#fff;padding:44px 0 60px}
.phero .grid{display:grid;grid-template-columns:1.2fr .8fr;gap:40px;align-items:center}
.phero h1{font-size:clamp(1.9rem,5vw,3rem);font-weight:800;margin-bottom:16px}
.phero p.sub{font-size:1.1rem;color:#cfe0f5;max-width:560px;margin-bottom:26px}
.phero .ph{aspect-ratio:4/5;border-radius:22px;overflow:hidden;border:4px solid rgba(255,255,255,.2);box-shadow:0 24px 50px rgba(0,0,0,.4)}
.phero .ph img{width:100%;height:100%;object-fit:cover}
@media(max-width:860px){.phero .grid{grid-template-columns:1fr}.phero .ph{aspect-ratio:16/10}}
.bens{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:20px;margin-top:30px}
.ben{border:1px solid var(--line);border-radius:var(--r);padding:24px;background:#fff}
.ben h3{font-size:1.1rem;margin-bottom:8px;color:var(--navy)}.ben p{color:var(--muted);font-size:.96rem}
.tempbox{background:var(--ice);border:1px solid var(--line);border-radius:var(--r);padding:28px;margin-top:24px}
.tempbox ul{list-style:none;display:flex;flex-wrap:wrap;gap:8px;margin-top:16px}
.tempbox li{background:#fff;border:1px solid var(--line);border-radius:99px;padding:7px 14px;font-weight:600;font-size:.88rem;color:var(--navy)}
.band{background:linear-gradient(160deg,var(--navy-dk),var(--navy));color:#fff;border-radius:24px;padding:40px 28px;text-align:center}
.band h2{font-size:clamp(1.5rem,4vw,2.1rem)}.band p{color:#c3d6ee;margin:0 auto 22px;max-width:520px}
.rel{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px;margin-top:24px}
.phero .ph.eqph{display:grid;place-items:center;background:radial-gradient(circle at 50% 40%,#29A9E8,#0040A0 75%)}.phero .ph.eqph svg{width:46%;height:auto}
.rel a{display:block;border:1px solid var(--line);border-radius:14px;padding:18px;text-decoration:none;font-weight:700;color:var(--navy);transition:.15s}
.rel a:hover{border-color:var(--sky);transform:translateY(-2px)}.rel a small{display:block;color:var(--muted);font-weight:500;margin-top:4px}
.crumbs span{color:#fff}
.phero.slim{padding:40px 0 52px}.phero.slim .grid{grid-template-columns:1fr}.phero.slim p.sub{max-width:720px}
.prose{max-width:820px}.prose p{color:var(--muted);font-size:1.04rem;margin-top:14px}.prose a{color:var(--navy);font-weight:600}.prose strong{color:var(--ink)}
.ben a{color:var(--navy);font-weight:700;text-decoration:none;white-space:nowrap}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin-top:30px}
.pgrid figure{cursor:zoom-in}.pgrid .im{aspect-ratio:3/4;border-radius:16px;overflow:hidden;background:#cfe0f0}
.pgrid img{width:100%;height:100%;object-fit:cover;transition:transform .4s}.pgrid figure:hover img{transform:scale(1.05)}
.pgrid figcaption{font-size:.86rem;color:var(--muted);margin-top:8px;font-weight:500}
@media(max-width:520px){.pgrid{grid-template-columns:1fr 1fr;gap:10px}}
.tiles + .more,.faq + .more{margin-top:24px}
.toc{margin:0 0 34px;gap:8px}.toc a{background:var(--ice);border:1px solid var(--line);border-radius:99px;padding:7px 14px;font-size:.9rem}
.fgroup{margin-bottom:46px;scroll-margin-top:90px}.fgroup h2{font-size:clamp(1.35rem,3vw,1.8rem)}.fgroup .faq{margin-top:16px}
.ccards{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}
.ccard{display:flex;flex-direction:column;gap:6px;border:1px solid var(--line);border-radius:var(--r);padding:28px;text-decoration:none;color:var(--ink);background:#fff;transition:.2s}
.ccard:hover{transform:translateY(-3px);box-shadow:var(--shadow)}
.ccard svg{width:34px;height:34px;color:var(--navy);margin-bottom:6px}.ccard.wa svg{color:var(--wa-dk)}
.ccard b{font:800 1.25rem/1.2 Sora,sans-serif}.ccard span{font-weight:700;color:var(--navy)}.ccard small{color:var(--muted)}
@media(max-width:760px){.ccards{grid-template-columns:1fr}}
"""

def wa_hrefs(s):
    """Pone el enlace real de WhatsApp en el HTML (wa.js luego le añade la página de origen)."""
    def f(m):
        tag = m.group(0)
        t = re.search(r'data-wa="([^"]*)"', tag)
        if not t or 'href="#"' not in tag: return tag
        return tag.replace('href="#"', f'href="{esc(wa_url(html.unescape(t.group(1))))}" target="_blank" rel="nofollow noopener"', 1)
    return re.sub(r"<a [^>]*data-wa=[^>]*>", f, s)

EMPRESA = {"@type": "LocalBusiness", "@id": f"{BASE}/#empresa", "name": "Refrigeración Team Cavas Cuarto", "telephone": "+584121856429", "url": f"{BASE}/"}

def head(title, desc, path, img, schema, canonical=True):
    url = f"{BASE}{path}"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots_meta()}
{f'<link rel="canonical" href="{url}">' if canonical else ""}
<meta name="theme-color" content="#0040A0">
<meta property="og:type" content="website"><meta property="og:locale" content="es_VE">
<meta property="og:site_name" content="Refrigeración Team">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/img/og.jpg">
<meta property="og:image:alt" content="Refrigeración Team: cavas cuarto a tu medida en toda Venezuela">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="icon" type="image/png" href="/img/icon-96.png"><link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
{analytics()}{FONTS}
{f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""}
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
"""

SCRIPT = '<script src="/js/wa.js"></script>\n<script src="/js/sitio.js"></script>\n</body>\n</html>\n'

WA_ICON = '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><use href="#i-wa"/></svg>'

def build_page(p):
    path = f"/{p['slug']}/"
    business = EMPRESA
    crumbs = ([PARENT[p["slug"]]] if p["slug"] in PARENT else []) + [(p["nombre"], path)]
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": p["h1"], "description": p["desc"], "serviceType": "Fabricación e instalación de cavas cuarto",
         "provider": business, "areaServed": {"@type": "Country", "name": "Venezuela"}, "url": f"{BASE}{path}"},
        crumbs_schema(crumbs),
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}]}
    o = head(p["title"], p["desc"], path, p["img"], schema) + TOPBAR + "\n" + header(path) + "\n<main>\n"
    o += f"""<section class="phero on-dark"><div class="wrap grid"><div>
{crumbs_html(crumbs)}
<h1>{esc(p['h1'])}</h1>
<p class="sub">{esc(p['intro'])}</p>
<div style="display:flex;flex-wrap:wrap;gap:12px"><a class="btn btn-wa" data-lugar="hero" data-wa="{esc(p['wa'])}" href="#">{WA_ICON}Cotizar por WhatsApp</a><a class="btn btn-ghost" href="tel:+584121856429" data-lugar="hero-llamar">Llamar ahora</a></div>
</div><div class="ph{' eqph' if p.get('icon') else ''}">{p['icon'] if p.get('icon') else f'<img src="/img/{p["img"]}.jpg" alt="{esc(p["imgalt"])}" fetchpriority="high">'}</div></div></section>
<section><div class="wrap"><span class="eyebrow">{p.get('ben_eyebrow') or ('Pasos a seguir' if p.get('guia') else 'Por qué una cava cuarto')}</span>
<h2>{p.get('ben_h2') or ('Qué tener claro antes de cotizar' if p.get('guia') else 'Lo que ganas con tu cava cuarto')}</h2>
<div class="bens">{''.join(f'<div class="ben rv"><h3>{esc(h)}</h3><p>{esc(t)}</p></div>' for h, t in p['ben'])}</div></div></section>
{p.get('extra', '')}
<section style="padding-top:0"><div class="wrap"><div class="tempbox rv"><h2 style="font-size:1.5rem">{esc(p['temp'][0])}</h2>
<p class="lead" style="margin-top:6px">{esc(p['temp'][1])}</p>
<ul>{''.join(f'<li>{esc(i)}</li>' for i in p['items'])}</ul></div></div></section>
<section style="background:var(--ice)"><div class="wrap"><span class="eyebrow">Preguntas frecuentes</span><h2>Dudas comunes</h2>
<div class="faq">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p['faq'])}</div></div></section>
<section><div class="wrap"><div class="band on-dark"><h2>Cuéntanos qué necesitas y te cotizamos</h2>
<p>Escríbenos por WhatsApp con tus medidas aproximadas y lo que vas a guardar. Si no las sabes, te ayudamos.</p>
<div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center"><a class="btn btn-wa" data-lugar="cierre" data-wa="{esc(p['wa'])}" href="#">{WA_ICON}Escribir por WhatsApp</a><a class="btn btn-ghost" href="/cotizar/">Llenar el cotizador</a></div></div>
<h2 style="font-size:1.4rem;margin-top:44px">También te puede interesar</h2>
<div class="rel">{''.join(f'<a href="/{r}/">{esc(BYSLUG[r]["h1"])}<small>Ver más →</small></a>' for r in p['rel'])}</div></div></section>
</main>
""" + FOOTER + "\n" + FAB + "\n" + MBAR + "\n" + LB + "\n" + SYMBOL + "\n" + SCRIPT
    d = SITIO / p["slug"]; d.mkdir(exist_ok=True)
    (d / "index.html").write_text(wa_hrefs(add_dims(o)), encoding="utf-8")

# ------------------------------------------------------- rutas (breadcrumbs)
PARENT = {s: ("Para tu negocio", "/sectores/") for s in SECTORES}
PARENT.update({"cuarto-de-refrigeracion": ("Cavas cuarto", "/cavas-cuarto/"), "cuarto-de-congelacion": ("Cavas cuarto", "/cavas-cuarto/"),
               "como-elegir-una-cava-cuarto": ("Cavas cuarto", "/cavas-cuarto/"), "freezers-comerciales": ("Equipos y materiales", EQUIPOS)})

def crumbs_html(crumbs):
    partes = ['<a href="/">Inicio</a>'] + [f'<a href="{u}">{esc(n)}</a>' for n, u in crumbs[:-1]] + [f'<span aria-current="page">{esc(crumbs[-1][0])}</span>']
    return '<nav class="crumbs" aria-label="Ruta">' + " › ".join(partes) + "</nav>"

def crumbs_schema(crumbs):
    todos = [("Inicio", "/")] + crumbs
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": f"{BASE}{u}"} for i, (n, u) in enumerate(todos)]}

def tiles(slugs):
    return '<div class="tiles">' + "".join(
        f'<a class="tile rv" href="/{s}/"><img src="/img/{BYSLUG[s]["img"]}.jpg" alt="{esc(BYSLUG[s]["imgalt"])}" loading="lazy"><h3>{esc(BYSLUG[s]["nombre"])}<small>{esc(TILE_SUB[s])}</small></h3></a>'
        for s in slugs) + "</div>"

def faq_html(items):
    return '<div class="faq">' + "".join(f"<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>" for q, a in items) + "</div>"

def faq_schema(items):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

def band(wa, titulo="Cuéntanos qué necesitas y te cotizamos", texto="Escríbenos por WhatsApp con tus medidas aproximadas y lo que vas a guardar. Si no las sabes, te ayudamos."):
    return (f'<section><div class="wrap"><div class="band on-dark"><h2>{esc(titulo)}</h2><p>{esc(texto)}</p>'
            f'<div style="display:flex;flex-wrap:wrap;gap:12px;justify-content:center"><a class="btn btn-wa" data-lugar="cierre" data-wa="{esc(wa)}" href="#">{WA_ICON}Escribir por WhatsApp</a>'
            f'<a class="btn btn-ghost" href="/cotizar/">Llenar el cotizador</a></div></div></div></section>')

def shell(path, title, desc, crumbs, h1, intro, body, nodes, wa, img=None, imgalt="", extra=""):
    schema = {"@context": "https://schema.org", "@graph": nodes + [crumbs_schema(crumbs)]}
    foto = f'<div class="ph"><img src="/img/{img}.jpg" alt="{esc(imgalt)}" fetchpriority="high"></div>' if img else ""
    o = head(title, desc, path, img or "", schema) + TOPBAR + "\n" + header(path) + "\n<main>\n"
    o += (f'<section class="phero on-dark{"" if img else " slim"}"><div class="wrap grid"><div>{crumbs_html(crumbs)}'
          f'<h1>{esc(h1)}</h1><p class="sub">{esc(intro)}</p>'
          f'<div style="display:flex;flex-wrap:wrap;gap:12px"><a class="btn btn-wa" data-lugar="hero" data-wa="{esc(wa)}" href="#">{WA_ICON}Cotizar por WhatsApp</a>'
          f'<a class="btn btn-ghost" href="tel:+584121856429" data-lugar="hero-llamar">Llamar ahora</a></div></div>{foto}</div></section>\n')
    o += body + "\n</main>\n" + FOOTER + "\n" + FAB + "\n" + MBAR + "\n" + LB + "\n" + extra + SYMBOL + "\n" + SCRIPT
    d = SITIO / path.strip("/"); d.mkdir(exist_ok=True)
    (d / "index.html").write_text(wa_hrefs(add_dims(o)), encoding="utf-8")

def seccion(h, sid, quitar=None):
    """Toma una sección de la home ya armada; quita el enlace 'ver más' que apunta a la página actual."""
    s = re.search(r'<section[^>]*id="%s".*?</section>' % sid, h, re.S).group(0)
    if quitar:
        s = re.sub(r'\s*<p class="more">(?:(?!</p>).)*href="%s"(?:(?!</p>).)*</p>' % re.escape(quitar), "", s, flags=re.S)
    return s

def build_extra_pages(h):
    home_faq = [(html.unescape(q), html.unescape(a)) for q, a in re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", seccion(h, "faq"))]
    emp = {"@id": f"{BASE}/#empresa"}

    # /cavas-cuarto/
    q = [x for x in home_faq if not x[0].startswith("¿Venden")]
    body = f'''<section><div class="wrap prose"><span class="eyebrow">Qué es una cava cuarto</span>
<h2>Un cuarto frío hecho para tu espacio</h2>
<p>Una cava cuarto es un cuarto frío que se arma con paneles aislantes en paredes y techo, una puerta que sella bien y un equipo de refrigeración. A diferencia de una nevera, puedes entrar a ordenar el producto, guardar mucho más volumen y mantener una temperatura estable todo el día.</p>
<p>El sistema tiene cinco partes: los <strong>paneles aislantes</strong>, que mantienen el frío adentro; la <strong>puerta</strong>, con su sellado y cerradura; el <strong>evaporador</strong> o difusor, que reparte el frío dentro de la cava; la <strong>unidad condensadora</strong>, que trabaja afuera y expulsa el calor; y el <strong>control de temperatura</strong>, para vigilarla y ajustarla.</p>
<p>Cada cava se diseña según tres cosas: el espacio que tienes, lo que vas a guardar y la temperatura que necesita tu producto. Si aún no lo tienes claro, revisa la guía <a href="/como-elegir-una-cava-cuarto/">cómo elegir tu cava cuarto</a> o escríbenos y te orientamos.</p>
</div></section>
{seccion(h, "servicios", "/cavas-cuarto/")}
{seccion(h, "temperaturas")}
<section><div class="wrap"><span class="eyebrow">Para tu negocio</span><h2>Cavas cuarto según tu negocio</h2>
<p class="lead">Cada negocio guarda productos distintos. Mira lo que hacemos para el tuyo.</p>{tiles(SECTORES)}
<p class="more"><a href="/sectores/">Ver todos los negocios →</a></p></div></section>
{seccion(h, "proceso")}
<section style="background:var(--ice)"><div class="wrap"><span class="eyebrow">Preguntas frecuentes</span><h2>Dudas sobre cavas cuarto</h2>{faq_html(q)}
<p class="more"><a href="/preguntas-frecuentes/">Ver todas las preguntas →</a></p></div></section>
{band("Hola, quiero cotizar una cava cuarto.")}'''
    shell("/cavas-cuarto/", "Cavas Cuarto: Fabricación e Instalación | Refrigeración Team",
          "Fabricamos e instalamos cavas cuarto a la medida de tu espacio, con paneles, puerta, evaporador, condensadora y control de temperatura. Toda Venezuela.",
          [("Cavas cuarto", "/cavas-cuarto/")], "Cavas cuarto a la medida de tu negocio",
          "Diseñamos, armamos e instalamos tu cava cuarto con todo el sistema de frío incluido, del tamaño exacto de tu espacio y a la temperatura que necesita tu producto.",
          body, [{"@type": "Service", "name": "Fabricación e instalación de cavas cuarto", "serviceType": "Cava cuarto / cuarto frío a medida",
                  "provider": emp, "areaServed": {"@type": "Country", "name": "Venezuela"}, "url": f"{BASE}/cavas-cuarto/"}, faq_schema(q)],
          "Hola, quiero cotizar una cava cuarto.", img="c50", imgalt="Cava cuarto armada dentro de un galpón")

    # /sectores/
    body = f'''<section><div class="wrap"><span class="eyebrow">Para tu negocio</span><h2>Elige tu tipo de negocio</h2>
<p class="lead">Del local pequeño al galpón industrial. Toca tu negocio para ver qué temperatura necesitas, qué puedes guardar y las dudas más comunes.</p>{tiles(SECTORES)}</div></section>
<section style="background:var(--ice)"><div class="wrap prose"><span class="eyebrow">¿No ves tu negocio?</span><h2>También hacemos cavas para otros rubros</h2>
<p>Si guardas alimentos, bebidas, flores, medicinas u otro producto que necesite frío, también podemos hacer tu cava cuarto. Lo importante es saber qué vas a guardar, cuánto espacio tienes y a qué temperatura debe estar.</p>
<p>Para producto fresco se usa un <a href="/cuarto-de-refrigeracion/">cuarto de refrigeración de 0 a 5 °C</a>. Para almacenar por más tiempo, un <a href="/cuarto-de-congelacion/">cuarto de congelación de −18 °C</a>. Si manejas ambos, se hacen dos cavas o una combinada.</p>
</div></section>
{band("Hola, quiero cotizar una cava cuarto para mi negocio.")}'''
    shell("/sectores/", "Cavas Cuarto para Negocios y Comercios | Refrigeración Team",
          "Cavas cuarto para carnicerías, pescaderías, pollerías, restaurantes, heladerías, panaderías, abastos y galpones en Venezuela. Cotiza por WhatsApp.",
          [("Para tu negocio", "/sectores/")], "Cavas cuarto para cada tipo de negocio",
          "Hacemos la cava cuarto que tu negocio necesita: el tamaño, la temperatura y la distribución dependen de lo que vendes y de cómo trabajas.",
          body, [{"@type": "CollectionPage", "name": "Cavas cuarto para negocios", "url": f"{BASE}/sectores/",
                  "mainEntity": {"@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{BASE}/{s}/", "name": BYSLUG[s]["h1"]} for i, s in enumerate(SECTORES)]}}],
          "Hola, quiero cotizar una cava cuarto para mi negocio.")

    # /proyectos/
    figs = re.findall(r'<figure><div class="im">(<img [^>]*>)</div><figcaption>(.*?)</figcaption></figure>', seccion(h, "trabajos"))
    limpia = lambda im: re.sub(r' (loading|fetchpriority|decoding)="[^"]*"', "", im).replace("<img ", '<img loading="lazy" ')
    grid = "".join('<figure><div class="im">%s</div><figcaption>%s</figcaption></figure>' % (limpia(im), c) for im, c in figs)
    body = f'''<section class="gal"><div class="wrap"><span class="eyebrow">Galería</span><h2>Cavas reales, instaladas por nosotros</h2>
<p class="lead">Algunas de las cavas cuarto y cuartos fríos que hemos entregado. Toca una foto para verla en grande.</p>
<div class="pgrid" id="galeria">{grid}</div>
<p class="more"><a href="https://www.instagram.com/cavascuartoteam/" target="_blank" rel="noopener">Ver más trabajos en Instagram →</a></p></div></section>
<section><div class="wrap prose"><span class="eyebrow">Cada cava es distinta</span><h2>Hechas a la medida de cada cliente</h2>
<p>Ninguna de estas cavas es igual a otra: cada una se diseñó para el espacio, el producto y la temperatura de su dueño. Hay cavas de refrigeración para producto fresco, cuartos de congelación, cavas dobles y cuartos fríos industriales dentro de galpones.</p>
<p>Si te gusta alguna, envíanos la foto por WhatsApp con las medidas de tu espacio y te cotizamos una parecida.</p></div></section>
{band("Hola, vi sus proyectos y quiero una cava como esas.", "¿Quieres una cava como estas?")}'''
    shell("/proyectos/", "Proyectos: Cavas Cuarto Instaladas | Refrigeración Team",
          "Fotos de cavas cuarto y cuartos fríos que hemos fabricado e instalado en Venezuela: refrigeración, congelación, cavas dobles e industriales.",
          [("Proyectos", "/proyectos/")], "Cavas cuarto que hemos instalado",
          "Mira algunos de nuestros trabajos: cavas de refrigeración, cuartos de congelación y cuartos fríos industriales hechos a la medida.",
          body, [{"@type": "CollectionPage", "name": "Proyectos de cavas cuarto", "url": f"{BASE}/proyectos/", "about": emp}],
          "Hola, vi sus proyectos y quiero una cava como esas.")

    # /nosotros/
    body = f'''{seccion(h, "equipo", "/nosotros/")}
<section style="background:var(--ice)"><div class="wrap"><span class="eyebrow">Qué hacemos</span><h2>Todo lo que necesitas para el frío de tu negocio</h2>
<div class="bens">
<div class="ben rv"><h3>Cavas cuarto a medida</h3><p>Diseñamos, armamos e instalamos cavas de refrigeración y de congelación. <a href="/cavas-cuarto/">Ver cavas cuarto →</a></p></div>
<div class="ben rv"><h3>Equipos y materiales</h3><p>Unidades condensadoras, compresores, difusores, controles e insumos de marcas reconocidas. <a href="{EQUIPOS}">Ver equipos →</a></p></div>
<div class="ben rv"><h3>Freezers para negocios</h3><p>Freezers y neveras para el punto de venta, como complemento de tu cava. <a href="/freezers-comerciales/">Ver freezers →</a></p></div>
</div></div></section>
{seccion(h, "proceso")}
<section><div class="wrap prose"><span class="eyebrow">Dónde estamos</span><h2>Trabajamos en toda Venezuela</h2>
<p>Llevamos el material y el equipo hasta tu local, estés donde estés. Mira las zonas donde hemos trabajado en la página de <a href="/cobertura/">cobertura</a>, o escríbenos tu ciudad por WhatsApp.</p>
<p>Síguenos en Instagram, <a href="https://www.instagram.com/cavascuartoteam/" target="_blank" rel="noopener">@cavascuartoteam</a>, donde publicamos nuestros trabajos.</p></div></section>
{band("Hola, quiero información sobre sus servicios.")}'''
    shell("/nosotros/", "Quiénes Somos | Refrigeración Team Cavas Cuarto",
          "Conoce al equipo de Refrigeración Team: diseñamos, fabricamos e instalamos cavas cuarto y vendemos equipos de refrigeración en toda Venezuela.",
          [("Nosotros", "/nosotros/")], "Somos Refrigeración Team",
          "Un equipo propio dedicado a las cavas cuarto y la refrigeración comercial: diseñamos tu cava, la armamos, la instalamos y te vendemos los equipos para ella.",
          body, [{"@type": "AboutPage", "name": "Quiénes somos", "url": f"{BASE}/nosotros/", "about": emp}],
          "Hola, quiero información sobre sus servicios.", img="equipo-grupo", imgalt="Equipo de Refrigeración Team junto al camión de trabajo")

    # /cobertura/
    body = f'''{seccion(h, "cobertura", "/cobertura/")}
<section><div class="wrap prose"><span class="eyebrow">Fuera de tu ciudad</span><h2>Cómo trabajamos en tu zona</h2>
<p>Escríbenos tu ciudad o estado, las medidas aproximadas del espacio y lo que vas a guardar. Con eso te enviamos la cotización y coordinamos el traslado del material y del equipo hasta tu local.</p>
<p>Si no sabes las medidas, una foto del espacio ayuda mucho. También puedes usar el <a href="/cotizar/">cotizador</a>: en menos de un minuto nos llega todo por WhatsApp.</p></div></section>
{band("Hola, quiero cotizar una cava cuarto en mi ciudad.")}'''
    shell("/cobertura/", "Cobertura en Toda Venezuela | Refrigeración Team",
          "Fabricamos e instalamos cavas cuarto en toda Venezuela: occidente, los Andes, centro, oriente, Guayana y los llanos. Cotiza en tu ciudad por WhatsApp.",
          [("Nosotros", "/nosotros/"), ("Cobertura", "/cobertura/")], "Instalamos cavas cuarto en toda Venezuela",
          "Llevamos tu cava cuarto hasta tu local, en cualquier estado del país.",
          body, [{"@type": "WebPage", "name": "Cobertura", "url": f"{BASE}/cobertura/", "about": emp}],
          "Hola, quiero cotizar una cava cuarto en mi ciudad.")

    # /cotizar/
    q = [x for x in home_faq if x[0].startswith(("¿Cuánto", "¿Y si no"))]
    tv = re.search(r'<div id="tv".*?</div>', h, re.S).group(0)
    body = f'''{seccion(h, "cotizar")}
{seccion(h, "proceso")}
<section style="background:var(--ice)"><div class="wrap"><span class="eyebrow">Antes de cotizar</span><h2>Dudas comunes</h2>{faq_html(q)}
<p class="more"><a href="/como-elegir-una-cava-cuarto/">Guía: cómo elegir tu cava cuarto →</a><a href="/preguntas-frecuentes/">Más preguntas →</a></p></div></section>'''
    shell("/cotizar/", "Cotiza tu Cava Cuarto por WhatsApp | Refrigeración Team",
          "Pide la cotización de tu cava cuarto en menos de un minuto: cuéntanos tu negocio, la temperatura y las medidas, y te respondemos por WhatsApp.",
          [("Cotizar", "/cotizar/")], "Cotiza tu cava cuarto",
          "Llena el cotizador con lo que sepas y se abrirá tu WhatsApp con el mensaje listo. Si prefieres, escríbenos o llámanos directo.",
          body, [{"@type": "WebPage", "name": "Cotizar cava cuarto", "url": f"{BASE}/cotizar/", "about": emp}, faq_schema(q)],
          "Hola, quiero cotizar una cava cuarto.", extra=tv + "\n")

    # /preguntas-frecuentes/
    vistos, grupos = set(), []
    def grupo(titulo, items, enlace=None):
        out = []
        for qq, aa in items:
            k = re.sub(r"\W+", " ", qq.lower()).strip()
            if k not in vistos: vistos.add(k); out.append((qq, aa))
        if out: grupos.append((titulo, out, enlace))
    grupo("Generales", home_faq)
    grupo("Antes de cotizar", BYSLUG["como-elegir-una-cava-cuarto"]["faq"], ("Guía: cómo elegir tu cava cuarto", "/como-elegir-una-cava-cuarto/"))
    grupo("Refrigeración", BYSLUG["cuarto-de-refrigeracion"]["faq"], ("Cuarto de refrigeración", "/cuarto-de-refrigeracion/"))
    grupo("Congelación", BYSLUG["cuarto-de-congelacion"]["faq"], ("Cuarto de congelación", "/cuarto-de-congelacion/"))
    for s in SECTORES:
        grupo(BYSLUG[s]["nombre"], BYSLUG[s]["faq"], (BYSLUG[s]["h1"], f"/{s}/"))
    grupo("Equipos y materiales", BYSLUG["equipos-y-materiales-para-cavas-cuarto"]["faq"], ("Equipos y materiales", EQUIPOS))
    grupo("Freezers", BYSLUG["freezers-comerciales"]["faq"], ("Freezers comerciales", "/freezers-comerciales/"))
    todas = [x for _, it, _ in grupos for x in it]
    indice = '<p class="more toc">' + "".join(f'<a href="#g{i}">{esc(t)}</a>' for i, (t, _, _) in enumerate(grupos)) + "</p>"
    body = '<section><div class="wrap">' + indice + "".join(
        f'<div class="fgroup" id="g{i}"><h2>{esc(t)}</h2>{faq_html(it)}' + (f'<p class="more"><a href="{e[1]}">{esc(e[0])} →</a></p>' if e else "") + "</div>"
        for i, (t, it, e) in enumerate(grupos)) + "</div></section>\n" + band("Hola, tengo una pregunta sobre las cavas cuarto.", "¿No encontraste tu respuesta?", "Escríbenos por WhatsApp y te respondemos.")
    shell("/preguntas-frecuentes/", "Preguntas Frecuentes sobre Cavas Cuarto | Refrigeración Team",
          "Respuestas sobre cavas cuarto: precio, medidas, temperaturas, instalación, equipos, freezers y cobertura en Venezuela.",
          [("Nosotros", "/nosotros/"), ("Preguntas frecuentes", "/preguntas-frecuentes/")], "Preguntas frecuentes sobre cavas cuarto",
          f"Reunimos las {len(todas)} preguntas que más nos hacen sobre cavas cuarto, cuartos fríos, equipos y freezers.",
          body, [faq_schema(todas)], "Hola, tengo una pregunta sobre las cavas cuarto.")

    # /contacto/
    body = f'''<section><div class="wrap"><div class="ccards">
<a class="ccard wa" data-lugar="contacto" data-wa="Hola, quiero información sobre cavas cuarto." href="#">{WA_ICON}<b>WhatsApp</b><span>0412 1856429</span><small>La forma más rápida de cotizar</small></a>
<a class="ccard" href="tel:+584121856429" data-lugar="contacto-llamar"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg><b>Llamar</b><span>0412 1856429</span><small>Habla directo con nosotros</small></a>
<a class="ccard" href="https://www.instagram.com/cavascuartoteam/" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg><b>Instagram</b><span>@cavascuartoteam</span><small>Mira nuestros trabajos</small></a>
</div></div></section>
<section style="background:var(--ice)"><div class="wrap prose"><span class="eyebrow">Cotización</span><h2>¿Quieres una cotización?</h2>
<p>Usa el <a href="/cotizar/">cotizador</a> o escríbenos por WhatsApp con lo que vas a guardar, la temperatura y las medidas aproximadas del espacio. Atendemos en <a href="/cobertura/">toda Venezuela</a>.</p></div></section>'''
    shell("/contacto/", "Contacto | Refrigeración Team Cavas Cuarto",
          "Escríbenos por WhatsApp o llámanos al 0412 1856429. Cotizamos cavas cuarto, equipos y freezers en toda Venezuela.",
          [("Nosotros", "/nosotros/"), ("Contacto", "/contacto/")], "Contacto",
          "Escríbenos por WhatsApp, llámanos o síguenos en Instagram. Te respondemos con gusto.",
          body, [{"@type": "ContactPage", "name": "Contacto", "url": f"{BASE}/contacto/", "about": emp}],
          "Hola, quiero información sobre cavas cuarto.")

EXTRA_URLS = ["/cavas-cuarto/", "/sectores/", "/proyectos/", "/nosotros/", "/cobertura/", "/cotizar/", "/preguntas-frecuentes/", "/contacto/"]

# ------------------------------------------------------------------- build
make_og()
(SITIO / "js").mkdir(exist_ok=True)
(SITIO / "js" / "wa.js").write_text(WAJS, encoding="utf-8")
(SITIO / "js" / "sitio.js").write_text((AQUI / "sitio.js").read_text(encoding="utf-8"), encoding="utf-8")
# WebP de cada foto (el worker la sirve a los navegadores que la aceptan)
for jp in (SITIO / "img").glob("*.jpg"):
    wp = jp.with_suffix(".webp")
    if not wp.exists() or wp.stat().st_mtime < jp.stat().st_mtime:
        Image.open(jp).convert("RGB").save(wp, "WEBP", quality=74, method=6)
h = (home.replace("{{ICON_COMPRESOR}}", ICON_COMPRESOR).replace("{{ICON_FREEZER}}", ICON_FREEZER).replace("{{ICON_LUCES}}", ICON_LUCES).replace("{{MAPA_VZLA}}", (AQUI / "mapa_vzla.svg.html").read_text(encoding="utf-8")).replace("{{TOPBAR}}", TOPBAR).replace("{{ANALYTICS}}", analytics()).replace("{{ROBOTS}}", robots_meta()).replace("{{BASE}}", BASE).replace("{{FOOTCOLS}}", foot_cols()).replace("{{NAV}}", nav_html("/")))
(SITIO / "index.html").write_text(wa_hrefs(add_dims(h)), encoding="utf-8")
# la página de equipos muestra las tarjetas con fotos y las marcas de la home
eqsec = re.sub(r'\s*<div class="eqs-foot">.*?</div>', "", re.search(r'<section id="equipos".*?</section>', h, re.S).group(0), flags=re.S)
BYSLUG["equipos-y-materiales-para-cavas-cuarto"]["extra"] = eqsec.replace('<section id="equipos" style="background:var(--ice)">', '<section id="equipos" style="background:var(--ice)">').replace('<span class="eyebrow">También vendemos</span>', '<span class="eyebrow">Catálogo</span>').replace('<h2>Todo el material para tu cava cuarto</h2>', '<h2>Equipos y marcas disponibles</h2>') + \
    re.search(r'<section class="marcas" id="marcas">.*?</section>', h, re.S).group(0)
for p in PAGES: build_page(p)
build_extra_pages(h)

urls = ["/"] + EXTRA_URLS + [f"/{p['slug']}/" for p in PAGES]
# lastmod solo cambia cuando cambia el contenido de esa página (registro en lastmod.json)
REG = AQUI / "lastmod.json"
reg = json.loads(REG.read_text()) if REG.exists() else {}
for u in urls:
    hsh = hashlib.sha1((SITIO / u.strip("/") / "index.html").read_bytes()).hexdigest()
    if reg.get(u, {}).get("hash") != hsh: reg[u] = {"hash": hsh, "fecha": HOY}
REG.write_text(json.dumps(reg, indent=1, ensure_ascii=False))
(SITIO / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{reg[u]['fecha']}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
(SITIO / "robots.txt").write_text(("User-agent: *\nAllow: /\n" if INDEXAR else "User-agent: *\nDisallow: /\n") + f"Sitemap: {BASE}/sitemap.xml\n")
(SITIO / "404.html").write_text(head("Página no encontrada | Refrigeración Team", "Esta página no existe.", "/404.html", "", None, canonical=False).replace(robots_meta(), '<meta name="robots" content="noindex">') +
    TOPBAR + wa_hrefs(header("/404")) + '<main><section><div class="wrap" style="text-align:center;padding:60px 0"><h1>Esta página no existe</h1><p class="lead" style="margin:12px auto 24px">Pero tu cava cuarto sí podemos hacerla.</p><a class="btn btn-wa" href="/">Ir al inicio</a></div></section></main>' +
    wa_hrefs(FOOTER + FAB + MBAR + SYMBOL) + SCRIPT, encoding="utf-8")
print("OK:", len(urls), "páginas | INDEXAR =", INDEXAR, "| BASE =", BASE)
