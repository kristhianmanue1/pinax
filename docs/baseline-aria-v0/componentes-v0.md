# Entregable A — Registro de componentes (v0)

Snapshot 2026-09-10. Cada afirmación lleva su nivel de certeza y su fuente.
"Manifiesto" = `project-manifest.yaml` (pinax/project-manifest/v1).

---

## 1. Pinax — `COMPONENT` · plano: Ecosystem Map

* **Responsabilidad** (`DECLARED`, manifiesto propio): catálogo y compilador
  del mapa; valida forma, nunca verdad.
* **No ofrece** (`DECLARED`, manifiesto): verificación de verdad, ejecución de
  descubrimiento, control del espacio de IDs (plano del Mediador), gobernanza
  de otros repos, memoria, autoridad, garantía enforced.
* **Publica**: `pinax/project-manifest v1`.
* **Consume**: `an-kla-memory` (continuidad; no requerido), `epistates/task-card v1`
  (política de este repo; no requerido).
* **Estado** (`VERIFIED`): piloto; manifiesto propio `OK` en validación de hoy;
  HEAD `e2ce286` == origin/main.

## 2. SKEVI — `COMPONENT` · plano: Development Method / Normative Process

* **Responsabilidad** (`DECLARED`, README): cuerpo normativo para diseñar
  software y operar agentes; estándar atemporal + guía F0–F3 ejecutable por
  agente; fases, planes, gates, criterios de cierre, disciplina documental,
  revisión adversarial.
* **No es** (`DECLARED`+encargo): runtime, memoria, orquestador, supervisor de
  procesos, autoridad humana, motor de ejecución.
* **Estado** (`VERIFIED`): HEAD `ffc7252`, **rama `feat/manifest-scripts-adr020`**
  (no main); rondas adversariales recientes sobre ADR-028; manifiesto propio
  presente y validando `OK`.
* **Adopción en Pinax** (`VERIFIED`): `skevi-gate.json` + `check_sizes.py`/
  `check_plans.py` adoptados sin edición (docs/adopcion-gate-skevi-2026-08-21.md).
* **Frontera con Praxis** (`PROPOSED`): SKEVI organiza cómo desarrollar; Praxis
  gobierna qué acciones/decisiones/autoridad/evidencia son válidas. No cerrada
  hasta contrastar ambos repos a fondo (encargo amen 14).

## 3. Praxis Dev — `COMPONENT` · plano: Governance

* **Responsabilidad** (`DECLARED`, README): estándar ejecutable de gobernanza
  `0.1.0-draft.1`, diseño fundacional; separa solicitud/autoridad/decisión/
  ejecución/evidencia; "compone herramientas existentes; no las absorbe".
* **No es** (`DECLARED`, README): orquestador, motor de memoria, plataforma de
  colaboración. (Runtime: ver fronteras.)
* **Publica**: contratos/políticas de gobernanza; sin manifiesto pinax hoy.
* **Estado** (`VERIFIED`): README y tabla de límites presentes; sin manifiesto.
* **Frontera enforcement** (`PROPOSED`): Praxis puede expresar políticas y
  condiciones de autorización; un runtime externo puede hacer enforcement.
  No fusionar conceptos. Sin ancla en repo: sólo encargo.

## 4. EKTEL — `COMPONENT` · plano: Execution / Enforcement

* **Estado** (`VERIFIED`): acta humana de cierre `e28da25` (2026-09-10, HEAD
  del repo): `M2 = CLOSED`, `G-M2-01..15 = 15/15 CONFORMING`,
  `M3 = BLOCKED / NOT AUTHORIZED`; implementación cerrada preservada
  `f944493`; MANIFEST-ROOT `b59553bc…`. El cierre es exclusivamente
  documental; no autoriza M3/M4/tags/releases.
* **Limitaciones preservadas** (`DECLARED`, acta): R13-STRONG
  `KNOWN-LIMITATION/OUT-OF-THREAT-MODEL/NO-CLAIM`; no afirma aislamiento
  frente a código arbitrario co-residente, ni interproceso derivado de R15,
  ni recuperación durable del lifecycle local, ni latencia acotada.
* **Publica** (`DECLARED`, manifiesto): 11 contratos wire v1 experimentales
  (`ektel/envelope`, `protected-header`, `capability-payload`,
  `admission-*`, `action-request`, `invocation-proof`, `execution-result`,
  `start-outcome`, `termination-*`).
* **Consume** (`DECLARED`, manifiesto): `epistates/task-card/v1`
  (requerido); `propylon` (canal de interrupción A0 futuro; no requerido).
* **DISCREPANCIA temporal**: su manifiesto declara "M2 sin autorizar" en
  `no_ofrece` — texto anterior al acta de hoy. Ver H-1 en
  `fronteras-y-hallazgos-v0.md`.

## 5. Epistates — `COMPONENT` · plano: Operational Supervision

