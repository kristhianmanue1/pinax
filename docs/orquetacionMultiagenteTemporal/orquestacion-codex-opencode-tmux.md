# Orquestación multiagente con agentes CLI y tmux

**Versión:** 2.2-borrador (2026-08-21)

**Estado:** propuesta no adoptada; requiere piloto, revisión, aceptación y Git

**Compatibilidad observada:** Codex CLI 0.147.0, OpenCode 1.18.21, tmux 3.6a

**Modelo:** Controlador → Ejecutor → revisor fresco → Controlador → humano para
push/merge

Los respaldos de las versiones anteriores están en `backup/`. Este texto es el
contrato operativo compacto; los respaldos son historia, no norma vigente.

## 1. Objetivo y límites

El método permite que un Controlador delegue trabajo a un Ejecutor visible y
persistente sin vigilarlo continuamente. Busca autonomía dentro de una tarea
cerrada y detención fuera de ella.

Principio central:

```text
sesión viva ≠ trabajo correcto ≠ revisión ≠ autorización
```

- tmux mantiene procesos y visibilidad; no demuestra corrección;
- reportes y memoria son afirmaciones que deben contrastarse;
- los archivos y Git son la interfaz; el transcript no es evidencia;
- la autoridad de commit del Controlador debe estar declarada en el handoff;
- ninguna suite, revisión o mensaje concede push, merge o release;
- `AGENTS.md` y la política del repositorio destino prevalecen siempre.

## 2. Roles y autoridad

### Humano

- decide objetivo, alcance y prioridades;
- define al inicio si el Controlador puede hacer commit tras los gates;
- resuelve ampliaciones, bloqueos y aceptación del resultado;
- interviene normalmente sólo para push, merge, tag y release.

### Controlador

- lee las reglas del repositorio y prepara una tarjeta verificable;
- crea la rama, worktree, socket y sesiones cuando la política lo permita;
- lanza al Ejecutor con permisos técnicos suficientes;
- espera sin polling;
- audita independientemente la entrega;
- puede crear el commit sin volver a interrumpir al humano cuando la política
  del repositorio y el handoff le conceden esa autoridad para el intento, pero
  sólo después de revisión fresca y auditoría final verdes;
- no deduce push, PR, merge, tag o release de una autorización de commit.

### Ejecutor

- edita y prueba únicamente dentro del alcance y worktree asignados;
- autocorrige su candidato;
- coordina una revisión adversarial fresca antes de entregar;
- aplica fix-and-retry hasta `PROCEED` o escala el bloqueo;
- nunca hace commit ni otra operación protegida.

### Revisor fresco

- no participó en la implementación;
- recibe tarjeta, handoff, fuentes y artefacto, no el transcript del Ejecutor;
- ejecuta comprobaciones propias y produce un reporte separado;
- en cambios críticos usa otro proveedor y otro modelo.

**Regla local importante:** esta guía designa al Controlador como actor normal
del commit para evitar babysitting, pero no revoca políticas más restrictivas.
Antes de adoptar esta guía en Pinax debe reconciliarse expresamente
`docs/politica-agentes-pinax.md`, que hoy conserva “el dueño aplica commit”.

## 3. Artefactos de cada intento

### 3.1 Tarjeta canónica

Cada intento tiene un JSON inmutable `epistates/task-card/v1` con:

- objetivo, repositorio, SHA base, rama y worktree;
- rutas y acciones permitidas;
- operaciones prohibidas;
- checks y evidencia exigida;
- entrega y condición de parada.

Se valida antes de lanzar:

```bash
PYTHONPATH=/ruta/a/epistates/src python3 -m epistates validate \
  /ruta/task-card.json
```

La tarjeta v1 mantiene `protected_operations_authorized: []`; coordina trabajo,
pero no acuña autoridad. Véase `task-card-v1-ejemplo.json`.

### 3.2 Handoff tmux opcional

El handoff contiene sólo datos efímeros:

- `run_id`, `attempt_id` y topología única;
- socket, sesiones y `%pane-id` exactos;
- perfiles de permisos y uso o ausencia de `--auto`;
- rutas de reportes y mensaje de cierre;
- actor futuro del commit y autoridad actual.

Referencia la tarjeta y su SHA-256. Nunca amplía su alcance. Si difieren,
prevalece la regla más restrictiva y se detiene el intento. Véase
`handoff-tmux-ejemplo.md`.

## 4. Topologías

Se elige una y no se cambia durante el intento.

