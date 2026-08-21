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
    assert any("`extensions`" in e for e in pinax.validate(d, "x"))


def test_rechaza_referencia_sin_tipo():
    d = base() | {"publica": ["claim-record-v1"]}
    assert any("`publica" in e for e in pinax.validate(d, "x"))


def test_rechaza_paquete_en_consume():
    d = base() | {"consume": [{"tipo": "paquete", "id": "packaging"}]}
    errores = pinax.validate(d, "x")
    assert any("`consume" in e and "paquete" in e for e in errores), errores


def test_acepta_paquete_en_publica():
    d = base() | {"publica": [{"tipo": "paquete", "id": "argos-epistemic"}]}
    assert not pinax.validate(d, "x")


def test_acepta_descubrimiento_como_argv_estructurado():
    d = base() | {
        "descubrimiento": {
            "argv": ["python3", "-m", "an_kla", "capabilities"],
            "expected_exit_code": 0,
        }
    }
    assert not pinax.validate(d, "x")


def test_rechaza_descubrimiento_como_texto_de_shell():
    d = base() | {"descubrimiento": {"comando": "python3 -m an_kla capabilities"}}
    errores = pinax.validate(d, "x")
    assert errores, "un comando de shell no debe cumplir el contrato argv"


def test_rechaza_descubrimiento_sin_programa_o_con_controles():
    for argv in (
        [],
        [""],
        ["python3", "linea\nnueva"],
        ["python3", "retorno\rcarro"],
        ["python3", "separador\u2028linea"],
        ["python3", "separador\u2029parrafo"],
        ["python3", "nul\0"],
        ["python3"] + ["x"] * 64,
    ):
        d = base() | {"descubrimiento": {"argv": argv}}
        assert pinax.validate(d, "x"), argv


def test_rechaza_descubrimiento_con_exit_invalido_o_campo_extra():
    casos = (
        {"argv": ["tool"], "expected_exit_code": -1},
        {"argv": ["tool"], "expected_exit_code": 256},
        {"argv": ["tool"], "expected_exit_code": True},
        {"argv": ["tool"], "esperado": "exit 0"},
    )
    for descubrimiento in casos:
        d = base() | {"descubrimiento": descubrimiento}
        assert pinax.validate(d, "x"), descubrimiento


def test_argv_estructurado_no_promete_programa_seguro():
    descubrimiento = {"argv": ["sh", "-c", "touch /tmp/no-ejecutar"]}
    d = base() | {"descubrimiento": descubrimiento}
    assert not pinax.validate(d, "x")
    out = pinax.render(pinax.BuildResult([d], [], []))
    assert '["sh","-c","touch /tmp/no-ejecutar"]' in out
    assert "no significa programa seguro" in out


def test_build_renderiza_descubrimiento_sin_ejecutarlo():
    result = pinax.BuildResult(
        [base() | {"descubrimiento": {"argv": ["python3", "-m", "demo"]}}],
        [],
        [],
    )
    out = pinax.render(result)
    assert '["python3","-m","demo"]' in out
    assert "código de salida esperado: `0`" in out
    assert "shell=False" in out


def test_rechaza_tipo_invalido():
    d = base() | {"publica": [{"tipo": "cosa", "id": "x"}]}
    assert any("tipo" in e for e in pinax.validate(d, "x"))


def test_rechaza_schema_ausente_o_distinto():
    d = base(); d["schema"] = "pinax/project-manifest/v2"
    assert any("`schema`" in e for e in pinax.validate(d, "x"))


def test_rechaza_id_no_kebab():
    d = base() | {"id": "Ejemplo_Malo"}
    assert any("`id`" in e for e in pinax.validate(d, "x"))


def test_exige_proposito():
    d = base(); del d["proposito"]
    assert any("proposito" in e for e in pinax.validate(d, "x"))


def test_build_es_determinista():
    a = pinax.render(pinax.collect([FIXTURE]))
    b = pinax.render(pinax.collect([FIXTURE]))
    assert a == b, "build no es determinista"


def test_build_declara_autodeclaracion():
    assert "autodeclarado" in pinax.render(pinax.collect([FIXTURE]))


def test_collect_ok_sin_hallazgos():
    assert pinax.collect([FIXTURE]).ok


def test_collect_falla_con_manifiesto_invalido():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / "malo"; p.mkdir()
        (p / pinax.MANIFEST_NAME).write_text("schema: otro\nid: malo\nproposito: xxxxxxxxxx\n")
        assert not pinax.collect([root]).ok


