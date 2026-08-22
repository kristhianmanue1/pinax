# Adopción del gate de skevi y manifiesto propio (2026-08-21)

**Qué se hizo:** Pinax declara su propio `project-manifest.yaml` y adopta el
gate local de skevi (`check_sizes.py` + `check_plans.py`), copiados **sin
editar**; los valores de este proyecto viven en `skevi-gate.json`.

**Por qué:** dos brechas verificadas el 2026-08-21.

1. El catálogo no estaba en el catálogo: `pinax/project-manifest.yaml` no
   existía, mientras argos, epistates y skevi sí declaraban el suyo. El
   único proyecto exento del contrato era quien lo define.
2. `docs/politica-agentes-pinax.md` §3 declaraba límites de tamaño y añadía
   "duro cuando exista gate; advisory mientras tanto". El gate existe, es
   copiable sin edición y no tiene dependencias — la condición se cumplía
   sin que nadie la cerrara.

**Procedencia:** `skevi/scripts/check_sizes.py` y `check_plans.py`, copia
byte a byte de `skevi@7bfd759` (verificado con `cmp`). El mecanismo de
configuración por proyecto es ADR-006 de skevi; el gate de planes es
ADR-014. Adoptar exige copiar **ambos** scripts: comparten config y
`check_plans` importa `CONFIG_KEYS` de `check_sizes`.

## Qué comprueba aquí

- Archivos canónicos presentes (`required` de `skevi-gate.json`).
- Ningún Markdown operativo suelto en la raíz salvo los declarados.
- Límites: `AGENTS.md` 200, `README.md` 300, cualquier otro texto 800.
- `check_plans` **inactivo**: sin clave `plans` no comprueba nada. Es
  fail-closed por ausencia, no un error. Se activará si algún día hay
  `docs/plans/`.

## Exenciones declaradas y su razón

| Exención | Razón |
|---|---|
| `root_markdown: AN-KLA.md` | Contrato de la integración de memoria; su hogar canónico es la raíz, junto a `AGENTS.md`, que lo referencia. |
| `root_markdown: MAPA.md` + `exempt_paths: MAPA.md` | Artefacto **generado** por `build --output`, gitignored. Ni su ubicación ni su tamaño son decisiones de autoría. |
| `exempt_paths: rondas/2026-08-20-m0-ektel-externas/codex-raw.log` | Transcripción cruda de una ronda externa (2 441 líneas). Es evidencia capturada, no texto redactado; recortarla la destruiría como evidencia. |
| `skip_dirs: orquetacionMultiagenteTemporal` | Borrador deliberadamente fuera de Git y fuera del ciclo publicado (decisión d5 del checkpoint AN-KLA rev 26). Requiere análisis, ronda adversarial y autorizaciones propias antes de entrar. **Si entra, entra bloqueado**: tres de sus archivos superan las 800 líneas. |

La última no es una exención permanente sino un aplazamiento con fecha de
revisión: se retira cuando se decida el hogar canónico de ese borrador.

## Evidencia de que el gate muerde

Anti-gate-vacuo: un gate que no puede fallar no verifica nada. Al retirar
temporalmente `skip_dirs` y volver a correrlo:

```text
BLOQ — check_sizes encontró incumplimientos
- docs/orquetacionMultiagenteTemporal/backup/orquestacion-codex-opencode-tmux-v1.0-20260818.md: 940 líneas > límite 800
- docs/orquetacionMultiagenteTemporal/backup/orquestacion-codex-opencode-tmux-v2.0-20260818.md: 1075 líneas > límite 800
- docs/orquetacionMultiagenteTemporal/orquestacion-codex-opencode-tmux.md: 1261 líneas > límite 800
```

La config se restauró inmediatamente después y el gate volvió a `OK`.

## Confirmación del mantenedor

El propio protocolo de adopción de Pinax (AGENTS.md) exige confirmación del
autor sobre `no_ofrece`, `pospuesto`, `consume` y los contratos de
`publica`: sólo el mantenedor sabe qué ausencias son deliberadas. El
manifiesto de este repo fue redactado desde sus fuentes publicadas
(AGENTS.md, README, código y políticas).

**Confirmación registrada el 2026-08-22:** el dueño autorizó commit y
cierre de este lote (manifiesto incluido) tras la revisión crítica de la
sesión — que propuso y ejecutó además lint de grafo, `build --format json`,
discover por manifiesto/`.git` y render escapado. La confirmación acredita
autoría del contenido, no verificación técnica de lo que afirma.
