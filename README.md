# Presentaciones SIGNOS (estático)

Sitio estático (HTML + CSS + JS en línea). Las animaciones (`@keyframes`, `IntersectionObserver`, transiciones) se ejecutan en el navegador; no hace falta un paso de build.

La encuesta **nacional unificada** en este proyecto vive sólo en `index.html` (sin copia `presentacion_encuesta.html`; la cadena navega hacia los decks regionales y temáticos).

## Dos repositorios (política de publicación)

| Remoto | Repositorio | Rol |
|--------|----------------|-----|
| `origin` | [houdasaad/encuesta_signos](https://github.com/houdasaad/encuesta_signos) | **Encuesta / línea base**: conservar sin mezclar la versión unificada de presentaciones si así lo defines con tu equipo. |
| `presentaciones` | [smartpredictionAI/presentaciones](https://github.com/smartpredictionAI/presentaciones) | **Sitio unificado** (catálogo, barra Anterior/Índice/Siguiente, todos los HTML + `assets/` + workflow de Pages). |

Configuración esperada en este clon:

```bash
git remote -v
# origin        https://github.com/houdasaad/encuesta_signos.git
# presentaciones https://github.com/smartpredictionAI/presentaciones.git
```

### Publicar la versión unificada (smartprediction)

Tras commitear en `main`:

```bash
git push presentaciones main
```

La primera vez, si el historial de `presentaciones` no es ancestro de tu `main`, Git rechazará el push (non-fast-forward). Entonces o bien haces un merge planificado, o —solo si quieres **reemplazar** el contenido remoto de `presentaciones` con este árbol— consulta con el equipo antes de usar `git push --force-with-lease presentaciones main`.

**No** uses `git push origin main` para “actualizar la encuesta unificada” si la política es dejar **`origin` (houdasaad)** tal como está para la primera encuesta; sube la unificación **sólo** a `presentaciones`.

Autenticación: PAT con alcance **`repo`** (y SSO aprobado en la org si aplica) para la cuenta que tenga push en cada remoto.

## GitHub Pages (repositorio `presentaciones`)

1. En [smartpredictionAI/presentaciones](https://github.com/smartpredictionAI/presentaciones): **Settings → Pages → Build and deployment**.
2. **Source**: **GitHub Actions** (workflow [`.github/workflows/static-pages.yml`](.github/workflows/static-pages.yml) de este proyecto).
3. Cada push a **`main`** en `presentaciones` dispara el despliegue; el artefacto incluye los `.html` de la raíz, `assets/` y `.nojekyll`.

Los archivos tienen que estar **commiteados** en la rama que empujes; lo que no está en git no se despliega.

## Comprobar localmente

Abre `index.html` desde la raíz del proyecto (o sirve la carpeta con un servidor estático) para comprobar rutas relativas `assets/…`.

## Nota sobre animaciones

Si el sistema tiene **“Reducir movimiento”** (`prefers-reduced-motion: reduce`), algunas laminas desactivan animaciones a propósito por accesibilidad.
