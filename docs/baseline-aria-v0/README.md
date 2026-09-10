# Baseline Arquitectónica de Aria v0

Estado: `PROPUESTA-PARA-REVISION` · Snapshot de inspección: **2026-09-10** ·
Autor del registro: Pinax (agente), para revisión adversarial del Mediador.

## Qué es y qué no es

Congela el estado observado del ecosistema Aria antes del experimento
Runtime Contract. Pinax valida estructura y consistencia del mapa; **no
convierte autodeclaraciones en verdad**. Nada de lo que otro proyecto
declara aquí ha sido elevado a hecho verificado sin evidencia directa
citada. Este documento no modifica ningún otro repositorio.

## Niveles de certeza (obligatorios en todo el baseline)

| Nivel | Significado |
|---|---|
| `VERIFIED` | Evidencia comprobada directamente en esta inspección (commit, archivo, tag, salida de herramienta), con fuente citada. |
| `DECLARED` | Declaración del propio proyecto (README, manifiesto, acta), citada; no re-verificada técnicamente. |
| `INFERRED` | Conclusión arquitectónica de Pinax a partir de lo anterior. Nunca se serializa como hecho. |
| `PROPOSED` | Diseño todavía no adoptado por nadie; incluye todo lo venido del encargo sin ancla en repos. |
| `UNKNOWN` | Información insuficiente; se declara explícitamente. |

Una inferencia nunca se serializa como hecho verificado.

## Dimensiones separadas (regla 22 del encargo)

`COMPONENTE` ≠ `PLANO` ≠ `CAPABILITY`. Un componente puede ofrecer varias
capabilities; una capability puede ser implementada por distintos
componentes; un plano es una clasificación, no una dependencia. Estas tres
dimensiones viajan separadas en todos los archivos de este baseline.

## Clasificación de madurez

* `COMPONENT` — existente, con implementación o cuerpo normativo operativos.
* `COMPONENT_MINOR` — funcional pero de alcance/madurez menor (no mide importancia).
* `PROPOSED_COMPONENT` — repositorio/intención sin implementación funcional suficiente. **No se promueve a componente por tener repositorio.**

## Plano preliminar (hipótesis, no taxonomía cerrada)

| Plano | Componentes |
|---|---|
| Ecosystem Map | Pinax |
| Development Method / Normative Process | SKEVI |
| Governance | Praxis Dev |
| Execution / Enforcement | EKTEL |
| Operational Supervision | Epistates |
| Memory / Information | AN-KLA, Skopos, Ágora |
| Epistemic Evaluation | Argos Epistemic |
| External Capability Intelligence | Escrubery |
| Interface / Interaction Channel | Glosomata |
| Security / Secrets Capability | Llavero |
| Proposed Gateway / Authorization Boundary | Propylon (`PROPOSED_COMPONENT`) |

Contrastes registrados contra esta hipótesis: ver
`fronteras-y-hallazgos-v0.md` (H-3: solapamiento Epistates/EKTEL;
H-6: ubicación del motor AN-KLA; H-8: rama vigente de SKEVI).

## Recuento

`12 COMPONENTES` (11 `COMPONENT` + 1 `COMPONENT_MINOR`) + `1 PROPUESTA`
(`PROPOSED_COMPONENT`). El número no es criterio de completitud.

Índice de entregables:

* `componentes-v0.md` — Entregable A: registro de los 13.
* `grafo-contratos-v0.md` — Entregable B: `productor → contrato → consumidor`.
* `fronteras-y-hallazgos-v0.md` — Entregable C: solapamientos, fronteras abiertas y registro de discrepancias.
* `runtime-capability-matrix-v0.yaml` — Entregable D: esqueleto sin rellenar.
* `protocolo-runtime-contract-v0.md` — Entregable E: protocolo congelado del experimento.

## Candidatos observados NO incorporados a Aria

Per Amen 19: repositorios presentes en `/Users/krisnova/www/aria` que no
entran al baseline; se listan como candidatos separados (`VERIFIED` su
existencia, `UNKNOWN` su relación con Aria):

* `krathos` (+ `krathos-h2/h3-{coach,executor}`, worktrees sin `.git`
  propio) — Praxis lo nombra como "Coordinación y conocimiento del
  ecosistema" en su tabla de límites (`DECLARED`, praxis-dev/README.md).
* `basanos`, `proteinomenos`, `quantoken` — sin inspección en este ciclo.
* `an-kla-memory` (motor de AN-KLA) vive fuera de `/aria`
  (`/Users/krisnova/www/an-kla-memory`): se registra como el componente
  AN-KLA, con su ubicación real anotada.
