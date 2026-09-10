# Ronda adversarial — orquestación Codex/OpenCode/tmux

> **Tipo de documento:** registro histórico (evidencia de la revisión). No
> editar. Sus lecciones (F1–F10) están absorbidas en la guía
> `orquestacion-codex-opencode-tmux.md` v2.0, que es el documento canónico.

**Fecha:** 2026-08-12  
**Alcance:** corrección operativa, no burocracia de seguridad  
**Documento revisado:** `orquestacion-codex-opencode-tmux.md`  
**Revisor:** contexto fresco e independiente  
**Decisión inicial:** `fix-and-retry`  
**Decisión después de correcciones:** `proceed`  
**Validación operativa adicional:** arranque del modo directo probado al iniciar H4 Slice3 de Epistates

## Resultado ejecutivo

La arquitectura es viable, pero la primera versión tenía un fallo que rompía el
ciclo de correcciones: `opencode run` es one-shot y, después de terminar, el pane
normalmente vuelve al shell. Enviar allí una frase `CORRECTION ...` intentaría
ejecutarla como comando en vez de reanudar al agente.

Se corrigió el flujo para crear una tarjeta inmutable por intento y relanzar
OpenCode mediante `opencode run --continue`, con fallback a una ejecución nueva.
También se fijó el pane exacto para las notificaciones, se eliminó un evento no
definido y se añadió un preflight único de versiones y proceso.

## Hallazgos y resolución

### F1 — BLOCKER — corrección enviada a un OpenCode ya terminado

**Problema:** la guía lanzaba `opencode run`, ordenaba terminar después de
`AGENT_DONE` y luego intentaba enviar una corrección textual a la misma sesión.

**Impacto:** el shell podía interpretar `CORRECTION` como un comando; Codex
volvería a esperar un agente que nunca se reanudó.

**Corrección aplicada:** cada reintento crea una tarjeta nueva y relanza
`opencode run --continue`; si no existe sesión reanudable, abre una ejecución
nueva que lee la tarjeta original y la corrección. La guía advierte
explícitamente que no debe enviarse `CORRECTION ...` directamente al shell.

**Estado:** cerrado.

### F2 — HIGH — `attempt_id` podía quedar obsoleto

**Problema:** incrementar el intento en la conversación no actualizaba la
tarjeta ni el mensaje `AGENT_DONE` que OpenCode debía enviar exactamente.

**Impacto:** una segunda entrega podía volver como `attempt=1` y confundirse con
el resultado anterior.

**Corrección aplicada:** tarjeta inmutable por intento con `run`, `attempt`,
ruta de reporte y mensaje final completos. Se añadió un ejemplo de intento 2.

**Estado:** cerrado.

### F3 — HIGH — modalidad crítica usaba un evento inexistente

**Problema:** la modalidad B introducía `IMPLEMENTATION_READY`, ausente de la
máquina de estados, tarjeta y prompt del ejecutor.

**Impacto:** el flujo de revisión para cambios críticos no era ejecutable.

**Corrección aplicada:** la modalidad B reutiliza `AGENT_DONE`; Codex audita y
después lanza un reviewer nuevo. No existe un segundo protocolo especial.

**Estado:** cerrado.

### F4 — HIGH — flags o CLI inválidos podían aparentar un lanzamiento exitoso

**Problema:** no se verificaban versiones ni opciones antes de enviar los
comandos de arranque.

**Impacto:** el CLI podía terminar por un flag inválido y dejar sólo un shell
visible, mientras Codex declaraba `WAITING_EXTERNAL`.

**Corrección aplicada:** preflight de `codex`, `opencode` y `tmux`, seguido de
una inspección única de `pane_dead`, `pane_current_command` y directorio. No es
polling.

**Estado:** cerrado.

### F5 — MED — mensajes dirigidos sólo al nombre de sesión

