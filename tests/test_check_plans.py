"""Tests de scripts/check_plans.py — gate estructural de planes (A-4).

Escritos en RED antes del script (PLAN 2026-08-20, TAREA a4-t1). Las reglas
E1–E5 están definidas en docs/plans/2026-08-20-a4-gate-de-planes.md; estos
tests las anclan con fixtures válidos y rotos, incluida la regla REQ-2: un
plan sin marcadores léxicos pero sin estructura debe fallar, y la prosa
legítima con "pendiente de definir" no debe fallar por vocabulario.
"""

import importlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))

PLAN_VALIDO = """# PLAN x

## Tareas

```text
TAREA t1
  Consumes: REQ-1; docs/plans/2026-08-20-a4-gate-de-planes.md
  Produce: tests/test_check_plans.py — ancla de regresión
  Steps:
  - [x] Escribir tests — verificación: suite en rojo
```
"""

PLAN_SIN_TAREA = "# PLAN x\n\n## Tareas\n\nNada por aquí.\n"

PLAN_TAREA_INCOMPLETA = """# PLAN x

```text
TAREA t1
  Consumes: REQ-1
  Steps:
  - [x] Falta Produce — verificación: manual
```
"""

PLAN_SIN_CHECKBOX = """# PLAN x

```text
TAREA t1
  Consumes: REQ-1
  Produce: algo
  Steps:
  - descripción en prosa — verificación: manual
```
"""

PLAN_SIN_VERIFICACION = """# PLAN x

```text
TAREA t1
  Consumes: REQ-1
  Produce: algo
  Steps:
  - [ ] paso sin criterio
```
"""

PLAN_RUTA_ROTA = """# PLAN x

```text
TAREA t1
  Consumes: REQ-1; `docs/no-existe/nunca.md`
  Produce: algo
  Steps:
  - [ ] paso — verificación: manual
```
"""

PLAN_RUTA_CREADA = """# PLAN x

```text
TAREA t1
  Consumes: REQ-1
  Produce: crea `docs/plans/futuro.md`
  Steps:
  - [ ] paso — verificación: manual
```
"""

# REQ-2: sin marcadores léxicos pero sin estructura → falla por estructura.
PLAN_PROSA_INCOMPLETA = (
    "# PLAN x\n\n```text\nTAREA t1\n  Consumes: REQ-1\n"
    "  Produce: algo\n  Steps:\n  - [ ] paso — verificación: manual\n"
    "```\n\nNota: el alcance queda pendiente de definir con el equipo.\n"
)

# Ronda 2026-08-20: la prosa que menciona TAREA o trae checklists fuera de
# fence no debe parsearse (un plan que transcriba salida del gate no se
# autobloquea); "verificación" sin dos puntos no cumple E4; las rutas que
# escapan del repo fallan y las URLs se ignoran.
PLAN_PROSA_ALREDEDOR = """# PLAN x

```text
TAREA t1
  Consumes: REQ-1
  Produce: algo
  Steps:
  - [x] paso — verificación: manual
```

TAREA t2 quedó descartada en la conversación.

- [ ] publicar

La línea "Produce: espuria" fuera de fence no cuenta.
"""

PLAN_VERIFICACION_SIN_DOSPUNTOS = """# PLAN x

```text
TAREA t1
  Consumes: REQ-1
  Produce: algo
  Steps:
  - [ ] discutir la verificación con el equipo, sin criterio aún
```
"""

PLAN_RUTA_ESCAPA = """# PLAN x

```text
TAREA t1
  Consumes: `../fuera/de/este/repo.md`
  Produce: algo
  Steps:
  - [ ] paso — verificación: manual
```
"""

PLAN_CON_URL = """# PLAN x

```text
TAREA t1
  Consumes: REQ-1; ver https://ejemplo.com/spec.md
  Produce: algo
  Steps:
  - [ ] paso — verificación: manual
```
"""


