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
   - `SPOTIFY_URL`: link de un tema o playlist de Spotify para el botón de música (vacío lo oculta).
2. Corré `python3 build_index.py`.
3. Subí el `index.html` nuevo.
