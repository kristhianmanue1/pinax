# Entregable B — Grafo inicial de contratos y fronteras (v0)

Modelo obligatorio: `PRODUCTOR → CONTRATO → CONSUMIDOR`, no `proyecto A →
proyecto B`. Contrato, implementación, dependencia, autoridad, integración,
evidencia y propuesta viajan como etiquetas separadas.

Una arista declarada por un proyecto no implica control interno del
productor sobre el consumidor.

## Aristas con evidencia

| # | Productor | Contrato / servicio | Consumidor | Clase | Fuente |
|---|---|---|---|---|---|
| G1 | Epistates | `epistates/task-card/v1` | EKTEL | `DECLARED` — `uso: entrada estándar de ejecución`, `requerido: true` | ektel/project-manifest.yaml `consume` |
| G2 | Epistates | `epistates/task-card/v1` | Pinax | `DECLARED` — política de este repo, `requerido: false` | pinax/project-manifest.yaml `consume` |
| G3 | Praxis Dev | contratos/autoridad/evidencia de gobernanza (`0.1.0-draft.1`) | Epistates | `DECLARED` — relación de diseño README §4, "sin dependencia operativa en código a la fecha" | epistates README §4 + manifiesto |
| G4 | Escrubery | `CONTRATO_API_v0` | Skopos | `DECLARED` una sola cara — "consulta a escrubery" en el pipeline; escrubery no registra consumidores | skopos README (línea de F3); docs/CONTRATO_API_v0.md |
| G5 | Llavero | inyección de secretos por entorno | Skopos | `DECLARED` — "Uso con skopos + z.ai" | llavero README |
| G6 | AN-KLA (motor) | memoria/checkpoint como servicio local, **sin contrato pinax publicado** | Pinax, Argos, Epistates, SKEVI | `DECLARED` — `consume proyecto`, todas `requerido: false`, nivel checkout-mantenedor, no runtime | manifiestos de pinax/argos/epistates; lint 2026-09-10 |
| G7 | EKTEL | canal de interrupción A0 (futuro) | Propylon | `DECLARED`-como-futuro, `requerido: false` — **arista hacia una propuesta sin código** | ektel/project-manifest.yaml |
| G8 | SKEVI | gate de estructura/tamaños (scripts copiados sin edición) + estándar F0–F3 | Pinax | `DECLARED`/`VERIFIED` — adopción documentada con `skevi-gate.json` | docs/adopcion-gate-skevi-2026-08-21.md |

## Productores sin consumidor registrado

Estado 2026-09-10 — los contratos existen, los consumidores son `UNKNOWN`:

* EKTEL: 11 contratos wire v1 (`DECLARED` en manifiesto; experimentales, sin
  compromiso de estabilidad).
* Epistates: los otros 10 contratos además de task-card (audit-result,
  preflight-result, dispatch-receipt, human-notice, review-evidence,
  discovery, adapter-capabilities, validation-report, schema-catalog,
  schema-show).
* Argos: 5 contratos de evaluación.
* Praxis Dev: contratos/políticas de gobernanza en draft; único consumidor
  declarado: Epistates (G3, relación de diseño).

## Aristas hipotéticas (PROPOSED — sin ancla en repos)

* Praxis expresa política ↔ runtime externo (EKTEL) la enforced. No fusionar
  con G1: Epistates consume contratos de Epistates, no de Praxis, hoy.
* Escrubery como productor de inteligencia operativa para Epistates/EKTEL.
* Glosomata como futuro consumidor de contratos de sesión/identidad/
  interrupción/runtime.
* Llavero como proveedor detrás de una capability de secretos de un runtime
  (`EKTEL → adapter → Llavero` sin `EKTEL = secret store`).
* Propylon como PDP/PEP del ecosistema. Pregunta de si es responsabilidad
  independiente queda abierta.

Ninguna de estas aristas puede promocionarse sin manifiesto o código que la
declare.

## Cosecha de Pinax al día del snapshot

`VERIFIED` (salida de herramientas 2026-09-10):

* Manifiestos legibles y `OK`: pinax, argos, epistates, ektel, skevi.
* Manifiesto ILEGIBLE: skopos (YAML malformado, ver H-2) — sus aristas no
  entran a la cosecha; la G4/G5 vienen de su README, no del manifiesto.
* Sin manifiesto: praxis-dev, escrubery, glosomata, llavero, propylon,
  agora, an-kla-memory (motor).
* `lint` (9 hallazgos, relativos a las raíces): consume sin manifiesto en
  an-kla-memory, praxis, propylon; `pinax consume epistates/task-card` sin
  publicador cosechado **por convención de id divergente** — epistates
  publica `id: epistates/task-card/v1` (versión dentro del id) y ektel
  consume esa misma forma, mientras pinax declara
  `id: epistates/task-card, version: v1` (ver H-9); nada de esto es verdad
  ni falsedad — forma relativa a la cosecha.
* `build` del mapa: **fail-closed** por H-2; mapa machine-readable no
  regenerado en este ciclo.