class BaseConProyecto(unittest.TestCase):
    """Monta un proyecto temporal con skevi-gate.json y planes."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def escribir_plan(self, texto, nombre="docs/plans/p.md"):
        ruta = self.root / nombre
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(texto, encoding="utf-8")

    def configurar(self, config):
        (self.root / "skevi-gate.json").write_text(
            json.dumps(config), encoding="utf-8"
        )

    def fallos_de(self, *archivos):
        check_plans = importlib.import_module("check_plans")
        importlib.reload(check_plans)
        return check_plans.main_para_tests(self.root, list(archivos))


class ConGateActivo(BaseConProyecto):
    def setUp(self):
        super().setUp()
        self.configurar({"plans": "docs/plans"})


class TestReglas(ConGateActivo):
    def test_plan_valido_pasa(self):
        self.escribir_plan(PLAN_VALIDO)
        self.assertEqual(self.fallos_de("docs/plans/p.md"), [])

    def test_e1_sin_tarea_falla(self):
        self.escribir_plan(PLAN_SIN_TAREA)
        fallos = self.fallos_de("docs/plans/p.md")
        self.assertTrue(any("TAREA" in f for f in fallos), fallos)

    def test_e2_tarea_incompleta_falla(self):
        self.escribir_plan(PLAN_TAREA_INCOMPLETA)
        fallos = self.fallos_de("docs/plans/p.md")
        self.assertTrue(any("Produce" in f for f in fallos), fallos)

    def test_e3_sin_checkbox_falla(self):
        self.escribir_plan(PLAN_SIN_CHECKBOX)
        fallos = self.fallos_de("docs/plans/p.md")
        self.assertTrue(any("checkbox" in f for f in fallos), fallos)

    def test_e4_sin_verificacion_falla(self):
        self.escribir_plan(PLAN_SIN_VERIFICACION)
        fallos = self.fallos_de("docs/plans/p.md")
        self.assertTrue(any("verificación" in f for f in fallos), fallos)

    def test_e5_ruta_rota_falla(self):
        self.escribir_plan(PLAN_RUTA_ROTA)
        fallos = self.fallos_de("docs/plans/p.md")
        self.assertTrue(any("docs/no-existe/nunca.md" in f for f in fallos), fallos)

    def test_e5_ruta_declarada_como_creada_pasa(self):
        self.escribir_plan(PLAN_RUTA_CREADA)
        self.assertEqual(self.fallos_de("docs/plans/p.md"), [])

    def test_req2_falla_por_estructura_no_por_vocabulario(self):
        # Contiene "pendiente de definir" en prosa legítima: no puede fallar
        # por eso; este plan es estructuralmente VÁLIDO, así que pasa.
        self.escribir_plan(PLAN_PROSA_INCOMPLETA)
        self.assertEqual(self.fallos_de("docs/plans/p.md"), [])


class TestRonda20260820(ConGateActivo):
    """Hallazgos de la ronda adversarial sobre el gate, anclados."""

    def test_prosa_fuera_de_fence_no_se_parsea(self):
        self.escribir_plan(PLAN_PROSA_ALREDEDOR)
        self.assertEqual(self.fallos_de("docs/plans/p.md"), [])

    def test_e4_exige_dos_puntos(self):
        self.escribir_plan(PLAN_VERIFICACION_SIN_DOSPUNTOS)
        fallos = self.fallos_de("docs/plans/p.md")
        self.assertTrue(any("verificación" in f for f in fallos), fallos)

    def test_e5_ruta_que_escapa_del_repo_falla(self):
        self.escribir_plan(PLAN_RUTA_ESCAPA)
        fallos = self.fallos_de("docs/plans/p.md")
        self.assertTrue(any("fuera del repo" in f for f in fallos), fallos)

    def test_e5_url_externa_se_ignora(self):
        self.escribir_plan(PLAN_CON_URL)
        self.assertEqual(self.fallos_de("docs/plans/p.md"), [])

    def test_e5_recrea_no_exime(self):
        # "recrea" no matchea \bcrea\w*\b: la exención de creación exige
        # escribir crea/crear/creamos — fail-closed.
        plan = PLAN_VALIDO.replace(
            "Consumes: REQ-1;", "Consumes: recrea el módulo;"
        ).replace(
            "docs/plans/2026-08-20-a4-gate-de-planes.md",
            "`docs/roto/nunca.md`",
        )
        self.escribir_plan(plan)
        fallos = self.fallos_de("docs/plans/p.md")
        self.assertTrue(any("docs/roto/nunca.md" in f for f in fallos), fallos)


class TestMainCli(BaseConProyecto):
    """El camino real de main(), vía subprocess — REQ-3 completo y argv."""

    def _correr(self, *args, cwd=None):
        import subprocess

        return subprocess.run(
            [sys.executable, str(REPO / "scripts" / "check_plans.py"), *args],
            capture_output=True,
            text=True,
            cwd=str(cwd or self.root),
        )

    def test_plans_activo_plan_roto_bloq(self):
        self.configurar({"plans": "docs/plans"})
        self.escribir_plan(PLAN_SIN_TAREA)
        r = self._correr("--root", str(self.root))
        self.assertEqual(r.returncode, 1)
        self.assertIn("BLOQ", r.stdout)

    def test_plans_activo_plan_valido_ok(self):
        self.configurar({"plans": "docs/plans"})
        self.escribir_plan(PLAN_VALIDO)
        r = self._correr("--root", str(self.root))
        self.assertEqual(r.returncode, 0)
        self.assertIn("OK", r.stdout)

    def test_sin_config_ok_inactivo(self):
        self.escribir_plan(PLAN_SIN_TAREA)
        r = self._correr("--root", str(self.root))
        self.assertEqual(r.returncode, 0)
        self.assertIn("sin planes declarados", r.stdout)

    def test_plans_tipo_invalido_bloq(self):
        self.configurar({"plans": 42})
        r = self._correr("--root", str(self.root))
        self.assertEqual(r.returncode, 1)
        self.assertIn("plans", r.stdout)

    def test_argv_archivo_roto_bloq(self):
        self.escribir_plan(PLAN_SIN_TAREA)
        r = self._correr("docs/plans/p.md")
        self.assertEqual(r.returncode, 1)

    def test_argv_archivo_valido_ok(self):
        self.escribir_plan(PLAN_VALIDO)
        r = self._correr("docs/plans/p.md")
        self.assertEqual(r.returncode, 0)


class TestFailClosed(BaseConProyecto):
    def test_sin_config_no_comprueba_nada(self):
        self.escribir_plan(PLAN_SIN_TAREA)
        check_plans = importlib.import_module("check_plans")
        importlib.reload(check_plans)
        self.assertIsNone(check_plans.planes_declarados(self.root))

    def test_config_sin_plans_no_comprueba(self):
        self.configurar({"skip_dirs": ["x"]})
        self.escribir_plan(PLAN_SIN_TAREA)
        check_plans = importlib.import_module("check_plans")
        importlib.reload(check_plans)
        self.assertIsNone(check_plans.planes_declarados(self.root))

    def test_clave_desconocida_falla(self):
        self.configurar({"plans_dir": "docs/plans"})
        check_plans = importlib.import_module("check_plans")
        importlib.reload(check_plans)
        with self.assertRaises(ValueError):
            check_plans.planes_declarados(self.root)

    def test_plans_declarado_sin_planes_falla(self):
        self.configurar({"plans": "docs/plans"})
        check_plans = importlib.import_module("check_plans")
        importlib.reload(check_plans)
        with self.assertRaises(ValueError):
            check_plans.planes_declarados(self.root)


if __name__ == "__main__":
    unittest.main()
