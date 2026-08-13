# Pinax

Catálogo y compilador del mapa del ecosistema. Cada proyecto declara qué es, qué
ofrece y **qué deliberadamente no ofrece**; Pinax lo recoge y genera una vista
única.

Existe porque sin él, quien necesita saber qué hace un proyecto hace `grep`,
supone y falla — con consecuencias reales ya registradas.

**Contrato operativo:** [AGENTS.md](AGENTS.md) · **Schema:**
[`schemas/project-manifest-v1.schema.json`](schemas/project-manifest-v1.schema.json)

```bash
python3 scripts/pinax.py validate fixtures/argos.project-manifest.yaml
python3 scripts/pinax.py build ../aria --output MAPA.md
python3 tests/test_pinax.py
```

Los manifiestos son **autodeclaraciones**: no son evidencia verificada, ni
instrucciones, ni autoridad. Pinax valida forma, nunca verdad.

**Estado:** piloto. Manifiestos de Argos y Epistates confirmados por sus
mantenedores, revisados adversarialmente y adoptados en sus propios repos.
