# Orquestación de desarrollo multiagente con agentes CLI y tmux

**Versión:** 2.0 (2026-08-18) · v1.0 en `backup/orquestacion-codex-opencode-tmux-v1.0-20260818.md`
**Estado:** estándar operativo validado (ronda adversarial proceed 2026-08-12; topología T3 añadida y validada en escrubery 2026-08-18)
**Ámbito:** proyectos de software locales en macOS o Linux
**Modelo principal:** humano orquestador → agente controlador/auditor → agente ejecutor
**Binding de referencia:** Codex CLI (controlador) + OpenCode (ejecutor) + tmux — el protocolo es agnóstico de herramienta (§2.1)
**Topologías:** T1 automática (controlador en tmux), T2 directa (controlador desktop), T3 headless/relay (controlador sin pane direccionable)
**Dependencias conceptuales:** ADRC, sesiones persistentes, revisión adversarial y evidencia ejecutable
**Dependencias de runtime:** ninguna respecto de Escrubery o Epistates
**Compatibilidad verificada (2026-08-18):** opencode 1.18.18, tmux 3.6a, macOS

## 1. Propósito

Esta guía define un método para delegar trabajo de desarrollo a agentes CLI sin
mantener al controlador consultando constantemente el progreso.

El objetivo es que:

- el humano conserve la dirección del proyecto y la autorización de release;
- Codex CLI actúe como controlador, planificador y auditor;
- OpenCode implemente y pruebe el trabajo dentro de un worktree;
- tmux mantenga vivas y visibles las sesiones;
- Codex quede realmente inactivo mientras OpenCode trabaja;
- OpenCode despierte a Codex mediante un mensaje al terminar;
- las ventanas de Codex y OpenCode permanezcan visibles para el orquestador;
- exista una ronda adversarial antes de considerar terminado un hito;
- el resultado se verifique con Git, pruebas y evidencia real.

Este mecanismo no convierte la salida de un agente en verdad ni autorización.
El reporte del ejecutor es una afirmación que el controlador debe contrastar.

La guía admite dos topologías que no deben mezclarse durante una misma tarea:

- **modo automático:** Codex CLI y OpenCode viven en sesiones tmux distintas;
  OpenCode despierta a Codex con `AGENT_DONE`;
- **modo directo:** Codex Desktop conserva el control y sólo OpenCode vive en
  tmux; el humano avisa a Codex Desktop cuando ve la marca final.

El modo automático sigue siendo el recomendado para trabajos largos sin
supervisión. El modo directo es una alternativa deliberada para pilotos,
depuración del protocolo y tareas en las que el humano observa la ventana.

## 2. Principio central

```text
sesión viva ≠ trabajo activo ≠ trabajo correcto ≠ verificación ≠ autorización
```

- tmux demuestra que una sesión puede persistir.
- una salida en terminal puede indicar progreso, pero no corrección.
- una suite verde aporta evidencia, pero no autoriza una publicación.
- una notificación sólo indica que llegó el momento de inspeccionar.
- el humano conserva las decisiones de alcance importante y release.

### 2.1 Estándar agnóstico de herramienta: protocolo vs bindings

Este documento es un **protocolo** (roles, máquina de estados, tarjeta, entrega,
auditoría, adversarial) con **bindings** concretos. El protocolo no depende de
ningún agente; los bindings sí:

| Requisito del protocolo | Binding de referencia | Alternativas válidas |
|---|---|---|
| Agente controlador/auditor interactivo | Codex CLI | Qwen Code, Claude Code, cualquier CLI LLM con tools de shell |
| Agente ejecutor | OpenCode | Codex CLI, otro agente con acceso a worktree |
| Sesiones persistentes visibles | tmux | Terminal persistente equivalente |
| Wake-up del controlador | `AGENT_DONE` vía `send-keys` (T1) | notificación humana (T2/T3), scheduler del controlador |
| Interfaz de entrega | archivo de reporte + tarjeta | SIEMPRE archivo; nunca transcript |

Al adoptar el estándar con otras herramientas, sustituir el binding conservando
el requisito. Si un binding no puede cumplir un requisito (p. ej. el controlador
no vive en tmux y no puede recibir `AGENT_DONE`), **cambiar de topología**
(§4.2), no forzar el mecanismo.

### 2.2 Principio de interfaz de comunicación

- **Los archivos son la interfaz entre agentes:** tarjeta de trabajo, tarjetas de
  corrección y reporte final. Son inmutables por intento y verificables.
- **Los mensajes tmux son sólo interrupciones:** `AGENT_DONE`/`AGENT_BLOCKED`
  (o el aviso humano en T2/T3) indican *cuándo* inspeccionar; no transportan
  contenido de trabajo ni constituyen evidencia.
- **Los transcripts no son entrada:** el controlador audita por Git, archivos y
  comandos ejecutados por él. Leer el transcript del ejecutor contamina el
  contexto del auditor con ruido de herramienta y rompe la independencia.
- Esto es también disciplina de costo: los tokens del controlador se gastan en
  auditar artefactos, no en observar proceso.

## 3. Roles

### 3.1 Orquestador humano

- define objetivo y prioridades;
- autoriza el inicio del ciclo;
- resuelve decisiones importantes o ampliaciones de alcance;
- puede observar las ventanas tmux cuando lo desee;
- conserva la autorización exclusiva para merge final, tag y release;
- puede pedir una auditoría externa adicional.

### 3.2 Codex CLI — controlador y auditor