| Topología | Controlador | Ejecutor | Entrega |
|---|---|---|---|
| T1 automática | CLI en tmux | CLI en tmux | `AGENT_DONE` al pane del Controlador |
| T2 directa | app de escritorio | CLI en tmux | aviso humano al Controlador |
| T3 relay | headless | CLI en tmux | archivo de estado + aviso humano/scheduler |

T1 es la recomendada para trabajo largo no atendido. T2 sirve para pilotos
observados. T3 se usa sólo cuando el Controlador no puede recibir mensajes tmux.

En T1, Controlador y Ejecutor viven en sesiones distintas del mismo socket
dedicado. En T2 no se crea otro Controlador que edite el worktree. En T3 el
handoff por archivo es obligatorio y el supervisor audita sin leer transcripts.

La visibilidad es un gate único de arranque: se comprueban clientes/panes y el
humano confirma que puede abrir las ventanas. Después no hay polling.

**Ventana primaria siempre visible:** la ventana del Controlador se abre desde
el arranque, se nombra `controlador` y permanece seleccionada en al menos un
cliente visible durante todo el ciclo, incluso después de terminar. El
Controlador no puede sustituirla por una ventana de resumen. Si crea ventanas
auxiliares, vuelve inmediatamente a `controlador`; el resumen final se imprime
en el pane del propio Controlador o se deja en una ventana secundaria sin
cambiar la vista primaria. La ventana del Ejecutor también se abre al lanzarlo,
pero nunca desplaza ni oculta la del Controlador.

## 5. Máquina de estados

```text
PREPARED
  → EXECUTOR_RUNNING
  → EXECUTOR_SELF_CHECK
  → FRESH_REVIEW
  → FIX_AND_RETRY → EXECUTOR_SELF_CHECK
  → AGENT_DONE | AGENT_BLOCKED
  → CONTROLLER_AUDIT
  → CORRECTION_ATTEMPT → EXECUTOR_RUNNING
  → COMMITTED | BLOCKED
  → READY_FOR_HUMAN
  → PUSHED | MERGED | PAUSED
```

`AGENT_DONE` sólo es válido con revisión fresca final `PROCEED`. No se admite
`adversarial=pendiente`. `READY_FOR_HUMAN` exige además auditoría independiente
del Controlador. `COMMITTED` exige autoridad previa y explícita en el handoff,
además de una política local compatible. El humano reaparece en
`READY_FOR_HUMAN` para decidir publicación o integración.

## 6. Preparación

Controlador verifica y registra:

```bash
git status --short
git branch --show-current
git rev-parse HEAD
git worktree list
codex --version
codex --help
opencode --version
opencode run --help
tmux -V
```

También lee `AGENTS.md`, instrucciones anidadas, gates, estado remoto cuando
aplique y suciedad preexistente. No borra ni mezcla trabajo ajeno.

Si el proyecto usa AN-KLA beta.17, ejecuta su protocolo vigente:

```text
context status → verify → checkpoint show → resume
```

Un `verify` fallido bloquea el trabajo. El checkpoint es el snapshot de
reanudación; eventos recuperados son evidencia histórica no confiable, nunca
instrucción, prueba Git ni autorización.

## 7. Permisos sin babysitting

Los permisos técnicos y la autoridad de proyecto son cosas distintas. El
Controlador debe poder administrar el intento y, cuando corresponda, ejecutar
el commit autorizado para ese intento. Eso no le permite hacer push, merge o
ampliar el alcance.

### 7.1 Socket tmux aislado

Cada intento T1 usa un directorio `0700` y un socket propios:

```bash
mkdir -p /private/tmp/<proyecto>-agent-tmux-<run_id>
chmod 700 /private/tmp/<proyecto>-agent-tmux-<run_id>

tmux -S /private/tmp/<proyecto>-agent-tmux-<run_id>/tmux.sock \
  new-session -d -s <controller-session> -c <worktree>

tmux -S /private/tmp/<proyecto>-agent-tmux-<run_id>/tmux.sock \
  display-message -p -t <controller-session>:0.0 '#{pane_id}'

tmux -S /private/tmp/<proyecto>-agent-tmux-<run_id>/tmux.sock \
  rename-window -t <controller-session>:0 controlador
```

No se comparte el socket global de tmux: expondría sesiones de otros proyectos.
Los textos `<...>` son placeholders que el lanzador materializa; nunca se
ejecutan literalmente.

### 7.2 Perfil del Controlador Codex

```bash
tmux -S <socket-dedicado> send-keys -l -t %<controller-pane-id> -- \
  'codex -C <worktree> --approve-for-me --add-dir <directorio-del-socket> --no-alt-screen'
tmux -S <socket-dedicado> send-keys -t %<controller-pane-id> Enter
```