**Problema:** `tmux send-keys -t <session>` puede resolver al pane activo. Si el
humano añade o cambia panes, el evento puede llegar al destino equivocado.

**Impacto:** `AGENT_DONE` podría escribirse en un shell que no contiene Codex.

**Corrección aplicada:** se obtiene y registra `%pane_id` para Codex y OpenCode;
la entrega literal y `Enter` se dirigen al pane exacto.

**Estado:** cerrado.

### F6 — MED — colisión con nombres de sesiones existentes

**Problema:** los ejemplos creaban sesiones sin indicar qué hacer si el nombre
ya estaba ocupado.

**Impacto:** lanzamiento fallido o tentación de cerrar una sesión con trabajo.

**Corrección aplicada:** preflight `tmux list-sessions`; ante colisión se adjunta
la ejecución correspondiente o se elige un nombre nuevo, sin reemplazo
automático.

**Estado:** cerrado.

## Evidencia ejecutada

- `codex --version` → `codex-cli 0.147.0`.
- `opencode --version` → `1.18.16`.
- `tmux -V` → `tmux 3.6a`.
- `opencode run --help` → confirma `--auto`, `--model`, `--continue` y
  `--session`.
- `codex resume --help` → confirma reanudación por ID/nombre y `--last`.
- Validación Markdown → 744 líneas y 60 delimitadores de code fence, número par.
- Búsqueda de drift → no permanece `IMPLEMENTATION_READY` ni el patrón de enviar
  corrección textual a una sesión OpenCode supuestamente activa.
- Prueba tmux con dos panes `%170` y `%171`:
  `send-keys -l -t %170` + `send-keys -t %170 Enter` imprimió
  `AGENT_DONE task=test run=2 attempt=2` sólo en `%170`; `%171` quedó intacto.
- La sesión efímera `doc-guide-rerun-019ff04a` fue inventariada y retirada al
  terminar la prueba.

## Riesgos residuales aceptados

- `--continue` reanuda según la semántica de OpenCode instalada; cuando no sea
  inequívoca se usa una ejecución nueva con ambas tarjetas.
- La apertura visual depende del emulador de terminal del host; la guía incluye
  ejemplos para Terminal.app y GNOME Terminal.
- El humano aún puede cerrar una ventana o sesión manualmente; la recuperación
  por tmux/Codex sigue documentada.

Estos riesgos no bloquean el piloto y no justifican añadir gateway, firmas,
watchers ni aprobaciones por cada comando.

## Validación posterior: modo directo y readiness de OpenCode

Después de la ronda original se probó el arranque de una segunda topología:

```text
Codex Desktop controlador → OpenCode interactivo en tmux visible
```

La ejecución confirmó que el modo directo es útil cuando el humano observa el
trabajo y desea conservar una sesión conversacional. También reveló un fallo de
lanzamiento que la guía original no describía.

### F7 — HIGH — primer prompt enviado antes de que la TUI estuviera lista

**Problema:** `tmux new-session ... opencode` inicia el proceso antes de que la
interfaz muestre `Ask anything`. En dos lanzamientos reales, enviar la tarea
demasiado pronto no la insertó en la TUI aunque `pane_current_command` ya era
`opencode`.

**Impacto:** el controlador podía creer que el agente trabajaba mientras éste
permanecía ocioso en el prompt inicial.

**Corrección aplicada:** la guía separa `opencode run` one-shot del modo
interactivo. Para el segundo exige abrir la ventana, comprobar una sola vez el
prompt visible, enviar texto literal y `Enter` por separado y confirmar una vez
que la instrucción apareció. Un `sleep` fijo no cuenta como readiness.

**Estado:** cerrado.

### F8 — MED — la topología Desktop no podía cumplir `AGENT_DONE`

**Problema:** Codex Desktop no vive en un pane tmux direccionable. Exigir a
OpenCode que lo despertara mediante `send-keys` era imposible y mezclaba dos
topologías distintas.