- lee las instrucciones del repositorio;
- revisa issues, PRs, memoria y estado Git cuando corresponda;
- divide el trabajo y crea una tarjeta verificable;
- prepara rama, worktree y sesiones;
- lanza OpenCode con permisos suficientes;
- termina su turno y queda en el prompt, sin polling;
- al despertar, inspecciona el diff y ejecuta verificaciones independientes;
- envía correcciones concretas si encuentra fallas;
- puede ejecutar CI local, crear ramas, commits y push de ramas cuando esté
  autorizado por la tarea;
- se detiene antes de merge final, tag o publicación de release.

### 3.3 OpenCode — ejecutor

- trabaja sólo sobre el objetivo y worktree asignados;
- modifica código, documentación y tests dentro del alcance;
- ejecuta los checks del Definition of Done;
- realiza o coordina una ronda adversarial con contexto fresco;
- corrige los hallazgos aplicables;
- deja un reporte con comandos y resultados reales;
- notifica a Codex por tmux y termina.

### 3.4 Auditor externo opcional

Un segundo controlador, agente de escritorio o humano puede inspeccionar el
estado cuando el orquestador lo solicite. No debe hacer polling permanente ni
interferir con el ejecutor salvo orden explícita.

## 4. Topología de procesos

### Invariantes obligatorios del modo automático

1. Codex y OpenCode se ejecutan en **sesiones tmux distintas**.
2. Cada sesión se muestra en una ventana o pestaña de terminal visible para el
   orquestador humano durante toda la ejecución.
3. No basta con que la sesión exista en segundo plano: después de crearla se
   abre o adjunta una terminal visible.
4. OpenCode **debe despertar a Codex por tmux para entregar el trabajo**.
5. OpenCode no puede marcar la tarea como entregada ni terminar silenciosamente
   antes de enviar `AGENT_DONE` y la pulsación `Enter` a la sesión Codex.
6. Si OpenCode no puede terminar, envía `AGENT_BLOCKED` con una causa breve para
   despertar a Codex; no queda esperando permisos indefinidamente.

```text
Terminal visible
└── tmux: <proyecto>-codex-<tarea>
    └── Codex CLI interactivo
        ├── prepara y supervisa el ciclo
        └── queda inactivo en el prompt

Terminal o ventana visible
└── tmux: <proyecto>-opencode-<tarea>
    └── OpenCode ejecutor
        ├── implementa
        ├── prueba
        ├── ejecuta revisión adversarial fresca
        ├── corrige
        └── envía AGENT_DONE a la sesión Codex
```

Para una independencia adversarial mayor puede usarse una tercera sesión:

```text
tmux: <proyecto>-review-<tarea>
└── OpenCode nuevo, otro agente o preferiblemente otro modelo
```

### 4.1 Modo directo validado: Codex Desktop → OpenCode interactivo

En este modo no se crea una segunda instancia de Codex CLI. Codex Desktop es el
único controlador técnico y OpenCode se ejecuta interactivamente en tmux:

```text
Codex Desktop (controlador y auditor)
└── Terminal visible
    └── tmux: <proyecto>-opencode-<tarea>
        └── opencode interactivo
```

Reglas específicas:

1. no existe una sesión tmux receptora de Codex y por tanto OpenCode no puede
   usar `AGENT_DONE` para despertar esta conversación Desktop;
2. el humano observa la marca final y avisa a Codex Desktop;
3. Codex Desktop inspecciona Git y ejecuta los gates igual que en el modo
   automático;
4. la sesión interactiva permanece abierta para correcciones conversacionales;
5. no se lanza otro controlador que pueda editar simultáneamente el worktree.

El arranque de este modo fue validado al iniciar H4 Slice3 de Epistates.
Conserva visibilidad y persistencia, pero no ofrece wake-up automático ni pausa
totalmente autónoma.

### 4.2 Topología T3 — controlador headless con supervisor (relay)

Cuando el controlador es un agente LLM que **no vive en tmux ni en una app de
escritorio con pane direccionable** (p. ej. una sesión CLI headless de Qwen Code
o similar), `AGENT_DONE` no puede alcanzarlo. La entrega la hace el humano (o el
scheduler del propio controlador), y se añade un rol de **supervisor externo**:

```text
Supervisor (agente externo, auditor de última línea)
└── controlador headless (turnos cortos; pausa real al terminar cada turno)
    └── tmux: <proyecto>-opencode-<tarea> (visible)
        └── opencode ejecutor
```

Reglas específicas:

1. el controlador termina su turno y pausa de verdad; no hay polling;
2. el ejecutor deja marca final visible (`FIN <TASK>-IMPLEMENTATION`) y reporte
   escrito; el humano avisa al controlador o al supervisor;
3. el supervisor audita lo que el controlador aprueba, por Git/archivos/gates —
   nunca por transcript del ejecutor (§2.2);
4. la autoridad de commit se define explícitamente por tarea (puede delegarse al
   controlador para agilizar; merge/PR/release quedan en humano+supervisor);
5. si el controlador headless necesita delegar en otro agente, puede lanzarlo en
   tmux y actuar como controlador de ese ejecutor — la topología se compone.

**Validación (2026-08-18, escrubery):** el gap T3 se detectó en vivo — un
supervisor Qwen Code headless no podía recibir `AGENT_DONE`; la solución
adoptada fue **T1 + supervisor externo (§3.4)**: controlador qwen-code en tmux
(recibe el wake-up) + ejecutor opencode en tmux + supervisor headless como
auditor de última línea. T3 pura queda para controladores headless sin
alternativa tmux; la doble auditoría se logra componiendo T1 + supervisor.

