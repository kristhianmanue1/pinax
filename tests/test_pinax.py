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
        p = root / "sin-manifiesto"
        p.mkdir()
        (p / ".git").mkdir()  # repo propio sin manifiesto: sí es un proyecto
        out = pinax.render(pinax.collect([root]))
        assert "missing_manifest" in out
        assert "sin-manifiesto" in out


def test_directorio_sin_git_ni_manifiesto_no_es_proyecto():
    # Un hijo que no trae manifiesto ni .git propio (docs/, src/, tests/ de un
    # repo convencional) no es un proyecto: listarlo como missing_manifest
    # sería ruido que devalúa la señal de adopción.
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for ruido in ("docs", "src", "tests"):
            (root / ruido).mkdir()
        result = pinax.collect([root])
        assert result.faltan == [], result.faltan
        assert "missing_manifest" not in pinax.render(result)


def test_repo_git_sin_manifiesto_cuenta_como_missing():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / "proyecto-real"; p.mkdir()
        (p / ".git").mkdir()
        result = pinax.collect([root])
        assert result.faltan == ["proyecto-real"], result.faltan


def test_build_reporta_manifiesto_invalido():
    import tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / "malo"; p.mkdir()
        (p / pinax.MANIFEST_NAME).write_text("schema: otro\nid: malo\nproposito: xxxxxxxxxx\n")
        out = pinax.render(pinax.collect([root]))
        assert "manifiestos inválidos" in out


# --- lint: consistencia del grafo cosechado ---


def _fila(**extra):
    d = base() | extra
    return d


def test_lint_consume_proyecto_sin_manifiesto():
    filas = [_fila(consume=[{"tipo": "proyecto", "id": "inexistente"}])]
    h = pinax.lint_filas(filas)
    assert any("consume proyecto `inexistente`" in x for x in h), h


def test_lint_consume_proyecto_resuelto_no_halla():
    filas = [
        _fila(id="alfa"),
        _fila(id="beta", consume=[{"tipo": "proyecto", "id": "alfa"}]),
    ]
    assert pinax.lint_filas(filas) == []


def test_lint_consume_contrato_nadie_publica():
    filas = [_fila(consume=[{"tipo": "contrato", "id": "nadie/x-v1"}])]
    h = pinax.lint_filas(filas)
    assert any("que ningún manifiesto cosechado publica" in x for x in h), h


def test_lint_consume_contrato_resuelto_no_halla():
    filas = [
        _fila(id="alfa", publica=[{"tipo": "contrato", "id": "alfa/x-v1"}]),
        _fila(id="beta", consume=[{"tipo": "contrato", "id": "alfa/x-v1"}]),
    ]
    assert pinax.lint_filas(filas) == []


def test_lint_consume_externo_no_se_comprueba():
    # Externo es externo por definición: no hay manifiesto que esperar.
    filas = [_fila(consume=[{"tipo": "externo", "id": "tmux"}])]
    assert pinax.lint_filas(filas) == []


def test_lint_contrato_publicado_por_dos_proyectos():
    filas = [
        _fila(id="alfa", publica=[{"tipo": "contrato", "id": "x/v1"}]),
        _fila(id="beta", publica=[{"tipo": "contrato", "id": "x/v1"}]),
    ]
    h = pinax.lint_filas(filas)
    assert any("publicado por 2 proyectos" in x for x in h), h


def test_lint_contrato_publicado_dos_veces_por_el_mismo():
    filas = [
        _fila(id="alfa",
              publica=[{"tipo": "contrato", "id": "x/v1"},
                       {"tipo": "contrato", "id": "x/v1"}]),
    ]
    h = pinax.lint_filas(filas)
    assert any("2 veces" in x for x in h), h


def test_lint_rechaza_uso_o_requerido_en_publica():
    # La descripción del schema v1 reserva `uso` para consume; el schema no
    # lo exige por retrocompatibilidad — lint lo hace visible sin romper v1.
    filas = [
        _fila(id="alfa",
              publica=[{"tipo": "contrato", "id": "x/v1", "uso": "para algo"}]),
    ]
    h = pinax.lint_filas(filas)
    assert any("reserva para consume" in x for x in h), h


