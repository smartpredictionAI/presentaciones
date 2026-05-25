# Presentaciones SIGNOS (estático)

Sitio estático (HTML + CSS + JS en línea). Las animaciones (`@keyframes`, `IntersectionObserver`, transiciones) se ejecutan en el navegador; no hace falta un paso de build.

La encuesta **nacional** vive sólo en `index.html` (un solo HTML; no hay copia paralela tipo “archivo”).

## Repositorio

La organización canónica es **smartpredictionAI** (cuenta/org de producción).

- Opción típica: crea **`https://github.com/smartpredictionAI/encuesta_signos`** (repositorio vacío en GitHub). Luego enlaza este clon (`git remote set-url origin https://github.com/smartpredictionAI/encuesta_signos.git`) y ejecuta `git push -u origin main`.
- Si ya publicas desde otro nombre de repo dentro de esa org (p. ej. `presentaciones`), usa esa URL como `origin` en su lugar.

Necesitas un **personal access token** con permiso **`repo`** (y SSO aprobado si la org usa SAML) ligado a la cuenta que sea **propietaria o mantenedora** de ese repositorio; el `403`/“permission denied” casi siempre es token o SSO.

## GitHub Pages

1. En el repositorio: **Settings → Pages → Build and deployment**.
2. **Source**: **GitHub Actions** (no “Deploy from branch” con Jekyll si usas este workflow).
3. Haz push a **`main`**: el workflow [Deploy static site to Pages](.github/workflows/static-pages.yml) empaqueta los `.html` de la raíz, la carpeta `assets/` y `.nojekyll` en el artefacto publicado.

Los archivos tienen que estar **commiteados** en `main`; lo que no está en git no se despliega.

## Comprobar localmente

Abre `index.html` desde la raíz del proyecto (o sirve la carpeta con un servidor estático) para comprobar rutas relativas `assets/…`.

## Nota sobre animaciones

Si el sistema tiene **“Reducir movimiento”** (`prefers-reduced-motion: reduce`), algunas laminas desactivan animaciones a propósito por accesibilidad.