### 4.3 Selección de topología

| Pregunta | T1 | T2 | T3 |
|---|---|---|---|
| ¿El controlador vive en un pane tmux? | sí | no (desktop) | no (headless) |
| Wake-up automático al controlador | `AGENT_DONE` | no: humano | no: humano/scheduler |
| Pausa totalmente autónoma | sí | parcial | sí (por turnos) |
| Doble auditoría (supervisor) | opcional | opcional | natural |
| Recomendada para | trabajos largos sin supervisión | pilotos observados | controladores headless, doble auditoría |

No mezclar topologías dentro de una misma tarea. Si el binding no cumple el
requisito de wake-up, cambiar de topología, no forzar el mecanismo (§2.1).

## 5. Máquina de estados operativa

```text
PREPARED
  → EXECUTOR_RUNNING
  → WAITING_EXTERNAL
  → EXECUTOR_DONE
  → AUDITING
  → CORRECTION_SENT → WAITING_EXTERNAL
  → ADVERSARIAL_REVIEW
  → CI_LOCAL
  → READY_FOR_HUMAN
  → RELEASED | BLOCKED
```

Reglas:

1. `WAITING_EXTERNAL` significa que Codex terminó su turno y está en el prompt.
2. No se implementa espera mediante `sleep`, bucles o capturas repetidas.
3. `AGENT_DONE` sólo habilita auditoría; no significa aceptación automática.
4. Una corrección conserva la misma tarea y aumenta el número de intento.
5. `READY_FOR_HUMAN` es el límite de autonomía para publicación.

## 6. Preparación del repositorio

Antes de lanzar agentes:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git worktree list
tmux list-sessions
```

Si un nombre de sesión ya existe, inspecciónalo y decide si corresponde al mismo
`run_id`; adjunta esa sesión o usa un nombre nuevo. No la reemplaces ni la mates
automáticamente, porque podría contener trabajo vigente.

El controlador debe identificar:

- repositorio y raíz esperados;
- SHA base;
- rama de trabajo;
- ruta absoluta del worktree;
- instrucciones `AGENTS.md` aplicables;
- issues y PRs abiertos cuando el repositorio use GitHub como backlog;
- pruebas base obligatorias;
- archivos autorizados y prohibidos;
- operaciones Git autorizadas;
- operación que requiere autorización humana final.

Ejemplo de nombres:

```text
task_id: issue-60-g-view
run_id: issue-60-g-view-20260812-01
attempt_id: 1
controller_session: an-kla-codex-issue60
controller_pane: %<pane-id>
executor_session: an-kla-opencode-issue60
executor_pane: %<pane-id>
worktree: /ruta/absoluta/proyecto-wt-issue60
branch: codex/issue-60
```

### 6.1 Integración con el contrato de agentes del repo destino

Si el repositorio tiene su propio contrato para agentes (`AGENTS.md`, política
de procedencia, reglas de gobernanza), **ese contrato manda sobre esta guía**.
Antes de lanzar agentes, el controlador debe:

1. leer el `AGENTS.md` (o equivalente) del repo destino y extraer sus reglas
   duras (qué no se edita, qué exige procedencia, quién autoriza commits);
2. volcar esas reglas en la tarjeta: prohibiciones explícitas y DoD que incluya
   los gates propios del repo (p. ej. `check_sizes`, CI local);
3. reconciliar la autoridad de Git: si el repo exige aprobación humana para
   commitear (patrón Mediador de ADRC), la tarjeta lo declara y esta guía cede
   (§15 es un default, no una autorización);
4. respetar capas de memoria/estado del repo (p. ej. AN-KLA) sin escribirlas
   salvo por sus flujos gobernados.

Ejemplo real (escrubery, 2026-08-18): repo con procedencia obligatoria,
generados que no se editan a mano y commits con autorización humana; la tarjeta
del piloto incorporó esas reglas como prohibiciones y el gate
`bash scripts/ci_local.sh` como DoD; el commit se delegó al controlador solo
tras autorización explícita del orquestador.

## 7. Tarjeta de trabajo

La tarjeta es el contrato operativo entre Codex y OpenCode. Debe vivir en un
archivo `.md` pequeño, legible y verificable.

### 7.1 Campos mínimos

```markdown
# Tarea: <task_id>

## Identidad
- Repositorio: <owner/repo>
- Worktree: <ruta absoluta>
- Rama: <rama>
- SHA base: <sha completo>
- Run: <run_id>
- Intento: <attempt_id>
- Sesión Codex: <controller_session>
- Pane Codex: <controller_pane>
- Sesión OpenCode: <executor_session>
- Pane OpenCode: <executor_pane>

## Objetivo
<un solo resultado concreto>

## Entradas obligatorias
- AGENTS.md
- documentación o ADR aplicable
- issue o especificación

## Alcance permitido
- <rutas y tipos de cambio>
- ejecutar tests, lint y gates
- corregir fallas dentro del alcance

## Fuera de alcance
- cambios no relacionados
- borrados destructivos
- reescritura de historia Git
- merge, tag o release

## Definition of Done
- [ ] <comando> → <resultado esperado>
- [ ] <test focal>
- [ ] suite completa
- [ ] git diff --check
- [ ] reporte final con evidencia
- [ ] ronda adversarial con decisión proceed

## Ronda adversarial
Usar un contexto fresco. Buscar BLOCKER/HIGH/MED/LOW, corregir los hallazgos
aplicables y repetir los checks. No limitarse a estilo.