* **Estado** (`VERIFIED`, README): `0.1.0a2` (sólo prerelease GitHub
  `v0.1.0-alpha.2`; PyPI sin publicar); H1–H4 y E3 cerrados; E4 interno sin
  activar; software experimental sin estabilidad prometida.
* **Responsabilidad** (`DECLARED`, manifiesto): entorno de ejecución y
  supervisión contractual de tareas delegadas a agentes externos; contratos
  task-card/audit-result/preflight; adaptador `opencode-tmux/v1`.
* **Publica** (`DECLARED`, manifiesto): 11 contratos `epistates/*`.
* **Consume** (`DECLARED`, manifiesto): `an-kla` (checkout local; no
  requerido), `praxis` (relación de diseño README §4; sin dependencia
  operativa en código), `tmux` (externo; adaptador).
* **No ofrece** (`DECLARED`, manifiesto): aislamiento por worktrees,
  ejecución automática de comandos, gestión de secretos, memoria semántica,
  plataforma universal, Windows.
* **Relación con Praxis** (`DECLARED`, README §4): "Epistates ────► contratos
  publicados por Praxis"; pertenece al ecosistema Praxis, no al núcleo.

## 6. AN-KLA — `COMPONENT` · plano: Memory / Information

* **Baseline** (`VERIFIED`): `v0.1.0-beta.25` es el último tag publicado
  (`git fetch --tags` en el motor; instalación local en pinax desde ese tag).
* **Ciclo pre-G3 cerrado** (`DECLARED`, commits de release `dbe9497`/`09f7aac`
  del 2026-09-10, con acta REL y registro de SHA-256 del wheel).
* **G3/#57 fuera de la baseline** (`VERIFIED` con matiz): el wheel instalado
  declara en `an_kla/startup.py:142` que declarar `store_root` "belongs to
  issue #57"; ADR-0048 (store_root externo) aceptada 2026-09-05 pero **no
  implementada**. Matiz: la línea de release beta.25 sí contiene los commits
  de la ADR aceptada y el fix #119 (export host-managed). Leer "fuera de la
  baseline" como: ciclo de feature G3 no entregado — ver H-5.
* **Features del encargo** (identidad de artefacto, upgrade desde release
  anterior, black-box contra wheel, contrato contextual versionado, gates
  deterministas, artefacto idéntico al probado): `DECLARED` por actas de
  release y CHANGELOG; método black-box descrito en CHANGELOG.
* **No es** (`DECLARED`+encargo): runtime, supervisor, autoridad.
* **Ubicación**: motor en `/Users/krisnova/www/an-kla-memory`, fuera de
  `/aria` (`VERIFIED`). Sin manifiesto pinax.

## 7. Skopos — `COMPONENT` · plano: Memory / Information

* **Estado** (`VERIFIED`, README): `F3 — pipeline completo funcionando de
  punta a punta con datos reales`: captura → análisis LLM (Ollama local por
  defecto; multi-proveedor ADR-014) → MongoDB local → consulta → vigilante.
* **Multi-CLI** (`VERIFIED`, README): ciclo P-002 cerrado 2026-09-06 —
  captura de 5 CLIs (codex, claude-code, cline, kimi-code, opencode).
* **Consume** (`DECLARED`, README): consulta a escrubery (una sola cara;
  escrubery no lo registra). Sin manifiesto legible: ver H-2.
* **Necesidades potenciales de runtime** (persistencia, filesystem,
  almacenamiento, proveedores LLM): `INFERRED` de su arquitectura declarada;
  **sin fuerza normativa** (encargo §2).
* **DISCREPANCIA**: su `project-manifest.yaml` commiteado tiene YAML
  malformado — ver H-2.

## 8. Ágora — `COMPONENT` · plano: Memory / Information

* **Estado** (`VERIFIED`, docs raíz del repo): `agora-baseline/v1`
  (2026-09-07, `estado: vigente`) congela el instruction pack C0/C1:
  vertical slice `Source → SourceVersion → EvidenceUnit →
  TransformationRun → DerivedRepresentation → consolidación → Revision →
  Query + provenance`. No diseña L0..Ln superiores, ranking global, política
  de verdad ni integración obligatoria.
* **M1-R1** (`VERIFIED`, 2026-09-08): revisión adversarial del harness; "M1-R1
  como base para diseñar M2. **No autoriza ejecutar productores reales**".
  M2 diseñado, NO ejecutado/autorizado.
* **Productor/reviewer/harness separados** (`DECLARED`, M1-R1: reporte propio
  del productor = `unverified_self_report`; M1-R1 no afirma enforcement).
* Sin manifiesto pinax. Memoria interna de pinax (2026-08-22 "diferida")
  quedó obsoleta ante docs 2026-09-07/08 — ver H-7.

## 9. Argos Epistemic — `COMPONENT` · plano: Epistemic Evaluation

* **Estado** (`VERIFIED`): `0.2.0rc2` (pyproject + tag). Manifiesto adoptado
  y validando `OK`.
* **Ofrece** (`DECLARED`, manifiesto): evidencia L0–L5, presupuesto y
  degradaciones explícitas, claims content-addressed con `supports`/`refutes`
  tipados, manifest/envelope/inventory/attestations, fingerprints
  reproducibles, librería Python local.
