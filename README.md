# Beer Rock

Web del torneo de beer pong Beer Rock. 1ª edición: sábado 21 de noviembre, 19 hs, Cuba Fátima.

## Archivos

- `index.html`: la web pública (versión de preinscripción). Es la que publica GitHub Pages.
- `mockup.html`: versión completa con datos de ejemplo (tabla, partidos, copas y mesa de control) para mostrar cómo funciona la noche del evento. Es la fuente de `index.html`.
- `build_index.py`: genera `index.html` a partir de `mockup.html`.
- `plantillas/Reglas_Beer_Pong.pdf`: reglas para imprimir.

## Cómo actualizar la web

1. Editá en `build_index.py`:
   - `FORM_URL`: link del Google Form de inscripción.
   - `PRECIO`: valor de la inscripción (vacío deja el que tiene `mockup.html`).
   - `SPOTIFY_TRACKS`: links de temas de Spotify; en cada visita suena uno al azar (lista vacía oculta el botón de música).
2. Corré `python3 build_index.py`.
3. Subí el `index.html` nuevo.

## Formulario de inscripción

- `formulario/crear_formulario.gs`: script de Google Apps Script que crea el Google Form y la planilla de respuestas. Para cada edición nueva, actualizar fecha y valores y ejecutarlo de nuevo.
- `formulario/vista-previa.html`: cómo queda el formulario, con el tipo de cada pregunta.