## Cierre
Guardar el reporte en <ruta>. Después enviar a Codex:
AGENT_DONE task=<task_id> run=<run_id> attempt=<attempt_id> report=<ruta>
```

### 7.2 Regla de tamaño

Una tarea debe caber holgadamente en una sesión. Si mezcla múltiples contratos,
formatos o subsistemas críticos, se divide en fases. Cada fase deja un diff
pequeño y revisable.

## 8. Lanzamiento de Codex CLI en tmux

Codex debe ejecutarse en modo interactivo, no como proceso `exec` que termina al
final de una respuesta.

Antes de crear sesiones, confirma una vez que las opciones usadas existen:

```bash
codex --version
codex --help
opencode --version
opencode run --help
tmux -V
```

Si una versión no expone `--approve-for-me`, `--auto`, `--model` o `--continue`,
adapta el comando antes de lanzar; no entres a `WAITING_EXTERNAL` con un CLI que
terminó inmediatamente por una opción inválida.

Ejemplo conceptual:

```bash
tmux new-session -d -s an-kla-codex-issue60 \
  -c /ruta/absoluta/al/worktree

tmux display-message -p -t an-kla-codex-issue60:0.0 '#{pane_id}'

tmux send-keys -t %<controller-pane-id> \
  "codex -C /ruta/absoluta/al/worktree --sandbox workspace-write --approve-for-me --no-alt-screen" Enter
```

Registra el `%pane-id` devuelto en la tarjeta. Es el destino estable para los
mensajes de OpenCode aunque el humano cree otras ventanas o cambie el pane
activo de la sesión.

La sesión se muestra inmediatamente al orquestador. En macOS con Terminal:

```bash
osascript -e 'tell application "Terminal" to do script "tmux attach-session -t an-kla-codex-issue60"'
```

En Linux, el equivalente depende del emulador disponible; por ejemplo:

```bash
gnome-terminal -- tmux attach-session -t an-kla-codex-issue60
```

La ventana visible es parte del contrato operativo: no se considera lanzado el
controlador hasta que el orquestador pueda observarla.

Después se entrega a Codex una tarjeta de controlador. El texto debe indicarle:

- que puede trabajar con autonomía dentro del worktree;
- que puede lanzar OpenCode y administrar tmux;
- que puede ejecutar CI local, crear commits y gestionar la rama autorizada;
- que debe auditar independientemente los reportes;
- que debe finalizar cada turno y quedar en el prompt;
- que no debe hacer polling;
- que debe detenerse antes de merge/tag/release.

`--approve-for-me` permite que Codex resuelva de forma automática las
aprobaciones compatibles con `workspace-write`. No debe usarse bypass total de
sandbox salvo que exista un sandbox externo real y el humano lo haya decidido.

## 9. Lanzamiento de OpenCode

Codex crea una segunda sesión visible:

```bash
tmux new-session -d -s an-kla-opencode-issue60 \
  -c /ruta/absoluta/al/worktree

tmux display-message -p -t an-kla-opencode-issue60:0.0 '#{pane_id}'
```

Puede iniciar OpenCode con el modelo definido para el proyecto:

```bash
tmux send-keys -t %<executor-pane-id> \
  "opencode run --auto --model <proveedor/modelo> 'Lee completamente <tarjeta.md> y ejecútala'" Enter
```

Registra también este `%pane-id`. Tras el arranque realiza **una sola**
inspección acotada:

```bash
tmux list-panes -t an-kla-opencode-issue60 \
  -F '#{pane_id}|#{pane_dead}|#{pane_current_command}|#{pane_current_path}'
```

Entra a `WAITING_EXTERNAL` únicamente si el pane está vivo, su ruta corresponde
al worktree y el comando observado es OpenCode. Esto es un preflight único, no
polling.

Codex debe abrir también esta sesión en otra ventana o pestaña visible. En
macOS con Terminal:

```bash
osascript -e 'tell application "Terminal" to do script "tmux attach-session -t an-kla-opencode-issue60"'
```

El orquestador debe poder ver simultáneamente o alternar directamente entre:

- ventana Codex: planificación, espera, auditoría y correcciones;
- ventana OpenCode: implementación, pruebas y ronda adversarial.

Que OpenCode sea lanzado por Codex no autoriza dejar su sesión oculta.

Para evitar problemas de quoting en tareas grandes, la instrucción enviada al
CLI debe ser breve y apuntar al archivo de tarjeta; el contenido completo no se
incrusta en el comando.

### 9.1 Dos formas de iniciar OpenCode

#### One-shot con entrega automática

`opencode run` recibe la instrucción en el propio comando, por lo que no existe
una carrera entre el arranque de la TUI y la inyección del primer prompt. Es la
forma recomendada para el modo automático:

```bash
tmux new-session -d -s <executor-session> -c <worktree>
tmux send-keys -l -t %<executor-pane-id> -- \
  "opencode run --auto 'Lee completamente <tarjeta.md> y ejecútala'"
tmux send-keys -t %<executor-pane-id> Enter
```

Al terminar vuelve normalmente al shell; las correcciones requieren otro
`opencode run --continue` o una ejecución nueva.

#### Interactivo persistente para observación y control humano

Cuando el humano necesita observar con colores, escribir preguntas o intervenir
durante la ejecución, esta es la forma recomendada. No debe lanzarse
`opencode run`: ese subcomando es one-shot y su salida puede parecer una TUI,
pero no ofrece un prompt conversacional. Cambiar Terminal.app por iTerm2 no
convierte un `run` en interactivo.

Para conservar además un shell recuperable si OpenCode termina o se interrumpe,
crea primero la sesión tmux y arranca la TUI en su pane:

```bash
tmux new-session -d -s <executor-session> -c <worktree>
tmux display-message -p -t <executor-session>:0.0 '#{pane_id}'
tmux send-keys -l -t %<executor-pane-id> -- \
  'opencode --auto --model <proveedor/modelo>'
