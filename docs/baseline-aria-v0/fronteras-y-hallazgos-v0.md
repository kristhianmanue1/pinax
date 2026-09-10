# Entregable C — Solapamientos, fronteras abiertas y hallazgos (v0)

Snapshot 2026-09-10. Cada punto indica su clase: `DECLARED` (fuente citada),
`INFERRED` (conclusión de Pinax), `PROPOSED` (sin ancla), `VERIFIED`
(evidencia directa), `UNKNOWN`.

## Fronteras entre pares

### Praxis ↔ Epistates

Relación declarada por Epistates (README §4): Epistates pertenece al
ecosistema Praxis y consume "contratos publicados por Praxis"; el manifiesto
de Epistates la clasifica como "relación de diseño... sin dependencia
operativa en código a la fecha" (`DECLARED`). Frontera provisional: Praxis
define contratos/autoridad/evidencia; Epistates supervisa ciclos operativos
mediante adaptadores. Solapamiento potencial de vocabulario (ambos hablan de
"evidencia" y "conformidad") sin solapamiento de responsabilidad declarado
hoy (`INFERRED`).

### Praxis ↔ EKTEL

Sin arista declarada en ningún repositorio (`VERIFIED` negativo en
manifiestos). Frontera del encargo — Praxis puede expresar políticas que un
runtime externo enforced — queda `PROPOSED`. No fusionar conceptos; la
existencia de G1 (task-card de Epistates como entrada de EKTEL) no sustituye
esta frontera.

### Epistates ↔ EKTEL

Arista contractal declarada: G1, task-card/v1 requerida por EKTEL
(`DECLARED`). Frontera abierta: el propósito de Epistates se autodeclara
"entorno de ejecución y supervisión contractual" y el de EKTEL "runtime que
separa admisión autorizada, ejecución restringida y resolución observada"
(`DECLARED` ambos manifiestos). El solapamiento léxico ("ejecución") está
registrado; la pregunta de si EKTEL reemplazará el runtime interno de
Epistates queda abierta y sin respuesta (`UNKNOWN`). No resolver en la
baseline.

### SKEVI ↔ Praxis Dev

Hipótesis del encargo (amen 14): SKEVI organiza cómo desarrollar; Praxis
gobierna qué acciones/decisiones/autoridad/evidencia son válidas. Explicitamente
"no considerar cerrada hasta contrastar ambos repositorios" (`PROPOSED`).
Evidencia parcial disponible: la tabla de límites de Praxis no nombra SKEVI,
y el gate skevi adoptado por pinax opera sobre estructura/tamaños, no sobre
autoridad (`VERIFIED` parcial, lado pinax).

### AN-KLA ↔ Skopos ↔ Ágora

Tres componentes del plano Memory/Information con clases de memoria
distintas (`DECLARED` cada uno): AN-KLA memoria privada de continuidad y
checkpoint por proyecto; Skopos observación y recuperación de
conversaciones/turnos de CLIs; Ágora transformación de fuentes/evidencias
hacia representaciones derivadas con provenance. Sin aristas declaradas
entre los tres (`VERIFIED` negativo en manifiestos/lint). El plano común es
hipótesis, no identidad: no realizan la misma clase de memoria
(`INFERRED`). Fronteras internas del plano: abiertas.

### Argos ↔ assurance / verificación

Argos no certifica verdad total ni sirve como autoridad de ejecución
(`DECLARED`, manifiesto). Su frontera con perfiles de aseguramiento de
Praxis y con los gates de EKTEL/SKEVI no está declarada en ningún repos
(`UNKNOWN`). El mapa registra sólo la capacidad evaluativa con presupuesto
explícito.

### Escrubery ↔ consumidores de inteligencia de modelos/CLIs

Consumidor declarado: Skopos (G4, una sola cara). El resto `UNKNOWN`.
"Posible productor de conocimiento operativo consumible por otros" es
`PROPOSED` hasta que un segundo consumidor lo declare.

### Propylon ↔ (Praxis, EKTEL, Epistates)

Propylon es `PROPOSED_COMPONENT`; las tres fronteras que su maduración
afectaría (autorización, interrupción, PDP/PEP, gate reachability) se
registran como abiertas. Pregunta de pertenencia de responsabilidad sin
resolver (encargo amen 17).

## Propiedades transversales registradas

### Gate reachability (`PROPOSED`, transversal)