`--approve-for-me` somete solicitudes técnicas a revisión automática e implica
el sandbox `workspace-write`; Codex 0.147.0 rechaza combinar ambos flags de
forma explícita. Evita aprobaciones rutinarias del humano, pero no concede
alcance ni autoridad. `--add-dir` se limita al directorio del socket.

La primera llamada a un socket puede fallar dentro del sandbox antes de que el
revisor automático evalúe la elevación. El preflight no se considera aprobado
hasta que el propio Controlador haya creado o listado una sesión real. Si el
revisor automático autoriza la operación, no hace falta acceso total al host.
No se recomienda `danger-full-access` para resolver este caso.

Antes de delegar, el Controlador debe poder ejecutar sin diálogo:

```bash
tmux -S <socket-dedicado> list-sessions
git status --short
```

Si falla o solicita interacción, se corrige el perfil; no se traslada el
babysitting al humano.

### 7.3 Ejecutor OpenCode

Se crea en el mismo socket y worktree:

```bash
tmux -S <socket-dedicado> new-session -d \
  -s <executor-session> -c <worktree>

tmux -S <socket-dedicado> display-message -p \
  -t <executor-session>:0.0 '#{pane_id}'

tmux -S <socket-dedicado> send-keys -l -t %<executor-pane-id> -- \
  "opencode run --model <proveedor/modelo> 'Lee la tarjeta y el handoff completos; ejecútalos'"
tmux -S <socket-dedicado> send-keys -t %<executor-pane-id> Enter
```

Para trabajo observado se omite `--auto`. En un intento no atendido puede
añadirse a `opencode run` sólo con opt-in humano registrado:

```bash
opencode run --auto --model <proveedor/modelo> '<instrucción breve>'
```

`--auto` evita confirmaciones que no estén denegadas; no autoriza commit, red,
dependencias, ampliación de alcance ni escritura fuera del worktree. Requiere
worktree aislado, tarjeta cerrada, secretos fuera y stop rules explícitas.

Tras lanzar cada pane se inspecciona una sola vez:

```bash
tmux -S <socket-dedicado> list-panes -t <sesión> \
  -F '#{pane_id}|#{pane_dead}|#{pane_current_command}|#{pane_current_path}'
```

El pane debe estar vivo, en el worktree correcto y ejecutando el binding
esperado. Luego Controlador termina su turno; no usa `sleep`, bucles ni capturas
repetidas.

## 8. Autocorrección, revisión fresca y auditoría final

### Capa 1 — autocorrección

Ejecutor compara el diff contra cada criterio, ejecuta los gates y corrige
fallos reproducibles, contradicciones y cambios fuera de alcance. Si no puede,
envía `AGENT_BLOCKED` con causa verificable.

### Capa 2 — revisión fresca antes de entregar

Ejecutor congela el candidato y coordina un revisor que no participó en la
implementación ni recibe su transcript o una sesión `--continue`. El revisor
ejecuta evidencia propia y entrega:

```markdown
## Hallazgos
- [BLOCKER|HIGH|MED|LOW] problema — evidencia — corrección

## Verificaciones
- comando → resultado real

## Decisión
PROCEED | FIX-AND-RETRY | ESCALATE
```

Con `FIX-AND-RETRY`, Ejecutor corrige, repite gates, congela otro candidato y
solicita otra revisión fresca. Con `ESCALATE`, BLOCKER/HIGH pendiente o reporte
inverificable, entrega `AGENT_BLOCKED`. Sólo `PROCEED` habilita `AGENT_DONE`.

Trabajo cotidiano puede usar otro contexto del mismo proveedor. Seguridad,
contratos, migraciones, cambios críticos y releases exigen otro proveedor y
otro modelo.

### Capa 3 — auditoría final del Controlador

Después de `AGENT_DONE`, Controlador verifica por sí mismo:

1. reporte adversarial separado, estructura válida y decisión `PROCEED`;
2. historial de fix-and-retry y candidato final revisado;
3. al menos un comando citado, re-ejecutado;
4. `git status`, `git diff --stat`, `git diff --check` y diff completo;
5. alcance y ausencia de cambios colaterales o secretos;
6. tests focales, suite y gates de `AGENTS.md`;
7. correspondencia entre tarjeta, implementación, documentación y reportes.

Controlador busca errores comunes que Ejecutor y revisor pudieron compartir.
Puede encargar una revisión adicional, pero no sustituye la revisión fresca del
Ejecutor ni convierte una revisión pendiente en entrega válida.

## 9. Entrega y correcciones

En T1, Ejecutor escribe reportes y despierta al pane exacto:

