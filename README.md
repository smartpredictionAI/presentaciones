# Presentaciones SIGNOS (estático)

Sitio estático (HTML + CSS + JS en línea). Las animaciones (`@keyframes`, `IntersectionObserver`, transiciones) se ejecutan en el navegador; no hace falta un paso de build.

La portada del sitio (`index.html`) es el hub **Programa Copiapó**: dos láminas (intro + enlace a **Atacama · Vargas** en `presentacion_vargas.html`); el catálogo inferior enlaza el resto de decks. La **última lámina de la serie** es `presentacion_smartgore_atacama_nemoclaw.html` (Programa NemoClaw · GORE Atacama); en `references/` hay un prototipo JSX con pestañas para la misma línea editorial.

## Dos repositorios (política de publicación)

| Remoto | Repositorio | Rol |
|--------|----------------|-----|
| `origin` | [houdasaad/encuesta_signos](https://github.com/houdasaad/encuesta_signos) | **Encuesta / línea base**: conservar sin mezclar la versión unificada de presentaciones si así lo defines con tu equipo. |
| `presentaciones` | [smartpredictionAI/presentaciones](https://github.com/smartpredictionAI/presentaciones) | **Sitio unificado** (catálogo, barra Anterior/Índice/Siguiente, todos los HTML + `assets/` + `.nojekyll`). |

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
2. **Source**: **Deploy from branch** → **main** → **/(root)**. El sitio es estático (`*.html`, `assets/`, `.nojekyll`).
3. Opcional más adelante: si quieres **GitHub Actions** en lugar de publicar desde la rama, necesitas un PAT con alcances **`repo`** **y `workflow`** (para poder actualizar YAML bajo `.github/workflows/`), volver a añadir un workflow tipo `deploy-pages`.

Los archivos tienen que estar **commiteados** en **`main`**; lo que no está en git no se despliega.

## Comprobar localmente

Abre `index.html` desde la raíz del proyecto (o sirve la carpeta con un servidor estático) para comprobar rutas relativas `assets/…`.

## Nota sobre animaciones

Si el sistema tiene **“Reducir movimiento”** (`prefers-reduced-motion: reduce`), algunas laminas desactivan animaciones a propósito por accesibilidad.
