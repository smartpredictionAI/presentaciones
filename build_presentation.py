"""
Parse Encuesta2.xlsx and emit a single responsive HTML presentation.
Branding uses SIGNOS analytics palette (navy, purple, cyan).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import openpyxl

XLSX_PATH = Path(r"c:\Users\mz\Dropbox\toshiba 2021 F\Encuesta2.xlsx")
OUT_INDEX = Path(__file__).resolve().parent / "index.html"

P_START = re.compile(r"^P(\d+)\.\s*(.+)$")
URL_IN_TEXT = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)


def strip_reference_urls(s: str) -> str:
    """Strip bare URLs from labels and notes (keep human-readable text)."""
    t = URL_IN_TEXT.sub("", s)
    t = re.sub(r"\s{2,}", " ", t)
    return t.strip(" ,;—-").strip()


def clean_label(s: str | None) -> str:
    if not s or not isinstance(s, str):
        return ""
    t = re.sub(r"\s*\[[^\]]+\]\s*", " ", s).strip()
    return strip_reference_urls(t)


def is_url_only_cell(val: Any) -> bool:
    if not isinstance(val, str):
        return False
    st = val.strip()
    if not st:
        return False
    return bool(re.match(r"^https?://\S+$", st, re.I)) or bool(
        re.match(r"^www\.\S+$", st, re.I)
    )


def question_from_row(row: list[Any]) -> str:
    for cell in row[1:6]:
        if isinstance(cell, str) and cell.strip():
            return strip_reference_urls(cell.strip())
    return ""


def is_p_header(a: Any) -> bool:
    return isinstance(a, str) and bool(P_START.match(a.strip()))


def row_is_blank(row: list[Any], max_col: int = 8) -> bool:
    for c in row[:max_col]:
        if c is not None and c != "":
            return False
    return True


def looks_like_note(a: Any) -> bool:
    if not isinstance(a, str):
        return False
    t = a.strip()
    if len(t) < 80:
        return False
    if P_START.match(t):
        return False
    return True


def parse_sections(rows: list[list[Any]]) -> list[dict[str, Any]]:
    sections: list[dict[str, Any]] = []
    n = len(rows)
    i = 0
    while i < n:
        row = rows[i]
        a0 = row[0] if row else None
        if not (isinstance(a0, str) and P_START.match(a0.strip())):
            i += 1
            continue

        m = P_START.match(a0.strip())
        assert m
        pid = int(m.group(1))
        short_title = strip_reference_urls(m.group(2).strip())
        full_title = strip_reference_urls(a0.strip())
        question = question_from_row(row)

        i += 1
        notes: list[str] = []
        while i < n:
            r = rows[i]
            ra = r[0] if r else None
            if isinstance(ra, str) and P_START.match(ra.strip()):
                break
            if looks_like_note(ra):
                notes.append(str(ra).strip())
                i += 1
                continue
            break

        if i >= n:
            break

        header = list(rows[i])
        i += 1

        h0 = header[0] if header else None
        h1 = header[1] if len(header) > 1 else None

        columns: list[str] = []
        table_type = "generic"

        if h0 == "Opción" and h1 == "Porcentaje":
            table_type = "simple_pct"
            columns = ["Opción", "Porcentaje"]
        elif h0 == "Autoridad" and h1 == "Conoce":
            table_type = "two_pct"
            columns = ["Autoridad", "Conoce", "No conoce"]
        elif h0 == "Área" and h1 == "Cumple":
            table_type = "three_pct"
            cols = []
            for c in header:
                if c is None:
                    break
                if isinstance(c, str) and c.strip():
                    cols.append(c.strip())
                elif isinstance(c, (int, float)):
                    continue
                else:
                    break
            columns = cols[:4]
        elif h0 == "Autoridad" and isinstance(h1, str) and "Nota" in h1:
            table_type = "grade_bands"
            columns = [
                clean_label(str(x))
                for x in header[:6]
                if x and str(x).strip() and str(x).strip() != "Total"
            ]
            if len(columns) < 4:
                columns = ["Autoridad", "Nota 1-3", "Nota 4-5", "Nota 6-7"]
        elif h0 == "Área" and isinstance(h1, str) and "Ha mejorado" in h1:
            table_type = "evolution"
            cols = []
            for c in header:
                if c is None:
                    continue
                if c == 0:
                    continue
                if isinstance(c, str) and c.strip():
                    cols.append(c.strip())
            columns = cols
        elif h0 in ("Autoridad", "Figura política") and h1 == "Mucha":
            table_type = "credibility"
            cols = []
            for c in header:
                if c is None:
                    continue
                if isinstance(c, str) and c.strip():
                    if c.strip() == "Total":
                        continue
                    cols.append(c.strip())
            columns = cols
        elif h0 == "Institución" and h1 == "Mucha":
            table_type = "credibility"
            columns = [c.strip() for c in header if isinstance(c, str) and c.strip()]
        else:
            columns = [
                clean_label(str(x))
                for x in header
                if x is not None and str(x).strip() != "" and not isinstance(x, (int, float))
            ]
            if not columns:
                columns = ["Col A", "Col B"]

        data_rows: list[dict[str, Any]] = []

        while i < n:
            r = rows[i]
            ra = r[0] if r else None
            if isinstance(ra, str) and P_START.match(ra.strip()):
                break
            if row_is_blank(r):
                i += 1
                continue
            if looks_like_note(ra):
                notes.append(str(ra).strip())
                i += 1
                continue

            if table_type == "simple_pct":
                pct = r[1] if len(r) > 1 else None
                if is_url_only_cell(ra):
                    i += 1
                    continue
                label = clean_label(str(ra)) if ra is not None else ""
                if not label and pct is None:
                    i += 1
                    continue
                if not label:
                    i += 1
                    continue
                data_rows.append({"label": label, "pct": pct})
            elif table_type == "two_pct":
                label = clean_label(str(ra)) if ra is not None else ""
                data_rows.append(
                    {
                        "label": label,
                        "a": r[1] if len(r) > 1 else None,
                        "b": r[2] if len(r) > 2 else None,
                    }
                )
            elif table_type == "three_pct":
                label = clean_label(str(ra)) if ra is not None else ""
                data_rows.append(
                    {
                        "label": label,
                        "c1": r[1],
                        "c2": r[2],
                        "c3": r[3],
                    }
                )
            elif table_type == "grade_bands":
                label = clean_label(str(ra)) if ra is not None else ""
                total_cell = r[4] if len(r) > 4 else None
                data_rows.append(
                    {
                        "label": label,
                        "b1": r[1],
                        "b2": r[2],
                        "b3": r[3],
                        "total": total_cell,
                    }
                )
            elif table_type == "evolution":
                label = clean_label(str(ra)) if ra is not None else ""
                data_rows.append(
                    {
                        "label": label,
                        "v1": r[1],
                        "v2": r[2],
                        "v3": r[3],
                        "v4": r[4],
                        "v5": r[5],
                    }
                )
            elif table_type == "credibility":
                label = clean_label(str(ra)) if ra is not None else ""
                vals: list[float] = []
                for j in range(1, len(r)):
                    cell = r[j]
                    if cell is None:
                        break
                    if isinstance(cell, (int, float)):
                        vals.append(float(cell))
                subcols = columns[1:]
                vals = vals[: len(subcols)]
                row_map: dict[str, Any] = {"label": label}
                for j, key in enumerate(subcols):
                    row_map[key] = vals[j] if j < len(vals) else None
                data_rows.append(row_map)
            else:
                data_rows.append({"raw": [r[j] for j in range(min(len(r), 8))]})

            i += 1

        sections.append(
            {
                "id": pid,
                "title": full_title,
                "short_title": short_title,
                "question": question,
                "table_type": table_type,
                "columns": columns,
                "rows": data_rows,
                "notes": notes,
            }
        )

    return sections


def is_regional_section(section: dict[str, Any]) -> bool:
    """
    True for items tied to the regional module; national block comes first
    when sections are reordered via order_sections_national_first.
    P12 (Reconstrucción Nacional / incendios) is treated as regional per survey design.
    """
    if section.get("id") == 12:
        return True
    blob = " ".join(
        str(section.get(k) or "") for k in ("title", "short_title", "question")
    ).lower()
    if "valparaíso" in blob:
        return True
    if "presupuesto regional" in blob:
        return True
    if "mundaca" in blob and "millones" in blob:
        return True
    return False


def order_sections_national_first(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    national = [s for s in sections if not is_regional_section(s)]
    regional = [s for s in sections if is_regional_section(s)]
    return national + regional


def pct_fmt(v: Any) -> str:
    if v is None:
        return "—"
    try:
        x = float(v)
    except (TypeError, ValueError):
        return str(v)
    return f"{x * 100:.1f}%"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


# Labels sorted last (NS/NR, catch-all options), stable order among themselves.
TAIL_LABEL_RE = re.compile(
    r"(?:^|\b)(?:no\s+sabe|no\s+responde|ns\s*/\s*nr|\botros?\b|\bninguno\b)(?:\b|$)",
    re.IGNORECASE,
)


def is_tail_result_label(label: str) -> bool:
    if not label or not isinstance(label, str):
        return False
    return bool(TAIL_LABEL_RE.search(label.strip()))


def sort_tail_last(
    rows: list[dict[str, Any]],
    sort_key_fn: Any,
    *,
    reverse: bool = True,
) -> list[dict[str, Any]]:
    """Sort rows by numeric key (highest first); tail labels (NS/NR, Otro, etc.) always at end."""
    main: list[dict[str, Any]] = []
    tail: list[dict[str, Any]] = []
    for r in rows:
        lbl = str(r.get("label") or "")
        if is_tail_result_label(lbl):
            tail.append(r)
        else:
            main.append(r)

    def safe_key(r: dict[str, Any]) -> float:
        try:
            v = sort_key_fn(r)
            return float(v) if v is not None else float("-inf")
        except (TypeError, ValueError):
            return float("-inf")

    main.sort(key=safe_key, reverse=reverse)

    def tail_rank(r: dict[str, Any]) -> tuple[int, str]:
        lbl = (r.get("label") or "").lower()
        if re.search(r"\botros?\b", lbl):
            return (0, lbl)
        if "ninguno" in lbl:
            return (1, lbl)
        if re.search(r"no\s+sabe|no\s+responde|ns\s*/\s*nr", lbl):
            return (2, lbl)
        return (3, lbl)

    tail.sort(key=tail_rank)
    return main + tail


def apply_display_sort_to_sections(sections: list[dict[str, Any]]) -> None:
    """Mutate section rows: descending by main metric; NS/NR, Otro, Ninguno last."""
    for s in sections:
        rows: list[dict[str, Any]] = list(s.get("rows") or [])
        if not rows:
            continue
        t = s["table_type"]
        if t == "simple_pct":
            s["rows"] = sort_tail_last(
                rows, lambda r: r.get("pct") if r.get("pct") is not None else None
            )
        elif t == "two_pct":
            s["rows"] = sort_tail_last(
                rows, lambda r: r.get("a") if r.get("a") is not None else None
            )
        elif t == "three_pct":
            s["rows"] = sort_tail_last(
                rows, lambda r: r.get("c1") if r.get("c1") is not None else None
            )
        elif t == "grade_bands":
            s["rows"] = sort_tail_last(
                rows, lambda r: r.get("b3") if r.get("b3") is not None else None
            )
        elif t == "evolution":

            def ev_key(r: dict[str, Any]) -> float | None:
                try:
                    return float(r.get("v1") or 0) + float(r.get("v2") or 0)
                except (TypeError, ValueError):
                    return None

            s["rows"] = sort_tail_last(rows, ev_key)
        elif t == "credibility":
            cols = s.get("columns") or []
            subkeys = cols[1:] if len(cols) > 1 else []

            def cred_key(r: dict[str, Any]) -> float:
                tsum = 0.0
                for k in subkeys[:2]:
                    v = r.get(k)
                    if isinstance(v, (int, float)):
                        tsum += float(v)
                return tsum

            s["rows"] = sort_tail_last(rows, cred_key)


def render_stacked_bar(row: dict[str, Any], keys: list[str], colors: list[str]) -> str:
    parts: list[str] = []
    total = 0.0
    vals: list[tuple[str, float]] = []
    for k in keys:
        v = row.get(k)
        if isinstance(v, (int, float)):
            vals.append((k, float(v)))
            total += float(v)
    if total <= 0:
        total = 1.0
    for k, v in vals:
        w = max(0.0, min(100.0, (v / total) * 100))
        ci = keys.index(k) % len(colors)
        parts.append(
            f'<span class="stack-seg" style="width:{w:.2f}%;background:{colors[ci]}" title="{esc(k)} {pct_fmt(v)}"></span>'
        )
    return '<div class="stack-bar">' + "".join(parts) + "</div>"


def build_html(sections: list[dict[str, Any]]) -> str:
    accent = "#8a56c3"
    accent2 = "#29e3f1"
    stack_colors = [accent, accent2, "#e8a317", "#3d9df0", "#43aa8b", "#7c8aad"]

    nav_items = (
        '<a href="#portada">Portada</a>'
        '<a href="#metodologia">Metodología</a>'
        '<a href="#bloque-regional">Regional</a>'
        + "".join(f'<a href="#p{s["id"]}">P{s["id"]}</a>' for s in sections)
    )

    methodology_section = """
