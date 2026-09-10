# 03 — Visibilidad, estados y recuperación

## Evidencia por nivel

| Observación | Lo que demuestra | Lo que no demuestra |
|---|---|---|
| sesión tmux existe | recuperabilidad | ventana visible o trabajo |
| pane vivo | proceso no terminó | prompt enviado |
| proceso Codex/OpenCode | TUI activa | tarea ejecutándose |
| `session_attached=1` | cliente terminal conectado | ventana correcta sin ID |
| ventana iTerm2 identificada | visibilidad humana | ejecución |
| texto en composer | prompt pegado | envío |
| `Thinking`/tools | ejecución iniciada | éxito |
| `FIN` | afirmación del ejecutor | verificación |
| wake-up recibido | final notificable | corrección del resultado |

## Comprobación mínima de ventana

- nombre exacto de sesión;
- pane ID;
- comando actual;
- `pane_dead=0`;
- `session_attached=1`;
- ID de ventana iTerm2;
- captura breve sin secretos.

Una sesión con `attached=0` sigue siendo recuperable, pero no debe reportarse
como visible.

## Recuperación manual

Si iTerm2 se cierra y tmux continúa:

```text
tmux attach-session -t <sesion>
```

Si Codex está esperando y OpenCode terminó sin señal:

1. revisar visualmente/capturar la TUI;
2. confirmar `FIN` y task/run/attempt;
3. señalar manualmente el canal sólo con autorización del usuario;
4. registrar que el wake-up automático falló.

Si OpenCode sigue en `Thinking` sin progreso verificable, el usuario puede
interrumpir desde su ventana. No lanzar otro escritor sobre el mismo worktree.

## Regla de intervención humana

El usuario puede escribir en una TUI, pero debe avisar al controlador para no
producir entrada simultánea. Una frase escrita en la ventana no modifica por sí
sola la tarjeta ni amplía alcance.

## Retención

- Conservar sesiones hasta terminar auditoría/correcciones.
- No confundir una TUI histórica viva con un agente activo.
- Cerrar sesiones completadas cuando ya no sean necesarias, sin borrar recibos
  ni evidencia.

