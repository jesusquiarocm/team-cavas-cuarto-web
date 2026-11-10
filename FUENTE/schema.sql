-- Base de datos D1 "tcc-leads" (Cloudflare): solicitudes del cotizador y clics de contacto.
-- Aplicar:  cd SITIO && npx wrangler d1 execute tcc-leads --remote --file ../FUENTE/schema.sql
-- Privacidad: no se guarda la IP; "huella" es un hash corto de IP + fecha (sirve solo para frenar spam y cambia cada día).

CREATE TABLE IF NOT EXISTS leads (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  creado      TEXT NOT NULL DEFAULT (datetime('now')),   -- UTC
  nombre      TEXT,
  necesito    TEXT,
  negocio     TEXT,
  temperatura TEXT,
  largo       TEXT,
  ancho       TEXT,
  alto        TEXT,
  ciudad      TEXT,
  con_foto    INTEGER NOT NULL DEFAULT 0,
  pagina      TEXT,
  pais        TEXT,
  huella      TEXT
);
CREATE INDEX IF NOT EXISTS leads_creado ON leads (creado);
CREATE INDEX IF NOT EXISTS leads_huella ON leads (huella, creado);

CREATE TABLE IF NOT EXISTS clics (
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  creado  TEXT NOT NULL DEFAULT (datetime('now')),       -- UTC
  tipo    TEXT NOT NULL,                                  -- whatsapp | llamada | cotizador
  lugar   TEXT,                                           -- botón o sección (hero, cierre, flotante…)
  pagina  TEXT,                                           -- ruta desde la que se hizo clic
  pais    TEXT,
  huella  TEXT
);
CREATE INDEX IF NOT EXISTS clics_creado ON clics (creado);
CREATE INDEX IF NOT EXISTS clics_huella ON clics (huella, creado);