<section class="slide slide-metodologia" id="metodologia" aria-labelledby="metodologia-title">
  <header class="slide-head">
    <span class="pill">Metodología</span>
    <h2 id="metodologia-title">Ficha técnica</h2>
    <p class="lead">Caracterización del levantamiento de datos.</p>
  </header>
  <dl class="ficha-list ficha-list--sheet">
    <div class="ficha-item">
      <dt>Tipo de Encuesta</dt>
      <dd>Encuesta telefónica con selección aleatoria de números.</dd>
    </div>
    <div class="ficha-item">
      <dt>Fecha de Aplicación</dt>
      <dd>Entre el 24 de abril y 2 de mayo de 2026</dd>
    </div>
    <div class="ficha-item">
      <dt>Cantidad de Encuestas</dt>
      <dd>
        1,809 Encuesta nacional
        <span class="sub-line">606 encuestas regionales</span>
      </dd>
    </div>
    <div class="ficha-item">
      <dt>Error para muestra total</dt>
      <dd>
        2,5 puntos porcentuales (muestra nacional)
        <span class="sub-line">3,7 puntos porcentuales (muestra regional)</span>
      </dd>
    </div>
  </dl>
</section>
"""

    body_sections: list[str] = []
    prev_regional = False
    for s in sections:
        cur_regional = is_regional_section(s)
        if cur_regional and not prev_regional:
            body_sections.append(
                """