tmux send-keys -t %<executor-pane-id> Enter
```

No uses `--continue` cuando el objetivo sea un revisor con contexto fresco. Usa
`--continue` sólo cuando conservar deliberadamente la conversación previa sea
parte del contrato del intento.

En macOS, iTerm2 ofrece una visualización más fiel de colores ANSI y pantalla
completa. Abrir una ventana visible sin reiniciar el proceso:

```bash
osascript \
  -e 'tell application "iTerm2"' \
  -e 'activate' \
  -e 'set w to (create window with default profile)' \
  -e 'tell current session of w to write text "tmux attach-session -t <executor-session>"' \
  -e 'end tell'
```

La ventana es sólo un cliente: cerrar iTerm2 no mata la sesión tmux. Puede
reabrirse y adjuntarse de nuevo al mismo agente.

Hay una carrera de arranque real: `pane_current_command=opencode` no demuestra
que la TUI ya acepte entrada. Si se envía el prompt inmediatamente, éste puede
perderse. El orden validado es:

1. crear la sesión;
2. abrir la ventana visible;
3. hacer una inspección única y confirmar que aparece el prompt `Ask anything`;
4. sólo entonces enviar el texto literal y `Enter` en llamadas separadas;
5. confirmar una vez que la tarea aparece en la TUI o que OpenCode comenzó a
   pensar/leer la tarjeta.

```bash
tmux capture-pane -p -t <executor-session>:0 -S -40

tmux send-keys -l -t <executor-session>:0 -- \
  'Lee completamente <tarjeta.md> y ejecuta la tarea. No hagas commit.'
tmux send-keys -t <executor-session>:0 Enter
```

Si la inspección muestra que la TUI terminó de iniciar pero la tarea no aparece,
se permite reenviar **una vez** la misma instrucción exacta. Esto es recuperación
del lanzamiento, no polling ni un nuevo intento contractual.

Después del arranque, humano y controlador comparten el mismo pane:

- el humano escribe directamente en iTerm2;
- Codex puede usar `tmux send-keys -l -t %<executor-pane-id>` y una llamada
  separada con `Enter`;
- ambos pueden inspeccionar la salida, y `AGENT_DONE` puede seguir dirigido al
  pane exacto del controlador si éste vive en tmux.

No deben escribir simultáneamente. El humano avisa antes de intervenir y el
controlador no inyecta texto mientras haya entrada humana en curso.

#### Migrar un one-shot estancado a TUI fresca

Si `opencode run` guardó sus cambios pero quedó esperando un subagente o dejó de
producir actividad:

1. inventariar el estado Git y la última modificación de los artefactos;
2. interrumpir una vez con `C-c` y confirmar que el pane volvió al shell;
3. crear una tarjeta inmutable para el intento siguiente, limitada al trabajo
   pendiente;
4. lanzar `opencode --auto --model ...` **sin** `run` y, si se requiere contexto
   fresco, sin `--continue`;
5. abrir iTerm2, esperar `Ask anything`, enviar tarjeta + `Enter` por separado y
   confirmar una vez que aparece `Thinking` o que la tarjeta fue leída.

Los archivos ya escritos permanecen en el worktree; se pierde sólo el estado
conversacional no persistido del proceso interrumpido. Un revisor fresco debe
revalidar las afirmaciones en vez de heredar conclusiones del one-shot.

### 9.2 Permisos prácticos de OpenCode

En desarrollo normal se recomienda autonomía amplia:

- lectura, búsqueda, edición y patches: permitidos;
- bash necesario para tests, linters y herramientas del proyecto: permitido;
- subagentes o tareas de revisión: permitidos;
- escritura dentro del worktree: permitida;
- acceso a dependencias o red: permitido cuando la tarea lo requiera;
- commit: puede reservarse a Codex para mantener separación de responsabilidades;
- push, merge, tag y release: reservados al controlador/humano.

El objetivo no es pedir aprobación por cada comando, sino impedir únicamente
acciones claramente fuera del ciclo de desarrollo.

## 10. Pausa real de Codex

Después de confirmar que OpenCode arrancó, Codex debe responder con un estado
breve y terminar su turno. Ejemplo:

```text
OpenCode ejecutándose en an-kla-opencode-issue60.
Estado: WAITING_EXTERNAL.
```

En ese momento:

- Codex permanece abierto dentro de tmux;
- el cursor queda en el prompt de entrada;
- no hay generación de tokens;
- no se ejecutan `sleep`, polling ni `capture-pane` repetidos;
- el humano puede observar ambas ventanas.

Un proceso vivo consume recursos locales mínimos, pero no inferencia mientras
no reciba un nuevo mensaje.

En el modo directo, Codex Desktop no tiene un pane que OpenCode pueda despertar.
El controlador termina su turno y el humano lo reactiva al observar la marca
final. No debe simularse el wake-up mediante polling desde Desktop.

## 11. Ronda adversarial

La revisión adversarial debe usar contexto fresco. Hay dos modalidades.

### Modalidad A — coordinada por OpenCode

El ejecutor termina la implementación y lanza un subagente o sesión de revisión
nueva. El revisor inspecciona el diff, los requisitos y las pruebas. El ejecutor
corrige hallazgos y repite hasta obtener `proceed` o `escalate`.

Es la modalidad más rápida y suficiente para trabajo cotidiano.

### Modalidad B — coordinada por Codex

OpenCode completa su ciclo normal y notifica `AGENT_DONE`. Codex audita la
entrega y luego lanza una sesión de revisión nueva, preferiblemente con otro
modelo. Si el reviewer es externo, Codex puede volver a `WAITING_EXTERNAL`
hasta recibir su propio `AGENT_DONE`. Es más adecuada para cambios críticos o
releases y no introduce un segundo protocolo de notificación.

### Modalidad C — revisor como subagente del controlador/supervisor

El controlador (o el supervisor externo) delega la revisión en un subagente de
contexto fresco dentro de su propio runtime. Fue la modalidad usada en los
cierres H4/H5 de escrubery (2026-08-18): el supervisor lanzó un subagente
independiente que ejecutó los gates y produjo el veredicto.

Trade-offs honestos:

- a favor: rápida, barata, el revisor ejecuta evidencia real con las mismas
  herramientas del proyecto; el controlador conserva el contexto de la tarea;
- en contra: misma familia de modelo que el auditado (menos decorrelación que
  un proveedor distinto); el sesgo del modelo puede repetirse en ambos lados.

Regla de uso: modalidad C para hitos cotidianos; modalidad B con **otro
proveedor/modelo** para cambios críticos y releases (la decorrelación real es
el punto de un quórum). El formato del reporte es el mismo en las tres.

### Formato del reporte adversarial

```markdown
## Hallazgos
- [BLOCKER] problema — evidencia — corrección requerida
- [HIGH] problema — evidencia — corrección requerida
- [MED] problema — evidencia — corrección sugerida
- [LOW] problema — evidencia — seguimiento opcional