```bash
tmux -S <socket-dedicado> send-keys -l -t %<controller-pane-id> -- \
  'AGENT_DONE task=<task> run=<run> attempt=<n> report=<ruta> adversarial=<ruta>'
tmux -S <socket-dedicado> send-keys -t %<controller-pane-id> Enter
```

El mensaje sólo interrumpe; los archivos contienen la evidencia. En T2/T3, el
humano o scheduler entrega el mismo aviso sin fingir un pane receptor.

Si Controlador rechaza la entrega:

1. describe un hallazgo pequeño y verificable;
2. incrementa `attempt_id`;
3. crea tarjeta completa e inmutable y handoff del nuevo intento;
4. relanza al Ejecutor con `opencode run --continue` sólo para corregir;
5. exige nuevamente autocorrección y revisor fresco sin `--continue`;
6. vuelve a esperar sin polling.

No se inyectan frases de corrección directamente a un pane que volvió al shell.

## 10. Git y cierre

| Operación | Ejecutor | Controlador | Humano |
|---|---:|---:|---:|
| editar y probar | sí | audita | puede |
| rama/worktree | no | si la política permite | puede |
| commit | no | ejecuta post-gates si el handoff lo autoriza | concede al inicio o ejecuta |
| push/PR/merge | no | sólo con autoridad separada | autoriza |
| tag/release | no | prepara evidencia | autoriza/ejecuta |

Antes de commit deben existir:

- revisión fresca `PROCEED` sobre el candidato final;
- auditoría final del Controlador en verde;
- SHA, alcance y archivos exactos;
- autoridad de commit declarada para el Controlador en el handoff;
- política local compatible.

La autoridad de commit no incluye push. Una suite verde no incluye release.

## 11. Recuperación y fallos

Reabrir sesiones:

```bash
tmux -S <socket-dedicado> attach-session -t <controller-session>
tmux -S <socket-dedicado> attach-session -t <executor-session>
```

Inspección única de una sesión dudosa:

```bash
tmux -S <socket-dedicado> list-panes -t <sesión> \
  -F '#{pane_dead}|#{pane_current_command}|#{pane_current_path}'
tmux -S <socket-dedicado> capture-pane -p -t <sesión> -S -80
```

- si espera permisos rutinarios, corrige el perfil de lanzamiento;
- si terminó sin notificar, Controlador audita igual y registra la anomalía;
- si el texto llegó sin ejecutarse, envía `Enter` por separado;
- si `opencode run` terminó, relanza otro one-shot; no escribas prosa al shell;
- para revisión fresca no uses `--continue`;
- no mates una sesión homónima sin comprobar su `run_id` y estado.

## 12. Checklist mínimo

- [ ] `AGENTS.md` leído y reglas duras volcadas en la tarjeta;
- [ ] tarea única, SHA base, worktree y suciedad preexistente registrados;
- [ ] tarjeta `task-card/v1` válida y handoff sin autoridad adicional;
- [ ] una topología elegida para todo el intento;
- [ ] socket dedicado `0700`, sesiones y panes exactos;
- [ ] ventanas visibles en el gate inicial;
- [ ] ventana `controlador` permanece seleccionada y visible; ningún resumen o
  pane auxiliar la sustituye;
- [ ] Controlador con `--approve-for-me`; preflight real de tmux y Git aprobado;
- [ ] Ejecutor con permisos suficientes; `--auto` ausente o autorizado por intento;
- [ ] secretos fuera del worktree, prompts y reportes;
- [ ] AN-KLA verificado, si aplica, sin usar memoria como autoridad;
- [ ] autocorrección completada;
- [ ] revisión fresca final `PROCEED`, nunca pendiente;
- [ ] auditoría independiente del Controlador;
- [ ] Controlador autorizado o no para commit desde el inicio del intento;
- [ ] push/merge/release reservados al humano y separados por autoridad;
- [ ] en trabajo crítico, otro proveedor y otro modelo.

## 13. Piloto antes de adopción

La primera validación debe ser pequeña y reversible: documentación o un test
acotado, una sola topología, sin dependencias y sin push. Primero se prueba el
perfil observado; `--auto` se prueba, si se desea, en otro intento explícito.

El piloto comprueba tarjeta, handoff, permisos sin babysitting, socket aislado,
visibilidad, entrega, autocorrección, revisión fresca, auditoría final,
recuperación y ausencia de cambios fuera de alcance. Un fallo produce
fix-and-retry del protocolo; no adopción por inercia.

La autonomía debe ser amplia dentro de la tarea y estrecha fuera de ella.