<section class="slide slide-block-intro" id="bloque-regional" aria-labelledby="titulo-regional">
  <h2 id="titulo-regional">Preguntas regionales</h2>
  <p class="lead">Bloque de contenidos de ámbito regional.</p>
</section>
"""
            )
        prev_regional = cur_regional
        sid = s["id"]
        ttype = s["table_type"]
        rows_html = ""
        chart_html = ""

        if ttype == "simple_pct":
            table_rows = []
            bar_blocks = []
            for dr in s["rows"]:
                if not dr.get("label"):
                    continue
                lbl = esc(dr.get("label", ""))
                pf = pct_fmt(dr.get("pct"))
                table_rows.append(f"<tr><td>{lbl}</td><td class=\"num\">{pf}</td></tr>")
                try:
                    p = float(dr["pct"]) * 100 if dr.get("pct") is not None else 0
                except (TypeError, ValueError):
                    p = 0
                bar_blocks.append(
                    f'<div class="hbar-row"><span class="hbar-label">{lbl}</span>'
                    f'<div class="hbar-track"><span class="hbar-fill" style="width:{p:.1f}%"></span></div>'
                    f'<span class="hbar-pct">{pf}</span></div>'
                )
            rows_html = (
                '<table class="data-table"><thead><tr><th>Opción</th><th>%</th></tr></thead>'
                f"<tbody>{''.join(table_rows)}</tbody></table>"
            )
            chart_html = '<div class="hbar-block">' + "".join(bar_blocks) + "</div>"

        elif ttype == "two_pct":
            table_rows = []
            for dr in s["rows"]:
                table_rows.append(
                    "<tr><td>"
                    + esc(dr.get("label", ""))
                    + "</td><td class=\"num\">"
                    + pct_fmt(dr.get("a"))
                    + "</td><td class=\"num\">"
                    + pct_fmt(dr.get("b"))
                    + "</td></tr>"
                )
            rows_html = (
                '<table class="data-table"><thead><tr><th>Autoridad</th><th>Conoce</th><th>No conoce</th></tr></thead>'
                f"<tbody>{''.join(table_rows)}</tbody></table>"
            )
            bar_blocks = []
            for dr in s["rows"]:
                if not dr.get("label"):
                    continue
                lbl = esc(dr.get("label", ""))
                try:
                    a = float(dr["a"]) * 100 if dr.get("a") is not None else 0
                except (TypeError, ValueError):
                    a = 0
                pa = pct_fmt(dr.get("a"))
                pb = pct_fmt(dr.get("b"))
                bar_blocks.append(
                    f'<div class="hbar-row"><span class="hbar-label">{lbl}</span>'
                    f'<div class="hbar-track duo"><span class="hbar-fill" style="width:{a:.1f}%;background:{accent}"></span>'
                    f'<span class="hbar-fill secondary" style="width:{100-a:.1f}%;background:{accent2}"></span></div>'
                    f'<span class="hbar-pct">{pa} / {pb}</span></div>'
                )
            chart_html = '<div class="hbar-block">' + "".join(bar_blocks) + "</div>"

        elif ttype == "three_pct":
            table_rows = []
            for dr in s["rows"]:
                table_rows.append(
                    "<tr><td>"
                    + esc(dr.get("label", ""))
                    + "</td>"
                    + "".join(
                        f'<td class="num">{pct_fmt(dr.get(k))}</td>'
                        for k in ("c1", "c2", "c3")
                    )
                    + "</tr>"
                )
            rows_html = (
                '<table class="data-table"><thead><tr>'
                + "".join(f"<th>{esc(c)}</th>" for c in s["columns"])
                + "</tr></thead><tbody>"
                + "".join(table_rows)
                + "</tbody></table>"
            )

        elif ttype == "grade_bands":
            table_rows = []
            for dr in s["rows"]:
                table_rows.append(
                    "<tr><td>" + esc(dr.get("label", "")) + "</td>"
                    + "".join(
                        f'<td class="num">{pct_fmt(dr.get(k))}</td>'
                        for k in ("b1", "b2", "b3")
                    )
                    + f'<td class="num">{pct_fmt(dr.get("total"))}</td></tr>'
                )
            cols = s["columns"] + ["Total"]
            rows_html = (
                '<table class="data-table"><thead><tr>'
                + "".join(f"<th>{esc(c)}</th>" for c in cols)
                + "</tr></thead><tbody>"
                + "".join(table_rows)
                + "</tbody></table>"
            )
            chart_html = '<div class="stack-list">'
            keys = ["b1", "b2", "b3"]
            for dr in s["rows"]:
                chart_html += (
                    f'<div class="stack-item"><div class="stack-title">{esc(dr.get("label", ""))}</div>'
                    + render_stacked_bar(dr, keys, stack_colors)
                    + "</div>"
                )
            chart_html += "</div>"

        elif ttype == "evolution":
            cols = s["columns"]
            table_rows = []
            for dr in s["rows"]:
                table_rows.append(
                    "<tr><td>"
                    + esc(dr.get("label", ""))
                    + "</td>"
                    + "".join(
                        f'<td class="num">{pct_fmt(dr.get("v" + str(i + 1)))}</td>'
                        for i in range(5)
                    )
                    + "</tr>"
                )
            rows_html = (
                '<table class="data-table"><thead><tr>'
                + "".join(f"<th>{esc(c)}</th>" for c in cols)
                + "</tr></thead><tbody>"
                + "".join(table_rows)
                + "</tbody></table>"
            )
            chart_html = '<div class="stack-list">'
            vkeys = ["v1", "v2", "v3", "v4", "v5"]
            for dr in s["rows"]:
                chart_html += (
                    f'<div class="stack-item"><div class="stack-title">{esc(dr.get("label", ""))}</div>'
                    + render_stacked_bar(dr, vkeys, stack_colors)
                    + "</div>"
                )
            chart_html += "</div>"

        elif ttype == "credibility":
            cols = s["columns"]
            subkeys = cols[1:]
            table_rows = []
            for dr in s["rows"]:
                cells = (
                    "<tr><td>"
                    + esc(dr.get("label", ""))
                    + "</td>"
                    + "".join(
                        f'<td class="num">{pct_fmt(dr.get(k))}</td>' for k in subkeys
                    )
                    + "</tr>"
                )
                table_rows.append(cells)
            rows_html = (
                '<table class="data-table tight"><thead><tr>'
                + "".join(f"<th>{esc(c)}</th>" for c in cols)
                + "</tr></thead><tbody>"
                + "".join(table_rows)
                + "</tbody></table>"
            )
            chart_html = '<div class="stack-list">'
            for dr in s["rows"]:
                chart_html += (
                    f'<div class="stack-item"><div class="stack-title">{esc(dr.get("label", ""))}</div>'
                    + render_stacked_bar(dr, subkeys, stack_colors)
                    + "</div>"
                )
            chart_html += "</div>"

        else:
            rows_html = "<pre>" + esc(json.dumps(s["rows"], ensure_ascii=False, indent=2)) + "</pre>"

        q = esc(s.get("question", ""))
        title_esc = esc(s["title"])

        body_sections.append(
            f"""
