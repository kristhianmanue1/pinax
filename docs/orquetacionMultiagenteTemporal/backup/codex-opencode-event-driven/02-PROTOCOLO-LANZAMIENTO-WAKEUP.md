# 02 — Protocolo de lanzamiento y wake-up

## Lanzamiento de Codex

1. Crear sesión tmux única.
2. Iniciar Codex CLI en el worktree exacto con sandbox `workspace-write` y
   revisión automática de aprobaciones.
3. No usar bypass que elimine sandbox/aprobaciones.
4. Abrir una ventana iTerm2 adjunta a la sesión.
5. Verificar sesión, pane, proceso, terminal adjunta y ventana.
6. Entregar contexto y mandato de orquestación.
7. Enviar texto y `Enter` por separado.

## Lanzamiento de OpenCode por Codex

1. Crear un nombre que incluya proyecto, task y run.
2. Crear sesión tmux en el worktree autorizado.
3. Iniciar OpenCode TUI conversacional.
4. Abrir ventana iTerm2 y adjuntar exactamente esa sesión.
5. Verificar:
   - `pane_dead=0`;
   - `pane_current_command=opencode`;
   - `session_attached=1`;
   - ventana iTerm2 identificada.
6. Enviar referencia absoluta a la tarjeta con `send-keys -l`.
7. Enviar `Enter` en una segunda acción.
8. Capturar una muestra corta que demuestre lectura/`Thinking`.

## Canal de evento

El canal debe ser único:

```text
emd-<task>-<run>-finished
```

OpenCode cierra en este orden:

```text
FIN <DONE|BLOCKED|FAILED> task=... run=... attempt=...
tmux wait-for -S <canal>
```

Codex espera:

```text
tmux wait-for <canal>
```

No hay polling, sleeps repetidos ni lectura constante de la TUI. La espera
retorna cuando OpenCode señala el canal.

## Al despertar

Codex debe:

1. capturar la salida final;
2. comprobar task/run/attempt y orden `FIN`→señal;
3. verificar HEAD/rama/worktree y drift;
4. inspeccionar alcance completo;
5. reproducir checks y hashes;
6. revisar eventos sticky;
7. adjudicar `VERIFIED`, `CORRECTION_REQUIRED` o `BLOCKED`;
8. continuar sólo si la siguiente dependencia está satisfecha.

## Fallos de protocolo

- Prompt pegado sin `Enter`: OpenCode no está trabajando.
- Señal antes de `FIN`: evento inválido; auditar como fallo.
- Señal duplicada/reutilizada: riesgo de despertar el run equivocado.
- OpenCode termina sin señal: el usuario puede despertar manualmente a Codex.
- Codex despierta pero no reproduce evidencia: no existe verificación.

