# REANUDAR — Pinax (actualizado 2026-08-20 ~20:45, cierre por límite de tokens)

## Quién eres

Eres **Pinax** (Kimi/kimi-k2), catálogo y orquestador del ecosistema aria.
Directorio: `/Users/krisnova/www/pinax`. Lee `AGENTS.md` primero (reglas del
proyecto) y `docs/guia-an-kla-pinax.md` cuando vayas a tocar memoria AN-KLA
(flujo dominado, con lecciones aprendidas en vivo).

## Protocolo de arranque (obligatorio)

```bash
cd /Users/krisnova/www/pinax
.venv/bin/python -m an_kla --project-root . context status   # diagnostics == []
.venv/bin/python -m an_kla --project-root . verify           # si falla: NO operar
.venv/bin/python -m an_kla --project-root . checkpoint show  # working state completo
```

Memoria: AN-KLA beta.16 instalada (0.1.0b16); checkpoint ligado a Git
(`git/v1`); 18+ eventos del día asentados. Escritura SIEMPRE vía
`plan-write` → `commit-write-plan` (guía tiene las claves exactas y trampas).

## Estado del ecosistema (snapshot 2026-08-20 ~20:45)

### skopos — `/Users/krisnova/www/aria/skopos`
- Ciclo de 7 fases: **0,1,2,3(a),4,6 cerradas**; rondas 0–8 con actas;
  102/102 verde. Decisiones firmadas: C-9, C-8 (ADR-007 B), C-10 (ADR-008:
  watch desde-ahora + --backfill), C-6 (ADR-009: P4a sello fragmento-only +
  P5 presupuesto + P3 marca no-instrucción).
- **EN CURSO: Fase 5 (C-5)** — piloto sesión única acotada + detector de eco.
  Timeout del piloto: **300 s vía parámetro existente + fallos como dato**
  (decisión del dueño). Restricción Pinax: ya honrada (sello antes de ingesta).
- Después: **Fase 7** — contrato de parser por CLI (abre multi-CLI: claude,
  kimi, qwen...). Gated tras Fases 1–6.
- Cuando entregue el reporte del piloto: revisión de cierre de Pinax y
  actualizar MAPA.md del ecosistema (ofrecido al dueño).

### ektel — `/Users/krisnova/www/aria/ektel`
- **M0 NO cerrado.** Rondas externas (Codex+Claude, lanzadas por Pinax):
  NO-GO doble. Logs y síntesis: `pinax/rondas/2026-08-20-m0-ektel-externas/`.
- **ADR-010 firmado (alternativa a)**: rechazar base64url no canónico (bits
  residuales en cero, verificado re-codificando). H1/H2 reproducidos por Pinax.
- **EN CURSO**: paquete de correcciones (parsers A/B, schemas oneOf,
  vocabulario admisión, enmiendas spec §8.3/§6.6/§6.8/§5.5/§5.1, corpus
  ampliado). Instrucción completa: `instruccion-agente-ektel-correccion-m0.md`.
- **Gate de salida**: ronda propia + re-verificación externa con Codex Y
  Claude sobre el diff. **Pinax las lanza** (flujo ya probado; ver abajo).

### an-kla — `/Users/krisnova/www/an-kla-memory`
- #67 cerrado como límite documentado; #45 mergeado (PR #90).
- **EN CURSO: #68 (inventario)** en rama `feat/issue-68-inventario` — fixes
  H1 (catálogo-primero) + H2 (**decisión: bucket `eliminada` en schema+counts,
  invariante intacta**) + H3 → re-ronda → PR → release **beta.17**.
- Al publicar beta.17: avisan a pinax → actualizar .venv de pinax (con gate
  de upgrade beta.16→17 como evidencia). Será la primera prueba real de #45
  con el AGENTS.md de pinax.
- Después (sin prisa): #46 (export sellado, decisión B vs D), G2–G4.

### agora — `/Users/krisnova/www/aria/agora`
- Decisión del dueño: **fundación simple, sin CAGF ni ektel**.
- Encargo LISTO pero **NO ENVIADO** (diferido por el dueño): archivos en
  `pinax/rondas/2026-08-20-vision-skopos-ektel/` — `instruccion-agente-agora.md`
  + `task-card-agora.json` (VALID, epistates; ojo: catálogo check_id cerrado:
  git_status/diff_check/unit_tests). Esperando orden del dueño para enviar.

### propylon / proteinomenos (analizados, sin acción)
- propylon: solo README. NO construir hasta que ektel tenga tráfico real.
  Su manifiesto futuro debe declarar `no_ofrece` (no es parada completa).
- proteinomenos: paper anti-confirmación; única acción legítima pendiente =
  **escribir el prerregistro de Fase −1**. Su CapabilityMap futuro debe LEER
  de pinax, no construirse aparte.

## Cómo lanzar rondas externas (Codex/Claude) — dominado hoy

- Codex: `cd <repo> && codex exec --sandbox read-only "<prompt>"` — una
  corrida completa cabe en 300 s si el prompt pide una sola respuesta.
- Claude: `claude -p "<prompt>"` — **bufferiza y se muere a los 300 s** si la
  tarea es grande: trocear por frentes (probado: 1-2, 4, 5 por separado).
- Auth claude: el token OAuth expira; si dice "Not logged in",
  `security find-generic-password -s "Claude Code-credentials" -w >
  ~/.claude/.credentials.json && chmod 600` lo revive (hecho hoy).
- Verificación de hallazgos: Pinax SIEMPRE reproduce los bloqueantes con sus
  propias manos (python3 contra los parsers) antes de aceptarlos.

## Método Pinax (lo que hice todo el día)

1. Verificar contra código/git/tests, nunca contra README o reporte solo.
2. Toda métrica fechada como snapshot.
3. Decisión primero, código después; ronda adversarial pre y post.
4. Commits/push/instalaciones: autorización del dueño POR OPERACIÓN.
5. Todo evento relevante se asienta en AN-KLA (trazabilidad del día completa).
6. Respuestas al dueño en español, con texto listo para pegar a cada agente.

## Commits propios de hoy en pinax

`6645100` (guía AN-KLA lecciones 5-6), `87e1cd1` (guía beta.16 + encargo
agora). Pendiente de commit si procede: este REANUDAR.md actualizado.