<section class="slide" id="p{sid}" aria-labelledby="t{sid}">
  <header class="slide-head">
    <span class="pill">P{sid}</span>
    <h2 id="t{sid}">{title_esc}</h2>
    {f'<p class="lead">{q}</p>' if q else ''}
  </header>
  <div class="slide-body">
    <div class="panel">{chart_html or ''}</div>
    <div class="panel scroll-x">{rows_html}</div>
  </div>
</section>
"""
        )

    export_sections = [{k: v for k, v in s.items() if k != "notes"} for s in sections]
    data_json = json.dumps(export_sections, ensure_ascii=False, indent=2)

    html_core = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Encuesta SIGNOS analytics</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,600;0,9..40,700&family=Montserrat:wght@500;600;700&display=swap" rel="stylesheet" />
  <style>
    :root {{
      --signos-navy: #004a99;
      --signos-purple: #8a56c3;
      --signos-cyan: #29e3f1;
      --signos-navy-deep: #003671;
      --dk: #1e2d44;
      --accent: var(--signos-purple);
      --accent2: var(--signos-cyan);
      --muted: #6b7c99;
      --surface: #ffffff;
      --bg: linear-gradient(165deg, #e8f3fb 0%, #eef1f8 45%, #e4e9f2 100%);
      --shadow: 0 6px 18px rgba(0, 54, 113, 0.12);
      --radius: 10px;
      --maxw: 920px;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: "DM Sans", system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
      color: var(--dk);
      background: var(--bg);
      line-height: 1.55;
      font-size: clamp(13px, 2.2vw, 15px);
    }}
    a {{ color: var(--signos-navy); text-decoration: none; }}
    a:hover {{ color: var(--signos-purple); text-decoration: underline; }}
    .sticky-head {{
      position: sticky;
      top: 0;
      z-index: 80;
      background: rgba(255, 255, 255, 0.97);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid rgba(0, 74, 153, 0.12);
      box-shadow: 0 2px 14px rgba(0, 54, 113, 0.07);
    }}
    .brand-bar {{
      text-align: center;
      padding: 0.35rem 1rem 0.4rem;
      border-bottom: 1px solid rgba(0, 74, 153, 0.08);
    }}
    .brand-bar a {{
      display: inline-block;
      line-height: 0;
    }}
    .brand-bar .logo-site {{
      height: clamp(26px, 4vw, 34px);
      width: auto;
      max-width: min(220px, 42vw);
      object-fit: contain;
    }}
    .cover-hero {{
      position: relative;
      width: 100%;
      max-width: 900px;
      margin: 0 auto;
      aspect-ratio: 16 / 9;
      max-height: min(48vh, 360px);
      min-height: 200px;
      border-radius: 0 0 var(--radius) var(--radius);
      overflow: hidden;
      box-shadow: var(--shadow);
      scroll-margin-top: 6.5rem;
    }}
    .cover-bg {{
      position: absolute;
      inset: 0;
      background-color: var(--signos-navy);
      background-image: url("assets/cover-signos.png");
      background-position: center center;
      background-size: contain;
      background-repeat: no-repeat;
    }}
    .ficha-list--sheet {{
      margin: 0.75rem 0 0;
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
    }}
    .slide-metodologia .ficha-item dt {{
      font-family: Montserrat, system-ui, sans-serif;
      font-size: 0.68rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      color: var(--signos-purple);
      margin: 0 0 0.12rem;
      text-shadow: none;
    }}
    .slide-metodologia .ficha-item dd {{
      margin: 0;
      font-size: 0.86rem;
      font-weight: 500;
      line-height: 1.45;
      color: var(--dk);
      text-shadow: none;
    }}
    .slide-metodologia .ficha-item dd .sub-line {{
      display: block;
      margin-top: 0.25rem;
      padding-left: 0.65rem;
      border-left: 3px solid var(--signos-cyan);
    }}
    @media (max-width: 640px) {{
      .cover-hero {{
        aspect-ratio: 16 / 9;
        max-height: min(42vh, 280px);
        min-height: 160px;
        border-radius: 0;
      }}
      .cover-bg {{
        background-size: contain;
      }}
    }}
    nav.toc {{
      position: relative;
      z-index: 1;
      background: transparent;
      border-bottom: none;
    }}
    nav.toc .inner {{
      max-width: var(--maxw);
      margin: 0 auto;
      padding: 0.55rem 1rem;
      display: flex;
      flex-wrap: wrap;
      gap: 0.35rem 0.5rem;
      align-items: center;
      font-size: 0.82rem;
    }}
    nav.toc a {{
      padding: 0.2rem 0.55rem;
      border-radius: 999px;
      background: rgba(138, 86, 195, 0.12);
      color: var(--dk);
      font-weight: 600;
    }}
    nav.toc a:hover {{ background: rgba(41, 227, 241, 0.22); text-decoration: none; }}
    main {{ max-width: var(--maxw); margin: 0 auto; padding: 0.85rem 0.75rem 2.5rem; }}
    .slide {{
      background: var(--surface);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding: 0.75rem 0.85rem 0.85rem;
      margin-bottom: 1rem;
      scroll-margin-top: 6.5rem;
      max-width: 100%;
      overflow-x: hidden;
    }}
    .slide-head h2 {{
      margin: 0.25rem 0 0;
      font-size: clamp(0.95rem, 2.4vw, 1.12rem);
      letter-spacing: -0.01em;
      line-height: 1.3;
      word-break: break-word;
    }}
    .pill {{
      display: inline-block;
      font-size: 0.62rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      color: #fff;
      background: linear-gradient(90deg, var(--signos-purple), var(--signos-cyan));
      padding: 0.12rem 0.45rem;
      border-radius: 999px;
    }}
    .lead {{
      margin: 0.45rem 0 0;
      color: #4b5569;
      font-size: 0.82rem;
      line-height: 1.4;
      word-break: break-word;
    }}
    .slide-body {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 0.65rem;
      margin-top: 0.65rem;
    }}
    .panel {{ min-width: 0; max-width: 100%; overflow: hidden; }}
    .scroll-x {{
      overflow-x: auto;
      -webkit-overflow-scrolling: touch;
      max-width: 100%;
    }}
    .data-table {{
      width: 100%;
      max-width: 100%;
      border-collapse: collapse;
      font-size: 0.78rem;
      table-layout: fixed;
    }}
    .data-table th, .data-table td {{
      border: 1px solid rgba(68, 84, 106, 0.12);
      padding: 0.28rem 0.38rem;
      text-align: left;
      vertical-align: top;
      word-wrap: break-word;
      overflow-wrap: anywhere;
    }}
    .data-table th {{
      background: rgba(0, 74, 153, 0.1);
      font-weight: 700;
      white-space: normal;
    }}
    .data-table td:first-child {{
      white-space: normal;
      width: 36%;
    }}
    .data-table td.num {{ text-align: right; font-variant-numeric: tabular-nums; white-space: nowrap; width: auto; }}
    .data-table.tight th, .data-table.tight td {{ font-size: 0.7rem; padding: 0.22rem 0.28rem; }}
    .data-table.tight td:first-child {{ width: 28%; }}
    .hbar-block {{ display: flex; flex-direction: column; gap: 0.35rem; }}
    .hbar-row {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1.6fr) minmax(3.2rem, auto);
      gap: 0.35rem 0.4rem;
      align-items: center;
      max-width: 100%;
    }}
    .hbar-label {{
      font-size: 0.75rem;
      color: #3d475c;
      word-break: break-word;
      overflow-wrap: anywhere;
      line-height: 1.25;
      min-width: 0;
    }}
    .hbar-track {{
      height: 8px;
      border-radius: 999px;
      background: rgba(68, 84, 106, 0.12);
      overflow: hidden;
      display: flex;
    }}
    .hbar-track.duo {{ gap: 0; }}
    .hbar-fill {{
      display: block;
      height: 100%;
      border-radius: 999px;
      background: linear-gradient(90deg, var(--signos-purple), var(--signos-cyan));
      min-width: 2px;
    }}
    .hbar-fill.secondary {{ opacity: 0.9; }}
    .hbar-pct {{
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--dk);
      font-variant-numeric: tabular-nums;
    }}
    .stack-list {{ display: flex; flex-direction: column; gap: 0.5rem; }}
    .stack-title {{
      font-size: 0.75rem;
      font-weight: 600;
      margin-bottom: 0.22rem;
      word-break: break-word;
      overflow-wrap: anywhere;
      line-height: 1.25;
    }}
    .stack-bar {{
      display: flex;
      width: 100%;
      max-width: 100%;
      height: 10px;
      border-radius: 999px;
      overflow: hidden;
      background: rgba(68, 84, 106, 0.08);
    }}
    .stack-seg {{ display: block; height: 100%; min-width: 2px; }}
    .slide-block-intro {{
      text-align: center;
      padding: 0.75rem 1rem 0.85rem;
      background: linear-gradient(
        95deg,
        rgba(138, 86, 195, 0.14),
        rgba(41, 227, 241, 0.12)
      );
      border: 1px solid rgba(0, 74, 153, 0.18);
    }}
    .slide-block-intro h2 {{
      margin: 0;
      font-family: Montserrat, system-ui, sans-serif;
      font-size: clamp(0.95rem, 2.5vw, 1.08rem);
      font-weight: 700;
      color: var(--signos-navy-deep);
      letter-spacing: 0.04em;
      text-transform: uppercase;
    }}
    .slide-block-intro .lead {{ margin: 0.35rem 0 0; font-size: 0.78rem; }}
    footer {{
      text-align: center;
      padding: 1.25rem 0.75rem;
      color: #6b7284;
      font-size: 0.78rem;
    }}
  </style>
</head>
<body>
  <div class="sticky-head">
    <div class="brand-bar">
      <a href="#portada" aria-label="SIGNOS analytics — inicio">
        <img src="assets/logo-signos.png" alt="SIGNOS analytics" class="logo-site" width="200" height="45" decoding="async" />
      </a>
    </div>
    <nav class="toc" aria-label="Índice de preguntas">
      <div class="inner">
        <span style="font-weight:700;margin-right:0.35rem;color:var(--dk)">Ir a:</span>
        {nav_items}
      </div>
    </nav>
  </div>
  <header class="cover-hero" id="portada" aria-label="Portada">
    <div class="cover-bg" role="img" aria-label="SIGNOS analytics — portada institucional"></div>
  </header>
  <main>
    {methodology_section}
    {"".join(body_sections)}
  </main>
  <footer>
    Datos embebidos en JSON. Portada: SIGNOS analytics.
  </footer>
"""

    return (
        html_core
        + '<script type="application/json" id="survey-data">'
        + data_json
        + "</script>\n</body>\n</html>\n"
    )


def main() -> None:
    wb = openpyxl.load_workbook(XLSX_PATH, data_only=True)
    ws = wb.active
    rows = [list(r) for r in ws.iter_rows(values_only=True)]
    sections = order_sections_national_first(parse_sections(rows))
    apply_display_sort_to_sections(sections)
    html = build_html(sections)
    OUT_INDEX.write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_INDEX} with {len(sections)} sections.")


if __name__ == "__main__":
    main()
