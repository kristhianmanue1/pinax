# 06 — Checklists y criterio de adopción

## Antes de lanzar Codex

- [ ] Usuario autorizó tarea o lote.
- [ ] Fuentes canónicas y bloqueos identificados.
- [ ] Worktree y escritores concurrentes comprobados.
- [ ] Sandbox `workspace-write`; sin bypass peligroso.
- [ ] Sesión Codex única creada.
- [ ] Ventana Codex visible y adjunta.

## Antes de enviar la tarjeta a OpenCode

- [ ] Task/run/attempt únicos.
- [ ] Objetivo único y dependencias satisfechas.
- [ ] Rutas de lectura/escritura exactas.
- [ ] Comandos y efectos autorizados.
- [ ] Paradas sticky.
- [ ] DoD reproducible.
- [ ] Canal wake-up único.
- [ ] Sesión OpenCode viva y ventana visible.

## Después de enviar

- [ ] Texto enviado con modo literal.
- [ ] `Enter` enviado por separado.
- [ ] TUI muestra lectura/`Thinking`.
- [ ] Codex informó sesiones, ventana, tarea y canal.
- [ ] Codex entró en espera por evento, sin polling.

## Al finalizar OpenCode

- [ ] `FIN` exacto visible.
- [ ] Señal emitida después de `FIN` y una sola vez.
- [ ] Codex despertó por la señal.
- [ ] Identidad y SHA coinciden.
- [ ] Scope/diff/staging reproducidos.
- [ ] Tests y hashes reproducidos.
- [ ] Eventos sticky revisados.
- [ ] Resultado adjudicado independientemente.

## Recuperación

- [ ] Si iTerm cerró, tmux continúa y puede adjuntarse.
- [ ] Si faltó señal, intervención manual queda registrada.
- [ ] Si un pane murió, no se relanza sobre el mismo run sin auditoría.
- [ ] Dos intentos fallidos producen diagnóstico, no tercero ciego.

## Criterio de adopción canónica

Adoptar sólo después de una ejecución completa demostrada:

```text
launch Codex
→ launch OpenCode visible
→ ejecución
→ adversarial
→ FIN
→ señal
→ wake-up Codex
→ auditoría independiente
→ siguiente decisión
```

Además:

- cero polling durante la ejecución;
- cero permisos concedidos por memoria o logs;
- cero escritura fuera de tarjeta;
- recovery probado;
- commits exactos probados en worktree aislado;
- PR/merge continúan bajo control humano.

Hasta cumplirlo, mantener estos documentos como referencia no autoritativa.

