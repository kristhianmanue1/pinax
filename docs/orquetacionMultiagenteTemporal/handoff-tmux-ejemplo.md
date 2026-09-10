# Handoff tmux opcional — piloto-tmux-docs

Este archivo transporta datos efímeros. No es una tarjeta, una fuente de verdad
ni una concesión de autoridad. Si contradice la tarjeta canónica o `AGENTS.md`,
prevalece la regla más restrictiva y la tarea se detiene.

- Tarjeta canónica: `task-card-v1-ejemplo.json`
- SHA-256 de la tarjeta: `<calcular sobre el archivo materializado>`
- Run: `piloto-tmux-docs-20260821-01`
- Intento: `1`
- Topología: `T1` — única durante este intento
- Socket tmux dedicado: `/private/tmp/proyecto-agent-tmux-piloto-tmux-docs-20260821-01/tmux.sock`
- Directorio del socket: modo `0700`; no exponer el servidor tmux general
- Sesión Controlador: `proyecto-codex-piloto`
- Ventana primaria Controlador: `controlador` — siempre visible y seleccionada
- Pane Controlador: `%<controller-pane-id>`
- Sesión Ejecutor: `proyecto-opencode-piloto`
- Pane Ejecutor: `%<executor-pane-id>`
- Perfil Controlador: `--approve-for-me` (implica `workspace-write`); `--add-dir`
  limitado al directorio del socket; preflight tmux real aprobado
- Perfil Ejecutor: observado, permisos de lectura/edición/checks dentro del
  worktree
- OpenCode: `1.18.21`
- `--auto`: `no autorizado / ausente`
- Reporte: `docs/piloto/reporte-rag.md`
- Adversarial: `docs/piloto/reporte-adversarial.md`
- Secuencia obligatoria: autocorrección → revisión fresca → fix-and-retry hasta
  `PROCEED` → `AGENT_DONE` → auditoría final del Controlador
- Revisor fresco: no participó en la implementación y no recibe el transcript;
  para un cambio crítico debe usar otro proveedor y otro modelo
- Actor designado del commit: `Controlador`
- Autoridad actual del commit: `concedida_al_controlador_post_gates_para_este_intento`
- Push, PR, merge, tag y release: `no autorizados`

Mensaje de cierre exacto:

```text
AGENT_DONE task=piloto-tmux-docs run=piloto-tmux-docs-20260821-01 attempt=1 report=docs/piloto/reporte-rag.md adversarial=docs/piloto/reporte-adversarial.md
```