def test_main_lint_exit_cero_cuando_consistente():
    # Un ecosistema mínimo que se resuelve a sí mismo: alfa publica lo que
    # beta consume. (El fixture de argos solo consume `an-kla`, que no está
    # en la cosecha — lint DEBE hallarlo; ese caso lo cubre el test con
    # hallazgos.)
    import contextlib, io, tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for pid, cuerpo in (
            ("alfa", "publica:\n  - { tipo: contrato, id: alfa/x-v1 }\n"),
            ("beta", "consume:\n  - { tipo: proyecto, id: alfa }\n"),
        ):
            p = root / pid; p.mkdir()
            (p / pinax.MANIFEST_NAME).write_text(
                f"schema: pinax/project-manifest/v1\nid: {pid}\n"
                f"proposito: proposito suficientemente largo de {pid}\n{cuerpo}"
            )
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = pinax.main(["lint", str(root)])
        assert rc == 0, out.getvalue()
        assert "OK" in out.getvalue()


def test_main_lint_halla_consuma_dentro_de_fixture_solitario():
    # El fixture de argos consume `an-kla`, ausente de una cosecha solitaria:
    # hallazgo legítimo, relativo a las raíces cosechadas.
    import contextlib, io
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = pinax.main(["lint", str(FIXTURE)])
    assert rc != 0
    assert "an-kla" in out.getvalue()


def test_main_lint_exit_no_cero_con_hallazgos():
    import contextlib, io, tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / "solo"; p.mkdir()
        (p / pinax.MANIFEST_NAME).write_text(
            "schema: pinax/project-manifest/v1\nid: solo\n"
            "proposito: proposito suficientemente largo\n"
            "consume:\n  - { tipo: proyecto, id: fantasma }\n"
        )
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = pinax.main(["lint", str(root)])
        assert rc != 0
        assert "fantasma" in out.getvalue()


# --- build --format json ---


def test_render_json_estructura_y_determinismo():
    import json as _json
    a = pinax.render_json(pinax.collect([FIXTURE]))
    b = pinax.render_json(pinax.collect([FIXTURE]))
    assert a == b
    data = _json.loads(a)
    assert data["schema"] == "pinax/mapa/v1"
    assert any(p["id"] == "argos" for p in data["proyectos"])
    assert "autodeclarado" in data["nota"]


def test_render_json_incluye_faltan_y_hallazgos():
    import json as _json, tempfile
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        p = root / "repo-solo"; p.mkdir()
        (p / ".git").mkdir()  # proyecto sin manifiesto -> missing
        q = root / "malo"; q.mkdir()
        (q / pinax.MANIFEST_NAME).write_text("schema: otro\nid: malo\nproposito: xxxxxxxxxx\n")
        data = _json.loads(pinax.render_json(pinax.collect([root])))
        assert data["missing_manifest"] == ["repo-solo"]
        assert any("malo" in h for h in data["hallazgos"])


def test_main_build_format_json_a_archivo():
    import contextlib, io, json as _json, tempfile
    with tempfile.TemporaryDirectory() as d:
        destino = Path(d) / "mapa.json"
        with contextlib.redirect_stdout(io.StringIO()):
            rc = pinax.main(["build", str(FIXTURE), "--format", "json",
                             "--output", str(destino)])
        assert rc == 0
        assert _json.loads(destino.read_text())["schema"] == "pinax/mapa/v1"


# --- render: celdas de tabla seguras ---


def test_render_escapa_tuberia_en_proposito():
    d = _fila(proposito="Un propósito con | tubería y \\ barra, largo suficiente.")
    out = pinax.render(pinax.BuildResult([d], [], []))
    assert "\\|" in out      # tubería escapada: la tabla no se rompe
    assert "\\\\" in out     # barra escapada: no puede falsificar el escape


def test_render_trunca_por_palabra():
    import re
    palabras = " ".join(f"palabra{i}" for i in range(40))
    d = _fila(proposito=palabras)
    fila = [ln for ln in pinax.render(pinax.BuildResult([d], [], [])).splitlines()
            if ln.startswith("| **ejemplo**")][0]
    celda = fila.split(" | ")[1]
    assert celda.endswith("…")
    assert re.search(r"palabra\d+…$", celda), celda  # termina en palabra completa


if __name__ == "__main__":
    tests = [(n, f) for n, f in sorted(globals().items()) if n.startswith("test_")]
    ok = sum(run(n, f) for n, f in tests)
    print(f"\n{ok}/{len(tests)} pruebas pasan")
    sys.exit(0 if ok == len(tests) else 1)
