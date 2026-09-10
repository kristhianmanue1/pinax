# 01 — Arquitectura y roles

## Topología

```text
Usuario
  │ intención, prioridad, permisos, PR y merge
  ▼
Codex Desktop externo
  │ arranque y comprobación inicial; luego se retira
  ▼
Codex CLI orquestador (tmux + iTerm2)
  │ tarjeta, sesión hija, espera y auditoría
  ▼
OpenCode ejecutor (tmux + iTerm2)
  │ implementación/análisis, adversarial, FIN y señal
  └──────────────────────────────► Codex CLI despierta
```

## Usuario

- Define intención y prioridad.
- Autoriza operaciones que cambian autoridad o estado externo.
- Conserva responsabilidad exclusiva sobre PR y merge.
- Puede observar ambas ventanas y despertar/interrumpir manualmente.

## Codex Desktop externo

- Lanza al Codex CLI con el contexto mínimo suficiente.
- Verifica que Codex realmente lanzó OpenCode y que ambas ventanas son visibles.
- Después queda fuera del ciclo para no competir por el worktree ni consumir
  turnos de espera.
- Sólo vuelve a intervenir cuando el usuario lo solicita.

## Codex CLI orquestador

- Lee fuentes canónicas, estado Git, dependencias, bloqueos y autorizaciones.
- Selecciona una tarea que el plan permita; no inventa excepciones.
- Materializa la tarjeta y fija task/run/attempt, alcance, DoD y paradas.
- Crea la sesión OpenCode y conoce su nombre, pane, ventana y canal wake-up.
- Se bloquea en una espera por evento.
- Al despertar captura la TUI, reproduce evidencia y adjudica el resultado.
- No acepta `FIN DONE` como verificación automática.

## OpenCode ejecutor

- Lee la tarjeta y sólo las referencias indicadas.
- Trabaja dentro de rutas y comandos autorizados.
- Ejecuta checks y adversarial propio.
- Registra límites y eventos sticky.
- Emite `FIN` antes de señalar el canal.
- Nunca se autoasigna `VERIFIED` ni amplía permisos.

## Separación de responsabilidades

| Acción | Usuario | Desktop externo | Codex CLI | OpenCode |
|---|---:|---:|---:|---:|
| Prioridad/autorización | dueño | transmite | verifica | consume |
| Materializar tarjeta | revisa | no | dueño | lee |
| Ejecutar | observa | no | coordina | dueño |
| Adversarial propio | no | no | exige | ejecuta |
| Auditoría independiente | decide excepciones | opcional a petición | dueño | no |
| Commit local autorizado | autoriza política | no | valida | ejecuta si tarjeta |
| Push | autorización nueva | no | no por defecto | no |
| PR/merge | dueño | no | no | no |