**Impacto:** una tarjeta podía exigir una entrega técnicamente irrealizable o
motivar el lanzamiento innecesario de un segundo controlador Codex.

**Corrección aplicada:** el documento distingue explícitamente:

- modo automático Codex CLI→OpenCode, con `AGENT_DONE` al pane exacto;
- modo directo Codex Desktop→OpenCode interactivo, con marca `FIN ...` visible
  y notificación humana.

Se prohíbe que ambos controladores editen simultáneamente el mismo worktree.

**Estado:** cerrado.

### Evidencia de la validación adicional

- sesión `epistates-h4-slice3` creada sobre el worktree y rama esperados;
- ventana Terminal visible adjunta a la sesión;
- primera inyección temprana no apareció en la TUI;
- segunda inyección, después de observar `Ask anything`, apareció literalmente
  y OpenCode comenzó a procesarla;
- Codex Desktop conservó el rol de controlador único;
- OpenCode recibió prohibición de commit/push/PR/merge/tag/release.

### Decisión de la validación adicional

`proceed`

Ambas topologías son viables si se selecciona una por tarea y se respetan sus
mecanismos de entrega diferentes.

## Validación operativa adicional: issue #60 G-VIEW en iTerm2

Durante el spike documental de G-VIEW se comprobó una diferencia que la guía
aún no hacía suficientemente visible: adjuntar iTerm2 a un proceso
`opencode run --continue` mejora la presentación, pero no lo convierte en una
sesión conversacional.

### F9 — HIGH — apariencia de TUI atribuida incorrectamente al emulador

**Problema:** un one-shot mostraba progreso dentro de iTerm2, pero las teclas de
navegación aparecían literalmente como `^[[A`/`^[[B`. El operador podía concluir
que iTerm2 o tmux estaban mal configurados.

**Causa verificada:** el pane ejecutaba `opencode run --continue`. `run` acepta
el mensaje en el comando y no conserva `Ask anything`; el emulador sólo renderiza
la salida recibida.

**Corrección aplicada:** la guía declara el modo interactivo como opción
recomendada cuando el humano desea conversar y proporciona el comando TUI sin
`run`, además del patrón AppleScript para iTerm2.

**Estado:** cerrado.

### F10 — HIGH — recuperación podía conservar el bloqueo del contexto previo

**Problema:** reanudar siempre con `--continue` después de un subagente colgado
podía heredar la misma conversación y volver a esperar el estado roto.

**Corrección aplicada:** para una revisión adversarial fresca se crea una
tarjeta de intento nueva y se inicia `opencode --auto --model ...` sin
`--continue`. Los artefactos se preservan en el worktree, mientras el nuevo
agente revalida el informe desde archivos y código.

**Estado:** cerrado.

### Evidencia de issue #60

- el one-shot fue interrumpido después de más de una hora sin cambios en el
  informe ni proceso hijo observable;
- el pane volvió a `zsh`, conservando el único informe rastreable;
- se inició `opencode --auto --model zhipuai-coding-plan/glm-5.2` sin
  `--continue` en el mismo pane tmux;
- una captura única mostró `Ask anything` antes de inyectar la tarjeta;
- texto literal y `Enter` separados hicieron aparecer la tarjeta y `Thinking`;
- iTerm2 se adjuntó después a la sesión viva sin reiniciar OpenCode;
- el humano y Codex conservaron control del mismo pane `%177`, con la regla de
  no escribir simultáneamente.

### Decisión

`proceed`

Para trabajo observado o colaborativo en macOS, la combinación validada es:
TUI OpenCode persistente + tmux + iTerm2 + readiness `Ask anything`. El modo
one-shot permanece apropiado para entrega automática sin conversación.

## Decisión final

`proceed`

La guía es apta para un piloto en proyectos de software: ambas ventanas son
visibles, OpenCode despierta obligatoriamente a Codex, Codex no hace polling y
los reintentos ya relanzan correctamente el ejecutor.
