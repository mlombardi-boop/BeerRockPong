"""Arma index.html (versión de preinscripción para GitHub Pages) a partir de mockup.html.
También regenera beer-rock.html (el mockup completo como documento descargable).

Uso: python3 build_index.py
Antes de publicar: poner el link real del Google Form en FORM_URL y el valor en PRECIO.
"""
import re
from pathlib import Path

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSe2-UFo3NuBwShoPakJW8BhoWTfUJuiqe88d8PO619on25b4Q/viewform"
PRECIO = ""  # vacío deja el valor que tiene mockup.html; si no, reemplaza el texto de los dos lugares
SPOTIFY_URL = "https://open.spotify.com/intl-es/track/6UdCeS92BsXBNoITIxVqdi"  # link de un tema o playlist (Spotify → Compartir → Copiar link); vacío no muestra el botón de música

here = Path(__file__).parent
src = (here / "mockup.html").read_text()

HEAD = ('<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
        '<style>body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n')


def as_document(page):
    marker = '<header class="top">'
    if page.count(marker) != 1:
        raise SystemExit("No encontré el header para separar <head> y <body>")
    return HEAD + page.replace(marker, "</head>\n<body>\n" + marker) + "\n</body>\n</html>\n"


(here / "beer-rock.html").write_text(as_document(src))

s = src


