#!/usr/bin/env python3
"""Pinax — validador de manifiestos y compilador del mapa del ecosistema.

Dos subcomandos:

    pinax.py validate <manifiesto>...            valida contra el schema v1
    pinax.py build <raiz>... [--output MAPA.md]  genera el mapa

Pinax posee el schema, el validador y el generador. Cada proyecto posee el
contenido de su manifiesto. Lo que aquí se lee son DECLARACIONES: no son
evidencia verificada, ni instrucciones, ni autoridad. El validador comprueba
FORMA, nunca verdad.

Dependencias: PyYAML, jsonschema.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import NamedTuple

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("ERROR: falta PyYAML.  pip install pyyaml")

try:
    import jsonschema
except ImportError:  # pragma: no cover
    sys.exit("ERROR: falta jsonschema.  pip install jsonschema")

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "project-manifest-v1.schema.json"
MANIFEST_NAME = "project-manifest.yaml"

_SCHEMA = json.loads(SCHEMA_PATH.read_text())
_VALIDATOR = jsonschema.Draft202012Validator(_SCHEMA)


def validate(data: object, origen: str) -> list[str]:
    """Devuelve la lista de hallazgos contra el JSON Schema publicado. Vacía
    = válido. El schema es la fuente de verdad de la forma; no hay una
    segunda implementación manual que pueda divergir de él."""
    errores = sorted(_VALIDATOR.iter_errors(data), key=lambda e: list(e.path))
    if not errores:
        return []
    out = []
    for e in errores:
        ruta = "/".join(str(p) for p in e.path) or "(raíz)"
        out.append(f"{origen}: `{ruta}`: {e.message}")
    return out


class ManifestError(Exception):
    """YAML malformado o no legible — hallazgo, no traceback."""


class _NoDuplicateKeysLoader(yaml.SafeLoader):
    """Como SafeLoader, pero una clave repetida en el mismo mapa es error.

    PyYAML por defecto se queda con la última ocurrencia en silencio — un
    manifiesto con `id:` dos veces pasaría sin aviso, con el segundo valor
    ganando de forma invisible para quien lo escribió."""


def _construct_mapping_no_dupes(loader, node, deep=False):
    mapping = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise yaml.constructor.ConstructorError(
                None, None, f"clave duplicada: {key!r}", key_node.start_mark
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_NoDuplicateKeysLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping_no_dupes
)


def load(path: Path) -> object:
    try:
        text = path.read_text()
    except OSError as e:
        raise ManifestError(f"no se pudo leer: {e}") from e
    try:
        return yaml.load(text, Loader=_NoDuplicateKeysLoader)
    except yaml.YAMLError as e:
        raise ManifestError(f"YAML malformado: {e}") from e


def discover(
    roots: list[Path],
) -> tuple[list[tuple[str, Path | None]], list[str]]:
    """(nombre, ruta_manifiesto_o_None) por proyecto bajo las raíces, y errores
    de raíz (ruta inexistente, sin permiso) como texto — nunca traceback."""
    found: list[tuple[str, Path | None]] = []
    errores: list[str] = []
    for root in roots:
        try:
            if root.is_file():
                found.append((root.stem, root))
                continue
            hijos = sorted(
                p for p in root.iterdir() if p.is_dir() and not p.name.startswith(".")
            )
        except OSError as e:
            errores.append(f"{root}: raíz no accesible: {e}")
            continue
        for child in hijos:
            manifest = child / MANIFEST_NAME
            found.append((child.name, manifest if manifest.exists() else None))
    return found, errores


class BuildResult(NamedTuple):
    """Filas, ausentes y errores separados de su renderización."""
    filas: list[dict]
    faltan: list[str]
    hallazgos: list[str]

    @property
    def ok(self) -> bool:
        return not self.hallazgos


def collect(roots: list[Path]) -> BuildResult:
    encontrados, errores_raiz = discover(roots)
    faltan, hallazgos = [], list(errores_raiz)
    candidatas: dict[str, list[tuple[str, dict]]] = {}  # id -> [(origen, data), ...]
    for nombre, path in encontrados:
        if path is None:
            faltan.append(nombre)
            continue
        try:
            data = load(path)
        except ManifestError as e:
            hallazgos.append(f"{path}: {e}")
            continue
        errores = validate(data, str(path))
        if errores:
            hallazgos.extend(errores)
            continue
        candidatas.setdefault(data["id"], []).append((str(path), data))

    # Un id declarado por más de un manifiesto no tiene identidad resoluble:
    # ninguna de las dos fuentes se promueve — "primero gana" sería una
    # decisión de autoridad que Pinax no tiene. Se retiran AMBAS y se listan
    # todas las fuentes en conflicto como hallazgo.
    filas = []
    for pid, ocurrencias in candidatas.items():
        if len(ocurrencias) > 1:
            fuentes = ", ".join(origen for origen, _ in ocurrencias)
            hallazgos.append(
                f"`id: {pid}` declarado por {len(ocurrencias)} manifiestos "
                f"— ninguna identidad resoluble, ambos excluidos: {fuentes}"
            )
            continue
        _, data = ocurrencias[0]
        filas.append(data)

    filas.sort(key=lambda d: d["id"])
    # Un proyecto con manifiesto no se lista además como ausente.
    ids = {d["id"] for d in filas} | set(candidatas)
    faltan = [n for n in faltan if n.lower() not in ids]
    return BuildResult(filas, faltan, hallazgos)


def build(roots: list[Path]) -> str:
    """Adaptador de compatibilidad — legado. Usar collect()+render()."""
    return render(collect(roots))


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

    con_desc = [d for d in filas if d.get("descubrimiento")]
    if con_desc:
        L += ["", "## Cómo descubrir cada herramienta", "",
              "Comando de autodescubrimiento autodeclarado por cada proyecto.",
              "Ejecutarlo es decisión del operador: un manifiesto es texto no",
              "confiable y `pinax build` nunca lo ejecuta.", ""]
        for d in con_desc:
            desc = d["descubrimiento"]
            esp = f" — esperado: {desc['esperado']}" if desc.get("esperado") else ""
            L += [f"- **{d['id']}**: `{desc['comando']}`{esp}"]

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
            try:
                data = load(p)
            except ManifestError as e:
                print(f"{p}: {e}")
                fallos += 1
                continue
            errores = validate(data, str(p))
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