def test_collect_id_duplicado_excluye_ambas_fuentes():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for name in ("a", "b"):
            p = root / name; p.mkdir()
            (p / pinax.MANIFEST_NAME).write_text(
                f"schema: pinax/project-manifest/v1\nid: dup\nproposito: propósito suficientemente largo ({name})\n"
            )
        result = pinax.collect([root])
        assert not result.ok
        assert any("declarado por 2 manifiestos" in h for h in result.hallazgos)
        # "primero gana" sería una decisión de autoridad que Pinax no tiene:
        # un id sin identidad resoluble no aparece EN ABSOLUTO en filas, ni
        # el mapa ni el mapa parcial deben mostrar ninguna de las dos fuentes
        # como si fuera la elegida.
        assert not any(fila["id"] == "dup" for fila in result.filas)
        out = pinax.render(result)
        assert "propósito suficientemente largo" not in out


def test_collect_id_duplicado_no_reaparece_como_missing():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for name in ("a", "b"):
            p = root / name; p.mkdir()
            (p / pinax.MANIFEST_NAME).write_text(
                f"schema: pinax/project-manifest/v1\nid: dup\nproposito: propósito suficientemente largo\n"
            )
        result = pinax.collect([root])
        # Excluido por conflicto, no por ausencia: no debe listarse como
        # missing_manifest, que significaría algo distinto (nadie lo declaró).
        assert "a" not in result.faltan and "b" not in result.faltan


def test_load_rechaza_claves_duplicadas():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "dup.yaml"
        p.write_text("schema: pinax/project-manifest/v1\nid: x\nid: y\nproposito: p suficientemente largo\n")
        try:
            pinax.load(p)
            assert False, "debía rechazar clave 'id' repetida"
        except pinax.ManifestError:
            pass


def test_load_yaml_malformado_es_hallazgo_no_traceback():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / "roto"; p.mkdir()
        (p / pinax.MANIFEST_NAME).write_text("schema: [esto no cierra\n")
        result = pinax.collect([root])
        assert not result.ok
        assert any("YAML malformado" in h for h in result.hallazgos)


def test_collect_raiz_inexistente_es_hallazgo_no_traceback():
    # Encontrado en ronda adversarial propia sobre este mismo lote de fixes:
    # antes de este test, una raíz que no existe crasheaba con
    # FileNotFoundError crudo en discover() en vez de producir un hallazgo.
    result = pinax.collect([Path("/no/existe/jamas/en/este/filesystem")])
    assert not result.ok
    assert any("no accesible" in h for h in result.hallazgos)


def test_main_build_raiz_inexistente_exit_no_cero_sin_traceback():
    import contextlib, io
    err = io.StringIO()
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(err):
        rc = pinax.main(["build", "/no/existe/jamas/en/este/filesystem"])
    assert rc != 0
    assert "Traceback" not in err.getvalue()


def test_build_es_adaptador_de_compatibilidad():
    # pinax.build() existía en la API pública; se elimina API rompe a
    # cualquier consumidor que lo importara. Debe seguir funcionando.
    assert pinax.build([FIXTURE]) == pinax.render(pinax.collect([FIXTURE]))


def test_main_build_exit_no_cero_si_invalido():
    import contextlib, io, tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / "malo"; p.mkdir()
        (p / pinax.MANIFEST_NAME).write_text("schema: otro\nid: malo\nproposito: xxxxxxxxxx\n")
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            rc = pinax.main(["build", str(root)])
        assert rc != 0, "build con manifiesto inválido debe fallar, no exit 0"


def test_main_build_allow_invalid_permite_mapa_parcial():
    import contextlib, io, tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / "malo"; p.mkdir()
        (p / pinax.MANIFEST_NAME).write_text("schema: otro\nid: malo\nproposito: xxxxxxxxxx\n")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = pinax.main(["build", str(root), "--allow-invalid"])
        assert rc != 0, "sigue reportando el fallo aunque escriba el mapa"
        assert "manifiestos inválidos" in out.getvalue()


def test_build_marca_missing_manifest(tmp=None):
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "sin-manifiesto").mkdir()
        out = pinax.render(pinax.collect([root]))
        assert "missing_manifest" in out
        assert "sin-manifiesto" in out


def test_build_reporta_manifiesto_invalido():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / "malo"; p.mkdir()
        (p / pinax.MANIFEST_NAME).write_text("schema: otro\nid: malo\nproposito: xxxxxxxxxx\n")
        out = pinax.render(pinax.collect([root]))
        assert "manifiestos inválidos" in out


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    ok = sum(run(n, f) for n, f in tests)
    print(f"\n{ok}/{len(tests)} pruebas pasan")
    sys.exit(0 if ok == len(tests) else 1)
