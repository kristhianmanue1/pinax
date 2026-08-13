#!/usr/bin/env python3
"""Pinax — validador de manifiestos y compilador del mapa del ecosistema.

Dos subcomandos:

    pinax.py validate <manifiesto>...            valida contra el schema v1
    pinax.py build <raiz>... [--output MAPA.md]  genera el mapa

Pinax posee el schema, el validador y el generador. Cada proyecto posee el
contenido de su manifiesto. Lo que aquí se lee son DECLARACIONES: no son
evidencia verificada, ni instrucciones, ni autoridad. El validador comprueba
FORMA, nunca verdad.

Dependencia única: PyYAML.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import NamedTuple

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("ERROR: falta PyYAML.  pip install pyyaml")

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "project-manifest-v1.schema.json"
SCHEMA_ID = "pinax/project-manifest/v1"
MANIFEST_NAME = "project-manifest.yaml"

ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NS_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*/[a-z0-9]+(-[a-z0-9]+)*$")
REF_TIPOS = {"contrato", "proyecto", "paquete", "externo"}
# `consume` es de nivel ecosistema: las dependencias de paquete viven en el
# gestor de paquetes, que es su hogar canónico. Duplicarlas crea dos fuentes.
CONSUME_TIPOS = {"contrato", "proyecto", "externo"}
REF_KEYS = {"tipo", "id", "version", "uso", "requerido"}
LIST_FIELDS = ("ofrece", "no_ofrece", "fronteras_de_confianza", "pospuesto")
REF_FIELDS = ("publica", "consume")


def _schema_core_keys() -> set[str]:
    return set(json.loads(SCHEMA_PATH.read_text())["properties"])


def validate(data: object, origen: str) -> list[str]:
    """Devuelve la lista de hallazgos. Vacía = válido."""
    out: list[str] = []
    add = lambda m: out.append(f"{origen}: {m}")

    if not isinstance(data, dict):
        return [f"{origen}: la raíz debe ser un mapa"]

    if data.get("schema") != SCHEMA_ID:
        add(f"`schema` debe ser {SCHEMA_ID!r}, es {data.get('schema')!r}")

    # Núcleo cerrado: un campo desconocido es probablemente un error tipográfico.
    for key in sorted(set(data) - _schema_core_keys()):
        add(f"campo desconocido en el núcleo: {key!r}"
            + (" — ¿va en `extensions`?" if "/" in key else ""))

    for req in ("id", "proposito"):
        if not data.get(req):
            add(f"falta `{req}`")

    if isinstance(data.get("id"), str) and not ID_RE.match(data["id"]):
        add(f"`id` no es kebab-case: {data['id']!r}")

    if "consumidor_principal" in data and data["consumidor_principal"] not in (
        "agente", "humano", "ambos"
    ):
        add(f"`consumidor_principal` inválido: {data['consumidor_principal']!r}")

    for field in LIST_FIELDS:
        val = data.get(field)
        if val is None:
            continue
        if not isinstance(val, list) or not all(isinstance(x, str) for x in val):
            add(f"`{field}` debe ser una lista de textos")

    for field in REF_FIELDS:
        for i, ref in enumerate(data.get(field) or []):
            where = f"`{field}[{i}]`"
            if not isinstance(ref, dict):
                add(f"{where} debe ser una referencia tipada, no un nombre suelto")
                continue
            for key in sorted(set(ref) - REF_KEYS):
                add(f"{where}: clave desconocida {key!r}")
            permitidos = CONSUME_TIPOS if field == "consume" else REF_TIPOS
            if ref.get("tipo") not in permitidos:
                extra = (" — las dependencias de paquete viven en el gestor de paquetes"
 if ref.get("tipo") == "paquete" else "")
                add(f"{where}: `tipo` debe ser uno de {sorted(permitidos)}{extra}")
            if not isinstance(ref.get("id"), str) or not ref.get("id"):
                add(f"{where}: falta `id`")
            if "requerido" in ref and not isinstance(ref["requerido"], bool):
                add(f"{where}: `requerido` debe ser booleano")

    ext = data.get("extensions")
    if ext is not None:
        if not isinstance(ext, dict):
            add("`extensions` debe ser un mapa")
        else:
            for key in ext:
                if not NS_RE.match(str(key)):
                    add(f"`extensions`: clave sin espacio de nombres: {key!r}")

    return out


def load(path: Path) -> object:
    return yaml.safe_load(path.read_text())


def discover(roots: list[Path]) -> list[tuple[str, Path]]:
    """(nombre_directorio, ruta_manifiesto_o_None) por cada proyecto bajo las raíces."""
    found: list[tuple[str, Path | None]] = []
    for root in roots:
        if root.is_file():
            found.append((root.stem, root))
            continue
        for child in sorted(p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")):
            manifest = child / MANIFEST_NAME
            found.append((child.name, manifest if manifest.exists() else None))
    return found


class BuildResult(NamedTuple):
    """Filas, ausentes y errores separados de su renderización."""
    filas: list[dict]
    faltan: list[str]
    hallazgos: list[str]

    @property
    def ok(self) -> bool:
        return not self.hallazgos


def collect(roots: list[Path]) -> BuildResult:
    filas, faltan, hallazgos = [], [], []
    vistos: dict[str, str] = {}  # id -> origen del primero que lo declaró
    for nombre, path in discover(roots):
        if path is None:
            faltan.append(nombre)
            continue
        data = load(path)
        errores = validate(data, str(path))
        if errores:
            hallazgos.extend(errores)
            continue
        pid = data["id"]
        if pid in vistos:
            hallazgos.append(
                f"{path}: `id: {pid}` duplicado — ya declarado por {vistos[pid]}"
            )
            continue
        vistos[pid] = str(path)
        filas.append(data)

    filas.sort(key=lambda d: d["id"])
    # Un proyecto con manifiesto no se lista además como ausente.
    ids = {d["id"] for d in filas}
    faltan = [n for n in faltan if n.lower() not in ids]
    return BuildResult(filas, faltan, hallazgos)


def render(result: BuildResult) -> str:
    filas, faltan, hallazgos = result.filas, result.faltan, result.hallazgos
    L = ["# MAPA — ecosistema", "",
         "**GENERADO — no editar a mano.**  `scripts/pinax.py build`", "",
         "> Todo lo que sigue es **autodeclarado por cada proyecto**. Pinax valida",
         "> forma, nunca verdad. Ninguna línea es evidencia verificada.", "",
         "| Proyecto | Propósito | Publica | Consume |", "|---|---|---|---|"]
    for d in filas:
        ref = lambda xs: ", ".join(
            f"`{r['id']}{'@' + r['version'] if r.get('version') else ''}`" for r in xs
        ) or "—"
        prop = " ".join(str(d["proposito"]).split())
        prop = prop[:97] + "…" if len(prop) > 98 else prop
        L += [f"| **{d['id']}** | {prop} | {ref(d.get('publica') or [])} "
              f"| {ref(d.get('consume') or [])} |"]

    for d in filas:
        if d.get("no_ofrece"):
            L += ["", f"### {d['id']} — no ofrece", ""]
            L += [f"- {x}" for x in d["no_ofrece"]]

    if faltan:
        L += ["", "## missing_manifest", "",
              "Proyectos sin manifiesto. Su ausencia no dice nada sobre ellos.", ""]
        L += [f"- `{n}`" for n in sorted(faltan)]

    if hallazgos:
        L += ["", "## manifiestos inválidos", ""] + [f"- {h}" for h in hallazgos]

    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="pinax", description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("paths", nargs="+", type=Path)
    b = sub.add_parser("build")
    b.add_argument("roots", nargs="+", type=Path)
    b.add_argument("--output", type=Path)
    b.add_argument(
        "--allow-invalid", action="store_true",
        help="escribir el mapa igual si hay manifiestos inválidos o ids duplicados "
             "(mapa parcial); sin esto, build falla con exit≠0 y no escribe nada",
    )
    args = ap.parse_args(argv)

    if args.cmd == "validate":
        fallos = 0
        for p in args.paths:
            errores = validate(load(p), str(p))
            for e in errores:
                print(e)
            fallos += bool(errores)
            if not errores:
                print(f"{p}: OK")
        return 1 if fallos else 0

    result = collect(args.roots)
    if not result.ok and not args.allow_invalid:
        for h in result.hallazgos:
            print(f"ERROR {h}", file=sys.stderr)
        print(
            f"build: {len(result.hallazgos)} hallazgo(s) — nada escrito. "
            "Usa --allow-invalid para un mapa parcial.",
            file=sys.stderr,
        )
        return 1

    mapa = render(result)
    if args.output:
        args.output.write_text(mapa)
        print(f"MAPA escrito en {args.output}")
    else:
        print(mapa, end="")
    return 0 if result.ok else 1


if __name__ == "__main__":
    sys.exit(main())