* **Publica** (`DECLARED`): `argos/evaluation-manifest`, `evaluation-envelope`,
  `discovery-inventory`, `run-attestation`, `claim-record` (v1).
* **Consume** (`DECLARED`, manifiesto): `an-kla` (memoria del checkout
  mantenedor; no requerido, "no forma parte del runtime de Argos").
* **No ofrece** (`DECLARED`, manifiesto): verdad total o certificación
  universal; ejecución de terceros sin sandbox; autorización implícita. Un
  bundle certifica qué observó/configuró/infirió el evaluador — no la verdad
  del sistema (`DECLARED`, encargo+manifiesto).

## 10. Escrubery — `COMPONENT` · plano: External Capability Intelligence

* **Estado** (`VERIFIED`, README): operación continua; releases v0.3.0–v0.5.0;
  backend Evidentia (NestJS+PostgreSQL); vigilancia diaria con introspección
  sandbox de CLIs; checkpoint firmado diario.
* **Ofrece** (`DECLARED`, README): datos normalizados con fuente citada sobre
  modelos, CLIs, precios, contextos, comandos, cambios, divergencias,
  procedencia (hash, Ed25519 por fases, Merkle, timestamps).
* **Publica**: `CONTRATO_API_v0` — contrato JSON de consulta, con ruptura
  permitida hasta cierre de Fase 2 (`DECLARED`, docs/CONTRATO_API_v0.md).
* **No es runtime general** (`DECLARED` por encargo; el README no lo afirma
  explícitamente — clasificación honesta: `INFERRED` de alcance + encargo).
* Sin manifiesto pinax — nunca existió en su git (`VERIFIED` negativo; ver H-3).

## 11. Glosomata — `COMPONENT` · plano: Interface / Interaction Channel

* **Responsabilidad** (`DECLARED`, README): canal de voz 100% local agente↔
  orquestador humano: STT (whisper.cpp), TTS (Kokoro MLX / Piper / say),
  contrato de turnos (libre o por plantilla); consumo como CLI o servidor
  MCP stdio. Sin navegador, sin APIs de terceros, sin retención de audio/texto.
* **Principio** (`DECLARED`, README): "el canal — no el cerebro"; el LLM vive
  en el consumidor; los contadores de sesión son metadata consultiva.
* **No es** (`DECLARED`, README): agente, sistema de decisión; garantía de
  seguridad dependiente de sesión.
* **Relaciones futuras** (sesión/identidad/interrupción/runtime):
  `PROPOSED`, sin evidencia hoy (encargo amen 15).
* Sin manifiesto pinax. Tiene AN-KLA.md propio (`VERIFIED`, ls).

## 12. Llavero — `COMPONENT_MINOR` · plano: Security / Secrets Capability

* **Responsabilidad** (`DECLARED`, README): configuración segura de API keys
  "para skopos (y lo que venga)"; stdlib puro; macOS Keychain; entrada a
  ciegas, guardado cifrado, inyección por entorno sólo al proceso que la
  necesita — el modelo jamás ve la key.
* **Superficie** (`DECLARED`, README): persistir, resolver, inyectar por
  entorno; separación secreto-persistido / proceso-consumidor.
* **No es** (`DECLARED`+encargo): gestor general de identidad, autorización,
  runtime, memoria, orquestador.
* **Madurez menor**: script único, consumidor declarado skopos (`DECLARED`,
  README "Uso con skopos + z.ai"). La clase `COMPONENT_MINOR` describe
  madurez/alcance, no importancia.
* **Hipótesis runtime** (`PROPOSED`): un runtime puede requerir
  solicitar/inyectar secretos sin ser su almacén canónico; Llavero como
  proveedor especializado detrás de la capability. Sin ancla en repos.

## 13. Propylon — `PROPOSED_COMPONENT` · plano: Proposed Gateway / Authorization Boundary

* **Estado** (`VERIFIED`, README): "sin código todavía. Este README documenta
  intención, no implementación." Contenido del repo: LICENSE + README.
* **Propósito preliminar** (`DECLARED`, README): punto de ingreso del
  ecosistema — validar capacidad/autorización (existencia, expiración,
  profundidad de delegación) **antes** de llegar a ektel; alojar parte de la
  vía de interrupción en dominio separado. Precisión del propio README:
  recibir una señal no es tener la potestad de detener; es "una pieza de esa
  vía, no su totalidad".
* **Clasificación** (`PROPOSED_COMPONENT` + `ARCHITECTURAL_PROPOSAL`): no es
  dependencia ni componente operativo. Pregunta abierta (no resolver en la
  baseline): ¿responsabilidad independiente o funciones repartibles entre
  Praxis/EKTEL/Epistates/gateway común vía contratos?
* **Arista entrante declarada** (`DECLARED`, manifiesto ektel): canal de
  interrupción A0 futuro, no requerido — arista hacia una propuesta.
