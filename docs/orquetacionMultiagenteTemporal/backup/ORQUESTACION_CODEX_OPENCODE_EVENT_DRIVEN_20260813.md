# Codex → OpenCode por eventos — índice ejecutivo

**Fecha:** 2026-08-13  
**Estado:** referencia para análisis posterior; no es política canónica ni
concede permisos.

## Objetivo

Codex CLI sustituye temporalmente al controlador interactivo, lanza un OpenCode
visible, conoce su TUI/sesión, espera sin polling y despierta cuando OpenCode
emite `FIN` y señala un canal `tmux wait-for`.

```text
Usuario → Codex Desktop externo → Codex CLI orquestador
                                      ↓
                               OpenCode ejecutor
                                      ↓ FIN + señal
                               Codex despierta y audita
```

## Reglas esenciales

- Codex y OpenCode viven en sesiones tmux distintas y ventanas iTerm2 visibles.
- Una sesión existente no prueba visibilidad; se exige pane vivo,
  `session_attached=1` y ventana identificada.
- Prompt y `Enter` se envían por separado; `Thinking` confirma inicio real.
- OpenCode señala un canal único después de `FIN`; Codex espera ese canal sin
  polling y luego audita independientemente.
- OpenCode puede hacer commits locales sólo si la tarjeta lo autoriza y limita
  staging a rutas exactas. No push; PR y merge pertenecen al usuario.
- No validar seguridad mediante denylist creciente de strings Git: usar `argv`
  estructurado, allowlist exacta, construcción de comandos y sandbox.

## Documentos detallados

1. [Arquitectura y roles](codex-opencode-event-driven/01-ARQUITECTURA-Y-ROLES.md)
2. [Protocolo de lanzamiento y wake-up](codex-opencode-event-driven/02-PROTOCOLO-LANZAMIENTO-WAKEUP.md)
3. [Visibilidad, estados y recuperación](codex-opencode-event-driven/03-VISIBILIDAD-ESTADOS-RECUPERACION.md)
4. [Permisos Git y evasiones](codex-opencode-event-driven/04-PERMISOS-GIT-Y-EVASIONES.md)
5. [Evidencia del piloto](codex-opencode-event-driven/05-EVIDENCIA-PILOTO-20260813.md)
6. [Checklists y criterio de adopción](codex-opencode-event-driven/06-CHECKLISTS-Y-ADOPCION.md)

La navegación completa está en
[README](codex-opencode-event-driven/README.md).

