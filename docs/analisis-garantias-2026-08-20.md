# Análisis — qué herramienta debe garantizar qué (2026-08-20)

**Pregunta del dueño:** lo que Pinax improvisó hoy (REANUDAR.md, política
local, guía local, tabla de herramientas) es temporal — solución a *mi*
problema de sesión. ¿Qué herramienta del ecosistema debe garantizar cada
pieza, para mí y para los demás agentes de proyectos?

**Regla de lectura:** vocabulario de clases de garantía de ektel
(`enforced` / `reactive` / `observed` / `unsupported`) y regla 1 de Pinax
(autodeclaración no es verificación).

## Mapa pieza → garante canónico

| Pieza improvisada hoy | Garante que debe absorberla | Hoy | Madurez del garante |
|---|---|---|---|
| `REANUDAR.md` (contexto entre sesiones) | **AN-KLA** — checkpoint + resume gobernados | Duplicado a propósito: el checkpoint v2 ya lo contiene; REANUDAR es puente hasta que el hábito de arranque sea universal | beta.15, funcional y adoptado en 5 repos |
| Política de agentes local (`docs/politica-agentes-pinax.md`) | **praxis-dev** — gobernanza ejecutable: autoridad, plan/apply, evidencia, perfiles de aseguramiento | Copia local del patrón de escrubery; cuando praxis-dev madure, las políticas por repo se generan/verifican contra el estándar, no se improvisan | `0.1.0-draft.1` — sin adoptantes; pinax sería el primero |
| Encargos obligatorios (task-cards) | **epistates** — contrato + preflight + evidencia rag/v1 | Ya adoptado hoy: 2 task-cards VALID | alpha `0.1.0a1`, validador read-only funcional |
| Evidencia de rondas (actas firmadas) | **argos** — claims content-addressed, evidencia L0–L5, attestations | Hoy son Markdown firmado "en palabra"; con argos serían claims con fingerprint verificable | `0.2.0rc2`, sin CLI estable |
| Descubrimiento de herramientas (tabla de REANUDAR) | **Pinax mismo** — el manifiesto puede declarar `descubrimiento.argv` y el mapa lo publica como claim verificable | La tabla vive en un doc temporal; debería ser dato del mapa | Campo aditivo incorporado como argv estructurado; Pinax no lo ejecuta |
| Método de construcción | **skevi** — F0→F3, ADRs, rondas | Ya adoptado por referencia en skopos | maduro, en uso real |
| Verdad sobre CLIs/modelos | **escrubery** — fichas con procedencia | Canal instruido para skopos (REQ-10); falta ejercitar | Fase 0 funcional |
| Protocolo de ronda adversarial | **proteinomenos** — independencia, procedencia, "primero fallos" | Lo apliqué informal hoy; debería ser el protocolo citado, no reinventado | documento de misión, sin tooling |
| **Que el agente no pueda violar el contrato** | **ektel + propylon** — admisión autorizada (`enforced`), capacidad validada en el punto de ingreso | **No existe.** Todo lo demás es `reactive`: detecto y rechazo después | ektel: a un acto del dueño (v1.2 + M0); propylon: sin código |

## La conclusión incómoda

Hoy construí la **capa reactive completa** (contratos, evidencia, memoria
verificada, política) usando las herramientas correctas en modo puente.
Pero la cadena de garantía del ecosistema tiene exactamente un eslabón
`enforced` y está vacío: **ektel**. Hasta que exista:

- un agente puede ignorar su task-card y yo sólo puedo *no aceptar* su
  reporte;
- un agente puede no leer REANUDAR.md y no pasa nada;
- mi propia disciplina de `verify` al arrancar es autoimpuesta.

Todo eso se declara así en la tabla — no se vende como más de lo que es.

## Acciones registradas

1. `REANUDAR.md` se retira cuando AN-KLA contiene un checkpoint vigente. El
   mapa no absorbe estado dinámico; `descubrimiento` sólo publica la interfaz
   estática autodeclarada.
2. `politica-agentes-pinax.md` es candidata a perfil de praxis-dev cuando
   el draft lo admita; retroalimentación de primer adoptante registrada.
3. Las actas de rondas futuras deberían emitirse como claims de argos,
   no sólo Markdown firmado.
4. Nada de esto elimina el bloqueo principal: consenso de v1.2 + M0 de
   ektel (dueño).
