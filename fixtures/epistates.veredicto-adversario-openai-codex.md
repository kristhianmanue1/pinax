# Veredicto adversario — Epistates — OpenAI Codex

> **Nota de integridad.** Codex ejecutó esta revisión con `codex exec -s
> workspace-write` desde `aria/epistates/`, y su sandbox restringió la escritura
> a esa raíz. `pinax/fixtures` quedó fuera de lo escribible, así que **Codex no
> pudo crear este archivo por sí mismo** — lo reportó como texto en su salida y
> pidió que se habilitara pinax como raíz escribible. Este archivo transcribe
> ese texto **sin alterarlo**, y quien lo persiste (Claude Opus 5, revisor
> distinto) verificó cada hallazgo nuevo contra el código fuente de epistates
> antes de aplicar las correcciones al manifiesto. Esa verificación se declara
> aparte, al final, para no mezclarse con el veredicto original de Codex.

**Posición:** CONCURRE CON CORRECCIONES

## Hallazgos (texto original de Codex, íntegro)

- `no_ofrece`: contiene 9 de las 10 exclusiones. Falta la cita exacta:
  «despertar tareas mediante APIs privadas o mecanismos no soportados».
- Praxis: cambiar `requerido: true` a `false` y describirla como relación de
  diseño futura, sin dependencia operativa actual.
- `publica`: añadir `epistates/discovery/v1`, `epistates/validation-report/v1`,
  `epistates/schema-catalog/v1` y `epistates/schema-show/v1`.
- `ofrece`: añadir la validación machine-readable mediante
  `validation-report/v1`.
- Eliminar `repo: epistates`: el schema indica que sólo se declara si difiere
  del directorio local.
- Eliminar de `pospuesto` la supuesta integración automática de Git para
  tags/releases: no está en el roadmap y la prerelease ya está publicada.
- No detecté imperativos, estado dinámico impropio ni tipos incorrectos en
  `consume`.

## Verificación read-only de Codex

- Manifiesto original: `pinax.py validate` → `OK`.
- `test_pinax.py` → 16/16 pruebas pasan.
- Ningún archivo fue modificado por Codex.

## Verificación independiente de cada hallazgo (Claude Opus 5, antes de aplicar)

| Hallazgo | Verificado contra | Resultado |
|---|---|---|
| `no_ofrece` — falta 1/10 | `README.md` §6 "No objetivos iniciales" | Confirmado: 9 de 10 presentes, falta la décima cita literal |
| `praxis` no es dependencia de código | `grep -rn praxis src/` → 0 resultados; README §4 en tiempo futuro ("podrá", "declarará") | Confirmado |
| `epistates/discovery/v1` es identificador real | `README.md:74` — `# (epistates/discovery/v1), estable ante locale/encoding/TZ` | Confirmado |
| `epistates/validation-report/v1` es identificador real | `README.md:84` | Confirmado |
| `epistates/schema-catalog/v1` es identificador real | `src/epistates/__main__.py`, help de `schema list`: *"Emite un unico documento JSON epistates/schema-catalog/v1"* | Confirmado |
| `epistates/schema-show/v1` es identificador real | `src/epistates/__main__.py`, help de `schema show`: *"...epistates/schema-show/v1..."* | Confirmado |
| `repo: epistates` es redundante | `basename` del directorio local = `epistates` | Confirmado — coincide, el campo sólo se declara si difiere |
| Release ya publicada, no `pospuesto` | `README.md:11,15` — *"la prerelease GitHub fue publicada con wheel y checksum certificados"* | Confirmado |

Las ocho afirmaciones de Codex se sostienen contra la fuente. Correcciones
aplicadas a `epistates.project-manifest.yaml`.

## Defecto adicional encontrado al aplicar (no reportado por Codex)

Al añadir los cuatro IDs nuevos con `version: v1` —siguiendo el patrón usado
para los siete contratos existentes— el mapa generado mostraba
`epistates/task-card/v1@v1`: versión duplicada. Epistates trata
`epistates/task-card/v1` como su identificador canónico **completo**, con la
versión ya incrustada (`src/epistates/schemas.py:62`), a diferencia de argos,
que usa `argos/evaluation-manifest` como base y un campo `version` aparte. Se
retiró el campo `version` redundante de las once referencias de `publica` para
respetar la convención propia de epistates.

## Lo que no pude determinar

- Codex no pudo ejecutar `pinax.py validate` sobre el manifiesto corregido
  porque no pudo escribirlo. Esa validación queda pendiente de quien aplique
  las correcciones (hecho: ver commit).
- Codex no confirmó si `an-kla` con `requerido: false` seguía siendo correcto
  tras sus cambios — no lo tocó, y esta revisión tampoco encontró motivo para
  cambiarlo.

---
*Agente: OpenAI Codex — Modelo: no expuesto por el host — CLI: 0.147.0 — Rol:
adversario. Fecha: 2026-08-13*
*Persistencia y verificación cruzada: Anthropic Claude Opus 5 — Fecha:
2026-08-13*
