#!/usr/bin/env python3
"""Genera el sitio de Refrigeración Team en ../SITIO a partir de home.src.html.

Uso:  python3 build_web.py
Al publicar con dominio real: INDEXAR = True y BASE = "https://tudominio.com", correr de nuevo.
"""
import html, json, re, datetime
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

const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } }), {threshold:.12});
document.querySelectorAll(".rv").forEach(el => io.observe(el));
const yr = document.getElementById("yr"); if (yr) yr.textContent = new Date().getFullYear();
''' % WHATSAPP

def foot_links():
    items = [("/equipos-y-materiales-para-cavas-cuarto/", "Equipos y materiales"), ("/freezers-comerciales/", "Freezers"), ("/cuarto-de-refrigeracion/", "Cuarto de refrigeración"), ("/cuarto-de-congelacion/", "Cuarto de congelación"),
             ("/cavas-cuarto-carniceria/", "Para carnicerías"), ("/cuartos-frios-pescaderia/", "Para pescaderías"),
             ("/cava-cuarto-restaurante/", "Para restaurantes"), ("/como-elegir-una-cava-cuarto/", "Cómo elegir tu cava")]
    return "".join(f'<li><a href="{u}">{t}</a></li>' for u, t in items)

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
    logo = Image.open(SITIO / "img/logo.png").convert("RGBA"); logo.thumbnail((170, 170))
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
HEADER = re.search(r"<header>.*?</header>", home, re.S).group(0).replace('href="#inicio"', 'href="/"')
HEADER = re.sub(r'href="#(servicios|equipos|temperaturas|negocios|trabajos|cotizar|faq)"', r'href="/#\1"', HEADER)
FOOTER = re.search(r"<footer>.*?</footer>", home, re.S).group(0).replace("{{FOOTLINKS}}", foot_links())
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
"""

def head(title, desc, path, img, schema):
    url = f"{BASE}{path}"
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{robots_meta()}
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0040A0">
<meta property="og:type" content="website"><meta property="og:locale" content="es_VE">
<meta property="og:site_name" content="Refrigeración Team">
<meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" href="/img/icon.png"><link rel="apple-touch-icon" href="/img/icon.png">
{analytics()}{FONTS}
<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
"""

SCRIPT = '<script src="/js/wa.js"></script>\n</body>\n</html>\n'

WA_ICON = '<svg viewBox="0 0 32 32" fill="currentColor" aria-hidden="true"><use href="#i-wa"/></svg>'

def build_page(p):
    path = f"/{p['slug']}/"
    business = {"@type": "LocalBusiness", "name": "Refrigeración Team Cavas Cuarto", "telephone": "+584121856429", "url": f"{BASE}/"}
    schema = {"@context": "https://schema.org", "@graph": [
        {"@type": "Service", "name": p["h1"], "description": p["desc"], "serviceType": "Fabricación e instalación de cavas cuarto",
         "provider": business, "areaServed": {"@type": "Country", "name": "Venezuela"}, "url": f"{BASE}{path}"},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Inicio", "item": f"{BASE}/"},
            {"@type": "ListItem", "position": 2, "name": p["nombre"], "item": f"{BASE}{path}"}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p["faq"]]}]}
    o = head(p["title"], p["desc"], path, p["img"], schema) + TOPBAR + "\n" + HEADER + "\n<main>\n"
    o += f"""<section class="phero on-dark"><div class="wrap grid"><div>
<nav class="crumbs" aria-label="Ruta"><a href="/">Inicio</a> › {esc(p['nombre'])}</nav>
<h1>{esc(p['h1'])}</h1>
<p class="sub">{esc(p['intro'])}</p>
<div style="display:flex;flex-wrap:wrap;gap:12px"><a class="btn btn-wa" data-lugar="hero" data-wa="{esc(p['wa'])}" href="#">{WA_ICON}Cotizar por WhatsApp</a><a class="btn btn-ghost" href="tel:+584121856429" data-lugar="hero-llamar">Llamar ahora</a></div>
</div><div class="ph{' eqph' if p.get('icon') else ''}">{p['icon'] if p.get('icon') else f'<img src="/img/{p["img"]}.jpg" alt="{esc(p["imgalt"])}" fetchpriority="high">'}</div></div></section>
<section><div class="wrap"><span class="eyebrow">{p.get('ben_eyebrow') or ('Pasos a seguir' if p.get('guia') else 'Por qué una cava cuarto')}</span>
<h2>{p.get('ben_h2') or ('Qué tener claro antes de cotizar' if p.get('guia') else 'Lo que ganas con tu cava cuarto')}</h2>
<div class="bens">{''.join(f'<div class="ben rv"><h3>{esc(h)}</h3><p>{esc(t)}</p></div>' for h, t in p['ben'])}</div></div></section>
<section style="padding-top:0"><div class="wrap"><div class="tempbox rv"><h2 style="font-size:1.5rem">{esc(p['temp'][0])}</h2>
<p class="lead" style="margin-top:6px">{esc(p['temp'][1])}</p>
<ul>{''.join(f'<li>{esc(i)}</li>' for i in p['items'])}</ul></div></div></section>
<section style="background:var(--ice)"><div class="wrap"><span class="eyebrow">Preguntas frecuentes</span><h2>Dudas comunes</h2>
<div class="faq">{''.join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in p['faq'])}</div></div></section>
<section><div class="wrap"><div class="band on-dark"><h2>Cuéntanos qué necesitas y te cotizamos</h2>
<p>Escríbenos por WhatsApp con tus medidas aproximadas y lo que vas a guardar. Si no las sabes, te ayudamos.</p>
<a class="btn btn-wa" data-lugar="cierre" data-wa="{esc(p['wa'])}" href="#">{WA_ICON}Escribir por WhatsApp</a></div>
<h2 style="font-size:1.4rem;margin-top:44px">También te puede interesar</h2>
<div class="rel">{''.join(f'<a href="/{r}/">{esc(BYSLUG[r]["h1"])}<small>Ver más →</small></a>' for r in p['rel'])}</div></div></section>
</main>
""" + FOOTER + "\n" + FAB + "\n" + MBAR + "\n" + SYMBOL + "\n" + SCRIPT
    d = SITIO / p["slug"]; d.mkdir(exist_ok=True)
    (d / "index.html").write_text(add_dims(o), encoding="utf-8")

# ------------------------------------------------------------------- build
make_og()
(SITIO / "js").mkdir(exist_ok=True)
(SITIO / "js" / "wa.js").write_text(WAJS, encoding="utf-8")
h = (home.replace("{{ICON_COMPRESOR}}", ICON_COMPRESOR).replace("{{ICON_FREEZER}}", ICON_FREEZER).replace("{{ICON_LUCES}}", ICON_LUCES).replace("{{MAPA_VZLA}}", (AQUI / "mapa_vzla.svg.html").read_text(encoding="utf-8")).replace("{{TOPBAR}}", TOPBAR).replace("{{ANALYTICS}}", analytics()).replace("{{ROBOTS}}", robots_meta()).replace("{{BASE}}", BASE).replace("{{FOOTLINKS}}", foot_links()))
(SITIO / "index.html").write_text(add_dims(h), encoding="utf-8")
for p in PAGES: build_page(p)

urls = ["/"] + [f"/{p['slug']}/" for p in PAGES]
(SITIO / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
    "".join(f"<url><loc>{BASE}{u}</loc><lastmod>{HOY}</lastmod><priority>{'1.0' if u=='/' else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
(SITIO / "robots.txt").write_text(("User-agent: *\nAllow: /\n" if INDEXAR else "User-agent: *\nDisallow: /\n") + f"Sitemap: {BASE}/sitemap.xml\n")
(SITIO / "404.html").write_text(head("Página no encontrada | Refrigeración Team", "Esta página no existe.", "/404.html", "", {"@context": "https://schema.org"}).replace(robots_meta(), '<meta name="robots" content="noindex">') +
    HEADER + '<main><section><div class="wrap" style="text-align:center;padding:60px 0"><h1>Esta página no existe</h1><p class="lead" style="margin:12px auto 24px">Pero tu cava cuarto sí podemos hacerla.</p><a class="btn btn-wa" href="/">Ir al inicio</a></div></section></main>' +
    FOOTER + FAB + SYMBOL + SCRIPT, encoding="utf-8")
(SITIO / "netlify.toml").write_text("""[[headers]]
  for = "/img/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
[[headers]]
  for = "/js/*"
  [headers.values]
    Cache-Control = "public, max-age=3600"
[[headers]]
  for = "/video/*"
  [headers.values]
    Cache-Control = "public, max-age=31536000, immutable"
[[headers]]
  for = "/*"
  [headers.values]
    X-Content-Type-Options = "nosniff"
    Referrer-Policy = "strict-origin-when-cross-origin"
[[redirects]]
  from = "/*"
  to = "/404.html"
  status = 404
""")
print("OK:", len(PAGES) + 1, "páginas | INDEXAR =", INDEXAR, "| BASE =", BASE)
