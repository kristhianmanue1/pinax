# 05 — Evidencia del piloto 2026-08-13

## Versiones observadas

- Codex CLI `0.147.0`.
- OpenCode `1.18.18`.

## Instancia

| Elemento | Valor observado |
|---|---|
| Sesión Codex | `emd-codex-orchestrator-20260813-01` |
| Ventana Codex | iTerm2 `85198` |
| Sesión OpenCode | `emd-opencode-qa-01-preflight-20260813-01` |
| Ventana OpenCode | iTerm2 `85212` |
| Tarea | `QA-01-PREFLIGHT` read-only |
| Wake-up | `emd-qa01-preflight-20260813-01-finished` |

Tarjeta observada:

```text
docs/roadmap/agentic/orchestration/runs/20260813/qa-01-preflight/
qa-01-preflight-20260813-01-attempt-1.md
```

## Hechos confirmados

- Codex leyó autoridad y bloqueos.
- Seleccionó un preflight sin mutación de producto.
- Materializó una tarjeta v0.
- Creó la sesión OpenCode hija.
- Abrió y verificó la ventana iTerm2.
- Confirmó `opencode`, pane vivo y `session_attached=1`.
- Informó task/run, sesiones y canal de wake-up.
- Envió el prompt y después `Enter`.
- OpenCode pasó a estado `Thinking`.

## Hechos aún no confirmados al corte

- que Codex entró efectivamente en `tmux wait-for`;
- que OpenCode emitió `FIN` antes de la señal;
- que la señal despertó a Codex;
- que Codex auditó sin ayuda de Codex Desktop;
- que continuó el plan después de auditar.

## Incidencias útiles

1. El primer envío largo a Codex quedó como contenido pegado hasta recibir un
   `Enter` adicional.
2. Codex intentó inicialmente controlar iTerm2 mediante una habilidad que no lo
   permitía; recurrió a automatización local aprobada y verificó la ventana.
3. La existencia de la TUI OpenCode no bastó: se comprobó `Thinking` para
   confirmar trabajo real.

## Interpretación

El tramo de lanzamiento visible quedó demostrado. El ciclo completo sólo se
considerará validado después de observar wake-up y auditoría independiente.