"Un gate definido pero evitable por el camino real de promoción no constituye
enforcement suficiente." Distinción entre `gate existence`, `gate
reachability` y `gate unavoidable enforcement`. Evidencia de la propiedad
hoy: parcial y anedótica — el flujo de release de AN-KLA corrigió en
candidato 2 el SHA-256 del wheel registrado por el acta (`09f7aac`,
`VERIFIED`: un gate de identidad se aplicó sobre el propio proceso de
release). En el resto: expectativa arquitectónica sin medición
(`UNKNOWN`/`PROPOSED`). No se impone a ningún proyecto.

### Capability ≠ implementación interna (amen 21, `PROPOSED`)

El futuro Runtime Contract debe poder expresar "función requerida con
proveedor interno, externo o adaptado" (candidato: `secret_injection` vía
`EKTEL → adapter → Llavero` sin `EKTEL = secret store`). Hipótesis a
validar en el experimento; no decisión.

## Registro de hallazgos de la inspección

Discrepancias entre supuestos del encargo/contexto y el estado real
observado. Ninguna fue corregida en silencio ni en repos ajenos.

| # | Hallazgo | Clase | Evidencia | Estado |
|---|---|---|---|---|
| H-1 | El manifiesto de EKTEL declara "M2 sin autorizar" en `no_ofrece`; el acta humana de hoy (2026-09-10) cerró M2 con 15/15. Texto manifiesto anterior al acta. | `VERIFIED` ambos lados | ektel/project-manifest.yaml:17,46 vs docs/decisiones/cierre-m2-2026-09-10.md | Requiere revisión del mantenedor de EKTEL; Pinax no edita |
| H-2 | `skopos/project-manifest.yaml` commiteado tiene YAML malformado (colon sin comillas en "…ADR-014): Ollama…"); `build` fail-closed; el lint no cosecha aristas de skopos | `VERIFIED` | scripts/pinax.py build 2026-09-10; commit 3a3f37a | Requiere corrección del mantenedor de skopos |
| H-3 | El mensaje del commit 3a3f37a de skopos afirma que escrubery "lleva el manifiesto en git": falso; escrubery nunca tuvo `project-manifest.yaml` en su historial | `VERIFIED` negativo | git log --all --diff-filter=AD en escrubery: vacío | Registrado; el mapa refleja la realidad, no el mensaje |
| H-4 | El AGENTS.md de Pinax cita el registro narrativo en `kratos/docs/auditorias/`: ese directorio no existe; el repo se llama `krathos` y lo más cercano es `krathos/docs/gobernanza/{actas,contexto}` | `VERIFIED` negativo | find en /aria; ls krathos/docs | **RESUELTA (F0.1, 2026-09-10): la inferencia era incorrecta.** El hogar existe fuera de `/aria`, en `~/www/kratos/docs/auditorias/` (4 entradas, última 2026-08-13); pinax vivía en `~/www/pinax` al escribirse la línea (acta kratos 2026-08-13 §2) y su reubicación rompió la base relativa. Krathos nació el 24-08 con historias no relacionadas: nunca fue renombre de kratos. Decisión normativa vigente: el Mediador conservó las auditorías como registro histórico al retirar el auditor cross-project (kratos commit `b29dde0`, política de fotografía `a5076d5`). Corregida sólo la referencia en AGENTS.md propio (ruta absoluta + nota de congelación); no se designa hogar nuevo |
| H-5 | "G3/#57 fuera de la baseline beta.25" es cierto a nivel de feature, con matiz: la línea de release contiene la ADR-0048 aceptada y el fix #119; el wheel declara store_root diferido a #57 | `VERIFIED` con matiz | startup.py:142 del wheel instalado; ancestros de dbe9497 | Registrado; leer como "ciclo de feature no entregado" |
| H-6 | El motor AN-KLA vive fuera de `/aria` (`/Users/krisnova/www/an-kla-memory`); sin manifiesto pinax | `VERIFIED` | ls /aria; lint | Registrado en README del baseline |
| H-7 | La memoria interna de Pinax (checkpoint 2026-08-22: "Ágora diferida") quedó obsoleta: docs de Ágora muestran baseline-v1 vigente (2026-09-07) y revisión M1-R1 (2026-09-08) | `VERIFIED` | agora/2026-09-07-agora-baseline-v1.md; 2026-09-08-revision-adversarial-m1-r1.md | El mapa sigue los docs, no la memoria; checkpoint próximo lo reflejará |
| H-8 | SKEVI está en rama `feat/manifest-scripts-adr020`, no en main; su "ancla/identidad vigente" es móvil | `VERIFIED` | git -C skevi branch --show-current | Anotado en componentes-v0.md §2 |
| H-9 | `epistates/task-card` viaja con dos convenciones de id: `…/task-card/v1` (epistates publica, ektel consume) vs `…/task-card` + `version: v1` (pinax consume); el lint no los empareja | `VERIFIED` | manifiestos de epistates, ektel, pinax; lint 2026-09-10 | Requiere decisión de convención entre mantenedores; no es corregible por Pinax |
| H-10 | El ecosistema contiene repos no incorporados a Aria (krathos+worktrees, basanos, proteinomenos, quantoken); praxis nombra "Kratos" como coordinación del ecosistema | `VERIFIED` existencia; `UNKNOWN` relación | ls /aria; tabla de límites de praxis | Candidatos separados; no incorporados (amen 19) |