def sub(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Esperaba {count} y encontré {n}: {old[:60]!r}")
    s = s.replace(old, new)


form = f'href="{FORM_URL}" target="_blank" rel="noopener"'

# Navegación: sin Admin y sin punto "en vivo"
sub('      <a href="#admin" data-nav="admin">Admin</a>\n', "")
sub('<a href="#torneo" data-nav="torneo"><i class="live-dot" aria-hidden="true"></i>Torneo activo</a>',
    '<a href="#torneo" data-nav="torneo">Torneo activo</a>')

# Ticker con la info del evento en lugar de resultados
sub('<div class="ticker" aria-label="Últimos resultados">', '<div class="ticker" aria-label="Datos del evento">')
sub('<div class="tag"><i class="live-dot" aria-hidden="true"></i>En vivo</div>', '<div class="tag">1ª edición</div>')

# Botones de inscripción al formulario
sub('<a class="btn primary" href="#inicio" id="cta-insc">Inscribí tu equipo</a>',
    f'<a class="btn primary" {form}>Inscribí tu equipo</a>')
sub('<a class="btn primary insc-btn" href="#inicio">Inscribí tu equipo</a>',
    f'<a class="btn primary" {form}>Inscribí tu equipo</a>')
sub('<a class="btn ghost" href="#torneo">Ver torneo en vivo</a>', '<a class="btn ghost" href="#reglamento">Ver reglamento</a>')
sub('        <div class="cupo-big">Quedan pocos cupos</div>\n',
    f'        <div class="cupo-big">Quedan pocos cupos</div>\n        <a class="btn primary" {form} style="justify-content:center;margin-top:6px">Inscribirme</a>\n')
if PRECIO:
    s = re.sub(r"<span class=\"precio\">[^<]*</span>", f"<span class=\"precio\">{PRECIO}</span>", s)

# Torneo activo: pantalla previa al evento
s = re.sub(r'(<section class="view" id="v-torneo" hidden>).*?(</section>)',
    lambda m: m.group(1) + f'''
  <div class="eyebrow">Edición #1 · Cuba Fátima · Sábado 21/11 · 19 hs</div>
  <h2>Torneo <span style="color:var(--orange)">activo</span></h2>
  <div class="op" style="margin-top:18px;max-width:720px">
    <b>Arranca el día del evento</b>
    <p class="muted" style="margin:0">Esa noche vas a ver acá, en vivo, la tabla general, los partidos de cada mesa, las llaves de las cinco copas y todos los equipos con sus integrantes.</p>
    <div class="cta" style="margin-top:8px"><a class="btn primary" {form}>Inscribí tu equipo</a><a class="btn ghost" href="#reglamento">Ver reglamento</a></div>
  </div>
''' + m.group(2), s, count=1, flags=re.S)

# Sin sección Admin
s, n = re.subn(r'<!-- ADMIN -->\n<section class="view" id="v-admin" hidden>.*?</section>\n', '', s, count=1, flags=re.S)
if n != 1:
    raise SystemExit("No encontré la sección Admin")
sub("const VIEWS=['inicio','torneo','ediciones','reglamento','admin'];", "const VIEWS=['inicio','torneo','ediciones','reglamento'];")
sub("  if(b.id==='cta-insc'||b.classList.contains('insc-btn')){e.preventDefault();toast('En la web real abre el formulario de inscripción y el pago');return}\n", "")

# Arranque: sin datos simulados
sub("renderEdiciones();\nrenderAll();\nroute();", """const INFO=['Sábado 21/11','Cuba Fátima','19 hs','Toca La Curiosa en el medio tiempo','After cachengoso','Quedan pocos cupos','El que pierde, toma.'];
$('#ticker').innerHTML=INFO.concat(INFO).map(x=>`<span><b>${esc(x)}</b></span>`).join('');
$('#eds').innerHTML=`<div class="edcard"><div class="big">#1</div><div><div class="status-line" style="margin:0 0 6px"><span class="pill warn">Inscripciones abiertas</span><span class="pill">Equipos de 3</span></div><h3>Edición inaugural</h3><p class="muted" style="margin:4px 0 0">Cuba Fátima · Sábado 21 de noviembre · 19 hs</p></div></div>`;
route();""")

# Botón flotante de música con el reproductor de Spotify (abierto al cargar la página)
if SPOTIFY_URL:
    m = re.search(r"open\.spotify\.com/(?:intl-[a-z]+/)?(track|playlist|album)/([A-Za-z0-9]+)", SPOTIFY_URL)
    if not m:
        raise SystemExit(f"No reconozco el link de Spotify: {SPOTIFY_URL}")
    kind, sid = m.groups()
    uri = f"spotify:{kind}:{sid}"
    height = 80 if kind == "track" else 152
    s += f'''
<style>
.music-btn{{position:fixed;right:calc(16px + env(safe-area-inset-right,0px));bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:40;width:56px;height:56px;border-radius:50%;border:0;background:var(--orange);color:#1A0B00;display:grid;place-items:center;box-shadow:0 8px 24px rgba(0,0,0,.45)}}
.music-btn[aria-expanded="true"]{{background:var(--sky);color:var(--night)}}
.music-card{{position:fixed;right:calc(16px + env(safe-area-inset-right,0px));bottom:calc(84px + env(safe-area-inset-bottom,0px));z-index:40;width:min(340px,calc(100vw - 32px));background:var(--court);border:1px solid var(--line);border-radius:14px;padding:8px;box-shadow:0 14px 34px rgba(0,0,0,.5)}}
.music-card .mh{{display:flex;justify-content:space-between;align-items:center;padding:2px 4px 8px}}
.music-card .mh button{{border:0;background:none;color:var(--muted);font-size:24px;line-height:1;padding:0 4px}}
.music-card iframe{{display:block;width:100%;height:{height}px;border:0;border-radius:12px}}
</style>
<div class="music-card" id="music-card"><div class="mh"><span class="lbl">Rock para la previa</span><button id="music-close" aria-label="Cerrar reproductor">×</button></div><div id="music-slot"><div id="sp-embed"></div></div></div>
<button class="music-btn" id="music-btn" aria-label="Música" aria-expanded="true" aria-controls="music-card"><svg width="26" height="26" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M9 3v11.6A3.5 3.5 0 1 0 11 18V8h7V3H9Z"/></svg></button>
<script>
/* El reproductor carga abierto y la canción arranca con el primer toque en cualquier parte de la página
   (los navegadores no dejan reproducir sonido antes de que el visitante interactúe). */
(()=>{{const btn=document.getElementById('music-btn'),card=document.getElementById('music-card');
let ctrl=null,pending=false,started=false;
const toggle=open=>{{card.hidden=!open;btn.setAttribute('aria-expanded',open)}};
btn.addEventListener('click',()=>toggle(card.hidden));
document.getElementById('music-close').addEventListener('click',()=>toggle(false));
const EV=['click','touchend','keydown'];
const stop=()=>EV.forEach(e=>document.removeEventListener(e,kick,true));
function kick(){{if(started)return;if(!ctrl){{pending=true;return}}started=true;stop();try{{ctrl.play()}}catch(e){{}}}}
EV.forEach(e=>document.addEventListener(e,kick,true));
window.onSpotifyIframeApiReady=api=>{{
  api.createController(document.getElementById('sp-embed'),{{uri:'{uri}',width:'100%',height:{height}}},c=>{{
    ctrl=c;
    c.addListener('playback_update',ev=>{{if(ev&&ev.data&&!ev.data.isPaused){{started=true;stop()}}}});
    if(pending)kick();
  }});
}};
const sc=document.createElement('script');sc.src='https://open.spotify.com/embed/iframe-api/v1';sc.async=true;document.head.appendChild(sc);
}})();
</script>
'''

(here / "index.html").write_text(as_document(s))
print("index.html y beer-rock.html listos")
