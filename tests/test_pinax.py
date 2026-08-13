#!/usr/bin/env python3
"""Pruebas del validador y del compilador. Casos positivos y negativos.

Ejecutar:  python3 tests/test_pinax.py
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import pinax  # noqa: E402

FIXTURE = ROOT / "fixtures" / "argos.project-manifest.yaml"


def base() -> dict:
    return {
        "schema": "pinax/project-manifest/v1",
        "id": "ejemplo",
        "proposito": "Un propósito suficientemente largo.",
    }


def run(name, fn):
    try:
        fn()
    except AssertionError as e:
        print(f"FAIL {name}: {e}")
        return False
    print(f"PASS {name}")
    return True


def test_fixture_argos_valido():
    errores = pinax.validate(pinax.load(FIXTURE), "fixture")
    assert not errores, errores


def test_minimo_valido():
    assert not pinax.validate(base(), "x")


def test_rechaza_campo_desconocido_en_nucleo():
    d = base() | {"no_ofrce": ["typo"]}
    errores = pinax.validate(d, "x")
    assert any("no_ofrce" in e for e in errores), errores


def test_acepta_extensions_con_namespace():
    d = base() | {"extensions": {"skevi/fase": "F3"}}
    assert not pinax.validate(d, "x")


def test_rechaza_extension_sin_namespace():
    d = base() | {"extensions": {"fase": "F3"}}
    assert any("espacio de nombres" in e for e in pinax.validate(d, "x"))


def test_rechaza_referencia_sin_tipo():
    d = base() | {"publica": ["claim-record-v1"]}
    assert any("referencia tipada" in e for e in pinax.validate(d, "x"))


def test_rechaza_paquete_en_consume():
    d = base() | {"consume": [{"tipo": "paquete", "id": "packaging"}]}
    errores = pinax.validate(d, "x")
    assert any("gestor de paquetes" in e for e in errores), errores


def test_acepta_paquete_en_publica():
    d = base() | {"publica": [{"tipo": "paquete", "id": "argos-epistemic"}]}
    assert not pinax.validate(d, "x")


def test_rechaza_tipo_invalido():
    d = base() | {"publica": [{"tipo": "cosa", "id": "x"}]}
    assert any("`tipo`" in e for e in pinax.validate(d, "x"))


def test_rechaza_schema_ausente_o_distinto():
    d = base(); d["schema"] = "pinax/project-manifest/v2"
    assert any("`schema`" in e for e in pinax.validate(d, "x"))


def test_rechaza_id_no_kebab():
    d = base() | {"id": "Ejemplo_Malo"}
    assert any("kebab-case" in e for e in pinax.validate(d, "x"))


def test_exige_proposito():
    d = base(); del d["proposito"]
    assert any("proposito" in e for e in pinax.validate(d, "x"))


def test_build_es_determinista():
    a = pinax.build([FIXTURE])
    b = pinax.build([FIXTURE])
    assert a == b, "build no es determinista"


def test_build_declara_autodeclaracion():
    assert "autodeclarado" in pinax.build([FIXTURE])


def test_build_marca_missing_manifest(tmp=None):
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "sin-manifiesto").mkdir()
        out = pinax.build([root])
        assert "missing_manifest" in out
        assert "sin-manifiesto" in out


def test_build_reporta_manifiesto_invalido():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / "malo"; p.mkdir()
        (p / pinax.MANIFEST_NAME).write_text("schema: otro\nid: malo\nproposito: xxxxxxxxxx\n")
        out = pinax.build([root])
        assert "manifiestos inválidos" in out


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    ok = sum(run(n, f) for n, f in tests)
    print(f"\n{ok}/{len(tests)} pruebas pasan")
    sys.exit(0 if ok == len(tests) else 1)