## Verificaciones
- comando → resultado real

## Decisión
proceed | fix-and-retry | escalate
```

No se considera adversarial una revisión que sólo elogia el cambio o señala
estilo. Debe atacar invariantes, compatibilidad, errores silenciosos, casos edge
y correspondencia exacta con el contrato.

## 12. Notificación OpenCode → Codex

Al terminar el trabajo y escribir todos los archivos, OpenCode **obligatoriamente
despierta a Codex** enviando una línea breve a su sesión tmux. Este envío es el
mecanismo de entrega entre agentes, no un paso opcional.

Ejemplo:

```text
AGENT_DONE task=issue-60-g-view run=issue-60-g-view-20260812-01 attempt=1 report=docs/planning/issue-60-report.md
```

La entrega se realiza en dos llamadas:

```bash
tmux send-keys -l -t %<controller-pane-id> -- \
  'AGENT_DONE task=issue-60-g-view run=issue-60-g-view-20260812-01 attempt=1 report=docs/planning/issue-60-report.md'

tmux send-keys -t %<controller-pane-id> Enter
```

La primera llamada escribe texto literal. La segunda pulsa Enter. Separarlas
evita que el mensaje se quede visible sin ejecutarse o que tmux interprete parte
del texto como nombres de teclas.

El mensaje despierta a Codex, pero no sustituye el reporte ni las pruebas.

OpenCode sólo puede considerar entregada la tarea después de que ambas llamadas
`send-keys` hayan finalizado. El texto sin `Enter` no despierta a Codex.

Si existe un bloqueo que impide completar el trabajo:

```text
AGENT_BLOCKED task=issue-60-g-view run=issue-60-g-view-20260812-01 attempt=1 reason=permission-required
```

Se entrega con el mismo patrón literal + `Enter`. Codex despierta, inspecciona
el estado y decide si puede resolverlo o si debe informarlo al humano.

## 13. Auditoría de Codex al despertar

Codex no debe aceptar el mensaje como prueba de corrección. Debe inspeccionar:

```bash
git status --short
git diff --stat
git diff --check
git diff
```

Después ejecuta:

1. tests focales de los archivos cambiados;
2. suite completa exigida por `AGENTS.md`;
3. linters, type checks y gates de tamaño;
4. CI local equivalente al remoto cuando exista;
5. verificación de schemas, documentación y versión si aplica;
6. revisión de secretos y cambios accidentales;
7. correspondencia entre DoD, diff y reporte adversarial.

El resultado debe clasificarse:

- `OK`: contrato completo y evidencia suficiente;
- `PARCIAL`: trabajo útil, pero falta un gate no bloqueante o una operación
  externa;
- `BLOQ`: baseline rota, hallazgo crítico o decisión humana necesaria.

## 14. Correcciones y nuevos intentos

Si Codex encuentra fallas:

1. formula una instrucción pequeña y concreta;
2. incrementa `attempt_id`;
3. crea una tarjeta inmutable para el nuevo intento con el mensaje de cierre
   exacto (`run`, `attempt` y `report`);
4. relanza OpenCode desde el shell de su pane usando `opencode run --continue`
   o, si no hay sesión reanudable, abre una ejecución nueva que lea la tarjeta
   original y la tarjeta de corrección;
5. confirma una sola vez que OpenCode arrancó;
6. termina su turno y vuelve a `WAITING_EXTERNAL`.

Ejemplo:

```markdown
# Corrección — issue-60-g-view — intento 2

