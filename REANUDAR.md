# REANUDAR — sesión 2026-08-20 (documento temporal de contexto)

**Para:** el agente de Pinax (o cualquier agente de aria) que abra la
próxima sesión. Léelo completo: es corto. Después ejecuta el protocolo de
arranque de `/Users/krisnova/www/pinax/docs/guia-an-kla-pinax.md`.

## Qué pasó hoy (2026-08-20)

1. **Visión de ecosistema** sobre skopos (memoria de agentes) y ektel
   (preparación para M0). Mi v1 tenía 2 BLOCKER factuales; los encontré en
   autocritica; Codex CLI y Claude CLI hicieron rondas adversariales
   independientes con autocrítica propia obligatoria y firma asentada.
2. **Documento final firmado por tres modelos:**
   `/Users/krisnova/www/pinax/rondas/2026-08-20-vision-skopos-ektel/vision-final-firmada.md`
   (incorpora X-1, X-2 de Codex e Y-1..Y-7 de Claude).
3. **Decisión del dueño:** skopos será **multi-CLI** (Claude Code, Kimi
   CLI, Qwen CLI…); P-001 (integración AN-KLA) queda **superada** — su
   única justificación era cobertura y se resuelve con parsers propios.
4. **Encargos emitidos** a agentes de skopos y ektel: prosa
   (`instruccion-agente-*.md`) + contratos `task-card/v1` **validados
   con epistates** (`task-card-*.json`, ambos VALID). Están trabajando.
5. **AN-KLA inicializado en pinax** (tag beta.15, `.an-kla/` local
   gitignored). Primer episodio escrito por flujo gobernado.
6. **Adopciones como orquestador:** skevi (método), an-kla (memoria),
   epistates (encargos), argos (evidencia de rondas, pendiente de uso),
   escrubery (verdad versionada de CLIs). Disciplina: proteinomenos
   (rondas), praxis-dev (gobernanza, primer adoptante).
7. Commit del ciclo en pinax: `54c1109`. Sin push (requiere autorización).

## Estado de los frentes abiertos

| Frente | Estado | Próximo acto | De quién |
|---|---|---|---|
| skopos | Agente trabajando con encargo (C-9→C-8→C-10→C-6→C-5, luego escrubery REQ-10 y parser multi-CLI) | Recibir reporte con evidencia rag/v1; decisiones 🔒 pendientes del dueño (C-8 mutación vs retención, política de arranque, C-6) | dueño decide, agente ejecuta |
| ektel | Agente trabajando: borradores de acta de consenso v1.2 + acta de autorización M0, corrección README conservando no-claim, corrida Linux de las 8 pruebas | **Consenso del dueño sobre v1.2** → autorización de M0. Es el cuello de botella del ecosistema: sin ektel no hay garantía `enforced` de nada | dueño |
| pinax | Memoria propia + política + guía escritas hoy | Cosechar `project-manifest.yaml` de skopos y ektel cuando reporten; generar `/Users/krisnova/www/aria/AGENTS.md` índice del ecosistema (propuesto, no autorizado aún) | pinax con autorización |
| claude CLI | No lee su sesión del llavero desde shells no interactivos | Workaround probado y funcionando: `CLAUDE_CODE_OAUTH_TOKEN=$(security find-generic-password -s "Claude Code-credentials" -w \| python3 -c "import sys,json;print(json.load(sys.stdin)['claudeAiOauth']['accessToken'])")` | quien lo invoque |

## Herramientas del ecosistema y cómo descubrirlas (regla 3 propuesta)

Antes de usar una herramienta de aria, corre su comando de descubrimiento:

| Herramienta | Descubrimiento | Qué es |
|---|---|---|
| an-kla-memory | `.venv/bin/python -m an_kla capabilities` | memoria gobernada por proyecto |
| epistates | `.venv/bin/python -m epistates describe` | contratos task-card + validador |
| escrubery | `~/www/aria/escrubery/scripts/consultar listar` | inteligencia de CLIs/modelos con procedencia |
| skevi | `docs/ai-agent-guide/00-INDICE.md` | método F0→F3 de construcción |
| argos | README (sin CLI estable aún) | análisis con evidencia L0–L5, claims content-addressed |
| praxis-dev | `docs/estandar.md` (draft) | gobernanza ejecutable |

Guías de notas aprendidas (leer antes de depurar):
`/Users/krisnova/www/aria/escrubery/docs/an-kla-guia.md` y
`/Users/krisnova/www/pinax/docs/guia-an-kla-pinax.md`.

## Lecciones de método (no negociables, vienen de errores reales de hoy)

1. Afirmación de estado ⇒ verificar contra git/código/evidencia, nunca
   README solo.
2. Verificación citada ⇒ declarar si el verificador es quien firma.
3. Antes de depurar una herramienta, buscar la guía de notas de otro
   proyecto (mi fallo `authority_scope_mismatch` ya estaba resuelto en
   escrubery).
4. Métricas siempre fechadas como snapshot.
5. "Nadie obliga" es falso a medias: la obligación estructural existe —
   DoD ejecutable, gates con exit code, propongo/aplico, evidencia como
   condición de aceptación. Lo que no existe aún es contención de
   ejecución: eso es ektel.

## Estado de este documento

Temporal: su contenido durable vive en la memoria AN-KLA de pinax
(episodio `episodio-rondas-vision-2026-08-20` + checkpoint de cierre) y en
los commits. Cuando el mapa (MAPA.md) incluya estos estados, este archivo
puede borrarse.
