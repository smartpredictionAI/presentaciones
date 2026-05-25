# Presentaciones SIGNOS (estático)

Sitio estático (HTML + CSS + JS en línea). Las animaciones (`@keyframes`, `IntersectionObserver`, transiciones) se ejecutan en el navegador; no hace falta un paso de build.

## GitHub Pages

1. En el repositorio: **Settings → Pages → Build and deployment**.
2. **Source**: **GitHub Actions** (no “Deploy from branch” con Jekyll si usas este workflow).
3. Haz push a **`main`**: el workflow [Deploy static site to Pages](.github/workflows/static-pages.yml) empaqueta los `.html` de la raíz, la carpeta `assets/` y `.nojekyll` en el artefacto publicado.

Los archivos tienen que estar **commiteados** en `main`; lo que no está en git no se despliega.

## Comprobar localmente

Abre `index.html` desde la raíz del proyecto (o sirve la carpeta con un servidor estático) para comprobar rutas relativas `assets/…`.

## Nota sobre animaciones

Si el sistema tiene **“Reducir movimiento”** (`prefers-reduced-motion: reduce`), algunas laminas desactivan animaciones a propósito por accesibilidad.