- Tarjeta original: </ruta/tarjeta-intento-1.md>
- Run: issue-60-g-view-20260812-01
- Intento: 2
- Hallazgo: el cursor no está ligado al SHA de revisión.
- Corrección: añadir el binding y un test de cursor cruzado; repetir los gates.
- No ampliar el scope.
- Reporte: docs/planning/issue-60-report-attempt-2.md
- Cierre exacto: AGENT_DONE task=issue-60-g-view run=issue-60-g-view-20260812-01 attempt=2 report=docs/planning/issue-60-report-attempt-2.md
```

`opencode run` es one-shot: después de `AGENT_DONE` normalmente termina y deja
el shell en el pane. Por eso **no** se envía texto `CORRECTION ...` directamente
al pane; el shell intentaría ejecutarlo como comando. Se inicia otro
`opencode run`, con `--continue` cuando esté disponible. Para una auditoría
independiente se utiliza contexto fresco, no `--continue`.

Ejemplo de relanzamiento desde el pane de OpenCode:

```bash
tmux send-keys -l -t %<executor-pane-id> -- \
  "opencode run --continue --auto --model <proveedor/modelo> 'Lee completamente /ruta/correccion-intento-2.md y ejecútala'"

tmux send-keys -t %<executor-pane-id> Enter
```

La tarjeta del intento 2 contiene la entrega exacta `AGENT_DONE ... attempt=2`;
no depende de que el modelo recuerde sustituir el número anterior.

## 15. Git y CI

Una configuración práctica de autonomía es:

| Operación | OpenCode | Codex | Humano |
|---|---:|---:|---:|
| editar worktree | sí | sí | sí |
| tests/lint/CI local | sí | sí | sí |
| crear rama/worktree | no habitual | sí | sí |
| commit | opcional | sí | sí |
| push de rama | no habitual | sí | sí |
| abrir/actualizar PR | no | según autorización | sí |
| merge a main | no | no por defecto | sí |
| tag/release | no | prepara evidencia | autoriza/ejecuta |

Antes de commit:

```bash
git diff --check
git status --short
<tests focales>
<suite completa>
<CI local>
```

El commit debe ser pequeño, convencional y corresponder a una sola fase. El
release nunca se deduce de una suite verde: se presenta al humano con SHA,
gates, limitaciones y reporte adversarial.

## 16. Recuperación de sesiones

### Codex sigue vivo

```bash
tmux attach-session -t <controller_session>
```

### OpenCode sigue vivo

```bash
tmux attach-session -t <executor_session>
```

### Codex terminó inesperadamente

Abrir una sesión nueva en el mismo worktree y reanudar la sesión persistida:

```bash
codex resume --last -C <worktree>
```

Cuando haya varias sesiones, registrar el ID exacto de Codex en el reporte del
controlador y reanudar por ID en lugar de `--last`.

### OpenCode terminó sin notificar

El humano puede avisar a Codex o escribir manualmente `AGENT_DONE`. Codex debe
auditar el worktree de la misma forma; la ausencia de notificación no invalida
automáticamente los cambios.

En modo directo esto no es una anomalía: la notificación humana es el mecanismo
de entrega esperado. La tarjeta usa una marca final inequívoca como
`FIN <TASK>-IMPLEMENTATION` y ordena conservar la sesión conversacional.

## 17. Fallas comunes

### El mensaje aparece en Codex pero no se procesa

Causa: se envió texto literal sin una segunda llamada `Enter`.

Solución: enviar `tmux send-keys -t <sesión> Enter` por separado.

### La ventana parece congelada

Posibles causas:

- el agente espera un permiso;
- está ejecutando una prueba larga;
- el proceso terminó y quedó un shell;
- el mensaje se envió al nombre de sesión equivocado;
- Codex todavía estaba generando y la entrada quedó en cola.

Inspeccionar una sola vez:

```bash
tmux list-panes -t <sesión> -F '#{pane_dead}|#{pane_current_command}|#{pane_current_path}'
tmux capture-pane -t <sesión> -p -S -80
```

Después decidir; no convertir esta inspección en polling continuo.

### OpenCode pide permisos repetidamente

Configurar permisos amplios para lectura, edición, bash y subagentes dentro del
worktree, o usar `--auto` con las prohibiciones importantes ya definidas.

### El agente modificó archivos fuera del alcance

Codex separa cambios relacionados de cambios accidentales. No borra trabajo a
ciegas; informa el conflicto o pide al ejecutor que lo corrija.

### El primer prompt nunca apareció en OpenCode

Causa: se inició `opencode` interactivamente y se enviaron teclas antes de que
la TUI estuviera lista.

Solución: comprobar una sola vez que el prompt visible ya existe, enviar texto
literal y `Enter` por separado y confirmar una vez que la instrucción aparece.
No usar un `sleep` fijo como prueba de readiness: la latencia de inicio varía.

### La ventana muestra progreso, pero no permite conversar

**Síntoma:** las flechas o teclas aparecen literalmente como `^[[A`, `^[[B` o
otras secuencias de escape; no existe `Ask anything` aunque el pane reporte
`pane_current_command=opencode`.

**Causa:** el proceso fue lanzado con `opencode run`. Es un one-shot: recibe el
prompt en la línea de comandos y no mantiene una TUI conversacional. El
emulador de terminal no es la causa.

**Solución:** dejar terminar el intento o interrumpirlo de forma controlada si
está estancado; después lanzar una TUI nueva con `opencode --auto --model ...`,
sin `run`. Para revisión realmente fresca, omitir también `--continue`. Esperar
el prompt `Ask anything` antes de enviar la tarjeta.

### iTerm2 abrió, pero no muestra la sesión OpenCode

Comprobar `tmux list-clients` y volver a adjuntar una ventana de iTerm2 a la
sesión existente. No reiniciar OpenCode sólo para recuperar visibilidad. Una
comprobación válida muestra el cliente en `<executor-session>` y el pane vivo
con `pane_current_command=opencode`.

### La suite pasa, pero el requerimiento no está completo

Los tests son una dimensión. Codex también compara el diff contra cada criterio
del DoD y revisa compatibilidad, documentación y comportamiento observable.

## 18. Niveles recomendados de rigor

### Trabajo cotidiano

- OpenCode con autonomía amplia;
- adversarial coordinado por OpenCode;
- Codex audita diff y tests;
- commit y push de rama permitidos;
- humano interviene al final.

Cuando el humano desea observación continua y correcciones conversacionales,
puede usarse el modo directo con OpenCode interactivo y marca final visible.

### Cambio crítico

- worktree dedicado;
- fases pequeñas;
- adversarial en sesión y modelo frescos;
- CI local completa;
- Codex revisa cada invariante con evidencia;
- humano autoriza integración y release.

### Release

- SHA exacto;
- árbol limpio;
- suite completa y paquete instalable;
- ronda adversarial `proceed`;
- limitaciones externas declaradas;
- autorización humana explícita antes de tag/publicación.

## 19. Prompt base para Codex controlador

```text
Eres el controlador técnico de esta tarea. Lee AGENTS.md y la tarjeta completa.
Tienes autonomía para administrar el worktree y la rama, lanzar OpenCode en una
sesión tmux visible, ejecutar CI local, corregir problemas menores y crear
commits/push de la rama si la tarjeta lo permite.

OpenCode será el ejecutor. Dale una tarea verificable, permite que implemente,
pruebe y realice una ronda adversarial en contexto fresco. Después de lanzarlo,
termina tu turno y queda en WAITING_EXTERNAL: no hagas polling ni sleep.

OpenCode te despertará enviando AGENT_DONE a esta sesión tmux. Al recibirlo,
audita críticamente Git, diff, tests, gates y reporte adversarial. Si hay fallas,
envía una corrección pequeña y vuelve a esperar. Si todo está correcto, prepara
el commit y la evidencia final. No hagas merge, tag ni release sin autorización
actual del orquestador humano.
```

## 20. Prompt base para OpenCode ejecutor

```text
Lee completamente la tarjeta indicada y las instrucciones del repositorio.
Implementa el alcance con autonomía dentro del worktree. Ejecuta los checks del
DoD y corrige sus fallas.

Antes de terminar, realiza una ronda adversarial con contexto fresco enfocada en
corrección, requisitos, compatibilidad y casos edge. Corrige BLOCKER/HIGH y los
MED aplicables, repite las verificaciones y deja un reporte con evidencia real.

Cuando todos los archivos estén escritos y los comandos hayan terminado, envía
exactamente el mensaje AGENT_DONE indicado en la tarjeta a la sesión tmux de
Codex usando send-keys literal y Enter en llamadas separadas. Después termina.
No hagas merge, tag ni release.
```

## 21. Checklist de adopción en otro proyecto

- [ ] existe `AGENTS.md` o instrucciones equivalentes;
- [ ] se conoce el comando de tests y CI local;
- [ ] el repositorio está limpio o la suciedad existente está inventariada;
- [ ] la tarea tiene objetivo único y DoD ejecutable;
- [ ] existe worktree y rama aislados;
- [ ] los nombres tmux son únicos y conocidos por ambos agentes;
- [ ] Codex está en modo interactivo y visible;
- [ ] OpenCode está en otra ventana o pestaña visible;
- [ ] OpenCode tiene permisos suficientes dentro del worktree;
- [ ] la tarjeta declara quién puede hacer commit/push;
- [ ] el mensaje `AGENT_DONE` está definido;
- [ ] OpenCode tiene orden explícita de despertar a Codex por tmux antes de salir;
- [ ] existe ronda adversarial fresca;
- [ ] Codex audita independientemente;
- [ ] release permanece bajo autorización humana.

Checks añadidos en v2.0:

- [ ] topología elegida explícitamente (T1/T2/T3, §4.3) y su wake-up es
  realizable con los bindings disponibles;
- [ ] el contrato del repo destino (`AGENTS.md`) fue leído y sus reglas duras
  están en la tarjeta (§6.1);
- [ ] la autoridad de commit está declarada por escrito (ejecutor/controlador/
  humano) y coincide con la política del repo destino;
- [ ] los permisos amplios del ejecutor están configurados ANTES del arranque
  (config del proyecto o flags), no se confía en aprobar sobre la marcha;
- [ ] preflight de versiones/flags ejecutado en ESTE host hoy (F4);
- [ ] los agentes NO reciben secretos: claves fuera del worktree y de las
  tarjetas.

Para modo directo, sustituir los checks específicos de Codex/OpenCode visibles
y de `AGENT_DONE` por:

- [ ] Codex Desktop es el único controlador y no existe otro controlador
  editando el worktree;
- [ ] OpenCode interactivo está listo antes de enviar el primer prompt;
- [ ] la tarjeta define una marca `FIN ...` y el humano notificará su aparición.

## 22. Regla final

La autonomía debe ser amplia dentro de la tarea y estrecha fuera de ella.

No se busca interrumpir al desarrollador con aprobaciones rutinarias. Se busca
que los agentes puedan producir software de forma continua, verificable y
visible, mientras el humano conserva las decisiones que cambian el alcance o
publican resultados al exterior.
