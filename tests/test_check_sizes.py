"""Tests para scripts/check_sizes.py. Runner: `python3 -m unittest`."""

from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
_SPEC = importlib.util.spec_from_file_location(
    "check_sizes", SCRIPTS_DIR / "check_sizes.py"
)
check_sizes = importlib.util.module_from_spec(_SPEC)
sys.modules["check_sizes"] = check_sizes
_SPEC.loader.exec_module(check_sizes)


class LimitForTests(unittest.TestCase):
    def test_default_limit(self):
        self.assertEqual(check_sizes.limit_for("docs/history/foo.md"), 800)

    def test_agents_md_limit(self):
        self.assertEqual(check_sizes.limit_for("AGENTS.md"), 200)

    def test_readme_limit(self):
        self.assertEqual(check_sizes.limit_for("README.md"), 300)

    def test_template_limit(self):
        self.assertEqual(check_sizes.limit_for("templates/skevi/x.md"), 300)


class RegistryBlockTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self._orig_root = check_sizes.ROOT
        check_sizes.ROOT = self.root

    def tearDown(self):
        check_sizes.ROOT = self._orig_root

    def test_no_block_is_not_a_failure(self):
        text = "# AGENTS.md\n\nsin bloque de registro.\n"
        self.assertEqual(
            check_sizes.check_registry_block(Path("AGENTS.md"), text), []
        )

    def test_unbalanced_delimiters(self):
        text = "<!-- skevi:registry:start -->\n[skevi]\nx=y.md\n"
        failures = check_sizes.check_registry_block(Path("AGENTS.md"), text)
        self.assertEqual(len(failures), 1)
        self.assertIn("desbalanceados", failures[0])

    def test_missing_skevi_section(self):
        text = (
            "<!-- skevi:registry:start -->\n"
            "x=y.md\n"
            "<!-- skevi:registry:end -->\n"
        )
        failures = check_sizes.check_registry_block(Path("AGENTS.md"), text)
        self.assertTrue(any("sin sección [skevi]" in f for f in failures))

    def test_valid_block_points_to_existing_file(self):
        (self.root / "contexto.md").write_text("hola\n", encoding="utf-8")
        text = (
            "<!-- skevi:registry:start -->\n"
            "[skevi]\n"
            "contexto=contexto.md\n"
            "<!-- skevi:registry:end -->\n"
        )
        self.assertEqual(
            check_sizes.check_registry_block(Path("AGENTS.md"), text), []
        )

    def test_entry_points_to_missing_file(self):
        text = (
            "<!-- skevi:registry:start -->\n"
            "[skevi]\n"
            "contexto=no-existe.md\n"
            "<!-- skevi:registry:end -->\n"
        )
        failures = check_sizes.check_registry_block(Path("AGENTS.md"), text)
        self.assertTrue(any("ruta inexistente" in f for f in failures))

    def test_entry_escaping_root_is_rejected(self):
        text = (
            "<!-- skevi:registry:start -->\n"
            "[skevi]\n"
            "contexto=../fuera.md\n"
            "<!-- skevi:registry:end -->\n"
        )
        failures = check_sizes.check_registry_block(Path("AGENTS.md"), text)
        self.assertTrue(any("fuera de la raíz" in f for f in failures))


class MainIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self._orig_root = check_sizes.ROOT
        check_sizes.ROOT = self.root
        self._make_minimal_valid_repo()

    def tearDown(self):
        check_sizes.ROOT = self._orig_root

    def _make_minimal_valid_repo(self):
        for relative in sorted(check_sizes.REQUIRED):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"# {relative}\n", encoding="utf-8")

    def _run_main(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = check_sizes.main()
        return exit_code, buf.getvalue()

    def test_minimal_valid_repo_passes(self):
        exit_code, output = self._run_main()
        self.assertEqual(exit_code, 0)
        self.assertTrue(output.startswith("OK —"))

    def test_missing_required_file_fails(self):
        (self.root / "README.md").unlink()
        exit_code, output = self._run_main()
        self.assertEqual(exit_code, 1)
        self.assertIn("falta archivo requerido: README.md", output)

    def test_stray_root_markdown_fails(self):
        (self.root / "NOTAS.md").write_text("suelto\n", encoding="utf-8")
        exit_code, output = self._run_main()
        self.assertEqual(exit_code, 1)
        self.assertIn("Markdown operativo suelto en raíz", output)
        self.assertIn("NOTAS.md", output)

    def test_file_over_default_limit_fails(self):
        oversized = self.root / "docs" / "historia" / "largo.md"
        oversized.parent.mkdir(parents=True, exist_ok=True)
        oversized.write_text("\n".join(f"linea {i}" for i in range(801)) + "\n")
        exit_code, output = self._run_main()
        self.assertEqual(exit_code, 1)
        self.assertIn("801 líneas > límite 800", output)

    def test_file_at_default_limit_passes(self):
        exact = self.root / "docs" / "historia" / "justo.md"
        exact.parent.mkdir(parents=True, exist_ok=True)
        exact.write_text("\n".join(f"linea {i}" for i in range(800)) + "\n")
        exit_code, _ = self._run_main()
        self.assertEqual(exit_code, 0)

    def test_skip_dirs_are_not_scanned(self):
        node_modules = self.root / "node_modules" / "pkg"
        node_modules.mkdir(parents=True, exist_ok=True)
        (node_modules / "huge.md").write_text(
            "\n".join(f"linea {i}" for i in range(2000)) + "\n"
        )
        exit_code, _ = self._run_main()
        self.assertEqual(exit_code, 0)


class ConfigTests(unittest.TestCase):
    """`skevi-gate.json` — gate configurable por proyecto adoptante (A-6)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self._orig_root = check_sizes.ROOT
        check_sizes.ROOT = self.root
        # apply_config muta estado de módulo in situ; sin restaurarlo, un test
        # de esta clase corrompería LimitForTests o MainIntegrationTests
        # ejecutados después en el mismo proceso.
        self._orig_limits = dict(check_sizes.LIMITS)
        self._orig_default_limit = check_sizes.DEFAULT_LIMIT
        self._orig_exempt_paths = set(check_sizes.EXEMPT_PATHS)
        self._orig_required = set(check_sizes.REQUIRED)
        self._orig_skip_dirs = set(check_sizes.SKIP_DIRS)
        self._orig_root_markdown = set(check_sizes.ROOT_MARKDOWN)

    def tearDown(self):
        check_sizes.ROOT = self._orig_root
        check_sizes.LIMITS.clear()
        check_sizes.LIMITS.update(self._orig_limits)
        check_sizes.DEFAULT_LIMIT = self._orig_default_limit
        check_sizes.EXEMPT_PATHS.clear()
        check_sizes.EXEMPT_PATHS.update(self._orig_exempt_paths)
        check_sizes.REQUIRED.clear()
        check_sizes.REQUIRED.update(self._orig_required)
        check_sizes.SKIP_DIRS.clear()
        check_sizes.SKIP_DIRS.update(self._orig_skip_dirs)
        check_sizes.ROOT_MARKDOWN.clear()
        check_sizes.ROOT_MARKDOWN.update(self._orig_root_markdown)

    def _write_config(self, data):
        (self.root / check_sizes.CONFIG_NAME).write_text(
            json.dumps(data), encoding="utf-8"
        )

    def test_absent_config_returns_empty_dict(self):
        self.assertEqual(check_sizes.load_config(), {})

    def test_config_with_unknown_key_raises(self):
        self._write_config({"limites": {"AGENTS.md": 50}})
        with self.assertRaises(ValueError):
            check_sizes.load_config()

    def test_config_root_must_be_object(self):
        self._write_config([1, 2, 3])
        with self.assertRaises(ValueError):
            check_sizes.load_config()

    def test_limits_merge_onto_skevi_defaults(self):
        check_sizes.apply_config({"limits": {"docs/mio.md": 50}})
        self.assertEqual(check_sizes.limit_for("docs/mio.md"), 50)
        # AGENTS.md conserva su límite de Skevi: limits se añade, no reemplaza.
        self.assertEqual(check_sizes.limit_for("AGENTS.md"), 200)

    def test_default_limit_is_overridable(self):
        check_sizes.apply_config({"default_limit": 400})
        self.assertEqual(check_sizes.limit_for("docs/cualquiera.md"), 400)

    def test_exempt_paths_merge(self):
        check_sizes.apply_config({"exempt_paths": ["docs/congelado.md"]})
        self.assertIsNone(
            check_sizes.count_text_lines(Path("docs/congelado.md"))
        )

    def test_required_replaces_skevi_list(self):
        """Un adoptante con otra estructura no hereda los archivos de Skevi."""
        check_sizes.apply_config({"required": ["docs/architecture/README.md"]})
        self.assertEqual(check_sizes.REQUIRED, {"docs/architecture/README.md"})
        self.assertNotIn(
            "docs/estandar-diseno-software-github.md", check_sizes.REQUIRED
        )

    def test_required_can_be_declared_empty(self):
        check_sizes.apply_config({"required": []})
        self.assertEqual(check_sizes.REQUIRED, set())

    def test_skip_dirs_merge_onto_skevi_defaults(self):
        check_sizes.apply_config({"skip_dirs": ["coverage"]})
        self.assertIn("coverage", check_sizes.SKIP_DIRS)
        self.assertIn(".git", check_sizes.SKIP_DIRS)

    # --- Hallazgos de la ronda adversarial con contexto fresco (2026-08-17) ---

    def test_required_rejects_absolute_path(self):
        """Sin esto, `(ROOT / relative).is_file()` resuelve fuera de ROOT y
        un `required` puede darse por cumplido con un archivo del host."""
        with self.assertRaisesRegex(ValueError, "ruta inválida"):
            check_sizes.apply_config({"required": ["/etc/passwd"]})

    def test_required_rejects_path_escaping_root(self):
        with self.assertRaisesRegex(ValueError, "ruta inválida"):
            check_sizes.apply_config({"required": ["../../etc/passwd"]})

    def test_exempt_paths_rejects_absolute_path(self):
        with self.assertRaisesRegex(ValueError, "ruta inválida"):
            check_sizes.apply_config({"exempt_paths": ["/etc/passwd"]})

    def test_limits_with_non_integer_value_raises_value_error(self):
        """No una excepción cruda de Python: main() sólo atrapa ValueError."""
        with self.assertRaises(ValueError):
            check_sizes.apply_config({"limits": ["no", "dict"]})
        with self.assertRaises(ValueError):
            check_sizes.apply_config({"limits": {"AGENTS.md": "cincuenta"}})

    def test_limits_rejects_boolean_as_integer(self):
        """bool es subclase de int en Python; True/False no son un límite."""
        with self.assertRaises(ValueError):
            check_sizes.apply_config({"limits": {"AGENTS.md": True}})

    def test_default_limit_with_wrong_type_raises_value_error(self):
        with self.assertRaises(ValueError):
            check_sizes.apply_config({"default_limit": "ochocientas"})
        with self.assertRaises(ValueError):
            check_sizes.apply_config({"default_limit": [800]})

    def test_skip_dirs_rejects_non_string_list(self):
        with self.assertRaises(ValueError):
            check_sizes.apply_config({"skip_dirs": "coverage"})

    def test_root_markdown_is_additive(self):
        """CONTRIBUTING.md/SECURITY.md en la raíz de un adoptante real
        (an-kla-memory) no deben leerse como Markdown suelto."""
        check_sizes.apply_config({"root_markdown": ["CONTRIBUTING.md"]})
        self.assertIn("CONTRIBUTING.md", check_sizes.ROOT_MARKDOWN)
        self.assertIn("README.md", check_sizes.ROOT_MARKDOWN)

    def test_reset_to_skevi_defaults_undoes_a_previous_config(self):
        """Dos invocaciones de main() en el mismo proceso no acumulan
        configuración: la segunda no hereda lo que declaró la primera."""
        check_sizes.apply_config({"required": [], "root_markdown": ["X.md"]})
        self.assertEqual(check_sizes.REQUIRED, set())
        check_sizes.reset_to_skevi_defaults()
        self.assertEqual(check_sizes.REQUIRED, self._orig_required)
        self.assertEqual(check_sizes.ROOT_MARKDOWN, self._orig_root_markdown)

    def test_main_uses_adopter_config_end_to_end(self):
        """Un proyecto con otra estructura pasa el gate sin los archivos de Skevi."""
        self._write_config({
            "required": ["README.md"],
            "limits": {"README.md": 5},
        })
        (self.root / "README.md").write_text("una linea\n", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = check_sizes.main()
        self.assertEqual(exit_code, 0)
        self.assertIn("OK —", buf.getvalue())

    def test_main_fails_closed_on_malformed_config(self):
        self._write_config({"desconocida": 1})
        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = check_sizes.main()
        self.assertEqual(exit_code, 1)
        self.assertIn("BLOQ", buf.getvalue())

    def test_main_never_leaks_a_raw_traceback_on_malformed_config(self):
        """Reproduce el ataque de la ronda adversarial: limits con una lista
        en vez de un objeto no debe escapar como AttributeError crudo."""
        self._write_config({"limits": ["no", "dict"]})
        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = check_sizes.main()
        self.assertEqual(exit_code, 1)
        self.assertIn("BLOQ", buf.getvalue())
        self.assertNotIn("Traceback", buf.getvalue())

    def test_main_end_to_end_an_kla_memory_style_project(self):
        """El caso real que motiva ADR-006: otra estructura de directorios y
        Markdown de gobierno de proyecto adicional en la raíz."""
        self._write_config({
            "required": ["README.md", "docs/architecture/0001-foo.md"],
            "root_markdown": ["CONTRIBUTING.md", "SECURITY.md"],
        })
        (self.root / "docs" / "architecture").mkdir(parents=True)
        (self.root / "README.md").write_text("# proyecto\n", encoding="utf-8")
        (self.root / "docs" / "architecture" / "0001-foo.md").write_text(
            "# ADR\n", encoding="utf-8"
        )
        (self.root / "CONTRIBUTING.md").write_text("# contribuir\n", encoding="utf-8")
        (self.root / "SECURITY.md").write_text("# seguridad\n", encoding="utf-8")
        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = check_sizes.main()
        self.assertEqual(exit_code, 0)
        self.assertIn("OK —", buf.getvalue())

    def test_main_twice_in_same_process_does_not_leak_state(self):
        """Confirma en main(), no sólo en apply_config, que no hay
        acumulación entre invocaciones consecutivas."""
        self._write_config({"required": []})
        buf1 = io.StringIO()
        with redirect_stdout(buf1):
            exit_code1 = check_sizes.main()
        self.assertEqual(exit_code1, 0)

        (self.root / check_sizes.CONFIG_NAME).unlink()
        buf2 = io.StringIO()
        with redirect_stdout(buf2):
            exit_code2 = check_sizes.main()
        self.assertEqual(exit_code2, 1)
        self.assertIn("falta archivo requerido: AGENTS.md", buf2.getvalue())


if __name__ == "__main__":
    unittest.main()
